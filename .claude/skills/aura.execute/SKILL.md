---
name: aura.execute
description: Create beads from a scope file and implement them autonomously
argument-hint: <scope-or-epic-path>
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Execute Scope

Create beads from a scope/epic file and implement them in dependency order.

## Input

Path to a scope or epic file, e.g., `.aura/epics/my-feature/scope.md`

## Steps

1. **Create the bead graph** - Read the `create-graph.md` file in this skill's directory and follow its instructions to parse the scope file and create beads with dependencies:
   ```bash
   cat .claude/skills/aura.execute/create-graph.md
   ```

2. **Implement the graph** - Read the `implement-graph.md` file in this skill's directory and follow its instructions to work through beads in dependency order:
   ```bash
   cat .claude/skills/aura.execute/implement-graph.md
   ```

## Notes

- This skill combines `create_beads` and `implement` into a single invocation
- The supporting files (`create-graph.md` and `implement-graph.md`) contain the full instructions for each phase
- Read each supporting file completely before starting that phase
