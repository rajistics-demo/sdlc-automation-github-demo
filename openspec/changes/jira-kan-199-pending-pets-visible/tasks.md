# Tasks: Fix pending pets visibility

## Pre-Implementation
- [x] Read repository guidance (AGENTS.md, wiki, logs)
- [x] Review evidence waypoints (Jira issue, wiki, logs, code)
- [x] Create OpenSpec-style change artifacts

## Implementation
- [ ] Review frontend filter in `app/web/app.js`
- [ ] Verify status check exists and is correct
- [ ] Fix if needed: ensure `&& pet.status === "available"` is in filter
- [ ] Verify filter applies on page load and search

## Validation
- [ ] Run backend tests: `PYTHONPATH=app python3 -m pytest app/tests/ -v`
- [ ] Check if Playwright is available for UI testing
- [ ] Run UI smoke test if available, document limitation if not
- [ ] Verify Nova (pet-103) excluded from default view

## PR and Handoff
- [ ] Create feature branch for KAN-199
- [ ] Commit changes with descriptive message
- [ ] Push branch to origin
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-review` label to PR
- [ ] Post Jira comment with PR link

## Human Gates
- [ ] PR review approval
- [ ] Merge approval
- [ ] Deployment approval (outside automation scope)
