#!/usr/bin/env bash
# herdr-lib.sh — Gemeinsame Herdr-Helfer für start.sh und stop.sh
#
# Wird per `source` eingebunden, nicht direkt ausgeführt.
#
# Herdr gibt es in zwei Ausprägungen, und die Demo läuft in beiden:
#
#   tui — der Terminal-Multiplexer `herdr`. Erkennbar an HERDR_ENV=1 im Pane.
#         Gesteuert über `herdr tab …` / `herdr pane …`.
#   app — die Herdr-App (Herdr.app) mit ihren beiden Kommandozeilen:
#         `herdr-app` ordnet Tabs und Panes im Fenster an, `hc` (herdr-core)
#         kennt die Terminals. Erkennbar an HC_TERMINAL_ID im Pane.
#
# herdr_require stellt fest, in welcher der beiden das Skript läuft, und
# setzt HERDR_MODUS. Alle weiteren Helfer richten sich danach.
#
# Bewusst ohne jq: Die Antworten beider Kommandozeilen werden mit Bordmitteln
# (tr/grep/sed/awk) ausgewertet.

# Label des Tabs, in dem die Demo läuft. Dient zugleich als Wiedererkennung
# beim Neustart und beim Beenden.
HERDR_DEMO_TAB_LABEL="${HERDR_DEMO_TAB_LABEL:-Counting Agents (pi)}"

# tui oder app — gesetzt von herdr_require
HERDR_MODUS=""

# Prüft, ob wir in einem Herdr-Pane laufen, und setzt HERDR_MODUS.
# Die TUI wird zuerst geprüft: Läuft sie in einem Terminal der App, ist sie
# die innere — und damit die, in der das Skript tatsächlich steht.
herdr_require() {
    if [[ "${HERDR_ENV:-}" == "1" && -n "${HERDR_WORKSPACE_ID:-}" ]]; then
        command -v herdr >/dev/null 2>&1 || {
            echo "Fehler: herdr ist nicht installiert."
            return 1
        }
        HERDR_MODUS=tui
        return 0
    fi
    if [[ -n "${HC_TERMINAL_ID:-}" ]]; then
        command -v herdr-app >/dev/null 2>&1 && command -v hc >/dev/null 2>&1 || {
            echo "Fehler: herdr-app oder hc fehlt (beide liegen der Herdr-App bei)."
            return 1
        }
        if [[ -z "$(herdr_app_eigenes_label herdr.space)" ]]; then
            echo "Fehler: Dieses Terminal gehört zu keinem Space der Herdr-App."
            echo "        In einem Tab der Herdr-App erneut aufrufen."
            return 1
        fi
        HERDR_MODUS=app
        return 0
    fi
    echo "Fehler: Dieses Skript muss in einem Herdr-Pane laufen."
    echo "        Herdr-App öffnen (oder die TUI mit 'herdr' starten),"
    echo "        dann im Projektverzeichnis erneut aufrufen."
    return 1
}

# Extrahiert den ersten Wert eines JSON-Feldes aus einer Antwort.
# Verträgt Leerzeichen nach dem Doppelpunkt, wie sie herdr-app ausgibt.
# Usage: herdr_field <feldname>   (JSON kommt über stdin)
herdr_field() {
    sed -n "s/.*\"$1\": *\"\([^\"]*\)\".*/\1/p" | head -1
}

# App: Ein Label des eigenen Terminals, etwa herdr.space oder herdr.tab.
# Die App vergibt beide an jedes Terminal, das sie in einem Tab zeigt.
herdr_app_eigenes_label() {
    hc get "$HC_TERMINAL_ID" --json 2>/dev/null | herdr_field "$1"
}

# Liefert die Tab-ID, in der dieses Skript selbst läuft.
herdr_eigener_tab() {
    if [[ "$HERDR_MODUS" == tui ]]; then
        printf '%s' "${HERDR_TAB_ID:-}"
    else
        herdr_app_eigenes_label herdr.tab
    fi
}

# Liefert die Tab-ID des Demo-Tabs im aktuellen Workspace bzw. Space
# (leer, wenn keiner existiert).
herdr_demo_tab_id() {
    if [[ "$HERDR_MODUS" == tui ]]; then
        # `|| true`: ohne Treffer liefert grep 1 — das ist hier kein Fehler
        herdr tab list --workspace "$HERDR_WORKSPACE_ID" 2>/dev/null \
            | tr '{' '\n' \
            | grep -F "\"label\":\"$HERDR_DEMO_TAB_LABEL\"" \
            | sed -n 's/.*"tab_id":"\([^"]*\)".*/\1/p' \
            | head -1 || true
    else
        # `herdr-app ls` gibt Spaces > Tabs > Terminals als eingerücktes JSON
        # aus. Jeder Space und jeder Tab beginnt mit "id", gleich danach folgt
        # "name". Gesucht ist ein Tab (tb…) mit dem Demo-Label in unserem Space.
        herdr-app ls 2>/dev/null \
            | awk -v space="$(herdr_app_eigenes_label herdr.space)" \
                  -v label="\"name\": \"$HERDR_DEMO_TAB_LABEL\"" '
                /"id": "sp/ { split($0, f, "\""); in_space = (f[4] == space) }
                /"id": "tb/ { split($0, f, "\""); tab = f[4]; next }
                index($0, label) && in_space && tab != "" { print tab; exit }
                { tab = "" }
            ' || true
    fi
}

# Schließt einen Tab samt seinen Terminals.
herdr_tab_schliessen() {
    if [[ "$HERDR_MODUS" == tui ]]; then
        herdr tab close "$1" >/dev/null 2>&1
    else
        # confirmed: Die App fragt sonst nach, wenn es der letzte Tab ist
        herdr-app do tab.close "{\"id\":\"$1\",\"confirmed\":true}" >/dev/null 2>&1
    fi
}

# Holt einen Tab in den Vordergrund.
herdr_tab_zeigen() {
    if [[ "$HERDR_MODUS" == tui ]]; then
        herdr tab focus "$1" >/dev/null
    else
        herdr-app do tab.select --id "$1" >/dev/null
    fi
}

# --- Nur TUI ---

# Teilt ein Pane und gibt die ID des neuen Panes aus.
# Usage: herdr_split <pane-id> <right|down> <ratio> <cwd> [--focus|--no-focus]
herdr_split() {
    herdr pane split "$1" --direction "$2" --ratio "$3" --cwd "$4" "${5:---no-focus}" \
        | herdr_field pane_id
}

# --- Nur App ---

# Wandelt Argumente in ein JSON-Array, wie herdr-app es für argv erwartet.
# Usage: herdr_app_argv <programm> [argument]...
herdr_app_argv() {
    local json="" arg
    for arg in "$@"; do
        arg="${arg//\\/\\\\}"
        arg="${arg//\"/\\\"}"
        json+="${json:+,}\"$arg\""
    done
    printf '[%s]' "$json"
}

# Teilt ein Pane, startet darin ein Programm und gibt die ID des neuen Panes
# aus. Die App teilt immer zur Hälfte; ein Verhältnis lässt sich nicht angeben.
#
# Anders als tab.new startet pane.split das Programm nackt: ohne Login-Shell,
# also ohne den PATH, in dem pi liegt, und nicht im gewünschten Ordner. Darum
# läuft es hier in der Login-Shell, im angegebenen Ordner — und die Shell
# bleibt nach seinem Ende offen, wie bei einem von Hand getippten Befehl.
# Usage: herdr_app_split <pane-id> <right|down> <ordner> <programm> [argument]...
herdr_app_split() {
    local pane="$1" richtung="$2" ordner="$3"; shift 3
    local shell="${SHELL:-/bin/bash}"
    case "${shell##*/}" in
        zsh|bash|sh|ksh|dash) ;;
        *) shell=/bin/bash ;;  # etwa fish: versteht das Startstück unten nicht
    esac
    herdr-app do pane.split \
        "{\"direction\":\"$richtung\",\"pane\":\"$pane\",\"argv\":$(herdr_app_argv \
            "$shell" -lic 'cd -- "$1" || exit; shift; "$@"; exec "$0" -li' \
            "$shell" "$ordner" "$@")}" \
        | herdr_field pane
}

# Liefert die Pane-ID, in der ein Terminal der App angezeigt wird.
# Usage: herdr_app_pane_von <terminal-id>
herdr_app_pane_von() {
    herdr-app ls 2>/dev/null \
        | grep -A1 -F "\"terminal\": \"$1\"" \
        | herdr_field pane
}
