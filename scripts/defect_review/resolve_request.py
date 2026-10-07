#!/usr/bin/env python3
"""Resolve a Jira repository-review request without network access."""
import argparse
import json
import re
from urllib.parse import urlsplit

ALLOWED = {"rajistics-demo/petstore-defect-demo", "rajistics-demo/billing-defect-demo"}

def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(text(v) for v in value)
    if isinstance(value, dict):
        return "\n".join([str(value.get("text", "")), text(value.get("content", []))])
    return ""

def resolve(event):
    if isinstance(event.get("payload"), dict):
        event = event["payload"]
    issue = event.get("issue", {})
    fields = issue.get("fields", {})
    key = issue.get("key", "")
    if not re.fullmatch(r"[A-Z][A-Z0-9_]*-\d+", key):
        raise ValueError("a real or rehearsal Jira issue key is required")
    body = text(fields.get("description", ""))
    urls = re.findall(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?", body)
    slugs = {urlsplit(u).path.strip("/").removesuffix(".git") for u in urls}
    if len(slugs) != 1 or not slugs <= ALLOWED:
        raise ValueError("ticket must name exactly one allowlisted demo repository")
    ref_match = re.search(r"(?im)^\s*Ref:\s*([A-Za-z0-9_./-]+)\s*$", body)
    if re.search(r"(?im)^\s*Ref:", body) and not ref_match:
        raise ValueError("invalid ref")
    ref = ref_match.group(1) if ref_match else "main"
    if ref.startswith("-") or ".." in ref or "//" in ref or ref.endswith("/"):
        raise ValueError("invalid ref")
    scope_match = re.search(r"(?im)^\s*Scope:\s*(.+)$", body)
    mode_match = re.search(r"(?im)^\s*Mode:\s*(review-only|review-and-repair)\s*$", body)
    if not mode_match:
        raise ValueError("Mode must explicitly be review-only or review-and-repair")
    return {"issue_key": key, "repository": next(iter(slugs)), "ref": ref,
            "scope": scope_match.group(1).strip() if scope_match else "product contract",
            "mode": mode_match.group(1), "title": fields.get("summary", "")}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    args = parser.parse_args()
    with open(args.event) as source:
        print(json.dumps(resolve(json.load(source)), indent=2))
