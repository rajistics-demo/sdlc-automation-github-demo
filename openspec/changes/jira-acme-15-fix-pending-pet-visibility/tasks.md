# Tasks

## Evidence Checklist

- [x] **Stop 1 - Ticket**: Reviewed Jira issue ACME-15 describing pending pets appearing in customer searches
- [x] **Stop 2 - Wiki/Docs**: Reviewed `docs/repo-memory/petstore-intelligence.md` confirming product rule: "Default pet search returns only available pets"
- [x] **Stop 3 - Logs**: No logs provided in issue; bug reproduced directly via catalog API
- [x] **Stop 4 - Repo/Files**: Identified bug in `app/petstore_app/catalog.py` line 41/50 - empty status bypasses filter
- [ ] **Stop 5 - Tests/PR**: Pending implementation and PR creation

## Implementation Tasks

- [x] Create OpenSpec-style change folder: `openspec/changes/jira-acme-15-fix-pending-pet-visibility/`
- [x] Write proposal.md with source issue, assumptions, and impact
- [x] Write specs/catalog/spec.md with acceptance criteria
- [x] Write design.md with implementation decision and risks
- [x] Validate OpenSpec artifacts with validation script
- [ ] Implement fix in `app/petstore_app/catalog.py`
- [ ] Add regression test for empty status parameter
- [ ] Run focused tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- [ ] Run full test suite: `python3 -m pytest -q`
- [ ] Commit changes with descriptive message
- [ ] Open draft PR with evidence waypoints and validation results
- [ ] Add label `openhands-eks-demo` to PR
- [ ] Add label `openhands-eks-review` to PR for code review handoff
- [ ] Post PR link and summary back to Jira issue ACME-15

## Validation Status

- [ ] All catalog tests pass
- [ ] Full test suite passes
- [ ] Manual verification: `search_pets(status="")` excludes pending pets

## Human Approvals (Pending)

- [ ] Code review approval
- [ ] Merge approval
- [ ] Deployment approval
