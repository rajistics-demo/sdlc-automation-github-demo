# Change: Update SDLC Demo Setup Guide for rajistics-demo Organization

## Why

The SDLC Automation Demo repository has been transferred from the personal `rajshah4` GitHub account to the `rajistics-demo` organization. The customer-facing setup guide and related documentation must use the new repository URL so both demo accounts follow the same instructions and automation configurations reference the correct repository location.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-191
- Trigger: jira:issue_created
- Automation: Jira Bug to PR - KAN Task to PR

## Assumptions

- GitHub page links (issues, PRs, etc.) redirect automatically after a repository transfer
- OpenHands event filters and cloned repository settings must use the new owner/repository name
- The repository is already transferred and accessible at https://github.com/rajistics-demo/sdlc-automation-github-demo
- No changes to product code, credentials, GitHub permissions, or deployment settings are required

## Non-Goals

- Changing product code or application functionality
- Modifying credentials or secrets
- Updating GitHub permissions or branch protection rules
- Altering deployment settings or infrastructure
- Changing test fixtures that represent historical event data

## What Changes

- Documentation files updated to reference `rajistics-demo/sdlc-automation-github-demo` instead of `rajshah4/sdlc-automation-github-demo`
- Automation registration scripts updated with the new default repository URL
- README and setup guides updated with the correct GitHub organization
- Agent Canvas and related scripts updated to use the new repository reference
- Customer-facing Jira, review, and QA prompts shortened at the user's request while preserving the event handoffs and human gates
- Tests updated for the current repository defaults, trigger filter, and concise prompt contracts

## Impact

- **App behavior**: No changes to application code. Automation prompt instructions and the Jira trigger filter change; live configurations were updated and tested separately.
- **Tests**: Assertions change to match the current repository defaults and concise prompts. Historical GitHub event fixtures remain unchanged.
- **Humans**: Setup instructions now reference the correct repository location; existing automation configurations will need the environment variable `GITHUB_DEMO_REPO_URL` set to the new URL or will use the updated default

## Human Gates

- **Scope approval**: Jira issue KAN-191 covers the repository move; the user separately requested customer-readable prompts and live verification
- **Review approval**: Required before merge - humans must verify the repository references and prompt behavior
- **Merge approval**: Required - humans approve the final PR
- **Deployment approval**: Required if applying repository automation definitions to a new environment; this PR does not deploy the application
