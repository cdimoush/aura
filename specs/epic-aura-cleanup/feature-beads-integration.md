# Feature: Beads Integration

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 2 - Core Integration
**Priority**: P2

## Overview

Ensure Beads is properly integrated as a required component of Aura. Installation should fail with a clear error if Beads (`bd`) is not available, and `aura init` should properly initialize the `.beads/` directory.

## User Story

As a developer setting up a new project with Aura, I need Beads to be correctly installed and initialized so that I can use the task management features that power the Aura workflow.

## Current State

- Beads may be optional or have unclear integration
- Error handling for missing `bd` may be insufficient
- `.beads/` initialization may not be complete

## Target State

- Beads is a documented prerequisite
- `aura init` requires `bd` CLI to be available
- Clear error message when `bd` not installed
- `.beads/` directory properly initialized with config.yaml and README.md

## Acceptance Scenarios

1. **Given** Beads CLI (`bd`) is installed, **When** user runs `aura init`, **Then** `.beads/` directory is initialized with config.yaml and README.md

2. **Given** Beads CLI is NOT installed, **When** user attempts `aura init`, **Then** clear error message indicates beads must be installed first with installation instructions

3. **Given** a fresh Aura installation, **When** user runs `bd --version`, **Then** beads version is displayed (confirming beads is installed)

## Tasks

### 1. Implement Beads Check in Init
- [ ] Add check for `bd` CLI availability in `src/aura/init.py`
- [ ] Return clear error message with installation instructions if not found
- [ ] Error should include all three installation options:
  - `npm install -g @beads/bd`
  - `brew install steveyegge/beads/bd`
  - `go install github.com/steveyegge/beads/cmd/bd@latest`

### 2. Implement Beads Initialization
- [ ] Call `bd init` as part of `aura init` process
- [ ] Verify `.beads/` directory created with expected files
- [ ] Handle case where `.beads/` already exists (respect `--force` flag)

### 3. Add --no-beads Flag Behavior
- [ ] Document that `--no-beads` skips beads initialization
- [ ] Ensure warning is displayed when using `--no-beads`
- [ ] Slash commands that require beads should warn if `.beads/` missing

### 4. Update Documentation
- [ ] Add Beads prerequisite to README.md installation section
- [ ] Link to https://github.com/steveyegge/beads
- [ ] Document expected `.beads/` directory structure

### 5. Test Integration
- [ ] Test `aura init` with `bd` installed
- [ ] Test `aura init` without `bd` installed
- [ ] Test `aura init --no-beads`
- [ ] Verify `.beads/` directory contents

## Acceptance Criteria

- [ ] `aura init` fails with clear error if `bd` not installed
- [ ] Error message includes installation instructions
- [ ] `.beads/` directory created with config.yaml and README.md when `bd` available
- [ ] `--no-beads` flag works correctly with warning
- [ ] Documentation updated with Beads prerequisite

## Dependencies

- Chore: Installation Cleanup (needs working `aura` command)

## Blocks

- Feature: Slash Command Coherence (beads commands need working integration)
- Chore: Tron Verification Test (needs beads to verify)

## Related Requirements

From spec.md:
- FR-008: `aura init` MUST require beads CLI; fail with clear error if not installed
- FR-014: Beads commands (4): `/beads.status`, `/beads.ready`, `/beads.start`, `/beads.done`

## Edge Cases

- What if `bd init` fails? → Show error, suggest manual initialization
- What if `.beads/` exists but is corrupted? → `--force` should reinitialize
- What if user has old version of `bd`? → Check minimum version if critical
