# Tasks

- [x] **Stop 1 - Ticket**: Read Jira KAN-243 and understand the sparse bug report.
- [x] **Stop 2 - Wiki/Docs**: Check `docs/wiki/petstore-catalog-availability.md` for availability rules.
- [x] **Stop 3 - Logs**: Review `docs/logs/pending-pet-visible.ndjson` for error evidence.
- [x] **Stop 4 - Repo/Files**: Analyze `app/petstore_app/catalog.py` and identify the root cause (empty status filter bypass).
- [x] Create OpenSpec-style change artifacts (proposal, design, spec, tasks).
- [x] Validate change artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py`.
- [ ] Fix status normalization in `catalog.py` to treat empty/whitespace status as `"available"`.
- [ ] Add regression test for empty status string edge case.
- [ ] Run all catalog tests to verify no regressions.
- [ ] **Stop 5 - Tests/PR**: Open draft PR with evidence waypoints, test results, and OpenSpec artifacts.
- [ ] Add `openhands-review` label to PR for code review handoff.
