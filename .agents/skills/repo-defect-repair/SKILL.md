---
name: repo-defect-repair
description: Turn confirmed repository-review findings into a repair specification, implement bounded fixes, and validate them with regression evidence. Use after repo-defect-triage when the request authorizes repair.
---
# Defect Repair & Validation

> **Turn confirmed findings into a specified, tested repair.**  
> Every selected finding must connect to a requirement, regression test, and validation result.

**Flow:** Findings → repair spec → regression tests → bounded fixes → review evidence

## Reuse the software factory

| Existing guidance | Use it for |
| --- | --- |
| `skills/sdlc-story/references/open-spec-template.md` | Repair specification structure |
| `skills/sdlc-code-review/SKILL.md` | Review priorities |
| `skills/sdlc-qa/SKILL.md` | Validation expectations |

Apply the selected target's product rules and the request's publication permissions. The existing skills include Petstore examples and GitHub posting instructions; this workflow does not automatically invoke their publishing steps.

## 1. Select the repair scope

Read the triage artifacts and verify that the baseline SHA matches the checkout. Select only confirmed findings within the requested scope. A request to fix the highest-priority finding does not authorize silently fixing every finding.

## 2. Write the repair spec

**Before application edits**, create:

```text
openspec/changes/<issue-key>-repair/
├── proposal.md
├── design.md
├── tasks.md
└── specs/repair/spec.md
```

Map every selected finding through this chain:

**Finding ID → requirement → reproduction → regression test → acceptance criterion**

State preserved behavior, exclusions, deferred findings, and human merge/deployment gates. When review and repair are authorized, draft the spec automatically; do not introduce an unnecessary spec-approval stop.

## 3. Capture failure, then repair

Create a `codex/repair-<issue-key>` branch. Add regression tests and **capture their failing run against the original code** before implementing repairs.

Keep existing tests and business rules intact. Implement the smallest coherent repair. Do not rewrite the application or hardcode fixture results to satisfy checks.

## 4. Validate the result

Run the new tests, the full existing suite, and relevant boundary checks.

| Finding type | Required validation |
| --- | --- |
| Functional correctness | Regression fails before repair and passes after it |
| Scalability | Query-count or complexity evidence, beyond a single timing measurement |
| Concurrency and idempotency | Real SQLite connections/threads and persisted-state assertions |
| Atomicity | Fault injection demonstrates that writes commit or roll back together |

Fault-injection hooks must not become production authentication mechanisms. Fixture tests do not establish a performance or security certification.

## 5. Prepare human review

Review the final diff against the spec and original findings. Save:

| Artifact | Reviewer-facing content |
| --- | --- |
| `validation.md` | Actual commands, results, and before/after evidence |
| `review.md` | Spec compliance, remaining defects, and risks |
| `pr-draft.md` | Complete proposed PR description |

Place these in `review_runs/<issue-key>/`. Identify self-review explicitly; do not describe it as an independent agent review.

## Publication boundary

For this rehearsal, keep the repaired branch and artifacts in the sandbox. **Do not push fixes, open PRs, post reviews, or write Jira comments.** Return the exact proposed publication content and destinations for approval. Do not merge, deploy, or bypass infosec/pentest gates.

A PR draft is a reviewable artifact; it is not an opened pull request.

## Completion report

Report the target repository and baseline SHA, finding IDs, spec paths, changed files, failing-before/passing-after commands, remaining findings, publication status, and sandbox artifact paths.

Use an honest result: **`validated` · `partial` · `needs-human` · `failed`**. Automation transport completion does not establish that the repair passed.

## Write for the reviewer

Lead reports with the result, then a compact finding-to-test table and before/after test totals. Put detailed commands and logs below that overview. Keep the PR draft focused on the problem, changed behavior, validation, and remaining risks; link supporting artifacts rather than repeating their contents. Avoid decorative checkmarks, duplicate sections, and claims broader than the evidence.

## Keep the demo visible

**Do not archive this conversation or any related conversation.** Preserve the demo history for human review.
