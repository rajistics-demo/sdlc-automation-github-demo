# Change: Fix Pending Pet Visibility in Search Results

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The `search_pets` function has a status filter bug that allows pending pets to appear when an empty status string is passed, violating the product rule: "Default pet search returns only available pets."

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-9
- Trigger: Jira webhook - issue created
- Automation: sdlc-story (Jira issue to PR)

## Assumptions

- The bug occurs when external code passes `status=""` to `search_pets()`
- Empty status should default to "available" rather than "show all"
- No legitimate use case exists for showing all pets regardless of status through an empty string
- The JavaScript UI already filters correctly; this fix targets the Python backend

## Non-Goals

- This change does NOT add new filtering capabilities
- This change does NOT modify the ability to explicitly search for pending pets using `status="pending"`
- This change does NOT alter the UI behavior

## What Changes

- Update `app/petstore_app/catalog.py` status normalization to treat empty strings as "available"
- Add regression test to verify empty status strings don't bypass the filter
- Verify all existing tests continue to pass

## Impact

- App behavior: Customers will no longer see pending pets when empty status is passed
- Tests: New regression test added; all existing tests preserved
- Humans: Reduced support workload; operations team gets clearer pet visibility

## Human Gates

- Scope approval: Pending
- Review approval: Pending (via openhands-eks-review label)
- Merge approval: Pending
- Deployment approval: Pending
