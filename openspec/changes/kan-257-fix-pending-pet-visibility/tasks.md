# Tasks: Fix Pending Pet Visibility

## Implementation

- [x] Reproduce bug: confirm `search_pets(status="")` returns pending pets
- [x] Update `catalog.py` status filter to treat empty status as "available"
- [x] Add regression test for empty status string
- [x] Add test confirming default behavior excludes pending pets
- [x] Run catalog-specific tests
- [x] Run full test suite (catalog tests passed; infrastructure test failures are unrelated)

## Validation

- [x] All catalog tests pass (8/8)
- [x] Manual verification: `search_pets(status="")` excludes Nova
- [x] Manual verification: `search_pets(status="pending")` still returns Nova

## Delivery

- [ ] Open draft PR with fix and tests
- [ ] Add `openhands-review` label to PR
- [ ] Post Jira comment with PR link and validation results

## Human Gates

None - this is a straightforward bug fix with clear acceptance criteria and low risk.
