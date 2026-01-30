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

1. **Show bead** - Run `bd show <id>` for details and comments (prior agents leave context here)
2. **Read epic** - Follow the epic path in the bead description to understand overall context
3. **Implement** - Do the work described
4. **Close** - Run `bd close <id> --reason "<what was done>" --suggest-next`

## Implementation Guidelines

- A bead's work may be research, code, verification, or documentation — read the description, do what it asks, close with what you delivered
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

- If implementation fails, leave a comment (`bd comments add <id> "<what failed>"`) and do not close the bead
- If a downstream bead (verification) fails, reopen the upstream bead and leave a comment explaining what needs fixing
