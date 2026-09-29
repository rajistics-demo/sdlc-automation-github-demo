# Check the pull request and hand the result to people

When a PR receives `openhands-qa`, follow the repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-qa` skill. Read the diff and acceptance criteria. Run focused tests, then broaden checks when useful. For visible UI changes, gather browser evidence if available and name any fallback. Verify documentation claims against current settings or provider docs. Measure file and test counts from actual output, and report only checks and permissions you can substantiate. Do not infer account identities or permissions from `AGENTS.md`. People decide whether to merge or deploy.

Use the PR identified by the attached GitHub event. `pull_request.number` identifies a PR directly; for an `issues.labeled` event with `issue.pull_request`, resolve its PR number from the issue. The event need not be saved as `event.json`. Only when there is no event at all, check repository instructions and GitHub access read-only, then stop. Do not pick a labeled PR, post, or change labels. Say the event workflow was not exercised.

Post one QA report with commands, results, artifacts, and remaining risk. Confirm it exists before retrying. Then remove `openhands-qa` and stale `openhands:in-progress`; add `openhands:done` only if QA succeeded, or `openhands:needs-human` otherwise. Verify the final labels.

Link this run only if it provides a real conversation URL or ID. Summarize what was verified and whether the handoff completed; do not imply formal approval.
