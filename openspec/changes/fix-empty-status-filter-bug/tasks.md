# Tasks

## Evidence Waypoints

- [x] **Stop 1 - Ticket**: Jira issue KAN-263 - "Customers are seeing pets that are not available"
- [x] **Stop 2 - Wiki/Docs**: Reviewed `docs/wiki/petstore-catalog-availability.md` - confirms default search must show only available pets, Nova (pet-103) is pending
- [x] **Stop 3 - Logs**: Reviewed `docs/logs/pending-pet-visible.ndjson` - ERROR code PENDING_PET_VISIBLE indicates catalog availability regression
- [x] **Stop 4 - Repo/Files**: Identified bug in `app/petstore_app/catalog.py` line 50 - empty status bypasses filter
- [ ] **Stop 5 - Tests/PR**: Regression tests added, validation run, draft PR opened

## Implementation Tasks

- [x] Create OpenSpec-style change folder with proposal, spec delta, design, and tasks
- [x] Validate OpenSpec artifacts structure
- [x] Add regression test for empty status string
- [x] Add regression test for whitespace-only status string  
- [x] Fix the bug in catalog.py to default empty status to "available"
- [x] Run catalog tests to verify fix
- [x] Run full test suite (app tests pass, 1 unrelated test failure in context reporting)
- [x] Manual smoke tests for edge cases
- [ ] Open draft PR with evidence and validation results
- [ ] Add openhands-review label for code review handoff

## Validation Status

- [x] Unit tests pass: `python3 -m pytest -q app/tests/test_pet_catalog.py` ✓ (7/7 passed)
- [x] App test suite passes: `python3 -m pytest -q app/tests/` ✓ (11/11 passed)
- [x] Manual verification: `search_pets(status="")` returns only available pets ✓
- [x] Manual verification: `search_pets(status="pending")` still works correctly ✓

## Human Approvals (Pending)

- [ ] Scope approval
- [ ] Code review approval
- [ ] Merge approval
- [ ] Deployment approval
