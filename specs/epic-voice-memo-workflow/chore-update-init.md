# Chore: Update Init with New Features

## Overview

Ensure `aura init` distributes all new voice memo scripts and commands developed in this epic to target projects.

## Context

Throughout this epic, we've created:
- `record_memo.py` script (Phase 1)
- `/aura.process` command (Phase 2)
- `/cyborg.process` command (Phase 3)

These need to be included in the template files that `aura init` copies to target projects.

## Current Init Behavior

From `src/aura/init.py`, the init process:

1. **Scripts**: Copies all `.aura/scripts/*.py` from Aura repo to target
2. **Commands**: Copies all `.claude/commands/*.md` from Aura repo to target
3. **Configuration**: Copies `.aura/.env.example`, `.aura/.gitignore`
4. **Beads**: Runs `bd init` if available and not skipped

**Key insight**: Init uses glob patterns, so adding new files automatically includes them. This chore is about verification and documentation updates.

## Verification Tasks

### 1. Verify Script Distribution

Check that new scripts are distributed:

```bash
# In Aura repo root
ls .aura/scripts/

# Expected files:
# - transcribe.py (existing)
# - generate_title.py (existing)
# - record_memo.py (NEW)
# - requirements.txt (existing)
```

Test distribution:

```bash
cd /tmp/test-aura-init
mkdir test-project && cd test-project

# Dry run to see what will be copied
uv run aura init --dry-run | grep record_memo

# Actual init
uv run aura init

# Verify
ls .aura/scripts/
test -f .aura/scripts/record_memo.py && echo "✓ record_memo.py distributed"
```

- [ ] Verify `record_memo.py` is in Aura's `.aura/scripts/`
- [ ] Test `aura init --dry-run` lists it
- [ ] Test `aura init` copies it
- [ ] Test in Tron fixture: `cd tests/tron && uv run aura init`

### 2. Verify Command Distribution

Check that new commands are distributed:

```bash
# In Aura repo root
ls .claude/commands/

# Expected NEW files:
# - aura.process.md
# - cyborg.process.md (if created in Phase 3)
```

Test distribution:

```bash
cd /tmp/test-aura-init/test-project
uv run aura init

# Verify
ls .claude/commands/aura.process.md
test -f .claude/commands/aura.process.md && echo "✓ aura.process distributed"
```

- [ ] Verify `aura.process.md` is in Aura's `.claude/commands/`
- [ ] Test `aura init` copies it
- [ ] Verify in Claude Code: `/aura.process` is available
- [ ] If Cyborg command created, verify `cyborg.process.md` distribution

### 3. Verify Configuration

Ensure `.aura/.gitignore` includes new directories:

```bash
# Check .aura/.gitignore
cat .aura/.gitignore

# Should include:
# queue/
# output/
# .env
# .venv/
```

- [ ] Verify `queue/` is git-ignored
- [ ] Verify `output/` is git-ignored (if not already)
- [ ] Test that queued memos aren't committed

### 4. Update Requirements

Ensure `requirements.txt` is complete:

```bash
# Check .aura/scripts/requirements.txt
cat .aura/scripts/requirements.txt

# Should include all dependencies:
# openai
# pydub
# python-dotenv
# (any new dependencies from record_memo.py)
```

- [ ] Verify all required packages listed
- [ ] Test clean install: `uv pip install -r .aura/scripts/requirements.txt`
- [ ] Document any system dependencies (SoX, ffmpeg)

## Documentation Updates

### 1. README.md

Update Quick Start section to include new workflow:

```markdown
## Quick Start

### 4. Record and Process a Voice Memo

#### Using Python Script (Recommended)

```bash
# Activate Aura scripts environment
source .aura/.venv/bin/activate

# Record a memo
python .aura/scripts/record_memo.py

# ... speak your idea ...
# Press Ctrl+C to stop

# Process the memo
# In Claude Code:
/aura.process <memo-title>
```

#### Using SoX Directly (Alternative)

```bash
# In Claude Code:
/aura.record

# ... speak your idea ...
# Press Ctrl+C to stop

/aura.process <memo-title>
```
```

- [ ] Update Quick Start section
- [ ] Add recording workflow diagram
- [ ] Document `/aura.process` command
- [ ] Document `/cyborg.process` command (if applicable)

### 2. Command Reference

Add new commands to README:

```markdown
## Available Commands

### Voice Memo Workflow

- `/aura.record` - Record audio using SoX (requires sox installed)
- `/aura.process` - Process queued memos into formatted output
- `/aura.transcribe` - Transcribe an audio file (existing)
- `/aura.act` - Transcribe and act on audio file (existing)

### Cyborg Integration

- `/cyborg.process` - Process queued memos into brain notes
```

- [ ] Add command reference section
- [ ] Document each command with description
- [ ] Link to detailed docs if needed

### 3. CLAUDE.md

Update agent instructions with new workflows:

```markdown
## Voice Memo Workflow

When users record voice memos, the workflow is:

1. **Record**: `python .aura/scripts/record_memo.py`
   - Records audio via SoX
   - Transcribes immediately
   - Generates title
   - Saves to `.aura/queue/<title>/`

2. **Process (Aura)**: `/aura.process <title>`
   - Detects user intent
   - Formats as markdown
   - Moves to `.aura/output/<title>/`

3. **Process (Cyborg)**: `/cyborg.process <title>`
   - Converts to brain note
   - Adds tags
   - Moves to `brain/<title>.md`

Agents should suggest appropriate processing based on context.
```

- [ ] Document new workflows
- [ ] Update agent instructions
- [ ] Add examples for common scenarios

### 4. .claude/commands Files

Ensure command files have complete instructions:

**aura.process.md**:
- [ ] Frontmatter with allowed-tools
- [ ] Clear step-by-step instructions
- [ ] Examples for each intent type
- [ ] Error handling guidance

**cyborg.process.md** (if created):
- [ ] Frontmatter with allowed-tools
- [ ] Brain note format instructions
- [ ] Tag generation examples
- [ ] Integration with regenerate

## Testing Matrix

Test init in various scenarios:

| Scenario | Expected Behavior | Status |
|----------|-------------------|--------|
| Fresh directory | All files copied | [ ] |
| Existing .aura/ | Skips existing, adds new | [ ] |
| Force flag | Overwrites all | [ ] |
| No Beads | Aura files only | [ ] |
| Dry run | Shows files, doesn't create | [ ] |
| Tron fixture | Works as integration test | [ ] |

- [ ] Execute all test scenarios
- [ ] Document any failures or issues
- [ ] Verify file counts match expected

## Verification Script

Create a verification script to test init completeness:

```bash
#!/bin/bash
# test-init-completeness.sh

set -e

TEST_DIR="/tmp/aura-init-test-$$"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

echo "Testing aura init in fresh directory..."

# Init
uv run aura init

# Verify scripts
echo "Checking scripts..."
test -f .aura/scripts/record_memo.py || { echo "✗ record_memo.py missing"; exit 1; }
test -f .aura/scripts/transcribe.py || { echo "✗ transcribe.py missing"; exit 1; }
test -f .aura/scripts/generate_title.py || { echo "✗ generate_title.py missing"; exit 1; }
test -f .aura/scripts/requirements.txt || { echo "✗ requirements.txt missing"; exit 1; }
echo "✓ Scripts verified"

# Verify commands
echo "Checking commands..."
test -f .claude/commands/aura.process.md || { echo "✗ aura.process.md missing"; exit 1; }
test -f .claude/commands/aura.record.md || { echo "✗ aura.record.md missing"; exit 1; }
# Add more command checks
echo "✓ Commands verified"

# Verify config
echo "Checking configuration..."
test -f .aura/.env.example || { echo "✗ .env.example missing"; exit 1; }
test -f .aura/.gitignore || { echo "✗ .gitignore missing"; exit 1; }
echo "✓ Configuration verified"

# Verify gitignore contents
echo "Checking .gitignore..."
grep -q "queue/" .aura/.gitignore || { echo "✗ queue/ not in .gitignore"; exit 1; }
grep -q "output/" .aura/.gitignore || { echo "✗ output/ not in .gitignore"; exit 1; }
echo "✓ .gitignore verified"

echo "✓ All checks passed!"

# Cleanup
cd /
rm -rf "$TEST_DIR"
```

- [ ] Create verification script
- [ ] Run script and verify all checks pass
- [ ] Add to `tests/` directory
- [ ] Document usage in testing docs

## Acceptance Criteria

- [ ] `aura init` includes `record_memo.py` in `.aura/scripts/`
- [ ] `aura init` includes `/aura.process` in `.claude/commands/`
- [ ] `aura init` includes `/cyborg.process` if applicable
- [ ] `.aura/.gitignore` includes `queue/` and `output/`
- [ ] `requirements.txt` is complete and tested
- [ ] README.md documents new workflow
- [ ] CLAUDE.md has updated instructions
- [ ] All test scenarios pass
- [ ] Tron fixture verification passes
- [ ] Fresh init in external project works end-to-end

## Integration Test

Full end-to-end test:

```bash
# 1. Fresh init
cd /tmp
mkdir e2e-test && cd e2e-test
uv run aura init

# 2. Setup environment
cp .aura/.env.example .aura/.env
echo "OPENAI_API_KEY=sk-test" >> .aura/.env
cd .aura && uv venv && source .venv/bin/activate
uv pip install -r scripts/requirements.txt
cd ..

# 3. Record memo (short test)
python .aura/scripts/record_memo.py --duration 5
# Speak test memo

# 4. Verify queue
ls .aura/queue/
test -d .aura/queue/* || { echo "✗ No memo in queue"; exit 1; }

# 5. Process memo (in Claude Code session)
# /aura.process --all

# 6. Verify output
ls .aura/output/
test -f .aura/output/*/transcript.md || { echo "✗ No processed output"; exit 1; }

echo "✓ End-to-end test passed!"
```

- [ ] Execute integration test
- [ ] Document any issues encountered
- [ ] Verify full workflow works as expected

## Dependencies

- Requires: All Phase 1-4 features complete
- Blocks: Final epic completion and user adoption

## Future Enhancements

1. **Init Templates**: Support custom templates or profiles
   ```bash
   aura init --profile minimal  # Just scripts, no beads
   aura init --profile full      # Everything
   ```

2. **Update Command**: Sync scripts from global Aura
   ```bash
   aura update  # Re-sync scripts and commands
   ```

3. **Version Check**: Warn if local copy is outdated
   ```bash
   aura check --version
   # Local scripts: v0.1.0
   # Available: v0.2.0
   # Run 'aura update' to upgrade
   ```

4. **Init Hooks**: Post-init scripts for custom setup
   ```bash
   # .aura/hooks/post-init.sh
   # Runs after aura init completes
   ```

## Notes

- The glob-based approach makes this largely automatic
- Focus on verification and documentation
- Testing is critical to ensure nothing is missed
- Consider creating a CI check that verifies init completeness
