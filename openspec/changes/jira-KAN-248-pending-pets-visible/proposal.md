# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are seeing pets that are not available yet. Adoption flows are being started for pending pets, confusing customers and creating extra work for operations. The catalog must show only available pets by default.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-248
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-issue-to-pr`

## Assumptions

- The bug occurs when empty status strings bypass the status filter in `search_pets()`
- Nova is `pet-103` with `status="pending"` in the seed data
- Explicit pending-pet searches for support workflows should continue working
- Money is represented as integer cents (unchanged)

## Non-Goals

- UI changes (static UI already exists and is working)
- Adoption flow logic changes
- Pet data structure modifications
- Deployment or infrastructure changes

## What Changes

- Status filtering in `search_pets()` treats empty status as "available"
- Default catalog search excludes pending pets
- Explicit `status="pending"` searches continue to work for support workflows
- Regression test added for empty status parameter

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-248 reports customers seeing unavailable pets in adoption flows
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only available pets
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103 (Nova)
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 41-50 has filter bypass bug
- `Stop 5 - Tests/PR`: Regression test and draft PR for human review

## Impact

- App behavior: customers see only adoptable pets by default
- Tests: catalog tests cover empty status regression and explicit pending searches
- Humans: reviewers approve scope, review, merge, and deployment decisions

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review
- Merge approval: repository maintainers
- Deployment approval: outside this automation
