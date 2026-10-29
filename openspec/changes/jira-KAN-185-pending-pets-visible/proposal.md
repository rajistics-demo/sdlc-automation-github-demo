# Change: Fix Pending Pets Appearing in Available Search Results

## Why

Support reports that customers can see and start adoption flows for pets that should not be available yet. This violates the Petstore product rule that default pet search must return only available pets. The bug creates customer confusion and generates unnecessary operational work.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-185
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira to PR workflow

## Assumptions

- The default `status="available"` parameter intent is correct
- Empty string status (`status=""`) should not bypass the status filter
- Whitespace-only status values should be normalized
- No REST API currently exposes `search_pets()` so production impact is currently low
- The bug is latent and could be triggered by future API endpoints or integrations

## Non-Goals

- Creating a REST API endpoint for pet search
- Adding additional pet status values beyond `available` and `pending`
- Changing the adoption validation logic (already correctly rejects pending pets)
- Modifying frontend JavaScript filtering (already correct)
- Adding authentication or authorization

## What Changes

- Fix the status filter in `app/petstore_app/catalog.py` line 50 to prevent empty string bypass
- Add test coverage for empty string and whitespace-only status values
- Ensure the status filter always applies when the function is called

## Impact

- App behavior: `search_pets()` will correctly filter by status even when `status=""` is passed
- Tests: New test cases for edge cases (empty string, whitespace) added to `test_pet_catalog.py`
- Humans: This is a defensive fix; no current callers pass empty status, but future API endpoints or integrations could trigger the bug

## Human Gates

- Scope approval: Requires human confirmation that defensive fix approach is appropriate
- Review approval: Code reviewer must verify the fix doesn't break explicit pending pet searches
- Merge approval: Human must approve merging to main branch
- Deployment approval: Human must approve any deployment to production
