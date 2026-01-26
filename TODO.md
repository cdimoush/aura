# Main
## Airplane
[] pyproject.toml doesn't point at .aura/scripts/requirements.txt
    - link the req
    - consider better dependency management 
    - For aura + aura in other repos
[x] remove tron
[] AGENTS.md / CLAUDE.md ?
    [x] READ
    [] Single File / Pointer for Beads?
    [] Place where?
    [] Logic for aura init
[x] understand aura cli
[] read ALL aura commands
    [] General Notes
    [] Design Workflow 
    [] Remove bad ones
    [] Implement workflow
[] Modify transcribe.py to be file writing only (Don't return a string)
    [] Next in transcribe generate title (single script)
[] cleaner file mv and output directory creation for act
[] Move to tools, skills, hooks, or sub-agent?
## Simple Dev
[] Selection of python version? Whatever bc self contained?
[] remove --no-beads
[] aura check should check for .aura dir first
[] aura installs with a README (like beads)
[] move specs inside of .aura

## Sunday
[x] Read cyborg commands
[] Design workflow

# Aura Slash Commands
Is my frontmatter good? Do slash commands take allowed-tools???

# AGENTS.md / CLAUDE.md
## General
IDK if claude gets good access to these files if they are in repo root and not in .claude/

## Review
**AGENTS.md**:
This appears to stock from bd init. `bd onboard` and `bd prime` should be told to the agent. Or even better added in as hooks.

"Landing the Plane" seems to be a sequence that the pros / author swear by. Might be nice to define my own version of safely wrapping up a task.

**CLAUDE.md**:
File is too long. Too much information. Include workflows that are possible but hypothetical. Dogfood is likely noise. However, meta dev should be acknowledged.

## Agent Context for Aura?
The easiest thing todo would be to drop AGENTS.md and make a calibrated CLAUDE.md file in .claude/ that has the both aura and beads context. 

We would like aura and beads context in the repos we are wrapping with aura. However, we want less aura context and we also don't want to erase, override, or damage existing CLAUDE.md files in the users repo. 

This could be bigger than just CLAUDE.md | how to have aura safely edit the .claude/ dir of another project. We are looking to augment and not overwrite. 

# Aura CLI
Two files only!
- src/aura/cli.py
- src/aura/init.py

## Initialization Notes
- Should I allow for beadless install? I LOVE BEADS?
- using pathlib make python clean, learn more about pathlib
    - what is glob
- Added config.py for simple config dictionaries

# My Commands
## Aura Commands
### aura.act
- make argument less strict. you are going to look in queue folder
- Do we need prereq? Or do we assume aura installed correctly?
- transcribe.py should take additional arg to write to file
- Rely on scripts more for moving and creating dirs and files
- I think I am too prescriptive in step 4


This is one of the most important commands of all of aura. Lets get it correct. 

### aura.epic
okay.. points to vision and chore which doesn't exist. Layout of main epic README.md is good.

Should it point at README.md and CLAUDE.md or somewhere else. 

- point at .aura/specs/

### aura.feature
Pretty good, add testing?

### aura.implement
likely produces rocky starts. We should have a better generic process to kick of all work available via graph

### aura.prime
We should always be primed. Begs the question if nesting slash commands is good or should we add hooks for things like priming so context management is fool proof.

### aura.process
process is just acting on entire queue. We should only have one cmd

### aura.record
claude cmd for recording doesn't seem like the best

### aura.transcribe
backed into act or process

### aura.tickets
couple harder to epic! Try stronger chain of thought flows. Maybe epic already as task graph defined. Does epic acknowledge bead creation (at least suggest ticketing is a follow up)

### aura.ticket-dev
this is done wrong. Need to be in agent/ folder. Not a command

## Bead Commands
Do I really need beads commands? Beads status seems useful as it requires multiple commands to get status data.

ACTION: Will an agent use slash commands by itself? without prompting? Thought process is if agent sees beads/done.md it may use this for learning how and when to close a bead. However, if only when called by user this is dumb as the user should be using higher level workflows and should not have to know about bead management. 

# Beads
It would be a good idea to surf what is available thru bd terminal commands. For example I just found that you can configure differently from bd init by adding arguments (example is stealth right for aura)

```bash
(aura) conner@Mac aura % bd init --help
Initialize bd in the current directory by creating a .beads/ directory
and database file. Optionally specify a custom issue prefix.

With --no-db: creates .beads/ directory and issues.jsonl file instead of SQLite database.

With --from-jsonl: imports from the current .beads/issues.jsonl file on disk instead
of scanning git history. Use this after manual JSONL cleanup (e.g., bd compact --purge-tombstones)
to prevent deleted issues from being resurrected during re-initialization.

With --stealth: configures per-repository git settings for invisible beads usage:
  • .git/info/exclude to prevent beads files from being committed
  • Claude Code settings with bd onboard instruction
  Perfect for personal use without affecting repo collaborators.

Usage:
  bd init [flags]

Flags:
  -b, --branch string       Git branch for beads commits (default: current branch)
      --contributor         Run OSS contributor setup wizard
      --force               Force re-initialization even if JSONL already has issues (may cause data loss)
      --from-jsonl          Import from current .beads/issues.jsonl file instead of git history (preserves manual cleanups)
  -h, --help                help for init
  -p, --prefix string       Issue prefix (default: current directory name)
  -q, --quiet               Suppress output (quiet mode)
      --setup-exclude       Configure .git/info/exclude to keep beads files local (for forks)
      --skip-hooks          Skip git hooks installation
      --skip-merge-driver   Skip git merge driver setup
      --stealth             Enable stealth mode: global gitattributes and gitignore, no local repo tracking
      --team                Run team workflow setup wizard

Global Flags:
      --actor string            Actor name for audit trail (default: $BD_ACTOR, git user.name, $USER)
      --allow-stale             Allow operations on potentially stale data (skip staleness check)
      --db string               Database path (default: auto-discover .beads/*.db)
      --json                    Output in JSON format
      --lock-timeout duration   SQLite busy timeout (0 = fail immediately if locked) (default 30s)
      --no-auto-flush           Disable automatic JSONL sync after CRUD operations
      --no-auto-import          Disable automatic JSONL import when newer than DB
      --no-daemon               Force direct storage mode, bypass daemon if running
      --no-db                   Use no-db mode: load from JSONL, no SQLite
      --profile                 Generate CPU profile for performance analysis
      --readonly                Read-only mode: block write operations (for worker sandboxes)
      --sandbox                 Sandbox mode: disables daemon and auto-sync
  -v, --verbose                 Enable verbose/debug output
```

# Cyborg Slash Commands
## cyborg.status
Should I have agent read the entire notes.jsonl file just to get status? This could potentially contain ALOT of information!?!

Prescripted workflows for simple state analysis may be nicer.

This is important (more important) for the step that "counts" notes on local disk and compares to jsonl. We need deterministic scripts for things like counting

LET BE VERY CLEAR WHERE NOTES ARE STORED ACROSS ALL AGENT INSTRUCTIONS!!!


## cyborg.scan
This is too similar to status. We should just combine the two commands.

Again need deterministic scripts

## cyborg.process
This is JUST like aura.process. If we plan to utilize aura in cyborg as a dependency lets just wrap aura.process with special instructions to use the cyborg brain.

## cyborg.regenerate
This needs to be dialed in. This is one of the KEY features here. Also lets get fontmatter write for really good obsidian experience