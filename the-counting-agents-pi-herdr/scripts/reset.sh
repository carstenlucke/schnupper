#!/usr/bin/env bash
# reset.sh — Leert Bus und Zustand, auf Wunsch mit Neustart

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Setze Bus und Zustand zurück..."

: > "$PROJECT_DIR/_bus/numbers.log"
: > "$PROJECT_DIR/_bus/control.log"
rm -f "$PROJECT_DIR"/_state/{counter,odd,even,prime}.json

echo "Reset abgeschlossen."
echo ""

if [[ "${1:-}" == "--restart" ]]; then
    shift
    echo "Starte neu..."
    "$PROJECT_DIR/scripts/stop.sh" 2>/dev/null || true
    sleep 1
    # Alles Weitere geht an start.sh — so lässt sich beim Neustart auch das
    # Tempo ändern: ./scripts/reset.sh --restart --speed 0.5
    exec "$PROJECT_DIR/scripts/start.sh" "$@"
fi

echo "Zum Neustarten: ./scripts/reset.sh --restart"
