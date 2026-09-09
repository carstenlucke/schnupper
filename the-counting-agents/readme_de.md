# The Counting Agents

Eine terminalbasierte Demo eines Multi-Agenten-Systems. Autonome LLM-Agenten kommunizieren über dateibasierte Event-Logs und laufen nebeneinander in einem [Herdr](https://herdr.dev)-Tab — jeder Agent in einem eigenen, benannten Pane.

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
+-------------------------------------------+---------------------+
|             counter · Zähler              | control · Steuerung |
|                   (2/3)                   |        (1/3)        |
+---------------------+---------------------+---------------------+
|   odd · Ungerade    |    even · Gerade    | prime · Primzahlen  |
|        (1/3)        |        (1/3)        |        (1/3)        |
+---------------------+---------------------+---------------------+
```

Jeder Agent läuft über `opencode run --agent <name>` in einer Shell-Schleife. Die Agentenrollen sind als Custom Agents in `.opencode/agents/` definiert.

`start.sh` baut dieses Layout im aktuellen Herdr-Workspace als Tab **Counting Agents** auf und benennt jedes Pane nach dem Agenten, der darin läuft.

## Voraussetzungen

- [Herdr](https://herdr.dev) — die Demo wird aus einem Herdr-Pane heraus gestartet
- [opencode](https://github.com/opencode-ai/opencode) CLI
- [LM Studio](https://lmstudio.ai) mit der CLI `lms` im `PATH` — die Agenten laufen gegen ein lokales Modell, ein Cloud-Zugang ist nicht nötig

## Schnellstart

```bash
# 1. Repository klonen
git clone <repo-url> && cd the-counting-agents

# 2. Herdr starten und ein Pane in diesem Verzeichnis öffnen
herdr

# 3. Demo starten — öffnet den Tab "Counting Agents" und holt ihn nach vorn
./scripts/start.sh
```

`start.sh` ruft zuerst `scripts/start-lmstudio.sh` auf: Das Skript startet den
LM-Studio-Server, lädt das Modell beim ersten Mal herunter und hält es im
Speicher. Vor einer Vorlesung einmal separat aufrufen — dann wartet der erste
Agentendurchlauf nicht auf ein kaltes Modell.

## Steuerung

Das Control-Pane (oben rechts) zeigt ein interaktives Menü, das mit den Pfeiltasten navigiert wird. Von dort aus kann man auf das Status-Dashboard zugreifen, pausieren/fortsetzen, stoppen/zurücksetzen und eigene Anweisungen senden.

```bash
# Aus einem anderen Pane stoppen (schließt auch den Demo-Tab)
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
│   ├── start.sh          # Herdr-Tab öffnen und alle Agenten starten
│   ├── start-lmstudio.sh # LM-Studio-Server starten und Modell laden
│   ├── stop.sh           # Agenten stoppen und Tab schließen
│   ├── herdr-lib.sh      # Gemeinsame Helfer für die Herdr-CLI
│   ├── reset.sh          # Zustand zurücksetzen
│   ├── run-agent.sh      # Agenten-Schleifenwrapper
│   └── run-control.sh    # Interaktives Steuermenü
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

Die Agenten laufen gegen [Qwen3.6 35B-A3B](https://lmstudio.ai/models/qwen/qwen3.6-35b-a3b),
das LM Studio lokal über seine OpenAI-kompatible API bereitstellt. Es ist ein
Mixture-of-Experts-Modell: 35 Mrd. Parameter insgesamt, davon nur 3 Mrd. je Token
aktiv — schnell genug und zugleich stark genug für die mehrstufigen Werkzeugketten,
die diese Agenten brauchen. Provider und
Modell stehen in `opencode.json`:

```json
{
  "model": "lmstudio/qwen/qwen3.6-35b-a3b",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://127.0.0.1:1234/v1" },
      "models": { "qwen/qwen3.6-35b-a3b": { "name": "Qwen3.6 35B-A3B (lokal)" } }
    }
  }
}
```

Jeder Agent wiederholt dasselbe Modell in seinem Frontmatter
(`.opencode/agents/*.md`) und lässt sich damit einzeln umstellen.

`scripts/start-lmstudio.sh` liest vier Umgebungsvariablen — der schnellste Weg,
ein anderes lokales Modell auszuprobieren:

| Variable | Standard | Bedeutung |
|---|---|---|
| `COUNTING_AGENTS_MODEL` | `qwen/qwen3.6-35b-a3b` | Modellschlüssel in LM Studio |
| `COUNTING_AGENTS_PARALLEL` | `5` | Gleichzeitige Vorhersagen — eine je Agent |
| `COUNTING_AGENTS_CONTEXT_PER_AGENT` | `16384` | Kontext, den ein Durchlauf nutzen darf |
| `COUNTING_AGENTS_CONTEXT` | *pro Agent × parallel* (`81920`) | Gesamtkontext des Modells |

`--context-length` bemisst das **gesamte** Modell; LM Studio teilt diesen
Kontext auf die parallelen Slots auf. Ein Durchlauf braucht gemessen gut 10.000
Tokens — bei 16k und fünf Agenten blieben je rund 3k, und jeder Durchlauf
bräche mit „Context size has been exceeded“ ab. Deshalb wird der Gesamtwert
hochgerechnet statt fest gesetzt.

Wer das Modell hier wechselt, ändert es auch in `opencode.json` und im
Frontmatter der Agenten.

## Varianten

- **LLM-Variante** (Standard): Agenten nutzen `opencode` mit LLM-basierten Entscheidungen
- **Shell-Variante** (geplant): Reine Bash-Skripte ohne LLM — siehe `spec/Shell-Script-Variant-Spec.md`
