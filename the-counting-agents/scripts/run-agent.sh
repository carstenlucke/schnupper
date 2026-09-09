#!/usr/bin/env bash
# run-agent.sh — Generic agent loop wrapper
# Usage: ./scripts/run-agent.sh <agent-name> [interval]
#
# Runs opencode in a loop, invoking the specified agent mode each iteration.

set -euo pipefail

AGENT_NAME="${1:?Usage: run-agent.sh <agent-name> [interval]}"
INTERVAL="${2:-3}"
# Obergrenze für einen einzelnen Durchlauf in Sekunden.
# Gemessen braucht ein Durchlauf gegen das lokale 35B-Modell 85-115s, wenn
# alle fünf Agenten gleichzeitig anfragen. 90s hätten also regelmäßig den
# normalen Betrieb abgeschnitten; 240s greifen nur bei einem echten Hänger.
TIMEOUT="${COUNTING_AGENTS_TIMEOUT:-240}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$PROJECT_DIR"

# Jeder Agent bekommt sein eigenes opencode-Datenverzeichnis. Ohne das greifen
# alle fünf Prozesse gleichzeitig auf dieselbe SQLite-Datei in
# ~/.local/share/opencode zu — vier von ihnen brechen dann sofort mit
# "database is locked" ab.
export XDG_DATA_HOME="$PROJECT_DIR/.opencode-data/$AGENT_NAME"
mkdir -p "$XDG_DATA_HOME"

echo "=== Agent '$AGENT_NAME' gestartet ==="
echo "Interval: ${INTERVAL}s, Timeout: ${TIMEOUT}s"
echo ""

while true; do
    if [[ -f "bus/control.log" ]]; then
        # Check for stop command
        LAST_STOP=$(grep -o '"command":"stop"' bus/control.log | tail -1 || true)
        LAST_STOP_TARGET=$(grep '"command":"stop"' bus/control.log | tail -1 | grep -o '"target":"[^"]*"' | tail -1 || true)
        if [[ -n "$LAST_STOP" ]]; then
            if [[ "$LAST_STOP_TARGET" == '"target":"all"' || "$LAST_STOP_TARGET" == "\"target\":\"$AGENT_NAME\"" ]]; then
                echo "=== Stop-Befehl erkannt. Agent '$AGENT_NAME' beendet. ==="
                exit 0
            fi
        fi

        # Check for pause/resume — find the LAST relevant pause or resume command
        LAST_PAUSE_LINE=$(grep -n "\"command\":\"pause\"" bus/control.log | grep -E "\"target\":\"all\"|\"target\":\"$AGENT_NAME\"" | tail -1 | cut -d: -f1 || true)
        LAST_RESUME_LINE=$(grep -n "\"command\":\"resume\"" bus/control.log | grep -E "\"target\":\"all\"|\"target\":\"$AGENT_NAME\"" | tail -1 | cut -d: -f1 || true)

        LAST_PAUSE_LINE="${LAST_PAUSE_LINE:-0}"
        LAST_RESUME_LINE="${LAST_RESUME_LINE:-0}"

        if [[ "$LAST_PAUSE_LINE" -gt "$LAST_RESUME_LINE" ]]; then
            # Paused — wait and re-check
            echo "=== Agent '$AGENT_NAME' pausiert. Warte auf Resume... ==="
            sleep 2
            continue
        fi
    fi

    echo "--- Durchlauf $(date '+%H:%M:%S') ---"
    # Wachhund: Gegen ein lokales Modell bleibt opencode gelegentlich hängen —
    # ohne Abbruch stünde das Pane für den Rest der Vorführung still.
    # macOS bringt kein `timeout` mit, daher von Hand.
    opencode run --agent "$AGENT_NAME" "Führe deinen nächsten Schritt aus." 2>&1 &
    RUN_PID=$!
    WAITED=0
    while kill -0 "$RUN_PID" 2>/dev/null && [[ $WAITED -lt $TIMEOUT ]]; do
        sleep 1
        WAITED=$((WAITED + 1))
    done
    if kill -0 "$RUN_PID" 2>/dev/null; then
        kill -9 "$RUN_PID" 2>/dev/null || true
        echo "=== Durchlauf nach ${TIMEOUT}s abgebrochen (Modell antwortet nicht). ==="
    fi
    wait "$RUN_PID" 2>/dev/null || true
    echo ""

    sleep "$INTERVAL"
done
