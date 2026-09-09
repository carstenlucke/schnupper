#!/usr/bin/env bash
# herdr-lib.sh — Gemeinsame Herdr-Helfer für start.sh und stop.sh
#
# Wird per `source` eingebunden, nicht direkt ausgeführt.
# Bewusst ohne jq: die Herdr-CLI liefert einzeilige JSON-Antworten,
# die hier mit Bordmitteln (tr/grep/sed) ausgewertet werden.

# Label des Tabs, in dem die Demo läuft. Dient zugleich als Wiedererkennung
# beim Neustart und beim Beenden.
HERDR_DEMO_TAB_LABEL="${HERDR_DEMO_TAB_LABEL:-Counting Agents}"

# Prüft, ob wir in einer Herdr-Session laufen und die CLI erreichbar ist.
herdr_require() {
    command -v herdr >/dev/null 2>&1 || {
        echo "Fehler: herdr ist nicht installiert."
        return 1
    }
    if [[ "${HERDR_ENV:-}" != "1" || -z "${HERDR_WORKSPACE_ID:-}" ]]; then
        echo "Fehler: Dieses Skript muss in einem Herdr-Pane laufen."
        echo "        Herdr starten (herdr), dann im Projektverzeichnis erneut aufrufen."
        return 1
    fi
}

# Extrahiert den ersten Wert eines JSON-Feldes aus einer Herdr-Antwort.
# Usage: herdr_field <feldname>   (JSON kommt über stdin)
herdr_field() {
    sed -n "s/.*\"$1\":\"\([^\"]*\)\".*/\1/p" | head -1
}

# Liefert die Tab-ID des Demo-Tabs im aktuellen Workspace (leer, wenn keiner existiert).
herdr_demo_tab_id() {
    # `|| true`: ohne Treffer liefert grep 1 — das ist hier kein Fehler
    herdr tab list --workspace "$HERDR_WORKSPACE_ID" 2>/dev/null \
        | tr '{' '\n' \
        | grep -F "\"label\":\"$HERDR_DEMO_TAB_LABEL\"" \
        | sed -n 's/.*"tab_id":"\([^"]*\)".*/\1/p' \
        | head -1 || true
}

# Teilt ein Pane und gibt die ID des neuen Panes aus.
# Usage: herdr_split <pane-id> <right|down> <ratio> <cwd> [--focus|--no-focus]
herdr_split() {
    herdr pane split "$1" --direction "$2" --ratio "$3" --cwd "$4" "${5:---no-focus}" \
        | herdr_field pane_id
}
