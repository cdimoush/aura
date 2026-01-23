# Ticket-Dev Workflow Example

This example demonstrates how `/aura.ticket-dev` enables parallel development on multiple tickets.

## Scenario

You have an epic with 5 independent tickets ready to implement:

```bash
$ bd ready

Ready tasks (no blockers):
  auth-001: Add login endpoint
  auth-002: Add signup endpoint
  auth-003: Add password reset endpoint
  auth-004: Add email verification
  auth-005: Add rate limiting middleware
```

## Sequential Approach (Traditional)

```bash
/aura.implement auth-001
# ... wait for completion (5-10 minutes) ...

/aura.implement auth-002
# ... wait for completion (5-10 minutes) ...

/aura.implement auth-003
# ... wait for completion (5-10 minutes) ...

# Total time: 25-50 minutes for 5 tickets
```

## Parallel Approach (With ticket-dev)

```bash
# Launch all 5 agents simultaneously
/aura.ticket-dev auth-001 --parallel
/aura.ticket-dev auth-002 --parallel
/aura.ticket-dev auth-003 --parallel
/aura.ticket-dev auth-004 --parallel
/aura.ticket-dev auth-005 --parallel

# Check progress
/tasks
# Shows all 5 agents working

# Total time: ~10 minutes (time of slowest ticket)
# 5x speedup!
```

## What Each Agent Does

Each ticket-dev agent works independently:

1. **Loads context**: Reads README.md, CLAUDE.md, project structure
2. **Reads ticket**: Gets requirements from `bd show auth-XXX`
3. **Plans**: Creates implementation plan
4. **Implements**: Writes code following project patterns
5. **Tests**: Runs validation commands (pytest, mypy, etc.)
6. **Closes**: Marks ticket complete with `bd close auth-XXX`
7. **Reports**: Summarizes changes and results

## Example Output

```
Launching ticket-dev agent for: auth-001

Agent will:
  ✓ Load project context
  ✓ Analyze ticket requirements
  ✓ Create implementation plan
  ✓ Execute implementation
  ✓ Run all validation tests
  ✓ Update ticket status
  ✓ Report completion

Running in background. Check progress with:
  /tasks                    # View all tasks
  Read /tmp/agent-xyz.out   # Read agent output
```

## When Agent Completes

The agent reports back:

```
Ticket-dev agent completed: auth-001

Ticket: auth-001 - Add login endpoint

Files modified:
  - src/api/auth.py:45-78 (added login endpoint)
  - tests/test_auth.py:120-145 (added login tests)

Validation results:
  ✓ pytest tests/test_auth.py::test_login (passed)
  ✓ mypy src/api/auth.py (passed)
  ✓ Manual verification: endpoint responds correctly

Ticket status: CLOSED

Next unblocked tasks:
  auth-006: Add session management (was blocked by auth-001)
```

## Best Practices

### When to Use Parallel Execution

- Multiple independent tickets (no shared files)
- Different areas of codebase (auth, UI, database)
- Different tech stacks (frontend + backend tickets)
- Large epics with many small tasks

### When NOT to Use Parallel Execution

- Tickets modifying same files (merge conflicts)
- Sequential dependencies (B depends on A)
- Limited test resources (single database)
- Tickets requiring user input/decisions

### Managing Parallel Agents

```bash
# Check all running agents
/tasks

# Read agent output
Read /tmp/agent-abc.out

# Wait for specific agent
# (automatically notified when agent completes)

# If agent gets stuck, you can interact with it
# (agents can use AskUserQuestion if blocked)
```

## Safety Considerations

Each ticket-dev agent:

- Works in isolated context (won't interfere with others)
- Follows project patterns (reads CLAUDE.md conventions)
- Validates before closing (all tests must pass)
- Can ask questions if blocked (via AskUserQuestion)
- Reports conflicts if they occur

## Advanced Usage

### Staggered Launch

```bash
# Launch first batch
/aura.ticket-dev auth-001 --parallel
/aura.ticket-dev auth-002 --parallel

# Wait for completion, then launch next batch
/aura.ticket-dev auth-003 --parallel
/aura.ticket-dev auth-004 --parallel
```

### Mixing Approaches

```bash
# Work on one ticket yourself
/aura.implement auth-001

# While that's being done, launch parallel agents
/aura.ticket-dev auth-002 --parallel
/aura.ticket-dev auth-003 --parallel
```

### Review Before Close

You can modify the ticket-dev command to NOT auto-close tickets:

```bash
# Edit .claude/commands/aura.ticket-dev.md
# Remove the "bd close" step from Phase 6
# Agent implements and validates, but leaves ticket open for review
```

## Real-World Example

From the Aura codebase itself:

```bash
# Epic: Voice Memo Workflow
# Generated 8 tickets in specs/epic-voice-memo-workflow/

$ bd ready
# Shows 3 tickets ready (no dependencies)

$ /aura.ticket-dev vmw-001 --parallel  # Transcription script
$ /aura.ticket-dev vmw-002 --parallel  # Title generation
$ /aura.ticket-dev vmw-003 --parallel  # Queue management

# 3 agents work simultaneously
# All complete in ~8 minutes (vs ~24 minutes sequential)
# All tests pass, tickets closed automatically
```

## Troubleshooting

### Agent Appears Stuck

```bash
# Check agent output
Read /tmp/agent-xyz.out

# Look for questions - agent may be waiting for input
# via AskUserQuestion
```

### Merge Conflicts

If agents modify same files:

```bash
# Git will show conflicts
$ git status

# Resolve manually, then close tickets
$ bd close auth-001
$ bd close auth-002
```

### Test Failures

Agents won't close tickets if tests fail:

```bash
# Agent output shows:
Validation failed: pytest returned exit code 1

Leaving ticket open. Please review and fix:
  - tests/test_auth.py::test_login failed

Ticket status: IN_PROGRESS (not closed)
```

Fix the issue and re-run the agent, or fix manually and close the ticket.

## Summary

The `/aura.ticket-dev` command enables:

- **Parallel execution**: Work on multiple tickets simultaneously
- **Autonomous agents**: Each agent works independently
- **Quality assurance**: All validations must pass before closing
- **Scalability**: Handle large epics efficiently
- **Flexibility**: Mix sequential and parallel approaches

Use it to dramatically speed up implementation of independent tickets while maintaining code quality and following project conventions.
