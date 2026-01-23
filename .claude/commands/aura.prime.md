---
allowed-tools: Bash(ls:*), Bash(bd:*), Read, Glob
description: Load project context
---

# Prime Agent with Context

Load project context to prepare for work.

## Usage

```
/aura.prime
```

## Instructions

### 1. Read Project Structure

```bash
ls -la
```

Identify key directories and files.

### 2. Read Key Files

Read these files if they exist:
- `README.md` - Project overview
- `CLAUDE.md` - Agent instructions
- `.aura/config.md` - Aura configuration (if exists)

Summarize key information from each.

### 3. Check Beads Status (if initialized)

```bash
if [ -d ".beads" ]; then
    bd list --status in_progress
fi
```

Note any active tasks.

### 4. Report Summary

Output:

```
Project: [Name from README]
[Brief description]

Key Directories:
- src/ - [purpose]
- tests/ - [purpose]
- specs/ - [purpose]

Active Work:
  [task-id]: [Title]
  (or "No active tasks")

Available Aura Commands:
  /aura.record     - Record voice memo
  /aura.act        - Transcribe and act on audio
  /aura.epic       - Create epic plan
  /aura.feature    - Plan a feature
  /aura.tickets    - Convert epic to beads tasks
  /aura.implement  - Implement from ticket
  /aura.ticket-dev - Spawn autonomous agent for ticket
  /beads.status    - Show task overview
  /beads.ready     - Show available tasks
  /beads.start     - Start a task
  /beads.done      - Complete a task

Ready to help! What would you like to work on?
```

## Notes

- Run this at the start of a session to get oriented
- Provides context without modifying anything
- Use before diving into specific tasks
