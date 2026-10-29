# Tasks: Fix Pending Pets Visible in Available Catalog

## Investigation
- [x] Read repository documentation (AGENTS.md, wiki)
- [x] Review log evidence (docs/logs/pending-pet-visible.ndjson)
- [x] Reproduce the bug with empty status string
- [x] Identify root cause in catalog.py line 50

## OpenSpec Artifacts
- [x] Create proposal.md
- [x] Create design.md
- [x] Create tasks.md (this file)
- [ ] Validate artifacts with validation script

## Implementation
- [ ] Fix status filter logic in catalog.py
- [ ] Add test for empty status string
- [ ] Add test for default search excluding pending pets
- [ ] Run all catalog tests

## Validation
- [ ] Run `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Verify Nova (pet-103) excluded from default searches
- [ ] Run full test suite if needed

## PR and Handoff
- [ ] Create feature branch
- [ ] Commit changes with clear message
- [ ] Push branch
- [ ] Open draft PR with evidence waypoints
- [ ] Add openhands-review label

## Human Gates
- [ ] Product review: Confirm status filter behavior is correct (PENDING)
- [ ] Code review: Review changes via openhands-review automation (PENDING)
- [ ] Merge approval: Human approves and merges (PENDING)
