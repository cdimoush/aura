# Feature: implement Skill

## Description

Implement beads tickets from an epic in dependency order.

## Behavior

1. Read epic to understand context
2. Query beads for ready tasks (`bd ready`)
3. For each ready task:
   - Read task details
   - Implement the work
   - Mark complete with `bd close`
4. Repeat until all epic tasks done

## Skill Structure

```
.claude/skills/aura.implement/
└── SKILL.md
```

## Frontmatter

```yaml
---
name: aura.implement
description: Implement beads from an epic in dependency order
argument-hint: <epic-path or bead-id>
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---
```

## Tasks

- [ ] Create `.claude/skills/aura.implement/SKILL.md`
- [ ] Accept epic path or individual bead ID
- [ ] Use `bd ready` to find unblocked tasks
- [ ] Implement each task (full coding capability)
- [ ] Close completed tasks with `bd close`
- [ ] Test with sample bead

## Acceptance Criteria

- `/aura.implement .aura/epics/example.md` works through tasks
- Respects dependency order (blocked tasks not started)
- Tasks marked complete after implementation
