# Tasks

## Implementation

- [x] Create OpenSpec-style change folder and artifacts
- [x] Investigate and document the root cause
- [ ] Fix catalog.py status filter logic
- [ ] Add regression tests for empty status and default behavior
- [ ] Run validation and verify all tests pass
- [ ] Create branch and open draft PR
- [ ] Post results to Jira ticket ACME-11

## Validation

- [ ] pytest passes for `app/tests/test_pet_catalog.py`
- [ ] pytest passes for full test suite
- [ ] Regression tests confirm pending pets are excluded with empty/default status
- [ ] Existing functionality preserved (explicit pending searches still work)

## Evidence Waypoints

- [x] Stop 1 - Ticket: Jira ACME-11 - customers seeing pets that are not available
- [x] Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` - default must show only available pets
- [x] Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` - PENDING_PET_VISIBLE error for pet-103 (Nova)
- [x] Stop 4 - Repo/Files: `app/petstore_app/catalog.py` line 50 - status filter bypass bug
- [ ] Stop 5 - Tests/PR: Regression tests and PR link pending

## Human Gates

- [ ] PR review approval required
- [ ] Merge approval required by repository maintainer
- [ ] Standard deployment process applies
