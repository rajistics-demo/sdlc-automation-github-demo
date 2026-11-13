# Tasks: Fix Pending Pet Visibility in Search Results

## Implementation Tasks

- [x] Reproduce the bug: verify `search_pets(status="")` returns pending pets
- [x] Create OpenSpec change artifacts (proposal, design, tasks, spec)
- [x] Add regression test `test_search_pets_with_empty_status_returns_only_available`
- [x] Add test `test_search_pets_with_whitespace_status_returns_only_available`
- [x] Update `catalog.py` status normalization to treat empty string as "available"
- [x] Manual verification confirms fix works correctly
- [ ] Create draft PR with evidence waypoints

## Validation Checklist

- [x] Manual test: `search_pets(status="")` returns only available pets (no Nova)
- [x] Manual test: `search_pets(status="  ")` returns only available pets
- [x] Manual test: `search_pets(status="pending")` still returns pending pets
- [ ] Unit tests (pytest not available in sandbox - see note below)

**Note**: The sandbox does not have pytest installed. Per AGENTS.md: "If pytest is missing, report the setup gap rather than trying packaging workarounds." Manual verification confirms the fix works correctly.

## Human Gates

- [ ] Code review approval via `openhands-eks-review` label
- [ ] QA validation via downstream automation
- [ ] PR merge approval
- [ ] Deployment approval

## Evidence Waypoints

### Stop 1 - Ticket
- Jira: [ACME-9](https://rajiv-shah.atlassian.net/browse/ACME-9)
- Business impact: Customers seeing unavailable pets, operations workload

### Stop 2 - Wiki/Docs
- Repo memory: `docs/repo-memory/petstore-intelligence.md`
- Product rule: "Default pet search returns only available pets"
- Implementation map: `skills/sdlc-story/references/petstore-implementation-map.md`

### Stop 3 - Logs
- No log files or error traces attached to the issue
- Bug discovered through code inspection and reproduction

### Stop 4 - Repo/Files
- Bug location: `app/petstore_app/catalog.py` line 41 (status normalization)
- Test file: `app/tests/test_pet_catalog.py`
- Root cause: Empty string bypassed status filter due to falsy evaluation
- Fix: `normalized_status = status.strip().lower() if status.strip() else "available"`

### Stop 5 - Tests/PR
- Regression tests added: `test_search_pets_with_empty_status_returns_only_available` and `test_search_pets_with_whitespace_status_returns_only_available`
- Manual validation: ✅ Empty status returns only available pets (Mochi, Scout, Pip)
- Manual validation: ✅ Pending status still works correctly (Nova)
- PR: (pending creation)
