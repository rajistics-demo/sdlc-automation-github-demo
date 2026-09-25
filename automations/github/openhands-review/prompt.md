# Review a pull request

When a pull request receives `openhands-review`, follow the cloned repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-code-review` skill. Read the pull request and linked request, check the changed behavior and tests, and report concrete findings with evidence and remaining risk. Do not claim a test passed unless you ran it or can cite its result.

Before posting the final review comment, remove `openhands-review` and add `openhands-qa` so QA can start. Do not add `openhands:done`; QA owns the final status. Post one clear pull request review or comment that distinguishes findings from recommendations. If the GitHub account cannot formally review its own pull request, post a comment and do not claim GitHub approval. People decide whether to approve, change, or merge the pull request.

If started manually without a pull request event, check only the repository, instructions, and GitHub access. Do not change a pull request or its labels. Report that the event workflow was not exercised.

Use a conversation link only when it identifies this run. Never guess one. Finish with a structured status and a short outcome summary; mark success only after the GitHub handoff and review are complete.
