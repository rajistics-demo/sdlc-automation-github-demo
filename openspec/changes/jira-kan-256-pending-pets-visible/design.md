# Design

## Context

The Petstore demo catalog has:
- A `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by query, species, status, and tag
- Product rule: "Default pet search returns only available pets"
- Product rule: "Pending pets can be shown only when explicitly requested and cannot be adopted"
- Known test data: Nova (pet-103) is a dog with status="pending"
- Log evidence: `PENDING_PET_VISIBLE` error code indicates pending pets appeared in available-pets experience

## Root Cause

The bug is in `catalog.py` line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed (empty string), `normalized_status = ""` evaluates to falsy in Python. The condition `if normalized_status and ...` short-circuits to False, so the status filter is skipped entirely, allowing ALL pets (including pending ones) to be returned.

## Decision

- Change the condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures that even when `normalized_status = ""`, the filter still applies correctly
- Empty string will not match any pet status, so nothing will be returned (which is reasonable)
- Alternatively, we can normalize empty status to "available" explicitly before the loop
- **Chosen approach:** Normalize empty status to "available" at the parameter level to preserve the documented default behavior

The fix:
```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",  # Already has default
    tag: str | None = None,
    max_results: int = 10,
) -> list[Pet]:
    # ... validation ...
    
    normalized_status = status.strip().lower() if status and status.strip() else "available"
    # This ensures empty string becomes "available"
```

## Risks

- **Breaking change risk**: LOW - The function signature already documents `status="available"` as the default. We're just fixing a bug where empty string bypassed that default.
- **Existing test risk**: LOW - Current tests explicitly pass `status="pending"` or rely on the default. None pass empty string.
- **Operations workflow risk**: LOW - Support tools that need pending pets explicitly pass `status="pending"`.

## Validation Plan

1. Add regression test: `test_search_pets_excludes_pending_by_default()` - verify empty query returns only available pets
2. Add regression test: `test_search_pets_treats_empty_status_as_available()` - verify `status=""` returns only available pets
3. Add regression test: `test_search_pets_excludes_pending_from_species_filter()` - verify species search excludes pending
4. Run existing tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
5. Run full test suite: `python3 -m pytest -q`
