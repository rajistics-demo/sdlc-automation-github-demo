# Turn a Jira request into a draft pull request

When a new issue arrives in the KAN demo project, use its request and acceptance criteria to make a focused change in the cloned repository. Follow `AGENTS.md` and the `sdlc-story` skill. Run the relevant checks, then open a draft pull request for a person to review. After opening it, add the `openhands-review` label before finishing. Do not add `openhands-qa` here; the reviewer handles the QA handoff. People decide scope, approve, merge, and deploy.

Issues labeled `sidekick-v2`, `dependency-remediation`, or `security-remediation` belong to other demos. If one arrives, stop without changing Jira or GitHub; report that its own workflow should handle it.

For documentation, check claims about this deployment against current settings and general claims against provider documentation. Identify anything you cannot verify. Do not expose credentials or change branch protection or deployment settings.

If this is a manual run with no Jira event, check the repository, GitHub access, and Jira integration read-only, then stop. Do not pick an issue or post anything. Use the configured Jira authentication method (`JIRA_AUTH_MODE`) for any direct check. Say that the event workflow was not exercised.

Link this run in the pull request only if it provides a real conversation URL or ID. Never invent one. End any Jira comment or pull request description with: `Created by an AI agent (OpenHands) on behalf of Rajiv Shah.`

Finish with a short outcome summary. For an event run, report success only after the draft pull request and review handoff are complete; otherwise explain what is blocked or failed.
