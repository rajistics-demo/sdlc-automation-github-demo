# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are reporting that they can see pets that should not be available yet, causing confusion and creating extra work for operations. The default catalog search must return only available pets, but pending pets like Nova (pet-103) are appearing in search results when the status filter is bypassed with an empty string value.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-180
- Trigger: Jira webhook (issue_created)
- Automation: sdlc-automation-github-demo Jira-to-PR workflow

## Evidence Waypoints

### Stop 1 - Ticket
- **Jira KAN-180**: "Customers are seeing pets that are not available"
- Symptom: Customers able to see and start adoption flows for unavailable pets
- Impact: Customer confusion and operational overhead

### Stop 2 - Wiki/Docs
- **Path**: `docs/wiki/petstore-catalog-availability.md`
- **Rule**: "Default customer-facing catalog search must show only pets with `status="available"`"
- **Requirement**: Pending pets must not appear in default available-pets experience

### Stop 3 - Logs
- **Path**: `docs/logs/pending-pet-visible.ndjson`
- **Error Code**: `PENDING_PET_VISIBLE`
- **Timestamp**: 2026-06-29T12:00:00Z
- **Affected Pet**: pet-103 (Nova, status="pending")
- **Message**: "Pending pets were visible in the available-pets experience"

### Stop 4 - Repo/Files
- **Bug Location**: `app/petstore_app/catalog.py`, line 50
- **Root Cause**: Empty string status (`status=""`) bypasses filtering due to falsy check
- **Affected Function**: `search_pets()`
- **Current Logic**: `if normalized_status and normalized_status != pet.status:` - the falsy check for empty string causes filter bypass
- **Result**: When `status=""`, all pets regardless of status are returned

### Stop 5 - Tests/PR
- See validation plan in design.md and tasks.md

## Assumptions

- Empty string status should not bypass filtering; it should filter for pets with status="" (which is none) or raise validation error
- The default parameter `status="available"` is correct and should remain
- No API or service layer currently passes empty string to `search_pets()`, but the function should be defensively correct
- Frontend code in `app/web/app.js` is correct and does not need changes
- Adoption flows already validate status separately, so this is purely a catalog visibility issue

## Non-Goals

- Changes to adoption flow validation (already correct in `adoptions.py`)
- Changes to frontend filtering (already correct in `app/web/app.js`)
- Changes to database schema or pet status values
- Changes to API layer (none exists in current codebase)
- Adding new pet statuses beyond available/pending
- Modifying deployment settings or secrets

## What Changes

- Fix the status filtering condition in `catalog.py` line 50 to remove the falsy check
- Add regression test for empty string status parameter edge case
- Ensure status filtering is applied consistently regardless of input value

## Impact

- **App behavior**: Empty string status will no longer bypass filtering; default search remains available-only
- **Tests**: New regression test added to prevent future regressions; all existing tests continue to pass
- **Humans**: PR requires review approval, merge approval, and deployment approval per SDLC Automation Demo rules

## Human Gates

- **Scope approval**: Required - humans approve the fix approach and scope
- **Review approval**: Required - code review must approve changes before merge
- **Merge approval**: Required - humans merge the PR after review
- **Deployment approval**: Required - humans control deployment to production
