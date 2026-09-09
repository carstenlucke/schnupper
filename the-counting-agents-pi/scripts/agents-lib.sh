#!/usr/bin/env bash
# agents-lib.sh — Gemeinsame Helfer für die Startskripte
#
# Wird per `source` eingebunden, nicht direkt ausgeführt.

# Liest die projektlokale .env ein und exportiert sie.
# Dort steht der TensorX-Schlüssel für die Vorlesung; die Extension
# .pi/extensions/tensorx-schnupper.ts holt ihn sich von dort über die
# Prozessumgebung. Ohne Schlüssel hat ein Start keinen Zweck — die Agenten
# würden nacheinander ins Leere laufen.
load_env() {
    local project_dir="$1"
    if [[ -f "$project_dir/.env" ]]; then
        set -a
        # shellcheck disable=SC1091
        source "$project_dir/.env"
        set +a
    fi
    if [[ -z "${SCHNUPPER_TENSORX_API_KEY:-}" ]]; then
        echo "Fehler: SCHNUPPER_TENSORX_API_KEY fehlt."
        echo "        .env.example nach .env kopieren und den TensorX-Schlüssel eintragen."
        return 1
    fi
}

# Liest ein Feld aus dem Frontmatter einer Agentendatei.
# Usage: agent_meta <datei> <feld>
agent_meta() {
    sed -n '2,/^---$/p' "$1" | sed -n "s/^$2: *//p" | head -1
}

# Gibt den Text unterhalb des Frontmatters aus — den Systemprompt des Agenten.
# Usage: agent_prompt <datei>
agent_prompt() {
    awk '/^---$/ { marker++; next } marker >= 2' "$1"
}

# Ruft pi für einen Agenten auf.
# Usage: run_pi <agentendatei> <auftrag>
#
# Die Flags im Einzelnen:
#   -p                 einmal antworten und beenden, kein interaktives Fenster
#   -nc                CLAUDE.md/AGENTS.md ignorieren — der Agent kennt nur
#                      seinen eigenen Prompt
#   -nbt               keine eingebauten Werkzeuge: kein bash, kein read,
#                      kein write. Der Agent kann ausschließlich das, was
#                      --tools ihm zugesteht
#   -a                 die projektlokale .pi/ als vertrauenswürdig behandeln,
#                      damit die Werkzeug-Extension geladen wird
#   --no-session       keinen Gesprächsverlauf speichern. Jeder Durchlauf
#                      beginnt bei null, und über das Semester wächst nichts an
run_pi() {
    local agent_file="$1"
    local task="$2"
    pi -p -nc -nbt -a --no-session \
        --model "$(agent_meta "$agent_file" model)" \
        --thinking "$(agent_meta "$agent_file" thinking)" \
        --tools "$(agent_meta "$agent_file" tools)" \
        --system-prompt "$(agent_prompt "$agent_file")" \
        "$task"
}
