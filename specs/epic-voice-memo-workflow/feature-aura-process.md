# Feature: Aura Process Command

## Overview

Create `/aura.process` slash command that processes queued voice memos according to detected intent, formats as markdown, and moves to output directory.

## User Story

As a developer, after recording voice memos, I want to process them into clean, formatted documents so that I can reference them later or share them with my team.

## Context

Voice memos sit in `.aura/queue/` after recording and transcription. The process command:
1. Lists available memos in queue
2. Allows selection (or processes all)
3. Detects intent from transcript
4. Transforms according to intent
5. Creates formatted `transcript.md`
6. Moves to `.aura/output/`

This is the Aura-specific processing path (vs Cyborg which creates brain notes).

## Command Specification

**Location**: `.claude/commands/aura.process.md`

**Allowed Tools**:
- `Read` - Read transcript files
- `Glob` - Find queued memos
- `Write` - Create formatted markdown
- `Bash(mv:*)` - Move directories
- `Bash(ls:*)` - List directories

**Description**: Process voice memos from queue to output

**Argument Hint**: `[memo-title] | --all`

## Command Workflow

### 1. Discovery Phase

```markdown
## Step 1: Find Queued Memos

Use Glob to find all directories in `.aura/queue/`:

```bash
ls .aura/queue/
```

List found memos:
- memo-title-1 (timestamp)
- memo-title-2 (timestamp)
- memo-title-3 (timestamp)

If no memos found, inform user and exit.
```

### 2. Selection Phase

```markdown
## Step 2: Select Memo to Process

If user provided memo title as argument:
- Validate it exists in queue
- Process that memo only

If user provided `--all`:
- Process all queued memos in sequence

If no argument:
- Ask user to specify memo title or use `--all`
```

### 3. Intent Detection Phase

```markdown
## Step 3: Detect Intent

Read `transcript.txt` from memo directory.

Use intent detection logic (from chore-intent-detection.md):
- Pattern match for keywords
- Detect: research, summary, code, paraphrase, or default

Inform user of detected intent.
```

### 4. Processing Phase

```markdown
## Step 4: Process Based on Intent

#### Research Intent
- Perform web search if available
- Summarize findings
- Include sources
- Format as structured markdown

#### Summary Intent
- Extract key points
- Create bullet list
- Condense to essentials

#### Code Intent
- Format code blocks
- Add language tags
- Structure with comments
- Explain what the code does

#### Paraphrase Intent
- Improve clarity
- Fix grammar
- Maintain original meaning
- Enhance readability

#### Default Intent
- Remove stuttering (um, uh, like)
- Remove filler phrases
- Follow inline edits ("actually", "scratch that")
- Preserve content and tone
- Minimal transformation
```

### 5. Formatting Phase

```markdown
## Step 5: Create Formatted Markdown

Create `transcript.md` with this structure:

```markdown
# <Title>

*Processed: <timestamp>*
*Intent: <detected-intent>*

---

<processed content>

---

## Original Transcript

<raw transcript for reference>

## Files

- Audio: [audio.wav](./audio.wav)
- Raw Transcript: [transcript.txt](./transcript.txt)
```

Use Write tool to create this file in the memo directory.
```

### 6. Movement Phase

```markdown
## Step 6: Move to Output

Move entire directory from `.aura/queue/<title>/` to `.aura/output/<title>/`:

```bash
mkdir -p .aura/output
mv .aura/queue/<title> .aura/output/
```

Verify move completed successfully.

Show user the final location: `.aura/output/<title>/transcript.md`
```

## Implementation Tasks

- [ ] Create `.claude/commands/aura.process.md` with frontmatter
- [ ] Implement discovery phase (glob for queue directories)
- [ ] Implement selection phase (argument parsing)
- [ ] Integrate intent detection logic
- [ ] Implement each intent processing path
- [ ] Implement markdown formatting template
- [ ] Implement directory movement
- [ ] Add error handling for each phase
- [ ] Test with various intent types

## Acceptance Criteria

- [ ] Command lists all queued memos when run without arguments
- [ ] Command processes specific memo when title provided
- [ ] Command processes all memos with `--all` flag
- [ ] Intent detection correctly identifies user intent
- [ ] Each intent type produces appropriate output
- [ ] Default intent removes stuttering and filler
- [ ] `transcript.md` has consistent formatting
- [ ] Original files (`audio.wav`, `transcript.txt`) are preserved
- [ ] Directory moves from queue to output
- [ ] Error messages are clear and actionable
- [ ] Success message shows output location

## Example Usage

### Process Single Memo

```
User: /aura.process bug-fix-authentication

Agent: Processing memo: bug-fix-authentication

Reading transcript...
Detected intent: default (no explicit intent)

Cleaning transcript:
- Removed 12 filler words
- Applied 2 inline edits

Creating transcript.md...
Moving to output directory...

✓ Processed: .aura/output/bug-fix-authentication/transcript.md
```

### Process All Memos

```
User: /aura.process --all

Agent: Found 3 queued memos. Processing...

1/3: feature-dark-mode (intent: code)
  ✓ .aura/output/feature-dark-mode/transcript.md

2/3: research-oauth (intent: research)
  ✓ .aura/output/research-oauth/transcript.md

3/3: meeting-notes (intent: summary)
  ✓ .aura/output/meeting-notes/transcript.md

All memos processed successfully!
```

## Testing Plan

### Manual Testing

1. **Default Intent Test**:
   ```bash
   # Record memo with no explicit intent
   python .aura/scripts/record_memo.py
   # Say: "This is a note about the bug fix, um, we need to, uh, check the authentication"

   # Process
   /aura.process <title>

   # Verify: fillers removed, content preserved
   ```

2. **Research Intent Test**:
   ```bash
   # Record memo: "Research OAuth 2.0 best practices"
   /aura.process <title>
   # Verify: web search results included
   ```

3. **Multiple Memos Test**:
   ```bash
   # Record 3 different memos
   /aura.process --all
   # Verify: all processed correctly
   ```

4. **Inline Edit Test**:
   ```bash
   # Record memo: "We need three parameters... actually, make that four parameters"
   /aura.process <title>
   # Verify: "We need four parameters" (edit applied)
   ```

### Integration Testing

1. Full workflow: record → process → verify output
2. Process → edit transcript.md → verify edits persist
3. Multiple users processing same queue (race conditions)

## Documentation Updates

- [ ] Add `/aura.process` to README.md command list
- [ ] Document intent detection in CLAUDE.md
- [ ] Add examples to command file
- [ ] Update workflow diagrams

## Dependencies

- Must complete: [Chore: Intent Detection Logic](./chore-intent-detection.md)
- Must complete: [Chore: Queue Directory Structure](./chore-queue-structure.md)
- Uses: `transcript.txt` from recording script
- Creates: `transcript.md` in output directory

## Edge Cases

1. **Empty Queue**: Inform user, suggest `/aura.record`
2. **Invalid Title**: Show available memos, ask for valid selection
3. **Title Collision in Output**: Append timestamp suffix
4. **Corrupt Transcript**: Warn user, skip or prompt for manual intervention
5. **Network Failure** (for research intent): Fallback to local processing
6. **Very Long Transcript**: Truncate preview, process full content

## Future Enhancements

- Interactive selection (numbered list, pick one)
- Preview mode (show what would be generated without moving)
- Batch processing with progress bar
- Custom templates for formatting
- Export to other formats (PDF, HTML)
- Integration with Beads (create ticket from memo)
