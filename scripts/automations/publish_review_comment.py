#!/usr/bin/env python3
"""Publish one authorized review; reconcile retries without duplicate POSTs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.parse import urlsplit


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def github_request(method, path, payload=None):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is missing")
    request = Request(
        "https://api.github.com" + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"}, method=method,
    )
    with build_opener(NoRedirects()).open(request, timeout=30) as response:
        return json.load(response)


def publish(repo, pr, body, session_url, receipt_dir, request=github_request):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or pr < 1:
        raise ValueError("Expected an owner/repository and positive PR number")
    url = urlsplit(session_url)
    if (url.scheme != "https" or not url.hostname or url.username or url.password
            or "/conversations/" not in url.path
            or any(c.isspace() for c in session_url)):
        raise ValueError("A real runtime conversation URL is required")
    if body.count(session_url) != 1 or re.search(
        r"<url>|PLACEHOLDER_URL|\$\{?AUTOMATION_SESSION_URL", body
    ):
        raise ValueError("Body must contain the real conversation URL once, without placeholders")
    marker = f"<!-- openhands-review {session_url} -->"
    rendered = body.rstrip() + "\n\n" + marker + "\n"
    endpoint = f"/repos/{repo}/issues/{pr}/comments"

    def existing():
        matches = []
        for page in range(1, 101):
            comments = request("GET", f"{endpoint}?per_page=100&page={page}")
            matches.extend(c for c in comments if session_url in c.get("body", ""))
            if len(comments) < 100:
                break
        else:
            raise RuntimeError("Comment history exceeded bounded reconciliation")
        if len(matches) > 1:
            raise RuntimeError("Multiple matching comments exist; no write attempted")
        if matches and matches[0]["body"].replace("\n\n" + marker, "").rstrip() != body.rstrip():
            raise RuntimeError("Existing review differs; no edit or new comment attempted")
        return matches[0] if matches else None

    found = existing()
    if found:
        return {"status": "existing_verified", "url": found["html_url"]}
    key = hashlib.sha256(f"{repo}/{pr}/{session_url}".encode()).hexdigest()
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipt_dir / (key + ".json")
    try:
        with receipt.open("x") as stream:
            json.dump({"status": "pending", "body_sha256": hashlib.sha256(rendered.encode()).hexdigest()}, stream)
    except FileExistsError:
        raise RuntimeError("Prior publication outcome unresolved; no POST attempted") from None
    # Any exception leaves the receipt pending. A later invocation first reads
    # GitHub and can reconcile a successful POST whose response was lost.
    request("POST", endpoint, {"body": rendered})
    found = existing()
    if not found:
        raise RuntimeError("Publication not verified; receipt remains pending")
    receipt.write_text(json.dumps({"status": "verified", "comment_id": found["id"]}))
    return {"status": "published_verified", "url": found["html_url"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--body-file", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = publish(args.repo, args.pr, args.body_file.read_text(),
                         os.environ.get("AUTOMATION_SESSION_URL", ""),
                         Path(tempfile.gettempdir()) / "openhands-review-receipts")
    except Exception as exc:
        # Do not print HTTP response bodies, headers, tokens or the comment body.
        detail = str(exc) if isinstance(exc, (ValueError, RuntimeError)) else type(exc).__name__
        parser.exit(1, f"Review publication stopped: {detail}\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
