# Chore: Implement Cross-Project Recording Strategy

## Overview

Implement the chosen strategy (Option A: Copy Script) for recording audio across multiple Aura-initialized projects.

## Context

Based on [Decision: Cross-Project Audio Strategy](./decision-cross-project-audio.md), we're implementing the self-contained approach where each project gets its own copy of recording scripts.

## Prerequisites

- Decision document approved
- Recording script (`record_memo.py`) implemented
- Queue structure defined

## Implementation Tasks

### 1. Update Init Logic

Ensure `src/aura/init.py` copies `record_memo.py` to target projects:

```python
# In get_template_files()

# Already handles .aura/scripts/*.py via glob
# Just verify record_memo.py is included:

template_dir = Path(__file__).parent.parent / ".aura"
for script_file in template_dir.glob("scripts/*.py"):
    src = script_file
    dst = Path(".aura/scripts") / script_file.name
    files.append((src, dst))
```

- [ ] Verify `record_memo.py` is in `.aura/scripts/` at repo root
- [ ] Test `aura init` includes `record_memo.py` in output
- [ ] Test `aura init --dry-run` lists `record_memo.py`

### 2. Update Documentation

#### README.md

Add cross-project recording section:

```markdown
## Recording Across Projects

Voice recording works in any Aura-initialized project:

### Setup (Per-Project)

```bash
cd your-project
aura init

# Create virtual environment for scripts
cd .aura
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r scripts/requirements.txt
cd ..
```

### Recording

```bash
# Activate venv (if not already active)
source .aura/.venv/bin/activate

# Record a memo
python .aura/scripts/record_memo.py

# Or with duration limit
python .aura/scripts/record_memo.py --duration 120
```

Memos are saved to `.aura/queue/` in the current project directory.
```

- [ ] Add to README.md
- [ ] Add troubleshooting section for cross-project issues

#### CLAUDE.md

Add cross-project usage patterns:

```markdown
## Cross-Project Recording

When working across multiple projects (e.g., Aura and Cyborg), each project has its own `.aura/` directory with recording scripts.

**Pattern**:
- Each project's recordings go to that project's `.aura/queue/`
- Processing commands operate on local queue
- Scripts are self-contained (no imports from aura package)

**Example**:
```bash
# Record in Aura
cd ~/apps/aura
python .aura/scripts/record_memo.py
# → ~/apps/aura/.aura/queue/<title>/

# Record in Cyborg
cd ~/apps/aura/incubator/cyborg
python .aura/scripts/record_memo.py
# → ~/apps/aura/incubator/cyborg/.aura/queue/<title>/
```
```

- [ ] Add to CLAUDE.md under relevant section

### 3. Test in Multiple Contexts

Create a comprehensive test plan and execute:

#### Test 1: Aura Repository

```bash
cd ~/apps/aura

# Verify script exists
test -f .aura/scripts/record_memo.py && echo "✓ Script exists"

# Test recording (short duration)
python .aura/scripts/record_memo.py --duration 5
# Speak a test memo

# Verify output
ls -la .aura/queue/
# Should see new subdirectory with audio.wav and transcript.txt
```

- [ ] Execute Test 1
- [ ] Document results

#### Test 2: Cyborg Repository

```bash
cd ~/apps/aura/incubator/cyborg

# Initialize if not already
if [ ! -d .aura ]; then
    aura init
    cp .aura/.env.example .aura/.env
    # Add OPENAI_API_KEY
    cd .aura && uv venv && source .venv/bin/activate
    uv pip install -r scripts/requirements.txt
    cd ..
fi

# Verify script was copied
test -f .aura/scripts/record_memo.py && echo "✓ Script exists"

# Test recording
source .aura/.venv/bin/activate
python .aura/scripts/record_memo.py --duration 5

# Verify output in Cyborg's queue (not Aura's)
ls -la .aura/queue/
test ! -d ~/apps/aura/.aura/queue/$(ls -t .aura/queue/ | head -1) && echo "✓ Not in Aura queue"
```

- [ ] Execute Test 2
- [ ] Verify separation between Aura and Cyborg queues
- [ ] Document results

#### Test 3: External Project

```bash
# Create fresh test project
mkdir -p /tmp/aura-test-project
cd /tmp/aura-test-project

# Initialize
aura init
cp .aura/.env.example .aura/.env
echo "OPENAI_API_KEY=your-key-here" >> .aura/.env

# Setup venv
cd .aura
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements.txt
cd ..

# Test recording
python .aura/scripts/record_memo.py --duration 5

# Verify output
ls -la .aura/queue/
cat .aura/queue/*/transcript.txt

# Cleanup
cd ~
rm -rf /tmp/aura-test-project
```

- [ ] Execute Test 3
- [ ] Verify full workflow in external project
- [ ] Document results

### 4. Update Templates

Ensure all relevant command files reference local script paths:

#### `.claude/commands/aura.record.md`

Update to use the new Python script approach:

```markdown
---
allowed-tools: Bash(python:*), Bash(source:*), Glob, Read
description: Record voice memo to queue
argument-hint: [--duration SECONDS]
---

# Record Voice Memo

Record audio and immediately transcribe to `.aura/queue/`.

## Prerequisites

- SoX installed: `brew install sox` (macOS)
- Virtual environment setup (see README)
- OPENAI_API_KEY in `.aura/.env`

## Instructions

### 1. Activate Virtual Environment

If not already active:
```bash
source .aura/.venv/bin/activate
```

### 2. Start Recording

```bash
# Record until Ctrl+C
python .aura/scripts/record_memo.py

# Or with duration limit (seconds)
python .aura/scripts/record_memo.py --duration 120
```

### 3. Speak Your Memo

The recording will:
- Capture audio to WAV
- Stop on Ctrl+C (or duration limit)
- Transcribe immediately (with chunking for long recordings)
- Generate title from transcript
- Organize in `.aura/queue/<title>/`

### 4. Next Steps

After recording:
- Process with `/aura.process <title>` to create formatted output
- Or use `/aura.act <title>` to act on the memo immediately
```

- [ ] Update `aura.record.md`
- [ ] Test command in Claude Code
- [ ] Verify instructions are clear

### 5. Error Handling

Add robust error messages for common issues:

**In `record_memo.py`**:

```python
# Check for SoX
try:
    result = subprocess.run(["sox", "--version"], capture_output=True)
    if result.returncode != 0:
        raise FileNotFoundError
except FileNotFoundError:
    print("Error: SoX not installed", file=sys.stderr)
    print("Install with:", file=sys.stderr)
    print("  macOS: brew install sox", file=sys.stderr)
    print("  Ubuntu: sudo apt-get install sox libsox-fmt-all", file=sys.stderr)
    sys.exit(1)

# Check for venv (warning only)
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("Warning: Not running in virtual environment", file=sys.stderr)
    print("Recommended: source .aura/.venv/bin/activate", file=sys.stderr)

# Check for API key (already exists)
# Check for dependencies (already exists)
```

- [ ] Add error checks to `record_memo.py`
- [ ] Test each error path
- [ ] Verify messages are helpful

### 6. Performance Considerations

Ensure scripts perform well across projects:

- [ ] Test with long recordings (>10 minutes) - verify chunking works
- [ ] Test with slow network - verify graceful handling
- [ ] Test with multiple queued memos - verify no conflicts
- [ ] Profile script execution time - should be <30s for 5min recording

### 7. Integration with Processing Commands

Verify processing commands work with cross-project recordings:

- [ ] Test `/aura.process` in Aura project
- [ ] Test `/aura.process` in Cyborg project
- [ ] Test `/cyborg.process` in Cyborg project
- [ ] Verify memos don't cross-contaminate between projects

## Acceptance Criteria

- [ ] `aura init` copies `record_memo.py` to target projects
- [ ] Script works when called from any Aura-initialized project
- [ ] Each project's recordings go to that project's `.aura/queue/`
- [ ] No absolute path dependencies
- [ ] Clear error messages for missing prerequisites
- [ ] Documentation complete and accurate
- [ ] All test scenarios pass
- [ ] Performance is acceptable (<30s for 5min recording)

## Testing Checklist

### Functional Tests

- [ ] Record in Aura → output to Aura's queue
- [ ] Record in Cyborg → output to Cyborg's queue
- [ ] Record in external project → output to its queue
- [ ] Duration limit works correctly
- [ ] Ctrl+C stops recording gracefully
- [ ] Title generation works from any project
- [ ] Transcription works with chunking

### Error Tests

- [ ] No SoX installed → clear error
- [ ] No API key → clear error
- [ ] No venv → warning but continues
- [ ] No internet → transcription fails gracefully
- [ ] Invalid duration → helpful error

### Integration Tests

- [ ] Record → Process with `/aura.process`
- [ ] Record → Process with `/cyborg.process`
- [ ] Multiple recordings in sequence
- [ ] Process multiple memos at once

### Edge Cases

- [ ] Very short recording (<5 seconds)
- [ ] Very long recording (>10 minutes, tests chunking)
- [ ] Recording with background noise
- [ ] Recording with silence (no speech)
- [ ] Queue directory already has memo with same title

## Documentation Deliverables

- [ ] README.md updated with cross-project section
- [ ] CLAUDE.md updated with usage patterns
- [ ] `.claude/commands/aura.record.md` updated
- [ ] Troubleshooting guide for common issues
- [ ] Quick start guide for new projects

## Dependencies

- Requires: [Decision: Cross-Project Audio Strategy](./decision-cross-project-audio.md) approved
- Requires: [Feature: SoX Recording Script](./feature-sox-recording-script.md) complete
- Blocks: Distribution and usage of recording across projects

## Notes

- This chore is primarily testing and documentation
- Core implementation is in `record_memo.py` feature
- Focus on validation that the self-contained approach works reliably
- Gather feedback on UX during testing
