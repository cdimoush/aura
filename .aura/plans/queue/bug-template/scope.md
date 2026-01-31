# Feature: Bug Report Template

## Description

Add a `bug.md` template to `.aura/templates/` that the scope skill can select when the user's vision is about fixing a bug rather than building a feature. The template structures bug investigation and resolution with sections appropriate for debugging workflows.

## Problem Statement

Currently only a `feature.md` template exists. When a user runs `/aura.scope` for a bug fix, the feature template's sections (Problem/Solution Statements, Implementation Plan phases) don't fit well. Bug work needs different structure: reproduction steps, root cause analysis, and fix verification.

## Solution Statement

Create `.aura/templates/bug.md` with bug-appropriate sections. The scope skill already discovers templates via `ls .aura/templates/` and selects the best fit, so no skill changes are needed — just adding the template file.

## Relevant Files

- `.aura/templates/feature.md` - Existing template to use as structural reference
- `.aura/templates/bug.md` - New file to create
- `src/aura/init.py` - Auto-discovers and copies `.aura/templates/` files (no changes needed)
- `.claude/skills/aura.scope/SKILL.md` - Already handles template discovery (no changes needed)

## Implementation Plan

### Phase 1: Create Template

Create the bug template with sections for bug description, reproduction steps, expected vs actual behavior, root cause analysis, relevant files, fix tasks, and verification criteria.

## Tasks

### Phase 1: Create Template

1. [ ] Create `.aura/templates/bug.md` - Bug report template with sections: Bug Description, Reproduction Steps, Expected vs Actual Behavior, Root Cause Analysis, Relevant Files, Tasks (using standard epic task format), Dependencies, Testing Strategy, and Acceptance Criteria

### Phase 2: Verify

2. [ ] Verify bug template works with scope skill (depends on 1) - Confirm the template is discovered by `ls .aura/templates/`, can be read and populated by the scope skill, and the task list uses the standard format compatible with `create_beads` parsing

## Dependencies

- Task 2 blocked by: 1

## Testing Strategy

- Run `ls .aura/templates/` and confirm `bug.md` appears
- Verify the task list section uses the `N. [ ] <Title> (depends on X) - <Description>` format
- Optionally run `/aura.scope fix login timeout bug` and confirm it selects `bug.md`

## Acceptance Criteria

- [ ] `.aura/templates/bug.md` exists with bug-appropriate sections
- [ ] Template task format is compatible with `create_beads` parsing
- [ ] `aura init` will auto-copy the template (no init.py changes needed)
