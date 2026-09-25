# Review a pull request

**Manual test with no event:** Check only the repository, instructions, and GitHub access, then stop. Do not search for or select a pull request, even if one has `openhands-review`. Do not post comments or change labels. Mark the readiness check successful when those checks pass, and say that the event workflow was not exercised.

When a pull request receives `openhands-review`, follow the cloned repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-code-review` skill. Read the pull request and linked request, check the changed behavior and tests, and report concrete findings with evidence and remaining risk. For documentation, check deployment-specific claims against current settings and general rules against provider documentation; formatting checks alone do not establish accuracy. Do not claim a test passed unless you ran it or can cite its result.

Before posting the final review comment, remove `openhands-review` and add `openhands-qa` so QA can start. Check that the review label is gone. If QA already advanced the pull request to `openhands:done`, do not re-add `openhands-qa`. Do not add `openhands:done` yourself; QA owns the final status. Post exactly one GitHub result, then verify it exists before retrying. Distinguish findings from recommendations. In a PR comment, use “no blocking findings” when appropriate; never call the comment “approved” or imply formal GitHub approval. People decide whether to approve, change, or merge the pull request.

Use a conversation link only when it identifies this run. Never guess one. Finish with a structured status and a short outcome summary; for event runs, mark success only after the GitHub handoff and review are complete.
