# Change: Fix Pending Pet Visibility in Catalog

## Why

Support reports that customers are able to see and start adoption flows for pets with "pending" status that should not be visible in the default available-pets catalog. This creates customer confusion and extra work for operations. The default catalog search must return only pets with "available" status, while support and operations workflows can explicitly request pending pets when needed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-278
- Trigger: Jira webhook issue_created
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The backend `search_pets()` function is the authoritative source for catalog filtering logic.
- The web UI correctly implements status filtering on the client side.
- The bug is caused by an implementation gap that allows the status filter to be bypassed.
- Nova (pet-103) with status="pending" is the known test case.
- No database, persistence, or API changes are needed.
- The fix should not break existing support workflows that explicitly request pending pets.

## Non-Goals

- Changing the web UI implementation (it already filters correctly).
- Adding new pet statuses beyond "available" and "pending".
- Modifying the Pet data model or adding new fields.
- Changing adoption validation logic.
- Adding authentication or authorization.
- Deployment configuration changes.

## What Changes

- Backend catalog search logic will enforce status filtering even when an empty status value is provided.
- Regression tests will verify that pending pets never appear in default or available-only searches.
- The explicit pending-pet search capability for support workflows will be preserved.

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets. Support can still explicitly search for pending pets.
- Tests: New regression tests will prevent this bug from reoccurring. Existing tests will continue to pass.
- Humans: Customers will no longer see pending pets in adoption flows. Operations workload will decrease.

## Human Gates

- Scope approval: Pending - awaiting human confirmation this fix addresses the reported issue.
- Review approval: Pending - awaiting code review after PR creation.
- Merge approval: Pending - awaiting human approval to merge.
- Deployment approval: Pending - awaiting human approval to deploy.
