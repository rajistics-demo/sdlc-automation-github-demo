# Change: Verify Pending Pet Visibility Fix

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The default pet search must return only available pets, and pending pets should only be visible when explicitly requested by support or operations staff.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-187
- Jira key: KAN-187
- Issue type: Task
- Priority: Medium
- Reporter: Rajiv Shah
- Created: 2026-09-23T07:05:35-05:00
- Trigger: Jira webhook issue_created event
- Automation: SDLC Automation Demo - Jira to PR workflow

## Assumptions

- The reported issue refers to the default catalog search behavior showing pending pets
- "Pets that should not be available yet" means pets with `status="pending"`
- The catalog implementation in `app/petstore_app/catalog.py` is the relevant code path
- The adoption flow validation in `app/petstore_app/adoptions.py` should also prevent pending pet adoptions
- UI changes are in scope if the frontend is showing pending pets
- Historical log evidence from `docs/logs/pending-pet-visible.ndjson` indicates this was a known issue
- Current code investigation will determine if this is a regression or configuration issue

## Non-Goals

- Adding new pet status types beyond "available" and "pending"
- Implementing a pending pet management UI for operations staff
- Adding authentication or authorization for status-specific searches
- Changing the data model or adding persistence
- Modifying deployment configuration or environment variables

## What Changes

Investigation revealed that **the current code is already correct**:

- Backend default search parameter correctly set to `status="available"`
- Backend filter logic properly excludes non-matching status
- Frontend hardcoded filter limits results to available pets only
- Adoption validation prevents creating orders for non-available pets
- All existing tests pass and validate correct behavior

**Change**: Add comprehensive validation and defensive tests to ensure the fix remains stable and provide confidence that the issue is resolved.

## Impact

- App behavior: No functional changes needed; current behavior is correct
- Tests: Add additional validation tests to prevent future regressions
- Humans: Investigation results and validation evidence provided for review; confirms current implementation matches product requirements

## Human Gates

- Scope approval: ✅ Humans approved investigation and verification approach
- Review approval: ⏳ Humans must review investigation findings and validation results
- Merge approval: ⏳ Humans must approve PR merge
- Deployment approval: ⏳ Humans control deployment timing and rollout
