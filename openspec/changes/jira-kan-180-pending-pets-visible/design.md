# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters the pet catalog by species, status, tags, and max results. The default behavior is to return only available pets (`status="available"`).

**Current Bug**: Line 50 contains `if normalized_status and normalized_status != pet.status:` which uses a falsy check on `normalized_status`. When `status=""` is passed, the condition evaluates to False because empty string is falsy in Python, causing the entire status filter to be bypassed.

**Pet Fixture Data**: The catalog includes Nova (pet-103) with `status="pending"`, which should never appear in default search results but does when `status=""` is passed.

**Product Rule**: From `docs/wiki/petstore-catalog-availability.md` - "Default customer-facing catalog search must show only pets with `status="available"`"

## Decision

**Fix**: Remove the falsy check from line 50 of `catalog.py`

**Change from**:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

**Change to**:
```python
if normalized_status != pet.status:
    continue
```

**Rationale**:
- The default parameter already ensures `status="available"` when omitted
- Empty string should be treated as a specific filter value (matching pets with status=""), not as "skip filtering"
- This makes behavior consistent with other filters (species, tag) which don't have falsy checks
- After normalization (strip + lowercase), any non-matching status string will correctly exclude non-matching pets
- Empty string will filter to no results (correct) rather than bypassing the filter (incorrect)

## Risks and Mitigation

**Risk**: Breaking change if any code intentionally passes `status=""` to mean "all statuses"
- **Likelihood**: Low - no evidence of this pattern in codebase
- **Mitigation**: Existing tests verify default behavior; new regression test will catch any misuse
- **Search performed**: No API layer or service code found that calls `search_pets()` with empty string

**Risk**: Frontend impact
- **Likelihood**: None - frontend code in `app/web/app.js` line 17 uses hardcoded `pet.status === "available"` filter
- **Mitigation**: Frontend is independent and correct

**Risk**: Adoption flow impact
- **Likelihood**: None - adoption validation in `adoptions.py` is separate and already validates pet status
- **Mitigation**: This fix is isolated to catalog search visibility

## Validation Plan

### 1. Run existing tests
```bash
cd /workspace/project/sdlc-automation-github-demo
python -m pytest app/tests/test_pet_catalog.py -v
```

Expected: All 4 existing tests pass
- `test_search_pets_filters_by_species_and_status` - validates default filtering
- `test_search_pets_can_find_pending_pets_when_requested` - validates explicit pending search
- `test_search_pets_filters_by_tag` - validates tag filtering
- `test_search_pets_validates_max_results` - validates max results boundary

### 2. Add regression test for empty string edge case
```python
def test_search_pets_handles_empty_status():
    """Empty status string should not bypass filtering."""
    results = search_pets(status="")
    # No pets have status="", so result should be empty
    assert results == []
    # Specifically verify Nova is not returned
    assert "Nova" not in results
```

### 3. Run new test
```bash
python -m pytest app/tests/test_pet_catalog.py::test_search_pets_handles_empty_status -v
```

Expected: Test passes with fix in place

### 4. Optional UI validation
If UI Playwright tests are available:
```bash
cd app/web
npm test
```

Expected: All UI tests pass, including test that Nova is not visible in default search

## Implementation Notes

- **Files Modified**: `app/petstore_app/catalog.py` (1 line)
- **Files Added**: New test in `app/tests/test_pet_catalog.py`
- **No database changes**: Bug is pure logic, no schema or data changes needed
- **No dependency changes**: Fix uses existing Python standard library
- **No deployment changes**: Code change only, existing deployment process applies
