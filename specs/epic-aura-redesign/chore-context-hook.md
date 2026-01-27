# Chore: Context Hook

## Description

Create `aura.md` context file and SessionStart hook for automatic injection.

## Tasks

- [ ] Create `.aura/aura.md` with core aura instructions
- [ ] Add SessionStart hook to `.claude/settings.json`
- [ ] Test hook injects context on session start
- [ ] Document hook in aura.md itself

## Hook Configuration

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "cat \"$CLAUDE_PROJECT_DIR\"/.aura/aura.md 2>/dev/null || true"
      }]
    }]
  }
}
```

## Acceptance Criteria

- `.aura/aura.md` exists with skill reference and workflow guidance
- Hook registered in settings.json
- Starting new session shows aura context loaded
