# Change: Fix status filter to prevent unavailable pets from appearing in search results

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default pet search must return only available pets, but the current implementation allows empty status strings to bypass the status filter entirely.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-193
- Issue key: KAN-193
- Issue title: "Customers are seeing pets that are not available"
- Automation: `sdlc-story` (Jira webhook trigger)
- Reporter: Rajiv shah

## Assumptions

- The bug is in the backend `search_pets` function in `app/petstore_app/catalog.py`.
- When callers pass an empty string for `status=""`, the filter logic bypasses status checking entirely, returning all pets regardless of status.
- The fix should ensure that empty or whitespace-only status values default to "available" behavior.
- Explicitly passing `status="pending"` or other non-empty values should continue to work as expected.
- The web UI already filters correctly (confirmed in `app/web/app.js` line 17), so no frontend changes are needed.

## Non-Goals

- Deployment changes, authentication, database persistence, or new pet status types are out of scope.
- Schema changes or new dependencies are not required.
- UI changes are not needed since the web UI already filters correctly.

## What Changes

- Fix the status filter logic in `search_pets()` to treat empty or whitespace-only status strings as defaulting to "available".
- Change line 41 from `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() if status.strip() else "available"`.
- Change line 50 from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:` to always apply the status filter.
- Add regression tests that verify:
  - Default search returns only available pets
  - Passing `status=""` returns only available pets (not all pets)
  - Passing `status="pending"` explicitly still works

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-193 reports "Customers are seeing pets that are not available".
- `Stop 2 - Wiki/Docs`: Not applicable - no specific documentation found for this bug.
- `Stop 3 - Logs`: Not applicable - no log attachments provided in the ticket.
- `Stop 4 - Repo/Files`: Bug identified in `app/petstore_app/catalog.py` line 41-50. The truthy check on `normalized_status` allows empty strings to bypass the filter.
- `Stop 5 - Tests/PR`: Two new tests added to `app/tests/test_pet_catalog.py` to verify the fix. All 7 catalog tests and 4 adoption tests pass.

## Impact

- App behavior: Customers will only see available pets in search results, even when empty status is passed.
- Tests: Two new regression tests ensure the bug cannot reoccur.
- Humans: Reviewers approve scope, merge, and deployment decisions.

## Human Gates

- Scope approval: Jira issue acknowledgment.
- Review approval: GitHub PR review with `openhands-review` label.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
