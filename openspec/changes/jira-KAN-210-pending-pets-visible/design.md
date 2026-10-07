# Design

## Context

The petstore catalog provides `search_pets()` function in `app/petstore_app/catalog.py`. The function has a default parameter `status="available"` to filter pets by availability status. According to product rules and wiki documentation, the default search must return only available pets, excluding pending ones.

The current implementation has a bug on line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition uses a truthy check on `normalized_status`. When an empty string is passed as the status parameter, the normalized status becomes `""` (falsy), causing the entire status filter to be bypassed. This allows pending pets to appear in results where they shouldn't.

## Decision

Change the status filter logic to enforce filtering unless the status is explicitly `None`. The fix:

```python
if normalized_status is not None and normalized_status != pet.status:
    continue
```

This ensures:
- Default behavior with `status="available"` filters correctly
- Explicit `status="pending"` works as intended
- Empty string `status=""` is normalized to `""` and properly filtered
- The status parameter must be explicitly set to show all statuses (which isn't currently supported by the API)

Alternative considered: Normalize empty string to "available" in the parameter processing. This approach was rejected because it would change the parameter handling semantics and might hide caller bugs.

## Risks

- **Backward compatibility**: If any callers were relying on `status=""` to return all pets, this would break them. Mitigation: Search the codebase for existing callers; based on tests, explicit status values are always provided when filtering.

- **Test coverage**: The bug wasn't caught by existing tests. Mitigation: Add explicit regression tests for default search behavior and empty string handling.

## Validation Plan

1. Run existing test suite to ensure no regressions:
   ```bash
   cd app && python -m pytest tests/test_pet_catalog.py -v
   ```

2. Add and run new regression tests:
   - Test that default search excludes pending pets
   - Test that empty status string is handled correctly
   - Verify Nova (pet-103) is excluded from default search

3. Manual verification:
   - Confirm Scout (pet-101, available dog) appears in default dog search
   - Confirm Nova (pet-103, pending dog) does NOT appear in default dog search
   - Confirm Nova appears when explicitly searching with `status="pending"`
