# PR description format

Use this structure for `pr-draft.md` and the approved GitHub PR body. Replace the prompts with verified evidence; do not leave placeholders in a published description. Scale detail to the actual change. Keep the title concrete and the opening readable without inspecting the conversation.

## Result

State which confirmed defects the repair addresses and the resulting user-visible behavior. Give actual repository test totals and separately reported operator checks, if performed. State that human review and merge remain pending.

## Review request and baseline

Use a compact table with the Jira request link, review scope, full baseline commit SHA, repair branch, and existing test coverage. Explain when happy-path tests passed despite the discovered defects.

## Findings and repaired behavior

Use a table: finding ID, priority when established by triage, original behavior/business impact, and repair/acceptance criterion. Preserve IDs so readers can trace each finding to the spec and tests. For a simple fixture, use a concrete before/after example with accurate units.

If validation exposed a defect in the first repair, describe that refinement honestly. Distinguish initial findings from later additions; do not imply all findings were discovered autonomously in the first pass.

## Implementation and specification

Explain the relationship between the product contract, repair spec, and implemented changes. Use a file-to-change table for application code and tests. Mention schema changes explicitly. State preserved behavior and intentional behavior changes separately. Do not claim unchanged signatures mean unchanged behavior.

## Validation evidence

Use a before/after table separating existing tests, new regression tests, and total repository tests. Describe how the before run was obtained. Separate operator acceptance checks from repository tests and do not invent their baseline results. Explain tests that passed on the original code when relevant.

Provide the exact runnable repository test command. Add measured query counts, concurrency outcomes, or fault-injection evidence when relevant. Preserve units and tested sample sizes. A ledger entry is not a real payment-provider charge; query-count reduction is not a throughput multiplier. Do not copy unreproducible selectors or unavailable temporary files into test instructions.

## Review evidence and limitations

Identify agent self-review as self-review. Describe independently performed checks only when their evidence exists. List meaningful remaining risks, deferred scope, and fixture limitations. Avoid security certification, production readiness, universal concurrency guarantees, or “no regressions” claims broader than the tests. Keep merge/deployment decisions with humans.

## Trace the work

Provide clickable links to the repair specification, regression tests, triage/validation evidence, Jira ticket, and verified current OpenHands conversation. Use actual repository paths and branch names. Check required links before publication. Never include tokens, customer names, or real customer data.

State actual publication status. If historical sandbox artifacts say held locally after publication, explain that those describe the earlier state. An opened draft PR must be identified as draft, not approved or merged.
