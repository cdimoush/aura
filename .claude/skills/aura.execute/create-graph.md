# Create Beads from Epic

Convert an epic's tasks into beads tickets with proper dependency relationships.

## Input

Path to an epic file, e.g., `.aura/epics/my-feature.md`

## Steps

1. **Read epic** - Parse the epic markdown file

2. **Extract tasks** - Find all tasks in format:
   ```
   N. [ ] <Task title> (depends on X, Y) - <Description>
   ```
   or without dependencies:
   ```
   N. [ ] <Task title> - <Description>
   ```

3. **Create beads** - For each task, create a bead:
   ```bash
   bd create --title "<Task title>" --description "<Description>. Epic: <epic-path>"
   ```
   Record the bead ID returned (e.g., `aura-abc`)

4. **Build ID mapping** - Track task number → bead ID:
   ```
   1 → aura-abc
   2 → aura-def
   3 → aura-ghi
   ```

5. **Set dependencies** - For each task with dependencies:
   ```bash
   bd dep add <task-bead-id> <blocker-bead-id>
   ```
   Example: Task 3 depends on 1, 2:
   ```bash
   bd dep add aura-ghi aura-abc
   bd dep add aura-ghi aura-def
   ```

6. **Output summary** - Show created beads and dependency graph:
   ```
   Created beads:
   1. aura-abc: Task title 1
   2. aura-def: Task title 2
   3. aura-ghi: Task title 3 (blocked by aura-abc, aura-def)

   Run `bd ready` to see unblocked tasks.
   ```

## Parsing Rules

- Task numbers are sequential across all phases
- Dependencies reference task numbers, not bead IDs
- Phase headers are informational only
- Tasks without "(depends on ...)" have no blockers

## Error Handling

- If epic file not found, report error
- If bd create fails, report and continue with remaining tasks
- If bd dep add fails, report but don't fail entire operation

## Notes

- The epic path in each bead's description lets any agent trace back to the full plan
- After creating all beads, run `bd graph --all` to verify the dependency structure
