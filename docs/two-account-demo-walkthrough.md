# Two-account SDLC demo walkthrough

Use this walkthrough to show two GitHub identities working with one OpenHands Enterprise organization and one shared repository. The shared repository is `rajistics-demo/sdlc-automation-github-demo`; unrelated personal repositories stay where they are.

## Before the demo

- `rajshah4` is an owner of the `rajistics-demo` GitHub organization. `rajistics` is a member with **Read** access to the SDLC repository.
- The organization-owned OpenHands GitHub App is installed on the SDLC repository. Installation selects the repositories the App can reach; each person's GitHub sign-in identifies that person. Signing in does not grant new repository permissions.
- Both accounts can sign in to the same OpenHands Enterprise organization and open the shared repository. Use separate browser sessions or switch GitHub accounts deliberately so the presenter can show which identity is active.
- The SDLC Jira, review, and QA automations are configured for this repository. The Jira trigger accepts a `KAN` **Task** without the `sidekick-v2`, `dependency-remediation`, or `security-remediation` labels.

## Presenter flow

1. As `rajshah4`, show the shared repository in OpenHands and create a small `KAN` Task in Jira. The Jira automation should open a **draft** pull request in the SDLC repository and add `openhands-review`.
2. Show the review comment and handoff to `openhands-qa`. QA should post a test report and leave `openhands:done`. A comment saying there are no blocking findings is **not** formal GitHub approval.
3. Sign in as `rajistics` in a separate session. Open the same OpenHands organization and repository, then inspect the same pull request and ask OpenHands to explain the change. This is the Read-access path; it does not require moving the repository or copying the owner's credentials.
4. Explain the optional contribution path: `rajistics` needs **Write** on this repository to push a branch here. **Triage** or Write can apply labels to trigger the GitHub automations. The private `rajistics-demo/openhands-demo` starter repository already provides a separate safe Write-access example. Keep the SDLC repository at Read until its owner chooses to grant more access.

## What each layer controls

| Layer | What it controls |
| --- | --- |
| GitHub organization membership | Whether the account belongs to `rajistics-demo`; membership alone does not imply repository Write access. |
| Repository permission | Whether that account can read, comment, push branches, or manage labels. Read allows inspection; Triage can apply labels; Write allows direct pushes. |
| GitHub App installation | Which repositories the organization permits OpenHands to access. The owner manages this installation. |
| OpenHands sign-in | Which GitHub identity is attached to the person's OpenHands session. Each person signs in separately. |
| Automation configuration | Which events start an agent, and which configured integration or secret the agent uses. A member's sign-in does not automatically supply that member's credentials to an existing automation. |

Humans decide scope, review, merge, and deployment. Do not display or copy GitHub App keys, Jira tokens, or other secrets during the demo.

GitHub references: [App installation versus user authorization](https://docs.github.com/en/apps/using-github-apps/installing-a-github-app-from-a-third-party) and [organization repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).
