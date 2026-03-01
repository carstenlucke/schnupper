#!/usr/bin/env bash
# run-control.sh — Interactive control menu for the Control Agent
#
# Displays an arrow-key navigable menu to manage the multi-agent system.
# Simple commands (pause/resume/stop/reset/verbose/quiet) write directly
# to bus/control.log. Status dashboard and custom instructions use opencode.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

# --- Menu items ---
MENU_ITEMS=(
    "Status Dashboard anzeigen"
    "Counter pausieren"
    "Counter fortsetzen"
    "Alle Agents stoppen"
    "Alle Agents zurücksetzen"
    "Verbose/Quiet umschalten"
    "Custom-Anweisung eingeben"
)
MENU_COUNT=${#MENU_ITEMS[@]}
SELECTED=0

# --- Helper: write a control event to bus/control.log ---
write_control_event() {
    local target="$1"
    local command="$2"
    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
    echo "{\"type\":\"control\",\"target\":\"$target\",\"command\":\"$command\",\"timestamp\":\"$ts\"}" >> "$PROJECT_DIR/bus/control.log"
}

# --- Helper: draw the menu ---
draw_menu() {
    clear
    echo "╔══════════════════════════════════════╗"
    echo "║       🎛  Control Agent Menü         ║"
    echo "╠══════════════════════════════════════╣"
    for i in "${!MENU_ITEMS[@]}"; do
        if [[ $i -eq $SELECTED ]]; then
            printf "║  > %-33s║\n" "${MENU_ITEMS[$i]}"
        else
            printf "║    %-33s║\n" "${MENU_ITEMS[$i]}"
        fi
    done
    echo "╠══════════════════════════════════════╣"
    echo "║  ↑↓ Auswahl   Enter Ausführen   q ✕ ║"
    echo "╚══════════════════════════════════════╝"
}

# --- Helper: wait for keypress before returning to menu ---
wait_for_key() {
    echo ""
    echo "Drücke eine beliebige Taste für das Menü..."
    read -rsn1
}

# --- Helper: verbose/quiet submenu ---
verbose_submenu() {
    local agents=("counter" "odd" "even" "prime")
    local sub_sel=0
    local modes=("verbose" "quiet")
    local mode_sel=0

    while true; do
        clear
        echo "╔══════════════════════════════════════╗"
        echo "║     Verbose/Quiet umschalten         ║"
        echo "╠══════════════════════════════════════╣"
        echo "║  Agent auswählen:                    ║"
        for i in "${!agents[@]}"; do
            if [[ $i -eq $sub_sel ]]; then
                printf "║  > %-33s║\n" "${agents[$i]}"
            else
                printf "║    %-33s║\n" "${agents[$i]}"
            fi
        done
        echo "╠══════════════════════════════════════╣"
        echo "║  ↑↓ Auswahl   Enter Weiter   q ←    ║"
        echo "╚══════════════════════════════════════╝"

        read -rsn1 key
        case "$key" in
            $'\x1b')
                read -rsn2 seq
                case "$seq" in
                    '[A') ((sub_sel > 0)) && ((sub_sel--)) ;;
                    '[B') ((sub_sel < ${#agents[@]} - 1)) && ((sub_sel++)) ;;
                esac
                ;;
            '')
                # Enter pressed — choose mode
                local chosen_agent="${agents[$sub_sel]}"
                clear
                echo "╔══════════════════════════════════════╗"
                printf "║  Modus für %-26s║\n" "$chosen_agent:"
                echo "╠══════════════════════════════════════╣"
                for i in "${!modes[@]}"; do
                    if [[ $i -eq $mode_sel ]]; then
                        printf "║  > %-33s║\n" "${modes[$i]}"
                    else
                        printf "║    %-33s║\n" "${modes[$i]}"
                    fi
                done
                echo "╠══════════════════════════════════════╣"
                echo "║  ↑↓ Auswahl   Enter Ausführen   q ← ║"
                echo "╚══════════════════════════════════════╝"

                while true; do
                    read -rsn1 mkey
                    case "$mkey" in
                        $'\x1b')
                            read -rsn2 mseq
                            case "$mseq" in
                                '[A') ((mode_sel > 0)) && ((mode_sel--)) ;;
                                '[B') ((mode_sel < 1)) && ((mode_sel++)) ;;
                            esac
                            # Redraw mode menu
                            clear
                            echo "╔══════════════════════════════════════╗"
                            printf "║  Modus für %-26s║\n" "$chosen_agent:"
                            echo "╠══════════════════════════════════════╣"
                            for i in "${!modes[@]}"; do
                                if [[ $i -eq $mode_sel ]]; then
                                    printf "║  > %-33s║\n" "${modes[$i]}"
                                else
                                    printf "║    %-33s║\n" "${modes[$i]}"
                                fi
                            done
                            echo "╠══════════════════════════════════════╣"
                            echo "║  ↑↓ Auswahl   Enter Ausführen   q ← ║"
                            echo "╚══════════════════════════════════════╝"
                            ;;
                        '')
                            write_control_event "$chosen_agent" "${modes[$mode_sel]}"
                            echo ""
                            echo "✓ ${modes[$mode_sel]} für '$chosen_agent' gesendet."
                            wait_for_key
                            return
                            ;;
                        'q') return ;;
                    esac
                done
                ;;
            'q') return ;;
        esac
    done
}

# --- Main loop ---
draw_menu

while true; do
    read -rsn1 key

    case "$key" in
        $'\x1b')
            # Escape sequence — read the rest
            read -rsn2 seq
            case "$seq" in
                '[A') # Up arrow
                    ((SELECTED > 0)) && ((SELECTED--))
                    draw_menu
                    ;;
                '[B') # Down arrow
                    ((SELECTED < MENU_COUNT - 1)) && ((SELECTED++))
                    draw_menu
                    ;;
            esac
            ;;
        '') # Enter
            clear
            case $SELECTED in
                0) # Status Dashboard
                    echo "=== Status Dashboard wird geladen... ==="
                    echo ""
                    opencode run --agent control "Zeige das Status-Dashboard an." 2>&1 || true
                    wait_for_key
                    draw_menu
                    ;;
                1) # Counter pausieren
                    write_control_event "counter" "pause"
                    echo "✓ Counter pausiert."
                    wait_for_key
                    draw_menu
                    ;;
                2) # Counter fortsetzen
                    write_control_event "counter" "resume"
                    echo "✓ Counter fortgesetzt."
                    wait_for_key
                    draw_menu
                    ;;
                3) # Alle stoppen
                    write_control_event "all" "stop"
                    echo "✓ Stop-Befehl an alle Agents gesendet."
                    wait_for_key
                    draw_menu
                    ;;
                4) # Alle zurücksetzen
                    write_control_event "all" "reset"
                    echo "✓ Reset-Befehl an alle Agents gesendet."
                    wait_for_key
                    draw_menu
                    ;;
                5) # Verbose/Quiet
                    verbose_submenu
                    draw_menu
                    ;;
                6) # Custom-Anweisung
                    echo "╔══════════════════════════════════════╗"
                    echo "║     Custom-Anweisung eingeben        ║"
                    echo "╠══════════════════════════════════════╣"
                    echo "║  Eingabe (leer = abbrechen):         ║"
                    echo "╚══════════════════════════════════════╝"
                    echo ""
                    read -rep "> " custom_input
                    if [[ -n "$custom_input" ]]; then
                        echo ""
                        echo "Wird ausgeführt..."
                        echo ""
                        opencode run --agent control "$custom_input" 2>&1 || true
                    else
                        echo "Abgebrochen."
                    fi
                    wait_for_key
                    draw_menu
                    ;;
            esac
            ;;
        'q') # Quit — stop all agents and kill tmux session
            clear
            echo "Beende alle Agents und tmux-Session..."
            "$PROJECT_DIR/scripts/stop.sh"
            exit 0
            ;;
    esac
done
