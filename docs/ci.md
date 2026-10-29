# CI in the SDLC Automation Demo

The agent opens a draft PR. GitHub Actions runs **Python tests** alongside
agent code review. Independent QA follows as a separate stage, and a person
decides whether to merge or send the change back.

CI runs on PR creation, reopening, and each new commit, including draft PRs.
It runs `python -m pytest -q` across `app/tests` and `tests` using Python 3.11.
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

On an agent-created demo PR, retain a behavioral test that fails on the original
code and show the red CI run. Push the fix to the same PR and show the new green
run. Confirm the full suite passed and the recorded head matches the PR, then
verify fresh agent review and independent QA for that head. UI changes still
need UI evidence. Human review and merge remain pending.
