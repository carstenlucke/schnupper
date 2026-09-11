#!/bin/bash
set -euo pipefail

# Laufenden Server auf Port 8000 beenden (optional)
if [[ "${1:-}" == "--kill" || "${1:-}" == "--force" ]]; then
    echo "Beende laufenden Server auf Port 8000..."
    lsof -ti :8000 | xargs kill -9 2>/dev/null || true
    sleep 1
elif lsof -ti :8000 >/dev/null 2>&1; then
    echo "FEHLER: Port 8000 ist bereits belegt."
    echo "  Erneut starten mit:  ./start.sh --force"
    echo "  Oder manuell:        lsof -ti :8000 | xargs kill -9"
    exit 1
fi

# Die Agenten laufen über die pi CLI – ohne sie startet zwar das Dashboard,
# aber kein einziger Agent
if ! command -v pi >/dev/null 2>&1; then
    echo "FEHLER: pi CLI nicht gefunden."
    echo "  Installieren mit:  npm install -g @earendil-works/pi-coding-agent"
    echo "  Danach einmal 'pi' starten und mit /login beim Modell-Anbieter anmelden."
    exit 1
fi

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
