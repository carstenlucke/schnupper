#!/usr/bin/env bash
# start.sh — Start the multi-agent tmux session
#
# Creates a tmux session "agents" with 5 panes (3 equal columns):
# +----------+----------+----------+
# | counter  |   odd    |          |
# |          |          | control  |
# +----------+----------+          |
# |   even   |  prime   |          |
# |          |          |          |
# +----------+----------+----------+

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="agents"

# --- Check dependencies ---
command -v tmux >/dev/null 2>&1 || { echo "Error: tmux ist nicht installiert."; exit 1; }
command -v opencode >/dev/null 2>&1 || { echo "Error: opencode ist nicht installiert."; exit 1; }

# --- Kill existing session if present ---
tmux kill-session -t "$SESSION" 2>/dev/null || true

# --- Initialize directories and files ---
mkdir -p "$PROJECT_DIR/bus" "$PROJECT_DIR/state"
: > "$PROJECT_DIR/bus/numbers.log"
: > "$PROJECT_DIR/bus/control.log"

# Initialize state files so agents don't fail on first read
NOW=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
echo "{\"agent\":\"counter\",\"last_value\":0,\"status\":\"running\",\"updated_at\":\"$NOW\"}" > "$PROJECT_DIR/state/counter.json"
echo "{\"agent\":\"odd\",\"last_seq\":0,\"numbers\":[],\"count\":0,\"updated_at\":\"$NOW\"}" > "$PROJECT_DIR/state/odd.json"
echo "{\"agent\":\"even\",\"last_seq\":0,\"numbers\":[],\"count\":0,\"updated_at\":\"$NOW\"}" > "$PROJECT_DIR/state/even.json"
echo "{\"agent\":\"prime\",\"last_seq\":0,\"primes\":[],\"count\":0,\"updated_at\":\"$NOW\"}" > "$PROJECT_DIR/state/prime.json"

# --- Create tmux session ---
cd "$PROJECT_DIR"

# Create session with first pane (counter)
tmux new-session -d -s "$SESSION" -x 200 -y 50

# Split into 3 equal columns: left (pane 0) | middle | right
# First split: left 67% | right 33%
tmux split-window -h -t "$SESSION" -p 33

# Second split: left half into two equal columns (50/50)
tmux select-pane -t "$SESSION:.0"
tmux split-window -h -t "$SESSION" -p 50

# Now we have 3 equal columns: pane 0 | pane 1 | pane 2
# Split left column (pane 0) vertically: counter (top) | even (bottom)
tmux select-pane -t "$SESSION:.0"
tmux split-window -v -t "$SESSION"

# Split middle column (pane 2) vertically: odd (top) | prime (bottom)
tmux select-pane -t "$SESSION:.2"
tmux split-window -v -t "$SESSION"

# Result pane layout:
# 0: counter (top-left)
# 1: even (bottom-left)
# 2: odd (top-middle)
# 3: prime (bottom-middle)
# 4: control (right)

# --- Start agents in panes ---
tmux send-keys -t "$SESSION:.0" "$PROJECT_DIR/scripts/run-agent.sh counter 3" C-m
tmux send-keys -t "$SESSION:.1" "$PROJECT_DIR/scripts/run-agent.sh even 3" C-m
tmux send-keys -t "$SESSION:.2" "$PROJECT_DIR/scripts/run-agent.sh odd 3" C-m
tmux send-keys -t "$SESSION:.3" "$PROJECT_DIR/scripts/run-agent.sh prime 5" C-m
tmux send-keys -t "$SESSION:.4" "$PROJECT_DIR/scripts/run-control.sh" C-m

# --- Focus the control pane (right side) for user input ---
tmux select-pane -t "$SESSION:.4"

echo "tmux-Session '$SESSION' gestartet."
echo ""
echo "Anhängen mit:  tmux attach -t $SESSION"
echo "Beenden mit:   ./scripts/stop.sh"
echo "Reset mit:     ./scripts/reset.sh"
