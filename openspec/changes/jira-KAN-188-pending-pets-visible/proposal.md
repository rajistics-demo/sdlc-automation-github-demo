# Change: Fix pending pets appearing in default available catalog

## Why

Support reports that customers are seeing and attempting to adopt pets that should not be available yet. The default catalog search must exclude pending pets and show only available pets. This is confusing customers and creating extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-188
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story` via Jira webhook automation
- Evidence: `PENDING_PET_VISIBLE` log signal from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The bug occurs when `search_pets()` receives an empty string for the `status` parameter.
- Existing code that passes `status="available"` or `status="pending"` explicitly works correctly.
- The bug is in the truthy check logic on line 50 of `catalog.py`.
- No schema changes, new dependencies, or deployment changes are required.
- Explicit pending-pet searches (`status="pending"`) should continue to work when explicitly requested.

## Non-Goals

- Deployment changes, authentication, database persistence are out of scope.
- Schema changes or new dependencies are not required.
- Changes to adoption validation logic (already correct).
- Changes to UI filtering logic (already correct).

## What Changes

- Fix the status filter logic in `app/petstore_app/catalog.py` to properly handle empty string status values.
- Ensure empty string status is treated as the default `"available"` status.
- Add focused regression tests to verify pending pets are excluded from default searches.
- Add test coverage for empty string status parameter edge case.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-188 reports "Customers are seeing pets that are not available" with description stating support reports and customer confusion.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default catalog must show only available pets and that pending pets appear only when explicitly requested.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows ERROR with code PENDING_PET_VISIBLE for pet-103 (Nova) on 2026-06-29, indicating catalog regression with safe-to-fix signal.
- `Stop 4 - Repo/Files`: Bug identified in `app/petstore_app/catalog.py` line 50 - truthy check on `normalized_status` bypasses filter when empty string is passed.
- `Stop 5 - Tests/PR`: Regression tests added and validated; draft PR opened with fix and evidence.

## Impact

- App behavior: Default catalog search correctly excludes pending pets even when `status=""` is passed.
- Tests: New test coverage for empty string status parameter and default behavior verification.
- Humans: Reviewers approve scope, review, merge, and deployment decisions.

## Human Gates

- Scope approval: Jira issue acceptance.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
