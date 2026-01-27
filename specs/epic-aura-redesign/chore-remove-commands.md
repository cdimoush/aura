# Chore: Remove Old Commands

## Description

Delete all deprecated commands from `.claude/commands/`.

## Commands to Remove

| Command | Reason |
|---------|--------|
| `aura.act.md` | Merged into process_memo |
| `aura.transcribe.md` | Merged into process_memo |
| `aura.prime.md` | Replaced by SessionStart hook |
| `aura.record.md` | No Claude-controlled mic access |
| `aura.ticket-dev.md` | Wrong implementation |
| `aura.feature.md` | Use epic for all planning |
| `aura.tickets.md` | Replaced by create_beads |
| `beads.done.md` | Use bd CLI directly |
| `beads.ready.md` | Use bd CLI directly |
| `beads.start.md` | Use bd CLI directly |
| `beads.status.md` | Use bd CLI directly |

## Tasks

- [ ] Delete all files listed above
- [ ] Remove `.claude/commands/` directory if empty
- [ ] Create `.claude/skills/` directory

## Acceptance Criteria

- All 12 old command files deleted
- `.claude/skills/` directory exists for new skills
