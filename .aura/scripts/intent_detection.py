#!/usr/bin/env python3
"""Detect user intent from voice memo transcripts.

This module provides intent detection and inline edit cleaning for voice memo
transcripts. Intent detection uses pattern matching to classify transcripts into
one of five categories: research, summary, code, paraphrase, or default.

Usage:
    python .aura/scripts/intent_detection.py --text "Research OAuth patterns"
    python .aura/scripts/intent_detection.py --file transcription.txt
    echo "Some text" | python .aura/scripts/intent_detection.py

Requirements:
    No external dependencies (uses standard library only)
"""

import re
import sys
import argparse


# Intent detection patterns (case-insensitive)
RESEARCH_PATTERNS = [
    r'\b(research|look up|search for|find information)\b',
    r'\b(what is|how does|why does|how do I)\b',
    r'\bgoogle\b',
    r'\bfind articles\b',
]

SUMMARY_PATTERNS = [
    r'\b(summarize|sum up|tldr|tl;dr)\b',
    r'\b(key points|main ideas)\b',
    r'\b(condense|brief)\b',
]

CODE_PATTERNS = [
    r'\b(code|pseudocode|algorithm)\b',
    r'\b(write (a )?function|implement)\b',
    r'\b(example code|code snippet)\b',
]

PARAPHRASE_PATTERNS = [
    r'\b(paraphrase|rewrite|rephrase)\b',
    r'\b(say differently|clarify)\b',
    r'\b(make clearer|clean up)\b',
]

# Inline edit markers - text before these should be removed
INLINE_EDIT_PATTERNS = [
    # Ellipsis followed by correction words
    r'\.{2,}\s*(actually|wait|scratch that)',
    # Explicit correction phrases
    r'\b(no|correction)[,\s]+(I mean|that should be)',
    # Cancel phrases
    r'\b(never mind|forget that)\b',
]


def detect_intent(transcript: str) -> str:
    """Detect user intent from transcript.

    Analyzes the transcript text to determine what type of action the user
    wants. Uses pattern matching against known trigger phrases for each
    intent category.

    Args:
        transcript: The voice memo transcript text to analyze

    Returns:
        One of: 'research', 'summary', 'code', 'paraphrase', 'default'

    Examples:
        >>> detect_intent("I want to research OAuth implementation")
        'research'
        >>> detect_intent("How does JWT authentication work?")
        'research'
        >>> detect_intent("Please summarize this idea")
        'summary'
        >>> detect_intent("Write pseudocode for bubble sort")
        'code'
        >>> detect_intent("Can you rephrase this more clearly?")
        'paraphrase'
        >>> detect_intent("This is just a note about the meeting")
        'default'
    """
    if not transcript:
        return 'default'

    text_lower = transcript.lower()

    # Check research patterns
    if any(re.search(p, text_lower) for p in RESEARCH_PATTERNS):
        return 'research'

    # Check summary patterns
    if any(re.search(p, text_lower) for p in SUMMARY_PATTERNS):
        return 'summary'

    # Check code patterns
    if any(re.search(p, text_lower) for p in CODE_PATTERNS):
        return 'code'

    # Check paraphrase patterns
    if any(re.search(p, text_lower) for p in PARAPHRASE_PATTERNS):
        return 'paraphrase'

    # Default: no explicit intent detected
    return 'default'


def clean_inline_edits(text: str) -> str:
    """Remove text before inline edit markers, keeping the correction.

    Voice memos often contain self-corrections where the speaker says something
    and then corrects themselves. This function detects these patterns and
    removes the incorrect part, keeping only the corrected version.

    Args:
        text: The transcript text to clean

    Returns:
        Cleaned text with inline edits resolved

    Examples:
        >>> clean_inline_edits("The function should return true... actually, return false")
        'return false'
        >>> clean_inline_edits("We need three parameters... no, I mean four parameters")
        'four parameters'
        >>> clean_inline_edits("First approach... scratch that, use the second approach")
        'use the second approach'
        >>> clean_inline_edits("This is fine, never mind, let's do something else")
        "let's do something else"
    """
    if not text:
        return text

    result = text

    # Pattern 1: "... actually/wait/scratch that" - keep text after marker
    # Match: "anything... actually, something else" -> "something else"
    pattern1 = r'^.*\.{2,}\s*(actually|wait|scratch that)[,\s]*'
    match = re.search(pattern1, result, re.IGNORECASE)
    if match:
        result = result[match.end():].strip()

    # Pattern 2: "no, I mean" / "correction, that should be" - keep text after
    # Match: "anything no, I mean something else" -> "something else"
    pattern2 = r'^.*\b(no|correction)[,\s]+(I mean|that should be)[,\s]*'
    match = re.search(pattern2, result, re.IGNORECASE)
    if match:
        result = result[match.end():].strip()

    # Pattern 3: "never mind" / "forget that" - keep text after
    # Match: "anything never mind something else" -> "something else"
    pattern3 = r'^.*\b(never mind|forget that)[,\s]*'
    match = re.search(pattern3, result, re.IGNORECASE)
    if match:
        result = result[match.end():].strip()

    return result


def main():
    """CLI interface for intent detection."""
    parser = argparse.ArgumentParser(
        description="Detect user intent from voice memo transcripts",
        epilog="Examples:\n"
               "  python .aura/scripts/intent_detection.py --text 'Research OAuth'\n"
               "  python .aura/scripts/intent_detection.py --file transcription.txt\n"
               "  echo 'Summarize this idea' | python .aura/scripts/intent_detection.py\n"
               "  python .aura/scripts/intent_detection.py --clean --text 'old... actually, new'\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--file",
        type=str,
        help="Read transcript from file"
    )
    input_group.add_argument(
        "--text",
        type=str,
        help="Use provided text as transcript"
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean inline edits instead of detecting intent"
    )

    args = parser.parse_args()

    # Get transcript text from appropriate source
    try:
        if args.file:
            # Read from file
            import os
            if not os.path.exists(args.file):
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            with open(args.file, 'r', encoding='utf-8') as f:
                transcript = f.read()
        elif args.text:
            # Use provided text
            transcript = args.text
        else:
            # Read from stdin
            if sys.stdin.isatty():
                print("Error: No input provided. Use --file, --text, or pipe text via stdin.",
                      file=sys.stderr)
                print("Run 'python .aura/scripts/intent_detection.py --help' for usage information.",
                      file=sys.stderr)
                sys.exit(1)
            transcript = sys.stdin.read()

        # Handle empty input
        if not transcript or not transcript.strip():
            print("Error: Empty input provided", file=sys.stderr)
            sys.exit(1)

        transcript = transcript.strip()

        # Either clean inline edits or detect intent
        if args.clean:
            result = clean_inline_edits(transcript)
        else:
            result = detect_intent(transcript)

        print(result)

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
