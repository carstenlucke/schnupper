#!/usr/bin/env bash
# start-all.sh — Startet alle drei Demos und die Präsentation auf einmal
#
# Ruft nur die Startskripte der Projekte auf; was dort geprüft und gestartet
# wird, steht in deren eigener Doku.
#
#   ship-it/             → http://localhost:8000
#   agent-party/         → http://localhost:8100
#   the-counting-agents/ → eigener Herdr-Tab, Dashboard auf http://127.0.0.1:8777
#   presentation/        → http://localhost:3030
#
# Die Web-Demos und die Präsentation laufen im Hintergrund und öffnen ihren
# Browser-Tab selbst; ihre Ausgaben landen in logs/<projekt>.log. Die
# Counting Agents brauchen eine Herdr-Session — ohne sie werden sie
# übersprungen, der Rest startet trotzdem.
#
# Ctrl+C beendet alles wieder, auch den Herdr-Tab der Counting Agents; ein
# zweites Ctrl+C beendet sofort, ohne auf die Demos zu warten.
#
# Usage: ./start-all.sh [--force]
#
# --force beendet vorher, was noch auf den Ports von ship-it und agent-party
# läuft (wird an deren start.sh durchgereicht).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"

FORCE_ARG=()
case "${1:-}" in
    "")                FORCE_ARG=() ;;
    --force|--kill)    FORCE_ARG=(--force) ;;
    *)
        echo "Unbekannte Option: $1"
        echo "Usage: ./start-all.sh [--force]"
        exit 1
        ;;
esac

mkdir -p "$LOG_DIR"

NAMES=()
PIDS=()
COUNTING_GESTARTET=0

# Startet ein Projekt im Hintergrund, Ausgabe ins Log.
# stdin kommt aus /dev/null: Slidev liest sonst Tastenkürzel vom Terminal,
# und ein Hintergrundprozess, der das versucht, wird vom System angehalten —
# dann läuft die Präsentation nicht und lässt sich auch nicht mehr beenden.
# Usage: starte <name> <verzeichnis> <befehl...>
starte() {
    local name="$1" dir="$2"
    shift 2
    echo "▶ $name startet …"
    # Die Jobsteuerung ist nur für diesen Start an: Der Job bekommt so eine
    # eigene Prozessgruppe. Beim Beenden lässt sich damit der ganze Baum
    # abräumen (npm → slidev, start.sh → server.py), und Ctrl+C trifft nur
    # dieses Skript, nicht die Demos direkt. Dauerhaft an, bekäme auch jeder
    # Vordergrundbefehl hier eine eigene Gruppe und schluckte das Ctrl+C.
    set -m
    (cd "$ROOT_DIR/$dir" && exec "$@") </dev/null >"$LOG_DIR/$name.log" 2>&1 &
    set +m
    NAMES+=("$name")
    PIDS+=("$!")
}

# Schickt ein Signal an alle Prozessgruppen der Hintergrundjobs.
signal_an_alle() {
    local pid
    for pid in ${PIDS[@]+"${PIDS[@]}"}; do
        kill "-$1" -- "-$pid" 2>/dev/null || true
    done
}

# Läuft noch irgendein Prozess aus den Hintergrundjobs?
laeuft_noch() {
    local pid
    for pid in ${PIDS[@]+"${PIDS[@]}"}; do
        kill -0 -- "-$pid" 2>/dev/null && return 0
    done
    return 1
}

# Zweites Ctrl+C: nicht mehr freundlich fragen.
sofort_beenden() {
    trap - INT TERM
    signal_an_alle KILL
    echo ""
    echo "Sofort beendet."
    exit 1
}

aufraeumen() {
    trap sofort_beenden INT TERM
    echo ""
    echo "Beende alle Demos … (erneutes Ctrl+C beendet sofort)"
    # CONT hinterher, falls ein Prozess angehalten ist — sonst bliebe TERM
    # liegen, bis er weiterläuft.
    signal_an_alle TERM
    signal_an_alle CONT
    # stop.sh läuft im Hintergrund, und Hintergrundjobs ignorieren Ctrl+C:
    # Ein weiteres Ctrl+C bricht es so nicht ab, der Herdr-Tab wird trotzdem
    # geschlossen.
    if [[ $COUNTING_GESTARTET -eq 1 ]]; then
        "$ROOT_DIR/the-counting-agents/scripts/stop.sh" &
        wait $! || true
    fi
    # Bis zu fünf Sekunden Zeit geben, dann hart beenden.
    local i
    for i in 1 2 3 4 5 6 7 8 9 10; do
        laeuft_noch || break
        sleep 0.5
    done
    if laeuft_noch; then
        echo "Noch nicht alles beendet — wird hart beendet."
        signal_an_alle KILL
    fi
    echo "Alles beendet."
    exit 0
}
# Während des Starts räumt Ctrl+C sofort auf.
trap aufraeumen INT TERM

# --- Counting Agents: legen ihren eigenen Herdr-Tab an und kehren sofort zurück ---
echo "▶ the-counting-agents startet …"
if (cd "$ROOT_DIR/the-counting-agents" && ./scripts/start.sh); then
    COUNTING_GESTARTET=1
    # start.sh holt den Demo-Tab nach vorn — zurück hierher, damit die
    # Übersicht unten sichtbar bleibt und Ctrl+C an der richtigen Stelle landet.
    if [[ -n "${HERDR_TAB_ID:-}" ]]; then
        herdr tab focus "$HERDR_TAB_ID" >/dev/null 2>&1 || true
    fi
else
    echo "⚠ the-counting-agents übersprungen (siehe Meldung oben)."
fi
echo ""

# --- Web-Demos ---
starte ship-it     ship-it     ./start.sh ${FORCE_ARG[@]+"${FORCE_ARG[@]}"}
starte agent-party agent-party ./start.sh ${FORCE_ARG[@]+"${FORCE_ARG[@]}"}

# --- Präsentation: zuletzt, damit ihr Browser-Tab vorne liegt ---
if [[ ! -d "$ROOT_DIR/presentation/node_modules" ]]; then
    echo "▶ presentation: Abhängigkeiten fehlen, npm install läuft …"
    (cd "$ROOT_DIR/presentation" && npm install)
fi
starte presentation presentation npm run dev

# --- Kurz warten und prüfen, ob alles noch läuft ---
sleep 3
FEHLER=0
for i in "${!PIDS[@]}"; do
    if ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
        FEHLER=1
        echo ""
        echo "✗ ${NAMES[$i]} ist nicht gestartet. Letzte Zeilen aus logs/${NAMES[$i]}.log:"
        tail -n 10 "$LOG_DIR/${NAMES[$i]}.log" | sed 's/^/    /'
    fi
done

adresse() {
    case "$1" in
        ship-it)      echo "http://localhost:8000" ;;
        agent-party)  echo "http://localhost:8100" ;;
        presentation) echo "http://localhost:3030  (bei belegtem Port der nächste freie)" ;;
    esac
}

echo ""
echo "Übersicht:"
if [[ $COUNTING_GESTARTET -eq 1 ]]; then
    echo "  ✓ the-counting-agents  Herdr-Tab, Dashboard http://127.0.0.1:8777"
else
    echo "  ✗ the-counting-agents  nicht gestartet"
fi
for i in "${!PIDS[@]}"; do
    if kill -0 "${PIDS[$i]}" 2>/dev/null; then
        printf '  ✓ %-20s %s\n' "${NAMES[$i]}" "$(adresse "${NAMES[$i]}")"
    else
        printf '  ✗ %-20s %s\n' "${NAMES[$i]}" "nicht gestartet"
    fi
done
echo ""
echo "Logs:     $LOG_DIR/"
if [[ $FEHLER -eq 1 ]]; then
    echo "Hinweis:  Belegte Ports räumt ./start-all.sh --force ab."
fi
echo "Beenden:  Ctrl+C"

# Ab hier bricht Ctrl+C nur das Warten ab; aufgeräumt wird danach im normalen
# Ablauf. Liefe das Aufräumen im Signal-Handler selbst, griffe ein zweites
# Ctrl+C dort nicht mehr zuverlässig.
trap : INT TERM
wait || true
aufraeumen
