# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This creates confusion for customers and extra work for operations. The default catalog search must return only available pets, never pending pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-264
- Trigger: jira:issue_created
- Automation: Jira issue to draft pull request

## Assumptions

- The bug is in the catalog search filter logic where empty status strings bypass the status filter
- Nova (pet-103) with status="pending" is the known test case from logs
- No deployment, auth, secrets, or persistence changes are needed
- Fixing the filter logic in `catalog.py` is sufficient

## Non-Goals

- Changes to pending pet workflows or support tools
- UI redesign or new catalog features
- Deployment or infrastructure changes
- Database or persistence changes

## What Changes

- Fix the status filter in `search_pets()` to properly handle empty status strings
- Ensure that only pets with status="available" are returned by default
- Ensure that explicit status filters (including empty string) are properly enforced
- Add regression tests to prevent pending pets from appearing in available-only searches

## Impact

- App behavior: Customers will no longer see pending pets in the default catalog
- Tests: New regression tests ensure the bug does not return
- Humans: Operations team will see reduced confusion and support tickets

## Human Gates

- Scope approval: pending (human review of OpenSpec artifacts)
- Review approval: pending (code review via openhands-review)
- Merge approval: pending (human decision)
- Deployment approval: pending (human decision)
