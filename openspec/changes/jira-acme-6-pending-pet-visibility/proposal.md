# Change: Fix Pending Pet Visibility in Available Catalog

## Why

Customers are seeing pets with "pending" status in the default available-pets experience. This violates the product rule that only pets with "available" status should appear in customer-facing catalog searches. The confusion is creating extra work for support and operations teams.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-6
- Trigger: Jira issue created webhook
- Automation: SDLC Automation Demo - Jira Issue to PR

## Assumptions

- Nova (pet-103) is the only pending pet currently in the dataset
- The backend Python code (`search_pets`) correctly enforces status filtering
- The issue is isolated to the UI layer (JavaScript frontend)
- No persistence or deployment changes are needed
- This is a regression fix, not a new feature

## Non-Goals

- Authentication or authorization changes
- Deployment configuration changes
- Persistence or database schema changes
- UI redesign beyond the minimal fix
- Changes to the backend Python code (already correct)
- Support for additional pet statuses

## What Changes

- Fix the UI JavaScript to properly filter pets by status, matching the backend behavior
- Ensure the UI respects the `status="available"` filter that exists in the backend
- Add regression tests to prevent pending pets from appearing in default searches

## Impact

- App behavior: Default catalog search in the UI will only show available pets, matching the backend contract
- Tests: Add UI-level regression tests to verify pending pets are excluded from default searches
- Humans: Support and operations teams will no longer receive reports of customers seeing unavailable pets

## Human Gates

- Scope approval: Pending - awaiting confirmation this fix addresses the root cause
- Review approval: Pending - awaiting code review after implementation
- Merge approval: Pending - awaiting human approval to merge to main
- Deployment approval: Pending - awaiting human approval to deploy to production
