# Tasks

- [x] Create OpenSpec-style change artifacts
  - [x] proposal.md with evidence waypoints
  - [x] specs/catalog-availability/spec.md with acceptance scenarios
  - [x] design.md with implementation approach
  - [x] tasks.md (this file)
- [x] Validate OpenSpec artifacts
- [x] Add regression tests that fail before fix
  - [x] test_search_pets_filters_empty_status_to_available
  - [x] test_search_pets_filters_empty_status_with_species  
  - [x] test_search_pets_default_status_excludes_pending
- [x] Verify tests fail with current code
- [x] Implement the fix: normalize empty status to "available"
- [x] Verify all tests pass after fix
- [x] Run full test suite validation
- [ ] Open draft PR with evidence and validation results
- [ ] Add openhands-review label
- [ ] Post Jira comment with PR link and status

## Validation Results

✅ All tests pass (8/8 in test_pet_catalog.py, 12/12 in app/tests/)

**New tests added:**
1. `test_search_pets_filters_empty_status_to_available` - Verifies empty status filters to available only
2. `test_search_pets_filters_empty_status_with_species` - Verifies empty status works with species filter
3. `test_search_pets_default_status_excludes_pending` - Documents default behavior excludes pending pets

**Regression verification:**
- Existing tests continue to pass
- Explicit `status="pending"` requests still work correctly
- Species and tag filtering unchanged

## Human Approvals

- Scope: Pending
- Code review: Pending (openhands-review will trigger)
- Merge: Pending
- Deployment: Pending
