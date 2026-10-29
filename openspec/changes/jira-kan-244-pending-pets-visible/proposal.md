# Change: Fix Pending Pets Visibility in Catalog Search

## Why

Support reports that customers are able to see and start adoption flows for pets with `status="pending"` that should not be visible in the default available-pets experience. This violates the catalog availability rules and creates confusion for customers and extra work for operations.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-244
- Trigger: Jira webhook on issue creation (KAN-244)
- Automation: jira-issue-to-pr

## Assumptions

- The bug occurs when external code (web layer, API layer, or test code) passes an empty string for the status parameter
- The default behavior should always filter to available pets only, regardless of how the status parameter is provided
- Empty status should be treated the same as the default "available" status
- Support workflows that explicitly request `status="pending"` are unaffected

## Non-Goals

- This fix does not add new pet statuses or filtering capabilities
- This fix does not modify the UI layer
- This fix does not change the database schema or add persistence
- This fix does not add new API endpoints or authentication

## What Changes

- Fix `search_pets` function in `app/petstore_app/catalog.py` to enforce the default `status="available"` filter even when an empty string is passed
- Root Cause: When `status=""` is passed, the normalized empty string is falsy, causing the status filter check (`if normalized_status and ...`) to be skipped entirely
- Add regression test for empty status string behavior

## Impact

- App behavior: Eliminates confusion caused by seeing pets that cannot be adopted. Customers will only see truly available pets in the default catalog experience.
- Tests: Add focused regression test to verify empty status strings default to available-only filtering
- Humans: Reduces support burden from customers asking about pets that aren't actually available

## Human Gates

- Scope approval: Assumed approved via Jira issue creation
- Review approval: Required via openhands-review workflow
- Merge approval: Required by humans after review
- Deployment approval: Required by humans before production deployment
