---
name: aura.epic
description: Break a vision into an epic with ordered tasks and dependencies
argument-hint: <vision description>
disable-model-invocation: true
allowed-tools: Read, Write, Glob
---

# Create Epic

Break down a vision into a structured epic with phased tasks and dependencies.

## Input

The argument is a vision description - what the user wants to achieve.

## Output Location

Write the epic to `.aura/epics/<kebab-case-name>.md`

Generate the name from the vision (max 50 chars, lowercase, hyphens).

## Epic Format

```markdown
# Epic: <Title>

## Overview

<Description of what this epic achieves>

## Tasks

### Phase 1: <Phase Name>

1. [ ] <Task title> - <Brief description>
2. [ ] <Task title> - <Brief description>

### Phase 2: <Phase Name>

3. [ ] <Task title> (depends on 1, 2) - <Brief description>
4. [ ] <Task title> (depends on 3) - <Brief description>

### Phase 3: <Phase Name>

5. [ ] <Task title> (depends on 4) - <Brief description>

## Dependencies

- Task 3 blocked by: 1, 2
- Task 4 blocked by: 3
- Task 5 blocked by: 4

## Success Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>
```

## Steps

1. **Analyze vision** - Understand what needs to be built/changed
2. **Identify phases** - Group work into logical phases (Foundation, Core, Polish, etc.)
3. **Break into tasks** - Each task should be completable in one work session
4. **Map dependencies** - Which tasks must complete before others can start
5. **Write epic file** - Use the format above
6. **Report location** - Tell user where the epic was saved

## Guidelines

- Tasks should be actionable and specific
- Each task should have clear acceptance criteria implied by description
- Dependencies should form a DAG (no cycles)
- Number tasks sequentially across phases for easy dependency reference
- Keep phases to 3-5 tasks each
