# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) accepts a `status` parameter with a default value of `"available"`. The function normalizes the status string and filters pets based on the normalized value.

The current implementation has a bug on line 50: `if normalized_status and normalized_status != pet.status`. When `status=""` (empty string) is passed, `normalized_status` becomes `""` after normalization. The condition `if normalized_status` evaluates to False (empty string is falsy), so the status filtering is skipped entirely, returning all pets including pending ones.

Product rule (from `docs/wiki/petstore-catalog-availability.md`):
- Default customer-facing catalog search must show only pets with status="available"
- Pending pets must not appear in default or available-only searches

Log evidence (from `docs/logs/pending-pet-visible.ndjson`):
- Error code: `PENDING_PET_VISIBLE`
- Affected pet: pet-103 (Nova)
- Impact: Pending pets visible in available-pets experience

## Decision

- Normalize empty status strings to the default "available" value before filtering
- Add explicit handling for empty/whitespace-only status strings
- Maintain the existing default parameter value for backward compatibility
- Keep the filtering logic structure intact to minimize risk

Implementation approach:
```python
# After normalization, if status is empty, use the default
if not normalized_status:
    normalized_status = "available"
```

This ensures status filtering is always applied with a valid value.

## Risks

- **Backward compatibility:** Existing callers passing `status=""` will now get available-only results instead of all pets
  - **Mitigation:** This is the intended behavior per product rules; the current behavior is the bug
  
- **Test coverage:** Need to add explicit test for empty status string case
  - **Mitigation:** Add regression test that verifies empty status returns only available pets

- **UI consistency:** Web UI must also handle empty status correctly
  - **Mitigation:** Review app.js to ensure it doesn't rely on the buggy behavior (preliminary check shows UI filters correctly)

## Validation Plan

1. Run existing catalog tests to ensure no regressions: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add and run new test for empty status string scenario
3. Verify fix with direct Python test: `search_pets(status="")` returns only available pets
4. Run full test suite: `python3 -m pytest -q`
5. Check UI behavior remains correct (UI already filters to available only)
