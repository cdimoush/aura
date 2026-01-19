# Feature Specification: Aura Installation Cleanup

**Feature Branch**: `002-aura-install-cleanup`
**Created**: 2026-01-18
**Status**: Draft
**Input**: User description: "A brief clean up or refactor or alignment of the initial aura setup. Single method of download that actually works and can be proven to work. Use current aura setup to fix aura, remove uv environment, prove fresh install after clone is clean. Beads installed correctly from scratch. All slash commands and scripts work with each other. No dead ends. Solid foundation. Tron test with instructions to move outside aura directory, run aura init, develop game as demo."

## Clarifications

### Session 2026-01-18

- Q: Is Beads optional or required for Aura? → A: Beads is required - installation fails or warns if beads (`bd`) not present
- Q: What is the correct GitHub URL for Beads? → A: https://github.com/steveyegge/beads
- Q: Should Beads be installed before or as part of Aura? → A: Prerequisite - user installs Beads first, then Aura
- Q: Should all 12 slash commands be fully functional? → A: Yes, all 12 commands must be fully functional (no stubs)
- Q: What does "fully functional" mean for slash commands? → A: Complete agent-facing markdown instructions that provide logical workflows/recipes for agentic software development. NOT automated Python scripts - Claude Code reads and executes the instructions.
- Q: How to install Beads? → A: `npm install -g @beads/bd` OR `brew install steveyegge/beads/bd` OR `go install github.com/steveyegge/beads/cmd/bd@latest`

---

## Context

**What is Aura?**: An agentic workflow layer that can be initialized in any repository. It provides:
- `.aura/` directory: Scripts (transcription, title generation) and configuration
- `.beads/` directory: Git-native task management with persistent agent memory (required)
- `.claude/commands/` directory: Slash commands for Claude Code integration

**Current Location**: `~/dev/aura/` (independent Git repository)

**Problem**: The initial Aura setup has multiple documented installation methods creating confusion, some slash commands lack implementation details, and there's no verification test that proves a fresh clone works correctly.

**Solution**: Standardize on a single installation method, ensure all components work together, and create a comprehensive verification test.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Fresh Install from Clone (Priority: P1)

A new user clones the Aura repository and follows the documented installation instructions. After completing the steps, they have a working Aura installation that can initialize new projects.

**Why this priority**: This is the foundational capability - if a new user cannot install Aura successfully, nothing else matters. All other features depend on installation working correctly.

**Independent Test**: Clone Aura to a fresh location, follow the documented instructions exactly, verify `aura init` works in a test directory.

**Acceptance Scenarios**:

1. **Given** a machine with `uv`, `git`, and Beads (`bd`) installed, **When** user runs the documented clone and install commands, **Then** the `aura` command is available in the terminal
2. **Given** Aura is installed, **When** user runs `aura --version`, **Then** version number is displayed
3. **Given** Aura is installed, **When** user runs `aura init` in an empty directory, **Then** `.aura/`, `.claude/commands/`, and `.beads/` directories are created with all expected files

---

### User Story 2 - Beads Installation Verification (Priority: P2)

After installing Aura, the user verifies that Beads is correctly installed and functional. Beads is a required component of Aura - installation should fail or warn if beads is not available.

**Why this priority**: Beads integration provides the task management foundation that makes Aura valuable. Without beads, Aura loses its core workflow capabilities.

**Independent Test**: Verify beads CLI (`bd`) is available after Aura installation, and `aura init` creates properly initialized `.beads/` directory.

**Acceptance Scenarios**:

1. **Given** a fresh Aura installation, **When** user runs `bd --version`, **Then** beads version is displayed (confirming beads is installed)
2. **Given** beads CLI (`bd`) is installed, **When** user runs `aura init`, **Then** `.beads/` directory is initialized with config.yaml and README.md
3. **Given** beads CLI is NOT installed, **When** user attempts `aura init`, **Then** clear error message indicates beads must be installed first

---

### User Story 3 - Tron Demo Workflow (Priority: P3)

A user follows the Tron demo instructions to verify the complete Aura workflow: create a new project outside the Aura directory, initialize it with `aura init`, and develop a simple game to demonstrate slash commands working together.

**Why this priority**: The Tron test serves as both validation and documentation - it proves the system works and shows users how to use it in a real scenario.

**Independent Test**: Follow the Tron instructions end-to-end in a clean environment to verify all slash commands work.

**Acceptance Scenarios**:

1. **Given** Aura is installed, **When** user creates a new directory `/tmp/tron-test` and runs `aura init`, **Then** all template files are copied successfully
2. **Given** a project initialized with `aura init`, **When** user invokes `/aura.prime` in Claude Code, **Then** project context is loaded correctly
3. **Given** an initialized project with `.aura/.env` configured with OPENAI_API_KEY, **When** user runs `/aura.transcribe` on an audio file, **Then** transcription completes successfully
4. **Given** an initialized project, **When** user views `/beads.status`, **Then** task status is displayed

---

### User Story 4 - Slash Command Coherence (Priority: P4)

All 12 slash commands are fully functional with no stubs or dead ends. Each command completes its intended purpose.

**Why this priority**: Complete command coverage ensures users can rely on the full Aura workflow without encountering incomplete features.

**Independent Test**: Invoke each of the 12 slash commands and verify they complete their intended function.

**Acceptance Scenarios**:

1. **Given** any of the 8 aura commands, **When** user invokes it with valid input, **Then** the command executes successfully and produces expected output
2. **Given** any of the 4 beads commands, **When** user invokes it, **Then** the command interacts correctly with beads task system
3. **Given** `/aura.act` is invoked with a valid audio file, **When** processing completes, **Then** output directory contains: original audio, transcription, and deliverables
4. **Given** `/aura.epic` is invoked with a description, **When** processing completes, **Then** epic document with phases is created
5. **Given** `/aura.tickets` is invoked on an epic, **When** processing completes, **Then** beads tasks are created from the epic

---

### Edge Cases

- What happens when user has an existing `.aura/` directory and runs `aura init` without `--force`?
  - Expected: Skip existing files, report what was skipped
- What happens when OPENAI_API_KEY is not set and user runs transcription?
  - Expected: Clear error message indicating the missing API key
- What happens when audio file exceeds 25MB limit?
  - Expected: Clear error message with guidance (chunking or compression)
- What happens when user runs `aura init` inside the Aura source directory?
  - Expected: Warning or error - should not re-initialize source repo

---

## Requirements *(mandatory)*

### Functional Requirements

**Installation**
- **FR-001**: Aura MUST have exactly ONE documented installation method (git clone + uv-based setup)
- **FR-002**: Aura documentation MUST include Beads as a prerequisite with link to https://github.com/steveyegge/beads
- **FR-003**: Installation MUST complete with 5 or fewer terminal commands (excluding Beads prerequisite)
- **FR-004**: Installation MUST NOT require manual file editing (environment variables set via command or `.env.example` copy)
- **FR-005**: System MUST provide a verification command that confirms installation succeeded

**Initialization (`aura init`)**
- **FR-006**: `aura init` MUST copy all files from `.aura/` template to target directory
- **FR-007**: `aura init` MUST copy all files from `.claude/commands/` to target directory
- **FR-008**: `aura init` MUST require beads CLI (`bd`) to be available; fail with clear error if not installed
- **FR-009**: `aura init` MUST support `--force` flag to overwrite existing files
- **FR-010**: `aura init` MUST support `--dry-run` flag to preview changes without writing
- **FR-011**: `aura init` MUST NOT copy `.venv/`, `.env`, `queue/`, or `output/` directories

**Slash Commands**
- **FR-012**: All 12 slash commands MUST be fully functional agent-facing markdown instructions (complete workflows/recipes for Claude Code to execute - NOT automated Python scripts)
- **FR-013**: Aura commands (8): `/aura.prime`, `/aura.record`, `/aura.transcribe`, `/aura.act`, `/aura.epic`, `/aura.feature`, `/aura.tickets`, `/aura.implement`
- **FR-014**: Beads commands (4): `/beads.status`, `/beads.ready`, `/beads.start`, `/beads.done`
- **FR-015**: Each command MUST provide a coherent logical flow with no dead ends or incomplete instructions
- **FR-016**: `/aura.transcribe` and `/aura.act` instructions MUST reference the Python scripts in `.aura/scripts/`
- **FR-017**: `/aura.prime` MUST load project context for Claude Code agents

**Verification Test**
- **FR-018**: Aura MUST include a verification test that proves fresh install works (Tron demo)
- **FR-019**: Verification test MUST be runnable outside the Aura source directory
- **FR-020**: Verification test instructions MUST be documented in README or dedicated test file

---

### Key Entities

- **Aura Installation**: The installed Aura CLI tool on the user's machine, providing the `aura` command
- **Initialized Project**: Any directory where `aura init` has been run, containing `.aura/`, `.claude/commands/`, and `.beads/`
- **Template Files**: Source files in Aura repository that get copied during initialization (`.aura/**/*`, `.claude/commands/*.md`)
- **Slash Command**: A Claude Code command defined in `.claude/commands/<name>.md` with YAML frontmatter and markdown instructions

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New user can complete Aura installation in under 5 commands
- **SC-002**: Fresh clone and install succeeds 100% of the time on documented supported platforms (macOS, Ubuntu)
- **SC-003**: `aura init` in a new directory creates all expected files (17+ files across 3 directories)
- **SC-004**: All 12 slash commands (8 aura + 4 beads) are fully functional and execute without errors
- **SC-005**: Tron verification test can be completed end-to-end by following documented instructions
- **SC-006**: Zero stubs or incomplete commands - every command fully implements its intended purpose

---

## Assumptions

- Users have `uv` package manager installed (documented prerequisite)
- Users have `git` installed (documented prerequisite)
- Users have Beads CLI (`bd`) installed as a prerequisite from https://github.com/steveyegge/beads
- macOS and Ubuntu are the supported platforms (no Windows support in initial version)
- Claude Code is the only supported agent (no other LLM integrations)
- OpenAI API key is required for transcription features
- FFmpeg is required for audio processing (pydub dependency)

---

## Out of Scope

- `uv tool install aura` distribution method (future work, requires PyPI publishing)
- Windows platform support
- Support for agents other than Claude Code
- GUI or web interface
- Runtime configuration system (`.aura/config.md` mentioned but not implemented)
- Advanced features: context injection via project tags, multi-agent orchestration

---

## Verification Test: Tron Demo

The Tron test serves as both validation and onboarding documentation. It demonstrates a complete workflow:

1. **Setup**: Create a fresh directory outside Aura source
2. **Initialize**: Run `aura init` to scaffold the project
3. **Configure**: Copy `.aura/.env.example` to `.aura/.env` and add API key
4. **Verify**: Run verification commands to confirm setup
5. **Demo**: Use slash commands to develop a simple light-bike game concept

Expected output: A working initialized project demonstrating all Aura capabilities.

---

## Tags

`aura` `installation` `cleanup` `refactor` `verification` `tron-test` `beads` `slash-commands`
