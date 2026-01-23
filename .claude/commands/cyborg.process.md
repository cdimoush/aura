---
allowed-tools: Read, Glob, Write, Bash(mv:*), Bash(mkdir:*), Bash(ls:*), Bash(cp:*), Bash(python:*)
description: Process voice memos into brain notes
argument-hint: [memo-title] | --all
---

# Process Voice Memos into Brain Notes

Convert queued voice memos into brain-compatible notes with auto-generated tags for Cyborg's knowledge management system.

## Step 1: Find Queued Memos

List all directories in `.aura/queue/`:

```bash
ls -1 .aura/queue/ 2>/dev/null || echo "NO_QUEUE"
```

If the queue directory doesn't exist or is empty, inform the user:

> No memos found in `.aura/queue/`. Record a memo first with `/aura.record` or `/aura.act`.

## Step 2: Select Memo to Process

**If `$ARGUMENTS` is `--all`**:
- Process all queued memos in sequence.

**If `$ARGUMENTS` is a specific memo title**:
- Validate it exists in `.aura/queue/$ARGUMENTS/`
- Process that memo only.

**If no argument provided**:
- List all available memos with their creation dates.
- Ask user to specify a memo title or use `--all`.

## Step 3: Process Each Memo

For each memo to process:

### 3a. Read the Transcript

Read the transcript file:

```
.aura/queue/<title>/transcript.txt
```

If no transcript exists, check for alternative file names or inform user.

### 3b. Detect Intent

Use the intent detection script:

```bash
python .aura/scripts/intent_detection.py --file ".aura/queue/<title>/transcript.txt"
```

This returns one of: `research`, `summary`, `code`, `paraphrase`, or `default`.

### 3c. Extract Key Concepts and Generate Tags

Analyze the transcript to extract:

1. **Technical Terms**: API names, languages, frameworks, libraries
2. **Action Words**: implement, refactor, fix, design, research, test
3. **Domain Concepts**: authentication, frontend, testing, database, etc.
4. **From Intent**: Add the detected intent as a tag (research, code, summary)

Generate a tag list following these rules:
- Always include: `voice-memo`
- Always include temporal tag: current year-month (e.g., `2026-01`)
- Convert to lowercase
- Replace spaces with hyphens
- Keep alphanumeric and hyphens only
- Aim for 5-10 relevant tags

Example:
```
Transcript: "Research OAuth implementation patterns for our API"
Tags: [research, oauth, authentication, api, implementation, patterns, voice-memo, 2026-01]
```

### 3d. Create Brain Note

Create the brain note at `brain/<title>.md` with this structure:

```markdown
---
title: <Title (converted to Title Case)>
created: <ISO 8601 timestamp, e.g., 2026-01-22T14:30:00Z>
tags: [<comma-separated tags>]
source: voice-memo
audio: ../.aura/output/<title>/audio.wav
---

# <Title>

## Content

<Processed transcript content - clean up grammar, structure into paragraphs>

### Key Insights

<Extract 2-5 key points or insights from the memo>

### Questions

<Any questions raised in the memo, or "None identified">

### Related Topics

<List related concepts that could link to other brain notes>

## Original Transcript

<Raw transcript for reference>

## Metadata

- **Recorded**: <timestamp if available>
- **Intent**: <detected intent>
```

**Intent-based transformations**:
- **research**: Structure as findings, include suggested research areas
- **code**: Format any code references in code blocks, note technical details
- **summary**: Condense to key points, create bullet list summary
- **paraphrase**: Clean up and restructure the content
- **default**: Clean formatting, organize into logical sections

### 3e. Move Files to Output

1. Ensure brain directory exists:
   ```bash
   mkdir -p brain
   ```

2. Ensure output directory exists:
   ```bash
   mkdir -p .aura/output/<title>
   ```

3. Copy audio file to output (if exists):
   ```bash
   cp .aura/queue/<title>/audio.wav .aura/output/<title>/ 2>/dev/null || \
   cp .aura/queue/<title>/*.wav .aura/output/<title>/ 2>/dev/null || \
   cp .aura/queue/<title>/*.m4a .aura/output/<title>/ 2>/dev/null || true
   ```

4. Move entire queue directory to output:
   ```bash
   mv .aura/queue/<title> .aura/output/
   ```

## Step 4: Verify and Report

For each processed memo, verify:
- Brain note exists at `brain/<title>.md`
- Frontmatter is valid YAML
- Audio preserved in `.aura/output/<title>/`
- Queue directory moved successfully

Show user summary:

```
Processed: <title>
  Brain note: brain/<title>.md
  Tags: <tag list>
  Intent: <detected intent>
  Audio: .aura/output/<title>/audio.wav
```

## Step 5: Suggest Next Steps

After processing all memos:

```
Processing complete!

Next steps:
- Review brain notes in brain/ directory
- Run `brain regenerate` to update the brain index (if available)
- Use tags to search and connect related notes
```

## Edge Cases

### Title Collision
If `brain/<title>.md` already exists:
- Append timestamp suffix: `brain/<title>-<YYYYMMDD-HHMMSS>.md`
- Inform user of the renamed file

### Empty Transcript
If transcript is empty or whitespace only:
- Warn user: "Empty transcript found for <title>"
- Create minimal brain note with warning
- Still move files to output

### No Audio File
If no audio file exists:
- Set `audio:` frontmatter to empty or note "Audio not available"
- Continue processing transcript

### Special Characters in Title
Sanitize titles for filesystem safety:
- Replace spaces with hyphens
- Remove or replace special characters
- Convert to lowercase
- Keep alphanumeric and hyphens only

## Example Usage

### Process Single Memo

```
/cyborg.process oauth-research

Processing memo: oauth-research

Reading transcript...
Detected intent: research
Key concepts: OAuth 2.0, JWT, authentication, security

Generated tags: [research, oauth, jwt, authentication, security, voice-memo, 2026-01]

Creating brain note: brain/oauth-research.md
Preserving audio: .aura/output/oauth-research/audio.wav
Moving queue to output...

Processed: oauth-research
  Brain note: brain/oauth-research.md
  Tags: research, oauth, jwt, authentication, security, voice-memo, 2026-01
  Intent: research

Next steps:
- Review brain note: brain/oauth-research.md
- Run `brain regenerate` to update index
```

### Process All Memos

```
/cyborg.process --all

Found 3 queued memos. Processing...

1/3: oauth-research
  Intent: research
  Brain note: brain/oauth-research.md
  Tags: research, oauth, authentication, voice-memo, 2026-01

2/3: bug-fix-notes
  Intent: default
  Brain note: brain/bug-fix-notes.md
  Tags: bug-fix, debugging, voice-memo, 2026-01

3/3: code-pattern-idea
  Intent: code
  Brain note: brain/code-pattern-idea.md
  Tags: code, patterns, architecture, voice-memo, 2026-01

All 3 memos processed!

Next steps:
- Review brain notes in brain/ directory
- Run `brain regenerate` to update index
```
