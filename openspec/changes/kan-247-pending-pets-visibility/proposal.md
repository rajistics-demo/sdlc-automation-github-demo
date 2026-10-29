# Change: Fix pending pets appearing in available catalog

## Why

Support reports that Nova appears in the available-pets experience even though she is not adoptable. The catalog should not show pending pets in default available results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-247
- Issue: "Customers are seeing pets that are not available"
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` error code in logs

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The bug occurs when `search_pets()` is called with an explicit empty string for the status parameter (`status=""`).
- The request is limited to default catalog availability behavior.
- Explicit pending-pet searches should continue to work when callers request `status="pending"`.

## Non-Goals

- Deployment changes, auth, persistence, and unrelated UI changes are out of scope.
- Changes to the web UI filtering logic (already correct).

## What Changes

- Fix `search_pets()` in `app/petstore_app/catalog.py` to enforce the default `status="available"` filter even when empty string is passed.
- Default available-pets search excludes pending pets.
- Explicit pending-pet searches still return pending pets when requested.
- Focused regression tests cover the pending-pet visibility bug.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-247 says "Customers are seeing pets that are not available" and mentions Nova specifically.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms Nova is pet-103 with status="pending" and must not appear in default available-pets experience.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error code with `pending_pet_ids: ["pet-103"]`.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` line 50 has a bug where `normalized_status` can be empty string, bypassing the status filter entirely.
- `Stop 5 - Tests/PR`: Regression test added and draft PR opened for human review.

## Impact

- App behavior: adopters see only adoptable pets by default, even if API is called with `status=""`.
- Tests: catalog tests cover default available behavior, explicit empty string status, and explicit pending searches.
- Humans: reviewers approve the product scope and merge decision.

## Human Gates

- Scope approval: Jira issue KAN-247 and PR review.
- Review approval: GitHub PR review via `openhands-review` label.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
