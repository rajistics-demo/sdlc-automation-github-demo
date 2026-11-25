# Tasks: ACME-16 Pending Pets Visibility Fix

**Source:** [ACME-16](https://rajiv-shah.atlassian.net/browse/ACME-16)  
**Branch:** `codex/eks-demo-acme-16`

## Implementation Tasks

- [x] Reproduce the bug: Verify that `search_pets(status="")` returns pending pets
- [x] Create OpenSpec change artifacts (proposal, design, tasks, spec)
- [x] Fix `app/petstore_app/catalog.py` line 50: Change truthy check to explicit None check
- [x] Add regression test for empty status string
- [ ] Run existing tests to verify no regression (pytest not available in sandbox)
- [ ] Create draft pull request with evidence

## Validation Tasks

- [ ] Run `python3 -m pytest -q app/tests/test_pet_catalog.py` (pytest not available in this sandbox)
- [x] Manual logic verification: Fix is correct - empty string will be treated as filter value
- [x] Review test coverage for the catalog module

## Human Review Gates

- [ ] **PR Review:** Code review by team member
- [ ] **QA Approval:** Functional testing confirmation
- [ ] **Merge Approval:** Final sign-off before merge to main
- [ ] **Deployment Approval:** Production release decision

## Handoff

- [ ] Add `openhands-eks-demo` label
- [ ] Add `openhands-eks-review` label for code review handoff
- [ ] Post PR link and summary to ACME-16

## Notes

- The adoptions module (`adoptions.py`) already correctly validates that only available pets can be adopted (line 34-35)
- The UI JavaScript (`app/web/app.js`) hardcodes status to "available" (line 17), so this bug likely only affects direct API usage
- Pytest is not available in this sandbox environment; tests cannot be executed but logic has been verified manually
- Implementation is complete and ready for PR creation
