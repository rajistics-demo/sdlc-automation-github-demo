---
name: repo-defect-repair
description: Turn confirmed repository-review findings into a repair specification, implement bounded fixes, and validate them with regression evidence. Use after repo-defect-triage when the request authorizes repair.
---
# Findings to repair
Reuse the existing `skills/sdlc-story/references/open-spec-template.md` for artifact structure, `skills/sdlc-code-review/SKILL.md` for review priorities, and `skills/sdlc-qa/SKILL.md` for validation expectations. These existing skills contain Petstore-specific rules and GitHub posting instructions: apply the selected target's product rules and the request's publication permissions instead. This workflow does not automatically trigger their publishing steps.

1. Read triage artifacts and verify their baseline SHA matches the checkout. Select confirmed findings within the requested scope. If the request says fix the highest-priority finding, do not silently fix every finding.
2. Before application edits, create `openspec/changes/<issue-key>-repair/` with proposal.md, design.md, tasks.md, and specs/repair/spec.md. Map every selected finding ID to a requirement, reproduction, regression test, and acceptance criterion. State preserved behavior, exclusions, deferred findings, and human merge/deployment gates. Drafting this repair spec is automatic when the user has authorized review and repair; do not add an unnecessary spec-approval stop.
3. Create a `codex/repair-<issue-key>` branch. Add tests that fail on the original code. Capture that failing run before repairing. Keep existing tests and business rules intact. Implement the smallest coherent repair; do not rewrite the application or replace checks with hardcoded fixture results.
4. Run the new tests, full existing suite, and relevant boundary checks. For scalability findings use query-count or complexity evidence, not one laptop timing claim. For concurrency and idempotency use real SQLite connections/threads and persisted-state assertions. A hook for fault injection must not be part of a production authentication mechanism. Do not claim a performance or security certification from fixture tests.
5. Review the final diff against the spec and original findings. Save `review_runs/<issue-key>/validation.md`, `review.md`, and `pr-draft.md` containing actual commands/results, remaining risks, and a complete draft PR description. A self-review must be identified as such; do not call it an independent agent review.
6. For this operator's rehearsal, do not push, open PRs, post reviews, or write Jira comments. Keep the repaired branch and artifacts in the sandbox for inspection. Return proposed publication content and destinations for exact approval. Do not merge, deploy, or bypass infosec/pentest gates.

Final response: target repository and SHA; finding IDs; spec paths; changed files; failing-before/passing-after commands; remaining findings; publication status; sandbox artifact paths. Report `validated`, `partial`, `needs-human`, or `failed` honestly. The automation transport reporting completion does not prove the repair passed.

## Demo retention
Do not archive the current conversation or any related conversation. Keep the demo history visible.
