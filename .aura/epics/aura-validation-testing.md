# Epic: Aura Validation & Testing

## Overview

Validate the aura workflow end-to-end after the major redesign (14 commands → 4 skills, SessionStart hook, new folder structure). The approach is iterative: test locally with a real voice memo, then validate the install process by deploying to cyborg. Each phase has explicit pause points for user validation.

**Success Criteria**: A developer can `aura init` a fresh repo, record a voice memo, process it, and have working code generated—with minimal friction.

## Tasks

### Phase 1: Local Validation (Dogfood)

1. [ ] Test record_memo.py end-to-end - Record a real voice memo, verify transcript and title generation work correctly
2. [ ] Test `/aura.process_memo` skill (depends on 1) - Process the recorded memo, verify it reads transcript and executes the request
3. [ ] Test SessionStart hook injection (depends on 1) - Start a new Claude Code session, verify `.aura/aura.md` content is automatically injected

**PAUSE POINT**: User validates local dogfood workflow works before proceeding

### Phase 2: Install Validation (Cyborg)

4. [ ] Run `aura init` on cyborg repo (depends on 1, 2, 3) - Execute init in cyborg to verify file copying and settings.json merging
5. [ ] Verify cyborg folder structure (depends on 4) - Confirm `.aura/`, `.claude/skills/`, and settings.json are correctly created
6. [ ] Test voice memo workflow in cyborg (depends on 5) - Record and process a voice memo in cyborg to validate the full workflow

**PAUSE POINT**: User validates install process works correctly

## Dependencies

- Task 2 blocked by: 1
- Task 3 blocked by: 1
- Task 4 blocked by: 1, 2, 3
- Task 5 blocked by: 4
- Task 6 blocked by: 5

## Success Criteria

- [ ] `record_memo.py` successfully records, transcribes, and queues a memo
- [ ] `/aura.process_memo` skill processes queued memos and executes requests
- [ ] SessionStart hook automatically injects context at session start
- [ ] `aura init` runs without errors on cyborg
- [ ] End-to-end workflow tested in both aura repo (dogfood) and cyborg (external)
