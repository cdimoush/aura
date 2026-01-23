# Chore: Intent Detection Logic

## Overview

Define the rules and implementation for detecting user intent from voice memo transcripts. This logic determines how the processing commands transform raw transcripts into final output.

## Approach

**LLM-based inline analysis** - Claude analyzes the transcript directly during command execution. No external scripts or subprocess calls needed.

### Why LLM Instead of Pattern Matching?

1. **More accurate**: LLM understands context and nuance that regex patterns miss
2. **Faster**: No subprocess overhead or Python interpreter startup
3. **Simpler**: No cross-project script dependencies
4. **Self-contained**: Commands work without external files
5. **Flexible**: Can handle edge cases and ambiguous intents

## Intent Categories

When processing a voice memo, detect user intent:
- **Research**: "Look up how to implement OAuth" → web search, summary
- **Summary**: "Summarize this idea" → condensed version
- **Code**: "Write pseudocode for the algorithm" → code block formatting
- **Paraphrase**: "Rewrite this more clearly" → rephrased version
- **Default**: No explicit intent → clean transcript (remove stuttering, inline edits)

### 1. Research Intent
**Triggers**:
- "research", "look up", "search for", "find information about"
- "what is", "how does", "why does"
- "google", "find articles"

**Actions**:
- Perform web search (if agent has web access)
- Summarize findings
- Include sources

### 2. Summary Intent
**Triggers**:
- "summarize", "sum up", "tldr", "tl;dr"
- "key points", "main ideas"
- "condense", "brief version"

**Actions**:
- Create bullet-point summary
- Extract key concepts
- Remove filler content

### 3. Code Intent
**Triggers**:
- "code", "pseudocode", "algorithm"
- "write a function", "implement"
- "example code", "code snippet"

**Actions**:
- Format as code blocks
- Add appropriate language tags
- Structure with comments

### 4. Paraphrase Intent
**Triggers**:
- "paraphrase", "rewrite", "rephrase"
- "say differently", "clarify"
- "make clearer", "clean up"

**Actions**:
- Improve clarity
- Fix grammar
- Maintain meaning

### 5. Default (No Intent)
**Triggers**:
- None of the above patterns match

**Actions**:
- Remove stuttering ("um", "uh", "like")
- Remove filler phrases
- Follow inline edits ("actually, scratch that")
- Preserve content and tone
- Minimal transformation

## Implementation

The intent detection is embedded directly in the Claude Code slash commands (`/aura.process` and `/cyborg.process`). When Claude executes these commands, it:

1. Reads the transcript file
2. Analyzes the content against the trigger phrases table
3. Classifies into one of the five intents
4. Applies intent-specific transformations

### Inline Intent Detection Table

Commands include this reference table for Claude to use during analysis:

| Intent | Trigger Phrases |
|--------|-----------------|
| **research** | "research", "look up", "search for", "what is", "how does", "why does", "find information" |
| **summary** | "summarize", "sum up", "tldr", "key points", "main ideas", "condense" |
| **code** | "code", "pseudocode", "algorithm", "write a function", "implement", "code snippet" |
| **paraphrase** | "paraphrase", "rewrite", "rephrase", "clarify", "make clearer", "clean up" |
| **default** | None of the above patterns match |

## Inline Edit Detection

For default intent, detect and follow inline edits:

**Patterns to Detect**:
- "actually", "wait", "scratch that"
- "no, I mean", "correction"
- "edit that", "change that to"
- "never mind", "forget that"

**Examples**:
- "The function should return true... actually, return false"
  → "The function should return false"
- "We need three parameters... no, I mean four parameters"
  → "We need four parameters"

Claude handles these naturally during transcript processing - no separate function needed.

## Acceptance Criteria

- [x] Commands include intent trigger phrases for reference
- [x] No external script dependencies
- [x] Intent detection happens inline during command execution
- [x] All 5 intent types are documented
- [x] Inline edit handling is documented

## Testing

Test with actual voice memos:

```bash
# Record test memos with explicit intents
/aura.record  # "Research React hooks best practices"
/aura.record  # "Summarize the API design"
/aura.record  # "Just a random thought about the code"

# Process and verify intent detection
/aura.process --all
```

## Notes

- LLM approach handles ambiguous cases better than regex
- Future: Support multiple intents in single memo ("Research X and write code for Y")
- Future: User-configurable intent patterns via `.aura/config.md`
