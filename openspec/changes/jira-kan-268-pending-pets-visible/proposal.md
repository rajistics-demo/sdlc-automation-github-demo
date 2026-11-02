# Change: Fix Pending Pets Visible in Available Catalog

## Why

Support reports that customers are seeing pets in the available-pets catalog that are not yet ready for adoption. This creates confusion and extra work for operations teams when customers try to start adoption flows for pets with pending status. The catalog search must enforce availability rules to show only available pets by default.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-268
- Trigger: Jira webhook (issue created)
- Automation: SDLC Automation Demo - Jira issue to PR workflow

## Assumptions

- The bug is limited to the catalog search filter logic and does not require database or API changes.
- Pending pets (like Nova, pet-103) should never appear in default or available-only search results.
- Explicit pending-status searches (for support/operations workflows) should continue to work.
- The fix is safe to deploy without environment or configuration changes.

## Non-Goals

- Changes to adoption order validation (already correctly rejects pending pets).
- Changes to pet data structure or status values.
- New pet statuses beyond "available" and "pending".
- Authentication or authorization changes.
- Database schema or persistence layer changes.

## What Changes

- Fix the catalog search filter in `app/petstore_app/catalog.py` to properly handle empty status parameters.
- The current logic uses `if normalized_status and normalized_status != pet.status`, which fails when status is an empty string because empty strings evaluate to False.
- Change to always apply the status filter unless it matches, ensuring empty status parameters don't bypass the availability filter.
- Add regression tests to verify that empty status strings and default searches exclude pending pets.

## Impact

- App behavior: Default catalog searches will consistently return only available pets, even when status is passed as an empty string.
- Tests: Add regression tests for empty status parameter to prevent this bug from reoccurring.
- Humans: Support team will see reduced customer confusion about pet availability. Operations won't need to manually explain why pending pets appeared in search results.

## Human Gates

- Scope approval: Pending (automation proposes this fix based on Jira ticket KAN-268).
- Review approval: Pending (openhands-review label will be added after PR creation).
- Merge approval: Pending (requires human approval after review).
- Deployment approval: Pending (requires human approval before production deployment).
