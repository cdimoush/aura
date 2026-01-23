---
allowed-tools: Read, Glob, Write, Bash(mv:*), Bash(mkdir:*), Bash(ls:*), Bash(python:*), WebSearch
description: Process voice memos from queue to output
argument-hint: [memo-title] | --all
---

# Process Voice Memos

Process voice memos from `.aura/queue/` by detecting intent, transforming content, and moving to `.aura/output/`.

## Step 1: Find Queued Memos

List all directories in the queue:

```bash
ls -1 .aura/queue/
```

If no memos found, inform the user:
```
No memos found in .aura/queue/

Record a new memo with: /aura.record
```

Otherwise, list the available memos.

## Step 2: Select Memo to Process

Check the `$ARGUMENTS` value:

- **If a specific memo title is provided**: Validate it exists in `.aura/queue/`, then process that memo only
- **If `--all` is provided**: Process all queued memos in sequence
- **If no argument**: List available memos and ask the user which one to process, or suggest using `--all`

## Step 3: Process Each Memo

For each selected memo, perform these steps:

### 3a. Read the Transcript

Read the raw transcript from the memo directory:

```
.aura/queue/<memo-title>/transcript.txt
```

### 3b. Detect Intent

Analyze the transcript to detect the user's intent. Look for these patterns:

| Intent | Trigger Phrases |
|--------|-----------------|
| **research** | "research", "look up", "search for", "what is", "how does", "why does", "find information" |
| **summary** | "summarize", "sum up", "tldr", "key points", "main ideas", "condense" |
| **code** | "code", "pseudocode", "algorithm", "write a function", "implement", "code snippet" |
| **paraphrase** | "paraphrase", "rewrite", "rephrase", "clarify", "make clearer", "clean up" |
| **default** | None of the above patterns match |

Classify the transcript into one of these five intents and inform the user of the detected intent.

### 3c. Process Based on Intent

Transform the transcript content based on detected intent:

#### Research Intent
- Perform web search using WebSearch tool if available
- Search for the topic mentioned in the transcript
- Summarize findings with key points
- Include source URLs
- Format as structured markdown with sections

#### Summary Intent
- Extract key points from the transcript
- Create a bullet list of main ideas
- Condense to essentials
- Remove unnecessary details

#### Code Intent
- Format any code mentioned with proper code blocks
- Add language tags (```python, ```javascript, etc.)
- Structure with explanatory comments
- If describing an algorithm, provide pseudocode or implementation

#### Paraphrase Intent
- Improve clarity and readability
- Fix grammar and sentence structure
- Maintain the original meaning
- Enhance flow and coherence

#### Default Intent
- Remove filler words (um, uh, like, you know, so, basically)
- Remove stuttering and repeated words
- Apply inline edits (when user says "actually", "scratch that", "no I mean", keep only the correction)
- Preserve the original content and tone
- Minimal transformation - just clean up speech artifacts

### 3d. Create Formatted Markdown

Create `transcript.md` in the memo directory with this structure:

```markdown
# <Memo Title>

*Processed: <YYYY-MM-DD HH:MM>*
*Intent: <detected-intent>*

---

<processed content goes here>

---

## Original Transcript

<raw transcript text for reference>

## Files

- Audio: [audio.wav](./audio.wav)
- Raw Transcript: [transcript.txt](./transcript.txt)
```

Use the Write tool to create this file at `.aura/queue/<memo-title>/transcript.md`.

### 3e. Move to Output Directory

Move the entire memo directory from queue to output:

```bash
mkdir -p .aura/output
mv ".aura/queue/<memo-title>" ".aura/output/"
```

Verify the move completed successfully.

## Step 4: Completion Message

After processing all selected memos, show a summary:

For single memo:
```
Processed: .aura/output/<memo-title>/transcript.md
```

For multiple memos (--all):
```
Processed 3 memos:
  1. feature-idea (intent: code) -> .aura/output/feature-idea/transcript.md
  2. meeting-notes (intent: summary) -> .aura/output/meeting-notes/transcript.md
  3. random-thought (intent: default) -> .aura/output/random-thought/transcript.md

All memos processed successfully!
```

## Error Handling

### Empty Queue
```
No memos found in .aura/queue/
Record a new memo with: /aura.record
```

### Invalid Memo Title
```
Memo not found: <provided-title>

Available memos:
- memo-1
- memo-2

Please specify a valid memo title.
```

### Missing transcript.txt
```
Warning: <memo-title>/transcript.txt not found
Skipping this memo. Run /aura.transcribe on the audio file first.
```

### Title Already Exists in Output
If `.aura/output/<memo-title>` already exists, append a timestamp:
```bash
mv ".aura/queue/<memo-title>" ".aura/output/<memo-title>_$(date +%Y%m%d_%H%M%S)"
```

## Tips

- Use `/aura.process --all` to batch process multiple memos
- Check `.aura/output/` for processed memos
- The original audio and transcript files are preserved in the output
- You can manually edit `transcript.md` after processing
