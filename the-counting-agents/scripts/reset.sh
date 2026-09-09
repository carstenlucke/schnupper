#!/usr/bin/env bash
# reset.sh — Reset logs and state, optionally restart

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Setze Logs und State zurück..."

# Clear bus logs
: > "$PROJECT_DIR/bus/numbers.log"
: > "$PROJECT_DIR/bus/control.log"

# Clear state files
rm -f "$PROJECT_DIR/state/counter.json"
rm -f "$PROJECT_DIR/state/odd.json"
rm -f "$PROJECT_DIR/state/even.json"
rm -f "$PROJECT_DIR/state/prime.json"

echo "Reset abgeschlossen."
echo ""

# Optionally restart
if [[ "${1:-}" == "--restart" ]]; then
    echo "Starte neu..."
    "$PROJECT_DIR/scripts/stop.sh" 2>/dev/null || true
    sleep 1
    exec "$PROJECT_DIR/scripts/start.sh"
fi

echo "Zum Neustarten: ./scripts/reset.sh --restart"
