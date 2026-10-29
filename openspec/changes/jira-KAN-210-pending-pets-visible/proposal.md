# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are seeing pets with "pending" status in the default available-pets catalog search. This creates confusion because pending pets are not yet ready for adoption and should only be visible when explicitly requested by support or operations staff. The bug violates the product requirement that default search returns only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-210
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira issue to draft PR

## Evidence Waypoints

### Stop 1 - Ticket
Jira issue KAN-210 reports: "Support reports that some customers are able to see and start adoption flows for pets that should not be available yet."

### Stop 2 - Wiki/Docs
Checked `docs/wiki/petstore-catalog-availability.md` which states:
- "Default customer-facing catalog search must show only pets with status='available'"
- "Nova is pet-103 with status='pending'"
- "PENDING_PET_VISIBLE log means a pending pet appeared in the available-pets experience"

### Stop 3 - Logs
Found evidence in `docs/logs/pending-pet-visible.ndjson`:
- Error code: `PENDING_PET_VISIBLE`
- Pending pet IDs: `["pet-103"]` (Nova)
- Confirmed this is a catalog availability regression marked as safe to fix

### Stop 4 - Repo/Files
Inspected `app/petstore_app/catalog.py`:
- `search_pets()` function has default parameter `status="available"`
- Bug found on line 50: `if normalized_status and normalized_status != pet.status:`
- The condition incorrectly allows bypassing the status filter when an empty string is passed
- When `status=""` is provided, `normalized_status` becomes empty string (falsy), skipping the status check entirely
- This allows pending pets like Nova (pet-103) to appear in results

### Stop 5 - Tests/PR
Current test coverage in `app/tests/test_pet_catalog.py`:
- Test exists for finding pending pets when explicitly requested
- Test exists for default species search
- Missing: explicit test that default search excludes pending pets
- Missing: explicit test that empty status string defaults to available-only

## Assumptions

- The bug is in the status filter logic, not in data or deployment configuration
- Fixing the filter condition to properly enforce status filtering is safe
- No API contract changes are needed; the fix corrects the implementation to match documented behavior
- Existing tests for explicit `status="pending"` searches should continue to pass

## Non-Goals

- Changing the API signature of `search_pets()`
- Adding new pet statuses beyond "available" and "pending"
- Modifying adoption workflow or UI beyond the catalog filtering fix
- Changes to authentication, authorization, or deployment settings

## What Changes

- Fix the status filter logic in `catalog.py` to properly enforce status filtering even when empty string is provided
- Add regression tests to ensure pending pets are excluded from default searches
- Add test to verify empty status string behavior

## Impact

- App behavior: Default pet search will correctly exclude pending pets; explicit pending searches will continue to work
- Tests: Add focused regression tests for the fixed behavior
- Humans: Code review needed to approve the logic change; QA verification of filtering behavior

## Human Gates

- Scope approval: Humans confirm this fix is the right approach
- Review approval: Humans review and approve the code change
- Merge approval: Humans approve and merge the PR
- Deployment approval: Humans approve deployment to production
