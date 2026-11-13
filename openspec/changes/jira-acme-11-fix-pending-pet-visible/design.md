# Design

## Context

The petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` filters pets by query, species, status, and tag. The function has a default parameter `status: str = "available"` which should ensure that searches without an explicit status return only available pets.

However, the implementation has a subtle bug at line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed explicitly, `normalized_status` becomes an empty string after `.strip().lower()`, which is falsy. The condition `if normalized_status` fails, causing the status filter to be completely bypassed. This allows pending pets to appear in results.

The wiki documentation at `docs/wiki/petstore-catalog-availability.md` confirms that Nova (pet-103) is a pending pet and should not appear in default searches. The log file `docs/logs/pending-pet-visible.ndjson` contains a `PENDING_PET_VISIBLE` error showing this regression occurred.

## Decision

- Change the status filter logic to check if the normalized status does not match, without the falsy check
- Since the function parameter has a default value of "available", we know normalized_status will always be a string
- The fix ensures that even an empty status string is compared against pet.status, preventing the bypass

Implementation change in `catalog.py` line 50:
```python
# Before:
if normalized_status and normalized_status != pet.status:
    continue

# After:
if normalized_status != pet.status:
    continue
```

This simple change ensures the status filter always applies, using the default "available" value when no status is provided, and properly filtering even when an empty string is passed.

## Risks

- **Backward compatibility**: Low risk. The function signature already defaults to "available", so removing the falsy check aligns behavior with the documented contract.
- **Explicit empty status**: If callers explicitly pass `status=""` expecting to get all pets regardless of status, this will break that behavior. However, this is the bug we're fixing—the product rule requires default searches to return only available pets.
- **Test coverage**: Existing tests verify available and pending status filtering work correctly. We need to add regression tests for empty status strings.

## Validation Plan

1. Add regression test: `test_search_pets_with_empty_status_excludes_pending_pets`
2. Add regression test: `test_default_search_excludes_pending_pets`
3. Run existing test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
4. Run full test suite: `python3 -m pytest -q`
5. Verify existing tests still pass (they should, as they use proper status values)
