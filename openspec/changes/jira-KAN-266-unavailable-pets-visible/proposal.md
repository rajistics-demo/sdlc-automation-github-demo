# Change: Ensure unavailable pets are never shown to customers

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. Only pets with status="available" should appear in the customer-facing catalog.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-266
- Issue key: KAN-266
- Trigger: Jira webhook `jira:issue_created`
- Automation: `jira-to-story` (sdlc-story skill)

## Assumptions

- Nova maps to `pet-103` and has `status="pending"` in the Petstore seed data.
- The backend `search_pets()` function already correctly defaults to `status="available"`.
- The web UI must also filter to only show available pets.
- Explicit pending-pet searches (with `status="pending"`) should continue to work for support/ops workflows.
- The issue is specific to the customer-facing default catalog experience.

## Non-Goals

- Deployment changes, authentication, or data persistence changes.
- Payment processing or checkout functionality.
- Backend API changes (already working correctly).
- Unrelated UI redesign or feature additions.

## What Changes

- Add explicit test coverage verifying that default searches exclude pending pets.
- If UI code has gaps, ensure the web app filters match backend behavior.
- Add regression tests to prevent pending pets from appearing in available-only results.

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-266 reports customers seeing pets that should not be available yet.
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` states default catalog must show only `status="available"` pets.
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` contains `PENDING_PET_VISIBLE` error for Nova (`pet-103`).
- **Stop 4 - Repo/Files**: Backend (`app/petstore_app/catalog.py`) correctly filters; UI (`app/web/app.js`) also has filter.
- **Stop 5 - Tests/PR**: Add comprehensive test coverage and open draft PR for review.

## Impact

- App behavior: Customers see only available pets in the default catalog experience.
- Tests: Explicit test coverage for default search excluding pending pets.
- Humans: Reviewers approve the scope, implementation, and merge decision.

## Human Gates

- Scope approval: Jira issue describes the customer impact.
- Review approval: GitHub PR review with `openhands-review` label.
- Merge approval: Repository maintainers.
- Deployment approval: Outside this automation.
