#!/bin/bash
set -euo pipefail

# Projekte-Verzeichnis anlegen
mkdir -p projekte

# Server starten
echo "Starting Ship It! Dashboard on http://localhost:8000"
python3 server.py &
SERVER_PID=$!

# Browser öffnen (macOS)
sleep 1
open http://localhost:8000

# Auf Ctrl+C warten, dann aufräumen
trap "kill $SERVER_PID 2>/dev/null; exit" INT TERM
wait $SERVER_PID
