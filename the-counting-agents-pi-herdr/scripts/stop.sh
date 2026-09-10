#!/usr/bin/env bash
# stop.sh — Beendet die Multi-Agenten-Demo und schließt den Herdr-Tab

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/herdr-lib.sh"

# Stop-Ereignis in den Steuerungs-Bus schreiben
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"
echo "{\"type\":\"control\",\"target\":\"all\",\"command\":\"stop\",\"timestamp\":\"$TIMESTAMP\"}" \
    >> "$PROJECT_DIR/_bus/control.log"

echo "Stop-Ereignis geschrieben."

# Kurz warten, damit die Agenten den Stop bemerken
sleep 2

# Dashboard beenden. Beim Schließen des Tabs geht es ohnehin mit; wurde die
# Demo aber außerhalb von Herdr gestartet, bliebe der Port sonst belegt.
# Beendet wird nur, was tatsächlich das Dashboard ist — ein fremder Dienst auf
# demselben Port bleibt unangetastet.
DASHBOARD_PORT="${DASHBOARD_PORT:-8777}"
if command -v lsof >/dev/null 2>&1; then
    for PID in $(lsof -ti "tcp:$DASHBOARD_PORT" 2>/dev/null || true); do
        if ps -o command= -p "$PID" 2>/dev/null | grep -q "dashboard\.py"; then
            kill "$PID" 2>/dev/null || true
            echo "Dashboard auf Port $DASHBOARD_PORT beendet."
        fi
    done
fi

# Demo-Tab schließen
if ! herdr_require; then
    echo "Ohne Herdr-Session: Der Demo-Tab muss von Hand geschlossen werden."
    exit 0
fi

TAB_ID="$(herdr_demo_tab_id)"
if [[ -n "$TAB_ID" ]]; then
    herdr tab close "$TAB_ID" >/dev/null 2>&1 \
        && echo "Herdr-Tab '$HERDR_DEMO_TAB_LABEL' ($TAB_ID) geschlossen." \
        || echo "Herdr-Tab '$TAB_ID' konnte nicht geschlossen werden."
else
    echo "Kein Herdr-Tab '$HERDR_DEMO_TAB_LABEL' gefunden."
fi
