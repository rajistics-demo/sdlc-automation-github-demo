# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that some customers see and can start adoption flows for pets that should not be available yet. The catalog search function allows an empty status filter value, which bypasses the status check entirely, causing pending pets to appear in the available catalog.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-260
- Trigger: jira:issue_created
- Automation: Jira issue-to-PR workflow

## Assumptions

- The bug is limited to the status filter logic in catalog.py
- No database or persistence changes needed
- No authentication or authorization changes
- The fix applies to backend catalog search; UI changes are separate if needed

## Non-Goals

- Changes to adoption flow validation
- UI redesign or new UI features
- Changes to pending pet workflows
- Database schema changes
- Authentication or authorization changes

## What Changes

- Fix the status filter in `search_pets()` to properly handle empty status values
- Ensure the default `status="available"` is enforced even when empty strings are passed
- Add regression tests for empty status strings

## Impact

- App behavior: The default catalog will correctly show only available pets
- Tests: New regression tests added to prevent empty status bypass
- Humans: Reduced customer confusion and support workload

## Human Gates

- Scope approval: Pending - awaiting confirmation of fix approach
- Review approval: Pending - openhands-review automation
- Merge approval: Pending - human merge decision
- Deployment approval: Pending - human deployment decision
