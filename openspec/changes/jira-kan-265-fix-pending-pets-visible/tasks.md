# Tasks

## Evidence Waypoints

- [x] Stop 1 - Ticket: KAN-265 reports customers seeing pets that are not available
- [x] Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets; Nova (pet-103) is pending
- [x] Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103
- [x] Stop 4 - Repo/Files: Bug found in `app/petstore_app/catalog.py` line 50 - status filter uses falsy check that allows empty strings to bypass filter
- [x] Stop 5 - Tests/PR: Implementation complete, tests passing, PR ready

## Implementation Tasks

- [x] Create OpenSpec-style change artifacts (proposal, spec delta, design, tasks)
- [x] Validate OpenSpec structure
- [x] Fix status filter logic in `app/petstore_app/catalog.py`
- [x] Add regression tests to `app/tests/test_pet_catalog.py`
- [x] Run catalog tests to verify fix
- [x] Run full test suite (94 passed, 1 pre-existing failure unrelated to changes)
- [ ] Open draft PR with evidence and validation results

## Validation Status

- [x] Catalog tests passing (8/8 tests pass)
- [x] Full test suite mostly passing (94/95 pass, 1 pre-existing failure in context_reuse_report test)
- [x] No pending pets in default search results (verified: returns Mochi, Scout, Pip only)
- [x] Explicit pending status searches still work (verified: returns Nova only)

## Human Approvals

- [ ] Scope approval
- [ ] Code review approval
- [ ] Merge approval
- [ ] Deployment approval
