#!/usr/bin/env bash
# stop.sh — Stop the multi-agent tmux session

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SESSION="agents"

# Write stop event to control.log
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
echo "{\"type\":\"control\",\"target\":\"all\",\"command\":\"stop\",\"timestamp\":\"$TIMESTAMP\"}" >> "$PROJECT_DIR/bus/control.log"

echo "Stop-Event geschrieben."

# Wait briefly for agents to notice
sleep 2

# Kill tmux session
tmux kill-session -t "$SESSION" 2>/dev/null && echo "tmux-Session '$SESSION' beendet." || echo "Keine tmux-Session '$SESSION' gefunden."
