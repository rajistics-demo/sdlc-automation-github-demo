# Tasks: Fix Pending Pets Visible in Catalog

## Implementation Checklist

- [x] Investigate catalog.py search_pets() function
- [x] Confirm bug: empty status bypasses filter on line 50
- [x] Review docs/wiki/petstore-catalog-availability.md
- [x] Review docs/logs/pending-pet-visible.ndjson
- [ ] Fix status filter logic in catalog.py
- [ ] Add test: test_default_search_excludes_pending_pets
- [ ] Add test: test_empty_status_defaults_to_available
- [ ] Run pytest app/tests/test_pet_catalog.py -v
- [ ] Validate no regressions in existing tests
- [ ] Open draft PR with evidence waypoints
- [ ] Add openhands-review label to PR

## Human Gates

- Human review required before merge
- Human approval required for deployment
- QA team to verify in staging environment

## Validation Plan

1. **Unit Tests:** Run pytest on test_pet_catalog.py - all tests must pass
2. **Regression:** Verify existing pending-pet search still works with explicit status="pending"
3. **Default Behavior:** Confirm search without args returns only available pets
4. **Edge Case:** Confirm empty string status="" is handled correctly

## Evidence Checklist

- [x] **Stop 1 - Ticket:** Jira KAN-194 - sparse business description of customer impact
- [x] **Stop 2 - Wiki/Docs:** docs/wiki/petstore-catalog-availability.md - confirms product rule
- [x] **Stop 3 - Logs:** docs/logs/pending-pet-visible.ndjson - PENDING_PET_VISIBLE error for pet-103
- [x] **Stop 4 - Repo/Files:** app/petstore_app/catalog.py line 50 - status filter truthy bug
- [ ] **Stop 5 - Tests/PR:** Regression tests added, pytest passing, draft PR created
