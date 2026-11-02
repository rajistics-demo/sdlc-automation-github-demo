# Tasks

## Investigation (Complete)

- [x] Review Jira ticket KAN-268 and understand customer impact.
- [x] Check wiki documentation for pet availability rules.
- [x] Review log evidence in `docs/logs/pending-pet-visible.ndjson`.
- [x] Identify bug location in `app/petstore_app/catalog.py`.
- [x] Reproduce bug with `search_pets(status="")` returning Nova.

## OpenSpec Artifacts (In Progress)

- [x] Create proposal.md with why, assumptions, and impact.
- [x] Create specs/petstore-catalog/spec.md with acceptance criteria.
- [x] Create design.md with implementation approach and risks.
- [x] Create tasks.md (this file).
- [ ] Validate OpenSpec artifacts with validation script.

## Implementation (Pending)

- [ ] Fix catalog.py to normalize empty status strings to "available".
- [ ] Remove problematic `normalized_status and` condition from filter.
- [ ] Add test: `test_search_pets_with_empty_status_excludes_pending()`.
- [ ] Add test: `test_search_pets_default_excludes_pending()`.

## Validation (Pending)

- [ ] Run catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`.
- [ ] Run adoption tests: `python3 -m pytest -q app/tests/test_adoptions.py`.
- [ ] Run full test suite: `python3 -m pytest -q`.
- [ ] Verify Nova (pet-103) is excluded from default and empty-status searches.
- [ ] Verify explicit `status="pending"` still returns Nova.

## Pull Request (Pending)

- [ ] Create feature branch from main.
- [ ] Commit OpenSpec artifacts and implementation.
- [ ] Open draft PR with evidence waypoints.
- [ ] Link Jira issue and automation conversation in PR body.
- [ ] Add `openhands-review` label to trigger code review workflow.

## Human Gates (Pending)

- [ ] Scope approval: Human confirms this fix addresses KAN-268.
- [ ] Review approval: Code reviewer approves changes.
- [ ] Merge approval: Human merges PR to main.
- [ ] Deployment approval: Human deploys fix to production.
