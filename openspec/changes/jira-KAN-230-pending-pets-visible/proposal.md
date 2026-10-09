# Change: Fix Pending Pets Appearing in Available Search

## Why

Customers are seeing pets in the adoption catalog that aren't actually available for adoption yet. When pets have a "pending" status (meaning they're going through intake, training, or other preparation), they should not appear in the default customer-facing search results. This creates confusion and extra work for support and operations teams.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-230
- Trigger: jira:issue_created
- Automation: Jira issue to draft pull request

## Assumptions

- The bug affects the default available-pets search in `catalog.py`
- The status filter logic has a defect where empty or whitespace-only status values bypass the filter
- Fixing this requires only a code change to the status validation, not a schema or data migration
- Existing tests for explicit `status="pending"` searches should continue to work (support workflows need this)

## Non-Goals

- Changing the pet data structure or status values
- Modifying UI beyond what's necessary for correctness
- Adding new pet statuses or workflow states
- Changing how explicit `status="pending"` searches work for support staff

## What Changes

- Update `search_pets()` in `catalog.py` to enforce `status="available"` as the default when an empty string is provided
- Add regression tests to prove pending pets stay out of default search results
- Validate that explicit pending searches still work for support workflows

## Impact

- App behavior: Default catalog search will correctly exclude pending pets; only available pets will be shown to customers
- Tests: New tests will prevent this regression from happening again
- Humans: Support team workload should decrease as customers no longer see unavailable pets

## Human Gates

- Scope approval: Required before implementation (approved via Jira ticket creation)
- Review approval: Required via GitHub PR review process
- Merge approval: Required by repository maintainer
- Deployment approval: Required before production deployment
