# Design

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` has an optional `status` parameter with a default value of `"available"`. The function uses a pattern common to optional filters: check if the value is truthy before applying the filter.

The bug occurs at line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The `and normalized_status` check was appropriate for truly optional parameters like `species` and `tag` (which can be None), but inappropriate for `status` which has a mandatory default value. This allows the status filter to be bypassed if an empty string is explicitly passed.

## Decision

- Remove the `normalized_status and` check from line 50
- Change the condition to always apply the status filter: `if normalized_status != pet.status:`
- This ensures status filtering is always applied, matching the product requirement
- Keep the existing behavior for species and tag filters (they remain optional)
- Preserve the ability to explicitly search for pending pets with `status="pending"`

## Risks

- **Low risk**: The change is a one-line fix to conditional logic
- **Backward compatibility**: Any code explicitly passing `status=""` would change behavior, but this is the desired fix
- **Test coverage**: Existing test `test_search_pets_can_find_pending_pets_when_requested()` verifies explicit pending searches still work
- **Mitigation**: Add regression test to verify pending pets are excluded from default search

## Validation Plan

1. Run existing tests to ensure no regressions: `pytest app/tests/test_pet_catalog.py`
2. Add new regression test: `test_default_search_excludes_pending_pets()`
3. Verify the test fails before the fix and passes after
4. Manually verify UI behavior matches expected catalog filtering
