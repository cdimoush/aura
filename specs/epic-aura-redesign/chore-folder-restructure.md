# Chore: Folder Restructure

## Description

Reorganize `.aura/` directory to new structure.

## Tasks

- [ ] Create `.aura/memo/queue/`
- [ ] Create `.aura/memo/processed/`
- [ ] Create `.aura/memo/failed/`
- [ ] Create `.aura/epics/`
- [ ] Move existing `.aura/queue/*` to `.aura/memo/queue/`
- [ ] Move existing `.aura/output/*` to `.aura/memo/processed/`
- [ ] Remove old `.aura/queue/` and `.aura/output/` directories
- [ ] Update `.gitignore` to ignore new paths

## Acceptance Criteria

- New folder structure exists
- Old folders removed
- Gitignore updated for `.aura/memo/` and `.aura/epics/`
