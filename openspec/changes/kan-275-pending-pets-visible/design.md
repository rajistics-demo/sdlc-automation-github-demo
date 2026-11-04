# Design

## Context

The petstore catalog implements a `search_pets` function in `app/petstore_app/catalog.py` that filters pets by name, species, status, and tags. The function has a default parameter `status: str = "available"` to ensure customers see only available pets by default.

The current implementation on line 50 uses:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition checks if `normalized_status` is truthy before applying the filter. If an empty string is passed for status, the truthiness check fails, and the status filter is bypassed entirely, allowing pending pets to be returned.

## Decision

- Remove the truthiness check from the status filter condition.
- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter is always applied since status has a default value.
- Keep all other filter logic unchanged (species, tag, query filters use truthiness checks appropriately since they default to `None`).

## Risks

- **Risk**: The change might affect callers that explicitly pass `status=""` expecting to bypass the filter.
  - **Mitigation**: The repository documentation and product rules clearly state that default search must return only available pets. Any code passing empty status is incorrect behavior that should be fixed.

- **Risk**: The fix might break existing tests.
  - **Mitigation**: Run the full test suite. The existing tests already expect status filtering to work correctly.

## Validation Plan

- Run the existing catalog test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Add a regression test that verifies empty status doesn't bypass the filter
- Run the full test suite: `python3 -m pytest -q`
- If Playwright is available, run the UI smoke tests to verify the web UI still works correctly
