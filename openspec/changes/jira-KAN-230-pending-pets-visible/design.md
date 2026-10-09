# Design

## Context

The Petstore catalog provides `search_pets()` to filter pets by name, species, status, and tags. The function has a default parameter `status="available"` to ensure customer-facing searches show only available pets. However, the current implementation has a bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string (after calling `.strip().lower()` on an empty or whitespace-only input), the condition becomes falsy and the status filter is bypassed entirely. This allows pets with any status, including "pending", to appear in results.

Per `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing search must show only `status="available"` pets
- Support workflows may explicitly request `status="pending"`
- Nova is pet-103 with `status="pending"`

Per `docs/logs/pending-pet-visible.ndjson`:
- Error code `PENDING_PET_VISIBLE` confirms pet-103 appeared in available results
- This is classified as a catalog availability regression

## Decision

- Normalize the status parameter early and default to "available" if it's empty after stripping
- Keep the existing default parameter value for backward compatibility
- Maintain the existing filter logic but ensure `normalized_status` is never empty

Implementation approach:
```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

This ensures:
1. Explicit status values are respected (including `status="pending"` for support workflows)
2. Empty or whitespace-only status values default to "available"
3. The existing filter logic on line 50 works correctly
4. No breaking changes to the function signature or API

## Risks

- Low risk: The fix is a one-line change to status normalization
- Minimal behavior change: Only affects the edge case where empty/whitespace status was provided
- Test coverage: Existing tests verify explicit pending searches continue to work; new tests will prevent regression

## Validation Plan

- Add test: `test_search_pets_defaults_to_available_when_status_is_empty()`
- Add test: `test_search_pets_defaults_to_available_when_status_is_whitespace()`
- Run: `pytest app/tests/test_pet_catalog.py -v`
- Verify: All existing tests pass, including explicit pending search test
- Confirm: Nova (pet-103) does not appear in default search results

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-230 "Customers are seeing pets that are not available"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default must be available-only
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows PENDING_PET_VISIBLE error with pet-103
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 has the defect in status filter logic
- **Stop 5 - Tests/PR**: Added regression tests, ran validation, opened draft PR with openhands-review label
