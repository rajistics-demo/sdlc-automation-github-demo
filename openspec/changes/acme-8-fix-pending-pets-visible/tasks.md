# Tasks: Fix Pending Pets Visible in Search

**Source Issue:** [ACME-8](https://rajiv-shah.atlassian.net/browse/ACME-8)

## Implementation Tasks

- [x] **Stop 1 - Ticket:** Read issue ACME-8 and understand the business impact
- [x] **Stop 2 - Wiki/Docs:** Review `docs/repo-memory/petstore-intelligence.md` for product rules
- [x] **Stop 3 - Logs:** No logs provided; issue is behavioral (customers seeing wrong pets)
- [x] **Stop 4 - Repo/Files:** Located bug in `app/petstore_app/catalog.py` line 50
- [x] **Stop 5 - Reproduce:** Created reproduction test showing `status=""` returns pending pets
- [x] Create OpenSpec artifacts (proposal, design, tasks, spec delta)
- [x] Validate OpenSpec artifacts with validation script
- [x] Fix the status filter logic in `catalog.py`
- [x] Add regression test for empty status parameter
- [x] Run existing tests to ensure no breakage
- [x] Verify adoption flow still blocks pending pets (existing behavior)
- [x] **Stop 5 - Tests/PR:** All tests pass, ready to open draft PR

## Validation Results

- **Backend Tests:** ✅ PASSED - `pytest -q app/tests/test_pet_catalog.py` - 7 tests passed
- **All Tests:** ✅ PASSED - `pytest -q app/tests/` - 11 tests passed
- **Reproduction:** ✅ VERIFIED - `search_pets(status="")` now returns 0 pets (was 4 including pending)
- **UI Smoke:** Not applicable - bug is backend-only, UI already filters correctly

## Human Review Gates

- [ ] **Code Review:** Verify fix logic and test coverage
- [ ] **QA Approval:** Confirm no pending pets appear in default searches
- [ ] **Deployment Approval:** Authorize promotion to production
