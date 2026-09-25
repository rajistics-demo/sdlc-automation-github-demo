# Jira request to draft pull request

For a Jira event, follow the cloned repository’s `AGENTS.md` and `sdlc-story` skill. Use the Jira request and its acceptance criteria to make a focused change, validate it, and open a draft pull request for human review. After opening the pull request, add the `openhands-review` label before finishing so the review can start. Do not add `openhands-qa` here; review owns that handoff. Leave scope decisions, approval, merge, and deployment to people. Do not expose credentials or change branch protection or deployment settings.

Add a conversation link to the pull request only when the current run provides a verifiable URL or conversation ID. Never guess a link. End every Jira comment and pull request description posted by this run with: `Created by an AI agent (OpenHands) on behalf of Rajiv Shah.`

If started manually without a Jira event, check only that the repository, its instructions, GitHub access, and Jira integration are available. If probing Jira directly, use its configured authentication method (`JIRA_AUTH_MODE`); a failed probe with a different method does not prove the integration is broken. Do not change Jira or GitHub. Report that the event workflow was not exercised.

Finish with a structured status and a short outcome summary. Mark success only after the draft pull request and required handoff are complete; otherwise explain what remains blocked or failed.
