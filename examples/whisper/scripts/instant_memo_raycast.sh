#!/usr/bin/env bash

# Raycast Script Command Metadata
# @raycast.schemaVersion 1
# @raycast.title Instant Memo (Clipboard)
# @raycast.mode silent
# @raycast.packageName Whisper
# @raycast.icon 📋
# @raycast.needsConfirmation false

# This wrapper opens Terminal and runs the instant memo script
# Records, transcribes, and copies to clipboard
# Terminal auto-closes when done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

osascript <<EOF
tell application "Terminal"
    activate
    set newTab to do script "cd '$SCRIPT_DIR' && ./instant_memo.sh"

    -- Wait for the script to finish, then close the tab
    repeat
        delay 0.5
        if not busy of newTab then
            close (first window whose tabs contains newTab)
            exit repeat
        end if
    end repeat
end tell
EOF
