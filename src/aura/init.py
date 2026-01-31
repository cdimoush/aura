"""Aura initialization logic."""

import json
import shutil
import subprocess
from pathlib import Path

from aura.config import DOT_AURA_CFG, DOT_AURA_FOLDERS

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

    # .aura/ contents (except visions/, plans/ which are created empty)
    aura_source = AURA_ROOT / ".aura"
    if aura_source.exists():
        for src in aura_source.glob("**/*"):
            if src.is_file() and src.name != ".gitkeep":
                rel = src.relative_to(aura_source)
                # Skip blacklisted directories (visions, plans)
                if rel.parts and rel.parts[0] in DOT_AURA_CFG["blacklist"]:
                    continue
                # Skip .env file (contains secrets)
                if rel.name == ".env" and not DOT_AURA_CFG["copy_env"]:
                    continue
                dst = Path(".aura") / rel
                files.append((src, dst))

    # .claude/templates/ contents
    templates_source = AURA_ROOT / ".claude" / "templates"
    if templates_source.exists():
        for src in templates_source.glob("**/*"):
            if src.is_file():
                rel = src.relative_to(templates_source)
                dst = Path(".claude/templates") / rel
                files.append((src, dst))

    # .claude/skills/ contents (subdirectories with SKILL.md)
    skills_source = AURA_ROOT / ".claude" / "skills"
    if skills_source.exists():
        for src in skills_source.glob("**/*"):
            if src.is_file():
                rel = src.relative_to(skills_source)
                dst = Path(".claude/skills") / rel
                files.append((src, dst))

    # .claude/settings.json (handled separately for merging)
    # Not included here - merged in init_aura()

    return files


def get_session_start_hook():
    """Return the SessionStart hook configuration for aura.md injection."""
    return {
        "matcher": "",
        "hooks": [
            {
                "type": "command",
                "command": 'cat "$CLAUDE_PROJECT_DIR"/.aura/aura.md 2>/dev/null || true',
            }
        ],
    }


def merge_settings_json(target_path: Path, force: bool = False) -> dict:
    """Merge aura's SessionStart hook into existing settings.json.

    Returns dict with 'action' key: 'created', 'merged', 'skipped', or 'error'.
    """
    result = {"path": str(target_path)}

    # Load existing settings if present
    existing = {}
    if target_path.exists():
        try:
            existing = json.loads(target_path.read_text())
        except json.JSONDecodeError:
            if not force:
                result["action"] = "error"
                result["message"] = "Invalid JSON in existing settings.json"
                return result
            # Force mode: overwrite invalid JSON
            existing = {}

    # Ensure hooks.SessionStart exists
    if "hooks" not in existing:
        existing["hooks"] = {}
    if "SessionStart" not in existing["hooks"]:
        existing["hooks"]["SessionStart"] = []

    # Check if our hook already exists
    our_hook = get_session_start_hook()
    hook_exists = False
    for hook in existing["hooks"]["SessionStart"]:
        if hook.get("hooks") == our_hook.get("hooks"):
            hook_exists = True
            break

    if hook_exists and not force:
        result["action"] = "skipped"
        result["message"] = "Aura hook already present"
        return result

    if not hook_exists:
        existing["hooks"]["SessionStart"].append(our_hook)
        result["action"] = "merged" if target_path.exists() else "created"
    else:
        result["action"] = "skipped"
        result["message"] = "Aura hook already present (force=True)"
        return result

    # Write merged settings
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(existing, indent=2) + "\n")

    return result


def init_aura(force: bool = False, dry_run: bool = False):
    """Initialize Aura in current directory.

    Raises:
        BeadsNotFoundError: If beads CLI not available.
    """
    results = {"created": [], "skipped": [], "errors": [], "warnings": []}

    # Check beads availability upfront
    if not check_beads_available():
        raise BeadsNotFoundError(BEADS_INSTALL_MSG)

    # Create folder structure
    for folder in DOT_AURA_FOLDERS:
        folder_path = Path(".aura") / folder
        gitkeep_path = folder_path / ".gitkeep"

        if dry_run:
            if not folder_path.exists():
                results["created"].append(str(folder_path) + "/")
            continue

        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            if not gitkeep_path.exists():
                gitkeep_path.touch()
                results["created"].append(str(folder_path) + "/")
        except Exception as e:
            results["errors"].append(f"{folder_path}: {e}")

    # Copy template files
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

    # Merge settings.json with SessionStart hook
    settings_path = Path(".claude/settings.json")
    if dry_run:
        if settings_path.exists():
            results["created"].append(f"{settings_path} (merge hook)")
        else:
            results["created"].append(str(settings_path))
    else:
        merge_result = merge_settings_json(settings_path, force)
        if merge_result["action"] == "created":
            results["created"].append(str(settings_path))
        elif merge_result["action"] == "merged":
            results["created"].append(f"{settings_path} (merged hook)")
        elif merge_result["action"] == "skipped":
            results["skipped"].append(str(settings_path))
        elif merge_result["action"] == "error":
            results["errors"].append(f"{settings_path}: {merge_result.get('message', 'unknown error')}")

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
