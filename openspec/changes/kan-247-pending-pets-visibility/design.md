# Design: Fix pending pets visibility bug

## Context

Support reports indicate that Nova (pet-103, status="pending") appears in the default available-pets search results. The product requirement is that default pet search returns only available pets, and pending pets should only be visible when explicitly requested.

Investigation reveals the bug is in `app/petstore_app/catalog.py` at line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed explicitly, `normalized_status.strip().lower()` evaluates to `""` (empty string), which is falsy in Python. This causes the `if normalized_status` check to fail, completely bypassing the status filter.

## Decision

Change the status filter logic to treat empty string as the default "available" status. Replace line 50's conditional with a check that doesn't allow empty status to bypass the filter:

```python
# Treat empty status as "available" (the default)
if not normalized_status:
    normalized_status = "available"

if normalized_status != pet.status:
    continue
```

This ensures that:
1. Default behavior (`status="available"`) works as expected
2. Explicit empty string (`status=""`) is treated as the default "available"
3. Explicit status values (`status="pending"`, etc.) work correctly

Alternative considered: We could have changed the parameter default to handle the normalization earlier, but that would require more invasive changes. The current fix is minimal and handles the edge case at the point where the filter is applied.

## Validation Plan

1. Add a new test `test_search_pets_with_empty_string_status_returns_only_available()` to verify that `search_pets(status="")` returns only available pets
2. Ensure existing tests still pass
3. Verify that:
   - Default search returns only available pets
   - Explicit empty string returns only available pets  
   - Explicit "pending" status returns pending pets
   - Species filters work correctly with status filter

### Files Changed

- `app/petstore_app/catalog.py`: Fix status filter logic in `search_pets()` function
- `app/tests/test_pet_catalog.py`: Add regression test for explicit empty string status

### Risks

- **Low Risk**: The fix is a simple logic change in a well-tested function
- **Regression**: Existing tests confirm other filtering still works
- **Backwards Compatibility**: No API changes; only behavior correction
