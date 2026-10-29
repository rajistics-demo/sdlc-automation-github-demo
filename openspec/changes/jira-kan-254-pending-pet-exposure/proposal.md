# Change: Remove Pending Pet Data from Customer-Facing UI

## Why

Support reports that customers can see pending pets (pets not yet available for adoption) in the petstore UI. The customer-facing catalog should show only available pets by default. Pending pets are for internal support and operations workflows only.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-254
- Trigger: jira:issue_created with label codex-skill-589ebf68
- Automation: Replicated Jira Delegated Factory Demo

## Evidence Waypoints

### Stop 1 - Ticket

The Jira issue (KAN-254) states:
> "Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. Please investigate and fix."

The business language clues: "see", "not available yet", "confusing customers".

### Stop 2 - Wiki/Docs

Checked `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog must show only `status="available"` pets
- Nova is `pet-103` with `status="pending"`
- A `PENDING_PET_VISIBLE` log indicates a catalog regression

### Stop 3 - Logs

Checked `docs/logs/pending-pet-visible.ndjson`:
```json
{"error_code":"PENDING_PET_VISIBLE","pending_pet_ids":["pet-103"],"customer_impact":"Pending pets were visible in the available-pets experience."}
```

This confirms pet-103 (Nova) was exposed to customers.

### Stop 4 - Repo/Files

**Delegation Status**: Native task delegation is unavailable for this limited skill test run. This limitation is reported as authorized by the operator. The investigation proceeded with direct exploration.

**Backend**: `app/petstore_app/catalog.py` correctly defaults to `status="available"` (line 31), and `app/petstore_app/adoptions.py` correctly rejects non-available pets (line 34).

**Frontend**: `app/web/app.js` includes Nova (pet-103, status "pending") in the hardcoded pets array (line 5). While the filter at line 17 checks `pet.status === "available"`, the pending pet data is present in the client-side JavaScript, exposing it to customers who inspect the page source or modify client-side filters.

**Root cause**: Pending pets should not be in the customer-facing UI data at all.

## Assumptions

- Pending pet data is intended only for support/operations tools, not the customer-facing catalog UI
- The static UI currently has no legitimate need to load pending pets
- Removing pending pets from the client-side array will not break existing functionality since they were already filtered out at runtime

## Non-Goals

- Backend changes to catalog.py or adoptions.py (already correct)
- Adding a separate support/operations UI
- Dynamic data loading or API integration
- Authentication or authorization changes

## What Changes

- Remove pending pets from the hardcoded pets array in `app/web/app.js`
- Keep only available pets in the client-side data

## Impact

- App behavior: Pending pets will no longer be present in client-side code
- Tests: Playwright test at line 171-176 verifies pending pets remain hidden (should still pass)
- Humans: Support/operations workflows that need pending pet visibility will need a separate tool

## Human Gates

- Scope approval: Required before PR merge
- Review approval: Required before PR merge  
- Merge approval: Required before merging to main
- Deployment approval: Required before production deployment
