# Tron Verification Test Instructions

This document provides step-by-step instructions to verify your Aura installation works correctly.

## Prerequisites

Before running this test, ensure you have:

- [ ] `uv` installed (`uv --version`)
- [ ] `bd` (beads) installed (`bd --version`)
- [ ] `ffmpeg` installed (`ffmpeg -version`)
- [ ] Aura installed and in PATH (`aura --version`)
- [ ] OpenAI API key (optional, for transcription tests)

## Quick Verification

For a quick check that Aura is working:

```bash
# From a fresh directory
mkdir /tmp/aura-test && cd /tmp/aura-test
git init
aura init
aura check
```

Expected: All files created, `aura check` shows all prerequisites met.

## Full Verification Test

### Step 1: Create Test Directory

```bash
mkdir /tmp/tron-test && cd /tmp/tron-test
git init
```

**Expected**: Empty git repository created.

### Step 2: Initialize Aura

```bash
aura init
```

**Expected output**:
```
Initializing Aura...

  Created .aura/.gitignore
  Created .aura/.env.example
  Created .aura/scripts/requirements.txt
  Created .aura/scripts/generate_title.py
  Created .aura/scripts/transcribe.py
  Created .claude/commands/aura.prime.md
  Created .claude/commands/aura.act.md
  ... (12 command files total)
  Created .beads/ (via bd init)

Aura initialized! (18 created, 0 skipped)
```

### Step 3: Verify Structure

```bash
# Check .aura directory
ls .aura/scripts/
```

**Expected**: `generate_title.py`, `requirements.txt`, `transcribe.py`

```bash
# Check commands
ls .claude/commands/ | wc -l
```

**Expected**: `12` (8 aura commands + 4 beads commands)

```bash
# Check beads
ls .beads/
```

**Expected**: `config.yaml`, `README.md`, and other beads files

### Step 4: Run Aura Check

```bash
aura check
```

**Expected output** (with all prerequisites):
```
Checking prerequisites...

  + Python 3.12+
  + Claude Code
  + OPENAI_API_KEY  (or - if not configured)
  + ffmpeg
  + beads (bd)

All prerequisites met!
```

### Step 5: Configure Environment (Optional)

If testing transcription features:

```bash
cp .aura/.env.example .aura/.env
echo "OPENAI_API_KEY=sk-your-key" >> .aura/.env
```

### Step 6: Test in Claude Code

Open Claude Code in the test directory and run:

```
/aura.prime
```

**Expected**: Project context loaded, shows directory structure and available commands.

```
/beads.status
```

**Expected**: Shows "Beads not initialized" or empty task list (both are correct for new project).

### Step 7: Cleanup

```bash
cd ~
rm -rf /tmp/tron-test
```

## Troubleshooting

### "bd: command not found"

Install beads:
```bash
npm install -g @beads/bd
# or
brew install steveyegge/beads/bd
```

### "aura: command not found"

Ensure you've installed aura and activated the virtual environment:
```bash
cd /path/to/aura
source .venv/bin/activate
```

### "OPENAI_API_KEY not set"

This is expected if you haven't configured a key. Transcription features require:
```bash
cp .aura/.env.example .aura/.env
# Edit .aura/.env and add your key
```

### Commands not appearing in Claude Code

Ensure you're in a directory with `.claude/commands/`:
```bash
ls .claude/commands/*.md
```

## Success Criteria

The verification test passes if:

1. `aura init` creates all 18 files without errors
2. `aura check` shows no missing required prerequisites
3. `.aura/scripts/` contains both Python scripts
4. `.claude/commands/` contains all 12 command files
5. `.beads/` is initialized (if bd available)

## Running Inside tests/tron

You can also verify from the existing tron fixture:

```bash
cd /path/to/aura/tests/tron
rm -rf .aura .claude .beads
aura init --force
aura check
```

This uses the tron project structure as a more realistic test case.
