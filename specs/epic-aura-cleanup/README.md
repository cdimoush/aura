# Epic: Aura Installation Cleanup

## Epic Overview

This epic addresses the foundational issues with Aura's initial setup that create friction for new users. The current state has multiple documented installation methods creating confusion, some slash commands lack complete implementation details, and there's no verification test that proves a fresh clone works correctly.

The goal is to establish a solid foundation: a single, proven installation method, complete slash command implementations with coherent workflows, proper Beads integration, and a Tron demo that serves as both validation and onboarding documentation. When complete, a new user should be able to install Aura and use all 12 slash commands without hitting any dead ends.

This epic is critical because Aura is being developed using Aura (dogfooding). If the foundation is broken, development velocity suffers. A clean, working installation also enables external contributors and early adopters.

## Specs in This Epic

### Phase 0: Clean Slate Baseline
- [ ] [Chore: Clean Slate Test](./chore-clean-slate-test.md) - Reset environment completely, document current installation state

### Phase 1: Installation Foundation
- [ ] [Chore: Installation Cleanup](./chore-installation-cleanup.md) - Standardize on single installation method, remove dead documentation

### Phase 2: Core Integration
- [ ] [Feature: Beads Integration](./feature-beads-integration.md) - Ensure Beads is properly required and initialized

### Phase 3: Command Completion
- [ ] [Feature: Slash Command Coherence](./feature-slash-commands.md) - Complete all 12 slash commands with full workflows

### Phase 4: Validation
- [ ] [Chore: Tron Verification Test](./chore-tron-verification.md) - Create end-to-end verification with documented instructions

### Phase 5: Agent Verification
- [ ] [Chore: Agent Installation Test](./chore-agent-installation-test.md) - Agent follows README instructions from clean state, proves they work

## Execution Order

### Phase 0: Clean Slate Baseline
**Goal**: Establish a known-clean starting point and document what currently works/fails.

Execute in order:
1. [Chore: Clean Slate Test](./chore-clean-slate-test.md) - Reset uv environment, uninstall aura, test current state

**Actions**:
- Remove existing `.venv/` in aura directory
- Run `uv cache clean` to clear cached packages
- Uninstall global aura if present
- Attempt current README installation steps
- Document what works and what fails

**Success Criteria**:
- Environment is completely reset
- Current installation state documented (working/broken steps)
- Baseline established for measuring improvement

**Agent Testing Breakpoint**: The agent must execute these reset steps and document findings before proceeding.

---

### Phase 1: Installation Foundation
**Goal**: A single, working installation path that any new user can follow.

Execute in order:
1. [Chore: Installation Cleanup](./chore-installation-cleanup.md) - Must establish the foundation before anything else can be verified

**Success Criteria**:
- README documents exactly ONE installation method (git clone + uv)
- Installation completes in 5 or fewer commands (excluding Beads prerequisite)
- `aura --version` works after installation
- All competing installation documentation removed

**User Testing Breakpoint**: Have someone unfamiliar with the project follow the README installation instructions. They should succeed on first attempt.

---

### Phase 2: Core Integration
**Goal**: Beads integration is required and properly initialized.

Execute in order:
1. [Feature: Beads Integration](./feature-beads-integration.md) - Beads is the task management backbone; must work before slash commands can reference it

**Success Criteria**:
- `aura init` fails with clear error if `bd` not installed
- `aura init` creates properly initialized `.beads/` directory when `bd` is available
- Documentation includes Beads as explicit prerequisite with installation link

**User Testing Breakpoint**: Test `aura init` both with and without Beads installed. Error message should be actionable.

---

### Phase 3: Command Completion
**Goal**: All 12 slash commands are fully functional with no stubs.

Execute in order:
1. [Feature: Slash Command Coherence](./feature-slash-commands.md) - Each command provides complete agent-facing instructions

**Success Criteria**:
- All 8 aura commands have complete markdown workflows
- All 4 beads commands interact correctly with beads task system
- No command has TODO, stub, or placeholder content
- Each command has logical flow from start to completion

**User Testing Breakpoint**: Invoke each command in Claude Code and verify it executes its intended function without hitting dead ends.

---

### Phase 4: Validation
**Goal**: End-to-end verification that proves everything works together.

Execute in order:
1. [Chore: Tron Verification Test](./chore-tron-verification.md) - Creates the proof that installation and commands work

**Success Criteria**:
- Tron test can be run in `/tmp/tron-test` (outside aura source)
- Instructions are documented and followable
- Test exercises installation, init, and key slash commands
- Success/failure is unambiguous

**User Testing Breakpoint**: Run the Tron test yourself after completing all previous phases. It should pass completely.

---

### Phase 5: Agent Verification
**Goal**: Prove the installation instructions work by having the agent follow them from scratch.

Execute in order:
1. [Chore: Agent Installation Test](./chore-agent-installation-test.md) - Agent resets environment and follows README exactly

**Actions**:
- Agent removes `.venv/`, clears uv cache
- Agent follows README installation instructions verbatim
- Agent runs `aura --version` to verify
- Agent runs `aura init` in `/tmp/aura-agent-test`
- Agent verifies all expected files created
- Agent invokes key slash commands

**Success Criteria**:
- Agent successfully completes installation following only README
- No undocumented steps required
- All verification commands pass
- Agent can use aura to initialize a new project

**Agent Testing Breakpoint**: This is the final proof. If the agent cannot follow the instructions, they need revision.

---

## Path Dependencies Diagram

```
Phase 0: Clean Slate Baseline
    |
    | (establishes known-clean state)
    v
Phase 1: Installation Foundation
    |
    | (must have working aura command)
    v
Phase 2: Core Integration
    |
    | (must have beads integration)
    v
Phase 3: Command Completion
    |
    | (must have working commands)
    v
Phase 4: Validation (Tron Test)
    |
    | (proves manual workflow works)
    v
Phase 5: Agent Verification
    |
    | (proves agent can follow instructions)
    v
  DONE

Critical Path: Clean Slate -> Installation -> Beads -> Commands -> Tron -> Agent Test
```

## Success Metrics

- [ ] Clean slate test documents current state accurately
- [ ] New user completes installation in under 5 commands
- [ ] Fresh clone and install succeeds 100% on macOS/Ubuntu
- [ ] `aura init` creates all expected files (17+ across 3 directories)
- [ ] All 12 slash commands fully functional (8 aura + 4 beads)
- [ ] Tron verification test passes end-to-end
- [ ] Zero stubs or incomplete commands
- [ ] Agent can follow README installation instructions without assistance
- [ ] Agent can initialize and use aura in a fresh project

## Future Enhancements

Ideas that came up during planning but are out of scope:

1. `uv tool install aura` distribution (requires PyPI publishing)
2. Windows platform support
3. Support for agents other than Claude Code (Cursor, Copilot)
4. GUI or web interface
5. Runtime configuration system (`.aura/config.md`)
6. Context injection via project tags
7. Multi-agent orchestration

## Reference

- Original spec: [spec.md](./spec.md)
- Feature branch: `002-aura-install-cleanup`
- Created: 2026-01-18
