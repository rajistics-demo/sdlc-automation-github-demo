# Design

## Context

The bug exists in `app/petstore_app/catalog.py` at line 50. The current code checks `if normalized_status and normalized_status != pet.status:` before filtering. When `status=""` is passed, `normalized_status` becomes an empty string after `.strip().lower()`. The condition treats empty strings as falsy, skipping the entire status filter and allowing pending pets to appear in results.

The Petstore product rule states: "Default pet search returns only available pets." The wiki (docs/wiki/petstore-catalog-availability.md) confirms pending pets must not appear in default available-pets searches. Log evidence (docs/logs/pending-pet-visible.ndjson) shows Nova (pet-103, pending) appearing incorrectly with error code PENDING_PET_VISIBLE.

## Decision

- Remove the truthiness check from the status filter condition
- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter always applies, leveraging the default parameter `status="available"`
- Add regression test `test_search_pets_empty_status_excludes_pending` to verify empty strings don't bypass filtering
- Add test `test_search_pets_default_excludes_pending` to explicitly verify pending pets are excluded by default

## Risks

- Risk: Changing the filter logic could break explicit pending pet searches
  - Mitigation: Existing test `test_search_pets_can_find_pending_pets_when_requested` covers this case
- Risk: Empty status might be a valid use case we're unaware of
  - Mitigation: Product rules and wiki docs confirm only available pets should appear by default

## Validation Plan

- Run `python3 -m pytest -q app/tests/test_pet_catalog.py` to verify all tests pass
- Verify Nova (pet-103) is excluded from default searches
- Verify explicit `status="pending"` still returns Nova correctly
- Run full test suite `python3 -m pytest -q` if broader validation is needed
