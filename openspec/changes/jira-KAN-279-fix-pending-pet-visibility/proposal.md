# Change: Fix Pending Pet Visibility in Catalog

## Why

Customers are seeing pets in the adoption catalog that are not yet available for adoption. This happens when pets with "pending" status appear in the default available-pets search, creating confusion for customers and extra work for support teams. The catalog must show only available pets by default to prevent customers from starting adoption flows for pets that cannot yet be adopted.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-279
- Trigger: jira:issue_created
- Automation: Jira issue to draft pull request

## Assumptions

- The bug occurs when status filtering is bypassed by passing an empty status string
- The default behavior should always filter to available pets only
- Pending pets should only appear when explicitly requested with status="pending"
- No database or API changes are needed - this is a backend validation issue
- The fix can be deployed without customer data migration

## Non-Goals

- Changes to the pet data model or persistence layer
- Changes to authentication or authorization
- New deployment infrastructure
- UI redesign beyond what's needed to prevent the bug

## What Changes

- Backend catalog search validates that status filtering cannot be bypassed with empty strings
- Status parameter defaults to "available" and empty strings are normalized to the default
- Test coverage ensures pending pets never appear in default or available-only searches

## Impact

- App behavior: Empty status parameter now correctly filters to available pets instead of returning all pets
- Tests: New test added to verify empty status string behavior
- Humans: Support team will see fewer confused customers; operations workload reduced

## Human Gates

- Scope approval: Pending - awaiting confirmation this fix addresses the reported issue
- Review approval: Pending - awaiting code review
- Merge approval: Pending - requires passing tests and human review
- Deployment approval: Pending - requires merge approval first
