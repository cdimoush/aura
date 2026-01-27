# Feature: process_memo Skill

## Description

Single skill that processes all voice memos in queue sequentially.

## Behavior

1. List all directories in `.aura/memo/queue/`
2. For each memo:
   - Run transcribe script if no transcript exists
   - Read transcript
   - Act on the request
   - On success: move to `.aura/memo/processed/<title>_<timestamp>/`
   - On failure: move to `.aura/memo/failed/<title>_<timestamp>/`
3. Continue to next memo (no confirmation between)

## Skill Structure

```
.claude/skills/aura.process_memo/
├── SKILL.md
└── scripts/
    └── (reference .aura/scripts/)
```

## Frontmatter

```yaml
---
name: aura.process_memo
description: Process all voice memos from queue - transcribe and act on requests
disable-model-invocation: true
allowed-tools: Bash(python *), Read, Write, Glob, Grep, Edit
---
```

## Tasks

- [ ] Create `.claude/skills/aura.process_memo/SKILL.md`
- [ ] Use `!`command`` syntax for deterministic queue listing
- [ ] Handle empty queue gracefully
- [ ] Implement move-on-success and move-on-failure
- [ ] Test with sample memo

## Acceptance Criteria

- `/aura.process_memo` processes all queued memos
- Successful memos land in processed/
- Failed memos land in failed/
- Works with empty queue (no error)
