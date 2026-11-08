# Tasks

## Evidence Waypoints

- [x] Stop 1 - Ticket: Jira ACME-3 reports customers seeing unavailable pets in catalog
- [x] Stop 2 - Wiki/Docs: Confirmed in `docs/wiki/petstore-catalog-availability.md` that default must show only available
- [x] Stop 3 - Logs: Found `docs/logs/pending-pet-visible.ndjson` showing PENDING_PET_VISIBLE error for pet-103 (Nova)
- [x] Stop 4 - Repo/Files: Identified bug in `app/petstore_app/catalog.py` line 50 - empty status bypasses filter
- [ ] Stop 5 - Tests/PR: Tests added and PR opened

## Implementation Tasks

- [x] Create OpenSpec-style change artifacts (proposal, spec, design, tasks)
- [x] Validate OpenSpec structure
- [ ] Implement fix in `app/petstore_app/catalog.py`
- [ ] Add regression tests in `app/tests/test_pet_catalog.py`
- [ ] Run focused test suite (`app/tests/test_pet_catalog.py`)
- [ ] Run full test suite (`app/tests`)
- [ ] Create/update branch `codex/eks-demo-acme-3`
- [ ] Open draft PR with evidence waypoints
- [ ] Add label `openhands-eks-demo`
- [ ] Add label `openhands-eks-review` as final handoff
- [ ] Post PR link and summary to Jira ACME-3

## Validation Results

- OpenSpec validation: Pending
- Focused tests: Pending
- Full test suite: Pending
- PR creation: Pending
- Jira update: Pending

## Human Approvals

- Scope approval: Pending (human must confirm no clients depend on empty status behavior)
- Review approval: Pending (code review required)
- Merge approval: Pending (human must approve merge)
- Deployment approval: Pending (human decides deployment timing)
