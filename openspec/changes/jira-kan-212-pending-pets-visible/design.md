# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py::search_pets`) filters pets by multiple criteria including status. The current implementation has a bug where the status filter can be bypassed when an empty string is passed as the status parameter.

Current implementation on line 41:
```python
normalized_status = status.strip().lower()
```

And on line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The bug occurs when `status=""` is passed: `normalized_status` becomes an empty string, which is falsy in Python, causing the condition `if normalized_status and` to evaluate to False, skipping the status filter entirely.

According to `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Support workflows may explicitly request `status="pending"` when investigating
- `PENDING_PET_VISIBLE` log indicates a catalog regression

The log file `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with Nova (pet-103) visible in the available-pets experience.

## Decision

- **Fix line 41**: Use Python's `or` operator to default empty strings to "available":
  ```python
  normalized_status = status.strip().lower() or "available"
  ```
  
- **Fix line 50**: Remove the truthiness check since status should always have a value:
  ```python
  if normalized_status != pet.status:
      continue
  ```

This ensures:
1. Empty strings are treated as "available" (matching the function's default parameter)
2. The status filter is always applied
3. Explicit searches with status="pending" continue to work
4. The fix is minimal and focused on the specific bug

## Risks

- **Risk**: The change modifies filter logic that could affect existing callers
  - **Mitigation**: Existing tests cover the main use cases (default search, explicit pending search, species+status filtering), and we're adding a regression test for the empty string case

- **Risk**: Empty strings might be intentionally used somewhere to mean "any status"
  - **Mitigation**: The function signature has a default of status="available", so the intent is clear that status filtering is always applied; if "any status" was needed, the parameter should be Optional[str] instead

- **Risk**: Other parts of the codebase might rely on the buggy behavior
  - **Mitigation**: Running the existing test suite will catch any regressions; the wiki documentation confirms this is a bug, not a feature

## Validation Plan

1. Run existing tests: `python -m pytest app/tests/test_pet_catalog.py -v`
2. Add and run regression test for empty status string behavior
3. Verify that default search excludes pending pets
4. Verify that explicit pending search continues to work
