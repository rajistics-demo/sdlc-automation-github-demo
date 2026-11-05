# Change: Fix Pending Pet Visibility in Catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that are not available yet. Pending pets (like Nova, pet-103) should only appear when explicitly requested by support staff, not in the default customer-facing catalog search. This is confusing customers and creating extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-276
- Trigger: Jira issue created
- Automation: SDLC Story - Jira issue to PR

## Evidence Waypoints

### Stop 1 - Ticket
- **Jira**: KAN-276 "Customers are seeing pets that are not available"
- **Description**: Support reports pending pets visible in available-pets experience
- **Business Impact**: Customer confusion and extra operations work

### Stop 2 - Wiki/Docs
- **Checked**: `docs/wiki/petstore-catalog-availability.md`
- **Rule**: Default catalog search must show only `status="available"` pets
- **Note**: Nova is pet-103 with `status="pending"` and must not appear in default search

### Stop 3 - Logs
- **Checked**: `docs/logs/pending-pet-visible.ndjson`
- **Error Code**: `PENDING_PET_VISIBLE`
- **Evidence**: `pending_pet_ids: ["pet-103"]`
- **Severity**: ERROR - catalog availability regression

### Stop 4 - Repo/Files
- **File**: `app/petstore_app/catalog.py`
- **Bug**: Line 50 uses `if normalized_status and normalized_status != pet.status:` which treats empty string as falsy, bypassing status filter
- **Reproduction**: `search_pets(status="")` returns all pets including Nova (pending)
- **Root Cause**: When `status=""` is explicitly passed, the condition evaluates to False due to empty string being falsy in Python

### Stop 5 - Tests/PR
- Existing tests pass (they use explicit status values)
- Need regression test for empty status string
- PR to be created after implementation

## Assumptions

- The fix should treat empty string status the same as the default "available" status
- Existing behavior for explicit `status="pending"` and `status="available"` must be preserved
- This is a safe bug fix with no deployment, auth, or schema changes required

## Non-Goals

- Changing the UI adoption flow logic
- Modifying the pending pet workflow for operations staff
- Adding new status types or pet states
- Changes to persistence or database layer

## What Changes

- Fix the status filter logic in `catalog.py` to handle empty string correctly
- Add regression test to prevent empty status from returning pending pets
- Ensure default search and empty-status search both return only available pets

## Impact

- App behavior: Empty status parameter will now correctly filter for available pets only
- Tests: Add new test case for empty status string scenario
- Humans: Customers will no longer see pending pets in the available-pets catalog

## Human Gates

- Scope approval: Pending - requires human confirmation
- Review approval: Pending - requires human review via openhands-review label
- Merge approval: Pending - requires human approval
- Deployment approval: Pending - requires human approval
