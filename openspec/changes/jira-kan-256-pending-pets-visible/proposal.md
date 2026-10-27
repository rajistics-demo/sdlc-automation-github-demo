# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that customers are seeing pets that should not be available yet in the main catalog and can start adoption flows for them. This confuses customers and creates extra work for operations. The default pet catalog must show only available pets, not pending ones.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-256
- Trigger: Jira issue created webhook
- Automation: SDLC Story (issue-to-PR)

## Assumptions

- The bug is in the backend `search_pets()` function which incorrectly handles empty string status parameters.
- Fixing the status filter logic will resolve the issue without breaking existing functionality.
- The fix requires no schema changes, new dependencies, or environment changes.
- Explicit `status="pending"` searches by support/operations must continue to work.

## Non-Goals

- UI redesign or new UI features
- Changes to pet data structure or persistence
- Authentication or authorization changes
- Deployment or infrastructure changes
- Changes to adoption flow validation

## What Changes

- Fix the `search_pets()` function to treat empty status parameter as "available" (the documented default).
- Add regression tests to ensure pending pets never appear in default searches.
- Preserve the ability to explicitly search for pending pets when needed by support.

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets. Empty string status will be treated as "available".
- Tests: New regression tests added to prevent this bug from recurring.
- Humans: Customers will no longer see pending pets in the available catalog. Operations workflows can still explicitly query pending pets.

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge (automated review will be triggered)
- Merge approval: Required from human reviewer
- Deployment approval: Required before production deployment
