# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default available-pets search must exclude pets with status="pending" to maintain the proper customer experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-212
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira issue to draft pull request

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-212 "Customers are seeing pets that are not available"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` - confirms default catalog search must show only available pets, and `PENDING_PET_VISIBLE` log indicates a catalog regression
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` - shows error code `PENDING_PET_VISIBLE` with pending pet ID `pet-103` (Nova) visible in available-pets experience
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` - `search_pets()` function has a bug on line 50 where empty status strings bypass the status filter
- **Stop 5 - Tests/PR**: Added test to verify empty status strings default to available-only behavior; existing tests confirm pending pets can still be found when explicitly requested

## Assumptions

- The bug is in the catalog search logic, not in the adoption flow or UI layer
- Empty string status parameters should be treated as "available" (the default)
- The fix should not break the ability to explicitly search for pending pets (status="pending")
- This is a safe backend fix that does not require schema changes, auth changes, or new dependencies

## Non-Goals

- Changing how the adoption flow works
- Adding new pet statuses beyond "available" and "pending"
- Modifying the UI to prevent customers from manually constructing invalid queries
- Changing the default status from "available" to something else

## What Changes

- `app/petstore_app/catalog.py`: Fix status filter to handle empty strings correctly by defaulting them to "available" and always applying the status filter
- `app/tests/test_pet_catalog.py`: Add regression test to verify default search excludes pending pets and empty status strings behave correctly

## Impact

- **App behavior**: Default pet searches will correctly exclude pending pets; explicit searches with status="pending" continue to work
- **Tests**: New focused test added to prevent regression; all existing tests continue to pass
- **Humans**: Code review and merge approval required; no deployment configuration changes needed

## Human Gates

- **Scope approval**: Required before implementation
- **Review approval**: Required via `openhands-review` label
- **Merge approval**: Human decision
- **Deployment approval**: Human decision
