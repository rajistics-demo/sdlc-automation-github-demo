# Change: Fix Empty Status Filter Bug in Pet Catalog

## Why

Customers are seeing pets that are not available (specifically, pending pets) when they should only see available pets. This creates confusion for customers and extra work for operations. The catalog search function has a bug where passing an empty string for the status parameter bypasses the status filter entirely, allowing pending pets to appear in search results.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-263
- Trigger: Jira issue created webhook
- Automation: SDLC Automation Demo (Jira to PR workflow)

## Assumptions

- The bug is in the backend `catalog.py` where empty string status bypasses filtering
- The static UI is correctly filtering to available pets only
- This is a safe bug fix with no deployment, auth, or schema changes required
- Existing test coverage and validation commands are sufficient
- No new dependencies or infrastructure changes are needed

## Non-Goals

- Deployment or infrastructure changes
- Auth, secrets, or IAM changes
- Database or persistence changes
- UI redesign or new UI features
- Adding new pet statuses beyond available/pending
- Changes to adoption flow logic

## What Changes

- Update `catalog.py` to treat empty status string as "available" (the default)
- Add regression tests that verify empty status returns only available pets
- Ensure explicit status="pending" searches still work for support workflows

## Impact

- App behavior: Empty status searches will correctly return only available pets instead of all pets
- Tests: New regression tests added to prevent future regressions
- Humans: Customers will no longer see pending pets in available-pets searches; support can still explicitly search for pending pets when needed

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge (automated via openhands-review label)
- Merge approval: Required (human decision)
- Deployment approval: Required (human decision)
