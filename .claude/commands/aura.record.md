---
allowed-tools: Bash(python:*), Bash(rec:*), Bash(ls:*), Bash(mkdir:*), Read, Glob
description: Record voice memo to queue
argument-hint: [--duration SECONDS]
---

# Record Voice Memo

Record audio from your microphone, automatically transcribe it, and save to `.aura/queue/` with a generated title.

## Prerequisites

1. **SoX** for audio recording:
   - macOS: `brew install sox`
   - Ubuntu: `sudo apt-get install sox libsox-fmt-all`

2. **ffmpeg** for audio processing:
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt-get install ffmpeg`

3. **Python dependencies** in a virtual environment:
   ```bash
   cd .aura/scripts
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **OpenAI API key** set in `.aura/.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

## Instructions

1. Run the recording script:
   ```bash
   # Default: record until Ctrl+C
   python .aura/scripts/record_memo.py

   # With duration limit (in seconds):
   python .aura/scripts/record_memo.py --duration 120
   ```

2. The script will:
   - Record audio from your microphone
   - Transcribe the audio using OpenAI Whisper
   - Generate a descriptive title
   - Save to `.aura/queue/<title>/` with `audio.wav` and `transcript.txt`

3. After recording, the memo is ready for processing with `/aura.act`.

## Output Structure

Each memo is saved as a directory:
```
.aura/queue/
└── add-error-handling-to-login/
    ├── audio.wav
    └── transcript.txt
```

## Tips

- **Stop early**: Press Ctrl+C to stop recording before the duration limit
- **Custom duration**: Use `--duration 60` for a 60-second max
- **Custom queue dir**: Use `--queue-dir path/to/dir` to override default location
- **Batch process**: Record multiple memos, then process all with `/aura.act` (no arguments)

## Error Handling

If prerequisites are missing, the script will show specific installation instructions.

If recording fails, check:
- Microphone permissions (macOS: System Settings > Privacy & Security > Microphone)
- Audio device availability: `rec --help-device`
- API key is set: `cat .aura/.env`
