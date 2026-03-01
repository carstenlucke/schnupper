# The Counting Agents

Terminal-basierte Demo eines Multi-Agent-Systems. Autonome LLM-Agents kommunizieren über Filesystem-basierte Event-Logs und laufen in einer tmux-Session.

## Konzept

Fünf Agents arbeiten zusammen:

- **Counter** — Erzeugt fortlaufende Zahlen und schreibt sie in den Event-Bus
- **Odd** — Filtert und sammelt ungerade Zahlen
- **Even** — Filtert und sammelt gerade Zahlen
- **Prime** — Erkennt Primzahlen (absichtlich langsamer)
- **Control** — Zeigt Status-Dashboard, sendet Steuerungsbefehle

Die Agents kommunizieren ausschließlich über append-only JSONL-Dateien im `bus/`-Verzeichnis. Jeder Agent speichert seinen Zustand in `state/`.

## Architektur

```
+----------+----------+------------------+
| counter  |   odd    |                  |
|          |          |     control      |
+----------+----------+                  |
|   even   |  prime   |                  |
|          |          |                  |
+----------+----------+------------------+
```

Jeder Agent wird über `opencode run --agent <name>` in einer Shell-Schleife ausgeführt. Die Agent-Rollen sind als Custom Modes in `.opencode/modes/` definiert.

## Voraussetzungen

- [tmux](https://github.com/tmux/tmux)
- [opencode](https://github.com/opencode-ai/opencode) CLI
- GitHub Copilot Zugang (authentifiziert via `gh auth login`)

## Quickstart

```bash
# 1. Repository klonen
git clone <repo-url> && cd the-counting-agents

# 2. Starten
./scripts/start.sh

# 3. tmux-Session anzeigen
tmux attach -t agents
```

## Steuerung

```bash
# Session beenden
./scripts/stop.sh

# State und Logs zurücksetzen
./scripts/reset.sh

# Reset + Neustart
./scripts/reset.sh --restart
```

## Verzeichnisstruktur

```
the-counting-agents/
├── .opencode/modes/    # Agent-Definitionen (Custom Modes)
│   ├── counter.md
│   ├── odd.md
│   ├── even.md
│   ├── prime.md
│   └── control.md
├── opencode.json       # opencode Konfiguration
├── bus/                # Event-Bus (JSONL-Dateien)
│   ├── numbers.log     # Zahlen-Events
│   └── control.log     # Steuerungs-Events
├── state/              # Agent-State (JSON)
├── scripts/            # Shell-Skripte
│   ├── start.sh        # tmux-Session starten
│   ├── stop.sh         # Session beenden
│   ├── reset.sh        # State zurücksetzen
│   └── run-agent.sh    # Agent-Loop-Wrapper
└── spec/               # Spezifikationen
```

## Event-Formate

### Number Event (bus/numbers.log)
```json
{"type":"number","seq":1,"value":1,"timestamp":"2025-01-01T00:00:00Z"}
```

### Control Event (bus/control.log)
```json
{"type":"control","target":"all","command":"stop","timestamp":"2025-01-01T00:00:00Z"}
```

## Konfiguration

Das Model kann in `opencode.json` angepasst werden:

```json
{
  "model": "github-copilot/gpt-4o"
}
```

## Varianten

- **LLM-Variante** (Standard): Agents nutzen `opencode` mit LLM-Entscheidungen
- **Shell-Variante** (geplant): Reine Bash-Skripte ohne LLM — siehe `spec/Shell-Script-Variant-Spec.md`
