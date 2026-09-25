# QA a pull request

When a pull request receives `openhands-qa`, follow the cloned repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-qa` skill. Read the diff and acceptance criteria, run focused tests for the changed behavior, then broaden checks when useful. For visible UI changes, gather browser evidence if the available tools permit it; clearly identify any fallback checks. Do not claim a test or UI check passed without evidence.

Post a concise pull request report with the commands, results, artifacts, and remaining risk. Once the report is posted, remove `openhands-qa` and stale `openhands:in-progress`, then add `openhands:done` only when QA succeeded; otherwise add `openhands:needs-human`. People decide whether the evidence is sufficient and whether to merge or deploy.

If started manually without a pull request event, check only the repository, instructions, and GitHub access. Do not change a pull request or its labels. Report that the event workflow was not exercised.

Use a conversation link only when it identifies this run. Never guess one. Finish with a structured status and a short outcome summary that matches the checks and GitHub handoff actually completed.
