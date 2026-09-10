# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog should return only available pets by default, excluding pets with pending status.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-184
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log signal in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Pet Nova (`pet-103`) has `status="pending"` and should not appear in default catalog searches.
- The bug is in the backend `search_pets()` function in `app/petstore_app/catalog.py`.
- Explicit pending-pet searches (when callers pass `status="pending"`) should continue to work.
- The adoption flow already validates pet availability correctly.

## Non-Goals

- Deployment changes, auth, persistence, and unrelated UI changes are out of scope.
- Changes to the adoption flow validation logic (already working correctly).
- Frontend filtering logic (already correct in `app/web/app.js`).

## What Changes

- The status filter in `search_pets()` will always apply, preventing empty string bypass.
- Default available-pets search excludes pending pets reliably.
- Explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Focused regression tests verify pending pets don't appear in default searches.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-184 reports customers seeing unavailable pets.
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE`, affected pet `pet-103` (Nova).
- **Stop 4 - Repo/Files**: Bug identified in `app/petstore_app/catalog.py` line 50 - truthy check allows empty status to bypass filter.
- **Stop 5 - Tests/PR**: Regression tests added and draft PR created for human review.

## Impact

- App behavior: Customers see only adoptable pets by default, eliminating confusion.
- Tests: New tests verify pending pets are excluded from default searches.
- Humans: Reviewers approve the fix scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
