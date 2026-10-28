# Review the draft pull request

When a pull request receives `openhands-review`, review that PR and its linked request. Follow the repository’s `AGENTS.md`, `sdlc-context-reuse` skill, and `sdlc-code-review` skill. Check the changed behavior and tests; cite what you actually ran or inspected. For documentation, verify deployment claims against current settings and general claims against provider docs. Separate blocking findings, recommendations, and remaining risk. A GitHub comment is not formal approval. People decide changes and merge.

Before posting the final review, remove `openhands-review` and add `openhands-qa` to start QA. Confirm the review label is gone. If the PR already has `openhands:done`, do not restart QA. Do not add `openhands:done` yourself. Post one review comment and confirm it exists before retrying. Say “no blocking findings” when appropriate; never say “approved.”

If no GitHub event is attached, check only repository instructions and GitHub access, then stop. Do not pick a PR, comment, or change labels. Say the event workflow was not exercised.

Link this run only if it provides a real conversation URL or ID. Report success only when the review and QA handoff are complete; otherwise explain what failed.
