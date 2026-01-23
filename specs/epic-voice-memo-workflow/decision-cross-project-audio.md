# Cross-Project Audio Recording Strategy

## Decision

**Chosen Approach**: Option A - Copy Script (Self-Contained)

Scripts are copied to each project via `aura init` for self-contained operation. Each project manages its own recordings, dependencies, and queue.

## Context

Currently, `record_memo.py` will exist in `.aura/scripts/` within the Aura repository. When we run `aura init` in Cyborg (or any other project), we copy template files including scripts.

**The Question**: When recording audio from Cyborg, should we:
- Use the local copy of `record_memo.py` in Cyborg's `.aura/scripts/`?
- Reference the global Aura installation?
- Some hybrid approach?

This affects:
- Script distribution strategy
- Dependency management (SoX, Python packages)
- Update propagation (if script changes)
- User experience consistency

## Problem Statement

**Scenario 1**: Working in Aura repository
```bash
cd ~/apps/aura
python .aura/scripts/record_memo.py
# Records to ~/apps/aura/.aura/queue/
```

**Scenario 2**: Working in Cyborg repository (Aura-initialized)
```bash
cd ~/apps/aura/incubator/cyborg
python .aura/scripts/record_memo.py
# Records to ~/apps/aura/incubator/cyborg/.aura/queue/
```

**Scenario 3**: Working in external project (Aura-initialized)
```bash
cd ~/projects/my-app
python .aura/scripts/record_memo.py
# Records to ~/projects/my-app/.aura/queue/
```

All scenarios should "just work" with minimal user configuration.

## Options Analysis

### Option A: Copy Script (Self-Contained) ⭐ RECOMMENDED

**Implementation**:
- `aura init` copies `record_memo.py` to target project's `.aura/scripts/`
- Each project has its own copy of the recording script
- Scripts operate on local `.aura/queue/` directory
- SoX expected to be installed system-wide
- Python dependencies in local `.aura/.venv/`

**Pros**:
- ✅ Self-contained - project doesn't depend on external Aura installation
- ✅ Works offline/disconnected from Aura repo
- ✅ Simple mental model - everything in `.aura/` directory
- ✅ Consistent with Aura's current template approach
- ✅ Scripts can be customized per-project if needed

**Cons**:
- ❌ Duplicate code across projects
- ❌ Updates require re-running `aura init` or manual sync
- ❌ Multiple copies of dependencies if each has own venv

**User Workflow**:
```bash
# One-time setup per project
cd ~/projects/my-app
aura init
cp .aura/.env.example .aura/.env
# Add OPENAI_API_KEY to .aura/.env
cd .aura && uv venv && source .venv/bin/activate
uv pip install -r scripts/requirements.txt

# Recording (anytime)
cd ~/projects/my-app
source .aura/.venv/bin/activate  # or use full path
python .aura/scripts/record_memo.py
```

---

### Option B: Global Aura Install

**Implementation**:
- `aura init` creates `.aura/` but doesn't copy recording script
- Recording invokes script from global Aura installation
- Could use alias: `alias aura-record='python ~/apps/aura/.aura/scripts/record_memo.py'`
- Scripts detect current directory and create queue there

**Pros**:
- ✅ Single source of truth for scripts
- ✅ Updates automatically propagate
- ✅ Smaller footprint in target projects
- ✅ One set of dependencies to manage

**Cons**:
- ❌ Requires Aura to be installed and accessible
- ❌ Harder to customize per-project
- ❌ Path dependencies can break if Aura moves
- ❌ Less portable (can't zip project and move it)

**User Workflow**:
```bash
# One-time global setup
cd ~/apps/aura
source .venv/bin/activate
# (dependencies already installed)

# Recording from any project
cd ~/projects/my-app
python ~/apps/aura/.aura/scripts/record_memo.py  # or alias
```

---

### Option C: Hybrid - Detect and Fallback

**Implementation**:
- Copy script via `aura init` (like Option A)
- Script detects if it's in Aura repo vs external project
- In Aura repo: operate directly
- In external: check for global Aura, optionally sync script updates

**Pros**:
- ✅ Flexible - handles both scenarios
- ✅ Can auto-update from global if available
- ✅ Degrades gracefully if global not available

**Cons**:
- ❌ Most complex implementation
- ❌ Harder to reason about and debug
- ❌ Multiple code paths = more testing needed
- ❌ User confusion about which version is running

---

### Option D: Standalone Executable (Future)

**Implementation**:
- Package `record_memo.py` as standalone binary via PyInstaller or similar
- Install globally: `uv tool install aura-record`
- Single command works everywhere: `aura-record`

**Pros**:
- ✅ Best user experience - single command
- ✅ No Python environment management
- ✅ Easy to update via package manager

**Cons**:
- ❌ Out of scope for this epic (requires packaging work)
- ❌ Distribution complexity
- ❌ Still need SoX installed separately

---

## Recommended Decision: Option A (Copy Script)

**Rationale**:

1. **Consistency**: Matches Aura's existing pattern - all templates are copied
2. **Simplicity**: Self-contained projects are easier to reason about
3. **Portability**: Can move/copy project without external dependencies
4. **Dogfooding**: Aura itself uses this approach
5. **Incremental Path**: Can add Option D (standalone tool) later without breaking changes

**Trade-off Accepted**: Script duplication is acceptable because:
- Scripts are small and change infrequently
- Users can manually sync if needed: `aura init --force` to re-copy
- Future enhancement: `aura update` command to sync scripts

**Implementation Details**:

1. **Script Location**: `.aura/scripts/record_memo.py` (copied via `aura init`)

2. **Dependency Management**:
   ```bash
   # Each project has its own venv (recommended)
   cd .aura
   uv venv
   source .venv/bin/activate
   uv pip install -r scripts/requirements.txt
   ```

3. **SoX Installation**: System-wide (documented in README)
   ```bash
   # macOS
   brew install sox

   # Ubuntu
   sudo apt-get install sox libsox-fmt-all
   ```

4. **Recording Invocation**:
   ```bash
   # From project root
   python .aura/scripts/record_memo.py

   # Or with activated venv
   cd .aura && source .venv/bin/activate
   cd .. && python .aura/scripts/record_memo.py
   ```

5. **Update Strategy** (future):
   - Add `aura update` command to re-sync scripts from global Aura
   - Add `--check` flag to compare local vs global versions
   - Preserve local customizations if any

## Implementation Tasks

- [ ] Ensure `record_memo.py` works when called from any directory
- [ ] Update `aura init` to copy `record_memo.py` to target projects
- [ ] Document setup workflow in README.md
- [ ] Add section to CLAUDE.md about cross-project usage
- [ ] Test in Aura, Cyborg, and external project
- [ ] Verify `.aura/.venv/` pattern works consistently

## Acceptance Criteria

- [ ] Recording works from Aura repository
- [ ] Recording works from Cyborg repository
- [ ] Recording works from external Aura-initialized project
- [ ] Each project's recordings go to that project's `.aura/queue/`
- [ ] Setup documented clearly in README
- [ ] No unexpected path dependencies or errors

## Testing Plan

### Test Matrix

| Scenario | Expected Behavior |
|----------|-------------------|
| Record in Aura repo | Audio → `~/apps/aura/.aura/queue/` |
| Record in Cyborg repo | Audio → `~/apps/aura/incubator/cyborg/.aura/queue/` |
| Record in external project | Audio → `~/projects/my-app/.aura/queue/` |
| Move project to new location | Still works (no absolute paths) |
| No SoX installed | Clear error message |
| No API key | Clear error message |
| No venv activated | Uses system Python (still works if deps installed) |

### Manual Test Procedure

```bash
# 1. Test in Aura
cd ~/apps/aura
python .aura/scripts/record_memo.py
ls .aura/queue/  # Verify memo created

# 2. Test in Cyborg
cd ~/apps/aura/incubator/cyborg
aura init
cp .aura/.env.example .aura/.env
# Add API key
cd .aura && uv venv && source .venv/bin/activate
uv pip install -r scripts/requirements.txt
cd ..
python .aura/scripts/record_memo.py
ls .aura/queue/  # Verify memo created

# 3. Test in external project
mkdir -p /tmp/test-project && cd /tmp/test-project
aura init
# Setup same as Cyborg
python .aura/scripts/record_memo.py
ls .aura/queue/  # Verify memo created

# 4. Test without venv (system deps)
cd ~/apps/aura
deactivate  # if venv active
python .aura/scripts/record_memo.py
# Should work if openai, pydub installed globally
```

## Alternative Considered: Wrapper Command

Create a simple wrapper in `.aura/scripts/record.sh`:

```bash
#!/bin/bash
# Activates venv and runs record_memo.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/../.venv"

if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
fi

python "$SCRIPT_DIR/record_memo.py" "$@"
```

Usage: `./aura/scripts/record.sh`

**Status**: Nice-to-have, but adds complexity. Defer to future enhancement.

## Documentation Requirements

- [ ] README: Add cross-project recording section
- [ ] README: Document per-project venv setup
- [ ] CLAUDE.md: Add cross-project usage patterns
- [ ] Quick Start: Include recording setup in multi-project context

## Future Enhancements

1. **Aura Update Command**:
   ```bash
   aura update
   # Re-syncs scripts from global Aura installation
   # Preserves local customizations
   ```

2. **Standalone Tool**:
   ```bash
   uv tool install aura-record
   aura-record  # works anywhere
   ```

3. **IDE Integration**:
   - VS Code extension with "Record Memo" command
   - Automatically detects Aura projects
   - Handles venv activation transparently

4. **Remote Recording**:
   - Record on phone, sync to project via Dropbox/iCloud
   - Auto-transcribe on sync

## Open Questions

1. **Venv Activation**: Require users to activate manually, or have script detect and use local venv?
   - **Decision**: Manual activation (documented in README)
   - **Rationale**: More explicit, fewer surprises

2. **System Python Fallback**: If no venv, use system Python?
   - **Decision**: Yes, allow it (script tries to import, fails with clear message)
   - **Rationale**: Flexibility for power users

3. **SoX Installation Check**: Script checks for SoX on first run?
   - **Decision**: Yes, script checks and provides install instructions
   - **Rationale**: Better UX, catches issues early

## Rationale Summary

Option A provides the best balance of simplicity, portability, and consistency with Aura's existing template approach. Script duplication is acceptable because files are small and change infrequently. Users can re-sync with `aura init --force` when updates are needed.

**Implementation**: See [Chore: Implement Chosen Strategy](./chore-cross-project-impl.md)
