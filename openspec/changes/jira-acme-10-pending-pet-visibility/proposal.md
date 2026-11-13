# Change: Fix Pending Pet Visibility in Available Catalog

## Why

Customers are seeing pets that are not yet available for adoption in the default catalog search. This creates confusion and extra support work when customers try to start adoption flows for pets that should not be shown. The catalog search must only return available pets by default, while still allowing operations staff to explicitly search for pending pets when needed.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-10
- Trigger: Jira issue created webhook (ACME-10)
- Automation: EKS demo Jira-to-PR workflow

## Assumptions

- The default catalog search should always filter to `status="available"` even when an empty status string is passed.
- Explicit `status="pending"` searches must continue to work for operations use cases.
- Nova (pet-103) is the known test case for pending pet visibility.
- No changes to the data model or persistence layer are needed.
- No UI changes are required; the frontend already correctly filters to available pets.

## Non-Goals

- Changes to the pet data model or status values.
- Changes to adoption workflow logic.
- UI redesign or enhancement.
- Deployment or infrastructure changes.
- New dependencies or external service integration.

## What Changes

- Fix the `search_pets` function in `app/petstore_app/catalog.py` to properly filter by status even when an empty string is provided.
- Add regression tests to verify that default searches and empty-status searches do not return pending pets.
- Add tests to verify that explicit `status="pending"` searches still work correctly.

## Impact

- **App behavior**: Default catalog search will correctly exclude pending pets. Customers will no longer see unavailable pets in their search results.
- **Tests**: New regression tests will prevent this issue from reoccurring.
- **Humans**: Support team will see reduced customer confusion. Operations staff can still search for pending pets when explicitly needed.

## Human Gates

- **Scope approval**: Pending (human review of this proposal)
- **Review approval**: Pending (human code review via openhands-eks-review)
- **Merge approval**: Pending (human approval required)
- **Deployment approval**: Pending (human deployment decision)
