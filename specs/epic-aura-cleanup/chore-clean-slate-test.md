# Chore: Clean Slate Test

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 0 - Clean Slate Baseline
**Priority**: P0 (must run first)

## Overview

Before making any changes, establish a known-clean starting point by resetting the development environment completely. This documents what currently works (or doesn't) and provides a baseline for measuring improvement.

## Purpose

This phase answers: "What is the current state of installation?" It:
1. **Resets** all cached/installed state that might mask issues
2. **Documents** which installation steps currently work or fail
3. **Establishes** a baseline for comparison after fixes

## Why This Matters

Development environments accumulate state. A command might work because of cached dependencies, globally installed packages, or leftover configuration. By resetting to clean slate, we see what a new user would actually experience.

## Tasks

### 1. Reset UV Environment
- [ ] Remove existing virtual environment: `rm -rf .venv/`
- [ ] Clear uv cache: `uv cache clean`
- [ ] Verify no aura package cached: `uv pip list` should not show aura

### 2. Reset Beads (if testing beads integration)
- [ ] Check current beads installation: `which bd` and `bd --version`
- [ ] Document beads version for reproducibility
- [ ] Optionally uninstall/reinstall to verify beads installation instructions

### 3. Document Current README Instructions
- [ ] Read current README.md installation section
- [ ] Copy exact commands documented
- [ ] Note any ambiguities or missing steps

### 4. Execute Current Installation Steps
- [ ] Run each documented command in order
- [ ] Record output of each command
- [ ] Note which commands succeed vs fail
- [ ] Document any error messages verbatim

### 5. Test Current Functionality
- [ ] Run `aura --version` - record result
- [ ] Run `aura init --dry-run` - record result
- [ ] Run `aura check` (if exists) - record result
- [ ] Note any undocumented steps that were needed

### 6. Document Findings
- [ ] Create baseline report with:
  - Commands that worked
  - Commands that failed (with errors)
  - Undocumented steps required
  - Missing prerequisites discovered

## Environment Reset Commands

```bash
# From aura repository root
cd /Users/conner/dev/aura

# Remove virtual environment
rm -rf .venv/

# Clear uv cache
uv cache clean

# Verify clean state
ls -la .venv/  # Should not exist
uv pip list    # Should show nothing or error

# Check beads state
which bd
bd --version
```

## Expected Baseline Report Format

```markdown
## Clean Slate Baseline Report
Date: YYYY-MM-DD

### Environment
- OS: macOS/Ubuntu version
- uv version: X.Y.Z
- Python version: X.Y.Z
- Beads version: X.Y.Z (or "not installed")

### README Installation Steps Tested
1. `command` - SUCCESS/FAIL
   - Output: ...
   - Error (if any): ...

2. `command` - SUCCESS/FAIL
   ...

### Issues Discovered
- Issue 1: description
- Issue 2: description

### Undocumented Steps Required
- Step 1: what was needed but not documented
- Step 2: ...

### Recommendations
- Fix 1: ...
- Fix 2: ...
```

## Acceptance Criteria

- [ ] `.venv/` directory removed
- [ ] uv cache cleared
- [ ] Current README installation steps executed
- [ ] Results documented (success/fail for each step)
- [ ] Baseline report created

## Dependencies

None - this is Phase 0.

## Blocks

- All subsequent phases depend on understanding what currently works

## Agent Instructions

When executing this chore, the agent should:

1. **Actually run the reset commands** - don't just document them
2. **Follow README exactly** - don't use knowledge of the codebase to "help"
3. **Record everything** - every command, every output, every error
4. **Be honest** - if something fails, document the failure clearly
5. **Don't fix yet** - this phase is about documenting, not fixing

The goal is to experience what a new user would experience.
