# Aura

Agentic scaffolding for codebases. Skills, issue tracking, and vision capture — wired together.

## What is Aura?

Aura wraps your repository with Claude Code skills and beads-based issue tracking to make planning and implementing easier for both agents and humans. Visions (text or audio) provide hands-free idea capture.

**Key Features:**
- **Beads integration** — dependency-aware issue tracking via `bd` CLI
- **Scope planning** — break visions into phased, dependency-mapped tasks
- **Multi-agent ready** — beads carry context between agents via comments and dependency graphs
- **Vision capture** — queue text ideas or record audio via OpenAI Whisper
- **Automatic context injection** — SessionStart hook loads project context + `bd prime`

## Installation

### Prerequisites

- **uv**: Python package manager - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **git**: Version control
- **Claude Code**: [Install Claude Code](https://claude.ai/claude-code)
- **beads**: Issue tracking CLI (required) - [GitHub](https://github.com/steveyegge/beads)
  ```bash
  npm install -g @beads/bd
  ```
- **sox**: Audio recording
  - macOS: `brew install sox`
  - Ubuntu: `sudo apt-get install sox`
- **ffmpeg**: Audio processing (for transcription)
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`

### Install Aura

```bash
git clone https://github.com/cdimoush/aura.git
cd aura
uv venv && source .venv/bin/activate
uv pip install -e . -r .aura/scripts/requirements.txt
aura --version  # Verify installation
```

## Quick Start

### 1. Initialize Aura in Your Project

```bash
cd your-project
aura init
```

This creates:
- `.aura/` - Configuration, scripts, visions and plans directories
- `.claude/skills/` - Slash command skills for Claude Code
- `.claude/templates/` - Plan templates (feature, bug)
- `.claude/settings.json` - SessionStart hook for automatic context
- `.beads/` - Task tracking (if beads CLI available)

### 2. Set Up Environment

```bash
# Copy the example env file
cp .aura/.env.example .aura/.env

# Add your OpenAI API key (edit the file with your key)
echo "OPENAI_API_KEY=sk-your-key" >> .aura/.env

# Create a virtual environment for aura scripts
uv venv .aura/.venv
source .aura/.venv/bin/activate

# Install script dependencies
uv pip install -r .aura/scripts/requirements.txt
```

### 3. Verify Setup

```bash
# Check aura installation
aura check

# Start Claude Code - context auto-loads via SessionStart hook
```

### 4. Capture and Process Visions

```bash
# Option A: Text vision — just drop a file
echo "Add user authentication with OAuth" > .aura/visions/queue/add-auth.txt

# Option B: Audio vision — record and transcribe
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py
# Press Ctrl+C to stop recording

# In Claude Code session:
/aura.process_visions   # Process all queued visions
```

## Skills Reference

Aura provides 3 focused skills:

| Skill | Description | Example |
|-------|-------------|---------|
| `/aura.process_visions` | Process all visions from queue (text + audio) | `/aura.process_visions` |
| `/aura.scope` | Research codebase and produce a scope file | `/aura.scope "user authentication system"` |
| `/aura.execute` | Create beads from scope and implement autonomously | `/aura.execute .aura/plans/queue/user-auth/scope.md` |

### Context Injection

Aura automatically injects context at session start via Claude Code's hook system. No need to run a prime command - the aura context loads automatically when you start a session.

## Directory Structure

After `aura init`:

```
your-project/
├── .aura/
│   ├── AURA.md               # Context file (auto-injected at session start)
│   ├── .gitignore            # Ignores visions contents, .env, .venv/
│   ├── .venv/                # Virtual environment for scripts
│   ├── visions/
│   │   ├── queue/            # Text files or audio dirs waiting to be processed
│   │   ├── processed/        # Successfully processed visions
│   │   └── failed/           # Failed processing attempts
│   ├── plans/
│   │   ├── queue/            # Scoped plans awaiting execution
│   │   └── processed/        # Completed plans
│   └── scripts/
│       ├── record_memo.py    # Record → transcribe → title → queue
│       ├── transcribe.py     # OpenAI Whisper transcription
│       ├── generate_title.py # Intelligent title generation
│       └── requirements.txt  # Script dependencies
├── .beads/                   # Task tracking (if beads available)
└── .claude/
    ├── settings.json         # SessionStart hook configuration
    ├── templates/            # Plan templates (feature.md, bug.md)
    └── skills/
        ├── aura.process_visions/
        │   └── SKILL.md
        ├── aura.scope/
        │   └── SKILL.md
        └── aura.execute/
            └── SKILL.md
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | API key for transcription and title generation |
| `AURA_TRANSCRIPTION_MODEL` | No | Override transcription model (default: gpt-4o-mini-transcribe) |
| `AURA_TITLE_MODEL` | No | Override title model (default: gpt-4o-mini) |

## Workflow Examples

### Example 1: Vision to Code

```bash
# Option A: Text vision
echo "Add rate limiting to the API" > .aura/visions/queue/rate-limiting.txt

# Option B: Audio vision
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py
# Press Ctrl+C when done speaking

# In Claude Code session:
/aura.process_visions
# → Reads vision content
# → Acts on your request
# → Moves to .aura/visions/processed/
```

### Example 2: Scope and Execute

```bash
# Create a structured scope from a vision
/aura.scope "User authentication system with OAuth and MFA"
# → Creates .aura/plans/queue/user-authentication-system/scope.md

# Execute the scope (creates beads and implements)
/aura.execute .aura/plans/queue/user-authentication-system/scope.md
# → Creates beads tasks with dependencies
# → Works through tasks respecting dependencies
```

### Example 3: Using Beads Directly

```bash
# Check ready tasks
bd ready

# Start working on a task
bd update <id> --status in_progress

# Complete a task
bd close <id> --reason "Implemented feature"
```

## Cross-Project Recording

Each Aura-initialized project is fully self-contained for vision processing.

### Recording an Audio Vision

Use the included script to record, transcribe, and queue visions in one step:
```bash
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py [--max-duration SECONDS]
```

The script:
1. Records audio via sox (press Ctrl+C to stop)
2. Transcribes via OpenAI Whisper
3. Generates a kebab-case title from the transcript
4. Saves to `.aura/visions/queue/<title>/` with `audio.wav` and `transcript.txt`

If transcription fails, audio is preserved in `.aura/visions/failed/`.

### Vision Directory Structure

```
.aura/visions/queue/
├── <title>.txt          # Text vision (plain file)
└── <title>/             # Audio vision
    ├── audio.wav        # Recorded audio
    └── transcript.txt   # Whisper transcript
```

### Per-Project Setup

After `aura init`, set up Python dependencies for that project:
```bash
cd your-project

# Create virtual environment
uv venv .aura/.venv
source .aura/.venv/bin/activate

# Install dependencies
uv pip install -r .aura/scripts/requirements.txt

# Configure API key
cp .aura/.env.example .aura/.env
# Edit .aura/.env and add your OPENAI_API_KEY
```

### Multiple Projects

Each project operates independently:
```bash
# Project A
cd ~/projects/app-a
# Visions go to ~/projects/app-a/.aura/visions/queue/

# Project B
cd ~/projects/app-b
# Visions go to ~/projects/app-b/.aura/visions/queue/
```

To update skills after an Aura upgrade:
```bash
cd your-project
aura init --force
```

## Verification

After installation, verify everything works:

```bash
# Quick verification
mkdir /tmp/aura-test && cd /tmp/aura-test
git init
aura init
aura check
```

## Troubleshooting

### "OPENAI_API_KEY not set"

Create a `.env` file in the `.aura/` directory:
```bash
echo "OPENAI_API_KEY=sk-your-key" > .aura/.env
```

### "pydub/openai not installed"

Install script dependencies in a virtual environment:
```bash
uv venv .aura/.venv
source .aura/.venv/bin/activate
uv pip install -r .aura/scripts/requirements.txt
```

### Skills not appearing in Claude Code

Ensure you're in a directory with `.claude/skills/`:
```bash
ls .claude/skills/*/SKILL.md
```

If missing, run `aura init`.

## Development

Aura uses itself for development. The `.aura/`, `.claude/skills/`, and `.claude/templates/` at the repo root are:

1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

This means changes to skills are immediately testable without running init.

```bash
# Edit a skill
vim .claude/skills/aura.process_visions/SKILL.md

# Test immediately in Claude Code
/aura.process_visions
```

## Design Decisions

### Why Beads?

Beads provides dependency-aware issue tracking that agents can navigate autonomously. An agent runs `bd ready`, picks a bead, reads comments left by prior agents, does the work, and closes it — unlocking downstream beads. No orchestrator needed. When verification fails, `bd reopen` sends work back upstream with a comment explaining what broke.

### Why SessionStart Hook?

Automatic context injection means no manual priming. Every Claude Code session starts with project context (`.aura/AURA.md`) and beads workflow guidance (`bd prime`) loaded automatically. Configured in `.claude/settings.json` and merged with existing user settings by `aura init`.

## Future Work

- **`aura check` enhancements**: More detailed validation and diagnostics
- **Plugin system**: Custom skills and workflows
- **`uv tool install`**: Global installation support
- **`aura update`**: Selective skill updates without full re-init

## Contributing

1. Fork the repository
2. Create a feature branch
3. Edit skills in `.claude/skills/` or scripts in `.aura/scripts/`
4. Test locally - changes are live for development
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

*Built with Claude Code*
