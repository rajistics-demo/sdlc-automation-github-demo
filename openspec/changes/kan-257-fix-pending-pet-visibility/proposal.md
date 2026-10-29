# Change: Fix Pending Pet Visibility in Catalog

## Why

Support reports that some customers are able to see and start adoption flows for pets with `status="pending"` that should not be visible in the default available-pets experience. This causes customer confusion and creates extra work for operations staff. Log evidence confirms the regression with error code `PENDING_PET_VISIBLE`, identifying pet-103 (Nova) appearing in available-pets search results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-257
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The empty-string status case occurs in practice (from UI code or API callers passing `""`)
- The default `status="available"` parameter is the intended behavior for customer-facing catalog
- The fix should preserve explicit `status="pending"` searches for support/operations workflows
- Wiki documentation at `docs/wiki/petstore-catalog-availability.md` represents current product requirements

## Non-Goals

- Changes to the adoption flow validation
- UI redesign or additional filtering features
- Database/persistence layer changes
- Deployment or infrastructure changes

## What Changes

Fix the `search_pets()` function in `app/petstore_app/catalog.py` to enforce the default `status="available"` filter even when an empty string is provided.

**Root cause:** When `status=""` is passed, the condition `if normalized_status and normalized_status != pet.status:` treats the empty string as falsy, bypassing the status filter and allowing pending pets through.

**Fix:** Treat empty or whitespace-only status as "available" by changing line 41 from:
```python
normalized_status = status.strip().lower()
```
to:
```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

## Impact

- App behavior: Pending pets will no longer appear in default search results, preventing customer confusion
- Tests: Add regression tests for empty status string and default behavior
- Humans: Operations support burden reduced; no approval required for straightforward bug fix

## Human Gates

- Scope approval: Not required (straightforward bug fix with clear requirements)
- Review approval: Required via `openhands-review` automation
- Merge approval: Required by repository owner
- Deployment approval: Required by operations team
