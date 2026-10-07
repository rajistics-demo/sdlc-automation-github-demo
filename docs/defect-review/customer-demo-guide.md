# Customer walkthrough: existing code → verified repair

> **The demonstration:** a Jira ticket gives OpenHands a repository and review scope. The agent finds defects, proves them, writes a repair spec, and produces tested fixes for human review.

Use **billing as the finished example** and **Petstore as the live run**. Start with the evidence and business impact; use the implementation details when the customer asks how a fix works.

## Finished example: billing

Open [the billing conversation](https://app.replicated.rajistics.com/canvas/conversations/d19f7e68c2604e32867f748541b85dad?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6). Show `review_runs/KAN-216/validation.md` first, then a finding and its corresponding test and code change.

**Opening:** “The original tests were green, but they only checked happy paths. We asked the agent to review the existing service against its product rules, find defects, and repair the confirmed problems.”

### Three strong examples

| Customer problem | What OpenHands found and repaired | Evidence to show |
| --- | --- | --- |
| A caller could impersonate another customer or read their invoice | Removed client-header identity override, rejected invalid tokens, and constrained invoice reads and payments to the verified customer | AUTH-1, AUTH-2, ISO-1; unauthorized requests return 401 and cross-customer objects return 404 |
| Retries and concurrent payments could corrupt billing records | Added idempotent receipt replay, atomic ledger/balance writes, and serialized balance checks | Same-key retries share one receipt and one ledger row; competing payments cannot overpay; injected failures roll back both writes |
| Invoice listing made a query for every invoice | Replaced N+1 totals with one SQL aggregation and applied pagination | For the 60-invoice fixture, 61 SELECTs became 1; tests enforce a maximum of 3 SELECTs independent of page size |

### The validation story

| Evidence | Result |
| --- | --- |
| Original happy-path tests | 3 passed before and after |
| Final regression suite on original code | 20 failures, 1 error, 2 passes |
| Repository suite after repairs | 26 passed |
| Independent operator acceptance checks | 13 passed |

Independent checking caught a remaining simultaneous-retry failure in the first repair. The operator supplied the failing case; OpenHands reproduced it, added regression tests, corrected the transaction logic, and passed validation. Present this as a **review-and-correction loop**, not as a flawless first attempt.

The initial agent review found 10 defects. The retry refinement is tracked as PAY-5, bringing the final findings/refinements to 11. Initial triage ran on Sonnet; specification and repair ran on `openai/claude-opus-4-7`.

## Live example: Petstore

Follow [the live launch instructions](live-petstore.md). Create a **new KAN Task**, put **`defect-review` on it before creation**, and paste the repository and scope. The automation starts on `jira:issue_created`; editing an old ticket does not start a new run.

**Opening:** “I’m giving OpenHands the repo and a review scope. The ticket doesn’t list the defects. The agent will inspect the code and product rules, then show the evidence for its findings.”

While it runs, explain the five stages: **discover → specify → repair → validate → prepare human review**. Keep billing open as the completed example. The earlier Petstore rehearsal is available as a fallback.

## Claims supported by this demo

- OpenHands can review existing code against documented product intent and discover reproducible defects.
- It can produce a repair specification and tests linked to the findings.
- It can implement fixes across authentication, isolation, query handling, and transaction logic in this fixture.
- It can respond to validation feedback and correct a missed case.
- It can preserve existing happy-path tests and prepare evidence for human review.

## Keep the explanation precise

This is deliberately flawed synthetic code with fictional data and product rules in the repo. Fixture tokens simulate an upstream identity provider; this demo does not implement a production identity system. Payments are ledger entries, with no real provider or customer charge. Query counts demonstrate fewer database round trips; they do not measure production throughput. The agent's self-review is identified as self-review; the operator separately ran acceptance checks. A PR draft exists, but no pull request has been published.

**Closing:** “The useful result is a repair you can inspect: findings, a spec, changed code, and before-and-after tests. Your review and validation gates still decide whether it is ready to merge.”
