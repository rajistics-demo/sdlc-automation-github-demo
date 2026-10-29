# Change: Fix Pending Pets Visible in Available Catalog

## Why

Customers are seeing pets that are not available yet in the default catalog search. This is confusing customers who expect to see only pets ready for adoption, and creating extra work for operations who must handle inquiries about pets that cannot yet be adopted.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-255
- Trigger: Jira webhook event `jira:issue_created`
- Automation: sdlc-story (Jira issue to draft PR)

## Evidence Waypoints

### Stop 1 - Ticket

Sparse Jira issue KAN-255 reported: "Support reports that some customers are able to see and start adoption flows for pets that should not be available yet."

### Stop 2 - Wiki/Docs

Checked `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Pending pets must not appear in the default available-pets experience
- Nova is `pet-103` with `status="pending"`

### Stop 3 - Logs

Checked `docs/logs/pending-pet-visible.ndjson`:
- ERROR code `PENDING_PET_VISIBLE` logged for `pet-103` (Nova)
- Customer impact: "Pending pets were visible in the available-pets experience"
- Marked as safe_to_fix catalog_availability_regression

### Stop 4 - Repo/Files

**Root cause identified in `app/petstore_app/catalog.py` line 50:**

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, `normalized_status` becomes an empty string (falsy), causing the status filter to be skipped entirely. This exposes all pets including pending ones.

**Reproduction:**
- `search_pets()` with default `status="available"` → correctly returns only available pets
- `search_pets(status="")` with empty status → incorrectly returns ALL pets including pending

**Files:**
- `app/petstore_app/catalog.py` - contains the buggy filter logic
- `app/tests/test_pet_catalog.py` - has tests for explicit status filtering but missing test for empty/invalid status

### Stop 5 - Tests/PR

Will add regression test and fix, then open draft PR.

## Assumptions

- The default `status="available"` parameter should be enforced even when an empty string is passed
- Existing explicit `status="pending"` searches must continue to work for operations workflows
- No database or persistence layer changes needed (in-memory PETS tuple)
- No auth, secrets, or deployment configuration changes needed

## Non-Goals

- Changing the UI (it already filters correctly with hardcoded `status === "available"`)
- Adding new pet statuses beyond "available" and "pending"
- Changing the PETS data structure or adding persistence
- Adding API authentication or rate limiting

## What Changes

- Update `search_pets()` in `catalog.py` to enforce status filtering even when an empty or whitespace-only status is provided
- Add regression test to verify that empty status strings do not bypass the availability filter
- Add test to verify that the default status filter excludes pending pets

## Impact

- **App behavior:** Default catalog search and searches with empty status will now correctly return only available pets
- **Tests:** Added regression tests ensure pending pets never leak into available-only results
- **Humans:** Operations can still explicitly search for pending pets when needed; customers will no longer see pets that are not ready for adoption

## Human Gates

- **Scope approval:** Humans approve that this fix aligns with business requirements
- **Review approval:** Humans review the code change and test coverage
- **Merge approval:** Humans approve the merge after code review and QA validation
- **Deployment approval:** Humans control when this fix reaches production
