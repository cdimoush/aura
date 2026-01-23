# Chore: Intent Detection Logic

## Overview

Define the rules and implementation for detecting user intent from voice memo transcripts. This logic determines how the processing commands transform raw transcripts into final output.

## Approach

Pattern-based keyword matching for intent detection. Simple, fast, and covers most use cases. LLM-based analysis can be added as a future enhancement if needed.

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

### Pattern Matching

```python
import re

def detect_intent(transcript: str) -> str:
    """Detect user intent from transcript.

    Returns:
        One of: 'research', 'summary', 'code', 'paraphrase', 'default'
    """
    text_lower = transcript.lower()

    # Research patterns
    research_patterns = [
        r'\b(research|look up|search for|find information)\b',
        r'\b(what is|how does|why does|how do I)\b',
        r'\bgoogle\b'
    ]
    if any(re.search(p, text_lower) for p in research_patterns):
        return 'research'

    # Summary patterns
    summary_patterns = [
        r'\b(summarize|sum up|tldr|tl;dr)\b',
        r'\b(key points|main ideas)\b',
        r'\b(condense|brief)\b'
    ]
    if any(re.search(p, text_lower) for p in summary_patterns):
        return 'summary'

    # Code patterns
    code_patterns = [
        r'\b(code|pseudocode|algorithm)\b',
        r'\b(write (a )?function|implement)\b',
        r'\b(example code|code snippet)\b'
    ]
    if any(re.search(p, text_lower) for p in code_patterns):
        return 'code'

    # Paraphrase patterns
    paraphrase_patterns = [
        r'\b(paraphrase|rewrite|rephrase)\b',
        r'\b(say differently|clarify)\b',
        r'\b(make clearer|clean up)\b'
    ]
    if any(re.search(p, text_lower) for p in paraphrase_patterns):
        return 'paraphrase'

    # Default: no explicit intent
    return 'default'
```

### LLM Fallback (Future Enhancement)

If pattern matching proves insufficient, LLM-based intent detection can be added:

```python
def detect_intent_llm(transcript: str) -> str:
    """Use LLM to detect intent when pattern matching is ambiguous."""
    prompt = f"""Analyze this voice memo transcript and identify the user's intent.

Choose ONE of: research, summary, code, paraphrase, default

Transcript: {transcript[:500]}

Intent:"""

    # Call OpenAI API (similar to generate_title.py)
    # ...
    return intent
```

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

**Implementation**:
```python
def clean_inline_edits(text: str) -> str:
    """Remove text before inline edit markers."""
    # Split on edit markers
    patterns = [
        r'\.{2,}?\s*(actually|wait|scratch that)',
        r'\b(no|correction)[,\s]+(I mean|that should be)',
        r'(never mind|forget that)',
    ]

    # For each pattern, remove text before it
    # Keep text after the marker
    # ...

    return cleaned_text
```

## Tasks

- [ ] Implement `detect_intent()` function with pattern matching
- [ ] Implement `clean_inline_edits()` function
- [ ] Create unit tests for each intent pattern
- [ ] Create unit tests for inline edit detection
- [ ] Document patterns in processing command files
- [ ] Add examples to `.claude/commands/aura.process.md`

## Acceptance Criteria

- [ ] `detect_intent()` correctly identifies all 5 intent types
- [ ] Pattern matching is case-insensitive
- [ ] Inline edit detection works for common phrases
- [ ] False positive rate < 5% on test transcripts
- [ ] False negative rate < 10% on test transcripts
- [ ] Function is fast (< 50ms for typical transcript)
- [ ] Code is well-documented with examples

## Testing Plan

### Unit Tests

Create test cases for each intent:

```python
def test_research_intent():
    assert detect_intent("I want to research OAuth implementation") == "research"
    assert detect_intent("How does JWT authentication work?") == "research"

def test_summary_intent():
    assert detect_intent("Please summarize this idea") == "summary"
    assert detect_intent("Give me the key points") == "summary"

def test_code_intent():
    assert detect_intent("Write pseudocode for bubble sort") == "code"
    assert detect_intent("Show me example code") == "code"

def test_paraphrase_intent():
    assert detect_intent("Can you rephrase this more clearly?") == "paraphrase"

def test_default_intent():
    assert detect_intent("This is just a note about the meeting") == "default"
```

### Integration Tests

Test with actual transcripts:

```bash
# Record test memos with explicit intents
python .aura/scripts/record_memo.py  # "Research React hooks best practices"
python .aura/scripts/record_memo.py  # "Summarize the API design"
python .aura/scripts/record_memo.py  # "Just a random thought about the code"

# Process and verify intent detection
/aura.process
```

## Documentation

- [ ] Document intent categories in CLAUDE.md
- [ ] Add examples to processing command templates
- [ ] Include in README.md workflow section

## Dependencies

- No external dependencies (uses standard library regex)
- Must complete before: [Feature: Aura Process Command](./feature-aura-process.md)

## Notes

- Start simple with pattern matching only
- Add LLM fallback if users report misdetection
- Consider adding explicit intent markers: "Intent: research" in transcript
- Future: Support multiple intents in single memo ("Research X and write code for Y")
- Future: User-configurable patterns via `.aura/config.md`
