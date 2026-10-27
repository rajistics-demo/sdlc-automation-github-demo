# Tasks

## Evidence Waypoints

- [x] **Stop 1 - Ticket**: Jira KAN-256 - "Customers are seeing pets that are not available" - sparse bug report with no technical details
- [x] **Stop 2 - Wiki/Docs**: Checked `docs/wiki/petstore-catalog-availability.md` - confirms default catalog must show only available pets, Nova (pet-103) is pending
- [x] **Stop 3 - Logs**: Checked `docs/logs/pending-pet-visible.ndjson` - `PENDING_PET_VISIBLE` error with pet-103 confirmed
- [x] **Stop 4 - Repo/Files**: Found bug in `app/petstore_app/catalog.py` line 50 - empty status bypasses filter
- [x] **Stop 5 - Tests/PR**: Added 3 regression tests, implemented fix, validated (all tests pass), opened draft PR #231

## Implementation Tasks

- [x] Create OpenSpec-style change folder structure
- [x] Write proposal.md with why, assumptions, and human gates
- [x] Write specs/pet-catalog/spec.md with acceptance criteria
- [x] Write design.md with root cause and fix approach
- [x] Validate OpenSpec artifacts
- [x] Implement the fix in `app/petstore_app/catalog.py`
- [x] Add regression tests in `app/tests/test_pet_catalog.py`
- [x] Run focused validation: `python3 -m pytest -q app/tests/test_pet_catalog.py` (8/8 passed)
- [x] Run full test suite: `python3 -m pytest -q` (12/12 passed)
- [x] Open draft pull request (PR #231)
- [x] Add `openhands-review` label to PR
- [x] Post summary comment to Jira issue

## Status

- Investigation: ✅ Complete - bug reproduced and root cause identified
- OpenSpec artifacts: ✅ Complete - proposal, spec delta, design, tasks created and validated
- Implementation: ✅ Complete - fix implemented with 3 regression tests
- Validation: ✅ Complete - all tests pass (8/8 catalog, 12/12 full suite)
- PR creation: ✅ Complete - draft PR #231 created with evidence waypoints
- Code review handoff: ✅ Complete - `openhands-review` label added
- Jira notification: ✅ Complete - summary comment posted
- Human approval gates: ⏳ Pending - awaiting human review, merge, and deployment decisions
