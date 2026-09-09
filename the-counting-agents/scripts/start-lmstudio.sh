#!/usr/bin/env bash
# start-lmstudio.sh — LM-Studio-Server starten und das Demo-Modell laden
#
# Die Agenten sprechen über die OpenAI-kompatible API von LM Studio
# (http://127.0.0.1:1234/v1, konfiguriert in opencode.json). Dieses Skript
# stellt sicher, dass der Server läuft und das Modell im Speicher liegt —
# sonst würde der erste Agentendurchlauf minutenlang auf das Laden warten.
#
# Wird von start.sh automatisch aufgerufen, kann aber auch vorab von Hand
# laufen (empfohlen: einmal vor der Vorlesung, dann ist alles warm).

set -euo pipefail

MODEL="${COUNTING_AGENTS_MODEL:-qwen/qwen3.6-35b-a3b}"
# Fünf Agenten fragen gleichzeitig an, also fünf parallele Vorhersagen.
PARALLEL="${COUNTING_AGENTS_PARALLEL:-5}"
# Kontext, den ein einzelner Agentendurchlauf braucht. Gemessen sind gut
# 10.000 Tokens — opencode schickt System-Prompt, Werkzeugbeschreibungen und
# die Log-Auszüge mit. 16k lassen Luft nach oben.
CONTEXT_PER_AGENT="${COUNTING_AGENTS_CONTEXT_PER_AGENT:-16384}"
# ACHTUNG: `--context-length` ist der Kontext des GESAMTEN Modells, den LM
# Studio auf die parallelen Slots aufteilt. Bei 16k und fünf Slots bleiben je
# Agent nur gut 3k — dann bricht jeder Durchlauf mit "Context size has been
# exceeded" ab. Deshalb wird hier hochgerechnet statt ein fester Wert gesetzt.
CONTEXT_LENGTH="${COUNTING_AGENTS_CONTEXT:-$(( CONTEXT_PER_AGENT * PARALLEL ))}"

command -v lms >/dev/null 2>&1 || {
    echo "Fehler: die LM-Studio-CLI 'lms' ist nicht im PATH."
    echo "        LM Studio einmal starten oder '~/.lmstudio/bin' in den PATH aufnehmen."
    exit 1
}

# --- Server starten (idempotent) ---
if lms server status 2>/dev/null | grep -q "running"; then
    echo "LM-Studio-Server läuft bereits."
else
    echo "Starte LM-Studio-Server..."
    lms server start
fi

# --- Modell vorhanden? ---
if ! lms ls 2>/dev/null | grep -q "$MODEL"; then
    echo "Modell '$MODEL' ist nicht heruntergeladen. Lade es herunter..."
    lms get "$MODEL" -y
fi

# --- Modell laden (idempotent) ---
# Es genügt nicht zu prüfen, OB das Modell geladen ist: Ein von Hand oder aus
# einem früheren Lauf mit kleinerem Kontext geladenes Modell bliebe sonst
# stehen, und alle Agenten liefen in "Context size has been exceeded".
# Deshalb werden Kontext und Parallelität mitgeprüft.
#
# `lms ps --json` liefert ein Array; die Zeile zum gesuchten Modell wird
# herausgetrennt (bewusst ohne jq, wie im Rest des Projekts).
LOADED=$(lms ps --json 2>/dev/null \
    | sed 's/},[[:space:]]*{"type"/}\
{"type"/g' \
    | grep -F "\"modelKey\":\"$MODEL\"" | head -1 || true)
CURRENT_CONTEXT=$(printf '%s' "$LOADED" | sed -n 's/.*"contextLength":\([0-9]*\).*/\1/p')
CURRENT_PARALLEL=$(printf '%s' "$LOADED" | sed -n 's/.*"parallel":\([0-9]*\).*/\1/p')

if [[ -n "$LOADED" && "$CURRENT_CONTEXT" == "$CONTEXT_LENGTH" && "$CURRENT_PARALLEL" == "$PARALLEL" ]]; then
    echo "Modell '$MODEL' ist bereits passend geladen (Kontext: $CONTEXT_LENGTH, parallel: $PARALLEL)."
else
    if [[ -n "$LOADED" ]]; then
        echo "Modell '$MODEL' ist mit anderen Werten geladen (Kontext: ${CURRENT_CONTEXT:-?}, parallel: ${CURRENT_PARALLEL:-?}) — wird neu geladen."
        lms unload "$MODEL" >/dev/null 2>&1 || true
    fi
    echo "Lade Modell '$MODEL' (Kontext: $CONTEXT_LENGTH gesamt = ${CONTEXT_PER_AGENT} x ${PARALLEL} Agenten)..."
    lms load "$MODEL" --context-length "$CONTEXT_LENGTH" --parallel "$PARALLEL" -y
fi

echo "LM Studio ist bereit."
