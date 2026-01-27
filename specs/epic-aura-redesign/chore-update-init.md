# Chore: Update aura init

## Description

Update `aura init` CLI to deploy new folder structure and hooks.

## Changes to src/aura/init.py

1. Create new folder structure:
   - `.aura/memo/queue/`
   - `.aura/memo/processed/`
   - `.aura/memo/failed/`
   - `.aura/epics/`

2. Copy skills instead of commands:
   - From `.claude/skills/` to target `.claude/skills/`

3. Create/merge `.claude/settings.json`:
   - Add SessionStart hook for aura.md
   - Preserve existing user settings

4. Create `.aura/aura.md` context file

5. Update `.gitignore` additions

## Tasks

- [ ] Update `get_template_files()` for new paths
- [ ] Add settings.json merge logic (don't overwrite)
- [ ] Update folder creation logic
- [ ] Test `aura init` on fresh directory
- [ ] Test `aura init --force` on existing aura directory

## Acceptance Criteria

- `aura init` creates new structure
- Existing settings.json preserved, hook added
- Skills copied to `.claude/skills/`
- Works on fresh and existing directories
