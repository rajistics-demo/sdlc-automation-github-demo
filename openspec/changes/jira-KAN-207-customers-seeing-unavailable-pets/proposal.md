# Change: Fix customers seeing unavailable pets

## Why

Support reports that customers are seeing and starting adoption flows for pets with `status="pending"`. This violates the Petstore product rule that default pet search should return only available pets. The `PENDING_PET_VISIBLE` error log confirms this regression.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-207
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` error code in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- The default behavior should filter to `status="available"` when no status is specified or an empty status is provided.
- Explicit requests for `status="pending"` should continue to work for support workflows.
- Nova maps to `pet-103` and has `status="pending"` in the seed data.
- No schema, deployment, or environment changes are needed.
- Existing pets fixture data is correct.

## Non-Goals

- Do not add new status values.
- Do not change the UI beyond what default backend behavior provides.
- Do not alter authentication, authorization, or deployment settings.
- Do not add new dependencies.

## What Changes

- Default available-pets search excludes pending pets.
- Explicit pending-pet searches still return pending pets when requested.
- Focused regression tests cover the pending-pet visibility bug.

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-207 sparse bug report says "customers are seeing pets that are not available".
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default must be available-only.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with `pet-103`.
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 41/50 has the filter bug.
- **Stop 5 - Tests/PR**: regression tests added, validation passed, draft PR created.

## Impact

- App behavior: customers see only adoptable pets by default.
- Tests: catalog tests cover default available behavior and explicit pending searches.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
