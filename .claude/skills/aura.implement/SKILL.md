---
name: aura.implement
description: Implement beads from an epic in dependency order
argument-hint: <epic-path or bead-id>
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Implement Beads

Work through beads tickets from an epic, respecting dependency order.

## Input

Either:
- Path to an epic file: `.aura/epics/my-feature.md`
- A specific bead ID: `aura-abc`

## Mode: Epic Path

When given an epic path:

1. **Read epic** - Understand the overall goal and context
2. **Find ready beads** - Run `bd ready` to find unblocked tasks
3. **Implement loop** - For each ready bead:
   - Show bead details: `bd show <id>`
   - Implement the work described
   - Close when done: `bd close <id> --reason "<what was done>" --suggest-next`
4. **Repeat** - Check for newly unblocked tasks after each close
5. **Complete** - When no more ready tasks, epic is done

## Mode: Single Bead

When given a bead ID:

1. **Show bead** - Run `bd show <id>` for details
2. **Implement** - Do the work described
3. **Close** - Run `bd close <id> --reason "<what was done>" --suggest-next`

## Implementation Guidelines

- Read relevant files before making changes
- Follow existing code patterns in the codebase
- Make minimal, focused changes
- Test changes when possible
- Commit after completing each bead (if user requests)

## Status Updates

- Mark bead in_progress when starting: `bd update <id> --status in_progress`
- Close with summary of what was done: `bd close <id> --reason "<summary>"`
- Use `--suggest-next` to see what's unblocked

## Error Handling

- If implementation fails, do not close the bead
- Report what failed and what was attempted
- User can retry or modify the approach
