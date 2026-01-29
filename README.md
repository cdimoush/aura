# Aura

Agentic scaffolding for codebases. Skills, issue tracking, and voice capture — wired together.

## What is Aura?

Aura wraps your repository with Claude Code skills and beads-based issue tracking to make planning and implementing easier for both agents and humans. Voice memos provide optional hands-free idea capture.

**Key Features:**
- **Beads integration** — dependency-aware issue tracking via `bd` CLI
- **Epic planning** — break visions into phased, dependency-mapped tasks
- **Multi-agent ready** — beads carry context between agents via comments and dependency graphs
- **Voice memo capture** — record, transcribe, and queue ideas via OpenAI Whisper
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
- `.aura/` - Configuration, scripts, and memo directories
- `.claude/skills/` - Slash command skills for Claude Code
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

### 4. Record and Process a Voice Memo

```bash
# Activate the virtual environment
source .aura/.venv/bin/activate

# Record a voice memo (press Ctrl+C to stop recording)
python .aura/scripts/record_memo.py

# The script will:
# 1. Record audio via sox
# 2. Transcribe via OpenAI Whisper
# 3. Generate a title from the transcript
# 4. Save to .aura/memo/queue/<title>/

# In Claude Code session:
/aura.process_memo   # Process all queued memos
```

## Skills Reference

Aura provides 4 focused skills:

| Skill | Description | Example |
|-------|-------------|---------|
| `/aura.process_memo` | Process all voice memos from queue | `/aura.process_memo` |
| `/aura.epic` | Break a vision into an epic with tasks | `/aura.epic "user authentication system"` |
| `/aura.create_beads` | Convert epic tasks to beads tickets | `/aura.create_beads .aura/epics/user-auth.md` |
| `/aura.implement` | Implement beads in dependency order | `/aura.implement .aura/epics/user-auth.md` |

### Context Injection

Aura automatically injects context at session start via Claude Code's hook system. No need to run a prime command - the aura context loads automatically when you start a session.

## Directory Structure

After `aura init`:

```
your-project/
├── .aura/
│   ├── AURA.md               # Context file (auto-injected at session start)
│   ├── .gitignore            # Ignores memo contents, .env, .venv/
│   ├── .venv/                # Virtual environment for scripts
│   ├── memo/
│   │   ├── queue/            # Voice memos waiting to be processed
│   │   ├── processed/        # Successfully processed memos
│   │   └── failed/           # Failed processing attempts
│   ├── epics/                # Epic planning documents
│   └── scripts/
│       ├── record_memo.py    # Record → transcribe → title → queue
│       ├── transcribe.py     # OpenAI Whisper transcription
│       ├── generate_title.py # Intelligent title generation
│       └── requirements.txt  # Script dependencies
├── .beads/                   # Task tracking (if beads available)
└── .claude/
    ├── settings.json         # SessionStart hook configuration
    └── skills/
        ├── aura.process_memo/
        │   └── SKILL.md
        ├── aura.epic/
        │   └── SKILL.md
        ├── aura.create_beads/
        │   └── SKILL.md
        └── aura.implement/
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

### Example 1: Voice Memo to Code

```bash
# Record your idea
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py
# Press Ctrl+C when done speaking
# → Transcribes audio automatically
# → Generates title from content
# → Saves to .aura/memo/queue/<title>/

# In Claude Code session:
/aura.process_memo
# → Reads transcript
# → Acts on your request
# → Moves to .aura/memo/processed/<title>_<timestamp>/
```

### Example 2: Epic Planning

```bash
# Create a structured epic from a vision
/aura.epic "User authentication system with OAuth and MFA"
# → Creates .aura/epics/user-authentication-system.md with phases and tasks

# Convert to trackable tickets
/aura.create_beads .aura/epics/user-authentication-system.md
# → Creates beads tasks with dependencies

# Implement in order
/aura.implement .aura/epics/user-authentication-system.md
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

Each Aura-initialized project is fully self-contained for voice processing.

### Recording a Voice Memo

Use the included script to record, transcribe, and queue memos in one step:
```bash
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py [--max-duration SECONDS]
```

The script:
1. Records audio via sox (press Ctrl+C to stop)
2. Transcribes via OpenAI Whisper
3. Generates a kebab-case title from the transcript
4. Saves to `.aura/memo/queue/<title>/` with `audio.wav` and `transcript.txt`

If transcription fails, audio is preserved in `.aura/memo/failed/`.

### Voice Memo Directory Structure

```
.aura/memo/queue/<title>/
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
# Voice memos go to ~/projects/app-a/.aura/memo/queue/

# Project B
cd ~/projects/app-b
# Voice memos go to ~/projects/app-b/.aura/memo/queue/
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

Aura uses itself for development. The `.aura/` and `.claude/skills/` at the repo root are:

1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

This means changes to skills are immediately testable without running init.

```bash
# Edit a skill
vim .claude/skills/aura.process_memo/SKILL.md

# Test immediately in Claude Code
/aura.process_memo
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
