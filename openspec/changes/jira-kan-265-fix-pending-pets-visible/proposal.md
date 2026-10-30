# Change: Fix Pending Pets Appearing in Available Catalog

## Why

Customers are seeing pets with "pending" status in the available-pets catalog search, which violates product rules. This creates confusion for customers who attempt to start adoption flows for pets that are not yet ready, and generates extra work for operations staff who must handle these cases manually.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-265
- Trigger: Jira issue created event
- Automation: jira-to-story automation

## Assumptions

- The bug is in the backend `search_pets()` function's status filtering logic
- The fix should preserve backward compatibility for explicit status searches
- No schema, persistence, or deployment changes are needed
- The UI already correctly filters for available pets only

## Non-Goals

- Changing the UI implementation (already correct)
- Adding new pet statuses beyond "available" and "pending"
- Modifying adoption workflow logic
- Persistence or database changes
- Authentication or authorization changes

## What Changes

- Fix the `search_pets()` function in `app/petstore_app/catalog.py` to properly enforce the default `status="available"` filter
- Add regression tests to verify that default searches and available-only searches exclude pending pets
- Ensure explicit `status="pending"` searches continue to work for support/operations workflows

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets; explicit pending-status searches remain supported
- Tests: New regression tests added to prevent this bug from recurring
- Humans: Operations staff will no longer receive incorrect adoption requests for pending pets

## Human Gates

- Scope approval: Pending human review of change proposal
- Review approval: Pending human review of implementation
- Merge approval: Pending human merge decision
- Deployment approval: Pending human deployment decision
