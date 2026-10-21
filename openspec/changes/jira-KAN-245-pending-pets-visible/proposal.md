# Change: Fix Pending Pets Visibility in Default Catalog Search

## Why

Support reports that some customers are able to see and start adoption flows for pets with `status="pending"` that should not be available yet. This violates the petstore availability rule that default searches must show only `status="available"` pets. The log evidence confirms `PENDING_PET_VISIBLE` errors with pet-103 (Nova) appearing in the available-pets experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-245
- Trigger: Jira issue created webhook
- Automation: jira-issue-to-pr

## Assumptions

- The bug is triggered by calls passing an empty string for status, bypassing the filter
- No callers intentionally rely on empty status to show all pets
- The web UI correctly filters on the frontend but the backend API must enforce this rule
- No database or persistence layer is involved; this is in-memory catalog behavior only

## Non-Goals

- Changing the frontend UI filtering logic
- Adding new status types beyond "available" and "pending"
- Modifying adoption flow or permissions
- Adding authentication or authorization checks

## What Changes

- Fix the status filtering logic in `app/petstore_app/catalog.py` to prevent bypassing the availability check when an empty or invalid status value is provided
- Add regression test to ensure empty status cannot bypass filtering
- Ensure default searches continue to return only available pets

## Impact

- App behavior: Default catalog searches will correctly exclude all non-available pets
- Tests: New regression test added for empty status edge case
- Humans: Code review and merge approval required before deployment

## Human Gates

- Scope approval: Approved via Jira issue creation
- Review approval: Required via `openhands-review` label
- Merge approval: Required by human reviewer
- Deployment approval: Required by operations team
