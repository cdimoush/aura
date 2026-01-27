# Aura - Claude Code Agent Guide

This document provides context for Claude Code agents working on the Aura project itself (not repos wrapped by Aura).

## Project Overview

Aura is an agentic workflow layer that scaffolds repositories with Claude Code skills for voice-driven development. It enables a workflow where developers speak ideas into voice memos, which are transcribed and turned into structured plans and implementations.

**Core Philosophy**: Remove friction between ideas and code. Voice is faster than typing.

## Architecture

### Project Structure

```
aura/
├── .aura/                   # Working copy (dogfood) AND template source
│   ├── .gitignore           # Ignores memo/*, .env
│   ├── .env.example         # Example environment file
│   ├── aura.md              # Context file (injected at session start)
│   ├── memo/
│   │   ├── queue/           # Pending memos
│   │   ├── processed/       # Successfully processed
│   │   └── failed/          # Failed processing
│   ├── epics/               # Epic planning documents
│   └── scripts/
│       ├── transcribe.py    # OpenAI Whisper transcription
│       ├── generate_title.py # Intelligent title generation
│       └── requirements.txt  # Script dependencies
├── .claude/
│   ├── settings.json        # SessionStart hook configuration
│   └── skills/              # Working copy (dogfood) AND template source
│       ├── aura.process_memo/
│       │   └── SKILL.md
│       ├── aura.epic/
│       │   └── SKILL.md
│       ├── aura.create_beads/
│       │   └── SKILL.md
│       └── aura.implement/
│           └── SKILL.md
├── src/aura/
│   ├── __init__.py          # Package init
│   ├── cli.py               # Click CLI entry point
│   ├── config.py            # Configuration constants
│   └── init.py              # Scaffolding logic
├── pyproject.toml           # Package metadata
└── README.md                # User documentation
```

**Key insight**: The `.aura/` and `.claude/skills/` at repo root serve dual purposes:
1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

### Core Components

#### CLI (`src/aura/cli.py`)

Entry point for `aura init` and `aura check` commands.

#### Init Logic (`src/aura/init.py`)

Handles template file discovery, copying, and settings.json merging:

```python
def get_template_files() -> list[tuple[Path, Path]]:
    """Returns (src, dst) pairs for all template files."""

def merge_settings_json(target_path, force=False) -> dict:
    """Merge SessionStart hook into existing settings.json."""

def init_aura(force=False, dry_run=False) -> dict:
    """Initialize aura in target directory."""
```

The init process:
1. Creates folder structure: `.aura/memo/queue/`, `memo/processed/`, `memo/failed/`, `epics/`
2. Copies `.aura/` files (scripts, aura.md, .gitignore, etc.)
3. Copies `.claude/skills/` subdirectories
4. Merges SessionStart hook into `.claude/settings.json`
5. Runs `bd init` if beads CLI available

#### Skills (Dogfooding)

**Skill directory** (`.claude/skills/` at repo root):
- Source for `.claude/skills/` in target repositories
- Each skill is a directory containing `SKILL.md`
- Skills are invoked via `/skill-name` in Claude Code
- Also used directly when developing aura

**Available Skills**:
| Skill | Purpose |
|-------|---------|
| `aura.process_memo` | Process all voice memos from queue |
| `aura.epic` | Break a vision into an epic with tasks |
| `aura.create_beads` | Convert epic tasks to beads tickets |
| `aura.implement` | Implement beads in dependency order |

## Voice Memo Queue Structure

Voice memos are staged in a queue directory before processing.

### Directory Layout

```
.aura/
├── memo/
│   ├── queue/                   # Pending memos (git-ignored)
│   │   └── <title>/
│   │       ├── audio.wav        # Original recording
│   │       └── transcript.txt   # Raw transcript (created if missing)
│   ├── processed/               # Successfully processed (git-ignored)
│   │   └── <title>_<timestamp>/
│   │       ├── audio.wav
│   │       └── transcript.txt
│   └── failed/                  # Failed processing (git-ignored)
│       └── <title>_<timestamp>/
│           ├── audio.wav
│           └── transcript.txt
└── epics/                       # Epic planning documents
    └── <epic-name>.md
```

### Title Format

Titles are generated from transcript content by `generate_title.py`:
- **kebab-case**: lowercase with hyphens (e.g., `bug-fix-authentication`)
- **Max 50 characters**: truncated if necessary
- **Filesystem-safe**: alphanumeric and hyphens only
- **Fallback**: `memo-YYYYMMDD-HHMMSS` if generation fails

### Skill Anatomy

Claude Code skills have this structure:

```
.claude/skills/<skill-name>/
└── SKILL.md
```

With frontmatter:

```markdown
---
name: aura.process_memo
description: Process all voice memos from queue
disable-model-invocation: true
allowed-tools: Bash(python *), Read, Write, Glob
---

# Skill Title

Instructions for the agent...

## Steps

1. Do this
2. Then this
```

The frontmatter controls:
- `name`: Skill identifier (used for invocation)
- `description`: Shows in skill listing
- `disable-model-invocation`: Prevents auto-invocation
- `allowed-tools`: Which tools the skill can use

## Development Workflow

### Dogfooding

Aura is developed using aura. The skills and scripts at the repo root are the same ones copied to target repos.

**Benefits**:
- Changes are immediately testable
- No template drift between development and distribution
- Aura's own repo demonstrates expected structure
- If it works for us, it works for users

**Workflow**:
1. Edit `.claude/skills/aura.process_memo/SKILL.md`
2. Run `/aura.process_memo` to test immediately
3. Fix issues, repeat

### Testing Changes

1. Make changes to skills in `.claude/skills/` or scripts in `.aura/scripts/`
2. Test immediately - changes are live for aura development

### Adding a New Skill

1. Create skill directory at repo root:
   ```bash
   mkdir -p .claude/skills/aura.newskill
   touch .claude/skills/aura.newskill/SKILL.md
   ```

2. Add frontmatter and instructions:
   ```markdown
   ---
   name: aura.newskill
   description: What this skill does
   disable-model-invocation: true
   allowed-tools: Read, Glob
   ---

   # Skill Title

   Instructions...
   ```

3. Test immediately with `/aura.newskill` in Claude Code

4. Update README.md skill reference

### Adding a New Script

1. Create script at repo root:
   ```bash
   touch .aura/scripts/newscript.py
   ```

2. Ensure script is self-contained:
   - No imports from `aura` or `whisper` packages
   - All dependencies in `requirements.txt`
   - Works from any working directory
   - Outputs to stdout, errors to stderr

3. Update `.aura/scripts/requirements.txt` if new dependencies needed

4. Update relevant skills to call the script

5. Test directly: `python .aura/scripts/newscript.py`

### Running Tests

```bash
# Test scripts directly from aura root
python .aura/scripts/generate_title.py --text "test memo"

# Test transcription (requires audio file and API key)
OPENAI_API_KEY=sk-xxx python .aura/scripts/transcribe.py test.m4a

# Test init dry-run
uv run aura init --dry-run
```

## Key Files

| File | Purpose |
|------|---------|
| `src/aura/cli.py` | CLI commands (`init`, `check`) |
| `src/aura/init.py` | Scaffolding logic |
| `src/aura/config.py` | Configuration constants |
| `.claude/skills/*/SKILL.md` | Skill sources (dogfood + template) |
| `.claude/settings.json` | SessionStart hook configuration |
| `.aura/aura.md` | Context file (injected at session start) |
| `.aura/scripts/*.py` | Portable Python scripts (dogfood + template) |
| `README.md` | User documentation |
| `CLAUDE.md` | This file - agent guide |

## Common Tasks

### Modify a Skill

1. Edit the skill at repo root: `.claude/skills/<skill>/SKILL.md`
2. Test immediately with `/skill` in Claude Code

### Change Script Behavior

1. Edit the script at repo root: `.aura/scripts/<script>.py`
2. Test directly: `python .aura/scripts/<script>.py`

### Add Template File

1. Create file in `.aura/` or `.claude/skills/` at repo root
2. The init logic auto-discovers files via glob patterns
3. No code changes needed in init.py (for most files)
4. Test immediately (it's a working copy!)

### Debug Init Issues

Check dry-run output:
```bash
uv run aura init --dry-run
```

This shows all files that would be created without creating them.

## Design Decisions

### Why Skills Instead of Commands?

Skills provide a cleaner structure:
- Each skill is a directory (can contain supporting files)
- Better organization for complex skills
- Matches Claude Code's newer skills system
- Supports `disable-model-invocation` for explicit control

### Why SessionStart Hook?

Automatic context injection via hook:
- No need for users to run `/prime` manually
- Context loads at every session start
- Configured in `.claude/settings.json`
- Merges with existing user settings

### Why Self-Contained Scripts?

Scripts in `.aura/scripts/` don't import from aura or whisper packages because:
1. Target repos don't have aura installed as a package
2. Simpler dependency management (just requirements.txt)
3. Users can modify scripts without understanding the full package

### Why Copy vs Symlink?

Templates are copied (not symlinked) because:
1. Target repos shouldn't depend on aura installation location
2. Users can customize their copies
3. Works across different machines/environments

### Why Beads Integration?

Beads provides dependency-aware task management that pairs well with epic/feature planning. It's optional - aura works without it, but the workflow is enhanced with it.

## Troubleshooting

### Templates Not Copying

Check that files exist at repo root:
```bash
ls -la .aura/scripts/
ls -la .claude/skills/
```

### Init Fails Silently

Run with verbose output:
```bash
uv run aura init --dry-run
```

### Script Dependencies Missing

Ensure requirements.txt is complete:
```bash
cat .aura/scripts/requirements.txt
```

### SessionStart Hook Not Working

Check settings.json has the hook:
```bash
cat .claude/settings.json
```

Should contain:
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

---

*Last updated: 2026-01-27*
