# Jira OpenHands Automation

This folder contains the Jira-triggered automation packages for the SDLC Automation Demo.

The Jira webhook should send `jira:issue_created` events from the `KAN` project into the Rajistics custom webhook source named `jira-direct`.

## Work Cell

| Work cell | Jira trigger | Human boundary |
| --- | --- | --- |
| `jira-to-story` | Any KAN issue created | OpenHands opens or updates a PR; humans review and merge |
| `jira-to-story-sidekick-v2` | KAN Task created with `sidekick-v2` label | OpenHands starts visible read-only docs/logs/repo scout conversations, then the main implementation conversation. |

## Registration Notes

The visible automation prompts should stay short. Jira-specific implementation
details, OpenSpec-style artifacts, evidence waypoints, and handoff behavior live
in `skills/sdlc-story/`. The visible sidekick launcher contract lives in
`skills/sdlc-sidekick-launcher/`; context-scout output conventions live in
`skills/sdlc-context-sidekick/`.

Use the existing Rajistics webhook source:

- Source: `jira-direct`
- Event: `jira:issue_created`
- Filter: all new issues in `KAN`. No Jira label or issue type is required for the main demo.

The prompt tells the main work cell to stop without changing Jira or GitHub if a
issue has the `sidekick-v2`, `dependency-remediation`, or `security-remediation`
label. The filter will still start the main work cell for those issues, so the
separate demo automation may also start. Keep that overlap in mind when showing
one of the other demos.

Do not include repo names, file paths, log codes, or implementation clues in demo Jira tickets.

For the visible sidekick demo, disable the normal `jira-to-story` automation and
enable `jira-to-story-sidekick-v2` so one Jira issue wakes only one work cell.
