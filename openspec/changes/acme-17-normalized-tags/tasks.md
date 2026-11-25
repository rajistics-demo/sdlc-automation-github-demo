# Tasks: Normalized Tag Coverage

## Implementation Tasks

- [x] Create OpenSpec change artifacts
- [x] Review existing test patterns in `test_pet_catalog.py`
- [x] Review catalog implementation (`catalog.py`) to confirm normalization behavior
- [x] Add `test_search_pets_normalizes_tag_case`
- [x] Add `test_search_pets_normalizes_tag_whitespace`
- [x] Add `test_search_pets_max_results_applies_after_tag_filter`
- [ ] Run new tests to confirm they pass (pytest not available in sandbox)
- [ ] Run full test suite to ensure no regressions (pytest not available in sandbox)
- [x] Create draft PR with evidence

## Validation Tasks

- [ ] New tests pass on feature branch
- [ ] Full test suite passes (`python3 -m pytest -q app/tests`)
- [ ] Validation script passes (`python3 scripts/validation/preflight_github_demo.py --offline`)

## Human Gates

- [ ] PR review approval
- [ ] Independent QA validation
- [ ] Merge approval (not performed by agent)

## Notes

- No deployment needed - test coverage only
- No UI changes - backend tests only
- No schema or data changes
