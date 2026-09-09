#!/usr/bin/env bash
# run-agent.sh — Führt einen Agenten in einer Endlosschleife aus
# Usage: ./scripts/run-agent.sh <agent-name>
#
# Ein Agent ist bei pi kein eigenes Programm, sondern ein Aufruf mit eigenem
# Systemprompt, eigenem Werkzeugsatz und eigenem Modell. Alles drei steht im
# Frontmatter von agents/<name>.md.

set -euo pipefail

AGENT_NAME="${1:?Usage: run-agent.sh <agent-name>}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/agents-lib.sh"

cd "$PROJECT_DIR"
load_env "$PROJECT_DIR" || exit 1

AGENT_FILE="agents/$AGENT_NAME.md"
[[ -f "$AGENT_FILE" ]] || { echo "Fehler: $AGENT_FILE gibt es nicht."; exit 1; }

INTERVAL="$(agent_meta "$AGENT_FILE" interval)"
INTERVAL="${INTERVAL:-3}"
# Obergrenze für einen einzelnen Durchlauf. Gegen das Modell in der Cloud
# dauert ein Durchlauf wenige Sekunden; 60s greifen nur bei einem echten
# Hänger und schneiden den normalen Betrieb nie ab.
TIMEOUT="${COUNTING_AGENTS_TIMEOUT:-60}"

# Der zuletzt für diesen Agenten geltende Betriebsbefehl. Die Schleife wertet
# ihn selbst aus, statt dafür jedes Mal das Modell zu fragen: ein pausierter
# Agent soll ja gerade nichts kosten.
current_command() {
    [[ -f _bus/control.log ]] || return 0
    grep -E "\"target\":\"(all|$AGENT_NAME)\"" _bus/control.log 2>/dev/null \
        | grep -oE '"command":"(pause|resume|stop)"' \
        | tail -1 \
        | sed 's/.*:"//; s/"//' || true
}

echo "=== Agent '$AGENT_NAME' gestartet ==="
echo "Modell:   $(agent_model "$AGENT_FILE")"
echo "Werkzeug: $(agent_meta "$AGENT_FILE" tools)"
echo "Takt:     ${INTERVAL}s (Abbruch nach ${TIMEOUT}s)"
echo ""

while true; do
    case "$(current_command)" in
        stop)
            echo "=== Stop-Befehl erkannt. Agent '$AGENT_NAME' beendet. ==="
            exit 0
            ;;
        pause)
            echo "=== Agent '$AGENT_NAME' pausiert. Warte auf Fortsetzung... ==="
            sleep 2
            continue
            ;;
    esac

    echo "--- Durchlauf $(date '+%H:%M:%S') ---"
    # Wachhund: Bleibt ein Aufruf hängen, stünde das Pane für den Rest der
    # Vorführung still. macOS bringt kein `timeout` mit, daher von Hand.
    run_pi "$AGENT_FILE" "Führe deinen nächsten Schritt aus." 2>&1 &
    RUN_PID=$!
    WAITED=0
    while kill -0 "$RUN_PID" 2>/dev/null && [[ $WAITED -lt $TIMEOUT ]]; do
        sleep 1
        WAITED=$((WAITED + 1))
    done
    if kill -0 "$RUN_PID" 2>/dev/null; then
        kill -9 "$RUN_PID" 2>/dev/null || true
        echo "=== Durchlauf nach ${TIMEOUT}s abgebrochen (keine Antwort). ==="
    fi
    wait "$RUN_PID" 2>/dev/null || true
    echo ""

    sleep "$INTERVAL"
done
