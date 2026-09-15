#!/bin/bash
set -euo pipefail

PORT=8100

# Laufenden Server auf dem Port beenden (optional)
if [[ "${1:-}" == "--kill" || "${1:-}" == "--force" ]]; then
    echo "Beende laufenden Server auf Port $PORT..."
    lsof -ti :$PORT | xargs kill -9 2>/dev/null || true
    sleep 1
elif lsof -ti :$PORT >/dev/null 2>&1; then
    echo "FEHLER: Port $PORT ist bereits belegt."
    echo "  Erneut starten mit:  ./start.sh --force"
    echo "  Oder manuell:        lsof -ti :$PORT | xargs kill -9"
    exit 1
fi

# Die Profile diskutieren über die pi CLI – ohne sie startet zwar das
# Dashboard, aber keine einzige Party
if ! command -v pi >/dev/null 2>&1; then
    echo "FEHLER: pi CLI nicht gefunden."
    echo "  Installieren mit:  npm install -g @earendil-works/pi-coding-agent"
    echo "  Danach einmal 'pi' starten und mit /login beim Modell-Anbieter anmelden."
    exit 1
fi

# Laufzeitverzeichnis anlegen
mkdir -p partys

echo "Agent Party startet auf http://localhost:$PORT"
python3 server.py &
SERVER_PID=$!

# Browser öffnen (plattformabhängig)
sleep 1
URL="http://localhost:$PORT"
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
