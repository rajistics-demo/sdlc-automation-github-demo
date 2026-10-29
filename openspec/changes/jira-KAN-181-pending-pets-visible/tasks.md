# Tasks

- [x] Review Jira issue KAN-181 and gather requirements
- [x] Investigate wiki docs for catalog availability rules
- [x] Check logs for `PENDING_PET_VISIBLE` evidence
- [x] Examine `app/petstore_app/catalog.py` for bug location
- [x] Identify test coverage gaps in `app/tests/test_pet_catalog.py`
- [x] Create OpenSpec-style change artifacts
- [x] Validate OpenSpec folder structure
- [ ] Fix status filter condition in `catalog.py` line 50
- [ ] Add regression test: `test_search_pets_default_excludes_pending()`
- [ ] Add edge case test: `test_search_pets_empty_status_does_not_bypass_filter()`
- [ ] Add specific test: `test_search_pets_excludes_nova_from_default()`
- [ ] Run all catalog tests to verify fix and no regressions
- [ ] Create feature branch with naming convention
- [ ] Commit changes with clear message
- [ ] Push branch to remote
- [ ] Open draft PR with evidence waypoints and human gates
- [ ] Add `openhands-review` label to trigger code review workflow
- [ ] Post summary comment to Jira KAN-181 with PR link
