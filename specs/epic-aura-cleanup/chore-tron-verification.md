# Chore: Tron Verification Test

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 4 - Validation
**Priority**: P3

## Overview

Create a comprehensive verification test that proves the complete Aura workflow works. The Tron demo serves as both validation (proving the system works) and onboarding documentation (showing users how to use it).

## Purpose

The Tron test answers the question: "Does Aura actually work?" It provides:
1. **Proof** - Verifiable evidence that installation and commands function
2. **Documentation** - Step-by-step example of real-world usage
3. **Regression Protection** - Can be re-run after changes to verify nothing broke

## User Story

As a developer evaluating Aura, I need a verification test I can run to confirm the installation succeeded and see all features working together in a realistic scenario.

## Current State

- `tests/tron/` fixture exists but may be incomplete
- Instructions may not be documented
- End-to-end verification may not be possible

## Target State

- Complete Tron test runnable outside Aura source directory
- Documented instructions in README or dedicated file
- Test exercises key slash commands
- Clear success/failure criteria

## Test Workflow

### Setup
1. Create fresh directory: `mkdir /tmp/tron-test && cd /tmp/tron-test`
2. Initialize git: `git init`
3. Run Aura init: `aura init`

### Verify Structure
4. Check `.aura/` directory exists with scripts
5. Check `.claude/commands/` exists with all 12 commands
6. Check `.beads/` initialized (if bd available)

### Configure
7. Copy environment: `cp .aura/.env.example .aura/.env`
8. Add OPENAI_API_KEY (if testing transcription)

### Test Commands
9. Invoke `/aura.prime` - verify context loads
10. Invoke `/beads.status` - verify beads integration
11. (Optional) Test transcription with sample audio

### Cleanup
12. Remove test directory: `rm -rf /tmp/tron-test`

## Tasks

### 1. Document Test Instructions
- [ ] Create `tests/tron/INSTRUCTIONS.md` with step-by-step guide
- [ ] Include prerequisites checklist
- [ ] Include expected output for each step
- [ ] Include troubleshooting section

### 2. Create Verification Script (Optional)
- [ ] Consider `aura check` command that verifies setup
- [ ] Check for all required files
- [ ] Check for required CLI tools (bd, uv)
- [ ] Report pass/fail status

### 3. Update Tests/Tron Fixture
- [ ] Ensure `tests/tron/` has any test-specific files needed
- [ ] Add `AGENTS.md` if needed for Claude Code context
- [ ] Document fixture purpose in README

### 4. Add to Main README
- [ ] Add "Verification" section to main README
- [ ] Link to Tron test instructions
- [ ] Provide quick verification command

### 5. Test End-to-End
- [ ] Run full test workflow on macOS
- [ ] Run full test workflow on Ubuntu
- [ ] Document any platform-specific issues

## Acceptance Scenarios

1. **Given** Aura is installed, **When** user creates `/tmp/tron-test` and runs `aura init`, **Then** all template files are copied successfully

2. **Given** a project initialized with `aura init`, **When** user invokes `/aura.prime` in Claude Code, **Then** project context is loaded correctly

3. **Given** an initialized project with `.aura/.env` configured with OPENAI_API_KEY, **When** user runs `/aura.transcribe` on an audio file, **Then** transcription completes successfully

4. **Given** an initialized project, **When** user views `/beads.status`, **Then** task status is displayed (or appropriate message if no tasks)

## Acceptance Criteria

- [ ] Tron test can be run in `/tmp/tron-test` (outside aura source)
- [ ] Instructions documented in `tests/tron/INSTRUCTIONS.md`
- [ ] Test exercises: `aura init`, `/aura.prime`, `/beads.status`
- [ ] Success/failure is unambiguous
- [ ] Can be completed in under 10 minutes

## Dependencies

- Chore: Installation Cleanup (needs working installation)
- Feature: Beads Integration (needs working beads)
- Feature: Slash Command Coherence (needs working commands)

## Blocks

None - this is the final validation.

## Related Requirements

From spec.md:
- FR-018: Aura MUST include verification test (Tron demo)
- FR-019: Verification test MUST be runnable outside Aura source directory
- FR-020: Verification test instructions MUST be documented

## Edge Cases

- What if user runs test inside Aura source directory? → Warning or different behavior
- What if previous test left artifacts? → Instructions for cleanup
- What if some optional features fail? → Clear indication of what's optional vs required
