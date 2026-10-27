# Tasks

## Implementation

- [x] Investigate the issue and identify root cause in `catalog.py` line 41-50
- [x] Create OpenSpec-style change artifacts (proposal, spec delta, design)
- [x] Update `search_pets()` normalization to treat empty status as `"available"`
- [x] Add regression test: `test_search_pets_default_excludes_pending()`
- [x] Add regression test: `test_search_pets_empty_status_excludes_pending()`
- [x] Add regression test: `test_search_pets_whitespace_status_excludes_pending()`
- [x] Run focused validation: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [x] Verify fix with direct Python reproduction
- [ ] Open draft pull request with evidence and conversation link
- [ ] Add `openhands-review` label to trigger code review automation

## Validation Results

- **Focused tests:** ✓ All 8 tests passed in app/tests/test_pet_catalog.py
- **Direct reproduction:** ✓ All 4 scenarios verified:
  - Default search excludes pending pets
  - Empty status excludes pending pets
  - Whitespace status excludes pending pets
  - Explicit `status="pending"` includes pending pets
- **Full suite:** 90 passed, 5 failed (unrelated to this change - automation prompt test failures)

## Files Changed

- `app/petstore_app/catalog.py`: Fixed status normalization (line 41)
- `app/tests/test_pet_catalog.py`: Added 3 regression tests

## Human Approval Gates

- **Scope approval:** Pending - humans approve that this fix aligns with product requirements
- **Code review:** Pending - triggered by `openhands-review` label after PR creation
- **QA validation:** Pending - code review automation will add `openhands-qa` label if needed
- **Merge approval:** Pending - humans approve merge after review and validation
- **Deployment:** Pending - humans control production deployment timing
