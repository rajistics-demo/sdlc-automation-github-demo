# Design

## Context

The Petstore catalog provides a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by name, species, status, and tags. The function has a default parameter `status="available"` that should restrict results to available pets only.

The current implementation at line 50 uses:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition has a defect: when `normalized_status` is an empty string (after calling `.strip().lower()` on an empty string input), the condition `if normalized_status` evaluates to `False` in Python, causing the entire status filter to be skipped. This allows pending pets (like Nova/pet-103) to appear in results.

The product rule states that default searches must show only available pets, and the wiki at `docs/wiki/petstore-catalog-availability.md` explicitly requires pending pets not appear in the default available-pets experience.

## Decision

Change the status filter condition from:
```python
if normalized_status and normalized_status != pet.status:
```

To:
```python
if not normalized_status:
    normalized_status = "available"
if normalized_status != pet.status:
```

This approach:
- Explicitly treats empty/whitespace-only status as "available"
- Maintains backward compatibility with existing callers
- Keeps the filter logic simple and testable
- Preserves explicit `status="pending"` searches for operations use cases

Alternative considered but rejected: Change the filter to `if normalized_status is not None and normalized_status != pet.status`. This would still allow empty strings through and doesn't match the product requirement that empty should mean available.

## Risks

**Risk**: Changing filter behavior could affect existing code that relies on empty string bypassing the filter.

**Mitigation**: 
- Review shows no existing tests use `status=""` 
- The default parameter already documents "available" as the expected default
- The bug fix aligns behavior with documented product rules
- Regression tests will prevent future breakage

**Risk**: Operations workflows that need to see all pets might break.

**Mitigation**: 
- Operations should explicitly pass `status="pending"` for pending pet searches
- No evidence in the codebase of legitimate use of `status=""` to bypass filter
- The wiki explicitly states pending pets should only appear in explicit searches

## Validation Plan

1. **Unit tests**: Add regression tests to `app/tests/test_pet_catalog.py`:
   - Test `search_pets(status="")` returns only available pets (excludes Nova)
   - Test `search_pets(status="  ")` (whitespace) returns only available pets
   - Test `search_pets(status="pending")` still returns Nova
   - Test default `search_pets()` continues to work

2. **Existing tests**: Verify all existing tests in `app/tests/` continue to pass

3. **Reproduction verification**: Confirm the original bug reproduction no longer shows Nova in `search_pets(status="")` results

4. **Backend test suite**: Run full backend test suite with `python3 -m pytest -q app/tests`
