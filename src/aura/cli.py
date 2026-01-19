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
@click.option("--no-beads", is_flag=True, help="Skip beads initialization")
def init(force, dry_run, no_beads):
    """Initialize Aura in current directory."""
    if dry_run:
        click.echo("Dry run - no files will be created:\n")
    else:
        click.echo("Initializing Aura...\n")

    try:
        results = init_aura(force=force, dry_run=dry_run, no_beads=no_beads)
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
        click.echo("Run /aura.prime in Claude Code to get started.")


@main.command()
def check():
    """Verify prerequisites are installed."""
    import os
    import shutil
    from pathlib import Path

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


if __name__ == "__main__":
    main()
