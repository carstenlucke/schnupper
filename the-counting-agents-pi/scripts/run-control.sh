#!/usr/bin/env bash
# run-control.sh — Steuerungsmenü für die Multi-Agenten-Demo
#
# Die einfachen Befehle (pause, resume, stop, reset, verbose, quiet) schreibt
# dieses Menü direkt in bus/control.log — dafür braucht es kein Modell. Für
# die Zustandsübersicht und für freie Anweisungen wird der Control-Agent
# gerufen (agents/control.md).

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/agents-lib.sh"

cd "$PROJECT_DIR"
load_env "$PROJECT_DIR" || exit 1

CONTROL_AGENT="agents/control.md"

# --- Ein Steuerereignis in den Steuerungs-Bus schreiben ---
write_control_event() {
    local target="$1" command="$2" ts
    ts="$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")"
    echo "{\"type\":\"control\",\"target\":\"$target\",\"command\":\"$command\",\"timestamp\":\"$ts\"}" \
        >> "$PROJECT_DIR/bus/control.log"
}

# --- Ein Auswahlmenü zeichnen ---
# Usage: draw_box <titel> <ausgewählter-index> <fußzeile> <eintrag>...
draw_box() {
    local title="$1" selected="$2" footer="$3"; shift 3
    clear
    echo "╔══════════════════════════════════════╗"
    printf "║ %-36s ║\n" "$title"
    echo "╠══════════════════════════════════════╣"
    local i=0
    for item in "$@"; do
        if [[ $i -eq $selected ]]; then
            printf "║  > %-33s║\n" "$item"
        else
            printf "║    %-33s║\n" "$item"
        fi
        i=$((i + 1))
    done
    echo "╠══════════════════════════════════════╣"
    printf "║ %-36s ║\n" "$footer"
    echo "╚══════════════════════════════════════╝"
}

# --- Auswahl per Pfeiltasten ---
# Setzt CHOICE auf den gewählten Index, oder -1 bei Abbruch mit q.
# Usage: choose <titel> <fußzeile> <eintrag>...
choose() {
    local title="$1" footer="$2"; shift 2
    local items=("$@") selected=0 key seq
    while true; do
        draw_box "$title" "$selected" "$footer" "${items[@]}"
        read -rsn1 key
        case "$key" in
            $'\x1b')
                read -rsn2 seq
                case "$seq" in
                    '[A') ((selected > 0)) && ((selected--)) ;;
                    '[B') ((selected < ${#items[@]} - 1)) && ((selected++)) ;;
                esac
                ;;
            '') CHOICE=$selected; return ;;
            'q') CHOICE=-1; return ;;
        esac
    done
}

wait_for_key() {
    echo ""
    echo "Weiter mit einer beliebigen Taste..."
    read -rsn1
}

# --- Untermenü: Ausführlichkeit eines Agenten umschalten ---
verbosity_submenu() {
    local agents=("counter" "odd" "even" "prime")
    choose "Ausführlichkeit umschalten" "↑↓ Agent   Enter Weiter   q Zurück" "${agents[@]}"
    [[ $CHOICE -lt 0 ]] && return
    local agent="${agents[$CHOICE]}"

    choose "Modus für $agent" "↑↓ Modus   Enter Senden   q Zurück" "verbose (ausführlich)" "quiet (knapp)"
    [[ $CHOICE -lt 0 ]] && return
    local mode="quiet"
    [[ $CHOICE -eq 0 ]] && mode="verbose"

    write_control_event "$agent" "$mode"
    echo ""
    echo "✓ '$mode' an $agent gesendet."
    wait_for_key
}

MENU=(
    "Zustandsübersicht anzeigen"
    "Counter pausieren"
    "Counter fortsetzen"
    "Alle Agenten stoppen"
    "Alle Agenten zurücksetzen"
    "Ausführlichkeit umschalten"
    "Freie Anweisung eingeben"
)

while true; do
    choose "🎛  Steuerung" "↑↓ Auswahl   Enter Ausführen   q Beenden" "${MENU[@]}"

    if [[ $CHOICE -lt 0 ]]; then
        clear
        echo "Beende alle Agenten und schließe den Herdr-Tab..."
        "$PROJECT_DIR/scripts/stop.sh"
        exit 0
    fi

    clear
    case $CHOICE in
        0)
            echo "=== Zustandsübersicht wird geladen... ==="
            echo ""
            run_pi "$CONTROL_AGENT" "Zeige die Zustandsübersicht an." 2>&1 || true
            ;;
        1) write_control_event "counter" "pause";  echo "✓ Counter pausiert." ;;
        2) write_control_event "counter" "resume"; echo "✓ Counter fortgesetzt." ;;
        3) write_control_event "all" "stop";       echo "✓ Stop an alle Agenten gesendet." ;;
        4) write_control_event "all" "reset";      echo "✓ Reset an alle Agenten gesendet." ;;
        5) verbosity_submenu; continue ;;
        6)
            echo "Freie Anweisung an den Control-Agenten (leer = abbrechen):"
            echo ""
            read -rep "> " instruction
            if [[ -n "$instruction" ]]; then
                echo ""
                run_pi "$CONTROL_AGENT" "$instruction" 2>&1 || true
            else
                echo "Abgebrochen."
            fi
            ;;
    esac
    wait_for_key
done
