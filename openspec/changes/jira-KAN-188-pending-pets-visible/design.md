# Design

## Context

The Petstore catalog has a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by various criteria including status. Product rules state that default searches must return only available pets, while pending pets should only appear when explicitly requested with `status="pending"`.

The current bug occurs when an empty string is passed for the `status` parameter. The normalization logic converts it to an empty string, and then a truthy check (`if normalized_status and ...`) evaluates to False, causing the status filter to be completely bypassed.

## Decision

### Fix the status filter logic to handle empty strings correctly

**Current problematic code (line 50):**
```python
if normalized_status and normalized_status != pet.status:
    continue
```

**Fix approach:**
```python
# Line 41 - Use default if empty
normalized_status = status.strip().lower() if status.strip() else "available"

# Line 50 - No truthiness check needed
if normalized_status != pet.status:
    continue
```

**Rationale:**
- Status filtering is not optional according to product rules - it should always apply
- When `status=""` is passed, we should treat it as the default `"available"` status
- This prevents any scenario where the status filter is bypassed
- Aligns with the function's default parameter value of `"available"`
- More explicit about business logic and safety

### Alternative considered and rejected

We considered making status optional like species and tag (using `None` checks), but status filtering is a core business requirement, not an optional filter. The product rules explicitly state default searches must show only available pets.

## Risks

### Risk: Breaking existing callers that pass empty string

**Mitigation:** Investigation shows the web UI (`app/web/app.js`) correctly passes `status="available"` explicitly. The bug report itself indicates empty string behavior is incorrect. This fix corrects the bug rather than introducing a breaking change.

### Risk: Test coverage gaps

**Mitigation:** Add focused regression tests for:
1. Empty string status parameter
2. Default search behavior without status parameter
3. Species filter combined with empty string status

### Risk: Similar bugs in other filter parameters

**Assessment:** Other filters (species, tag, query) correctly use None-checking pattern and are optional by design. Status is the only mandatory filter, so no similar bugs exist.

## Validation Plan

1. Run existing test suite to ensure no regression: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add and run new regression tests for empty string status handling
3. Verify all four pets in test data are handled correctly:
   - pet-100 (Mochi, cat, available) ✓
   - pet-101 (Scout, dog, available) ✓
   - pet-102 (Pip, rabbit, available) ✓
   - pet-103 (Nova, dog, pending) ✗ excluded from default searches

## Implementation Scope

**Files to change:**
- `app/petstore_app/catalog.py` - Fix status filter logic (2 lines)
- `app/tests/test_pet_catalog.py` - Add regression tests (3 new test functions)

**No changes needed:**
- `app/petstore_app/adoptions.py` - Already has correct validation
- `app/web/app.js` - Already passes correct status parameter
- Database schema, secrets, deployment configuration
