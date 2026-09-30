# Change: Fix unavailable pets appearing in default catalog search

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default catalog search must show only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-203
- Trigger: Jira webhook `issue_created`
- Automation: `jira-issue-to-pr`
- Evidence: `PENDING_PET_VISIBLE` log signal in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The catalog behavior is in `app/petstore_app/catalog.py`.
- Nova (pet-103) has `status="pending"` and should not appear in default available-only searches.
- Explicit pending-pet searches (with `status="pending"`) should continue to work for support and operations workflows.
- The bug occurs when the status parameter is passed as an empty string or other falsy value.

## Non-Goals

- Deployment configuration changes, authentication, data persistence, and unrelated UI changes are out of scope.
- Changes to adoption flow behavior are out of scope.

## What Changes

- The `search_pets()` function in `catalog.py` will enforce the "available" default status even when an empty string is passed.
- Default available-pets searches will exclude pending pets.
- Explicit pending-pet searches (with `status="pending"`) will continue to return pending pets when requested.
- Regression tests will verify that pending pets do not appear in default searches.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-203 reports customers seeing pets that are not available.
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for pet-103 (Nova).
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` lines 50-51 have a bug where empty status bypasses the filter.
- **Stop 5 - Tests/PR**: Regression tests added and draft PR opened for human review.

## Impact

- App behavior: customers will only see adoptable pets in default catalog searches.
- Tests: new regression test ensures empty status strings don't bypass the availability filter.
- Humans: reviewers approve the fix scope, code review, and merge decision.

## Human Gates

- Scope approval: Jira issue and GitHub PR review.
- Review approval: GitHub PR review with `openhands-review` label.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
