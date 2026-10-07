# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default catalog search must exclude pending pets and show only available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-199
- Issue key: KAN-199
- Title: "Customers are seeing pets that are not available"
- Automation: `sdlc-story` (Jira webhook triggered)
- Evidence: `PENDING_PET_VISIBLE` log signal from `docs/logs/pending-pet-visible.ndjson`

## Assumptions

- Nova maps to `pet-103` with `status="pending"` in the Petstore catalog (confirmed in wiki).
- The investigation focuses on default catalog availability behavior in both backend and frontend.
- Explicit pending-pet searches (`status="pending"`) should continue to work when explicitly requested.
- Frontend UI filter may be missing the status check for available pets.
- Backend adoption validation already prevents pending pet adoptions (verified in `adoptions.py` line 34-35).

## Non-Goals

- Deployment changes, authentication, database persistence, and unrelated UI features are out of scope.
- Schema changes or new dependencies are not required.
- Backend adoption flow is already protected and doesn't need changes.

## What Changes

- Verify and fix frontend UI filter to exclude pending pets in default view (`app/web/app.js`).
- Verify that backend default search excludes pending pets (`app/petstore_app/catalog.py` - already correct).
- Ensure explicit pending-pet searches still return pending pets when `status="pending"` is requested.
- Run regression tests to prove pending pets stay out of default available results.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-199 reports "Customers are seeing pets that are not available" - specifically pending pets like Nova.
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms Nova is pet-103 with status="pending" and that PENDING_PET_VISIBLE logs indicate catalog regressions.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows ERROR with code PENDING_PET_VISIBLE for pet-103 on 2026-06-29.
- **Stop 4 - Repo/Files**: Backend catalog filtering (already correct with default status="available"), frontend UI filter needs verification, adoption flow already protected.
- **Stop 5 - Tests/PR**: Backend tests pass, UI smoke test available if Playwright is installed, draft PR created with evidence.

## Impact

- App behavior: Customers see only available pets in default catalog search on the web UI.
- Tests: Existing backend tests verify correct behavior; UI tests document expected behavior.
- Humans: Reviewers approve scope, merge, and deployment decisions.

## Human Gates

- Scope approval: Jira issue triage and automation trigger.
- Review approval: GitHub PR review (openhands-review label added).
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation scope.
