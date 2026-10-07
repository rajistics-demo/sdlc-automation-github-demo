# Live demo: Petstore defect review

> Create a Jira ticket. OpenHands reviews the existing repo, proves its defects, drafts a repair spec, and produces tested fixes.

## Start the automation

1. Open [Jira](https://rajiv-shah.atlassian.net) and create a **new Task** in project **KAN**.
2. Add the label **`defect-review` before creating the ticket**.
3. Paste the summary and description below, then click **Create**.
4. Open [OpenHands conversations](https://app.replicated.rajistics.com/canvas/conversations) and select the new **SDLC_0 - Jira Simple Defect Review** run.

**Summary**

```text
Review Petstore for defects and repair them
```

**Description**

```text
Repository: https://github.com/rajistics-demo/petstore-defect-demo
Ref: main
Mode: review-and-repair
Scope: Review catalog visibility, adoption eligibility, and order totals. Repair all confirmed defects in this scope.
```

The trigger is **ticket creation**. Adding the label to an old ticket or editing KAN-215 will not start a new run. A fresh ticket gets a fresh sandbox and a repair branch named for its issue key.

## What to show as it runs

| Stage | Customer-visible proof |
| --- | --- |
| Existing code | Original tests pass, despite defects in business rules |
| Discovery | Findings include source locations, impact, and reproductions |
| Specification | Each selected defect maps to a requirement and regression test |
| Repair | New tests fail before the fix and pass afterward |
| Review | Validation evidence, self-review, and a PR draft ready for a human |

Say: “The ticket gives the agent the repo and review scope. It has to find and prove the problems before fixing them.” The repository includes product rules, so this is review against documented intent, not guessing what the software should do.

## Launch check

| Setting | Required state |
| --- | --- |
| Automation | `SDLC_0 - Jira Simple Defect Review` enabled |
| Model | `Bedrock-Claude-Sonnet-4-5-fast` (Sonnet 4.5) |
| Trigger | KAN Task created with `defect-review` and the Petstore URL |
| Old flow | `SDLC_1 - Jira to PR` disabled |
| Controller branch | `codex/jira-defect-triage` |
| Target branch | `main` stays intentionally flawed |
| Publication | Local PR draft; no automatic PR or Jira comment |
| History | No archiving; sandbox files can expire, so preserve artifacts |

If no run appears, check the new ticket's project, issue type, label, and exact repository URL, then inspect [Automations](https://app.replicated.rajistics.com/canvas/automations). Do not re-enable the old broad Jira flow.

## Keep the finished example ready

Use [billing's finished conversation](https://app.replicated.rajistics.com/canvas/conversations/d19f7e68c2604e32867f748541b85dad?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6) while Petstore runs. Lead with the final findings and validation report; use the detailed history to explain the review and repair process.

The earlier [Petstore rehearsal](https://app.replicated.rajistics.com/canvas/conversations/be232b755ebc4c27901dcd0ca71dbecb?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6) is a fallback: 3 findings repaired, 13 repository tests and 5 independent acceptance checks passed.
