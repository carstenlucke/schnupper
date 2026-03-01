# Implementation Plan: Shell-Script Variant

## Übersicht

Implementierung der Shell-Script-Variante als Alternative zur LLM-gesteuerten Version. Jeder Agent wird als eigenständiges Bash-Skript realisiert.

## Voraussetzungen

- `jq` für JSON-Parsing
- `bash` 4+ für assoziative Arrays
- `tmux` für Multi-Pane-Layout

## Implementierungsreihenfolge

### 1. Hilfsfunktionen (`agents/lib.sh`)
- `read_json_field()` — Feld aus JSON-Datei lesen
- `write_state()` — State-Datei atomar schreiben
- `append_event()` — Event an Log-Datei anhängen
- `check_control()` — Control-Log auf Befehle prüfen
- `iso_timestamp()` — Aktuellen ISO-8601-Timestamp erzeugen

### 2. Counter-Agent (`agents/counter.sh`)
```
Loop:
  1. State lesen (last_value, status)
  2. Control-Log prüfen
  3. Wenn running: last_value++, Event schreiben
  4. State speichern
  5. Sleep 2s
```

### 3. Odd-Agent (`agents/odd.sh`)
```
Loop:
  1. State lesen (last_seq, numbers)
  2. Control-Log prüfen
  3. Neue Events aus numbers.log lesen (seq > last_seq)
  4. Ungerade filtern, zu numbers hinzufügen
  5. State speichern
  6. Sleep 3s
```

### 4. Even-Agent (`agents/even.sh`)
```
Loop:
  1-6: Wie Odd-Agent, aber gerade Zahlen filtern
```

### 5. Prime-Agent (`agents/prime.sh`)
```
Loop:
  1. State lesen (last_seq, primes)
  2. Control-Log prüfen
  3. Nächstes Event lesen (nur eins pro Durchlauf)
  4. Primzahl-Test (Trial Division)
  5. State speichern
  6. Sleep 4s
```

Primzahl-Algorithmus:
```bash
is_prime() {
    local n=$1
    [[ $n -lt 2 ]] && return 1
    [[ $n -lt 4 ]] && return 0
    [[ $((n % 2)) -eq 0 ]] && return 1
    local i=3
    while [[ $((i * i)) -le $n ]]; do
        [[ $((n % i)) -eq 0 ]] && return 1
        i=$((i + 2))
    done
    return 0
}
```

### 6. Control-Agent (`agents/control.sh`)
```
Loop:
  1. State-Dateien aller Agents lesen
  2. Dashboard formatiert ausgeben
  3. Sleep 4s
```

### 7. Start-Skript anpassen (`scripts/start-shell.sh`)
- Wie `start.sh`, aber ruft `agents/<name>.sh` statt `run-agent.sh` auf

## Dateien

```
agents/
├── lib.sh          # Shared helper functions
├── counter.sh      # Counter agent
├── odd.sh          # Odd filter agent
├── even.sh         # Even filter agent
├── prime.sh        # Prime detector agent
└── control.sh      # Control/dashboard agent
scripts/
└── start-shell.sh  # tmux launcher for shell variant
```

## Testplan

1. `./scripts/reset.sh` — Clean state
2. `./scripts/start-shell.sh` — Shell-Variante starten
3. Prüfen: Counter zählt, Odd/Even filtern korrekt, Prime findet Primzahlen
4. `./scripts/stop.sh` — Sauber beenden
5. Vergleich: Verhalten identisch zur LLM-Variante
