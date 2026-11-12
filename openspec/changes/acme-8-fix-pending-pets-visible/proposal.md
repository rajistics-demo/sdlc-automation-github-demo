# Change: Fix Pending Pets Visible in Search Results

## Why

Support reports that some customers can see and start adoption flows for pets with "pending" status. This violates the product rule that default pet search should return only available pets. Pending pets should only appear when explicitly requested and cannot be adopted.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-8
- Trigger: Jira webhook `jira:issue_created`
- Automation: EKS Demo Issue-to-PR

## Assumptions

- The bug is in the backend `search_pets()` function's conditional logic (line 50 in catalog.py)
- Callers that explicitly pass `status=""` expect the default "available" filtering behavior
- The web UI is already filtering correctly but the backend API is vulnerable

## Non-Goals

- Changing the default status filter behavior
- Modifying the adoption flow validation (already correctly rejects pending pets)
- Adding new pet statuses beyond "available" and "pending"

## What Changes

- Fix the `search_pets()` function in `app/petstore_app/catalog.py` to properly enforce the status filter when an empty string is passed for the `status` parameter
- Currently, passing `status=""` bypasses the filter and returns all pets including pending ones
- Remove the truthy check on line 50 to ensure the status filter is always applied

## Impact

- App behavior: Customers will no longer see pending pets in default search results
- Tests: Add regression test for empty status parameter handling
- Humans: Reduced confusion and support burden from customers attempting to adopt unavailable pets

## Human Gates

- Scope approval: Pending - human review of fix scope
- Review approval: Pending - code review via `openhands-review` label
- Merge approval: Pending - human approval to merge PR
- Deployment approval: Pending - human approval for production deployment
