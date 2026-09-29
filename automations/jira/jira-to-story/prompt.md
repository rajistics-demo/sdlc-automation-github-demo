# Jira issue to draft pull request

For each new KAN issue, follow the repository’s `AGENTS.md` and `sdlc-story` skill. Use the issue and its acceptance criteria to make a focused change, run relevant checks, and open a draft pull request. After opening it, add the `openhands-review` label before finishing. Do not add `openhands-qa`; review handles the QA handoff. People approve scope, pull requests, merges, and deployments.

If the issue has `sidekick-v2`, `dependency-remediation`, or `security-remediation`, leave it to that demo. Stop without changing Jira or GitHub. For documentation, verify deployment claims against current settings and general claims against provider docs; flag what you cannot verify.

For a manual run without a Jira event, check only the repository, GitHub access, and Jira integration, then stop. Do not pick an issue or post anything. Use the configured Jira authentication method (`JIRA_AUTH_MODE`) for direct checks, and say the event workflow was not exercised.

Link this run only if it provides a real conversation URL or ID. End any Jira comment or pull request description with: `Created by an AI agent (OpenHands) on behalf of Rajiv Shah.` Never expose credentials or change branch protection or deployment settings. Report success only after the draft pull request and review handoff; otherwise explain what failed.
