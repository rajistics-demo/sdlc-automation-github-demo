# Change: Fix Pending Pets Showing in Available Search

## Why

Support reports that customers are seeing pets that should not be available yet, specifically pending pets appearing in the default available-pets experience. This creates customer confusion and extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-196
- Trigger: Jira webhook issue_created event
- Automation: sdlc-story via Jira request-to-PR workflow

## Assumptions

- The catalog status filter logic has a bug where empty status strings bypass the filter entirely
- Default search behavior should always filter to available pets only
- Pending pets should only appear when explicitly requested with status="pending"
- No schema or data migration is required
- The fix is isolated to catalog.py filtering logic

## Non-Goals

- Changes to pet data model or database schema
- UI changes to how pets are displayed
- Changes to adoption workflow or business rules beyond catalog filtering
- Performance optimization or caching

## What Changes

- Catalog search filter will reject empty status strings and enforce default available-only filtering
- Add regression test to prove pending pets stay out of default available results
- Add test coverage for empty status parameter edge case

## Impact

- App behavior: Default searches will correctly exclude pending pets; empty status parameter will be treated as invalid input
- Tests: New regression tests added to prevent recurrence of PENDING_PET_VISIBLE error
- Humans: Operations will see reduced customer confusion and support tickets

## Human Gates

- Scope approval: Required from product owner before merge
- Review approval: Required via openhands-review automation and human reviewer
- Merge approval: Required from maintainer
- Deployment approval: Required before production rollout
