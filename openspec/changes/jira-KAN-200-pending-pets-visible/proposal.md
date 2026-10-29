# Change: Fix Pending Pets Appearing in Available Pets Search

## Why

Customers are currently able to see and interact with pets that have a "pending" status in the default available pets experience. This creates confusion and generates extra work for operations when customers try to adopt pets that should not yet be available. The default catalog search must return only pets with `status="available"` to maintain a clear customer experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-200
- Trigger: jira:issue_created
- Automation: Jira issue to draft pull request

## Assumptions

- The bug is isolated to the default search behavior in `search_pets()`.
- Explicit searches for `status="pending"` by support/operations should continue to work.
- The fix requires only filtering logic changes, no schema or data migrations.
- Existing test coverage for pending pet searches should remain unchanged.

## Non-Goals

- Changing the underlying pet data or status values.
- Modifying UI beyond what naturally flows from correct backend filtering.
- Adding new statuses or changing status lifecycle.
- Altering support/operations workflows that explicitly request pending pets.

## What Changes

- The `search_pets()` function in `app/petstore_app/catalog.py` will correctly filter out pending pets when `status="available"` is requested (the default).
- New test coverage will verify that the default search excludes pending pets.
- Existing test for explicitly searching pending pets will continue to pass.

## Impact

- App behavior: Default catalog searches will no longer return pets with `status="pending"`.
- Tests: Add regression test to verify pending pets stay out of default results.
- Humans: Customers will see only truly available pets; operations confusion will be reduced.

## Human Gates

- Scope approval: Required before implementation.
- Review approval: Required after PR creation (automated via `openhands-review` label).
- Merge approval: Required by human reviewer.
- Deployment approval: Required by authorized personnel.
