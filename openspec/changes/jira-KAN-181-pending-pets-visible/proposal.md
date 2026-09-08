# Change: Fix Pending Pets Visible in Default Search

## Why

Support teams report that customers are seeing pets with "pending" status in their default catalog searches. This violates the product rule that default searches should show only available pets. Customers are attempting to start adoption flows for pets that aren't ready, creating confusion and operational overhead.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-181
- Trigger: Jira webhook `jira:issue_created` event
- Automation: SDLC Automation Demo - Jira issue to PR workflow

## Evidence Waypoints

### Stop 1 - Ticket
Jira KAN-181: "Customers are seeing pets that are not available"
- Description: Support reports customers can see and start adoption flows for unavailable pets
- Priority: Medium
- Impact: Customer confusion and operational overhead

### Stop 2 - Wiki/Docs
**Found:** `docs/wiki/petstore-catalog-availability.md`
- Default customer catalog must show only `status="available"` pets
- Support may explicitly request `status="pending"` pets
- Nova (pet-103) has `status="pending"` and should not appear in default searches
- `PENDING_PET_VISIBLE` log code indicates this specific regression

### Stop 3 - Logs
**Found:** `docs/logs/pending-pet-visible.ndjson`
- Timestamp: 2026-06-29T12:00:00Z
- Error code: `PENDING_PET_VISIBLE`
- Pet ID: pet-103 (Nova)
- Evidence confirms pending pet was visible in available-pets experience

### Stop 4 - Repo/Files
**Bug location:** `app/petstore_app/catalog.py` line 50
```python
if normalized_status and normalized_status != pet.status:
    continue
```
**Problem:** When `status=""` (empty string) is passed, the falsy check `if normalized_status` bypasses the entire status filter, allowing all pets (including pending ones) to be returned.

**Root cause:** The condition treats empty string as a signal to skip filtering, but the function has a default `status="available"` parameter. However, if an API caller or form submission passes an explicit empty string, the filter is disabled.

### Stop 5 - Tests/PR
**Test coverage gaps identified:**
- No test for `search_pets(status="")` edge case
- No test explicitly verifying pending pets are excluded from default searches
- No regression test for Nova (pet-103)

## Assumptions

- The backend `search_pets()` function should always apply status filtering since it has a default `status="available"` parameter
- Empty string `status=""` should not disable the filter; if a caller wants to skip filtering, they should pass `None` or omit the parameter
- Existing tests for explicit `status="available"` and `status="pending"` should continue to pass
- Frontend (`app/web/app.js`) already has defensive filtering (`pet.status === "available"`), so this is a backend data integrity fix

## Non-Goals

- Changing the frontend filtering logic (already correct)
- Adding new pet statuses beyond "available" and "pending"
- Modifying database schema or adding new fields
- Changing API contracts or adding new query parameters
- Altering authentication, authorization, or deployment settings

## What Changes

**Backend:**
- Fix the status filter condition in `app/petstore_app/catalog.py` line 50 to not be skippable via empty string
- Change from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter is always applied when status is provided (including the default "available")

**Tests:**
- Add regression test verifying default `search_pets()` returns only available pets
- Add edge case test verifying `search_pets(status="")` does not bypass the filter
- Add specific test verifying Nova (pet-103) is excluded from default searches

## Impact

**App behavior:**
- Default pet searches will reliably return only available pets
- Pending pets will only appear when explicitly requested with `status="pending"`
- Empty string status parameter will no longer bypass filtering

**Tests:**
- 3 new test cases added to `app/tests/test_pet_catalog.py`
- All existing tests should continue to pass

**Humans:**
- PR requires human review and approval
- Merge requires human approval
- Humans control deployment timing
- Operations should monitor `PENDING_PET_VISIBLE` log metric after deployment

## Human Gates

- **Scope approval:** Required before implementation (covered by this proposal)
- **Review approval:** Required before merge (PR must be reviewed)
- **Merge approval:** Required (humans control git history)
- **Deployment approval:** Required (humans control when this reaches production)
