# Design

## Context

The Petstore catalog uses a `search_pets` function in `app/petstore_app/catalog.py` that filters pets by multiple criteria including status. The function has a default parameter `status: str = "available"` and normalizes the input before filtering.

The bug occurs at line 50-51:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This condition only applies the status filter when `normalized_status` is truthy. If an empty string is passed for status, the normalization results in `""`, which is falsy, causing the filter to be skipped entirely.

According to `docs/wiki/petstore-catalog-availability.md`:
- Default customer searches must show only `status="available"` pets
- Support may explicitly request `status="pending"` for investigations
- Nova (pet-103) has `status="pending"` and should never appear in default searches
- A `PENDING_PET_VISIBLE` log entry (found in `docs/logs/pending-pet-visible.ndjson`) confirms this regression

## Decision

- Change the status filter condition from `if normalized_status and ...` to `if normalized_status != pet.status`.
- This ensures the filter applies even when `normalized_status` is an empty string.
- The default parameter `status="available"` already provides the correct behavior for calls that don't specify status.
- No changes needed to the API signature or other filter logic.

## Risks

- **Breaking change risk**: Low. Existing tests show that explicit `status="pending"` searches work correctly, and the default behavior is already documented as "available only."
- **Performance risk**: None. The change only affects the filter condition logic.
- **Compatibility risk**: Low. The fix enforces the documented behavior; any code relying on empty status to return all pets was already violating the availability rules.

## Validation Plan

- Run existing tests: `pytest app/tests/test_pet_catalog.py -v`
- Add new regression test: `test_search_pets_excludes_pending_from_default_results`
- Verify Nova (pet-103) does not appear in default searches
- Verify Nova still appears when explicitly searching with `status="pending"`

## Evidence Checklist

- [x] Stop 1 - Ticket: Jira KAN-213 - "Customers are seeing pets that are not available"
- [x] Stop 2 - Wiki/Docs: `docs/wiki/petstore-catalog-availability.md` - confirms available-only rule
- [x] Stop 3 - Logs: `docs/logs/pending-pet-visible.ndjson` - `PENDING_PET_VISIBLE` error for pet-103
- [x] Stop 4 - Repo/Files: `app/petstore_app/catalog.py` line 50 - falsy check allows bypass
- [ ] Stop 5 - Tests/PR: Tests to be added and PR to be created
