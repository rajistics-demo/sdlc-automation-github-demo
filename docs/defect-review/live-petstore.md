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
| Review | Validation evidence, self-review, and a structured draft GitHub PR within the approved publication scope |

Say: “The ticket gives the agent the repo and review scope. It has to find and prove the problems before fixing them.” The repository includes product rules, so this is review against documented intent, not guessing what the software should do.

## Launch check

| Setting | Required state |
| --- | --- |
| Automation | `SDLC_0 - Jira Simple Defect Review` enabled |
| Model | `Bedrock-Claude-Sonnet-4-5-fast` (Sonnet 4.5) |
| Trigger | KAN Task created with `defect-review`, without `defect-review-complex` |
| Old flow | `SDLC_1 - Jira to PR` disabled |
| Controller branch | `codex/jira-defect-triage` |
| Target branch | `main` stays intentionally flawed |
| Publication | Use the approved demo publication scope; review the final title/body and verify both links |
| History | No archiving; sandbox files can expire, so preserve artifacts |

If no run appears, check the new ticket's project, issue type, label, and exact repository URL, then inspect [Automations](https://app.replicated.rajistics.com/canvas/automations). Do not re-enable the old broad Jira flow.

## Keep the finished example ready

The latest completed live run is [KAN-218](https://rajiv-shah.atlassian.net/browse/KAN-218) (**Done**), with [draft PR #3](https://github.com/rajistics-demo/petstore-defect-demo/pull/3) and its [OpenHands conversation](https://app.replicated.rajistics.com/canvas/conversations/729d5319cd9543c6b1129bb26979717d?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6).

It repaired three findings. The corrected result passes 11 repository tests and six separate operator acceptance checks. Running the final repository suite against the original code produces six failures. The first repair passed 10 tests but missed explicit `search_pets(None)` filtering; operator feedback prompted the agent to correct that case and add its regression test. Present that as a validation/refinement loop, not an unassisted first-pass success.

### Publication handoff for the live run

Use a guided live run. The Replicated prompt preset does not reliably supply its public conversation URL. If the agent asks for it, copy the actual browser URL for that run and provide it in the conversation before publishing. The rehearsal supplied that exact URL through operator feedback. Do not reuse a finished run's URL for a new run or accept a placeholder such as `${AUTOMATION_SESSION_URL}` in the final PR body.

Review the final PR description for consistent current test counts, clickable evidence links, and honest publication status. Publication and demo completion messages in GitHub, Jira, and OpenHands are authorized for this demo. Verify the real GitHub PR link appears in the conversation and the conversation link appears in the PR. Post the verified PR and conversation links to Jira and mark the validated ticket Done. This demo-scoped authorization does not authorize unrelated outreach. Keep merge pending and leave the fixture's `main` unchanged.

The initial private-repository clone stalled during this rehearsal; the agent recovered through its configured GitHub credentials. Allow setup time and keep the finished example available. Fully unattended URL injection remains a separate automation-runtime improvement.

Use the latest [billing conversation](https://app.replicated.rajistics.com/canvas/conversations/52dbfd1461164828a23d8f486918dfd9?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6), [draft PR #2](https://github.com/rajistics-demo/billing-defect-demo/pull/2), and [KAN-219](https://rajiv-shah.atlassian.net/browse/KAN-219) (**Done**) while Petstore runs. This fresh Opus 4.7 run repaired 11 initial findings, with 19 repository tests and 14 independent checks passing. Two operator-discovered concurrency gaps led to three additional regressions. Lead with the structured PR findings and measured results; use the history to explain the validation/refinement loop.

For future Petstore runs, the repair skill now requires the controller’s `scripts/defect_review/verify_petstore.py <target-repo>` before publication. Its six supplied contract checks include explicit `None` input. Report these supplied checks separately from independently performed operator checks.

The earlier [Petstore rehearsal](https://app.replicated.rajistics.com/canvas/conversations/be232b755ebc4c27901dcd0ca71dbecb?backend=locked-cloud&org=8b24fd08-7dea-431f-aa4d-811b59a302e6) is a fallback: 3 findings repaired, 13 repository tests and 5 independent acceptance checks passed.

## Model routing by label

The trigger does not inspect repository URLs. A KAN Task with `defect-review` selects Sonnet. A KAN Task with `defect-review-complex` selects Opus; that label takes precedence if both are present, so only one automation runs. The repository and scope still come from the ticket description and are checked by the triage skill.
