# Change: Fix Pending Pets Visibility in Search

## Why

Support reports that customers are seeing and starting adoption flows for pending pets that should not be visible. The log evidence shows `PENDING_PET_VISIBLE` error for pet-103 (Nova), confirming pending pets are leaking into the customer-facing catalog when they should only appear in explicit operations searches.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-204
- Trigger: Jira webhook `jira:issue_created`
- Automation: sdlc-story (Jira issue to draft PR)

## Assumptions

- The bug is in the backend `search_pets()` function where empty status strings bypass filtering
- The default behavior (`status="available"`) is correct
- Explicit `status="pending"` requests should continue to work for operations
- The web UI correctly passes the default status and doesn't need changes
- The adoption flow already validates pet availability (no changes needed)

## Non-Goals

- Changing the adoption order validation
- Modifying the web UI  
- Adding new pet statuses beyond available/pending
- Changing database schema or persistence logic

## What Changes

- Fix the `search_pets()` function in `app/petstore_app/catalog.py` to enforce the availability filter even when an empty status string is provided
- Add explicit test coverage for pending pet exclusion from default searches
- Prevent pending pets from appearing in search results unless explicitly requested with `status="pending"`

## Impact

- App behavior: Default searches will correctly exclude all pending pets
- Tests: Add explicit regression test for Nova (pet-103) exclusion
- Humans: Operations can still explicitly request pending pets when needed

## Human Gates

- Scope approval: Automated (bounded bug fix within known behavior)
- Review approval: Required before merge
- Merge approval: Required (humans control main branch)
- Deployment approval: Required (humans control production)
