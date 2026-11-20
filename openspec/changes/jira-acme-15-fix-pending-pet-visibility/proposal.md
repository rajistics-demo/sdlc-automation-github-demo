# Change: Fix Pending Pet Visibility in Catalog Search

## Why

Support reports that customers are seeing pets with "pending" status in their search results when they shouldn't. This creates confusion and extra operational work when customers attempt to start adoption flows for pets that are not yet available.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-15
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo (EKS)

## Assumptions

- The product rule is that default search returns only available pets.
- Pending pets should appear only when status is explicitly requested as "pending".
- Empty or whitespace-only status parameters should be treated as "available" (the default).
- The fix is scoped to the backend catalog search logic; UI already filters correctly.

## Non-Goals

- Changes to the UI (already working correctly)
- Changes to database schema or persistence layer
- Changes to adoption workflow or validation
- New authentication or authorization logic
- Infrastructure or deployment changes

## What Changes

- Backend `search_pets()` function will properly filter out pending pets when status is empty or whitespace
- Status filter logic will treat empty status parameter as "available" instead of skipping the filter entirely

## Impact

- App behavior: Default and empty-status searches will correctly exclude pending pets
- Tests: Add regression test for empty status parameter
- Humans: Code review approval required; merge approval required

## Human Gates

- Scope approval: ✅ Scoped to catalog filtering logic
- Review approval: Pending human review
- Merge approval: Pending human decision
- Deployment approval: Pending human decision
