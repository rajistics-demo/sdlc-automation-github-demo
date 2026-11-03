# Tasks

- [x] Understand Jira issue KAN-270 and identify the bug
- [x] Check wiki docs and log evidence for business rules
- [x] Investigate catalog.py and identify root cause (line 50 empty-status bypass)
- [x] Create OpenSpec-style change artifacts (proposal, design, tasks, spec delta)
- [ ] Validate OpenSpec artifacts with validation script
- [ ] Implement the fix in catalog.py (default empty status to "available")
- [ ] Add regression tests for empty-status edge case and default pending exclusion
- [ ] Run focused catalog tests to verify fix
- [ ] Run full pytest suite to ensure no regressions
- [ ] Open draft PR with evidence waypoints and OpenSpec artifacts
- [ ] Add `openhands-review` label for review handoff
- [ ] Post Jira comment with status, PR link, and conversation link
