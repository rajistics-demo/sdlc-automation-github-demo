# CI in the SDLC Automation Demo

The agent opens a draft PR. GitHub Actions runs **Application tests** alongside
agent code review. Independent QA follows as a separate stage, and a person
decides whether to merge or send the change back.

CI runs on PR creation, reopening, and each new commit, including draft PRs.
It runs `python -m pytest -q app/tests` using Python 3.11. These tests cover
catalog and adoption behavior. The demo-tooling suite in `tests` checks context
reports, prompt packages, and automation helpers; run it during demo maintenance
with `python -m pytest -q`. It is outside the application CI check, so generated
planning documents cannot fail that check through context-report ranking.
A green application check does not establish demo-tooling or browser coverage.
It needs no configured secrets or OpenHands API access. Standard GitHub-hosted
runners are free for this public repository; small JUnit reports expire after
seven days to limit storage. Action commit pins and test dependencies need
occasional updates.

The run summary records the PR head, base, tested merge commit, workflow revision,
and run attempt. A passing run applies to that candidate only. New commits cancel
superseded CI runs and start fresh ones. A cancelled run is not a pass.

CI does not trigger agent review or independent QA. Their existing label-based
handoffs remain in place. After a change, request fresh review and QA through the
existing operator procedure and verify their tested head matches the latest PR
head. An old QA comment or `openhands:done` label is not current validation or
human approval.

The workflow reports a check but does not configure required checks or merge
protection. Those are separate repository policy decisions.

## Validate before presenting

Before a presentation, validate a representative agent-created PR and confirm
the application tests pass for its recorded head. During the demo, show the
application check alongside agent review, then independent QA and human review.
Application test failures remain failures; the workflow does not suppress them.
UI changes still need UI evidence. Human review and merge remain pending.
