#!/usr/bin/env python3
"""Display status of audio files in the queue directory."""

import os
import sys
from pathlib import Path

# Supported audio formats
SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}
QUEUE_DIR = Path("queue")


def format_size(bytes_size: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            if unit == "B":
                return f"{bytes_size} {unit}"
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def get_audio_duration_ms(path: str) -> int | None:
    """Get the duration of an audio file in milliseconds.

    Returns None if duration extraction fails.
    Tries ffprobe first (faster), falls back to pydub.
    """
    # Try ffprobe first (more reliable and faster)
    try:
        import subprocess
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
                path
            ],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            duration_seconds = float(result.stdout.strip())
            return int(duration_seconds * 1000)
    except Exception:
        pass

    # Fall back to pydub if ffprobe not available
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(path)
        return len(audio)
    except Exception:
        # If both fail, return None
        return None


def format_duration(milliseconds: int) -> str:
    """Format milliseconds to a readable duration string."""
    total_seconds = milliseconds / 1000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    if minutes == 0:
        return f"{seconds}s"
    elif minutes < 60:
        return f"{minutes}m {seconds}s"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"


def find_queue_files() -> list[Path]:
    """Find all audio files in the queue directory.

    Returns a list of Path objects, sorted by modification time (newest first).
    """
    if not QUEUE_DIR.exists():
        return []

    files = []
    for ext in SUPPORTED_FORMATS:
        files.extend(QUEUE_DIR.glob(f"*.{ext}"))

    # Sort by modification time, newest first
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def estimate_processing_time(total_duration_ms: int) -> str:
    """Estimate transcription processing time.

    Based on typical Whisper performance: ~25-35% of audio duration for serial processing,
    or ~10-20% with parallelization (2-4 parallel processes).
    """
    total_seconds = total_duration_ms / 1000

    # Serial processing estimate (25-35% of audio duration)
    serial_min_seconds = int(total_seconds * 0.25)
    serial_max_seconds = int(total_seconds * 0.35)

    # Parallel processing estimate (10-20% with good parallelization)
    parallel_min_seconds = int(total_seconds * 0.10)
    parallel_max_seconds = int(total_seconds * 0.20)

    # Ensure minimum of 1 minute estimate
    if serial_max_seconds < 60:
        serial_min_seconds = 1
        serial_max_seconds = 1
    else:
        serial_min_seconds = max(1, serial_min_seconds // 60)
        serial_max_seconds = max(1, serial_max_seconds // 60)

    if parallel_max_seconds < 60:
        parallel_min_seconds = 1
        parallel_max_seconds = 1
    else:
        parallel_min_seconds = max(1, parallel_min_seconds // 60)
        parallel_max_seconds = max(1, parallel_max_seconds // 60)

    return f"{parallel_min_seconds}-{parallel_max_seconds} minutes (with parallelization) or {serial_min_seconds}-{serial_max_seconds} minutes (serial)"


def display_empty_queue():
    """Display the empty queue message."""
    print("Queue is empty ✓\n")
    print("Add audio files to queue/ to get started:")
    print("  - Drag and drop voice memos into queue/")
    print("  - Use system hotkey (coming soon)")
    print("  - Use /record_memo command (coming soon)\n")
    print("Supported formats: m4a, mp3, wav, mp4, mpeg, mpga, webm")


def display_queue_status(files: list[Path]):
    """Display the queue status with file details."""
    print("Queue Status")
    print("=" * 50 + "\n")

    # Calculate statistics
    total_size = sum(f.stat().st_size for f in files)
    file_count = len(files)

    print(f"Files queued: {file_count}")
    print(f"Total size: {format_size(total_size)}")

    # Try to calculate duration
    total_duration_ms = 0
    duration_available = True
    file_durations = []

    for file_path in files:
        duration_ms = get_audio_duration_ms(str(file_path))
        file_durations.append(duration_ms)
        if duration_ms is not None:
            total_duration_ms += duration_ms
        else:
            duration_available = False

    if duration_available and total_duration_ms > 0:
        print(f"Total duration: ~{format_duration(total_duration_ms)}")
    elif duration_available:
        print("Total duration: 0 seconds")
    else:
        print("Total duration: Unable to calculate (install pydub for duration info)")

    # Display file list
    print(f"\nFiles:")
    for i, file_path in enumerate(files, 1):
        file_size = file_path.stat().st_size
        size_str = format_size(file_size)

        duration_ms = file_durations[i - 1]
        if duration_ms is not None:
            duration_str = format_duration(duration_ms)
            print(f"  {i}. {file_path.name} ({size_str}, {duration_str})")
        else:
            print(f"  {i}. {file_path.name} ({size_str}, unknown duration)")

    # Display processing time estimate
    if duration_available and total_duration_ms > 0:
        print(f"\nEstimated processing time: {estimate_processing_time(total_duration_ms)}")

    # Display helpful tips
    print("\n" + "=" * 50)

    if file_count > 10:
        print("Large queue detected. Processing will happen in parallel.")

    if file_count > 0:
        # Check for quick files
        quick_files = sum(1 for d in file_durations if d is not None and d < 60000)
        if quick_files == file_count and file_count > 0:
            print("Quick files detected. Processing should be fast.")

    print(f"\nReady to process? Run: /process_queue")


def main():
    """Main entry point."""
    # Check if queue directory exists
    if not QUEUE_DIR.exists():
        print("Queue directory not found at: queue/\n")
        print("Creating queue/ directory...")
        QUEUE_DIR.mkdir(exist_ok=True)
        display_empty_queue()
        return

    # Find all audio files in queue
    files = find_queue_files()

    if not files:
        display_empty_queue()
    else:
        display_queue_status(files)


if __name__ == "__main__":
    main()
