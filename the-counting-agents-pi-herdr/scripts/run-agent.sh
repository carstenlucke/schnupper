#!/usr/bin/env bash
# run-agent.sh — Führt einen Agenten in einer Endlosschleife aus
# Usage: [AGENT_SPEED=<faktor>] ./scripts/run-agent.sh <agent-name>
#
# AGENT_SPEED staucht oder streckt den Takt aus dem Frontmatter: 2 = doppelt so
# schnell, 0.5 = halb so schnell. Voreinstellung ist 1.
#
# Ein Agent ist bei pi kein eigenes Programm, sondern ein Aufruf mit eigenem
# Systemprompt, eigenem Werkzeugsatz und eigenem Modell. Alles drei steht im
# Frontmatter von agents/<name>.md.

set -euo pipefail

AGENT_NAME="${1:?Usage: run-agent.sh <agent-name>}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/agents-lib.sh"

cd "$PROJECT_DIR"
# Ein beim Aufruf mitgegebenes Tempo soll das aus der .env schlagen — load_env
# überschreibt sonst alles, was schon in der Umgebung steht.
SPEED_ARG="${AGENT_SPEED:-}"
load_env "$PROJECT_DIR" || exit 1
if [[ -n "$SPEED_ARG" ]]; then
    AGENT_SPEED="$SPEED_ARG"
fi
AGENT_SPEED="${AGENT_SPEED:-1}"
if ! valid_speed "$AGENT_SPEED"; then
    echo "Hinweis: AGENT_SPEED='$AGENT_SPEED' ist keine positive Zahl — es gilt 1."
    AGENT_SPEED=1
fi

AGENT_FILE="agents/$AGENT_NAME.md"
[[ -f "$AGENT_FILE" ]] || { echo "Fehler: $AGENT_FILE gibt es nicht."; exit 1; }

INTERVAL="$(agent_interval "$AGENT_FILE")"
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
# `set -e` verträgt kein `[[ ... ]] && ...` auf oberster Ebene: Trifft die
# Bedingung nicht zu, wäre das Skript hier zu Ende.
TEMPO_HINWEIS=""
if [[ "$AGENT_SPEED" != "1" ]]; then
    TEMPO_HINWEIS=" · Tempo ${AGENT_SPEED}×"
fi
echo "Takt:     ${INTERVAL}s${TEMPO_HINWEIS} (Abbruch nach ${TIMEOUT}s)"
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
        # Erst das pi-Kind, dann die Subshell. Andernfalls läuft pi weiter,
        # meldet sich Minuten später zurück und schreibt einen längst
        # überholten Stand in den Bus.
        pkill -9 -P "$RUN_PID" 2>/dev/null || true
        kill -9 "$RUN_PID" 2>/dev/null || true
        echo "=== Durchlauf nach ${TIMEOUT}s abgebrochen (keine Antwort). ==="
    fi
    wait "$RUN_PID" 2>/dev/null || true
    echo ""

    sleep "$INTERVAL"
done
