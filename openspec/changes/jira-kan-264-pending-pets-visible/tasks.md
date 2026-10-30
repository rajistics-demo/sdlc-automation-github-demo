# Tasks

- [x] Create OpenSpec-style change artifacts (proposal, design, spec delta, tasks)
- [x] Reproduce the bug with empty status parameter
- [ ] Validate OpenSpec artifacts with validation script
- [ ] Implement the one-line fix in catalog.py
- [ ] Add regression tests for empty status scenarios
- [ ] Run catalog tests to verify fix
- [ ] Run full test suite
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with evidence waypoints
- [ ] Add openhands-review label for code review handoff

## Evidence Checklist

- [x] **Stop 1 - Ticket**: Jira issue KAN-264 reports customers seeing unavailable pets
- [x] **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` defines the rule: default search must show only available pets, Nova is pet-103 with status=pending
- [x] **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows PENDING_PET_VISIBLE error code with pet-103 visible to customers
- [x] **Stop 4 - Repo/Files**: Bug found in `app/petstore_app/catalog.py` line 50 where empty status bypasses filter due to truthiness check
- [ ] **Stop 5 - Tests/PR**: Regression tests added, all tests pass, draft PR opened
