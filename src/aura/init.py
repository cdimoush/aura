"""Aura initialization logic."""

import shutil
import subprocess
from pathlib import Path

from aura.config import DOT_AURA_CFG, DOT_CLAUDE_CFG

BEADS_INSTALL_MSG = """
Beads CLI (bd) is required but not installed.

Install beads:
  npm install -g @beads/bd
"""


class BeadsNotFoundError(Exception):
    """Raised when beads CLI is not available."""

    pass


def check_beads_available() -> bool:
    """Check if beads CLI (bd) is available."""
    return shutil.which("bd") is not None


def get_aura_root() -> Path:
    """Find aura package root directory.

    When developing: traverse up from init.py
    init.py is at aura/src/aura/init.py
    aura root is 3 levels up
    """
    init_path = Path(__file__).resolve()
    return init_path.parent.parent.parent


AURA_ROOT = get_aura_root()


def get_template_files():
    """Return list of (src, dst) tuples for all template files."""
    files = []

    # .aura/ contents (except queue/, output/)
    aura_source = AURA_ROOT / ".aura"
    if aura_source.exists():
        for src in aura_source.glob("**/*"):
            if src.is_file() and src.name != ".gitkeep":
                rel = src.relative_to(aura_source)
                # Skip queue, output, and .venv directories
                if rel.parts and rel.parts[0] in DOT_AURA_CFG["blacklist"]:
                    continue
                # Skip .env file (contains secrets)
                if rel.name == ".env" and not DOT_AURA_CFG["copy_env"]:
                    continue
                dst = Path(".aura") / rel
                files.append((src, dst))

    # .claude/commands/ contents
    claude_source = AURA_ROOT / ".claude" / "commands"
    if claude_source.exists():
        for src in claude_source.glob("*.md"):
            dst = Path(".claude/commands") / src.name
            files.append((src, dst))

    return files


def init_aura(force: bool = False, dry_run: bool = False):
    """Initialize Aura in current directory.

    Raises:
        BeadsNotFoundError: If beads CLI not available.
    """
    results = {"created": [], "skipped": [], "errors": [], "warnings": []}

    # Check beads availability upfront
    if not check_beads_available():
        raise BeadsNotFoundError(BEADS_INSTALL_MSG)

    for src, dst in get_template_files():
        if dry_run:
            if dst.exists() and not force:
                results["skipped"].append(str(dst))
            else:
                results["created"].append(str(dst))
            continue

        try:
            if dst.exists() and not force:
                results["skipped"].append(str(dst))
                continue

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dst)
            results["created"].append(str(dst))
        except Exception as e:
            results["errors"].append(f"{dst}: {e}")

    # Initialize beads
    if not dry_run:
        beads_dir = Path(".beads")
        if not beads_dir.exists() or force:
            try:
                subprocess.run(["bd", "init"], check=True, capture_output=True)
                results["created"].append(".beads/ (via bd init)")
            except subprocess.CalledProcessError as e:
                results["errors"].append(f".beads/: bd init failed: {e}")

    return results
