# Documentation Spec Delta

## ADDED Requirements

### Requirement: Setup documentation references correct repository organization

The setup guide, README, and automation registration scripts must reference the current repository location at `rajistics-demo/sdlc-automation-github-demo` so that users following the instructions can successfully clone and configure the demo.

#### Scenario: User follows setup instructions

- Given a user following the setup checklist or README
- When they reference repository URLs or clone commands
- Then all URLs point to `https://github.com/rajistics-demo/sdlc-automation-github-demo`

#### Scenario: User registers automations with default settings

- Given a user running automation registration scripts without custom environment variables
- When the scripts use default repository URL values
- Then the scripts register automations pointing to `https://github.com/rajistics-demo/sdlc-automation-github-demo`

### Requirement: Documentation explains GitHub transfer behavior

Setup documentation should explain the difference between resources that redirect automatically after a transfer versus those that require explicit updates.

#### Scenario: User understands what needs updating after repository transfer

- Given documentation explaining GitHub transfer behavior
- When a user reads about the repository move
- Then they understand that:
  - GitHub page links (issues, PRs) redirect automatically
  - OpenHands event filters must use the new owner/repository name
  - Cloned repository settings must reference the new organization

## UNCHANGED Requirements

### Requirement: Test fixtures preserve historical accuracy

Test fixtures that represent actual historical GitHub webhook events remain unchanged even if they reference the old organization, as they document what actually occurred.

#### Scenario: Historical test fixtures remain accurate

- Given test fixtures containing GitHub event payloads from before the transfer
- When reviewing test data
- Then the fixtures accurately reflect the `rajshah4` account as it existed at the time of the original events
