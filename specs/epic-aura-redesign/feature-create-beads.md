# Feature: create_beads Skill

## Description

Convert an epic's tasks into beads tickets with proper dependencies.

## Behavior

1. Read epic file from `.aura/epics/<name>.md`
2. Parse tasks and dependencies
3. Create beads ticket for each task via `bd create`
4. Set up blockedBy relationships via `bd dep add`
5. Output summary of created tickets

## Skill Structure

```
.claude/skills/aura.create_beads/
└── SKILL.md
```

## Frontmatter

```yaml
---
name: aura.create_beads
description: Convert epic tasks to beads tickets with dependencies
argument-hint: <epic-path>
disable-model-invocation: true
allowed-tools: Bash(bd *), Read
---
```

## Tasks

- [ ] Create `.claude/skills/aura.create_beads/SKILL.md`
- [ ] Parse epic format to extract tasks and dependencies
- [ ] Create beads with `bd create "<task>" --description "<details>"`
- [ ] Track task IDs for dependency setup
- [ ] Set dependencies with `bd dep add`
- [ ] Test with sample epic

## Acceptance Criteria

- `/aura.create_beads .aura/epics/example.md` creates beads
- Dependencies correctly set (bd dep list shows relationships)
- Summary shows task IDs and dependency graph
