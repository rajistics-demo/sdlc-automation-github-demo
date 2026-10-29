# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog search function has a defect where passing an empty string for status bypasses the availability filter, allowing pending pets like Nova (pet-103) to appear in the available-pets catalog.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-253
- Trigger: Jira issue created webhook
- Automation: SDLC Story to PR automation (skill evaluation run)

## Evidence Waypoints

### Stop 1 - Ticket
- **Jira KAN-253**: "Customers are seeing pets that are not available"
- **Description**: Support reports customers can see and start adoption flows for pets not yet available
- **Labels**: `codex-skill-589ebf68`
- **Priority**: Medium

### Stop 2 - Wiki/Docs
- **Found**: `docs/wiki/petstore-catalog-availability.md`
- **Rule**: Default customer-facing catalog search must show only pets with `status="available"`
- **Clarification**: Pending pets must not appear in default available-pets experience
- **Known mapping**: Nova is pet-103 with status="pending"

### Stop 3 - Logs
- **Found**: `docs/logs/pending-pet-visible.ndjson`
- **Error code**: `PENDING_PET_VISIBLE`
- **Affected pet**: `pet-103` (Nova)
- **Customer impact**: "Pending pets were visible in the available-pets experience"
- **Severity**: ERROR
- **Safe to fix**: true

### Stop 4 - Repo/Files
- **Catalog logic**: `app/petstore_app/catalog.py` - `search_pets()` function
- **Bug location**: Line 50 in `catalog.py`
- **Root cause**: `if normalized_status and normalized_status != pet.status` - empty string bypasses filter
- **Reproduction**: `search_pets(status="")` returns all 4 pets including Nova (pending)
- **Expected**: Should return only 3 available pets
- **Tests**: `app/tests/test_pet_catalog.py` - existing tests don't cover empty string case

## Assumptions

- The defect is limited to the status filter logic accepting empty strings
- The default parameter value `status="available"` remains correct
- Explicit `status="pending"` searches must continue to work for operations use cases
- No authentication, database, or API changes are needed
- The fix can be tested with unit tests and existing backend tests

## Non-Goals

- Changes to adoption order validation (already correct)
- UI changes (UI already filters correctly)
- Changes to data persistence or pet data structure  
- Deployment or infrastructure changes
- New external dependencies
- Authentication or authorization changes

## What Changes

- Modify the status filter condition in `catalog.py` to treat empty string as "available"
- Add regression tests to verify empty string status defaults to available-only results
- Add test to verify explicitly passing `status="pending"` still works

## Impact

- **App behavior**: Customers will no longer see pending pets when status is passed as empty string
- **Tests**: New regression tests added to prevent recurrence
- **Humans**: Requires code review approval and merge approval

## Human Gates

- **Scope approval**: Pending - awaiting human confirmation this fix matches requirements
- **Review approval**: Pending - PR must receive human code review
- **Merge approval**: Pending - human must approve and merge the PR
- **Deployment approval**: Pending - human controls deployment timing
