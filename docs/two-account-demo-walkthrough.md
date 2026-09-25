# Two-Account SDLC Demo Operator Walkthrough

This is a short operator guide for demonstrating the SDLC Automation Demo with two GitHub identities working in the same shared repository.

## Overview

This walkthrough shows how multiple team members can use OpenHands with the same organization and repository while maintaining separate identities and access levels.

- **Organization**: `rajistics-demo`
- **Repository**: `rajistics-demo/sdlc-automation-github-demo`
- **Presenter (Organization Owner)**: `rajshah4`
- **Team Member**: `rajistics`

## Key Concepts

This demo illustrates three independent access layers:

1. **GitHub Organization Membership** — Whether a user is a member of the `rajistics-demo` organization
2. **Repository Permissions** — Whether a user has Read or Write access to the shared repository
3. **OpenHands Sign-In** — Each person signs in to OpenHands with their own GitHub account

## Sign-In and Repository Access

### For Both Users

Each person:
1. Signs in to OpenHands using their own GitHub account credentials
2. Authorizes the OpenHands GitHub App to access their repositories
3. Ensures the GitHub App authorization includes the `rajistics-demo/sdlc-automation-github-demo` repository

**Critical**: The GitHub App must be authorized for the shared repository. Without this authorization, OpenHands cannot interact with the repository on behalf of that user.

## Read-Only Member Path

A team member with **Read access** (such as `rajistics` if configured as read-only) can:

- View issues, pull requests, and repository contents through OpenHands
- Analyze code and generate reports
- Review changes and provide feedback
- Use OpenHands to understand the codebase

They **cannot**:
- Create branches or push code changes
- Open pull requests
- Add labels or modify issues
- Trigger automations that require repository Write access

This path demonstrates how OpenHands can serve team members who need visibility and analysis capabilities without modification rights.

## Contribution Path

A team member with **Write access** can perform all read-only actions plus:

- Create feature branches
- Commit and push code changes
- Open pull requests for review
- Add labels to trigger OpenHands automations (`openhands-build`, `openhands-review`, `openhands-qa`)
- Collaborate on bug fixes and feature development

**Requirement**: Repository Write permission must be granted through GitHub organization settings or repository collaborator settings.

## What This Demo Does NOT Cover

- Moving personal repositories between accounts or organizations
- Transferring unrelated repositories into `rajistics-demo`
- Changing repository ownership
- Configuring organization-level settings or policies

## Presenter Flow

1. Show that `rajshah4` is signed in to OpenHands with GitHub
2. Demonstrate creating a sparse bug issue in the shared repository
3. Apply the `openhands-build` label to trigger the automation
4. Show the resulting PR with OpenSpec-style artifacts, tests, and implementation
5. (Optional) Show `rajistics` signed in separately, viewing the same PR
6. (Optional) Demonstrate the read-only vs. write access distinction

## Key Takeaways

- Each person maintains their own GitHub identity when using OpenHands
- Organization membership, repository permissions, and OpenHands access are separate concerns
- The GitHub App authorization determines which repositories OpenHands can access for each user
- Read access enables analysis and visibility; Write access enables contribution
- The same automation workflows work regardless of which authorized user triggers them
