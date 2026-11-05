# Tasks

## Investigation
- [x] Review Jira issue KAN-279
- [x] Check wiki documentation (`docs/wiki/petstore-catalog-availability.md`)
- [x] Review log evidence (`docs/logs/pending-pet-visible.ndjson`)
- [x] Examine catalog implementation (`app/petstore_app/catalog.py`)
- [x] Review existing tests (`app/tests/test_pet_catalog.py`)
- [x] Reproduce the bug (confirmed: `search_pets(status="")` returns all pets including pending)

## OpenSpec Artifacts
- [x] Create change folder: `openspec/changes/jira-KAN-279-fix-pending-pet-visibility/`
- [x] Write proposal.md with source, assumptions, and human gates
- [x] Write specs/catalog-availability/spec.md with acceptance criteria
- [x] Write design.md with implementation approach and risks
- [x] Write tasks.md (this file)
- [x] Validate OpenSpec artifacts with validation script

## Implementation
- [x] Fix status filtering in `app/petstore_app/catalog.py` - normalize empty status to "available"
- [x] Simplify status filter logic since normalized_status is now guaranteed non-empty
- [x] Add regression test for empty status string scenario
- [x] Add regression test for whitespace-only status string scenario
- [x] Run catalog tests to verify fix - all 7 tests pass
- [x] Run full app test suite - all 11 app tests pass

## Validation
- [x] Verify empty status returns only available pets - confirmed: returns Mochi, Scout, Pip
- [x] Verify existing tests still pass - all catalog tests pass
- [x] Confirm Nova (pet-103) is excluded from default/empty-status searches - confirmed
- [x] Confirm explicit status="pending" still works - test_search_pets_can_find_pending_pets_when_requested passes

## Delivery
- [ ] Create feature branch
- [ ] Commit OpenSpec artifacts
- [ ] Commit implementation and tests
- [ ] Open draft pull request
- [ ] Add `openhands-review` label
- [ ] Post Jira comment with PR link and evidence waypoints
