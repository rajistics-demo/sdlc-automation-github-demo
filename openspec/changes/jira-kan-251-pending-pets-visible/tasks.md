# Tasks: Fix Pending Pets Visibility

## Implementation Tasks

- [x] Investigate issue and analyze code
- [x] Create OpenSpec change artifacts
- [ ] Add regression test for backend default search
- [ ] Add explanatory comments to filtering logic
- [ ] Run backend tests to verify behavior
- [ ] Run Playwright UI test if available
- [ ] Create draft pull request
- [ ] Add openhands-review label for code review handoff
- [ ] Post completion comment to Jira issue

## Validation Tasks

- [ ] Confirm default search excludes Nova (pet-103)
- [ ] Confirm species="dog" filter excludes Nova
- [ ] Confirm searching for "nova" returns empty result
- [ ] Confirm adoption of pending pet is rejected
- [ ] Confirm Playwright UI test passes

## Documentation Tasks

- [ ] Document availability filtering in code comments
- [ ] Update PR description with evidence waypoints
- [ ] Link OpenHands conversation in PR and Jira

## Human Approval Gates

- [ ] Scope confirmation from requester
- [ ] Code review approval
- [ ] Merge approval
- [ ] Deployment approval
