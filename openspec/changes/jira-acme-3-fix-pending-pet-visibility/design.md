# Design

## Context

The petstore catalog search function (`app/petstore_app/catalog.py`) accepts an optional `status` parameter that defaults to "available". The function normalizes and filters pets by this status.

Current bug: Line 50 checks `if normalized_status and normalized_status != pet.status:` which means when `normalized_status` is an empty string (falsy), the entire status filter is skipped, allowing pending pets to be returned.

Evidence:
- **Wiki**: `docs/wiki/petstore-catalog-availability.md` specifies that default search must show only available pets
- **Log**: `docs/logs/pending-pet-visible.ndjson` shows PENDING_PET_VISIBLE error with pet-103 (Nova)
- **Data**: Pet-103 (Nova) is a dog with status="pending" in the PETS tuple

## Decision

- Change the status filter logic from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures that even an empty string status will be compared against pet.status, and since no pet has status="", the filter will work as an implicit "show all" (but we'll treat empty as default in practice)
- Actually, better approach: explicitly normalize empty status to "available" before the filtering loop, making the default behavior explicit

Implementation:
1. Add a check after normalization: `if not normalized_status: normalized_status = "available"`
2. Keep the existing filter logic which now always has a non-empty status to compare
3. This makes the fix explicit and easier to understand

## Risks

- **Risk**: Existing API clients that depend on `status=""` returning all pets will break
  - **Mitigation**: This behavior was never documented and violates the product rule. The bug report confirms it causes customer confusion. The fix aligns with documented behavior.
  
- **Risk**: Support workflows that need to see pending pets might be affected
  - **Mitigation**: Explicit `status="pending"` searches continue to work unchanged

## Validation Plan

1. Add test: `test_search_pets_treats_empty_status_as_available()` - verify empty string excludes pending
2. Add test: `test_search_pets_default_excludes_pending()` - verify default excludes pending explicitly  
3. Run existing tests to ensure no regression: `python3 -m pytest -q app/tests/test_pet_catalog.py`
4. Run full test suite: `python3 -m pytest -q app/tests`
5. Verify test passes with Nova (pet-103) excluded from default results
