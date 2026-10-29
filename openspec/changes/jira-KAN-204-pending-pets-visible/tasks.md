# Tasks: Fix Pending Pets Visibility

## Implementation Tasks

- [x] Stop 1 - Ticket: Reviewed Jira KAN-204 sparse issue
- [x] Stop 2 - Wiki/Docs: Checked `docs/wiki/petstore-catalog-availability.md` confirming Nova is pet-103 with status=pending
- [x] Stop 3 - Logs: Reviewed `docs/logs/pending-pet-visible.ndjson` showing PENDING_PET_VISIBLE error for pet-103
- [x] Stop 4 - Repo/Files: Analyzed `app/petstore_app/catalog.py` and found falsy check bug on line 50
- [x] Create OpenSpec-style change artifacts
- [x] Validate change artifacts with validation script
- [ ] Fix status filter in `catalog.py` line 50
- [ ] Add explicit test for pending pet exclusion
- [ ] Run backend tests
- [ ] Create branch and commit changes
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-review` label for review handoff

## Human Gates

- **Merge Approval**: Human reviewer must approve PR before merge
- **Production Deploy**: Human operator must approve deployment

## Validation Plan

1. Run `pytest app/tests/test_pet_catalog.py` to verify all tests pass
2. Verify new test explicitly checks Nova (pet-103) is excluded from default searches
3. Verify existing pending pet test still works
4. No UI testing needed - web filter is already correct
