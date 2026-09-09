# The Counting Agents

Eine terminalbasierte Demo eines Multi-Agenten-Systems. Autonome LLM-Agenten kommunizieren über dateibasierte Event-Logs und laufen in einer tmux-Session.

## Konzept

Fünf Agenten arbeiten zusammen:

- **Counter** — Erzeugt einen sequenziellen Zahlenstrom und schreibt ihn auf den Event-Bus
- **Odd** — Filtert und sammelt ungerade Zahlen
- **Even** — Filtert und sammelt gerade Zahlen
- **Prime** — Erkennt Primzahlen (absichtlich langsamer)
- **Control** — Zeigt ein Status-Dashboard an und sendet Steuerbefehle

Die Agenten kommunizieren ausschließlich über Append-only-JSONL-Dateien im Verzeichnis `bus/`. Jeder Agent persistiert seinen Zustand in `state/`.

## Architektur

```
+--------------------+----------+
|     counter        | control  |
|      (2/3)         |  (1/3)   |
+----------+---------+----------+
|   odd    |  even   |  prime   |
|  (1/3)   |  (1/3)  |  (1/3)  |
+----------+---------+----------+
```

Jeder Agent läuft über `opencode run --agent <name>` in einer Shell-Schleife. Die Agentenrollen sind als Custom Agents in `.opencode/agents/` definiert.

## Voraussetzungen

- [tmux](https://github.com/tmux/tmux)
- [opencode](https://github.com/opencode-ai/opencode) CLI
- GitHub-Copilot-Zugang (authentifiziert über `gh auth login`)

## Schnellstart

```bash
# 1. Repository klonen
git clone <repo-url> && cd the-counting-agents

# 2. Starten
./scripts/start.sh

# 3. An die tmux-Session anhängen
tmux attach -t agents
```

## Steuerung

Das Control-Pane (oben rechts) zeigt ein interaktives Menü, das mit den Pfeiltasten navigiert wird. Von dort aus kann man auf das Status-Dashboard zugreifen, pausieren/fortsetzen, stoppen/zurücksetzen und eigene Anweisungen senden.

```bash
# Session von außen stoppen
./scripts/stop.sh

# Zustand und Logs löschen
./scripts/reset.sh

# Zurücksetzen + Neustart
./scripts/reset.sh --restart
```

Ausführliche Skript-Dokumentation: [docs/scripts_de.md](docs/scripts_de.md)

Hintergrund zum Experiment und bewusste Architekturentscheidungen: [docs/experiment_de.md](docs/experiment_de.md)

Opencode als Custom-Agent-Plattform nutzen: [docs/opencode-custom-agents_de.md](docs/opencode-custom-agents_de.md)

## Verzeichnisstruktur

```
the-counting-agents/
├── .opencode/agents/   # Agentendefinitionen (Custom Agents)
│   ├── counter.md
│   ├── odd.md
│   ├── even.md
│   ├── prime.md
│   └── control.md
├── opencode.json       # opencode-Konfiguration
├── bus/                # Event-Bus (JSONL-Dateien)
│   ├── numbers.log     # Zahlen-Events
│   └── control.log     # Steuer-Events
├── state/              # Agentenzustand (JSON)
├── scripts/            # Shell-Skripte (Details: docs/scripts_de.md)
│   ├── start.sh        # tmux-Session starten
│   ├── stop.sh         # Session stoppen
│   ├── reset.sh        # Zustand zurücksetzen
│   ├── run-agent.sh    # Agenten-Schleifenwrapper
│   └── run-control.sh  # Interaktives Steuermenü
└── spec/               # Spezifikationen
```

## Event-Formate

### Zahlen-Event (bus/numbers.log)
```json
{"type":"number","seq":1,"value":1,"timestamp":"2025-01-01T00:00:00Z"}
```

### Steuer-Event (bus/control.log)
```json
{"type":"control","target":"all","command":"stop","timestamp":"2025-01-01T00:00:00Z"}
```

## Konfiguration

Das Modell kann in `opencode.json` geändert werden:

```json
{
  "model": "github-copilot/gpt-4o"
}
```

## Varianten

- **LLM-Variante** (Standard): Agenten nutzen `opencode` mit LLM-basierten Entscheidungen
- **Shell-Variante** (geplant): Reine Bash-Skripte ohne LLM — siehe `spec/Shell-Script-Variant-Spec.md`
