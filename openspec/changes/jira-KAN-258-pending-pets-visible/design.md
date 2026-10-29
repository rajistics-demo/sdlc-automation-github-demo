# Design

## Context

The Petstore catalog search function `search_pets()` in `app/petstore_app/catalog.py` accepts a `status` parameter that defaults to `"available"`. The function normalizes the status value and uses it to filter pets. However, the current implementation uses a falsy check `if normalized_status and ...` which allows empty strings to bypass the status filter entirely.

Product rules from `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog must show only `status="available"` pets
- Pending pets can be shown only when explicitly requested via `status="pending"`
- Nova (pet-103) is a known pending pet used in demos

The log evidence in `docs/logs/pending-pet-visible.ndjson` shows a `PENDING_PET_VISIBLE` error indicating Nova appeared in the available-pets experience.

## Decision

- Add validation at the start of `search_pets()` to reject empty or whitespace-only status values with a clear error message
- Keep the validation simple: `if not status.strip(): raise ValueError("status cannot be empty")`
- Place the validation immediately after the `max_results` check to maintain consistent parameter validation order
- Preserve the default `status="available"` parameter (callers who don't specify status are unaffected)
- Preserve the existing normalization and filtering logic
- No changes to the UI needed (it already filters correctly)

## Risks

- **Breaking change for callers passing empty status**: Mitigated by this being incorrect usage that should be caught
- **Backward compatibility**: The default parameter ensures existing callers are unaffected
- **Performance**: Validation adds one string check; negligible impact

## Validation Plan

- Add test case: `test_search_pets_rejects_empty_status()` to verify empty string raises ValueError
- Add test case: `test_search_pets_rejects_whitespace_status()` to verify whitespace-only string raises ValueError
- Add test case: `test_search_pets_excludes_pending_pets_by_default()` to verify Nova is excluded from species="dog" search
- Run existing tests to ensure backward compatibility: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q app/tests/`
