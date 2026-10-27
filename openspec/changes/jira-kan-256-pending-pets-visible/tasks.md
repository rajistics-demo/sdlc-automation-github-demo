# Tasks

## Evidence Waypoints

- [x] **Stop 1 - Ticket**: Jira KAN-256 - "Customers are seeing pets that are not available" - sparse bug report with no technical details
- [x] **Stop 2 - Wiki/Docs**: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default catalog must show only available pets, Nova (pet-103) is pending
- [x] **Stop 3 - Logs**: Checked `docs/logs/pending-pet-visible.ndjson` - `PENDING_PET_VISIBLE` error with pet-103 confirmed
- [x] **Stop 4 - Repo/Files**: Found bug in `app/petstore_app/catalog.py` line 50 - empty status bypasses filter
- [ ] **Stop 5 - Tests/PR**: Add regression tests, implement fix, validate, open draft PR

## Implementation Tasks

- [x] Create OpenSpec-style change folder structure
- [x] Write proposal.md with why, assumptions, and human gates
- [x] Write specs/pet-catalog/spec.md with acceptance criteria
- [x] Write design.md with root cause and fix approach
- [ ] Validate OpenSpec artifacts
- [ ] Implement the fix in `app/petstore_app/catalog.py`
- [ ] Add regression tests in `app/tests/test_pet_catalog.py`
- [ ] Run focused validation: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Run full test suite: `python3 -m pytest -q`
- [ ] Open draft pull request
- [ ] Add `openhands-review` label to PR
- [ ] Post summary comment to Jira issue

## Status

- Investigation: ✅ Complete - bug reproduced and root cause identified
- OpenSpec artifacts: ✅ Complete - proposal, spec delta, design, tasks created
- Implementation: ⏳ In progress
- Validation: ⏳ Pending
- PR creation: ⏳ Pending
- Human approval gates: ⏳ Pending review
