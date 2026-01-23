# Epic: Voice Memo Workflow - Aura & Cyborg Integration

## Epic Overview

This epic establishes a complete voice memo workflow across both Aura and Cyborg, enabling developers to capture ideas through voice, have them automatically transcribed and organized, then processed according to their intent. The workflow bridges the gap between spoken ideas and structured knowledge/tasks.

The system has three key flows:
1. **Record & Transcribe**: Capture audio via SoX, immediately transcribe with chunking support, auto-generate titles, organize in queue
2. **Aura Processing**: Move memos from queue to output, analyze user intent (research, summary, code examples), clean transcripts, format as markdown
3. **Cyborg Processing**: Move memos from queue to brain directory, convert to brain-compatible notes with tags and structure

This epic also establishes patterns for cross-project audio recording (recording from Cyborg while it's scaffolded with Aura) and adds cleanup capabilities to the Aura CLI (`aura remove`).

When complete, you'll be able to speak ideas anywhere in your workflow, have them intelligently processed, and end up with either clean documentation (Aura) or searchable brain notes (Cyborg) without manual formatting.

## Specs in This Epic

### Phase 1: Core Recording Infrastructure
- [ ] [Feature: SoX Recording Script](./feature-sox-recording-script.md) - Record audio to WAV with immediate transcription
- [ ] [Chore: Queue Directory Structure](./chore-queue-structure.md) - Define subdirectory format and file organization

### Phase 2: Aura Processing
- [ ] [Feature: Aura Process Command](./feature-aura-process.md) - Process queue memos, analyze intent, format as markdown
- [ ] [Chore: Intent Detection Logic](./chore-intent-detection.md) - Define how to detect web research, summaries, code examples, etc.

### Phase 3: Cyborg Integration
- [ ] [Feature: Cyborg Process Command](./feature-cyborg-process.md) - Convert memos to brain notes with tags
- [ ] [Chore: Brain Note Format](./chore-brain-note-format.md) - Define brain-compatible structure and tagging

### Phase 4: Cross-Project Recording (Decision Required)
- [ ] [Decision: Cross-Project Audio Strategy](./decision-cross-project-audio.md) - How to record from Cyborg or other Aura-initialized repos
- [ ] [Chore: Implement Chosen Strategy](./chore-cross-project-impl.md) - Implement the decided approach

### Phase 5: Aura Cleanup & Distribution
- [ ] [Feature: Aura Remove Command](./feature-aura-remove.md) - Clean up all Aura files from a directory
- [ ] [Chore: Update Init with New Features](./chore-update-init.md) - Ensure `aura init` distributes all new scripts and commands

## Execution Order

### Phase 1: Core Recording Infrastructure
**Goal**: Create a working recording script that captures audio, transcribes it immediately, and organizes it in the queue.

Execute in order:
1. [Chore: Queue Directory Structure](./chore-queue-structure.md) - Must define the structure before scripts create it
2. [Feature: SoX Recording Script](./feature-sox-recording-script.md) - Implements recording with transcription pipeline

**Success Criteria**:
- `record_memo.py` script records audio using SoX on macOS
- Audio saved as WAV to `.aura/queue/<title>/audio.wav`
- Transcript automatically generated with chunking support
- Raw transcript saved to `.aura/queue/<title>/transcript.txt`
- Title auto-generated from transcript content using LLM
- Script handles errors gracefully (no SoX, no API key, etc.)

**Testing Breakpoint**: Record a test memo, verify subdirectory creation, verify transcript content matches audio, verify title is meaningful.

---

### Phase 2: Aura Processing
**Goal**: Process queued memos according to user intent and move to output directory with clean formatting.

Execute in order:
1. [Chore: Intent Detection Logic](./chore-intent-detection.md) - Must define detection rules before implementing command
2. [Feature: Aura Process Command](./feature-aura-process.md) - Implements the `/aura.process` slash command

**Success Criteria**:
- `/aura.process` command lists all queued memos
- Command detects user intent from transcript (research, summary, code, paraphrase)
- If no intent: clean transcript (remove stuttering, follow inline edits)
- Creates `transcript.md` with markdown formatting, title, timestamp
- Moves entire subdirectory from `.aura/queue/` to `.aura/output/`
- Preserves original `transcript.txt` and `audio.wav` files
- Multiple memos can be processed in sequence

**Testing Breakpoint**: Process a memo with explicit intent ("summarize this"), verify output format. Process a memo without intent, verify transcript cleaning. Verify all files moved correctly.

---

### Phase 3: Cyborg Integration
**Goal**: Enable brain note creation from voice memos, compatible with Cyborg's regenerate system.

Execute in order:
1. [Chore: Brain Note Format](./chore-brain-note-format.md) - Must understand brain structure before implementing conversion
2. [Feature: Cyborg Process Command](./feature-cyborg-process.md) - Implements `/cyborg.process` command

**Success Criteria**:
- `/cyborg.process` command available in Cyborg-scaffolded projects
- Command detects user intent for note creation
- Converts transcript to brain-compatible format (subdirectory with multiple files)
- Adds appropriate tags for brain search/regenerate
- Moves from `.aura/queue/` to `brain/` directory
- Notes work correctly with `brain regenerate` command
- Preserves audio and raw transcript for reference

**Dependencies**: Requires understanding of Cyborg's brain directory structure and tagging system.

**Testing Breakpoint**: Create a voice memo in Cyborg, process it with `/cyborg.process`, verify brain note structure, run `brain regenerate` to ensure compatibility.

---

### Phase 4: Cross-Project Recording
**Goal**: Implement and test recording strategy across multiple Aura-initialized projects.

Execute in order:
1. [Cross-Project Audio Strategy](./decision-cross-project-audio.md) - Documents the self-contained script approach
2. [Chore: Implement Chosen Strategy](./chore-cross-project-impl.md) - Test and validate across projects

**Approach**: Scripts are copied to each project via `aura init`. SoX installed system-wide, Python dependencies per-project. Self-contained operation without external dependencies.

**Success Criteria**:
- Recording works from Aura, Cyborg, and test project
- Each project's recordings go to its own `.aura/queue/`
- Documentation covers cross-project workflow
- No absolute path dependencies

---

### Phase 5: Aura Cleanup & Distribution
**Goal**: Add removal capability and ensure all new features are distributed via `aura init`.

Execute in order:
1. [Feature: Aura Remove Command](./feature-aura-remove.md) - Implements `aura remove` CLI command
2. [Chore: Update Init with New Features](./chore-update-init.md) - Updates init logic to include new scripts and commands

**Success Criteria**:
- `aura remove` command cleanly removes all Aura files from directory
- Command lists files to be removed before deletion
- Confirmation prompt prevents accidental deletion
- `--force` flag for non-interactive removal
- `aura init` includes `record_memo.py` in script distribution
- `aura init` includes `/aura.process` command
- `aura init` includes `/cyborg.process` command (when in Cyborg context)
- Fresh `aura init` in test project includes all new features

**Testing Breakpoint**: Run `aura init` in fresh directory, verify all new files present. Run `aura remove`, verify all files removed. Run `aura init` again, verify clean reinstall.

---

## Path Dependencies Diagram

```
Phase 1: Core Recording
    |-- Queue Structure (defines organization)
    +-- SoX Recording Script (implements recording)
    |
    v
Phase 2: Aura Processing
    |-- Intent Detection (defines rules)
    +-- Aura Process Command (implements processing)
    |
    v
Phase 3: Cyborg Integration
    |-- Brain Note Format (defines structure)
    +-- Cyborg Process Command (implements conversion)
    |
    v
Phase 4: Cross-Project Recording
    |-- Strategy Decision (REQUIRED: user choice)
    +-- Implementation (depends on decision)
    |
    v
Phase 5: Cleanup & Distribution
    |-- Aura Remove Command (cleanup capability)
    +-- Update Init (distribution of new features)
    |
    v
  DONE

Critical Path: Recording → Aura Processing → Cyborg Integration → Cross-Project Decision → Distribution
Parallel Opportunities: Phases 2 and 3 can develop concurrently after Phase 1 completes
```

## Success Metrics

- [ ] `record_memo.py` script records and transcribes voice memos on macOS
- [ ] Transcription includes chunking for files >8 minutes
- [ ] Titles auto-generated from transcript content
- [ ] Queue directory structure: `.aura/queue/<title>/{audio.wav, transcript.txt}`
- [ ] `/aura.process` detects intent and processes accordingly
- [ ] `/aura.process` moves to `.aura/output/` with formatted markdown
- [ ] `/cyborg.process` creates brain-compatible notes with tags
- [ ] `/cyborg.process` moves to `brain/` directory
- [ ] Cross-project recording strategy decided and implemented
- [ ] `aura remove` cleanly removes all Aura files
- [ ] `aura init` distributes all new scripts and commands
- [ ] Documentation covers complete workflow from recording to output
- [ ] Zero manual file organization required

## Implementation Approach

### Cross-Project Recording
Scripts are copied to each project via `aura init` for self-contained operation. Each project has its own `.aura/` with scripts and queue. SoX is installed system-wide, Python dependencies per-project. See [decision-cross-project-audio.md](./decision-cross-project-audio.md) for details.

### Brain Note Format
Brain notes use single markdown files with YAML frontmatter for tags and metadata. Format: `brain/<title>.md` with auto-generated tags from content and intent. See [chore-brain-note-format.md](./chore-brain-note-format.md) for structure.

### Intent Detection
Pattern matching for keywords (research, summary, code, paraphrase) with fallback to default cleaning. Fast, simple, and covers most use cases. LLM-based analysis can be added later if needed. See [chore-intent-detection.md](./chore-intent-detection.md) for patterns.

## Future Enhancements

Ideas that came up during planning but are out of scope:

1. **Hotkey support** - System-wide hotkey to start/stop recording (deferred, use manual terminal invocation for now)
2. **Real-time transcription** - Stream audio and transcribe in real-time
3. **Speaker identification** - Multi-speaker transcription with labels
4. **Audio editing** - Trim, splice, or edit recordings before transcription
5. **Alternative transcription engines** - Support for Whisper local, Azure, Google Speech
6. **Mobile recording** - Capture voice memos on phone, sync to queue
7. **Voice command detection** - Parse commands like "create ticket" from speech
8. **Batch processing** - Process multiple memos at once with `/aura.process --all`
9. **Template-based formatting** - Custom markdown templates for different memo types
10. **Search and retrieval** - Search across processed memos by content or tags

## Reference

- Commands: `.claude/commands/aura.*.md`, `.claude/commands/cyborg.*.md`
- Scripts: `.aura/scripts/record_memo.py`, `transcribe.py`, `generate_title.py`
- Previous epic: [epic-aura-cleanup](../epic-aura-cleanup/README.md)
- Created: 2026-01-22
