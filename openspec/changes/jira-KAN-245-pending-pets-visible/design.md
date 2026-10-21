# Design

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` filters pets by status with a default value of "available". The petstore catalog availability rules require that default searches show only available pets, and pending pets should only appear when explicitly requested via `status="pending"`.

Evidence waypoints:
- **Stop 1 - Ticket:** Jira KAN-245 reports customers seeing unavailable pets
- **Stop 2 - Wiki/Docs:** `docs/wiki/petstore-catalog-availability.md` confirms default searches must exclude pending pets
- **Stop 3 - Logs:** `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with pet-103 (Nova)
- **Stop 4 - Repo/Files:** `app/petstore_app/catalog.py` line 50 has the buggy filter logic

## Decision

- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This removes the truthiness check that allows empty strings to bypass filtering
- Add regression test `test_search_pets_with_empty_status_returns_no_results()` to catch this edge case
- No changes to web UI, adoptions, or other modules

## Risks

- **Risk:** Existing callers passing `status=""` might depend on seeing all pets
  - **Mitigation:** This would be incorrect usage per the API contract; no legitimate caller should rely on this bypass
- **Risk:** The fix might break explicit pending searches
  - **Mitigation:** Existing test `test_search_pets_can_find_pending_pets_when_requested()` verifies this continues to work
- **Risk:** Default searches might break
  - **Mitigation:** Existing test `test_search_pets_filters_by_species_and_status()` verifies default behavior

## Validation Plan

- Run `python -m pytest app/tests/test_pet_catalog.py -v` to verify all tests pass
- Confirm new test `test_search_pets_with_empty_status_returns_no_results()` passes
- Verify existing tests still pass: 5 existing + 1 new = 6 total tests
