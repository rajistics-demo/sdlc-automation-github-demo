# Change: Fix Pending Pets Showing in Available Catalog

## Why

Customers are seeing pets marked as "pending" in the default available-pets search results, creating confusion and allowing them to start adoption flows for pets that aren't yet ready. This violates the catalog availability contract and creates extra work for support operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-190
- Trigger: Jira webhook `jira:issue_created`
- Automation: Jira-to-PR automation via OpenHands SDLC Automation Demo

## Evidence Waypoints

### Stop 1 - Ticket

Jira KAN-190: "Customers are seeing pets that are not available"
- Issue description reports customers seeing and starting adoption flows for pets that shouldn't be available yet
- Priority: Medium
- Impact: Customer confusion and extra operations work

### Stop 2 - Wiki/Docs

Checked: `docs/wiki/petstore-catalog-availability.md`
- **Found**: Product requirement that default catalog search must show only `status="available"` pets
- **Found**: Known demo mapping: Nova is pet-103 with `status="pending"`
- **Found**: `PENDING_PET_VISIBLE` log code indicates catalog regression

### Stop 3 - Logs

Checked: `docs/logs/pending-pet-visible.ndjson`
- **Found**: Error code `PENDING_PET_VISIBLE` logged on 2026-06-29
- **Found**: Severity: ERROR
- **Found**: Affected pet: pet-103 (Nova)
- **Found**: Marked as `safe_to_fix: true`

### Stop 4 - Repo/Files

Investigated: `app/petstore_app/catalog.py`
- **Root cause**: `search_pets()` function at line 50 uses `if normalized_status` which treats empty string as falsy
- **Bug pattern**: When `status=""` is explicitly passed, the status filter is bypassed entirely
- **Impact**: All pets (including pending ones) are returned when status filter should be applied

Investigated: `app/tests/test_pet_catalog.py`
- **Gap**: No test coverage for empty-string status edge case
- **Gap**: No explicit test proving pending pets are excluded from default search

### Stop 5 - Tests/PR

- Will add regression test proving pending pets don't appear in default available search
- Will add edge case test for empty-string status parameter
- Will validate fix with pytest

## Assumptions

- The bug is in the catalog search logic, not in how the UI calls the search function
- Fixing the falsy comparison is safe and won't break existing valid use cases
- Empty string status should be treated as "no status filter" (show all) or should default to "available"
- Based on product docs, empty status should behave the same as the default "available" status

## Non-Goals

- Not changing UI components (backend fix only)
- Not modifying deployment settings or branch protection
- Not adding new features beyond fixing the availability regression
- Not refactoring unrelated catalog behavior
- Not changing pet data or fixtures

## What Changes

- Fix `catalog.py` line 50 to properly filter by status even when empty string is passed
- Add regression test proving pending pets stay out of default available results
- Add edge case test for empty-string status parameter

## Impact

- App behavior: Default catalog search will correctly exclude pending pets
- Tests: New focused regression tests added to prevent recurrence
- Humans: PR requires review approval before merge; no deployment changes needed

## Human Gates

- Scope approval: This change is within safe boundaries (logic fix + tests only)
- Review approval: Required before merge via `openhands-review` label
- Merge approval: Human must approve and merge the PR
- Deployment approval: Standard deployment process applies
