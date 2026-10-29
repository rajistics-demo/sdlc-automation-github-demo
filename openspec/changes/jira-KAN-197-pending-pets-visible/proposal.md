# Change: Fix Pending Pets Visible in Default Search

## Why

Customers are seeing pets that are not available for adoption yet, causing confusion and creating extra operational work. The Petstore catalog is showing pending pets in default search results when it should only return available pets.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-197
- Trigger: Jira webhook `jira:issue_created`
- Automation: sdlc-story (Jira request to draft PR)

## Assumptions

- The product rule "default pet search returns only available pets" is the correct behavior
- Pending pets should only be visible when explicitly requested via `status="pending"`
- The bug is isolated to the backend catalog filtering logic (frontend JS already filters correctly)
- No API contract changes are needed; this is a backend correctness fix

## Non-Goals

- Changing the web UI (it already filters correctly)
- Adding new status types beyond `available` and `pending`
- Modifying the adoption flow logic (it already correctly blocks pending pets)
- Changing the API signature or adding new parameters

## What Changes

- Fix the status filter guard in `app/petstore_app/catalog.py` line 50 to ensure empty-string status values don't bypass the availability filter
- Add regression test coverage for the empty-string status edge case

## Impact

- **App behavior**: Default catalog searches will correctly exclude pending pets, even when called with `status=""`
- **Tests**: One new test case added to prevent regression of this specific bug
- **Humans**: Operations team will no longer receive complaints about pending pets being visible; customers will have a clearer adoption experience

## Human Gates

- **Scope approval**: Humans must confirm this fix aligns with product requirements
- **Review approval**: Code review required via `openhands-review` label workflow
- **Merge approval**: Humans must approve and merge the PR
- **Deployment approval**: Humans control deployment timing and rollout
