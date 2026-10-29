# Change: Fix Pending Pets Visible in Available Catalog

## Why

Customers are seeing and starting adoption flows for pets that are not yet available. This violates the product rule that default pet searches should only show available pets. Support reports indicate that pending pets (specifically Nova, pet-103) are appearing in the customer-facing catalog, creating confusion and extra operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-259
- Trigger: Jira issue created
- Automation: SDLC Automation Demo - Story to PR

## Evidence Waypoints

### Stop 1 - Ticket
Jira KAN-259: "Customers are seeing pets that are not available"
- Sparse business-language bug report
- No file paths, error codes, or implementation hints provided

### Stop 2 - Wiki/Docs
Checked: `docs/wiki/petstore-catalog-availability.md`
- Confirms: Default catalog must show only `status="available"`
- Known mapping: Nova is `pet-103` with `status="pending"`
- PENDING_PET_VISIBLE log means catalog regression

### Stop 3 - Logs
Checked: `docs/logs/pending-pet-visible.ndjson`
- Error code: `PENDING_PET_VISIBLE`
- Pending pet IDs: `["pet-103"]` (Nova)
- Customer impact: "Pending pets were visible in the available-pets experience"
- Bug signal: `safe_to_fix: true`

### Stop 4 - Repo/Files
Primary files:
- `app/petstore_app/catalog.py` - Pet search filtering logic
- `app/tests/test_pet_catalog.py` - Existing test coverage

Root cause identified:
- Line 50: `if normalized_status and normalized_status != pet.status:`
- When `status=''` (empty string), the condition evaluates as falsy
- The status filter is bypassed entirely, returning all pets including pending

Reproduction:
```python
search_pets(status='')  # Returns all 4 pets, including pet-103 (Nova, pending)
```

## Assumptions

- The bug is limited to empty status strings bypassing the filter
- Existing behavior for explicit status values ('available', 'pending') is correct
- No UI or API changes are needed to prevent empty status strings from being passed
- Default status='available' parameter should remain the same
- No schema, deployment, auth, or secret changes required

## Non-Goals

- Changing the default status parameter value
- Adding new pet statuses beyond available/pending
- Modifying adoption validation logic
- UI redesign or new UI features
- Persistence or database changes
- Authentication or authorization changes
- Deployment or infrastructure changes

## What Changes

- Update the status filter logic in `search_pets()` to treat empty status strings as invalid or default to 'available'
- Add regression tests that verify empty status strings do not return pending pets
- Ensure existing tests continue to pass

## Impact

- App behavior: Empty status strings will no longer bypass the availability filter
- Tests: New regression tests added to prevent future occurrences
- Humans: Support and operations see fewer erroneous adoption attempts; clearer customer experience

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge (openhands-review automation)
- Merge approval: Required (human decision)
- Deployment approval: Required (human decision)
