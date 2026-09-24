# Change: Verify pending pets are excluded from available catalog

## Why

Support reports that Nova is showing up in the available-pets list even though she should not be adoptable. The default catalog search must exclude pending pets and show only available pets.

## Source

- GitHub issue: https://github.com/rajistics-demo/sdlc-automation-github-demo/issues/67
- Trigger label: `openhands-build`
- Automation: `sdlc-story`
- Evidence: `PENDING_PET_VISIBLE` log signal from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` with `status="pending"` in the Petstore catalog.
- The investigation focuses on default catalog availability behavior in both backend and frontend.
- Explicit pending-pet searches (`status="pending"`) should continue to work when explicitly requested.
- This is a verification and regression test task; existing code may already be correct.

## Non-Goals

- Deployment changes, authentication, database persistence, and unrelated UI features are out of scope.
- Schema changes or new dependencies are not required.

## What Changes

- Verify that default available-pets search excludes pending pets in backend (`app/petstore_app/catalog.py`).
- Verify that frontend UI filter excludes pending pets (`app/web/app.js`).
- Ensure explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Add or verify focused regression tests that prove pending pets stay out of default available results.

## Evidence Waypoints

- `Stop 1 - Ticket`: Issue #67 reports "Customers are seeing pets that are not available" - specifically Nova.
- `Stop 2 - Wiki/Docs`: `docs/wiki/petstore-catalog-availability.md` confirms Nova is pet-103 with status="pending" and that PENDING_PET_VISIBLE logs indicate catalog regressions.
- `Stop 3 - Logs`: `docs/logs/pending-pet-visible.ndjson` shows ERROR with code PENDING_PET_VISIBLE for pet-103 on 2026-06-29.
- `Stop 4 - Repo/Files`: Backend catalog filtering and frontend UI filter code reviewed; tests executed.
- `Stop 5 - Tests/PR`: Regression tests validated; evidence posted to issue or PR created if code changes needed.

## Impact

- App behavior: Customers see only available pets in default catalog search.
- Tests: Focused catalog tests verify pending-pet exclusion from default searches.
- Humans: Reviewers approve scope, merge, and deployment decisions.

## Human Gates

- Scope approval: GitHub issue review.
- Review approval: GitHub PR review (if code changes are needed).
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
