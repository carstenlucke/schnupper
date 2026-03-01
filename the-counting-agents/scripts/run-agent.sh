#!/usr/bin/env bash
# run-agent.sh — Generic agent loop wrapper
# Usage: ./scripts/run-agent.sh <agent-name> [interval]
#
# Runs opencode in a loop, invoking the specified agent mode each iteration.

set -euo pipefail

AGENT_NAME="${1:?Usage: run-agent.sh <agent-name> [interval]}"
INTERVAL="${2:-3}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_DIR"

echo "=== Agent '$AGENT_NAME' gestartet ==="
echo "Interval: ${INTERVAL}s"
echo ""

while true; do
    # Check for stop command before running
    if [[ -f "bus/control.log" ]]; then
        LAST_STOP=$(grep -o '"command":"stop"' bus/control.log | tail -1 || true)
        LAST_TARGET=$(grep '"command":"stop"' bus/control.log | tail -1 | grep -o '"target":"[^"]*"' | tail -1 || true)
        if [[ -n "$LAST_STOP" ]]; then
            if [[ "$LAST_TARGET" == '"target":"all"' || "$LAST_TARGET" == "\"target\":\"$AGENT_NAME\"" ]]; then
                echo "=== Stop-Befehl erkannt. Agent '$AGENT_NAME' beendet. ==="
                exit 0
            fi
        fi
    fi

    echo "--- Durchlauf $(date '+%H:%M:%S') ---"
    opencode run --agent "$AGENT_NAME" "Führe deinen nächsten Schritt aus." 2>&1 || true
    echo ""

    sleep "$INTERVAL"
done
