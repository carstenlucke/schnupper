# Specification: Shell-Script Variant (ohne LLM)

## Motivation

Diese Variante ersetzt die LLM-gesteuerten Agents durch reine Bash-Skripte. Damit wird das gleiche Multi-Agent-Verhalten demonstriert, jedoch ohne API-Kosten und externe Abhängigkeiten.

## Unterschiede zur LLM-Variante

| Aspekt | LLM-Variante | Shell-Variante |
|--------|-------------|----------------|
| Agent-Engine | `opencode run --agent` | Bash-Skript |
| Entscheidungen | LLM interpretiert Prompt | Feste Logik im Skript |
| Primzahl-Prüfung | LLM "denkt nach" | Algorithmus in Bash |
| Fehlerverhalten | LLM kann sich erholen | Deterministisch |
| Kosten | API-Kosten pro Durchlauf | Keine |

## Architektur

Identisch zur LLM-Variante:
- Kommunikation über `bus/*.log` (JSONL, append-only)
- State in `state/*.json`
- tmux-Layout mit 5 Panes

## Agent-Skripte

### `agents/counter.sh`
```bash
# Liest state/counter.json, erhöht Wert, schreibt nach bus/numbers.log
# Prüft bus/control.log auf pause/resume/stop
```

### `agents/odd.sh`
```bash
# Liest bus/numbers.log, filtert ungerade (value % 2 != 0)
# Aktualisiert state/odd.json
```

### `agents/even.sh`
```bash
# Liest bus/numbers.log, filtert gerade (value % 2 == 0)
# Aktualisiert state/even.json
```

### `agents/prime.sh`
```bash
# Liest bus/numbers.log, prüft auf Primzahlen
# Verarbeitet nur eine Zahl pro Durchlauf (simuliert langsamere Verarbeitung)
# Aktualisiert state/prime.json
```

### `agents/control.sh`
```bash
# Liest state/*.json und zeigt Dashboard an
# Schreibt Control-Events bei Bedarf
```

## Voraussetzungen

- bash 4+
- jq (für JSON-Verarbeitung)
- tmux

## Event-Format

Identisch zur LLM-Variante:
```json
{"type":"number","seq":1,"value":1,"timestamp":"2025-01-01T00:00:00Z"}
{"type":"control","target":"all","command":"stop","timestamp":"2025-01-01T00:00:00Z"}
```
