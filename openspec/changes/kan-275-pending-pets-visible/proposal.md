# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default catalog search must show only pets with `status="available"`, but the current implementation allows the status filter to be bypassed when an empty status string is passed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-275
- Trigger: Jira issue created
- Automation: jira-issue-to-pr (sdlc-story skill)

## Assumptions

- The backend `search_pets` function is the source of truth for catalog filtering.
- The status parameter should always be applied, not conditionally based on whether it's truthy.
- No deployment, auth, schema, or infrastructure changes are needed.
- The fix is a one-line logic correction in the catalog search filter.

## Non-Goals

- Changes to the web UI (already correctly filters by available status).
- Changes to data persistence or pet status management.
- Changes to adoption workflows or validation.
- New dependencies or infrastructure changes.

## What Changes

- Fix the status filter logic in `catalog.py` to always apply the status filter, even when an empty string might be passed.
- Add regression tests to ensure empty status strings don't bypass the filter.

## Impact

- App behavior: Prevents pending pets from appearing in available-pets searches when an empty status filter is passed.
- Tests: Add regression tests for empty status handling.
- Humans: Requires review approval, merge approval, and deployment approval.

## Human Gates

- Scope approval: Pending (confirm this fix addresses the reported issue)
- Review approval: Pending (PR review required before merge)
- Merge approval: Pending (human must approve and merge the PR)
- Deployment approval: Pending (human must approve deployment to production)
