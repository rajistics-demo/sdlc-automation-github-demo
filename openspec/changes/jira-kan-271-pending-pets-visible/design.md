# Design

## Context

The Petstore catalog uses `search_pets()` in `app/petstore_app/catalog.py` to filter pets by name, species, status, and tags. The function has a default status parameter of "available" but the filtering logic has an edge case: when an empty string is explicitly passed, the status filter is bypassed.

**Current filtering logic (lines 40-50):**
```python
normalized_status = status.strip().lower()
# ...
if normalized_status and normalized_status != pet.status:
    continue
```

The condition `if normalized_status` evaluates to False when the normalized status is an empty string, causing the entire filter check to be skipped.

**Product rule from wiki:**
> Default customer-facing catalog search must show only pets with `status="available"`.

**Log evidence:**
The `PENDING_PET_VISIBLE` error in `docs/logs/pending-pet-visible.ndjson` confirms that pending pet-103 (Nova) appeared in the available-pets experience.

## Decision

Normalize empty status strings to "available" before the filtering loop begins. This ensures that explicit empty strings are treated the same as the default parameter value.

**Implementation approach:**
```python
# After line 41, add:
if not normalized_status:
    normalized_status = "available"
```

This is the minimal safe change:
- Preserves existing behavior when status is omitted (uses default "available")
- Fixes the bug when status="" is explicitly passed
- Does not change the filtering logic itself
- Maintains support for explicit status="pending" calls

**Alternative considered and rejected:**
Changing the filter condition to `if normalized_status != pet.status:` would make status filtering always active, but would break the product requirement that allows explicit pending status requests. The normalization approach is safer and clearer.

## Risks

**Risk:** Callers might rely on empty string to mean "all statuses"
**Mitigation:** Repository documentation and wiki explicitly state that default search returns only available pets. Empty string was never documented as a valid way to bypass status filtering.

**Risk:** Breaking change for existing callers
**Mitigation:** The function signature default hasn't changed. Only the edge case of explicitly passing `status=""` is affected, which is not documented behavior and violates the product rule.

## Validation Plan

1. Add test `test_search_pets_filters_empty_status_to_available()` that fails before fix
2. Add test `test_search_pets_filters_empty_status_with_species()` to cover combined filters
3. Add test `test_search_pets_default_status_excludes_pending()` to document default behavior
4. Run existing tests to ensure no regressions
5. Run full test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`

All tests must pass after the fix.
