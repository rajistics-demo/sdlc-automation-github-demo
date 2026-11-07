# Change: Fix blank availability filters revealing pending pets

## Why

When the availability filter is empty or contains only whitespace, customer catalog searches can include pending pets. This violates the product rule that default searches should show only available pets.

## Source

- Jira issue: ACME-1
- Trigger label: `openhands-eks-demo`
- Automation: EKS SDLC Demo
- Issue description: "Blank availability filters reveal pending pets"

## Assumptions

- Empty or whitespace-only availability filters should be treated as the ordinary available-only search.
- Explicit staff searches for pending pets (`status="pending"`) must continue to work.
- Pending pets must remain non-adoptable regardless of filter behavior.
- Nova (`pet-103`) has `status="pending"` in the Petstore catalog.

## Non-Goals

- No UI changes required.
- No dependency changes.
- No deployment configuration changes.
- No authentication changes.
- No merges (human review and merge remain required).

## What Changes

Backend fix in `app/petstore_app/catalog.py`:
- Modify `search_pets()` to treat empty or whitespace-only status values as "available".
- Change line 41 from `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() if status.strip() else "available"`.

Backend tests in `app/tests/test_pet_catalog.py`:
- Add `test_search_pets_empty_status_defaults_to_available()` to verify empty string status filters only available pets.
- Add `test_search_pets_whitespace_status_defaults_to_available()` to verify whitespace-only status filters only available pets.

## Evidence Waypoints

- `Stop 1 - Issue`: ACME-1 describes the bug - empty/whitespace availability filters reveal pending pets.
- `Stop 2 - Code`: `catalog.py` line 41 does not handle empty/whitespace status values correctly.
- `Stop 3 - Fix`: Modified normalization logic to default to "available" for empty/whitespace status.
- `Stop 4 - Tests`: Added regression tests to verify the fix prevents pending pets from appearing.
- `Stop 5 - PR`: Draft PR created with focused backend fix and regression tests.

## Impact

- App behavior: Empty or whitespace-only availability filters now return only available pets.
- Tests: Two new regression tests verify the fix.
- Explicit pending searches: Staff can still search for pending pets using `status="pending"`.
- Adoption guards: Pending pets remain non-adoptable (unchanged).

## Human Gates

- Scope approval: Jira issue review (completed).
- Code review: Draft PR must pass `openhands-eks-review` stage.
- QA review: PR must pass independent QA stage.
- Merge approval: Human reviewers must approve and merge.
- Deployment approval: Outside this automation scope.
