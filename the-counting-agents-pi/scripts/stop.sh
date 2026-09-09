#!/usr/bin/env bash
# stop.sh — Beendet die Multi-Agenten-Demo und schließt den Herdr-Tab

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/herdr-lib.sh"

# Stop-Ereignis in den Steuerungs-Bus schreiben
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"
echo "{\"type\":\"control\",\"target\":\"all\",\"command\":\"stop\",\"timestamp\":\"$TIMESTAMP\"}" \
    >> "$PROJECT_DIR/bus/control.log"

echo "Stop-Ereignis geschrieben."

# Kurz warten, damit die Agenten den Stop bemerken
sleep 2

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
