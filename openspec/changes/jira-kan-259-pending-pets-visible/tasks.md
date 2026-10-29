# Tasks

## OpenSpec Change Artifacts
- [x] Create proposal.md with why, source, evidence waypoints, assumptions, and human gates
- [x] Create specs/catalog/spec.md with acceptance criteria as requirements and scenarios
- [x] Create design.md with smallest safe implementation approach
- [x] Create tasks.md checklist
- [ ] Validate OpenSpec artifacts with validation script

## Implementation
- [ ] Update catalog.py to handle empty/whitespace status strings
- [ ] Add regression test for empty status string
- [ ] Add regression test for whitespace-only status string
- [ ] Verify existing tests still pass

## Validation
- [ ] Run pytest on catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Run full test suite: `python3 -m pytest -q app/tests/`
- [ ] Manual verification of empty status behavior

## Delivery
- [ ] Create feature branch from main
- [ ] Commit OpenSpec artifacts
- [ ] Commit implementation and tests
- [ ] Push branch to GitHub
- [ ] Open draft PR with evidence waypoints and validation results
- [ ] Add openhands-review label to PR
- [ ] Post Jira comment with PR link and automation session URL

## Human Approval Gates
- [ ] Scope approval (pending human review)
- [ ] Code review approval (pending openhands-review automation + human)
- [ ] Merge approval (pending human decision)
- [ ] Deployment approval (pending human decision)
