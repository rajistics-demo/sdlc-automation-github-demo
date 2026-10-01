# Design

## Context

The Petstore catalog serves two audiences:
- Customers see available pets through default searches
- Operations staff can explicitly query pending pets when investigating cases

The product rule (from `AGENTS.md`): "Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted."

Current implementation: `app/petstore_app/catalog.py` has a `search_pets()` function with default parameter `status: str = "available"`. The filter logic at line 50 checks `if normalized_status and normalized_status != pet.status:`.

Root cause: When `status=""` is passed, `normalized_status` becomes `""`, which is falsy in Python. The condition `if normalized_status` evaluates to `False`, causing the entire status filter to be skipped. This allows pending pets to leak into results.

Evidence:
- `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103
- `docs/wiki/petstore-catalog-availability.md` confirms Nova (pet-103) has `status="pending"` and should not appear in default searches

## Decision

Remove the falsy check from the status filter condition.

Change line 50 from:
```python
if normalized_status and normalized_status != pet.status:
```

To:
```python
if normalized_status != pet.status:
```

This ensures the status filter is always applied. Since the default parameter is `status: str = "available"`, all searches will filter to available pets unless a different status is explicitly provided.

Add explicit test `test_search_pets_excludes_pending_by_default` to verify Nova (pet-103) is excluded from default searches and prevent regression.

## Risks

- **Backward compatibility**: Low risk. The default parameter behavior is unchanged. Only edge case of explicitly passing `status=""` is affected (now correctly filters instead of bypassing).
- **Operations workflows**: No impact. Explicit `status="pending"` searches continue to work.
- **Web UI**: No changes needed. The UI already filters correctly.

## Validation Plan

1. Run `pytest app/tests/test_pet_catalog.py` to verify all tests pass
2. Verify new test explicitly checks Nova (pet-103) is excluded from default searches
3. Verify existing `test_search_pets_can_find_pending_pets_when_requested` still passes
4. No UI testing needed - web filter is already correct
