---
allowed-tools: Bash(python:*), Bash(mkdir:*), Bash(mv:*), Bash(date:*), Bash(ls:*), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
description: Transcribe audio and act on the request
argument-hint: [audio-file-path]
---

# Act on Audio

Transcribe audio file(s), generate intelligent titles, and execute requests spoken within them.

## Prerequisites

- `OPENAI_API_KEY` environment variable must be set
- Dependencies installed: `pip install -r .aura/scripts/requirements.txt`

## Step 0: Determine Input Mode

Check `$ARGUMENTS`:

- **If a file path is provided**: Process that single audio file (go to Step 1)
- **If no argument**: Process all audio files in `.aura/queue/` (go to Step 0a)

### Step 0a: Queue Processing Mode

List all audio files in the queue:

```bash
ls -1 .aura/queue/*.wav .aura/queue/*.m4a .aura/queue/*.mp3 2>/dev/null
```

If no files found:
```
No audio files found in .aura/queue/

Record a new memo with: /aura.record
```

Otherwise, process each file by repeating Steps 1-8 for each audio file. Track results and show a summary at the end:

```
Processed 3 audio files:
  1. feature-idea_2026-01-27_14-30-22 -> .aura/output/feature-idea_2026-01-27_14-30-22/
  2. bug-report_2026-01-27_14-32-15 -> .aura/output/bug-report_2026-01-27_14-32-15/
  3. meeting-notes_2026-01-27_14-35-00 -> .aura/output/meeting-notes_2026-01-27_14-35-00/
```

## Step 1: Transcribe the Audio

Use the local transcription script:

```bash
python .aura/scripts/transcribe.py "$AUDIO_FILE"
```

Save the full transcription text for use in subsequent steps.

## Step 2: Generate Intelligent Title

Use the title generation script:

```bash
echo "$TRANSCRIPT" | python .aura/scripts/generate_title.py
```

Or if transcript is in a variable, use `--text`:

```bash
python .aura/scripts/generate_title.py --text "$TRANSCRIPT"
```

Examples of good titles:
- `player-movement-feature-request`
- `api-refactor-discussion`
- `bug-fix-auth-flow`

## Step 3: Create Timestamp

Get the current timestamp:

```bash
date +%Y-%m-%d_%H-%M-%S
```

## Step 4: Analyze the Transcription

Identify:

1. **Request Type**: What is the user asking for?
   - **Summary**: User wants a summary of ideas or content
   - **Research**: User wants research on a topic
   - **Code**: User wants code or technical implementation
   - **Planning**: User wants a plan or structured approach
   - **Other**: Any other actionable request

2. **Key Details**: Extract main topics, requirements, constraints, and goals

3. **Deliverables**: What output files should be created?

## Step 5: Create Output Directory

Create the output directory using the generated title and timestamp:

```bash
mkdir -p ".aura/output/${TITLE}_${TIMESTAMP}/"
```

Example: `.aura/output/api-refactor-discussion_2026-01-08_14-30-22/`

## Step 6: Create README.md

In the output directory, create a `README.md` with:

```markdown
# {Generated Title}

## Source
- **Audio File**: [original filename]
- **Transcribed**: [timestamp]

## Transcription Summary
[2-3 sentence summary of what was spoken]

## Request Identified
- **Type**: [Summary/Research/Code/Planning/Other]
- **Description**: [What the user is asking for]

## Deliverables
- [ ] [List of files that will be created]

## Full Transcription
<details>
<summary>Click to expand</summary>

[Full transcription text]

</details>
```

## Step 7: Execute the Request

Based on the request type, create appropriate deliverables:

### For Summary Requests
- Create `summary.md` with key points, main ideas, action items

### For Research Requests
- Create `research.md` with overview, findings, sources, recommendations

### For Code Requests
- Create implementation files with appropriate extensions
- Include usage documentation if needed

### For Planning Requests
- Create `plan.md` with goals, steps, considerations, next actions

## Step 8: Move Audio to Output Directory

Move the processed audio file into the output directory:

```bash
mv "$ARGUMENTS" ".aura/output/${TITLE}_${TIMESTAMP}/"
```

## Important Notes

- Always create the output directory first before writing any files
- If the request is unclear, focus on the primary request and note others in the README
- Only move the audio after successful processing
