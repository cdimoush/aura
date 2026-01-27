# Epic: Aura Redesign

## Epic Overview

Redesign aura's architecture to leverage Claude Code's skills and hooks system. This consolidates 12 scattered commands into 5 focused skills, introduces automatic context injection via SessionStart hooks, and reorganizes the `.aura/` folder structure for clarity.

The end state: a cleaner, more maintainable aura that removes friction from voice-driven development. Users get automatic context loading, a simplified skill set, and clear separation between memo processing and planning workflows.

This work is self-bootstrapping - we're using aura to plan aura's own redesign.

## Specs in This Epic

### Phase 1: Foundation
- [ ] [Chore: Folder Restructure](./chore-folder-restructure.md) - Reorganize .aura/ directory structure
- [ ] [Chore: Context Hook](./chore-context-hook.md) - Implement SessionStart hook for aura.md injection

### Phase 2: Skill Migration
- [ ] [Chore: Remove Old Commands](./chore-remove-commands.md) - Delete deprecated commands
- [ ] [Feature: process_memo Skill](./feature-process-memo.md) - New unified memo processing skill
- [ ] [Feature: Epic Skill](./feature-epic-skill.md) - Revised epic planning skill

### Phase 3: Planning Flow
- [ ] [Feature: create_beads Skill](./feature-create-beads.md) - Convert epics to beads tickets
- [ ] [Feature: implement Skill](./feature-implement.md) - Implement beads in dependency order

### Phase 4: Polish
- [ ] [Chore: Update aura init](./chore-update-init.md) - Update init to deploy new structure
- [ ] [Chore: Cleanup](./chore-cleanup.md) - Remove old files, update docs

## Execution Order

### Phase 1: Foundation
**Goal**: Establish new folder structure and hook-based context injection.

Execute in order:
1. [Chore: Folder Restructure](./chore-folder-restructure.md) - Must exist before skills reference new paths
2. [Chore: Context Hook](./chore-context-hook.md) - Hook setup depends on aura.md location

**Success Criteria**:
- `.aura/memo/queue/`, `.aura/memo/processed/`, `.aura/memo/failed/` exist
- `.aura/epics/` exists
- `.aura/aura.md` exists with core instructions
- SessionStart hook in settings.json injects aura.md

---

### Phase 2: Skill Migration
**Goal**: Replace old commands with new skills format.

Execute in order:
1. [Chore: Remove Old Commands](./chore-remove-commands.md) - Clean slate before adding new
2. [Feature: process_memo Skill](./feature-process-memo.md) - Core voice workflow
3. [Feature: Epic Skill](./feature-epic-skill.md) - Planning entry point

**Success Criteria**:
- Old `.claude/commands/` directory removed
- `.claude/skills/aura.process_memo/SKILL.md` works
- `.claude/skills/aura.epic/SKILL.md` creates epics in `.aura/epics/`

---

### Phase 3: Planning Flow
**Goal**: Complete the epic → beads → implement pipeline.

Execute in order:
1. [Feature: create_beads Skill](./feature-create-beads.md) - Depends on epic skill format
2. [Feature: implement Skill](./feature-implement.md) - Depends on beads existing

**Success Criteria**:
- `/aura.create_beads .aura/epics/example.md` creates beads with dependencies
- `/aura.implement .aura/epics/example.md` works through beads in order

---

### Phase 4: Polish
**Goal**: Update tooling and clean up.

Execute in order:
1. [Chore: Update aura init](./chore-update-init.md) - Deploy new structure to target repos
2. [Chore: Cleanup](./chore-cleanup.md) - Final housekeeping

**Success Criteria**:
- `aura init` creates new folder structure
- `aura init` adds SessionStart hook to settings.json
- Old files removed, CLAUDE.md updated
- `.scratch/` files archived or deleted

---

## Path Dependencies Diagram

```
Phase 1: Foundation
    |-- Folder Restructure
    +-- Context Hook (depends on folder)
    |
Phase 2: Skill Migration
    |-- Remove Old Commands
    +-- process_memo Skill
    +-- Epic Skill
    |
Phase 3: Planning Flow
    |-- create_beads Skill (depends on epic)
    +-- implement Skill (depends on create_beads)
    |
Phase 4: Polish
    |-- Update aura init
    +-- Cleanup

Critical Path: Folder → Hook → Remove → process_memo → Epic → create_beads → implement → init → cleanup
```

## Success Metrics

- [ ] 12 commands reduced to 5 skills
- [ ] SessionStart hook auto-injects context (no manual /prime)
- [ ] `/aura.process_memo` handles full queue without user intervention
- [ ] Epic → beads → implement flow works end-to-end
- [ ] `aura init` deploys new structure cleanly

## Future Enhancements

Ideas that came up during planning but are out of scope:

1. `aura.tasks` as user-invocable skill (currently internal only)
2. Sub-agent for autonomous ticket implementation (ticket-dev revival)
3. Cyborg integration (brain notes from memos)
4. Plugin packaging for aura distribution
