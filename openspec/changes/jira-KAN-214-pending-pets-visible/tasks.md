# Tasks

- [x] Review source issue KAN-214 and repository documentation
- [x] Investigate catalog.py and identify the bug (line 50: empty status bypasses filter)
- [x] Check wiki docs (docs/wiki/petstore-catalog-availability.md) and logs (docs/logs/pending-pet-visible.ndjson)
- [x] Create OpenSpec-style change artifacts (proposal, spec delta, design, tasks)
- [ ] Validate OpenSpec artifacts with validation script
- [ ] Fix catalog.py to enforce status filter even with empty status
- [ ] Add regression test for pending pet exclusion
- [ ] Run all catalog tests to ensure existing behavior preserved
- [ ] Create feature branch and commit changes
- [ ] Open draft PR with evidence waypoints and review handoff
- [ ] Add `openhands-review` label for code review workflow

## Evidence Waypoints

- **Stop 1 - Ticket**: Jira KAN-214 "Customers are seeing pets that are not available" - sparse business-language bug report
- **Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` - confirms default search must show only available pets; Nova is pet-103 with status=pending
- **Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` - PENDING_PET_VISIBLE error code, pet-103 visible in available-pets experience
- **Stop 4 - Repo/Files**: `app/petstore_app/catalog.py` line 50 - bug found: `if normalized_status and` allows empty status to bypass filter
- **Stop 5 - Tests/PR**: To be completed after implementation
