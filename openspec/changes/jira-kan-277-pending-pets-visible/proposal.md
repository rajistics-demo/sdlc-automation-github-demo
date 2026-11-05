# Change: Add Explicit Regression Tests for Pending Pet Exclusion

## Why

Support reports that customers are seeing pets with "pending" status in the available-pets catalog and adoption flows. While the implementation correctly filters by `status="available"`, the test suite lacks explicit regression tests that verify pending pets like Nova (pet-103) are excluded from default searches. This gap means a future code change could accidentally break the availability filter without immediate test failure.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-277
- Trigger: Jira issue created webhook
- Automation: sdlc-story workflow (issue-to-PR)

## Assumptions

- The core catalog and adoption logic is correct; the fix is to add missing regression tests.
- Nova (pet-103) is the demo's canonical pending pet.
- No changes to business logic, UI behavior, or database schema are needed.
- The existing pytest and Playwright infrastructure is sufficient.

## Non-Goals

- Changes to catalog search implementation
- Changes to adoption validation logic  
- Changes to UI filtering behavior
- New test infrastructure or dependencies
- Performance optimization
- Support for additional pet statuses beyond "available" and "pending"

## What Changes

- Add backend regression tests that explicitly verify default searches exclude Nova
- Add backend regression tests that verify species filters exclude pending pets
- Add backend regression test that verifies searching for Nova by name returns empty when status defaults to "available"
- Document the PENDING_PET_VISIBLE regression scenario

## Impact

- App behavior: No changes - implementation already correct
- Tests: Three new regression tests added to `app/tests/test_pet_catalog.py`
- Humans: Review and approve the PR; merge when CI passes

## Human Gates

- Scope approval: Pending - awaiting confirmation that test-only changes are acceptable
- Review approval: Required before merge
- Merge approval: Required from maintainer
- Deployment approval: N/A (tests only)
