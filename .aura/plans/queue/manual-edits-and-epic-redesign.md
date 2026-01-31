# Epic: Manual Edits and Epic Redesign

## Overview

Two-phase developer-driven effort. Phase 1 (nica2): manually refine all markdown/skill files. Phase 2 (nica3): redesign the epic skill into a unified workflow with configuration options.

## Tasks

### Phase 1: Manual Markdown Edits (branch: nica2)

1. [x] Review and edit `.aura/aura.md`
2. [x] Review and edit `.claude/skills/aura.process_memo/SKILL.md`
3. [x] Review and edit `.claude/skills/aura.epic/SKILL.md`
4. [x] Review and edit `.claude/skills/aura.create_beads/SKILL.md`
5. [x] Review and edit `.claude/skills/aura.implement/SKILL.md`
6. [ ] Review and edit `CLAUDE.md`
7. [ ] Review and edit `README.md`
8. [ ] Commit nica2 as first-pass baseline

### Phase 2: Epic Skill Redesign (branch: nica3)

9. [ ] Design AskUserQuestion step at the start of epic flow
10. [ ] Design research phase
11. [ ] Design review/approval phase
12. [ ] Design implementation plan output
13. [ ] Design config: epic as planning-only mode
14. [ ] Design config: epic as planning + implementation mode
15. [ ] Combine epic, create_beads, and implement into unified flow
16. [ ] Decide what gets kept as separate skills vs merged
17. [ ] Update skill frontmatter and allowed-tools
18. [ ] Test the new unified flow end-to-end
19. [ ] Update documentation to reflect new workflow

## Dependencies

- Tasks 9-19 blocked by: 8 (nica2 must be finalized first)

## Success Criteria

- [ ] All markdown files in nica2 reflect exactly what the developer wants
- [ ] nica3 epic skill supports both planning-only and planning+implementation configs
- [ ] Unified flow includes user questions, research, review, and implementation phases
