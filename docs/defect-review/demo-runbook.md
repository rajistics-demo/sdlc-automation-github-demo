# Jira repository defect review demo

Create a KAN Task with label `defect-review`, a Repository URL, Ref, Mode, and Scope. The agent reviews existing code, records reproducible findings, drafts a repair spec, fixes confirmed defects, and validates the result.

## Verified results

| Demo | Model | Repository tests | Independent acceptance |
| --- | --- | --- | --- |
| Petstore | Sonnet 4.5 | 13 passing | 5 passing |
| Billing | Opus 4.7 for specification and repair; initial triage was Sonnet | 26 passing | 13 passing |

The independent checks caught a concurrent-retry defect in the first billing repair. The agent added regression tests, corrected the transaction logic, and passed the acceptance checks. This evidence is stronger than a passing happy-path suite alone.

## Current wiring

- Simple automation: `SDLC_0 - Jira Simple Defect Review`, ID `91953529-8cf5-4ee8-b42b-04ec5c339867`, model `Bedrock-Claude-Sonnet-4-5-fast`.
- Complex automation: `Jira Defect Review`, ID `6a20e4cd-23f9-4ef6-8f84-a76e58dcf5a1`, model `OpenHands-Opus-4-7` (`openai/claude-opus-4-7`).
- Model routing uses labels, not repository URLs: `defect-review` selects Sonnet; `defect-review-complex` selects Opus and takes precedence if both labels are present. The repository URL remains in the description for agent discovery and allowlist validation.
- KAN-215 completed on Sonnet: three findings repaired, 13 repository tests and five operator acceptance checks pass.
- KAN-216 completed its initial triage on Sonnet before the model preference arrived. It was switched to managed Opus before repairs; the first Opus inference failed with Bedrock 403 (Marketplace access). Rajiv then selected the existing `OpenHands-Opus-4-7` profile through its alternate provider, and the run resumed successfully. Billing now passes 26 repository tests and 13 operator acceptance checks, including a follow-up correction for simultaneous identical payment retries.
- The managed Opus profile is configured through OpenHands; discovery alone does not establish usable model access.
- Host: https://app.replicated.rajistics.com
- Controller: https://github.com/rajistics-demo/sdlc-automation-github-demo/tree/codex/jira-defect-triage
- Skills: `.agents/skills/repo-defect-triage/` and `.agents/skills/repo-defect-repair/`
- Trigger: `jira-direct`, `jira:issue_created`, project KAN, issue type Task, label `defect-review`
- Both fixture repos are private and use Python standard-library code. No packages need installation during the demo.
- Runtime cloning currently provides the controller checkout; agents successfully clone the chosen target through the existing GitHub integration.
- The existing broad KAN Jira-to-PR automation must stay disabled during this demo. Rajiv disabled it before KAN-215 and KAN-216 were created.
- `keep_alive` is true. No archive action is present in the generated automation scripts, and the prompt/skills explicitly forbid archiving conversations. Runtime TTL can still expire a sandbox; preserve evidence locally.

## Simple ticket

Summary: Review Petstore for defects and repair them

Label: `defect-review`

```text
Repository: https://github.com/rajistics-demo/petstore-defect-demo
Ref: main
Mode: review-and-repair
Scope: Review catalog visibility, adoption eligibility, and order totals. Repair all confirmed defects in this scope.
```

Test ticket: https://rajiv-shah.atlassian.net/browse/KAN-215

## Complex ticket

Summary: Review billing service for defects and repair them

Label: `defect-review-complex`

```text
Repository: https://github.com/rajistics-demo/billing-defect-demo
Ref: main
Mode: review-and-repair
Scope: Review authentication, customer isolation, invoice search and pagination, query scaling, and payment correctness under retries and concurrent requests. Repair confirmed defects in this scope.
```

Test ticket: https://rajiv-shah.atlassian.net/browse/KAN-216

## Evidence to show

1. Jira ticket naming repository and review scope without revealing the defects.
2. Triage findings with business impact and local reproduction evidence.
3. Repair spec linking findings to acceptance criteria, written before application changes.
4. Regression tests failing before the fix and passing afterward, with existing tests preserved.
5. Review/QA report and human-reviewable PR draft.

The five-part visual layout Rajiv supplied should be built after successful validation. Keep that work separate from the functional rehearsal.

## Publication and human gates

The current preset saves publication drafts in the sandbox; it does not publish PRs or comments. Exact content and destination must be approved before Jira/GitHub messages are sent. Jira ticket creation for KAN-215 and KAN-216 was explicitly approved. A local `pr-draft.md` is not an opened PR. Rehearsal self-review is not an independent agent review. Merge, deployment, infosec, and pentest remain human gates.

## Repeatability

Fixture `main` stays deliberately flawed. Each run works on a repair branch and must preserve the original existing tests and product contract. Use a new approved Jira Task for a new run. Do not reset or force-push an existing repair branch. Operator acceptance checks stay outside target repositories so the agent must discover defects rather than follow a supplied answer key.

## Bedrock Opus access blocker

The observed 403 names missing `aws-marketplace:ViewSubscriptions` and `aws-marketplace:Subscribe` permissions needed to enable `us.anthropic.claude-opus-4-8`. No IAM policies or Marketplace agreements were changed. See https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html. This blocker remains specific to managed Bedrock Opus 4.8. KAN-216 resumed and was independently validated using the alternate Opus 4.7 profile selected by Rajiv.

The current complex automation uses the existing OpenAI-compatible Opus 4.7 profile selected by Rajiv. This is an alternate configuration path; it does not validate Bedrock Opus 4.8 access through Replicated.
