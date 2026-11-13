# Design

## Context

The Petstore demo app has a `search_pets` function in `app/petstore_app/catalog.py` that filters pets by various criteria including status. The function has a default parameter `status="available"`, but the implementation contains a bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

The condition `if normalized_status and ...` means that when `normalized_status` is an empty string (which is falsy in Python), the entire status filter is bypassed. This allows pending pets like Nova (pet-103) to appear in search results when they should not.

**Evidence waypoints**:
- **Docs**: `docs/wiki/petstore-catalog-availability.md` specifies that default catalog search must show only `status="available"` pets
- **Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with `pet-103` (Nova) appearing in available-pets experience
- **Code**: Bug reproduced by calling `search_pets(status='')` which returns all 4 pets including Nova (pending)

## Decision

- Change the status filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter always applies, treating empty/whitespace strings the same as the default "available" value after normalization
- No changes to function signature or default parameter value
- No changes to the frontend (it already correctly filters to available pets)
- Add regression tests to verify default behavior, empty string behavior, and that explicit pending searches still work

## Risks

**Risk**: Breaking existing callers that rely on empty status string behavior.
- **Mitigation**: The test suite shows no existing tests rely on this behavior. The frontend already filters to available pets. The documented intent is that default searches show only available pets.

**Risk**: Operations workflows that use empty status to see all pets.
- **Mitigation**: Review of codebase shows no such usage. Operations can explicitly request `status="pending"` when needed. The fix maintains the explicit status parameter behavior.

## Validation Plan

1. Run existing test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add new regression tests for:
   - Default search excludes pending pets
   - Empty status string excludes pending pets
   - Species filter with default status excludes pending pets
3. Verify explicit `status="pending"` still works (existing test covers this)
4. Run full test suite: `python3 -m pytest -q`
