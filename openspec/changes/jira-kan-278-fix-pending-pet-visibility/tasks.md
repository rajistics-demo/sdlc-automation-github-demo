# Tasks

## Investigation
- [x] Read repository documentation and product rules
- [x] Review wiki documentation on catalog availability rules
- [x] Examine log evidence for PENDING_PET_VISIBLE error
- [x] Identify root cause in catalog.py line 50
- [x] Confirm web UI already implements correct filtering

## OpenSpec Artifacts
- [x] Create change folder structure
- [x] Write proposal.md with source, assumptions, and impact
- [x] Write specs/catalog-availability/spec.md with requirements and scenarios
- [x] Write design.md with context, decision, and risks
- [x] Write tasks.md (this file)
- [x] Validate OpenSpec artifacts with validation script

## Implementation
- [x] Remove `and normalized_status` guard from catalog.py line 50
- [x] Add regression test: test_default_search_excludes_pending_pets()
- [x] Add regression test: test_empty_status_does_not_bypass_filter()

## Validation
- [x] Run catalog tests: python3 -m pytest -xvs app/tests/test_pet_catalog.py - **7 tests passed**
- [x] Verify all tests pass including existing pending pet search test - **All pass**
- [x] Run full test suite: python3 -m pytest -q app/tests/ - **11 tests passed**

## Delivery
- [ ] Create feature branch
- [ ] Commit changes with clear message
- [ ] Push branch to GitHub
- [ ] Open draft PR with evidence waypoints and validation results
- [ ] Add openhands-review label to trigger code review
- [ ] Update Jira issue with PR link and completion status
