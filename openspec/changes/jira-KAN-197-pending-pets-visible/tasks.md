# Tasks

- [ ] Create OpenSpec-style change artifacts (proposal, spec delta, design, tasks)
- [ ] Validate change artifacts with `validate_open_spec.py`
- [ ] Fix the status filter guard in `app/petstore_app/catalog.py` line 50
- [ ] Add regression test `test_search_pets_empty_status_does_not_bypass_filter` in `app/tests/test_pet_catalog.py`
- [ ] Run existing catalog tests to verify no regressions
- [ ] Run new test to verify the fix works
- [ ] Document evidence waypoints in PR body
- [ ] Open draft PR with OpenSpec change path and validation results
- [ ] Add `openhands-review` label to trigger code review workflow
