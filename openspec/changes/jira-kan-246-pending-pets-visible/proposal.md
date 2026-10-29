# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are seeing and can start adoption flows for pets with `status="pending"`. This violates the product rule that default customer-facing catalog search must show only available pets. The `PENDING_PET_VISIBLE` error appears in production logs, confirming pending pets (specifically pet-103/Nova) are visible in the available-pets experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-246
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The status filter bypass is unintentional
- All legitimate callers either use the default `status="available"` or explicitly pass a valid status value
- Support and operations workflows that need pending pets already pass `status="pending"` explicitly
- No caller depends on bypassing the status filter with an empty string
- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data

## Non-Goals

- Change UI behavior (already correct - filters for status="available")
- Add new status values or states
- Modify adoption flow logic
- Change authentication or authorization
- Deployment changes or infrastructure modifications

## What Changes

- Fix catalog search status filter to prevent bypassing with empty strings
- Add validation that rejects empty status values
- Add test coverage for empty status rejection
- Existing behavior unchanged: default available-only search, explicit pending searches work

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-246 reports customers seeing pets that are not available
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default must be available-only
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with pet-103
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` status filter allows bypass with empty string
- `Stop 5 - Tests/PR`: Add validation test, run existing tests, draft PR for human review

## Impact

- App behavior: Customers see only available pets by default; empty status attempts fail fast
- Tests: Add empty status validation test; all existing tests pass
- Humans: Reviewers approve the fix scope and merge decision

## Human Gates

- Scope approval: Jira issue and PR review
- Review approval: GitHub PR review with `openhands-review` label
- Merge approval: Repository maintainers
- Deployment approval: Outside this automation
