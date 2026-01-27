# Feature: Epic Skill

## Description

Revised epic skill that creates planning documents in `.aura/epics/`.

## Behavior

1. Accept vision/description as argument
2. Create epic markdown in `.aura/epics/<name>.md`
3. Internally generate task breakdown with dependencies
4. Output epic ready for user review

## Skill Structure

```
.claude/skills/aura.epic/
└── SKILL.md
```

## Frontmatter

```yaml
---
name: aura.epic
description: Break a vision into an epic with ordered tasks and dependencies
argument-hint: <vision description>
disable-model-invocation: true
allowed-tools: Read, Write, Glob
---
```

## Epic Output Format

```markdown
# Epic: <name>

## Overview
<description>

## Tasks

### Phase 1: <name>
1. [ ] <task> - <description>
2. [ ] <task> - <description>

### Phase 2: <name>
3. [ ] <task> (depends on 1, 2) - <description>

## Dependencies
- Task 3 blocked by: 1, 2
- Task 4 blocked by: 3
```

## Tasks

- [ ] Create `.claude/skills/aura.epic/SKILL.md`
- [ ] Define epic markdown format with task dependencies
- [ ] Write to `.aura/epics/<name>.md`
- [ ] Test creating an epic from vision

## Acceptance Criteria

- `/aura.epic "my vision"` creates `.aura/epics/my-vision.md`
- Epic contains phases with ordered tasks
- Dependencies are explicit and parseable
