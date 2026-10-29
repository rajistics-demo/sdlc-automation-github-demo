# Change: Fix Pending Pet Visibility Bug

## Why

Support reports that customers are able to see and start adoption flows for pets that should not be available yet. This violates the Petstore product rule that default pet search returns only available pets. Pending pets should only appear when explicitly requested and cannot be adopted. This bug is confusing customers and creating extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-189
- Trigger: jira:issue_created
- Automation: SDLC Request To PR via Jira webhook

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-189 reports customers seeing unavailable pets
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` confirms default search must show only `status="available"` pets
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for Nova (pet-103) appearing in available-pets experience
- **Stop 4 - Repo/Files**: Bug found in `app/petstore_app/catalog.py` line 50 - status filter bypassed when empty string passed
- **Stop 5 - Tests/PR**: Missing test coverage for empty status parameter; fix and tests will be added in this PR

## Root Cause

The `search_pets()` function in `app/petstore_app/catalog.py` line 50 has a filter condition:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, the `and` operator causes short-circuit evaluation. Since empty string is falsy, the entire condition evaluates to `False` and the status filter is completely bypassed. This allows pending pets to appear in search results.

## Assumptions

- The fix should make status filtering consistent with species and tag filtering patterns
- Empty status strings should default to "available" behavior (match the parameter default)
- No external API consumers depend on the empty-string bypass behavior
- The frontend is safe due to hardcoded `status === "available"` filter
- This is a backend-only fix; no UI changes required

## Non-Goals

- Changing adoption flow validation (already works correctly)
- Modifying frontend filtering (already works correctly)
- Adding new status values beyond "available" and "pending"
- Performance optimization or caching
- API versioning or breaking changes

## What Changes

- Remove the truthiness check from the status filter in `app/petstore_app/catalog.py` line 50
- Add regression test to verify empty status parameter does not bypass filtering
- Add test to validate that explicit status values continue to work correctly

## Impact

- **App behavior**: Backend API will correctly filter out pending pets even when `status=""` is passed
- **Tests**: New test coverage for edge case ensures regression protection
- **Humans**: Operations team will see reduced confusion reports; review and merge approval required

## Human Gates

- **Scope approval**: ✅ Within bounded bug fix scope; no infrastructure or schema changes
- **Review approval**: Required - PR will be marked as draft for human review
- **Merge approval**: Required - humans must approve before merge
- **Deployment approval**: Required - humans control deployment timing
