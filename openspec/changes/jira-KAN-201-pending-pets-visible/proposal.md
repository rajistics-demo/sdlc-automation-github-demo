# Change: Fix pending pets appearing in default search

## Why

Customers are seeing and starting adoption flows for pets that are not yet available (status=pending), creating confusion and operational overhead. The default pet search must return only available pets as specified in the product rules.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-201
- Trigger: Jira issue created webhook
- Automation: SDLC Automation Demo - Jira issue to PR

## Assumptions

- The bug occurs when the search function receives an empty status string rather than using the default parameter value
- The fix should preserve the ability to explicitly search for pending pets when status="pending" is passed
- No schema changes or data migrations are needed
- The static UI correctly filters to available pets only

## Non-Goals

- Changing adoption workflow or status transitions
- Modifying UI filtering logic (already correct)
- Adding new pet statuses or fields
- Authentication or authorization changes

## What Changes

- Update `app/petstore_app/catalog.py` to correctly handle empty status string parameters
- Add regression test to prevent empty status from bypassing the filter

## Impact

- App behavior: Empty status strings will now default to "available" filtering instead of returning all pets
- Tests: New test case added to verify empty status handling
- Humans: Customers will no longer see pending pets in default search results

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required via openhands-review label
- Merge approval: Required via PR review
- Deployment approval: Required before production deployment
