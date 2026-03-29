#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIR_NAME="$(basename "$ROOT_DIR")"
# Sanitize: tmux session names must not contain dots or colons
SESSION="rsrc-${DIR_NAME//[.:]/-}"

# Kill existing session if present
tmux kill-session -t "$SESSION" 2>/dev/null || true

# Create session (pane 0)
tmux new-session -d -s "$SESSION" -c "$ROOT_DIR"

# Split: new pane on top (33%), original pane stays at bottom (67%)
# After split: 0=top, 1=bottom
tmux split-window -v -b -l '33%' -c "$ROOT_DIR"

# Split top pane horizontally: 0=top-left, 1=top-right, 2=bottom
tmux select-pane -t "$SESSION:0.0"
tmux split-window -h -l '50%' -c "$ROOT_DIR"

# Panes: 0=top-left, 1=top-right, 2=bottom
# Start claude in the bottom pane
tmux send-keys -t "$SESSION:0.2" 'claude' Enter

# Select the bottom pane (claude)
tmux select-pane -t "$SESSION:0.2"

# Attach
tmux attach-session -t "$SESSION"
