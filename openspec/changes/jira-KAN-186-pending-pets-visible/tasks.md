# Tasks

## Investigation ✅

- [x] Load sdlc-story skill and understand workflow
- [x] Launch code-explorer sub-agent to investigate catalog implementation
- [x] Review investigation findings and evidence
- [x] Confirm bug location and root cause

## Planning ✅

- [x] Create OpenSpec change folder: `openspec/changes/jira-KAN-186-pending-pets-visible/`
- [x] Write proposal.md with why, source, assumptions, non-goals, impact
- [x] Write specs/catalog/spec.md with requirements and acceptance criteria
- [x] Write design.md with problem analysis and solution
- [x] Write tasks.md (this file)

## Implementation

- [ ] Validate OpenSpec artifacts with validation script
- [ ] Review current catalog.py implementation
- [ ] Fix status filter logic on line 50
- [ ] Add regression test for empty status string

## Validation

- [ ] Run backend unit tests (`pytest app/tests/`)
- [ ] Verify new regression test fails before fix
- [ ] Verify new regression test passes after fix
- [ ] Verify all existing tests continue to pass
- [ ] Run frontend Playwright tests if available

## Delivery

- [ ] Create feature branch
- [ ] Commit OpenSpec artifacts
- [ ] Commit implementation and tests
- [ ] Push branch to GitHub
- [ ] Open draft PR with complete evidence waypoints
- [ ] Add conversation link to PR description
- [ ] Post result comment to Jira issue
- [ ] Add `openhands-review` label to trigger code review automation

## Human Gates

- [ ] **Scope approval**: Human created and approved Jira task
- [ ] **Review approval**: Humans review PR and provide feedback
- [ ] **Merge approval**: Humans merge PR when ready
- [ ] **Deployment approval**: Humans control deployment timing
