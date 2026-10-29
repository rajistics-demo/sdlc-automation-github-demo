# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that customers can see and start adoption flows for pets that should not be available yet. This creates confusion for customers and extra work for operations staff who must explain that these pets cannot actually be adopted.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-251
- Trigger: Jira issue created webhook
- Automation: jira-issue-to-pr

## Assumptions

- The Petstore catalog already has an availability status system in place
- Nova (pet-103) is the pending pet causing customer confusion
- The backend API and frontend UI both need to enforce the available-only filter
- The product requirement is to show only available pets by default

## Non-Goals

- Changing the data model or persistence layer
- Adding new pet statuses beyond "available" and "pending"
- Modifying authentication or authorization
- Redesigning the UI appearance or layout
- Adding ability for customers to explicitly view pending pets

## What Changes

- Backend: Ensure search_pets() defaults to status="available" and filters correctly
- Frontend: Ensure the UI filters pets by status="available" before displaying
- Tests: Add explicit regression tests that verify pending pets are excluded from default searches

## Impact

- App behavior: Customers will no longer see pending pets (like Nova) in the default catalog view
- Tests: New tests will prevent this regression from happening again
- Humans: Operations team will have fewer customer support issues about unavailable pets

## Human Gates

- Scope approval: Requester confirms this matches the reported issue
- Review approval: Code reviewer confirms the fix is safe and complete
- Merge approval: Maintainer approves merging to main branch
- Deployment approval: Operations approves deploying the fix to production
