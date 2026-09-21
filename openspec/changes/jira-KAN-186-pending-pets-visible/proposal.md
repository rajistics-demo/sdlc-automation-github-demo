# Change: Fix Pending Pets Visible in Catalog

## Why

Support reports that customers are seeing and can start adoption flows for pets that should not be available yet. Pending pets must remain hidden from default customer-facing catalog searches to avoid confusion and extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-186
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira to PR

## Assumptions

- The catalog backend `search_pets()` function is the source of the bug
- Empty string status parameter (`status=""`) is being passed from some client or API layer
- The adoption safety check already prevents completing adoptions for pending pets
- Frontend already filters correctly; this is a backend-only fix
- No schema migration, API contract change, or new dependencies are required

## Non-Goals

- Changing the adoption flow validation (already works correctly)
- Modifying frontend filtering logic (already works correctly)
- Adding new status types beyond available/pending
- Investigating or fixing how empty status strings are being passed to the backend

## What Changes

- Backend catalog `search_pets()` function will treat empty status string the same as any other non-matching status value
- The status filter will always be applied when a status value is provided, even if it's an empty string
- Default searches continue to return only available pets

## Impact

- App behavior: Empty status parameter will no longer bypass the status filter, preventing pending pets from appearing in unintended searches
- Tests: New regression test added to verify empty status string returns only available pets
- Humans: Must review fix, approve PR, and merge; no deployment configuration changes required

## Human Gates

- Scope approval: Human approved Jira task creation
- Review approval: Humans review and approve the PR
- Merge approval: Humans merge when ready
- Deployment approval: Humans control deployment timing
