# Feature: SoX Recording Script

## Overview

Create `record_memo.py` script that records audio using SoX, immediately transcribes it with chunking support, generates a title, and organizes it in the queue directory.

## User Story

As a developer using Aura, I want to record a voice memo from the terminal so that I can capture ideas without leaving my workflow. The recording should be automatically transcribed and organized so I can process it later.

## Context

The current `aura.record.md` command uses SoX directly via bash commands. We need a unified Python script that:
1. Records audio to WAV
2. Transcribes immediately (reusing existing `transcribe.py`)
3. Generates a title (reusing existing `generate_title.py`)
4. Organizes files in queue structure

This is inspired by Whisper project's voice memo recorder examples.

## Technical Approach

**Script Location**: `.aura/scripts/record_memo.py`

**Dependencies** (add to `requirements.txt`):
- All existing dependencies (openai, pydub, etc.)
- SoX must be installed system-wide (not Python package)

**Script Flow**:
```python
1. Check prerequisites (sox, API key, dependencies)
2. Create temp WAV file for recording
3. Start SoX recording (blocking until Ctrl+C or duration)
4. On completion:
   a. Transcribe audio (call transcribe.py functionality)
   b. Generate title (call generate_title.py functionality)
   c. Create queue subdirectory: .aura/queue/<title>/
   d. Move audio.wav to subdirectory
   e. Write transcript.txt to subdirectory
5. Print success message with location
```

**CLI Interface**:
```bash
# Record until Ctrl+C
python .aura/scripts/record_memo.py

# Record with duration limit (seconds)
python .aura/scripts/record_memo.py --duration 120

# Specify output directory (default: .aura/queue)
python .aura/scripts/record_memo.py --queue-dir /path/to/queue
```

## Implementation Details

### Error Handling

- Check for SoX installation: `sox --version`
- Check for ffmpeg installation: `ffmpeg -version`
- Check for OPENAI_API_KEY environment variable
- Handle transcription failures gracefully (fallback title)
- Handle title generation failures (timestamp fallback)
- Handle title collisions (append -1, -2, etc.)

### SoX Command

```bash
# Basic recording (stop with Ctrl+C)
rec output.wav

# With duration limit
rec output.wav trim 0 120

# With explicit settings (recommended)
rec -r 16000 -c 1 output.wav trim 0 120
```

Settings:
- `-r 16000`: 16kHz sample rate (sufficient for speech)
- `-c 1`: Mono channel (reduces file size)

### Reusing Existing Functions

Import functionality from existing scripts:

```python
# From transcribe.py
from .transcribe import split_audio_into_chunks, transcribe_chunks

# From generate_title.py
from .generate_title import generate_title
```

Actually, scripts are self-contained (no imports from aura package), so use subprocess:

```python
import subprocess

# Transcribe
result = subprocess.run(
    ["python", ".aura/scripts/transcribe.py", audio_path],
    capture_output=True,
    text=True
)
transcript = result.stdout

# Generate title
result = subprocess.run(
    ["python", ".aura/scripts/generate_title.py", "--text", transcript],
    capture_output=True,
    text=True
)
title = result.stdout.strip()
```

### Queue Directory Creation

```python
import os
from pathlib import Path

queue_dir = Path(".aura/queue")
queue_dir.mkdir(parents=True, exist_ok=True)

memo_dir = queue_dir / title
if memo_dir.exists():
    # Handle collision: append counter
    counter = 1
    while (queue_dir / f"{title}-{counter}").exists():
        counter += 1
    memo_dir = queue_dir / f"{title}-{counter}"

memo_dir.mkdir(parents=True, exist_ok=True)
```

## Tasks

- [ ] Create `.aura/scripts/record_memo.py` with CLI argument parsing
- [ ] Implement prerequisite checks (sox, ffmpeg, API key)
- [ ] Implement SoX recording subprocess
- [ ] Integrate transcription via subprocess call
- [ ] Integrate title generation via subprocess call
- [ ] Implement queue directory creation with collision handling
- [ ] Add comprehensive error messages
- [ ] Test on macOS (primary target)
- [ ] Update `.aura/scripts/requirements.txt` if needed
- [ ] Create/update `.aura/scripts/README.md` documenting usage

## Acceptance Criteria

- [ ] Script records audio using SoX on macOS
- [ ] Audio saved as WAV in temp location during recording
- [ ] Ctrl+C stops recording gracefully
- [ ] Optional `--duration` flag limits recording time
- [ ] Transcription happens immediately after recording
- [ ] Title auto-generated from transcript
- [ ] Files organized in `.aura/queue/<title>/` structure
- [ ] `audio.wav` and `transcript.txt` present in subdirectory
- [ ] Handles title collisions with counter suffix
- [ ] Clear error messages for missing prerequisites
- [ ] Script exits with appropriate status codes (0 success, 1 error)
- [ ] Progress messages to stderr, final location to stdout

## Testing Plan

### Manual Testing

1. **Basic Recording**:
   ```bash
   python .aura/scripts/record_memo.py
   # Speak for 10 seconds
   # Press Ctrl+C
   # Verify files in .aura/queue/<title>/
   ```

2. **Duration Limit**:
   ```bash
   python .aura/scripts/record_memo.py --duration 15
   # Speak for 15 seconds
   # Verify stops automatically
   ```

3. **Long Recording** (tests chunking):
   ```bash
   python .aura/scripts/record_memo.py --duration 600
   # Speak for 10 minutes
   # Verify chunks are processed
   ```

4. **Error Cases**:
   - Run without SoX installed → clear error
   - Run without API key → clear error
   - Run with no internet → transcription fails gracefully
   - Generate same title twice → verify `-1` suffix

### Integration Testing

1. Record memo, then run `/aura.process` on it
2. Record memo, then run `/cyborg.process` on it
3. Record from Aura project directory
4. Record from Cyborg project directory (after Phase 4)

## Documentation Updates

- [ ] Update `.claude/commands/aura.record.md` to use new script
- [ ] Add script usage to README.md
- [ ] Document in CLAUDE.md under "Scripts" section
- [ ] Add troubleshooting section for common errors

## Dependencies

- Must complete: [Chore: Queue Directory Structure](./chore-queue-structure.md)
- Reuses: `transcribe.py` (existing)
- Reuses: `generate_title.py` (existing)

## Notes

- macOS only for now (SoX syntax may differ on Linux)
- Consider adding `--no-transcribe` flag to skip transcription (just record)
- Consider adding `--title` flag to override auto-generated title
- Future: Add progress bar for transcription (currently uses stderr messages)
- Future: Support other audio formats (M4A input)
