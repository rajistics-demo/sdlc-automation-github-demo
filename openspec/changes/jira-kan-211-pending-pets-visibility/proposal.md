# Change: Fix pending pets appearing in default catalog search

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The catalog must only show available pets by default.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-211
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log signal

## Assumptions

- The bug occurs when the status filter in `search_pets()` is bypassed due to empty status strings.
- Nova (`pet-103`) has `status="pending"` in the Petstore seed data and should not appear in default searches.
- Explicit pending-pet searches must continue to work when callers request `status="pending"`.
- No deployment, auth, persistence, or UI changes are needed.

## Non-Goals

- Changes to deployment settings, authentication, data persistence, or unrelated UI behavior are out of scope.
- Changes to pet status values or adoption workflow are out of scope.

## What Changes

- The `search_pets()` function always applies the status filter, preventing pending pets from appearing when they shouldn't.
- Default available-pets search excludes pending pets.
- Explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Focused regression tests ensure pending pets stay out of default searches.

## Evidence Waypoints

- `Stop 1 - Ticket`: KAN-211 reports customers seeing pets that are not available.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms default searches must show only available pets.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error code with `pet-103`.
- `Stop 4 - Repo/Files`: `app/petstore_app/catalog.py` contains the status filter logic; existing tests in `app/tests/test_pet_catalog.py`.
- `Stop 5 - Tests/PR`: New regression test added; validation passed; draft PR opened for human review.

## Impact

- App behavior: customers see only adoptable pets by default, preventing confusion and extra support work.
- Tests: catalog tests ensure default behavior excludes pending pets while explicit pending searches still work.
- Humans: reviewers approve the fix scope, review the code, approve merge, and control deployment.

## Human Gates

- Scope approval: Jira issue and GitHub PR review.
- Review approval: GitHub PR review (automated with `openhands-review` label).
- Merge approval: repository maintainers.
- Deployment approval: outside this automation.
