# Change: Fix pending pets visible in available-pets search

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. According to repository documentation (`docs/wiki/petstore-catalog-availability.md`), the default customer-facing catalog must show only pets with `status="available"`. Log evidence (`docs/logs/pending-pet-visible.ndjson`) confirms a `PENDING_PET_VISIBLE` error with `pending_pet_ids: ["pet-103"]` (Nova, the pending dog). This is confusing customers and creating extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-243
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-issue-to-pr`
- Evidence: `PENDING_PET_VISIBLE` log signal in `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore catalog data.
- The request is limited to default catalog availability behavior.
- Explicit pending-pet searches must continue to work when support/operations callers request `status="pending"`.
- The UI (`app/web/app.js`) correctly filters for available pets; this is a backend-only fix.
- No external API clients are relying on the buggy behavior of `status=""` returning all pets.

## Non-Goals

- UI changes are out of scope; the static UI already filters correctly.
- New catalog features (age filters, fee filters, etc.) are out of scope.
- Pet data structure or PETS fixture changes are out of scope.
- Deployment changes, auth, persistence, secrets, and unrelated behavior are out of scope.

## What Changes

- Status normalization in `search_pets()` treats empty or whitespace-only status strings as `"available"`.
- Default available-pets search continues to exclude pending pets.
- Explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Regression test added to prove empty status strings return only available pets.

## Evidence Waypoints

- `Stop 1 - Ticket`: Jira KAN-243 sparse bug report says customers are seeing pets that are not available.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default search must be available-only.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103 (Nova).
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` lines 41-42: empty status bypasses filter due to falsy check.
- `Stop 5 - Tests/PR`: Regression tests and draft PR for human review.

## Impact

- App behavior: customers see only adoptable pets in default search; pending pets are hidden.
- Tests: catalog tests cover empty status edge case and confirm explicit pending searches still work.
- Humans: reviewers approve the product scope, implementation, and merge decision.

## Human Gates

- Scope approval: Jira issue and GitHub PR review.
- Review approval: GitHub PR review.
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
