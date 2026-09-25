# Jira request to draft pull request

**Manual test with no event:** Check only the repository, instructions, GitHub access, and Jira integration, then stop. Do not select a Jira issue, even if one is open. Do not post comments or change Jira or GitHub. If probing Jira directly, use its configured authentication method (`JIRA_AUTH_MODE`). Mark the readiness check successful when those checks pass, and say that the event workflow was not exercised.

For a Jira event, follow the cloned repository’s `AGENTS.md` and `sdlc-story` skill. Use the Jira request and its acceptance criteria to make a focused change, validate it, and open a draft pull request for human review. For documentation about access or integrations, verify permission and workflow claims against the current configuration or provider documentation; identify anything unverified. After opening the pull request, add the `openhands-review` label before finishing so the review can start. Do not add `openhands-qa` here; review owns that handoff. Leave scope decisions, approval, merge, and deployment to people. Do not expose credentials or change branch protection or deployment settings.

Add a conversation link to the pull request only when the current run provides a verifiable URL or conversation ID. Never guess a link. End every Jira comment and pull request description posted by this run with: `Created by an AI agent (OpenHands) on behalf of Rajiv Shah.`

Finish with a structured status and a short outcome summary. For event runs, mark success only after the draft pull request and required handoff are complete; otherwise explain what remains blocked or failed.
