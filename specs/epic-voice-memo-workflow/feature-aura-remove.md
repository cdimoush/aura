# Feature: Aura Remove Command

## Overview

Create `aura remove` CLI command that cleanly removes all Aura files from a directory, with confirmation prompts to prevent accidental deletion.

## User Story

As a developer, when I no longer want Aura in a project, I want to remove all Aura files cleanly so that my project returns to its original state without manual file hunting.

## Context

Currently, there's no way to uninstall Aura from a project. Users would need to manually identify and delete:
- `.aura/` directory
- `.claude/commands/aura.*.md` and `beads.*.md` files
- `.beads/` directory (if Beads was initialized)

This command provides a clean removal path and makes Aura feel less "permanent" which lowers adoption friction.

## Command Specification

**CLI Command**: `aura remove`

**Location**: Add to `src/aura/cli.py`

**Options**:
- `--force` - Skip confirmation prompt
- `--dry-run` - Show what would be deleted without deleting
- `--keep-output` - Remove Aura but preserve `.aura/output/` (processed memos)

## Implementation

### CLI Command Structure

Add to `src/aura/cli.py`:

```python
@main.command()
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.option("--dry-run", is_flag=True, help="Show what would be deleted")
@click.option("--keep-output", is_flag=True, help="Preserve .aura/output directory")
def remove(force, dry_run, keep_output):
    """Remove Aura from current directory."""
    import shutil
    from pathlib import Path

    # Find all Aura-related files/directories
    targets = []

    # .aura directory
    aura_dir = Path(".aura")
    if aura_dir.exists():
        if keep_output:
            # List individual subdirs except output
            for item in aura_dir.iterdir():
                if item.name != "output":
                    targets.append(item)
        else:
            targets.append(aura_dir)

    # .claude/commands aura and beads files
    commands_dir = Path(".claude/commands")
    if commands_dir.exists():
        for pattern in ["aura.*.md", "beads.*.md"]:
            targets.extend(commands_dir.glob(pattern))

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
        size = get_dir_size(target) if target.is_dir() else target.stat().st_size
        size_str = format_size(size)
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


def get_dir_size(path: Path) -> int:
    """Get total size of directory in bytes."""
    return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}TB"
```

## User Workflow

### Basic Removal

```bash
cd ~/projects/my-app
aura remove
```

Output:
```
The following will be removed:

  .aura (2.3MB)
  .claude/commands/aura.act.md (1.2KB)
  .claude/commands/aura.epic.md (1.5KB)
  .claude/commands/aura.feature.md (1.8KB)
  .claude/commands/aura.implement.md (1.4KB)
  .claude/commands/aura.prime.md (1.1KB)
  .claude/commands/aura.record.md (1.3KB)
  .claude/commands/aura.transcribe.md (1.2KB)
  .claude/commands/aura.act.md (1.4KB)
  .claude/commands/beads.done.md (900B)
  .claude/commands/beads.ready.md (850B)
  .claude/commands/beads.start.md (920B)
  .claude/commands/beads.status.md (880B)
  .beads (450KB)

Proceed with removal? [y/N]:
```

### Dry Run

```bash
aura remove --dry-run
```

Shows what would be deleted without actually deleting.

### Force Removal

```bash
aura remove --force
```

Skips confirmation prompt (useful for scripts).

### Keep Output

```bash
aura remove --keep-output
```

Removes Aura but preserves `.aura/output/` with processed memos.

## Implementation Tasks

- [ ] Add `remove` command to `src/aura/cli.py`
- [ ] Implement file/directory discovery logic
- [ ] Implement size calculation and formatting
- [ ] Implement confirmation prompt
- [ ] Implement deletion logic with error handling
- [ ] Add `--force`, `--dry-run`, `--keep-output` flags
- [ ] Test on various project states (partial install, full install, etc.)
- [ ] Add to README.md
- [ ] Update CLAUDE.md

## Acceptance Criteria

- [ ] `aura remove` lists all Aura-related files and directories
- [ ] Command shows file sizes for directories
- [ ] Confirmation prompt prevents accidental deletion
- [ ] `--force` skips confirmation
- [ ] `--dry-run` shows what would be deleted without deleting
- [ ] `--keep-output` preserves `.aura/output/` directory
- [ ] Error messages are clear and actionable
- [ ] Partial failures report which files couldn't be deleted
- [ ] Exit code 0 on success, 1 on error
- [ ] Works in projects with partial Aura installation

## Testing Plan

### Test 1: Full Removal

```bash
# Setup
cd /tmp/aura-test
mkdir test-project && cd test-project
aura init

# Remove
aura remove --force

# Verify
test ! -d .aura && echo "✓ .aura removed"
test ! -f .claude/commands/aura.*.md && echo "✓ commands removed"
test ! -d .beads && echo "✓ .beads removed"
```

### Test 2: Dry Run

```bash
# Setup
cd /tmp/aura-test/test-project
aura init

# Dry run
aura remove --dry-run

# Verify nothing deleted
test -d .aura && echo "✓ .aura still exists"
```

### Test 3: Keep Output

```bash
# Setup
cd /tmp/aura-test/test-project
aura init
mkdir -p .aura/output/memo-1
echo "test" > .aura/output/memo-1/transcript.md

# Remove with keep-output
aura remove --keep-output --force

# Verify
test ! -d .aura/scripts && echo "✓ scripts removed"
test -d .aura/output/memo-1 && echo "✓ output preserved"
```

### Test 4: Partial Installation

```bash
# Setup with only some files
mkdir test-partial && cd test-partial
mkdir -p .aura/scripts
touch .aura/scripts/test.py

# Remove
aura remove --force

# Verify
test ! -d .aura && echo "✓ partial install removed"
```

### Test 5: Permission Errors

```bash
# Setup
mkdir test-perms && cd test-perms
aura init
chmod 000 .aura  # Make read-only

# Try remove
aura remove --force
# Should report error but not crash

# Cleanup
chmod 755 .aura
```

## Edge Cases

1. **No Aura Installed**: Message "No Aura files found"
2. **Permission Denied**: Report error, continue with other files
3. **Symlinks**: Follow and delete symlink, not target
4. **Nested Projects**: Only remove from current directory
5. **Git Repository**: Don't touch `.git/` or other unrelated files
6. **Empty .claude/commands/**: Don't remove entire directory, just Aura files

## Documentation Updates

### README.md

Add removal section:

```markdown
## Removing Aura

To remove Aura from a project:

```bash
cd your-project

# Preview what will be removed
aura remove --dry-run

# Remove Aura
aura remove

# Or force removal without confirmation
aura remove --force

# Keep processed memos in .aura/output
aura remove --keep-output
```

This removes:
- `.aura/` directory (except output if --keep-output)
- `.claude/commands/aura.*.md` files
- `.claude/commands/beads.*.md` files
- `.beads/` directory
```

### CLAUDE.md

Add to troubleshooting:

```markdown
## Uninstalling Aura

If Aura needs to be removed from a project, use:

```bash
aura remove [--force] [--dry-run] [--keep-output]
```

This is useful for:
- Testing fresh installs
- Removing from projects that no longer need Aura
- Cleaning up after experiments
```

## Dependencies

- None (can be implemented independently)
- Useful after: All other features (provides clean exit path)

## Future Enhancements

1. **Selective Removal**:
   ```bash
   aura remove --scripts-only
   aura remove --commands-only
   aura remove --beads-only
   ```

2. **Backup Before Removal**:
   ```bash
   aura remove --backup
   # Creates .aura-backup.tar.gz before removing
   ```

3. **Restore Command**:
   ```bash
   aura restore .aura-backup.tar.gz
   ```

4. **Clean vs Purge**:
   - `aura clean` - Remove generated files (queue, output)
   - `aura purge` - Remove everything including scripts

5. **Interactive Selection**:
   ```bash
   aura remove --interactive
   # Shows checklist, user selects what to remove
   ```

## Notes

- Consider adding confirmation even with `--force` if large output directory exists
- Log removal to `.aura-removal.log` for audit trail
- Consider warning if unsaved work exists in queue
- Future: Integration with git (check for uncommitted Aura-related changes)
