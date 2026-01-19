# Feature: Slash Command Coherence

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 3 - Command Completion
**Priority**: P4

## Overview

Ensure all 12 slash commands are fully functional with complete agent-facing markdown instructions. Each command should provide a coherent logical workflow that Claude Code can execute without hitting dead ends or stubs.

## User Story

As a developer using Claude Code with Aura, I need every slash command to provide complete instructions so that I can use the full Aura workflow without encountering incomplete features or placeholder content.

## Current State

- Some commands may have incomplete instructions
- Some commands may reference non-existent scripts or files
- Workflows may have dead ends or unclear next steps

## Target State

- All 12 commands have complete markdown workflows
- Each command executes its intended purpose fully
- No TODO, stub, or placeholder content
- Logical flow from invocation to completion

## Commands to Verify/Complete

### Aura Commands (8)

| Command | Purpose | Status |
|---------|---------|--------|
| `/aura.prime` | Load project context for Claude Code | TBD |
| `/aura.record` | Record voice memo to queue | TBD |
| `/aura.transcribe` | Transcribe audio file to text | TBD |
| `/aura.act` | Transcribe audio and act on request | TBD |
| `/aura.epic` | Break vision into ordered specs | TBD |
| `/aura.feature` | Plan and implement a feature | TBD |
| `/aura.tickets` | Convert epic to beads tasks | TBD |
| `/aura.implement` | Implement from ticket or spec | TBD |

### Beads Commands (4)

| Command | Purpose | Status |
|---------|---------|--------|
| `/beads.status` | Show project status via Beads | TBD |
| `/beads.ready` | Show tasks ready to work on | TBD |
| `/beads.start` | Start working on a task | TBD |
| `/beads.done` | Mark a task as complete | TBD |

## Acceptance Scenarios

1. **Given** `/aura.act` is invoked with a valid audio file, **When** processing completes, **Then** output directory contains: original audio, transcription, and deliverables

2. **Given** `/aura.epic` is invoked with a description, **When** processing completes, **Then** epic document with phases is created in specs/

3. **Given** `/aura.tickets` is invoked on an epic, **When** processing completes, **Then** beads tasks are created from the epic

4. **Given** any beads command is invoked, **When** execution completes, **Then** the command interacts correctly with beads task system

## Tasks

### 1. Audit All Commands
- [ ] Read each command file in `.claude/commands/`
- [ ] Document current state (complete, partial, stub)
- [ ] Identify missing instructions or dead ends
- [ ] Note script references that may be broken

### 2. Complete Aura Commands
- [ ] `/aura.prime` - Ensure context loading instructions complete
- [ ] `/aura.record` - Ensure recording workflow complete
- [ ] `/aura.transcribe` - Ensure transcription instructions reference scripts correctly
- [ ] `/aura.act` - Ensure full workflow from audio to deliverables
- [ ] `/aura.epic` - Ensure epic creation workflow complete
- [ ] `/aura.feature` - Ensure feature planning workflow complete
- [ ] `/aura.tickets` - Ensure beads task creation workflow complete
- [ ] `/aura.implement` - Ensure implementation workflow complete

### 3. Complete Beads Commands
- [ ] `/beads.status` - Ensure `bd` integration correct
- [ ] `/beads.ready` - Ensure ready task query works
- [ ] `/beads.start` - Ensure task start workflow complete
- [ ] `/beads.done` - Ensure task completion workflow complete

### 4. Verify Script References
- [ ] Ensure `/aura.transcribe` references `.aura/scripts/transcribe.py`
- [ ] Ensure `/aura.act` references both transcribe and title scripts
- [ ] Verify all referenced scripts exist and work

### 5. Test Each Command
- [ ] Invoke each command in Claude Code
- [ ] Verify command executes without dead ends
- [ ] Document any issues discovered

## Acceptance Criteria

- [ ] All 8 aura commands have complete markdown workflows
- [ ] All 4 beads commands interact correctly with beads task system
- [ ] No command has TODO, stub, or placeholder content
- [ ] Each command has logical flow from start to completion
- [ ] Script references are correct and scripts exist

## Dependencies

- Chore: Installation Cleanup (needs working installation)
- Feature: Beads Integration (beads commands need working beads)

## Blocks

- Chore: Tron Verification Test (needs working commands to test)

## Related Requirements

From spec.md:
- FR-012: All 12 commands MUST be fully functional agent-facing markdown instructions
- FR-013: Aura commands (8)
- FR-014: Beads commands (4)
- FR-015: Each command MUST provide coherent logical flow
- FR-016: `/aura.transcribe` and `/aura.act` MUST reference Python scripts
- FR-017: `/aura.prime` MUST load project context

## Edge Cases

- What if transcription API is unavailable? → Clear error message
- What if audio file exceeds 25MB? → Guidance on chunking/compression
- What if OPENAI_API_KEY not set? → Clear error indicating missing key
- What if beads task doesn't exist? → Appropriate error from beads
