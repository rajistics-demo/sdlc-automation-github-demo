# Change: Fix Pending Pet Visibility in Catalog

## Why

Customers are seeing pets with pending status in the default available-pets catalog search and can start adoption flows for pets that are not yet ready. This creates confusion for customers and extra work for operations staff who must handle invalid adoption requests.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-3
- Trigger: Jira issue created webhook
- Automation: EKS demo issue-to-PR automation

## Assumptions

- The bug is caused by the status filter accepting empty strings, which bypasses the availability check
- No API clients legitimately depend on empty status strings returning all pets
- The fix can be made entirely in the backend catalog search function
- No database schema or persistence changes are needed

## Non-Goals

- Changes to adoption workflow beyond catalog filtering
- UI redesign or additional catalog features
- Deployment or infrastructure changes
- Authentication or authorization changes
- New dependencies

## What Changes

- The `search_pets()` function will treat empty status strings the same as the default "available" status
- Pending pets will never appear in default catalog searches, even when status="" is passed
- Explicit `status="pending"` searches will continue to work for support workflows

## Impact

- App behavior: Default catalog search will consistently return only available pets, fixing the customer-facing bug
- Tests: Add regression tests to ensure empty status and default searches exclude pending pets
- Humans: Support workflows that explicitly request pending pets remain unchanged

## Human Gates

- Scope approval: Required before merging - confirm no API clients depend on empty status behavior
- Review approval: Required - code review must verify the fix and test coverage
- Merge approval: Required - human must approve the merge
- Deployment approval: Required - deployment timing is a human decision
