#!/usr/bin/env python3
"""Record voice memos using SoX with immediate transcription.

Usage:
    python .aura/scripts/record_memo.py
    python .aura/scripts/record_memo.py --duration 120

Requirements:
    - SoX installed: brew install sox (macOS)
    - ffmpeg installed: brew install ffmpeg
    - pip install -r .aura/scripts/requirements.txt

Environment:
    OPENAI_API_KEY - Required. Your OpenAI API key.
"""

import os
import sys
import argparse
import subprocess
import tempfile
import signal
from pathlib import Path
from datetime import datetime


def check_prerequisites():
    """Check that all required tools are installed."""
    errors = []

    # Check for SoX
    try:
        result = subprocess.run(
            ["sox", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            errors.append("SoX not working properly")
    except FileNotFoundError:
        errors.append("SoX not installed. Install with: brew install sox (macOS)")

    # Check for ffmpeg (required by pydub)
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            errors.append("ffmpeg not working properly")
    except FileNotFoundError:
        errors.append("ffmpeg not installed. Install with: brew install ffmpeg (macOS)")

    # Check for API key
    # Load environment variables from .env file first
    try:
        from dotenv import load_dotenv
        aura_env = Path(".aura/.env")
        if aura_env.exists():
            load_dotenv(aura_env)
        else:
            load_dotenv()
    except ImportError:
        pass

    if not os.environ.get("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY not set. Add it to .aura/.env or export it")

    # Check for Python dependencies
    try:
        from pydub import AudioSegment
    except ImportError:
        errors.append("pydub not installed. Run: pip install -r .aura/scripts/requirements.txt")

    try:
        from openai import OpenAI
    except ImportError:
        errors.append("openai not installed. Run: pip install -r .aura/scripts/requirements.txt")

    if errors:
        print("Prerequisites check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


def record_audio(output_path: str, duration: int | None = None) -> bool:
    """Record audio using SoX.

    Args:
        output_path: Path to save the WAV file
        duration: Optional duration limit in seconds

    Returns:
        True if recording completed successfully
    """
    # Build SoX command
    # -r 16000: 16kHz sample rate (good for speech)
    # -c 1: Mono channel
    cmd = ["rec", "-r", "16000", "-c", "1", output_path]

    if duration:
        cmd.extend(["trim", "0", str(duration)])

    print("Recording... (Press Ctrl+C to stop)", file=sys.stderr)

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for the process to complete or be interrupted
        process.wait()
        return process.returncode == 0

    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        process.terminate()
        process.wait()
        print("\nRecording stopped.", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Recording error: {e}", file=sys.stderr)
        return False


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using the existing transcribe.py script.

    Args:
        audio_path: Path to the audio file

    Returns:
        Transcribed text
    """
    # Find the transcribe script relative to this script
    script_dir = Path(__file__).parent
    transcribe_script = script_dir / "transcribe.py"

    if not transcribe_script.exists():
        # Fallback to .aura/scripts/transcribe.py
        transcribe_script = Path(".aura/scripts/transcribe.py")

    print("Transcribing audio...", file=sys.stderr)

    result = subprocess.run(
        [sys.executable, str(transcribe_script), audio_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Transcription error: {result.stderr}", file=sys.stderr)
        return ""

    return result.stdout.strip()


def generate_title(transcript: str) -> str:
    """Generate a title from the transcript using the existing generate_title.py script.

    Args:
        transcript: The transcription text

    Returns:
        Generated title in kebab-case
    """
    # Find the generate_title script relative to this script
    script_dir = Path(__file__).parent
    title_script = script_dir / "generate_title.py"

    if not title_script.exists():
        # Fallback to .aura/scripts/generate_title.py
        title_script = Path(".aura/scripts/generate_title.py")

    print("Generating title...", file=sys.stderr)

    result = subprocess.run(
        [sys.executable, str(title_script), "--text", transcript],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Fallback to timestamp-based title
        print(f"Title generation failed, using timestamp", file=sys.stderr)
        return f"memo-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    return result.stdout.strip()


def create_queue_directory(title: str, queue_dir: Path) -> Path:
    """Create the queue directory for this memo.

    Handles title collisions by appending a counter.

    Args:
        title: The generated title
        queue_dir: Base queue directory path

    Returns:
        Path to the created memo directory
    """
    queue_dir.mkdir(parents=True, exist_ok=True)

    memo_dir = queue_dir / title

    # Handle collision: append counter
    if memo_dir.exists():
        counter = 1
        while (queue_dir / f"{title}-{counter}").exists():
            counter += 1
        memo_dir = queue_dir / f"{title}-{counter}"

    memo_dir.mkdir(parents=True, exist_ok=True)
    return memo_dir


def main():
    parser = argparse.ArgumentParser(
        description="Record voice memos with automatic transcription",
        epilog="Examples:\n"
               "  python .aura/scripts/record_memo.py\n"
               "  python .aura/scripts/record_memo.py --duration 120\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--duration",
        type=int,
        help="Recording duration limit in seconds (default: no limit, stop with Ctrl+C)"
    )

    parser.add_argument(
        "--queue-dir",
        type=str,
        default=".aura/queue",
        help="Queue directory path (default: .aura/queue)"
    )

    args = parser.parse_args()

    # Check prerequisites
    check_prerequisites()

    # Create temporary file for recording
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        temp_audio_path = tmp.name

    try:
        # Step 1: Record audio
        if not record_audio(temp_audio_path, args.duration):
            print("Recording failed.", file=sys.stderr)
            sys.exit(1)

        # Check if we actually recorded something
        if not os.path.exists(temp_audio_path) or os.path.getsize(temp_audio_path) == 0:
            print("No audio recorded.", file=sys.stderr)
            sys.exit(1)

        # Step 2: Transcribe
        transcript = transcribe_audio(temp_audio_path)

        if not transcript:
            print("Transcription failed or empty.", file=sys.stderr)
            # Still save the audio with timestamp title
            title = f"memo-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            transcript = "(transcription failed)"
        else:
            # Step 3: Generate title
            title = generate_title(transcript)

        # Step 4: Create queue directory
        queue_dir = Path(args.queue_dir)
        memo_dir = create_queue_directory(title, queue_dir)

        # Step 5: Move audio and write transcript
        import shutil
        audio_dest = memo_dir / "audio.wav"
        shutil.move(temp_audio_path, audio_dest)

        transcript_dest = memo_dir / "transcript.txt"
        with open(transcript_dest, "w", encoding="utf-8") as f:
            f.write(transcript)

        # Success output
        print(f"\nMemo saved to: {memo_dir}", file=sys.stderr)
        print(f"  Audio: {audio_dest}", file=sys.stderr)
        print(f"  Transcript: {transcript_dest}", file=sys.stderr)

        # Output the memo directory path to stdout for scripting
        print(str(memo_dir))

    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up temp file if it still exists
        if os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)


if __name__ == "__main__":
    main()
