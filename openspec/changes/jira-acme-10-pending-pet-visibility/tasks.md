# Tasks

## Evidence Waypoints

- [x] **Stop 1 - Ticket**: Jira ACME-10 reports customers seeing pets that are not available
- [x] **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets
- [x] **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with pet-103 (Nova)
- [x] **Stop 4 - Repo/Files**: Bug found in `app/petstore_app/catalog.py` line 50 - empty status string bypasses filter
- [x] **Stop 5 - Tests/PR**: Tests added and validated, draft PR opened

## Implementation Tasks

- [x] Create OpenSpec-style change artifacts (proposal, design, spec delta, tasks)
- [x] Validate OpenSpec artifacts with validation script
- [x] Fix the status filter bug in `app/petstore_app/catalog.py`
- [x] Add regression test for default search excluding pending pets
- [x] Add regression test for empty status string excluding pending pets
- [x] Add regression test for species filter with default status excluding pending pets
- [x] Run existing test suite to verify no regressions (8 tests passed)
- [x] Run full test suite (12 tests passed)
- [ ] Create branch `codex/eks-demo-acme-10`
- [ ] Commit changes
- [ ] Open draft PR with evidence and validation results
- [ ] Add `openhands-eks-demo` label to PR
- [ ] Post PR link and validation summary to ACME-10

## Human Approvals

- [ ] Scope approval: Pending human review
- [ ] Code review: Pending (openhands-eks-review handoff)
- [ ] Merge approval: Pending human decision
- [ ] Deployment approval: Pending human decision
