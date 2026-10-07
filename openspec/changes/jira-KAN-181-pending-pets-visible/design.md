# Design

## Context

The Petstore catalog maintains a list of pets with different statuses:
- `"available"`: pets ready for adoption
- `"pending"`: pets not yet ready (e.g., health checks in progress, paperwork incomplete)

The product rule states: **default searches return only available pets**. Pending pets should only appear when explicitly requested by support/operations staff.

The current implementation has a subtle bug in `app/petstore_app/catalog.py` where the status filter can be bypassed if an empty string is passed as the `status` parameter. This happens because the filter condition uses a falsy check: `if normalized_status and ...`, which treats `""` as `False` and skips the entire filter.

## Decision

### Fix the filter condition (Minimal Change)

**File:** `app/petstore_app/catalog.py`
**Line:** 50
**Change:**
```python
# Before:
if normalized_status and normalized_status != pet.status:
    continue

# After:
if normalized_status != pet.status:
    continue
```

**Rationale:**
- The function already has a default parameter `status: str = "available"`, so under normal circumstances `normalized_status` will never be empty
- However, if a caller explicitly passes `status=""` (e.g., from a form submission or API call), the current code incorrectly skips filtering
- Removing the `and normalized_status` check ensures the comparison always happens
- This aligns with how other string parameters might be handled: compare the actual value, don't treat empty as a bypass

**Alternative Considered: Validate Empty Status**
We could add explicit validation:
```python
if not normalized_status:
    raise ValueError("status cannot be empty")
```
**Rejected because:** The fix should be defensive and permissive. If empty string is passed, treating it as the default "available" (due to the string comparison) is safer than raising an error that could break existing API clients.

### Add Regression Tests

**File:** `app/tests/test_pet_catalog.py`
**Add 3 test cases:**
1. `test_search_pets_default_excludes_pending()` - Verify default search returns only available
2. `test_search_pets_empty_status_does_not_bypass_filter()` - Verify empty string edge case
3. `test_search_pets_excludes_nova_from_default()` - Verify Nova (pet-103) specifically

**Rationale:**
- The existing tests never triggered the bug because they always passed explicit status values
- These tests provide regression coverage for the exact failure mode reported in KAN-181

## Risks

### Risk: Breaking Change for Unintended Callers
**Description:** If any code intentionally passes `status=""` to mean "return all pets", this fix will break that behavior.

**Mitigation:**
- This would be a violation of the documented product rule (default = available only)
- No evidence in wiki docs, logs, or tests suggests this is intentional behavior
- Frontend already filters to available pets, so no user-facing breakage expected

**Likelihood:** Low

### Risk: Incomplete Fix
**Description:** There might be other code paths (API endpoints, form handlers) that also need status validation.

**Mitigation:**
- The frontend (`app/web/app.js` line 17) already has defensive filtering: `pet.status === "available"`
- This fix addresses the root data source
- Post-deployment monitoring of `PENDING_PET_VISIBLE` log metric will catch any remaining edge cases

**Likelihood:** Low

### Risk: Test Coverage Still Incomplete
**Description:** These tests cover the specific bug, but may not cover all possible status-related edge cases.

**Mitigation:**
- Existing tests for explicit `status="available"` and `status="pending"` continue to provide coverage
- This change adds the missing edge case (empty string)
- Future work could add fuzzing or property-based tests if needed

**Likelihood:** Low

## Validation Plan

**Pre-deployment:**
1. Run all existing catalog tests: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Verify new tests pass and explicitly check Nova exclusion
3. Visually inspect the catalog in `app/web/index.html` (if UI evidence is needed)

**Post-deployment:**
1. Monitor `PENDING_PET_VISIBLE` error metric in logs
2. Check support tickets for repeat reports of pending pets visible
3. Verify Nova (pet-103) no longer appears in customer-facing searches

**Rollback Plan:**
If issues arise, revert the one-line change in `catalog.py` and investigate further.
