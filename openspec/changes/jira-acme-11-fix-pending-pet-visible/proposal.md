# Change: Fix pending pets visible in default catalog search

## Why

Support reports that customers are seeing pets that should not be available yet. This confuses customers and creates extra work for operations. The catalog search must show only available pets by default, as documented in the product rules.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-11
- Trigger: Jira webhook `jira:issue_created` event
- Automation: EKS demo issue-to-PR automation

## Assumptions

- The default catalog search behavior should return only available pets
- Explicit status="pending" requests must still work for support and operations
- No schema, authentication, or deployment changes are required
- The fix is safe to implement in the current codebase without breaking backward compatibility

## Non-Goals

- Changing the UI implementation (already correct)
- Adding new pet statuses beyond available/pending
- Modifying adoption flow logic
- Persistence or database changes
- Authentication or authorization changes

## What Changes

- Fix `catalog.py` search_pets function to properly enforce status filtering even when an empty status string is provided
- Add regression tests to ensure empty status strings and default searches exclude pending pets

## Impact

- App behavior: Catalog searches with empty or missing status will correctly default to showing only available pets
- Tests: Add regression tests for empty status string and verify default behavior excludes pending pets
- Humans: PR requires review and merge approval; no deployment changes needed

## Human Gates

- Scope approval: Automated based on sparse bug report pattern
- Review approval: Required before merge (openhands-eks-review label)
- Merge approval: Required by human reviewer
- Deployment approval: Standard deployment process applies
