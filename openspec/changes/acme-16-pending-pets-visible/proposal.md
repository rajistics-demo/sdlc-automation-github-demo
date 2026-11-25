# Change: Fix Pending Pets Status Filter Bypass

## Why

Support reports that some customers are able to see and start adoption flows for pets that should not be available yet. This is confusing customers and creating extra work for operations. The pet catalog's status filter has a logic flaw that allows pending pets to be visible when an empty status string is provided, violating the product rule that "default pet search returns only available pets."

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/ACME-16
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Issue to PR

## Assumptions

- The status parameter should always be respected when provided
- Empty string is a meaningful filter value (matches no pets with status "")
- The default "available" behavior is correct and should be preserved
- This bug is likely exploited through direct API usage, not the UI (which hardcodes "available")

## Non-Goals

- Adding UI controls for filtering by pending status
- Changing the adoption validation logic (already correct in `adoptions.py`)
- Modifying the default status parameter value
- Investigating whether this was deliberately exploited or accidental

## What Changes

- Fix `app/petstore_app/catalog.py` line 50: Replace truthy check with explicit None check
- Add regression test to verify empty status string doesn't bypass the filter
- Ensure existing tests continue to pass

## Impact

- App behavior: Empty status strings will no longer bypass the filter and return all pets
- Tests: One new regression test added; all existing tests should pass
- Humans: Code review and QA approval required before merge

## Human Gates

- Scope approval: Automated (straightforward bug fix)
- Review approval: Required (via openhands-eks-review label)
- Merge approval: Required (human reviewer decision)
- Deployment approval: Required (production release decision)
