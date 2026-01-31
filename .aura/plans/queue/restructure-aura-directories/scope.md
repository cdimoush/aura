# Feature: Restructure .aura/ and .claude/ directories, consolidate skills

## Description

Restructure aura's directory layout: move templates into `.claude/`, transform memo into a visions pipeline (accepting text+audio), add queue/processed structure to plans, delete obsolete skills, and update all references.

## Problem Statement

Current layout mixes concerns — templates live in `.aura/` but Claude consumes them. Memo capture is audio-only. Plans have no processing pipeline. Three obsolete skills (epic, create_beads, implement) still exist.

## Solution Statement

New layout with clear pipelines:

```
.claude/
├── templates/        # plan templates (Claude's domain)
│   ├── feature.md
│   └── bug.md
├── skills/
└── settings.json

.aura/
├── scripts/          # recording/processing tools
├── visions/
│   ├── queue/        # text files OR audio+transcript dirs
│   ├── processed/
│   └── failed/
├── plans/
│   ├── queue/        # scoped, awaiting execution
│   └── processed/    # executed/completed
└── AURA.md
```

- **Visions** = input pipeline (replaces memo). Queue items can be a `.txt` file or a directory with `audio.wav` + `transcript.txt`.
- **Plans** = output pipeline. `aura.scope` writes to `plans/queue/`, `aura.execute` moves to `plans/processed/`.
- **Templates** move to `.claude/templates/` since Claude is the consumer.

## Relevant Files

- `src/aura/config.py` - DOT_AURA_FOLDERS and blacklist constants
- `src/aura/init.py` - Template discovery and folder creation logic
- `.aura/.gitignore` - Ignore patterns
- `.aura/AURA.md` - Context file injected at session start
- `.aura/scripts/record_memo.py` - Saves to memo/queue, needs to target visions/queue
- `.aura/scripts/generate_title.py` - Title generation (no path changes)
- `.aura/scripts/transcribe.py` - Transcription (no path changes)
- `.claude/skills/aura.scope/SKILL.md` - Template + output paths
- `.claude/skills/aura.execute/SKILL.md` - Input/output paths
- `.claude/skills/aura.process_memo/SKILL.md` - Becomes aura.process_visions or similar
- `.claude/skills/aura.epic/SKILL.md` - Delete
- `.claude/skills/aura.create_beads/SKILL.md` - Delete
- `.claude/skills/aura.implement/SKILL.md` - Delete
- `CLAUDE.md` - Architecture docs
- `README.md` - User docs

## Implementation Plan

### Phase 1: Delete obsolete skills

Remove aura.epic, aura.create_beads, aura.implement. Also remove `.claude/skills/aura.execute/create-graph.md` and `implement-graph.md` if they contain logic extracted from the deleted skills — that logic should be inlined into aura.execute's SKILL.md or dropped.

### Phase 2: Move and restructure directories

- Move `.aura/templates/` → `.claude/templates/`. Skills currently reference templates as `.aura/templates/` (relative from repo root). After the move, skills will reference `.claude/templates/` — same depth, just different prefix.
- Move `.aura/memo/` → `.aura/visions/`, keeping queue/processed/failed subdirs. The `record_memo.py` script hardcodes `memo/queue` as its output path — needs updating to `visions/queue`.
- Move `.aura/epics/` → `.aura/plans/queue/`. Existing epic dirs (like `scope-and-execute-skills/`, `bug-template/`) become queued plans. Create `.aura/plans/processed/` empty.
- Move `.aura/future_visions/*.md` into `.aura/visions/queue/` as individual text files. These are already plain markdown — they become vision queue items naturally.
- `aura.scope` currently writes to `.aura/epics/<slug>/scope.md`. New path: `.aura/plans/queue/<slug>.md` (flat files, no subdirs per plan).

### Phase 3: Update all references

Key path changes across the codebase:
- **Skills**: All skills reference paths from repo root. `.aura/templates/` → `.claude/templates/`, `.aura/epics/` → `.aura/plans/queue/`, `.aura/memo/` → `.aura/visions/`
- **config.py**: `DOT_AURA_FOLDERS` lists dirs to create (`memo/queue`, `memo/processed`, `memo/failed`, `epics`). Replace with `visions/queue`, `visions/processed`, `visions/failed`, `plans/queue`, `plans/processed`. Blacklist changes from `["memo", "epics"]` to `["visions", "plans"]`.
- **init.py**: `get_template_files()` globs `.aura/**/*` for templates. Templates now live in `.claude/templates/` so init needs a second glob for `.claude/templates/**/*` (separate from skills glob). The `.claude/skills/` glob already exists.
- **process_memo skill → process_visions**: Must handle two queue item formats: (a) bare `.txt` file = text vision, (b) directory with `audio.wav` + `transcript.txt` = audio vision. Processing logic stays the same for audio; text items just need reading directly.

### Phase 4: Verify

- `uv run aura init --dry-run` — confirm new folder structure appears, templates copy from `.claude/templates/`
- Check no references to old paths remain: `grep -r "memo/" .claude/skills/`, `grep -r "epics/" .claude/skills/`, `grep -r ".aura/templates" .claude/skills/`

## Tasks

### Phase 1: Delete obsolete skills

1. [ ] Delete obsolete skill directories - Remove `.claude/skills/aura.epic/`, `.claude/skills/aura.create_beads/`, `.claude/skills/aura.implement/`

### Phase 2: Move and restructure directories

2. [ ] Move templates to .claude/ - Move `.aura/templates/` → `.claude/templates/`
3. [ ] Restructure memo → visions - Rename `.aura/memo/` → `.aura/visions/`, keep queue/processed/failed subdirs
4. [ ] Restructure epics → plans with queue/processed - Move `.aura/epics/` contents → `.aura/plans/queue/`, create `.aura/plans/processed/`
5. [ ] Migrate future_visions → visions/queue (depends on 3) - Move `.aura/future_visions/*.md` into `.aura/visions/queue/` as text files, remove old dir
6. [ ] Update .aura/.gitignore (depends on 2, 3, 4) - Fix ignore patterns for new visions/ and plans/ paths, remove memo/ patterns

### Phase 3: Update references

7. [ ] Update src/aura/config.py (depends on 2, 3, 4) - Fix DOT_AURA_FOLDERS, blacklist to new paths
8. [ ] Update src/aura/init.py (depends on 2, 3, 4) - Fix template discovery (now .claude/templates/), folder creation
9. [ ] Update record_memo.py script (depends on 3) - Change output path from memo/queue to visions/queue
10. [ ] Update aura.scope skill (depends on 2, 4) - Read templates from .claude/templates/, write plans to .aura/plans/queue/
11. [ ] Update aura.execute skill (depends on 4) - Read from .aura/plans/queue/, move completed to .aura/plans/processed/
12. [ ] Update aura.process_memo → aura.process_visions (depends on 3, 5) - Rename skill, update to handle both text and audio queue items
13. [ ] Update AURA.md, CLAUDE.md, README.md (depends on 2, 3, 4) - Fix all path references and architecture docs

### Phase 4: Verify

14. [ ] Verify init dry-run works (depends on 7, 8) - Run `uv run aura init --dry-run` and check output

## Dependencies

- Task 5 blocked by: 3
- Task 6 blocked by: 2, 3, 4
- Tasks 7-8 blocked by: 2, 3, 4
- Task 9 blocked by: 3
- Task 10 blocked by: 2, 4
- Task 11 blocked by: 4
- Task 12 blocked by: 3, 5
- Task 13 blocked by: 2, 3, 4
- Task 14 blocked by: 7, 8

## Testing Strategy

- `uv run aura init --dry-run` should show new directory structure
- All skill files should reference correct paths
- `.gitignore` patterns should match new paths
- Visions queue should accept both text files and audio dirs

## Acceptance Criteria

- [ ] No aura.epic, aura.create_beads, or aura.implement skill dirs exist
- [ ] Templates live in `.claude/templates/`
- [ ] `.aura/visions/` has queue/processed/failed with .gitkeep files
- [ ] `.aura/plans/` has queue/processed with .gitkeep files
- [ ] `.aura/memo/` and `.aura/future_visions/` no longer exist
- [ ] `uv run aura init --dry-run` succeeds
- [ ] record_memo.py targets visions/queue/
