# Aura Context

Aura is a voice-driven development workflow. Voice memos are transcribed and turned into code.

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/aura.process_memo` | Process all voice memos from queue |
| `/aura.epic <vision>` | Break a vision into an epic with tasks |
| `/aura.create_beads <epic>` | Convert epic tasks to beads tickets |
| `/aura.implement <epic or bead>` | Implement beads in dependency order |

## Folder Structure

```
.aura/
├── memo/
│   ├── queue/       # Pending voice memos
│   ├── processed/   # Successfully processed
│   └── failed/      # Failed processing
├── epics/           # Epic planning documents
├── scripts/         # Python scripts for transcription
└── aura.md          # This file (injected at session start)
```

## Workflow

1. **Record** - User records voice memo (outside Claude)
2. **Queue** - Audio placed in `.aura/memo/queue/<title>/audio.wav`
3. **Process** - `/aura.process_memo` transcribes and acts on requests
4. **Plan** - `/aura.epic` for larger features needing breakdown
5. **Track** - `/aura.create_beads` converts epic to trackable tickets
6. **Implement** - `/aura.implement` works through tickets in order

## Context Injection

This file is automatically injected via Claude Code's SessionStart hook.
No need to run `/prime` - context is loaded automatically.
