---
allowed-tools: Bash(mkdir:*), Read, Write, Glob
description: Plan and implement a feature
argument-hint: <feature description>
---

# Feature Planning

Create a plan in `specs/<feature-name>.md` to implement the feature.

## Instructions

- Research the codebase before planning. Start with `README.md` and `CLAUDE.md` if they exist.
- Create the plan as `specs/<feature-name>.md`.
- Follow existing patterns in the codebase.
- Keep solutions simple and focused.

## Relevant Files

- `README.md` - Project overview
- `CLAUDE.md` - Agent instructions
- `specs/` - Example specs if they exist

## Plan Format

```md
# Feature: <feature name>

## Feature Description
<describe the feature, its purpose, and value to users>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem
<what problem does this feature solve?>

## Solution
<how will this feature solve the problem?>

## Relevant Files

### Files to Modify
<list existing files to change and why>

### New Files
<list new files to create and their purpose>

## Step by Step Tasks
<list tasks as h3 headers with bullet points. Order matters - start with foundational changes, then specific implementation. Last step should run Validation Commands.>

## Acceptance Criteria
<list specific criteria that must be met for the feature to be complete>

## Validation Commands
<list commands to verify the feature works>

## Notes
<optional: additional context, future considerations, or dependencies>
```

## Feature

$ARGUMENTS
