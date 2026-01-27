---
name: aura.process_memo
description: Process all voice memos from queue - transcribe and act on requests
disable-model-invocation: true
allowed-tools: Bash(python *), Bash(mv *), Read, Write, Glob, Grep, Edit
---

# Process Voice Memos

Process all voice memos in the queue sequentially.

## Queue Location

Memos are stored in `.aura/memo/queue/<title>/` with:
- `audio.wav` or `audio.m4a` - Original recording
- `transcript.txt` - Raw transcript (created if missing)

## Steps

1. **List queue** - Find all memo directories:
   ```bash
   ls -1 .aura/memo/queue/
   ```

2. **For each memo directory**, process sequentially:

   a. **Check for transcript** - If `transcript.txt` doesn't exist:
      ```bash
      python .aura/scripts/transcribe.py .aura/memo/queue/<title>/audio.* > .aura/memo/queue/<title>/transcript.txt
      ```

   b. **Read transcript** - Use Read tool on `.aura/memo/queue/<title>/transcript.txt`

   c. **Act on request** - Execute what the user asked for in the memo

   d. **On success** - Move to processed with timestamp:
      ```bash
      mv .aura/memo/queue/<title> .aura/memo/processed/<title>_$(date +%Y%m%d_%H%M%S)
      ```

   e. **On failure** - Move to failed with timestamp:
      ```bash
      mv .aura/memo/queue/<title> .aura/memo/failed/<title>_$(date +%Y%m%d_%H%M%S)
      ```

3. **Continue** - Process next memo without user confirmation

## Empty Queue

If `.aura/memo/queue/` is empty or contains only `.gitkeep`, report:
"No memos in queue. Add voice memos to `.aura/memo/queue/<title>/audio.wav`"

## Error Handling

- If transcription fails, move memo to failed/
- If acting on request fails, move memo to failed/
- Always continue to next memo after handling current one
