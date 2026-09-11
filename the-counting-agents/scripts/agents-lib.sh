#!/usr/bin/env bash
# agents-lib.sh — Gemeinsame Helfer für die Startskripte
#
# Wird per `source` eingebunden, nicht direkt ausgeführt.

# Liest die projektlokale .env ein und exportiert sie.
#
# Dort stehen zwei Dinge: das Modell, auf dem alle Agenten laufen sollen
# (COUNTING_AGENTS_MODEL), und — falls dieses Modell über TensorX läuft — der
# zugehörige Schlüssel. Der Schlüssel wird nur verlangt, wenn er auch gebraucht
# wird; wer auf einem Abo-Modell läuft, braucht keinen.
load_env() {
    local project_dir="$1"
    if [[ -f "$project_dir/.env" ]]; then
        set -a
        # shellcheck disable=SC1091
        source "$project_dir/.env"
        set +a
    fi
    if uses_tensorx "$project_dir" && [[ -z "${SCHNUPPER_TENSORX_API_KEY:-}" ]]; then
        echo "Fehler: SCHNUPPER_TENSORX_API_KEY fehlt."
        echo "        Die Agenten sollen über TensorX laufen, aber es ist kein Schlüssel"
        echo "        hinterlegt. .env.example nach .env kopieren und ihn eintragen —"
        echo "        oder in .env ein anderes COUNTING_AGENTS_MODEL setzen."
        return 1
    fi
}

# Läuft die Demo gerade über TensorX? Entscheidend ist COUNTING_AGENTS_MODEL,
# und wenn das nicht gesetzt ist, was in den Agentendateien steht.
uses_tensorx() {
    local project_dir="$1"
    if [[ -n "${COUNTING_AGENTS_MODEL:-}" ]]; then
        [[ "$COUNTING_AGENTS_MODEL" == tensorx-schnupper/* ]]
    else
        grep -q "^model: tensorx-schnupper/" "$project_dir"/agents/*.md 2>/dev/null
    fi
}

# Liest ein Feld aus dem Frontmatter einer Agentendatei.
# Usage: agent_meta <datei> <feld>
agent_meta() {
    sed -n '2,/^---$/p' "$1" | sed -n "s/^$2: *//p" | head -1
}

# Der Takt eines Agenten in Sekunden: `interval` aus seinem Frontmatter,
# gestaucht oder gestreckt um AGENT_SPEED.
#
# AGENT_SPEED ist ein Tempofaktor wie am Abspielgerät: 2 heißt doppelt so
# schnell (halber Takt), 0.5 halb so schnell (doppelter Takt), 1 lässt alles wie
# im Frontmatter. Der Faktor gilt für alle Agenten gleich.
# Ergebnis ist immer eine ganze Zahl, mindestens 1s.
# Usage: agent_interval <datei>
agent_interval() {
    local base
    base="$(agent_meta "$1" interval)"
    awk -v b="${base:-3}" -v s="${AGENT_SPEED:-1}" 'BEGIN {
        if (s + 0 <= 0) s = 1
        v = int(b / s + 0.5)
        print (v < 1) ? 1 : v
    }'
}

# Prüft, ob ein Tempofaktor eine positive Zahl ist (1, 1.5, .5 — nicht -1, "x").
# Usage: valid_speed <wert>
valid_speed() {
    awk -v s="$1" 'BEGIN { exit !(s ~ /^[0-9]*\.?[0-9]+$/ && s + 0 > 0) }'
}

# Das Modell, mit dem ein Agent tatsächlich läuft: COUNTING_AGENTS_MODEL aus
# der .env, sonst der Eintrag aus seinem Frontmatter.
# Usage: agent_model <datei>
agent_model() {
    echo "${COUNTING_AGENTS_MODEL:-$(agent_meta "$1" model)}"
}

# Gibt den Text unterhalb des Frontmatters aus — den Systemprompt des Agenten.
# Usage: agent_prompt <datei>
agent_prompt() {
    awk '/^---$/ { marker++; next } marker >= 2' "$1"
}

# Ruft pi für einen Agenten auf. Das Modell kommt aus agent_model, kann also
# über COUNTING_AGENTS_MODEL in der .env für alle Agenten zugleich gewechselt
# werden — gedacht für den Fall, dass ein Anbieter mitten in der Vorlesung
# bremst: eine Zeile ändern, Demo neu starten, weiter geht es.
#
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
        --model "$(agent_model "$agent_file")" \
        --thinking "$(agent_meta "$agent_file" thinking)" \
        --tools "$(agent_meta "$agent_file" tools)" \
        --system-prompt "$(agent_prompt "$agent_file")" \
        "$task"
}
