# QA a pull request

**Manual test with no event:** Check only the repository, instructions, and GitHub access, then stop. Do not search for or select a pull request, even if one has `openhands-qa`. Do not post comments or change labels. Mark the readiness check successful when those checks pass, and say that the event workflow was not exercised.

When a pull request receives `openhands-qa`, follow the cloned repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-qa` skill. Read the diff and acceptance criteria, run focused tests for the changed behavior, then broaden checks when useful. For documentation, verify factual claims against current configuration or provider documentation; a Markdown or keyword check alone is insufficient. For visible UI changes, gather browser evidence if the available tools permit it; clearly identify any fallback checks. Do not claim a test or UI check passed without evidence.

Post exactly one pull request report with the commands, results, artifacts, and remaining risk. Before retrying a post, check whether the report already exists. Once it is posted, remove `openhands-qa` and stale `openhands:in-progress`, then add `openhands:done` only when QA succeeded; otherwise add `openhands:needs-human`. Verify the final labels. People decide whether the evidence is sufficient and whether to merge or deploy.

Use a conversation link only when it identifies this run. Never guess one. Finish with a structured status and a short outcome summary that matches the checks and GitHub handoff actually completed.
