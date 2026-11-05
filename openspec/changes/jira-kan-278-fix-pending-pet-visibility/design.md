# Design

## Context

The Petstore catalog uses a Python backend (`app/petstore_app/catalog.py`) that provides a `search_pets()` function with filtering by name query, species, status, and tag. The function has a default parameter `status="available"` to ensure the default behavior returns only available pets.

The current implementation on line 50 has a conditional check:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This check includes `and normalized_status` which means if `normalized_status` is an empty string (falsy), the entire condition evaluates to `False` and the status filter is skipped. This allows pending pets to appear in results when an empty status is passed.

The log evidence (`docs/logs/pending-pet-visible.ndjson`) shows error code `PENDING_PET_VISIBLE` with Nova (pet-103) appearing in the available-pets experience.

Product rule from `docs/wiki/petstore-catalog-availability.md`: "Default customer-facing catalog search must show only pets with status='available'."

## Decision

- Remove the `and normalized_status` guard from line 50 of `catalog.py` to ensure status filtering is always enforced.
- The fix changes line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`.
- Add regression tests that verify:
  1. Default search (no status param) returns only available pets and excludes pending pets.
  2. Search with empty status string does not return pending pets.
  3. Explicit pending status search still works for support workflows.
- The web UI (`app/web/app.js`) already correctly filters by `pet.status === "available"` and requires no changes.

## Risks

- **Breaking change risk**: LOW - The function already defaults to `status="available"`. Removing the empty-string bypass makes behavior more consistent, not less.
- **Support workflow impact**: NONE - Explicit `status="pending"` searches continue to work as before.
- **Performance**: NONE - No additional computation, just removes a bypass.
- **Test coverage gap**: Addressed by adding regression tests that explicitly verify pending pets are excluded from default searches.

## Validation Plan

1. Add regression test: `test_default_search_excludes_pending_pets()`
2. Add regression test: `test_empty_status_does_not_bypass_filter()`  
3. Run all catalog tests: `python3 -m pytest -xvs app/tests/test_pet_catalog.py`
4. Run full test suite: `python3 -m pytest -q app/tests/`
5. Verify existing tests still pass, including `test_search_pets_can_find_pending_pets_when_requested()`
