---
allowed-tools: Bash(mkdir:*), Read, Write, Glob
description: Break a vision into ordered specs with dependencies
argument-hint: <epic description or vision-doc.md>
---

# Epic Planning

Create an epic document in `specs/epic-*/README.md` that breaks a vision into ordered specs.

## Instructions

- If a vision document is provided, read it first to understand the strategic context.
- If no vision document is provided, create a focused epic for the given scope.
- Break the scope into ordered feature and chore specs.
- Define execution order with explicit dependencies between specs.
- Include user testing breakpoints to validate assumptions before proceeding.
- Create the document as `specs/epic-<name>/README.md`.

## Relevant Files

- `README.md` - Project overview
- `CLAUDE.md` - Project-specific agent instructions
- `specs/` - Example epic structures if they exist

## Epic Format

```md
# Epic: <epic name>

## Epic Overview

<2-3 paragraphs describing the epic's purpose, scope, and expected outcome>

## Specs in This Epic

### Phase 1: <phase name>
- [ ] [Chore: <name>](./<filename>.md) - <brief description>
- [ ] [Feature: <name>](./<filename>.md) - <brief description>

### Phase 2: <phase name>
- [ ] [Feature: <name>](./<filename>.md) - <brief description>

<add more phases as needed>

## Execution Order

### Phase 1: <phase name>
**Goal**: <what this phase achieves>

Execute in order:
1. [Chore/Feature: <name>](./<filename>.md) - <why this is first>
2. [Chore/Feature: <name>](./<filename>.md) - <why this follows>

**Success Criteria**:
<bullet points defining what "done" looks like>

---

### Phase 2: <phase name>
**Goal**: <what this phase achieves>

<same structure as Phase 1>

---

## Path Dependencies Diagram

```
Phase 1
    |
Phase 2
    |-- Spec A (must exist first)
    +-- Spec B (depends on A)
    |
Phase 3

Critical Path: <list the must-have sequence>
```

## Success Metrics

- [ ] <measurable outcome 1>
- [ ] <measurable outcome 2>
- [ ] <measurable outcome 3>

## Future Enhancements

Ideas that came up during planning but are out of scope:

1. <future work item>
2. <future work item>
```

## Creating Individual Specs

After the epic README is complete, create individual spec files for each item:

- For features: Use `/aura.feature`
- For chores: Create `chore-<name>.md` with tasks and acceptance criteria

Place all spec files in the `specs/epic-<name>/` directory alongside the README.

## Epic

$ARGUMENTS
