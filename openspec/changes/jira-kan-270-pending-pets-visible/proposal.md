# Change: Fix pending pets appearing in default available catalog

## Why

Support reports that customers can see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog must show only available pets in default searches.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-270
- Issue key: KAN-270
- Automation: `sdlc-story` (Jira webhook trigger)
- Evidence: `PENDING_PET_VISIBLE` log signal from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The request is limited to default catalog availability behavior (backend API).
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.
- The web UI already correctly filters by status; this is a backend bug.

## Non-Goals

- Deployment changes, auth, persistence, and unrelated UI changes are out of scope.
- No changes to the adoption flow logic (already validates status correctly).
- No changes to the data model or pet fixtures.

## What Changes

- Default available-pets search in `catalog.py` ensures status filtering always applies.
- When `status=""` is passed, it defaults to `"available"` to prevent bypassing the filter.
- Explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Focused regression tests cover the empty-status bug and confirm pending pets don't leak.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-270 sparse bug report says customers are seeing pets that are not available.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` states default search must show only available pets.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson`, error code `PENDING_PET_VISIBLE` with `pending_pet_ids: ["pet-103"]`.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 50 bug - empty status string bypasses filtering.
- `Stop 5 - Tests/PR`: Regression tests confirm fix, draft PR for human review.

## Impact

- App behavior: adopters see only adoptable pets by default, even when status is empty string.
- Tests: catalog tests cover default available behavior, explicit pending searches, and empty-status edge case.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue and PR review.
- Review approval: GitHub PR review (handed off to `openhands-review`).
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
