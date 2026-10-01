# Design

## Context

The SDLC Automation Demo repository was transferred from `rajshah4` to `rajistics-demo` on GitHub. GitHub automatically redirects web page links (issues, PRs, etc.) from the old location to the new one, but automation configurations, event filters, and repository clone settings must explicitly reference the new organization name.

The repository contains:
- Customer-facing documentation in `README.md` and `docs/`
- Automation registration scripts in `scripts/automations/` that define default repository URLs
- Agent Canvas scripts that reference the demo repository
- Test fixtures that represent historical GitHub webhook events

## Decision

- **Update all documentation and setup scripts** to reference `rajistics-demo/sdlc-automation-github-demo`
- **Update default values in automation registration scripts** so new installations use the correct repository URL
- **Preserve test fixtures unchanged** because they represent historical data and should accurately reflect the organization name at the time of the original events
- **Add explanation to setup documentation** clarifying what redirects after a transfer and what requires explicit updates
- **Make the active Jira, review, and QA prompts readable to customers** while retaining event routing, evidence checks, label handoffs, and human approval boundaries. This follows the separate user request to improve automation prompts and check their live results.
- **Update prompt and repository-default tests** to cover the new behavior. Historical event fixtures remain unchanged. Product code, credentials, and deployment settings are outside this change.

## Risks

- **Risk**: Users with existing automation configurations may continue using old repository references that still work due to GitHub redirects
  - **Mitigation**: Documentation explains that while redirects work for web pages, automation event filters and repository cloning should use the new organization name for consistency and clarity

- **Risk**: Historical test fixtures referencing `rajshah4` might be mistaken for errors
  - **Mitigation**: Test fixtures intentionally preserve historical accuracy and represent actual GitHub events as they occurred

## Validation Plan

- Run the OpenSpec validation script: `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-KAN-191-update-rajistics-demo-repo-url/`
- Verify all URLs in documentation files reference `rajistics-demo`
- Confirm automation registration scripts use the new default URL
- Run the prompt, repository-default, and full test suites; confirm no product code or historical event fixtures were modified
- Verify the revised prompts with a live Jira Task to draft PR to review to QA run
