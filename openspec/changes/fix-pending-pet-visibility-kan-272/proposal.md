# Change: Fix Pending Pet Visibility in Catalog Search

## Why

Support reports that customers can see and start adoption flows for pets that are not yet available. Specifically, Nova (pet-103) with `status="pending"` appears in default catalog searches when it should only be visible in explicit pending-pet queries. This confuses customers and creates extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-272
- Trigger: Jira issue created webhook
- Automation: jira-to-story automation

## Assumptions

- The bug is in `catalog.py` where empty status strings bypass the status filter
- Fixing the status filter logic is safe and does not require schema changes
- The existing test suite provides adequate coverage for the fix
- No deployment, auth, or infrastructure changes are needed

## Non-Goals

- Changes to the adoption workflow or validation
- UI redesign or new UI features
- Changes to pet data structure or persistence
- New dependencies or deployment configuration

## What Changes

- Update the status filter logic in `catalog.py` to ensure empty status strings default to "available"
- Add regression tests to verify empty status parameters don't expose pending pets
- Add test to verify default searches exclude pending pets

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets even when status parameter is empty
- Tests: Added regression tests for empty status handling and default search behavior
- Humans: Customers will no longer see pending pets in default available-pet searches

## Human Gates

- Scope approval: Required before opening PR
- Review approval: Required via `openhands-review` label
- Merge approval: Required from human reviewer
- Deployment approval: Required before production release
