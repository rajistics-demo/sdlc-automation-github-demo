# Tasks

## Evidence Gathering

- [x] Stop 1 - Ticket: Read ACME-6 from Jira webhook payload - "Customers are seeing pets that are not available"
- [x] Stop 2 - Wiki/Docs: Reviewed `docs/wiki/petstore-catalog-availability.md` - confirms Nova (pet-103) should not appear in default available-pets experience
- [x] Stop 3 - Logs: Reviewed `docs/logs/pending-pet-visible.ndjson` - confirms `PENDING_PET_VISIBLE` error for pet-103, indicating a historical regression
- [x] Stop 4 - Repo/Files: Investigated `app/web/app.js` line 17 and `app/petstore_app/catalog.py` - **both already correctly filter by status="available"**
- [x] Stop 5 - Tests/PR: Added regression tests, documented findings, opening draft PR

## Implementation

- [x] Create OpenSpec-style change folder
- [x] Write proposal with assumptions and non-goals
- [x] Write spec delta with acceptance criteria
- [x] Write design with context, decisions, risks, and validation plan
- [x] Validate OpenSpec artifacts
- [x] Verify the implementation - **Backend and UI already correctly filter pending pets**
- [x] Add regression tests to prevent future occurrences
- [x] Document that the issue was either already fixed or never present in current code
- [ ] Run test suite (pytest not available in current sandbox - noted per AGENTS.md guidance)
- [x] Manual verification via code inspection and Node.js test

## Validation

- [x] Backend code review: `catalog.py` line 27-41 correctly defaults to `status="available"`
- [x] UI code review: `app.js` line 17 correctly filters `pet.status === "available"`
- [x] Manual logic test: Verified filter excludes Nova (pet-103) using Node.js
- [x] Added regression tests: `test_search_pets_default_excludes_pending_pets()` and `test_search_pets_species_filter_excludes_pending_pets()`
- [x] Existing test `test_search_pets_filters_by_species_and_status()` confirms Scout (not Nova) returned for dog species
- [~] Test execution: pytest not available in sandbox per AGENTS.md - runtime validation will occur in CI

## Pull Request

- [ ] Open draft PR with ACME-6 prefix
- [ ] Include OpenSpec change path in PR body
- [ ] Document evidence waypoints (wiki, logs, repo)
- [ ] List assumptions and non-goals
- [ ] Show acceptance criteria status
- [ ] List validation results
- [ ] Add `openhands-eks-demo` label
- [ ] Add `openhands-eks-review` label for handoff to code review

## Jira Update

- [ ] Post validation summary and PR link back to ACME-6
- [ ] Include conversation link
- [ ] Status: Completed implementation, awaiting review
