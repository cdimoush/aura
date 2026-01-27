DOT_AURA_CFG = {
    "blacklist": [
        "memo",  # memo/queue, memo/processed, memo/failed are created empty
        "epics",  # epics directory is created empty
    ],
    "copy_env": True,
}

# Folders to create (with .gitkeep)
DOT_AURA_FOLDERS = [
    "memo/queue",
    "memo/processed",
    "memo/failed",
    "epics",
]

DOT_CLAUDE_CFG = {}