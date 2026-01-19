# Chore: Installation Cleanup

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 1 - Installation Foundation
**Priority**: P1 (blocks all other work)

## Overview

Standardize Aura installation on a single, proven method. Remove all competing installation documentation and ensure the documented path works reliably.

## Current State

- Multiple installation methods may be documented
- No verification that documented steps actually work
- Environment setup may require manual intervention

## Target State

- Exactly ONE installation method documented (git clone + uv-based setup)
- Installation completes in 5 or fewer terminal commands
- No manual file editing required
- Verification command confirms success

## Tasks

### 1. Audit Current Documentation
- [ ] Review README.md for all installation instructions
- [ ] Identify any competing/conflicting methods
- [ ] Document what currently works vs what doesn't

### 2. Define Canonical Installation
- [ ] Document prerequisites: `uv`, `git`, Beads (`bd`)
- [ ] Write step-by-step installation commands
- [ ] Ensure all commands work on fresh macOS and Ubuntu

### 3. Update README.md
- [ ] Remove all non-canonical installation methods
- [ ] Add Beads prerequisite with link to https://github.com/steveyegge/beads
- [ ] Document Beads installation options:
  - `npm install -g @beads/bd`
  - `brew install steveyegge/beads/bd`
  - `go install github.com/steveyegge/beads/cmd/bd@latest`
- [ ] Add verification step: `aura --version`

### 4. Fix Environment Setup
- [ ] Ensure `.env.example` exists with all required variables
- [ ] Document copy command: `cp .aura/.env.example .aura/.env`
- [ ] Verify OPENAI_API_KEY handling for transcription

### 5. Test Installation
- [ ] Test on fresh macOS environment
- [ ] Test on fresh Ubuntu environment
- [ ] Document any edge cases discovered

## Acceptance Criteria

- [ ] README contains exactly ONE installation method
- [ ] Installation requires 5 or fewer commands (excluding Beads prerequisite)
- [ ] `aura --version` displays version after installation
- [ ] No manual file editing required (environment via `.env.example` copy)
- [ ] Fresh clone + documented steps succeeds 100% of the time

## Dependencies

None - this is the foundation.

## Blocks

- Feature: Beads Integration (needs working `aura` command)
- Feature: Slash Command Coherence (needs working installation)
- Chore: Tron Verification Test (needs working installation)

## Related Requirements

From spec.md:
- FR-001: Exactly ONE documented installation method
- FR-002: Beads as prerequisite with link
- FR-003: 5 or fewer terminal commands
- FR-004: No manual file editing
- FR-005: Verification command
