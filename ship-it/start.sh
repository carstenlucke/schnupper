#!/bin/bash
set -euo pipefail

# Projekte-Verzeichnis anlegen
mkdir -p projekte

# Server starten
echo "Starting Ship It! Dashboard on http://localhost:8000"
python3 server.py &
SERVER_PID=$!

# Browser öffnen (plattformabhängig)
sleep 1
URL="http://localhost:8000"
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 || true
elif command -v open >/dev/null 2>&1; then
    open "$URL" >/dev/null 2>&1 || true
else
    echo "Bitte öffne die URL manuell in deinem Browser: $URL"
fi

# Auf Ctrl+C warten, dann aufräumen
trap "kill $SERVER_PID 2>/dev/null; exit" INT TERM
wait $SERVER_PID
