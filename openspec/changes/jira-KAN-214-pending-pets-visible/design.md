# Design

## Context

The Petstore catalog search function in `app/petstore_app/catalog.py` provides a `search_pets()` function with a default `status="available"` parameter. The function normalizes the status parameter and filters pets accordingly.

Product requirement from `docs/wiki/petstore-catalog-availability.md`: Default customer-facing catalog search must show only pets with `status="available"`. Support may explicitly request pending pets, but they must not appear in default searches.

Evidence from `docs/logs/pending-pet-visible.ndjson`: Error code `PENDING_PET_VISIBLE` indicates Nova (pet-103, status="pending") appeared in available-pets experience, confirming a catalog regression.

## Decision

The bug is in `catalog.py` line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The condition `if normalized_status and` means when `normalized_status` is an empty string (falsy), the entire status filter is skipped. This allows pending pets to appear when an empty status is passed, bypassing the default filter.

**Fix**: Remove the truthiness check and always apply the status filter:
```python
if normalized_status != pet.status:
    continue
```

Since `status="available"` is the default parameter value, this ensures the filter is always applied correctly.

## Risks

- **Backward compatibility**: Low risk. The function signature already has `status="available"` as the default. Callers passing an explicit empty string `status=""` would previously see all statuses (bug); after the fix they'll see only available pets (correct behavior).
- **Test coverage**: Existing test `test_search_pets_can_find_pending_pets_when_requested()` proves explicit pending searches work. Need to add regression test for default behavior.

## Validation Plan

1. Run existing catalog tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add and run regression test for pending pet exclusion in default searches
3. Validate OpenSpec artifacts: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-214-pending-pets-visible/`
