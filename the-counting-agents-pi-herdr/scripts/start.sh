#!/usr/bin/env bash
# start.sh — Startet die Multi-Agenten-Demo in einem Herdr-Tab
#
# Legt im aktuellen Herdr-Workspace einen Tab mit 5 Panes an:
# +--------------------+----------+
# |  counter · Zähler  | control ·|
# |       (2/3)        | Steuerung|
# +----------+---------+----------+
# |   odd ·  | even ·  | prime ·  |
# | Ungerade | Gerade  |Primzahlen|
# +----------+---------+----------+

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$PROJECT_DIR/scripts/herdr-lib.sh"
source "$PROJECT_DIR/scripts/agents-lib.sh"

# --- Voraussetzungen prüfen ---
herdr_require || exit 1
command -v pi >/dev/null 2>&1 || { echo "Fehler: pi ist nicht installiert."; exit 1; }
load_env "$PROJECT_DIR" || exit 1

# --- Vorhandenen Demo-Tab schließen ---
EXISTING_TAB="$(herdr_demo_tab_id)"
if [[ -n "$EXISTING_TAB" && "$EXISTING_TAB" == "${HERDR_TAB_ID:-}" ]]; then
    # Sonst würde das Skript den Tab schließen, in dem es selbst läuft
    echo "Fehler: Dieses Pane liegt im Demo-Tab '$HERDR_DEMO_TAB_LABEL'."
    echo "        Erst './scripts/stop.sh' aufrufen oder aus einem Pane außerhalb starten."
    exit 1
fi
if [[ -n "$EXISTING_TAB" ]]; then
    echo "Bestehender Demo-Tab '$HERDR_DEMO_TAB_LABEL' ($EXISTING_TAB) wird geschlossen."
    herdr tab close "$EXISTING_TAB" >/dev/null 2>&1 || true
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

TAB_JSON=$(herdr tab create \
    --workspace "$HERDR_WORKSPACE_ID" \
    --label "$HERDR_DEMO_TAB_LABEL" \
    --cwd "$PROJECT_DIR" \
    --no-focus)
TAB_ID=$(printf '%s' "$TAB_JSON" | herdr_field tab_id)
PANE_COUNTER=$(printf '%s' "$TAB_JSON" | herdr_field pane_id)

[[ -n "$TAB_ID" && -n "$PANE_COUNTER" ]] || { echo "Fehler: Herdr-Tab konnte nicht angelegt werden."; exit 1; }

# Untere Reihe abtrennen (obere und untere Hälfte je 50 %)
PANE_ODD=$(herdr_split "$PANE_COUNTER" down 0.5 "$PROJECT_DIR")
# Untere Reihe dritteln: odd | even | prime
PANE_EVEN=$(herdr_split "$PANE_ODD" right 0.3333 "$PROJECT_DIR")
PANE_PRIME=$(herdr_split "$PANE_EVEN" right 0.5 "$PROJECT_DIR")
# Obere Reihe teilen: counter (2/3) | control (1/3) — zuletzt, damit der
# Fokus am Ende auf dem Steuerungs-Pane liegt
PANE_CONTROL=$(herdr_split "$PANE_COUNTER" right 0.6667 "$PROJECT_DIR" --focus)

# --- Panes benennen ---
herdr pane rename "$PANE_COUNTER" "counter · Zähler"    >/dev/null
herdr pane rename "$PANE_CONTROL" "control · Steuerung" >/dev/null
herdr pane rename "$PANE_ODD"     "odd · Ungerade"      >/dev/null
herdr pane rename "$PANE_EVEN"    "even · Gerade"       >/dev/null
herdr pane rename "$PANE_PRIME"   "prime · Primzahlen"  >/dev/null

# --- Agenten in den Panes starten ---
# Kurze Pause, damit alle Shells ihren Prompt gezeichnet haben
sleep 1

herdr pane run "$PANE_COUNTER" "$PROJECT_DIR/scripts/run-agent.sh counter" >/dev/null
herdr pane run "$PANE_CONTROL" "$PROJECT_DIR/scripts/run-control.sh"       >/dev/null
herdr pane run "$PANE_ODD"     "$PROJECT_DIR/scripts/run-agent.sh odd"     >/dev/null
herdr pane run "$PANE_EVEN"    "$PROJECT_DIR/scripts/run-agent.sh even"    >/dev/null
herdr pane run "$PANE_PRIME"   "$PROJECT_DIR/scripts/run-agent.sh prime"   >/dev/null

# --- Demo-Tab in den Vordergrund holen ---
herdr tab focus "$TAB_ID" >/dev/null

echo "Herdr-Tab '$HERDR_DEMO_TAB_LABEL' ($TAB_ID) gestartet."
echo ""
echo "Panes:       counter · Zähler | control · Steuerung"
echo "             odd · Ungerade | even · Gerade | prime · Primzahlen"
echo "Beenden mit: ./scripts/stop.sh   (oder 'q' im Steuerungs-Pane)"
echo "Reset mit:   ./scripts/reset.sh"
