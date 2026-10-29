# Design

## Context

The Petstore catalog provides a `search_pets()` function that filters pets by species, status, tags, and name query. According to `docs/wiki/petstore-catalog-availability.md`, the default customer-facing search must show only pets with `status="available"`. Pending pets should only appear when explicitly requested.

The current implementation has a bug in the status filter logic (line 50 of `catalog.py`):

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition uses `if normalized_status` which evaluates to `False` when normalized_status is an empty string after stripping. This allows the status filter to be completely bypassed, causing pending pets like Nova (pet-103) to appear in results where they shouldn't.

Evidence from `docs/logs/pending-pet-visible.ndjson` confirms this regression with error code `PENDING_PET_VISIBLE`.

## Decision

- Modify the status filter logic to ensure it always applies when a status is provided
- Change the condition from `if normalized_status` to check the original parameter
- Since status has a default value of "available", the filter should always apply unless explicitly overridden
- The fix is: check if the pet's status matches the requested status, without the truthy check that allows empty strings to bypass

**Implementation approach:**
```python
# Before:
if normalized_status and normalized_status != pet.status:
    continue

# After:
if normalized_status != pet.status:
    continue
```

Since `status` has a default value of `"available"`, `normalized_status` will never be None. The only way for it to be empty is if someone explicitly passes `status=""`, and in that case we should still apply the filter (which would exclude all pets with non-empty status, which is the correct behavior).

## Risks

- **Breaking change risk**: LOW - The current behavior where empty status bypasses the filter is a bug, not a feature
- **Test coverage**: Need to add regression test for the PENDING_PET_VISIBLE scenario
- **Performance**: No impact - same filter logic, just correct condition
- **Backwards compatibility**: The default behavior is preserved; only the edge case of empty string is fixed

## Validation Plan

1. Run existing test suite: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Verify `test_search_pets_filters_by_species_and_status` still passes
3. Add and run new regression test: `test_search_default_excludes_pending_pets`
4. Manually verify that search_pets() with default args excludes pet-103 (Nova)
5. Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-196-pending-pets-visible`
