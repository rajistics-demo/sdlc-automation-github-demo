# Design

## Context

The petstore catalog (`app/petstore_app/catalog.py`) implements a `search_pets()` function that filters pets by name, species, status, and tag. The function has a default parameter `status="available"` to ensure customer-facing searches only show available pets.

The current filter logic on line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition has a subtle bug: when `normalized_status` is an empty string (after `strip().lower()`), it evaluates as falsy in Python. The `and` operator short-circuits, causing the entire status filter to be skipped. As a result, all pets (including pending ones) are returned.

Product rules (from `AGENTS.md` and `docs/wiki/petstore-catalog-availability.md`):
- Default pet search returns only available pets
- Pending pets can be shown only when explicitly requested
- Nova (pet-103) is the known pending pet in the demo

Existing test coverage validates:
- Species and status filtering
- Finding pending pets when explicitly requested
- Tag filtering
- max_results validation

Missing test coverage:
- Empty status string behavior
- Whitespace-only status string behavior

## Decision

**Option chosen**: Treat empty or whitespace-only status strings as missing, defaulting to "available".

Implementation approach:
1. After normalizing the status string with `strip().lower()`, check if it's empty
2. If empty, replace it with the default "available" string
3. Apply the existing filter logic unchanged

This is the smallest safe change because:
- It preserves all existing behavior for non-empty status values
- It requires only 2-3 lines of code
- The fix happens early in the function, before any filtering logic
- No changes to function signature, defaults, or return type
- No downstream impacts on adoptions or UI

Alternative rejected: Change the filter condition to `if normalized_status != pet.status:` (removing the truthiness check). This would be risky because it could affect other filter conditions (species, tag) that use the same pattern.

## Risks

- **Low risk**: The fix is localized to the status normalization step
- **Regression risk**: Mitigated by adding explicit tests for empty/whitespace status
- **Backward compatibility**: No API changes; existing callers continue to work
- **Performance**: No impact; only adds one conditional check

## Validation Plan

1. Run existing tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add new regression tests for empty and whitespace status strings
3. Run full test suite: `python3 -m pytest -q app/tests/`
4. Manual verification:
   ```python
   search_pets(status='')      # Should return only available pets
   search_pets(status='   ')   # Should return only available pets
   search_pets()               # Should continue to work as before
   ```
