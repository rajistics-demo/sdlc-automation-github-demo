# Change: Fix Pending Pets Appearing in Default Search

## Why

Customers report seeing pets that should not be available yet in the default adoption catalog. This violates the product requirement that only available pets appear in default search results. Pending pets should only be visible when explicitly requested by support or operations workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-214
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The bug is limited to the catalog search logic; no UI, database, or API changes are needed.
- Existing tests for pending pet searches (when explicitly requested) should continue to pass.
- The fix can be safely deployed without data migration or configuration changes.

## Non-Goals

- Changing pending pet workflow or status transitions.
- Modifying adoption flow behavior.
- Adding new UI features or search filters.
- Updating deployment configuration or secrets.

## What Changes

- Fix `search_pets()` function in `app/petstore_app/catalog.py` to enforce the default `status="available"` filter even when an empty status is passed.
- Add regression test to ensure pending pets never appear in default search results.

## Impact

- App behavior: Default search will correctly exclude pending pets. Explicit pending searches remain unchanged.
- Tests: One new regression test added; all existing tests should pass.
- Humans: Requires PR review and merge approval before deployment.

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required via `openhands-review` label
- Merge approval: Required - human merges only
- Deployment approval: Required before production deployment
