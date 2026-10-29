# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are seeing pets in the available-pets experience that should not be adoptable yet. This creates confusion and extra work for operations. The catalog search function incorrectly allows pending pets to appear in default search results when the status filter is bypassed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-249
- Trigger: jira:issue_created
- Automation: Jira issue to PR (sdlc-story)

## Assumptions

- The bug is in the catalog search logic, not in the UI or data layer
- Fixing the status filter logic is safe and won't break existing integrations
- Pending pets should never appear in default searches, only when explicitly requested
- The fix does not require schema changes or new dependencies

## Non-Goals

- Changing the UI beyond what's needed for verification
- Adding new status types beyond available/pending
- Modifying adoption workflow or operations tools
- Changing how explicit pending-pet searches work for support staff

## What Changes

- Remove the conditional check that allows the status filter to be bypassed in `catalog.py`
- Ensure status filtering is always applied, not just when status is truthy
- Add regression tests to prevent pending pets from appearing in default search

## Impact

- App behavior: Pending pets will no longer appear in default available-pets searches
- Tests: New regression test added to verify pending pets are excluded from default results
- Humans: Code review required; merge approval required; QA verification of UI behavior

## Human Gates

- Scope approval: Required before merge
- Review approval: Required (openhands-review handoff)
- Merge approval: Required by human reviewer
- Deployment approval: Required before production rollout
