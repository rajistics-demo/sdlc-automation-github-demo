# Change: Fix Pending Pets Visible in Default Catalog Search

## Why

Customers are seeing and attempting to adopt pets that are not yet available. Support reports indicate that pets with "pending" status appear in the default available-pets catalog experience, causing customer confusion and creating extra operational work. The catalog search must show only available pets by default, per business rules.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-258
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira issue to PR workflow

## Evidence Waypoints

- **Stop 1 - Ticket**: KAN-258 - "Customers are seeing pets that are not available"
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error for pet-103 (Nova)
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` - status filter bypassed when empty string passed
- **Stop 5 - Tests/PR**: Added regression test; PR link to be added after creation

## Root Cause

The `search_pets()` function in `catalog.py` has a logic bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string) is passed as a parameter, `normalized_status` becomes an empty string (falsy), causing the condition to short-circuit. The status filter is skipped entirely, returning ALL pets including pending ones.

The default parameter `status="available"` works correctly, but any caller passing an explicit empty string bypasses the filter.

## Assumptions

- The fix should enforce non-empty status values while preserving backward compatibility with the default `status="available"` parameter.
- Support and operations workflows that explicitly request `status="pending"` must continue to work.
- No schema, persistence, authentication, or deployment changes are required.
- This is a backend logic fix; the UI already filters correctly.

## Non-Goals

- Changing the UI (it already filters by `status === "available"`)
- Adding new pet statuses beyond "available" and "pending"
- Modifying the pets database or persistence layer
- Changing authentication, authorization, or access control
- Deployment configuration changes

## What Changes

- Add validation to reject empty or whitespace-only status values
- Preserve the default `status="available"` parameter behavior
- Add regression tests to verify empty status is rejected and pending pets are excluded from default searches

## Impact

- **App behavior**: The catalog will correctly reject searches with empty status values, ensuring only available pets appear in default searches
- **Tests**: New test cases added to verify empty status rejection and default search behavior
- **Humans**: Operations team will no longer receive support tickets about customers seeing unavailable pets

## Human Gates

- **Scope approval**: Automated (Jira issue creation triggered this workflow)
- **Review approval**: Human reviewer must approve the PR
- **Merge approval**: Human must approve merge to main
- **Deployment approval**: Human must approve deployment to production
