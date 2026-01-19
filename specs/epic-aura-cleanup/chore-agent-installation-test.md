# Chore: Agent Installation Test

**Epic**: [Aura Installation Cleanup](./README.md)
**Phase**: 5 - Agent Verification
**Priority**: P1 (final validation)

## Overview

The ultimate test of installation documentation: can the Claude Code agent follow the README instructions from a clean slate and successfully install and use Aura? This is the final proof that the documentation is complete and accurate.

## Purpose

This phase answers: "Are the instructions good enough for an agent to follow?" It:
1. **Validates** that documentation is complete (no missing steps)
2. **Proves** instructions are unambiguous (agent doesn't need to guess)
3. **Confirms** the full workflow works end-to-end

## Why Agent Testing Matters

If an AI agent can follow the instructions successfully, a human almost certainly can too. Agents are:
- **Literal** - they follow instructions exactly as written
- **Unforgiving** - they don't fill in gaps with intuition
- **Reproducible** - the test can be repeated identically

## Prerequisites

Before running this test:
- [ ] Phase 0-4 must be complete
- [ ] All installation cleanup changes merged
- [ ] README reflects final installation method
- [ ] All slash commands complete

## Test Protocol

### Step 1: Environment Reset
```bash
# Agent executes these commands
cd /Users/conner/dev/aura
rm -rf .venv/
uv cache clean
```

### Step 2: Follow README Installation
Agent reads README.md and executes ONLY the documented installation commands.

**Rules**:
- Agent must not use any knowledge beyond what's in README
- Agent must execute commands exactly as documented
- Agent must report any ambiguity or missing information
- Agent must not "help" by adding undocumented steps

### Step 3: Verify Installation
```bash
aura --version
# Expected: version number displayed

aura check
# Expected: all checks pass (if command exists)
```

### Step 4: Test Initialization
```bash
mkdir -p /tmp/aura-agent-test
cd /tmp/aura-agent-test
git init
aura init
```

**Expected Results**:
- `.aura/` directory created with scripts
- `.claude/commands/` created with 12 command files
- `.beads/` initialized (if bd available)

### Step 5: Verify File Structure
```bash
ls -la .aura/
ls -la .aura/scripts/
ls -la .claude/commands/
ls -la .beads/
```

### Step 6: Test Key Commands
In Claude Code session in `/tmp/aura-agent-test`:

1. Invoke `/aura.prime` - should load context
2. Invoke `/beads.status` - should show status (or empty state message)

### Step 7: Cleanup
```bash
rm -rf /tmp/aura-agent-test
```

## Agent Report Format

```markdown
## Agent Installation Test Report
Date: YYYY-MM-DD
Agent: Claude Code (model version)

### Environment Reset
- [ ] .venv/ removed
- [ ] uv cache cleared

### README Instructions Followed
| Step | Command | Result | Notes |
|------|---------|--------|-------|
| 1 | `command` | PASS/FAIL | ... |
| 2 | `command` | PASS/FAIL | ... |

### Documentation Issues Found
- Issue 1: description (line X of README)
- Issue 2: description

### Installation Verification
- [ ] `aura --version` returned: X.Y.Z
- [ ] `aura check` passed (if applicable)

### Initialization Test
- [ ] `.aura/` created with expected files
- [ ] `.claude/commands/` created with 12 commands
- [ ] `.beads/` initialized

### Slash Command Tests
- [ ] `/aura.prime` executed successfully
- [ ] `/beads.status` executed successfully

### Final Result
- [ ] PASS - Agent successfully installed and used Aura
- [ ] FAIL - Issues documented above need resolution
```

## Acceptance Criteria

- [ ] Agent resets environment completely
- [ ] Agent follows README installation without assistance
- [ ] Installation succeeds (aura command available)
- [ ] `aura init` creates all expected directories and files
- [ ] Key slash commands execute successfully
- [ ] No undocumented steps were required

## Failure Handling

If the agent encounters issues:

1. **Document the exact failure** - command, error message, context
2. **Do not work around it** - the failure reveals a documentation gap
3. **Report back** - the failure indicates Phase 1-4 work is incomplete
4. **Iterate** - fix documentation, reset, try again

## Dependencies

- Chore: Clean Slate Test (Phase 0)
- Chore: Installation Cleanup (Phase 1)
- Feature: Beads Integration (Phase 2)
- Feature: Slash Command Coherence (Phase 3)
- Chore: Tron Verification Test (Phase 4)

## Blocks

None - this is the final phase.

## Success Definition

The epic is complete when an agent can:
1. Start with a clean environment
2. Read only the README
3. Execute the documented commands
4. End with a working Aura installation
5. Initialize a new project
6. Use slash commands

No human intervention. No hints. No workarounds.
