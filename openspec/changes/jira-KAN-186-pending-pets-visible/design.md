# Design: Fix Empty Status String Filter Bypass

## Context

The Petstore catalog must ensure that default customer-facing searches return only pets with `status="available"`. Pending pets should only appear when explicitly requested with `status="pending"`. This business rule exists to prevent customer confusion and operational issues.

## Problem

The catalog search function `search_pets()` in `app/petstore_app/catalog.py` has a bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, `normalized_status` becomes an empty string. The condition `if normalized_status and ...` treats empty strings as falsy, causing the entire status filter to be skipped. This allows all pets, including pending ones, to be returned.

## Evidence

- **Stop 1 - Ticket**: Jira KAN-186 reports customers seeing pets that should not be available
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default searches must show only available pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` contains `PENDING_PET_VISIBLE` error confirming Nova (pet-103) appeared in available-pets view
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 contains the buggy filter logic
- **Stop 5 - Tests/PR**: Existing tests pass but don't cover empty status string edge case

## Root Cause

The filter logic assumes status will either be:
1. A meaningful non-empty string like `"available"` or `"pending"` (works correctly)
2. The default value `"available"` (works correctly)
3. `None` for nullable filtering (but status parameter is not nullable, defaults to `"available"`)

It does not handle the edge case where status is an empty string `""`, which Python treats as falsy but is semantically different from `None`.

## Solution

Change the filter condition from:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

This ensures the status filter is always applied when a status value is provided. An empty string `""` will not match any pet's actual status (`"available"` or `"pending"`), so those pets will be correctly filtered out.

## Why This Fix Is Safe

1. **Default behavior unchanged**: When no status is passed, the default `"available"` is still used
2. **Explicit values unchanged**: `status="available"` and `status="pending"` continue to work exactly as before
3. **Empty string now safe**: `status=""` will match no pets (since no pet has status `""`), effectively filtering everything out - but since the default is `"available"`, this edge case won't break normal flows
4. **Adoption safety unchanged**: The adoption flow already validates pet status, providing a second line of defense
5. **Frontend unchanged**: Frontend filtering already works correctly and doesn't need modification

## Alternative Considered

We could normalize empty strings to the default value:
```python
normalized_status = (status.strip().lower()) or "available"
```

**Rejected** because:
- It's more complex than needed
- The simpler fix makes empty strings behave consistently with other non-matching values
- It's harder to reason about the difference between `status=""` and `status="available"` if they're silently equivalent

## Decision

Remove the falsy check from the status filter condition. Change line 50 from:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

This one-line change ensures the status filter is always applied when a status value is provided, treating empty strings consistently with any other non-matching status value.

## Files Changed

- `app/petstore_app/catalog.py` - Line 50: Remove falsy check from status filter
- `app/tests/test_pet_catalog.py` - Add regression test for empty status string

## Validation Plan

1. **Pre-fix validation**: Run new regression test to confirm it fails (demonstrating the bug exists)
2. **Implementation**: Apply the one-line fix to catalog.py
3. **Post-fix validation**: Run new regression test to confirm it passes
4. **Regression check**: Run all existing backend tests to ensure no breakage
5. **UI validation**: Run Playwright tests if available to verify frontend still works correctly
6. **Evidence check**: Confirm fix addresses the `PENDING_PET_VISIBLE` error scenario documented in logs

## Risks

- **Low risk**: This is a one-line fix to restore intended behavior
- **Mitigation**: Comprehensive test coverage including new regression test
- **Validation**: All existing tests must pass, new test must fail before fix and pass after
