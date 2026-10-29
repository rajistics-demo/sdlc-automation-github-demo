# Tasks

- [x] Investigate catalog behavior and identify root cause
- [x] Review docs/wiki/petstore-catalog-availability.md for product requirements  
- [x] Review docs/logs/pending-pet-visible.ndjson for error evidence
- [x] Create OpenSpec-style change artifacts (proposal, spec, design, tasks)
- [x] Validate change artifacts with validation script
- [ ] Add regression test to verify pending pets excluded from default search
- [ ] Implement the fix in app/petstore_app/catalog.py (line 50)
- [ ] Run all catalog tests to verify no regressions
- [ ] Create draft PR with evidence waypoints
- [ ] Add openhands-review label for code review handoff
- [ ] Post status comment to Jira issue KAN-249

## Evidence Waypoints

### Stop 1 - Ticket
- Jira issue KAN-249: "Customers are seeing pets that are not available"
- Business language: "confusing customers and creating extra work for operations"

### Stop 2 - Wiki/Docs
- Checked: `docs/wiki/petstore-catalog-availability.md`
- Found: "Default customer-facing catalog search must show only pets with status='available'"
- Found: "Nova is pet-103 with status='pending'"
- Found: "PENDING_PET_VISIBLE log means catalog regression"

### Stop 3 - Logs
- Checked: `docs/logs/pending-pet-visible.ndjson`
- Found: ERROR log with error_code "PENDING_PET_VISIBLE"
- Evidence: pending_pet_ids ["pet-103"] visible in available-pets experience
- Bug signal: type="catalog_availability_regression", safe_to_fix=true

### Stop 4 - Repo/Files
- File: `app/petstore_app/catalog.py`
- Bug location: Line 50, conditional status filter logic
- Root cause: `if normalized_status and normalized_status != pet.status:` allows bypass when status is empty string
- Fix: Remove `normalized_status and` to always apply status filter
- Existing tests: `app/tests/test_pet_catalog.py` has test for explicit pending search

### Stop 5 - Tests/PR
- Plan: Add `test_default_search_excludes_pending_pets()` regression test
- Plan: Run `pytest app/tests/test_pet_catalog.py` for validation
- Plan: Open draft PR with evidence and OpenSpec artifacts
