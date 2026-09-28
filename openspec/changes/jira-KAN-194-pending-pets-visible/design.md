# Design

## Context

The Petstore catalog uses `search_pets()` in `app/petstore_app/catalog.py` to filter pets by status, species, tags, and name query. The product rule states "Default pet search returns only available pets" and "Pending pets can be shown only when explicitly requested."

Current implementation on line 50 uses `if normalized_status and normalized_status != pet.status:` which has a truthy check that bypasses the filter when status is an empty string. Log evidence shows error code `PENDING_PET_VISIBLE` with pet-103 (Nova, a pending dog) appearing in available-pets results.

## Decision

Normalize empty status strings to "available" at the point of parameter processing (line 41), ensuring the filter is always applied consistently. This approach:
- Maintains backward compatibility with the existing `status="available"` default
- Makes the behavior explicit and predictable
- Avoids truthy/falsy logic pitfalls
- Requires minimal code change

Implementation:
```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

Then always apply the filter:
```python
if normalized_status != pet.status:
    continue
```

## Risks

**Risk:** Callers relying on `status=""` to bypass filtering will break  
**Mitigation:** No evidence of legitimate use; empty status is likely a bug in callers  
**Likelihood:** Low

**Risk:** Existing tests may assume empty string bypasses filter  
**Mitigation:** Review and update test suite; add explicit regression tests  
**Likelihood:** Low (existing tests use explicit status values)

## Validation Plan

1. Run `pytest app/tests/test_pet_catalog.py -v` - all existing tests must pass
2. Add `test_default_search_excludes_pending_pets()` - verify default returns only available
3. Add `test_empty_status_defaults_to_available()` - verify empty string is normalized
4. Verify `test_search_pets_can_find_pending_pets_when_requested()` still works
