# Publish one authorized review comment

Prepare the reviewed body in a file with the actual `$AUTOMATION_SESSION_URL`
expanded exactly once. Do not put placeholders in the body. Publication still
requires the active workflow's authorization for this PR and comment.

```bash
python3 scripts/automations/publish_review_comment.py \
  --repo <owner/repository> --pr <number> --body-file /tmp/review_body.md
```

The helper uses `GITHUB_TOKEN`, posts once, and verifies through GET requests.
Repeating the same command reconciles an existing comment instead of posting
again. A pending local receipt prevents another POST after an uncertain outcome.
It never edits or deletes an existing comment. If the body changed, multiple
matching comments exist, or the outcome cannot be reconciled, stop and report
that state. Do not fall back to a separate `gh pr comment` or POST request.

This is a review comment, not formal approval. Keep findings, evidence limits
and the configured QA handoff explicit.
