# Change: Fix Pending Pets Visible in Default Search

## Why

Support reports that customers are seeing and can start adoption flows for pets with `status="pending"` that should not be visible in the default available-pets experience. This violates the product rule that "Default pet search returns only available pets" and creates customer confusion and operational overhead.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-194
- Trigger: Jira webhook (issue_created)
- Automation: jira-to-pr automation

## Assumptions

- The bug is in the `search_pets()` function in `app/petstore_app/catalog.py`
- The issue occurs when `status=""` (empty string) is passed, bypassing the status filter
- No external callers rely on empty-string-bypasses-filter behavior
- Existing pending-pet-specific searches with `status="pending"` will continue to work
- Log evidence `PENDING_PET_VISIBLE` in docs/logs/pending-pet-visible.ndjson confirms the regression

## Non-Goals

- Not adding new pet statuses or catalog features
- Not modifying adoption flow business logic
- Not changing the UI or API contracts
- Not altering authentication or authorization
- Not requiring schema or deployment changes

## What Changes

- Fix the status filter logic in `search_pets()` to normalize empty status to "available"
- Ensure the status filter is always applied, not bypassed by falsy values
- Add regression tests to verify pending pets never appear in default searches
- Verify explicit `status="pending"` searches still work for support workflows

## Impact

- App behavior: Pending pets will be correctly excluded from default catalog searches
- Tests: New regression tests added to prevent future occurrences
- Humans: Customer confusion eliminated, operations workload reduced

## Human Gates

- Scope approval: Required before implementation proceeds
- Review approval: Required via openhands-review label workflow
- Merge approval: Human reviewer must approve PR
- Deployment approval: Human must approve production deployment
