#!/usr/bin/env bash
# start.sh — Startet die Multi-Agenten-Demo in einem Herdr-Tab
#
# Läuft in der Herdr-App ebenso wie in der Herdr-TUI (siehe herdr-lib.sh).
# Legt im aktuellen Space bzw. Workspace einen Tab mit 6 Panes an. In der TUI:
# +--------------------+----------+
# |  counter · Zähler  | control ·|
# |       (2/3)        | Steuerung|
# +----------+---------+----------+
# |   odd ·  | even ·  | prime ·  |
# | Ungerade | Gerade  |Primzahlen|
# +----------+---------+----------+
# |     dashboard · Übersicht     |
# +-------------------------------+
#
# Die App teilt Panes nur zur Hälfte und kennt keine Pane-Namen. Dort sieht
# der Tab so aus — prime bekommt den meisten Platz, weil er beim Nachdenken
# am meisten ausgibt:
# +---------------+---------------+
# |               |    control    |
# |    counter    +---------------+
# |               |   dashboard   |
# +-------+-------+---------------+
# |  odd  | even  |     prime     |
# +-------+-------+---------------+
#
# Das Dashboard-Pane startet das Web-Dashboard für den Beamer und gibt nur
# seine Adresse aus. Mit --ohne-dashboard bleibt es bei den fünf Agenten-Panes.
#
# Usage: ./scripts/start.sh [--ohne-dashboard] [--speed <faktor>] [--im-hintergrund]
#
# --speed staucht oder streckt den Takt aller Agenten gemeinsam: 1.5 heißt
# anderthalbfaches Tempo, 0.5 halbes. Dasselbe geht über die Umgebungsvariable
# AGENT_SPEED oder einen Eintrag in der .env; der Aufruf hat Vorrang.
#
# --im-hintergrund lässt den aufrufenden Tab vorne, statt zum Demo-Tab zu
# wechseln (für start-all.sh, dessen Übersicht sichtbar bleiben soll).

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/herdr-lib.sh"
source "$PROJECT_DIR/scripts/agents-lib.sh"

# --- Aufrufoptionen ---
DASHBOARD_PORT="${DASHBOARD_PORT:-8777}"
MIT_DASHBOARD=1
SPEED_ARG=""
IM_HINTERGRUND=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ohne-dashboard) MIT_DASHBOARD=0; shift ;;
        --speed)          SPEED_ARG="${2:?Fehler: --speed braucht einen Faktor, z. B. --speed 1.5}"; shift 2 ;;
        --speed=*)        SPEED_ARG="${1#*=}"; shift ;;
        --im-hintergrund) IM_HINTERGRUND=1; shift ;;
        *)
            echo "Unbekannte Option: $1"
            echo "Usage: ./scripts/start.sh [--ohne-dashboard] [--speed <faktor>] [--im-hintergrund]"
            exit 1
            ;;
    esac
done

# --- Voraussetzungen prüfen ---
herdr_require || exit 1
command -v pi >/dev/null 2>&1 || { echo "Fehler: pi ist nicht installiert."; exit 1; }
load_env "$PROJECT_DIR" || exit 1

# Tempo festlegen — nach load_env, damit ein `AGENT_SPEED` aus der .env den
# Aufruf nicht überschreibt: Aufruf schlägt .env schlägt Voreinstellung.
AGENT_SPEED="${SPEED_ARG:-${AGENT_SPEED:-1}}"
if ! valid_speed "$AGENT_SPEED"; then
    echo "Fehler: '$AGENT_SPEED' ist kein Tempofaktor. Erwartet wird eine"
    echo "        positive Zahl, etwa 1.5 (schneller) oder 0.5 (langsamer)."
    exit 1
fi
export AGENT_SPEED

# Ohne python3 läuft die Demo trotzdem — nur eben ohne Dashboard.
if [[ $MIT_DASHBOARD -eq 1 ]] && ! command -v python3 >/dev/null 2>&1; then
    echo "Hinweis: python3 fehlt — die Demo startet ohne Dashboard."
    MIT_DASHBOARD=0
fi

# --- Vorhandenen Demo-Tab schließen ---
EIGENER_TAB="$(herdr_eigener_tab)"
EXISTING_TAB="$(herdr_demo_tab_id)"
if [[ -n "$EXISTING_TAB" && "$EXISTING_TAB" == "$EIGENER_TAB" ]]; then
    # Sonst würde das Skript den Tab schließen, in dem es selbst läuft
    echo "Fehler: Dieses Pane liegt im Demo-Tab '$HERDR_DEMO_TAB_LABEL'."
    echo "        Erst './scripts/stop.sh' aufrufen oder aus einem Pane außerhalb starten."
    exit 1
fi
if [[ -n "$EXISTING_TAB" ]]; then
    echo "Bestehender Demo-Tab '$HERDR_DEMO_TAB_LABEL' ($EXISTING_TAB) wird geschlossen."
    herdr_tab_schliessen "$EXISTING_TAB" || true
    sleep 1
fi

# --- Bus und Zustand leeren ---
# Die Werkzeuge legen fehlende Dateien selbst an und kommen mit leeren
# Dateien zurecht — vorbelegen muss hier niemand mehr etwas.
mkdir -p "$PROJECT_DIR/_bus" "$PROJECT_DIR/_state"
: > "$PROJECT_DIR/_bus/numbers.log"
: > "$PROJECT_DIR/_bus/control.log"
rm -f "$PROJECT_DIR"/_state/{counter,odd,even,prime}.json

# --- Tab und Panes aufbauen ---
cd "$PROJECT_DIR"

# Was in den Panes läuft. Jedes Pane bekommt eine frische Shell — das Tempo
# muss deshalb im Aufruf selbst stehen, exportieren allein reicht nicht.
RUN_AGENT="$PROJECT_DIR/scripts/run-agent.sh"
RUN_CONTROL="$PROJECT_DIR/scripts/run-control.sh"
DASHBOARD="$PROJECT_DIR/scripts/dashboard.py"

# Herdr-TUI: Panes mit Verhältnis teilen, benennen, dann die Befehle in die
# Shells tippen lassen.
aufbau_tui() {
    local tab_json
    tab_json=$(herdr tab create \
        --workspace "$HERDR_WORKSPACE_ID" \
        --label "$HERDR_DEMO_TAB_LABEL" \
        --cwd "$PROJECT_DIR" \
        --no-focus)
    TAB_ID=$(printf '%s' "$tab_json" | herdr_field tab_id)
    local pane_counter
    pane_counter=$(printf '%s' "$tab_json" | herdr_field pane_id)

    [[ -n "$TAB_ID" && -n "$pane_counter" ]] || { echo "Fehler: Herdr-Tab konnte nicht angelegt werden."; exit 1; }

    # Schmalen Streifen für das Dashboard ganz unten abtrennen — zuerst, damit er
    # über die volle Breite läuft und die Agenten-Panes sich den Rest teilen.
    local pane_dashboard=""
    if [[ $MIT_DASHBOARD -eq 1 ]]; then
        pane_dashboard=$(herdr_split "$pane_counter" down 0.88 "$PROJECT_DIR")
    fi
    # Untere Reihe abtrennen (obere und untere Hälfte je 50 %)
    local pane_odd pane_even pane_prime pane_control
    pane_odd=$(herdr_split "$pane_counter" down 0.5 "$PROJECT_DIR")
    # Untere Reihe dritteln: odd | even | prime
    pane_even=$(herdr_split "$pane_odd" right 0.3333 "$PROJECT_DIR")
    pane_prime=$(herdr_split "$pane_even" right 0.5 "$PROJECT_DIR")
    # Obere Reihe teilen: counter (2/3) | control (1/3) — zuletzt, damit der
    # Fokus am Ende auf dem Steuerungs-Pane liegt
    pane_control=$(herdr_split "$pane_counter" right 0.6667 "$PROJECT_DIR" --focus)

    # --- Panes benennen ---
    herdr pane rename "$pane_counter" "counter · Zähler"    >/dev/null
    herdr pane rename "$pane_control" "control · Steuerung" >/dev/null
    herdr pane rename "$pane_odd"     "odd · Ungerade"      >/dev/null
    herdr pane rename "$pane_even"    "even · Gerade"       >/dev/null
    herdr pane rename "$pane_prime"   "prime · Primzahlen"  >/dev/null
    if [[ -n "$pane_dashboard" ]]; then
        herdr pane rename "$pane_dashboard" "dashboard · Übersicht" >/dev/null
    fi

    # --- Agenten in den Panes starten ---
    # Kurze Pause, damit alle Shells ihren Prompt gezeichnet haben
    sleep 1

    herdr pane run "$pane_counter" "AGENT_SPEED=$AGENT_SPEED $RUN_AGENT counter" >/dev/null
    herdr pane run "$pane_control" "$RUN_CONTROL"                                >/dev/null
    herdr pane run "$pane_odd"     "AGENT_SPEED=$AGENT_SPEED $RUN_AGENT odd"     >/dev/null
    herdr pane run "$pane_even"    "AGENT_SPEED=$AGENT_SPEED $RUN_AGENT even"    >/dev/null
    herdr pane run "$pane_prime"   "AGENT_SPEED=$AGENT_SPEED $RUN_AGENT prime"   >/dev/null

    # Das Dashboard liest nur mit; es darf ruhig vor den ersten Zahlen laufen und
    # öffnet den Browser selbst.
    if [[ -n "$pane_dashboard" ]]; then
        herdr pane run "$pane_dashboard" "$DASHBOARD $DASHBOARD_PORT" >/dev/null
    fi

    # Der Fokus ist Komfort: Scheitert er, läuft die Demo trotzdem.
    if [[ $IM_HINTERGRUND -eq 0 ]]; then
        herdr tab focus "$TAB_ID" >/dev/null 2>&1 || true
    elif [[ -n "$EIGENER_TAB" ]]; then
        # Die Teilung mit --focus oben kann den neuen Tab nach vorn holen —
        # zurück in den Tab, aus dem start.sh gerufen wurde
        herdr tab focus "$EIGENER_TAB" >/dev/null 2>&1 || true
    fi
}

# Herdr-App: Jedes Pane startet gleich mit seinem Programm; es läuft in der
# Login-Shell, die danach offen bleibt (siehe herdr_app_split). Die App zeigt
# einen neuen Tab sofort und fokussiert jedes neue Pane — am Ende wird der
# Fokus deshalb gezielt gesetzt.
aufbau_app() {
    local tab_json pane_counter
    tab_json=$(herdr-app do tab.new \
        "{\"name\":$(herdr_json "$HERDR_DEMO_TAB_LABEL"),\"space\":\"$HERDR_APP_SPACE\",\"folder\":$(herdr_json "$PROJECT_DIR"),\"argv\":$(herdr_app_argv env "AGENT_SPEED=$AGENT_SPEED" "$RUN_AGENT" counter)}")
    TAB_ID=$(printf '%s' "$tab_json" | herdr_field tab)
    [[ -n "$TAB_ID" ]] || { echo "Fehler: Herdr-Tab konnte nicht angelegt werden."; exit 1; }

    # Ab hier steht ein Tab mit laufendem Counter. Bricht der Aufbau ab — über
    # einen der Fehlerzweige unten oder weil set -e bei einem gescheiterten
    # herdr-app-Aufruf greift —, schließt der Trap ihn wieder, statt ihn halb
    # fertig stehen zu lassen.
    trap 'echo "Halb angelegter Demo-Tab wird wieder geschlossen."; herdr_tab_schliessen "$TAB_ID" || true' EXIT

    local term_counter
    term_counter=$(printf '%s' "$tab_json" | herdr_field terminal)
    pane_counter=""
    if [[ -n "$term_counter" ]]; then
        pane_counter=$(herdr_app_pane_von "$term_counter")
    fi
    [[ -n "$pane_counter" ]] || { echo "Fehler: Herdr-Tab konnte nicht angelegt werden."; exit 1; }

    # Untere Hälfte: odd | even | prime (prime rechts mit halber Breite)
    local pane_odd pane_control
    pane_odd=$(herdr_app_split "$pane_counter" down "$PROJECT_DIR" env "AGENT_SPEED=$AGENT_SPEED" "$RUN_AGENT" odd)
    # Ohne Pane-ID teilte die App das gerade fokussierte Pane — das Layout
    # geriete durcheinander. Lieber gleich abbrechen.
    [[ -n "$pane_odd" ]] || { echo "Fehler: Pane konnte nicht geteilt werden."; exit 1; }
    herdr_app_split "$pane_odd" right "$PROJECT_DIR" env "AGENT_SPEED=$AGENT_SPEED" "$RUN_AGENT" prime >/dev/null
    herdr_app_split "$pane_odd" right "$PROJECT_DIR" env "AGENT_SPEED=$AGENT_SPEED" "$RUN_AGENT" even  >/dev/null
    # Obere Hälfte: counter | control, darunter rechts das Dashboard
    pane_control=$(herdr_app_split "$pane_counter" right "$PROJECT_DIR" "$RUN_CONTROL")
    [[ -n "$pane_control" ]] || { echo "Fehler: Pane konnte nicht geteilt werden."; exit 1; }
    if [[ $MIT_DASHBOARD -eq 1 ]]; then
        herdr_app_split "$pane_control" down "$PROJECT_DIR" "$DASHBOARD" "$DASHBOARD_PORT" >/dev/null
    fi

    # Der Tab steht vollständig — ab hier nichts mehr wegräumen
    trap - EXIT

    # Der Fokus ist Komfort: Scheitert er, läuft die Demo trotzdem, und
    # start.sh darf deshalb nicht als gescheitert gelten.
    if [[ $IM_HINTERGRUND -eq 0 ]]; then
        herdr-app do pane.focus --pane "$pane_control" >/dev/null 2>&1 || true
    else
        # Zurück in den Tab und das Pane, aus dem start.sh gerufen wurde
        herdr-app do pane.focus --terminal "$HC_TERMINAL_ID" >/dev/null 2>&1 || true
    fi
}

if [[ "$HERDR_MODUS" == tui ]]; then
    aufbau_tui
else
    aufbau_app
fi

echo "Herdr-Tab '$HERDR_DEMO_TAB_LABEL' ($TAB_ID) gestartet."
echo ""
echo "Panes:       counter · control$( [[ $MIT_DASHBOARD -eq 1 ]] && echo " · dashboard" )"
echo "             odd · even · prime"
if [[ "$AGENT_SPEED" != "1" ]]; then
    echo "Tempo:       ${AGENT_SPEED}×  (Takt aus dem Frontmatter durch $AGENT_SPEED geteilt)"
fi
if [[ $MIT_DASHBOARD -eq 1 ]]; then
    echo "Dashboard:   http://127.0.0.1:$DASHBOARD_PORT/  (öffnet sich von selbst)"
fi
echo "Beenden mit: ./scripts/stop.sh   (oder 'q' im Steuerungs-Pane)"
echo "Reset mit:   ./scripts/reset.sh"
