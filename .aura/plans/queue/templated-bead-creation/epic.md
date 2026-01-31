# Epic: Templated Bead Creation

## Overview

Add a ticket-type template system to bead creation so that high-level epic tasks like "SW FEATURE: Auth system" automatically expand into a sequence of typed sub-beads (scope, plan, implement, test) with pre-filled, role-specific descriptions. This saves tokens, improves agent instructions, and enforces a consistent workflow.

The system has three layers:
1. **Template definitions** — YAML files that declare ticket types and their stages
2. **Template engine** — A small Python module that expands a task + type into N beads with interpolated descriptions
3. **Skill integration** — Updated `create_beads` skill that detects typed tasks in epics and expands them via templates

## Tasks

### Phase 1: Design & Define Templates

1. [ ] Design template schema — Define the YAML schema for ticket-type templates (fields: type name, stages list, each stage's title suffix, description template with placeholders, default priority). Write schema doc to `.aura/templates/README.md`.

2. [ ] Create SW_FEATURE template — Author `.aura/templates/sw_feature.yaml` with four stages: scope, plan, implement, test. Each stage description should include placeholders like `{{title}}`, `{{epic_path}}`, `{{parent_task_number}}`, and stage-specific instructions (e.g. scope stage says "Define acceptance criteria and boundaries", implement stage says "Write code per the plan in the scope bead").

3. [ ] Create BUG_FIX template — Author `.aura/templates/bug_fix.yaml` with three stages: reproduce, fix, verify. Demonstrates that templates can have varying stage counts.

### Phase 2: Template Engine

4. [ ] Implement template loader (depends on 1, 2) — Python module `.aura/scripts/bead_templates.py` with `load_template(type_name) -> dict` that reads YAML from `.aura/templates/`, validates against schema, and returns parsed template. Should raise clear errors for missing/malformed templates.

5. [ ] Implement bead expansion function (depends on 4) — Add `expand_task(template, task_title, epic_path, task_number) -> list[dict]` to `bead_templates.py`. Returns a list of bead descriptors `{title, description, depends_on_offsets}` with all placeholders resolved. Stage N+1 depends on stage N by default (linear chain).

6. [ ] Add CLI wrapper for template expansion (depends on 5) — Add a standalone entry point: `python .aura/scripts/bead_templates.py expand --type sw_feature --title "Auth system" --epic .aura/epics/foo/epic.md` that prints the expanded beads as JSON. Useful for testing and debugging.

### Phase 3: Skill Integration

7. [ ] Update epic format to support typed tasks (depends on 1) — Document a new optional syntax in epic task lines: `N. [ ] [SW_FEATURE] <Title> - <Description>`. The bracket tag signals which template to use. Tasks without a tag remain simple (single bead, current behavior).

8. [ ] Update create_beads skill (depends on 5, 7) — Modify `.claude/skills/aura.create_beads/SKILL.md` to: detect `[TYPE]` tags in task lines, call `bead_templates.py expand` for typed tasks, create the resulting sub-beads with proper dependencies (both intra-task stage chain and inter-task epic dependencies), and fall back to simple single-bead creation for untagged tasks.

9. [ ] Update implement skill for stage awareness (depends on 8) — Modify `.claude/skills/aura.implement/SKILL.md` to note that stage-typed beads contain role-specific instructions in their description. The agent should follow those instructions rather than inferring work from the title alone.

### Phase 4: Verification

10. [ ] Write integration test epic (depends on 8) — Create a small test epic at `.aura/epics/test-templates/epic.md` with one `[SW_FEATURE]` task and one untagged task. Run `/aura.create_beads` against it and verify: correct number of beads created, descriptions contain expanded template text, dependencies form the right DAG.

11. [ ] Validate token savings (depends on 10) — Compare bead descriptions from templated vs manual creation. Document in epic close-out that templated descriptions are consistent and don't require the agent to re-derive instructions from scratch.

## Dependencies

- Task 4 blocked by: 1, 2
- Task 5 blocked by: 4
- Task 6 blocked by: 5
- Task 7 blocked by: 1
- Task 8 blocked by: 5, 7
- Task 9 blocked by: 8
- Task 10 blocked by: 8
- Task 11 blocked by: 10

## Success Criteria

- [ ] At least two template types exist (sw_feature, bug_fix) with distinct stage counts
- [ ] `bead_templates.py expand` produces correct JSON output for each template type
- [ ] `create_beads` skill handles mixed epics (typed and untyped tasks) in a single pass
- [ ] Expanded bead descriptions contain actionable, role-specific instructions without needing extra context
- [ ] Existing untagged epic workflow is unaffected (backward compatible)
