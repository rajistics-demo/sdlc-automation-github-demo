# Change: Fix Pending Pets Visibility in Catalog

## Why

Customers are seeing pets with "pending" status in the available pets catalog and can start adoption flows for them. This violates the product rule that only available pets should appear in the default customer experience. The bug causes confusion for customers and creates extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-267
- Trigger: Jira webhook `jira:issue_created` event
- Automation: SDLC Story automation (Jira-to-PR workflow)

## Assumptions

- The bug is a catalog filtering issue, not a status data problem
- The backend `search_pets` function has a logic error when handling empty or whitespace-only status values
- Fixing the filter logic is safe and does not require schema or deployment changes
- Nova (pet-103) is the known pending pet referenced in logs and wiki documentation

## Non-Goals

- Changing pet status data or adding new statuses
- Modifying adoption order validation (already correct)
- Redesigning the UI or adding new catalog features
- Changing authentication, authorization, or deployment settings
- Adding new dependencies or infrastructure changes

## What Changes

- Fix the status filter logic in `catalog.py` to ensure pending pets never appear in default searches
- Add regression tests to verify default searches exclude pending pets
- Add tests to verify empty-string status parameter doesn't bypass filtering
- Preserve existing behavior for explicit `status="pending"` searches

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets; operations can still search explicitly for pending pets
- Tests: New regression tests added to prevent the bug from recurring
- Humans: PR review and merge approval required; no deployment changes needed

## Human Gates

- Scope approval: Automated via Jira trigger with `openhands-build` workflow
- Review approval: Required before merge
- Merge approval: Required by branch protection
- Deployment approval: Standard deployment process (no special approval needed for this bug fix)
