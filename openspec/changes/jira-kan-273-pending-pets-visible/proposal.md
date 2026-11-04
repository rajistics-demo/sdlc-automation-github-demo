# Change: Fix pending pets appearing in available catalog

## Why

Support reports that customers are seeing pets marked as pending in the adoption flow. These pets are not yet available for adoption, which confuses customers and creates extra operations work. The default catalog search must exclude pending pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-273
- Issue key: KAN-273
- Trigger: Jira webhook `jira:issue_created`
- Automation: `sdlc-story` via Jira automation

## Assumptions

- Nova (pet-103) has `status="pending"` in the Petstore catalog data.
- The bug is in the catalog search filter logic when status is an empty string.
- Explicit `status="pending"` searches should continue to work for operations workflows.
- No database, auth, deployment, or dependency changes are needed.

## Non-Goals

- Persistence or database changes
- Authentication or authorization changes
- Deployment configuration
- UI redesign beyond what the filter fix naturally provides
- New dependencies

## What Changes

- Catalog search filter logic correctly handles empty status parameter
- Default and explicit `status="available"` searches exclude pending pets
- Explicit `status="pending"` searches continue to work for operations
- Regression tests prevent empty status from bypassing filter

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-273 sparse report: "customers are able to see and start adoption flows for pets that should not be available yet"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` states default search must show only `status="available"` pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error with Nova (pet-103)
- **Stop 4 - Repo/Files**: Bug confirmed in `app/petstore_app/catalog.py` line 50 - empty status string bypasses filter
- **Stop 5 - Tests/PR**: Regression test, fix implementation, validation, and draft PR

## Impact

- **App behavior**: Customers see only available pets in default searches, pending pets appear only in explicit pending-status queries
- **Tests**: New regression test for empty status, existing tests continue to pass
- **Humans**: Review approval required; humans control merge and deployment

## Human Gates

- **Scope approval**: Jira issue review and PR review
- **Review approval**: GitHub PR review with `openhands-review` handoff
- **Merge approval**: Repository maintainers control merge decision
- **Deployment approval**: Outside this automation scope
