# Aura

Agentic workflow layer for codebases. Voice-driven development from idea to implementation.

## What is Aura?

Aura scaffolds your repository with Claude Code slash commands that enable a voice-first development workflow:

```
Voice Memo → Transcription → Planning → Tickets → Implementation
```

Instead of writing code manually, you speak your ideas into voice memos. Aura transcribes them, creates structured plans, generates actionable tickets, and helps implement them step by step.

**Key Features:**
- Voice memo transcription via OpenAI Whisper API
- Intelligent title generation for organized output
- Epic and feature planning with structured specs
- Beads integration for dependency-aware task management
- Self-contained scripts that work in any repository

## Installation

### Prerequisites

- **Claude Code**: [Install Claude Code](https://claude.ai/claude-code)
- **Python 3.12+**: Required for transcription scripts
- **ffmpeg**: Required by pydub for audio processing
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`
- **sox** (optional): For recording from CLI
  - macOS: `brew install sox`
  - Ubuntu: `sudo apt-get install sox libsox-fmt-all`
- **beads** (optional): For task management ([beads CLI](https://github.com/anthropics/beads))

### Option 1: Git Clone (Development)

```bash
# Clone the repository
git clone https://github.com/youruser/aura.git
cd aura

# Create and activate a virtual environment
uv venv
source .venv/bin/activate

# Install aura in development mode
uv pip install -e .

# Install script dependencies
uv pip install -r .aura/scripts/requirements.txt
```

### Option 2: UV Tool Install (Coming Soon)

```bash
uv tool install aura
```

## Quick Start

### 1. Initialize Aura in Your Project

```bash
cd your-project
aura init
```

This creates:
- `.aura/` - Configuration and scripts
- `.claude/commands/` - Slash commands for Claude Code
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

# List available commands in Claude Code
# (In Claude Code session)
/aura.prime
```

### 4. Record and Process a Voice Memo

```bash
# In Claude Code session:
/aura.record           # Start recording
# ... speak your idea ...
# Press Ctrl+C to stop

/aura.act .aura/queue/memo_*.wav   # Process the recording
```

## Commands Reference

### Voice Commands (aura.*)

| Command | Description | Example |
|---------|-------------|---------|
| `/aura.record` | Record voice memo from microphone | `/aura.record 60` (60s max) |
| `/aura.transcribe` | Transcribe audio file to text | `/aura.transcribe audio.m4a` |
| `/aura.act` | Full pipeline: transcribe + act | `/aura.act .aura/queue/memo.wav` |

### Planning Commands (aura.*)

| Command | Description | Example |
|---------|-------------|---------|
| `/aura.epic` | Create epic document with phases | `/aura.epic user-auth-system` |
| `/aura.feature` | Plan a feature with spec | `/aura.feature add-dark-mode` |
| `/aura.tickets` | Convert epic to beads tasks | `/aura.tickets specs/epic-auth/` |
| `/aura.implement` | Implement from ticket or spec | `/aura.implement abc-123` |
| `/aura.prime` | Load project context | `/aura.prime` |

### Task Commands (beads.*)

| Command | Description | Example |
|---------|-------------|---------|
| `/beads.status` | Project task overview | `/beads.status` |
| `/beads.ready` | Show available tasks | `/beads.ready` |
| `/beads.start` | Start working on task | `/beads.start abc-123` |
| `/beads.done` | Mark task complete | `/beads.done abc-123` |

## Directory Structure

After `aura init`:

```
your-project/
├── .aura/
│   ├── config.md              # Aura configuration (future)
│   ├── .gitignore             # Ignores queue/, output/, .env, .venv/
│   ├── .venv/                 # Virtual environment for scripts
│   ├── queue/                 # Audio files waiting to be processed
│   ├── output/                # Processed memo outputs
│   └── scripts/
│       ├── transcribe.py      # OpenAI Whisper transcription
│       ├── generate_title.py  # Intelligent title generation
│       └── requirements.txt   # Script dependencies
├── .beads/                    # Task tracking (if beads available)
├── .claude/
│   └── commands/
│       ├── aura.act.md
│       ├── aura.epic.md
│       ├── aura.feature.md
│       ├── aura.implement.md
│       ├── aura.prime.md
│       ├── aura.record.md
│       ├── aura.tickets.md
│       ├── aura.transcribe.md
│       ├── beads.done.md
│       ├── beads.ready.md
│       ├── beads.start.md
│       └── beads.status.md
└── specs/                     # Created by planning commands
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | API key for transcription and title generation |
| `AURA_TRANSCRIPTION_MODEL` | No | Override transcription model (default: gpt-4o-mini-transcribe) |
| `AURA_TITLE_MODEL` | No | Override title model (default: gpt-4o-mini) |

### .aura/config.md (Future)

Configuration file for project-specific settings. Not yet implemented.

## Workflow Examples

### Example 1: Feature from Voice Memo

```bash
# Record your idea
/aura.record
# "I want to add a dark mode toggle to the settings page..."

# Process the recording
/aura.act .aura/queue/memo_20260118_143022.wav
# → Creates .aura/output/dark-mode-toggle_2026-01-18_14-30-22/
# → README.md with transcription and deliverables

# Create a formal plan
/aura.feature "Add dark mode toggle based on voice memo"
# → Creates specs/dark-mode-toggle.md

# Convert to tasks
/aura.tickets specs/dark-mode-toggle.md
# → Creates beads tasks with dependencies

# Start implementation
/beads.ready
/aura.implement abc-123
```

### Example 2: Epic Planning

```bash
# Create high-level epic
/aura.epic "User authentication system with OAuth and MFA"
# → Creates specs/epic-user-auth/README.md with phases

# Convert to tasks
/aura.tickets specs/epic-user-auth
# → Creates beads tasks for each spec

# Work through tasks
/beads.ready
/aura.implement first-task-id
```

## Testing

The `tests/tron/` directory contains a test fixture that demonstrates aura initialization.

```bash
cd tests/tron
aura init --force
ls -la .aura/scripts/
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

### "sox/rec command not found"

Install sox for recording:
- macOS: `brew install sox`
- Ubuntu: `sudo apt-get install sox libsox-fmt-all`

### Commands not appearing in Claude Code

Ensure you're in a directory with `.claude/commands/`:
```bash
ls .claude/commands/*.md
```

If missing, run `aura init`.

## Development

Aura uses itself for development. The `.aura/` and `.claude/commands/` at the repo root are:

1. **Working copies** - Used when developing aura with Claude Code
2. **Template sources** - Copied to target repos by `aura init`

This means changes to commands are immediately testable without running init.

```bash
# Edit a command
vim .claude/commands/aura.act.md

# Test immediately in Claude Code
/aura.act test.wav

# Verify it works for users too
cd tests/tron && aura init --force
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Edit commands in `.claude/commands/` or scripts in `.aura/scripts/`
4. Test locally - changes are live for development
5. Verify with `aura init --force` in `tests/tron/`
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

*Built with Claude Code*
