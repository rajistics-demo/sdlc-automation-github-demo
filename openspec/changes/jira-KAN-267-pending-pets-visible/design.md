# Design

## Context

The Petstore catalog has a default product rule: only available pets should appear in customer-facing searches. Support and operations can explicitly search for pending pets when investigating cases, but pending pets must never leak into the default experience.

The current implementation in `app/petstore_app/catalog.py` has a bug in the status filtering logic. When the status parameter is an empty string or contains only whitespace, the filter check `if normalized_status` evaluates to False (empty strings are falsy in Python), causing the status filter to be skipped entirely.

Evidence from repository context:
- Wiki: `docs/wiki/petstore-catalog-availability.md` confirms the product rule
- Logs: `docs/logs/pending-pet-visible.ndjson` shows error_code "PENDING_PET_VISIBLE" for pet-103 (Nova)
- Tests: Existing tests verify explicit status="pending" works, but don't test edge cases like empty strings

## Decision

- Change the status filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter is always applied, even when normalized_status is an empty string
- Since the default parameter is `status="available"`, normalized_status will be "available" by default
- If someone explicitly passes status="", it normalizes to "" which won't match any pet status, returning no results (safe behavior)
- Preserve all existing behavior for explicit status values including "pending"

## Risks

- **Risk**: Changing filter logic could break existing callers that rely on empty status behavior
  - **Mitigation**: Add comprehensive tests including empty string, whitespace, default, and explicit status cases. The test suite will catch any regression.

- **Risk**: Empty status parameter might be used intentionally to bypass filtering
  - **Mitigation**: This would be a security/product bug, not a feature. The fix enforces the documented product rule.

## Validation Plan

- Add test: `test_default_search_excludes_pending_pets()` - verify Nova is not in default results
- Add test: `test_empty_status_excludes_pending_pets()` - verify status="" doesn't bypass filtering
- Add test: `test_species_filter_excludes_pending_pets()` - verify species="dog" excludes Nova by default
- Run full test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run all tests: `python3 -m pytest -q`
