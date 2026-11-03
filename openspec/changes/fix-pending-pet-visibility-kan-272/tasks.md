# Tasks

- [x] Gather evidence from logs, wiki, and code
- [x] Create OpenSpec-style change artifacts (proposal, design, spec delta)
- [ ] Validate OpenSpec artifacts structure
- [ ] Implement the status filter fix in catalog.py
- [ ] Add regression test for empty status string
- [ ] Add regression test for default search excluding pending pets
- [ ] Run test suite and verify all tests pass
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with evidence waypoints
- [ ] Add `openhands-review` label to PR
- [ ] Update Jira issue with PR link and status

## Evidence Waypoints

### Stop 1 - Ticket
- Jira issue KAN-272: "Customers are seeing pets that are not available"
- Support reports pending pets visible in adoption flows
- Business impact: customer confusion and ops overhead

### Stop 2 - Wiki/Docs
- `docs/wiki/petstore-catalog-availability.md` confirms:
  - Default search must show only `status="available"` pets
  - Pending pets only for explicit `status="pending"` requests
  - Nova (pet-103) is the demo pending pet
  - `PENDING_PET_VISIBLE` log indicates catalog regression

### Stop 3 - Logs
- `docs/logs/pending-pet-visible.ndjson`:
  - Error code: `PENDING_PET_VISIBLE`
  - Pending pet IDs: ["pet-103"] (Nova)
  - Customer impact: "Pending pets were visible in the available-pets experience"
  - Bug signal: catalog_availability_regression, safe_to_fix=true

### Stop 4 - Repo/Files
- `app/petstore_app/catalog.py` line 50: Bug in status filter
  - Current: `if normalized_status and normalized_status != pet.status:`
  - Problem: Empty string after `.strip().lower()` is falsy, bypasses filter
  - Reproduction: `search_pets(status="")` returns all 4 pets including Nova
  - Fix: Change to `if normalized_status != pet.status:`
- `app/tests/test_pet_catalog.py`: Existing tests for species, status, tag filters

### Stop 5 - Tests/PR
- Pending: Implementation and test addition
- Pending: Draft PR with fix and evidence
