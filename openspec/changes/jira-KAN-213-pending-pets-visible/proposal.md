# Change: Fix Pending Pets Showing in Available Pet Search

## Why

Customers are seeing pets that are not yet available for adoption, which creates confusion and generates unnecessary support requests. The default pet search must return only pets with `status="available"` to provide a clear customer experience and reduce operational overhead.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-213
- Trigger: Jira webhook (issue created)
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The bug affects the `search_pets` function in `app/petstore_app/catalog.py`.
- Empty status strings bypass the availability filter, allowing pending pets to appear.
- Fixing the filter logic is safe and does not require database or schema changes.
- Existing explicit `status="pending"` searches for support workflows must continue working.

## Non-Goals

- Changing the pet data model or adding new pet statuses.
- Modifying UI components beyond what's necessary for this bug fix.
- Adding user authentication or access control.
- Implementing new search features or filters.

## What Changes

- Update the `search_pets` status filter to handle empty strings correctly.
- Ensure default searches always filter to `status="available"`.
- Add regression test to verify pending pets never appear in default available searches.

## Impact

- App behavior: Default pet searches will correctly exclude pending pets.
- Tests: New regression test added to prevent future occurrences.
- Humans: Requires code review and merge approval before deployment.

## Human Gates

- Scope approval: Humans approve the fix approach and implementation plan.
- Review approval: Code review via `openhands-review` label triggers review automation.
- Merge approval: Humans approve and merge the PR.
- Deployment approval: Humans control when the fix deploys to production.
