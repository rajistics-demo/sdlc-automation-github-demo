# Tasks

- [x] Review Jira issue KAN-246 and gather business context
- [x] Check wiki docs: `docs/wiki/petstore-catalog-availability.md`
- [x] Check log evidence: `docs/logs/pending-pet-visible.ndjson` confirms PENDING_PET_VISIBLE error
- [x] Identify root cause in `catalog.py` status filter logic
- [x] Create OpenSpec change artifacts (proposal, design, tasks, spec)
- [x] Validate OpenSpec artifacts with validation script
- [ ] Implement status validation in `catalog.py`
- [ ] Add test for empty status validation
- [ ] Run existing tests to ensure no regression
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-review` label for code review handoff
- [ ] Post Jira comment with PR link and conversation URL
