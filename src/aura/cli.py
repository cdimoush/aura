"""Aura CLI entry point."""

import click

from aura.init import init_aura, BeadsNotFoundError


@click.group()
@click.version_option()
def main():
    """Aura - Agentic workflow layer for codebases."""
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--dry-run", is_flag=True, help="Show what would be created")
def init(force, dry_run):
    """Initialize Aura in current directory."""
    if dry_run:
        click.echo("Dry run - no files will be created:\n")
    else:
        click.echo("Initializing Aura...\n")

    try:
        results = init_aura(force=force, dry_run=dry_run)
    except BeadsNotFoundError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)

    for warning in results.get("warnings", []):
        click.echo(f"  Warning: {warning}", err=True)

    for path in results["created"]:
        prefix = "Would create" if dry_run else "Created"
        click.echo(f"  {prefix} {path}")

    for path in results["skipped"]:
        click.echo(f"  Skipped {path} (already exists)")

    for error in results["errors"]:
        click.echo(f"  Error: {error}", err=True)

    if not dry_run:
        created = len(results["created"])
        skipped = len(results["skipped"])
        click.echo(f"\nAura initialized! ({created} created, {skipped} skipped)")
        click.echo("Start Claude Code - aura context loads automatically via SessionStart hook.")


@main.command()
def check():
    """Verify prerequisites are installed."""
    import os
    import shutil
    from pathlib import Path

    # Verify .aura directory exists first
    aura_dir = Path(".aura")
    if not aura_dir.exists():
        click.echo("Error: .aura directory not found.", err=True)
        click.echo("Run 'aura init' to initialize Aura in this directory.", err=True)
        raise SystemExit(1)

    # Load .aura/.env if it exists
    env_file = Path(".aura/.env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)

    checks = [
        ("Python 3.12+", lambda: True),  # We're running, so yes
        ("Claude Code", lambda: shutil.which("claude") is not None),
        ("OPENAI_API_KEY", lambda: os.environ.get("OPENAI_API_KEY") is not None),
        ("ffmpeg", lambda: shutil.which("ffmpeg") is not None),
        ("beads (bd)", lambda: shutil.which("bd") is not None),
    ]

    click.echo("Checking prerequisites...\n")
    issues = 0

    for name, check_fn in checks:
        try:
            if check_fn():
                click.echo(f"  + {name}")
            else:
                click.echo(f"  - {name}")
                issues += 1
        except Exception:
            click.echo(f"  - {name}")
            issues += 1

    if issues:
        click.echo(f"\n{issues} issues found. Some features may not work.")
        raise SystemExit(1)
    else:
        click.echo("\nAll prerequisites met!")


def get_dir_size(path) -> int:
    """Get total size of directory in bytes."""
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"


@main.command()
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.option("--dry-run", is_flag=True, help="Show what would be deleted")
@click.option("--keep-memos", is_flag=True, help="Preserve .aura/memo directory")
def remove(force, dry_run, keep_memos):
    """Remove Aura from current directory."""
    import shutil
    from pathlib import Path

    # Find all Aura-related files/directories
    targets = []

    # .aura directory
    aura_dir = Path(".aura")
    if aura_dir.exists():
        if keep_memos:
            # List individual subdirs except memo
            for item in aura_dir.iterdir():
                if item.name != "memo":
                    targets.append(item)
        else:
            targets.append(aura_dir)

    # .claude/skills aura directories
    skills_dir = Path(".claude/skills")
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir() and item.name.startswith("aura."):
                targets.append(item)

    # .beads directory
    beads_dir = Path(".beads")
    if beads_dir.exists():
        targets.append(beads_dir)

    if not targets:
        click.echo("No Aura files found in current directory.")
        return

    # Show what will be deleted
    click.echo("The following will be removed:\n")
    for target in targets:
        try:
            size = get_dir_size(target) if target.is_dir() else target.stat().st_size
            size_str = format_size(size)
        except (OSError, PermissionError):
            size_str = "unknown"
        click.echo(f"  {target} ({size_str})")

    if dry_run:
        click.echo("\nDry run - nothing was deleted.")
        return

    # Confirm deletion
    if not force:
        click.echo()
        if not click.confirm("Proceed with removal?"):
            click.echo("Cancelled.")
            return

    # Delete
    errors = []
    for target in targets:
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            click.echo(f"  Removed {target}")
        except Exception as e:
            errors.append(f"{target}: {e}")
            click.echo(f"  Error removing {target}: {e}", err=True)

    if errors:
        click.echo(f"\nCompleted with {len(errors)} errors.", err=True)
        raise SystemExit(1)
    else:
        click.echo("\nAura removed successfully!")


if __name__ == "__main__":
    main()
