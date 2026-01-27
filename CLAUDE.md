# Aura - Claude Code Agent Guide

This document provides context for Claude Code agents working on the Aura project itself (not repos wrapped by Aura).

## Project Overview

Aura is an agentic workflow layer that scaffolds repositories with Claude Code slash commands for voice-driven development. It enables a workflow where developers speak ideas into voice memos, which are transcribed and turned into structured plans and implementations.

**Core Philosophy**: Remove friction between ideas and code. Voice is faster than typing.

## Architecture

### Project Structure

```
aura/
├── .aura/                   # Working copy (dogfood) AND template source
│   ├── .gitignore           # Ignores queue/, output/, .env
│   ├── .env.example         # Example environment file
│   └── scripts/
│       ├── transcribe.py    # OpenAI Whisper transcription
│       ├── generate_title.py # Intelligent title generation
│       └── requirements.txt  # Script dependencies
├── .claude/
│   └── commands/            # Working copy (dogfood) AND template source
│       ├── aura.*.md        # Aura slash commands
│       └── beads.*.md       # Beads slash commands
├── src/aura/
│   ├── __init__.py          # Package init
│   ├── cli.py               # Click CLI entry point
│   └── init.py              # Scaffolding logic (copies from root .aura/ and .claude/)
├── pyproject.toml           # Package metadata
└── README.md                # User documentation
```

**Key insight**: The `.aura/` and `.claude/commands/` at repo root serve dual purposes:
1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

### Core Components

#### CLI (`src/aura/cli.py`)

Entry point for `aura init` and `aura check` commands:

```python
@click.group()
def cli(): ...

@cli.command()
@click.option("--force", is_flag=True)
@click.option("--dry-run", is_flag=True)
def init(force, dry_run): ...

@cli.command()
def check(): ...
```

#### Init Logic (`src/aura/init.py`)

Handles template file discovery and copying:

```python
def get_template_files() -> list[tuple[Path, Path]]:
    """Returns (src, dst) pairs for all template files."""

def init_aura(force=False, dry_run=False, no_beads=False) -> dict:
    """Copies templates to current directory, returns results."""
```

The init process:
1. Globs all files in aura root `.aura/**/*` → copies to target `.aura/` (excludes queue/, output/)
2. Globs all files in aura root `.claude/commands/*.md` → copies to target `.claude/commands/`
3. Runs `bd init` if beads CLI available and not skipped

#### Templates (Dogfooding)

**Aura directory** (`.aura/` at repo root):
- Source for `.aura/` in target repositories
- Contains scripts and configuration
- Scripts are self-contained (no aura/whisper imports)
- Also used directly when developing aura

**Claude commands** (`.claude/commands/` at repo root):
- Source for `.claude/commands/` in target repositories
- Markdown files with frontmatter for Claude Code
- Define slash commands available in Claude Code sessions
- Also used directly when developing aura

## Voice Memo Queue Structure

Voice memos are staged in a queue directory before processing. Each memo is self-contained in its own subdirectory.

### Directory Layout

```
.aura/
├── queue/                       # Pending memos (git-ignored)
│   ├── <title>/
│   │   ├── audio.wav            # Original recording (WAV/PCM)
│   │   └── transcript.txt       # Raw Whisper transcript (UTF-8)
│   └── <another-title>/
│       ├── audio.wav
│       └── transcript.txt
└── output/                      # Processed results (git-ignored)
```

### Title Format

Titles are generated from transcript content by `generate_title.py`:
- **kebab-case**: lowercase with hyphens (e.g., `bug-fix-authentication`)
- **Max 50 characters**: truncated if necessary
- **Filesystem-safe**: alphanumeric and hyphens only
- **Fallback**: `memo-YYYYMMDD-HHMMSS` if generation fails

### File Contents

| File | Format | Purpose |
|------|--------|---------|
| `audio.wav` | WAV (PCM) | Archival, re-transcription |
| `transcript.txt` | Plain text (UTF-8) | Input for processing commands |

### Template Anatomy

Claude Code command templates have this structure:

```markdown
---
allowed-tools: Bash(python:*), Read, Write
description: Short description for command listing
argument-hint: <required> [optional]
---

# Command Name

Instructions for the agent...

## Steps

1. Do this
2. Then this
```

The frontmatter controls:
- `allowed-tools`: Which tools the command can use
- `description`: Shows in `/help` listing
- `argument-hint`: Shows expected arguments

## Development Workflow

### Dogfooding

Aura is developed using aura. The commands and scripts at the repo root are the same ones copied to target repos.

**Benefits**:
- Changes are immediately testable
- No template drift between development and distribution
- Aura's own repo demonstrates expected structure
- If it works for us, it works for users

**Workflow**:
1. Edit `.claude/commands/aura.act.md`
2. Run `/aura.act` to test immediately
3. Fix issues, repeat

### Testing Changes

1. Make changes to commands in `.claude/commands/` or scripts in `.aura/scripts/`
2. Test immediately - changes are live for aura development

### Adding a New Command

1. Create command at repo root:
   ```bash
   # Naming convention: aura.<name>.md or beads.<name>.md
   touch .claude/commands/aura.newcommand.md
   ```

2. Add frontmatter and instructions:
   ```markdown
   ---
   allowed-tools: Read, Glob
   description: What this command does
   argument-hint: <required-arg>
   ---

   # Command Title

   Instructions...
   ```

3. Test immediately with `/aura.newcommand` in Claude Code

4. Update README.md command reference

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

4. Update relevant command templates to call the script

5. Test directly: `python .aura/scripts/newscript.py`

### Running Tests

```bash
# Test scripts directly from aura root
python .aura/scripts/generate_title.py --text "test memo"

# Test transcription (requires audio file and API key)
OPENAI_API_KEY=sk-xxx python .aura/scripts/transcribe.py test.m4a
```

## Key Files

| File | Purpose |
|------|---------|
| `src/aura/cli.py` | CLI commands (`init`, `check`) |
| `src/aura/init.py` | Scaffolding logic |
| `.claude/commands/*.md` | Slash command sources (dogfood + template) |
| `.aura/scripts/*.py` | Portable Python scripts (dogfood + template) |
| `README.md` | User documentation |
| `CLAUDE.md` | This file - agent guide |

## Common Tasks

### Modify a Slash Command

1. Edit the command at repo root: `.claude/commands/<command>.md`
2. Test immediately with `/command` in Claude Code

### Change Script Behavior

1. Edit the script at repo root: `.aura/scripts/<script>.py`
2. Test directly: `python .aura/scripts/<script>.py`

### Add Template File

1. Create file in `.aura/` or `.claude/commands/` at repo root
2. The init logic auto-discovers files via glob patterns
3. No code changes needed in init.py
4. Test immediately (it's a working copy!)

### Debug Init Issues

Check dry-run output:
```bash
uv run aura init --dry-run
```

This shows all files that would be created without creating them.

## Design Decisions

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

### Cross-Project Recording

Scripts are distributed via `aura init` to enable self-contained recording in any project.

**Design Decision**: Each project gets its own copy of recording scripts rather than using a global Aura installation. This matches Aura's template approach where all files are copied to target repos.

**Rationale**:
1. **Self-contained**: Projects work without external Aura dependencies
2. **Portable**: Move/copy project without path issues
3. **Consistent**: Same distribution pattern as all other templates
4. **Customizable**: Users can modify scripts per-project if needed

**How Scripts Are Distributed**:
- `aura init` copies `.aura/scripts/*.py` to target project
- Each project has its own `.aura/.venv/` for Python dependencies
- SoX is the only system-wide dependency (for audio recording)
- Recordings go to that project's `.aura/queue/`

**Update Strategy**:
- Run `aura init --force` to re-sync scripts from Aura
- Future: `aura update` command for selective script updates

**Trade-off**: Script duplication across projects is acceptable because:
- Scripts are small and change infrequently
- Users can manually sync when needed
- Independence outweighs the minor storage cost

### Why Beads Integration?

Beads provides dependency-aware task management that pairs well with epic/feature planning. It's optional - aura works without it, but the workflow is enhanced with it.

## Brain Note Format

Brain notes are knowledge artifacts created from voice memos. They use single markdown files with YAML frontmatter in a flat directory structure.

### Location and Structure

```
brain/
└── <title>.md
```

### Required Frontmatter Fields

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Generated title for the note | `Bug Fix Authentication Issue` |
| `created` | ISO 8601 timestamp | `2026-01-22T14:30:00Z` |
| `tags` | Auto-generated and manual tags | `[bug-fix, authentication, voice-memo]` |
| `source` | Origin of the note | `voice-memo` |

### Example Brain Note

```markdown
---
title: Bug Fix Authentication Issue
created: 2026-01-22T14:30:00Z
tags: [bug-fix, authentication, security, voice-memo, 2026-01]
source: voice-memo
audio: .aura/output/bug-fix-authentication/audio.wav
---

# Bug Fix Authentication Issue

<processed content from transcript>

## Original Transcript

<raw transcript for reference>
```

### Auto-Tagging Strategy

When creating brain notes from voice memos, tags are auto-generated from multiple sources:

1. **From Intent**: Research intent adds `#research`, code intent adds `#code`, summary intent adds `#summary`
2. **From Content**: Technical terms (OAuth, API, React), action verbs (refactor, implement, fix), domain concepts (authentication, frontend, database)
3. **Temporal Tags**: Timestamp-based tags like `#2026-01` for monthly grouping
4. **Source Tag**: All voice memos get `#voice-memo`

### Design Rationale

Single file with frontmatter was chosen because:
- Simplest to implement and maintain
- Standard markdown format with wide tool support
- Portable (one file = one note)
- Easy to grep/search by tag or content
- Git-friendly and human-readable

## Future Work

- `aura check` command to validate setup
- `.aura/config.md` for project-specific configuration
- Plugin system for custom commands
- `uv tool install` support for global installation
- Multi-agent tool support (Cursor, Copilot, etc.)

## Troubleshooting

### Templates Not Copying

Check that files exist at repo root:
```bash
ls -la .aura/scripts/
ls -la .claude/commands/
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

---

*Last updated: 2026-01-22*
