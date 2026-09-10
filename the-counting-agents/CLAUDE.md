# CLAUDE.md

**The Counting Agents** — Terminal-Demo für eine Schnuppervorlesung. Fünf
LLM-Agenten koordinieren sich ausschließlich über dateibasierte Event-Logs und
laufen nebeneinander in einem [Herdr](https://herdr.dev)-Tab, je ein benanntes
Pane pro Agent.

Laufzeit ist die **OpenCode CLI** gegen ein **lokal über LM Studio**
bereitgestelltes Modell — kein Cloud-Zugang, kein Netz nötig.

> Das Schwesterprojekt `the-counting-agents-pi-herdr/` zeigt dieselbe Demo mit
> der pi CLI. Beide sind absichtlich getrennt; der Vergleich ist der
> didaktische Gegenstand. **Eine Änderung hier ist keine Anweisung, das andere
> Projekt nachzuziehen.**

## Starten & Stoppen

Alle Skripte laufen **aus einem Herdr-Pane heraus**, aus dem Projektverzeichnis
und **außerhalb** des Demo-Tabs — `start.sh` weigert sich, den Tab zu
schließen, in dem es selbst läuft.

```bash
./scripts/start-lmstudio.sh   # Modell vorab laden (vor der Vorlesung einmal separat)
./scripts/start.sh            # Tab "Counting Agents" anlegen, 5 Agenten starten
./scripts/stop.sh             # Stop-Event schreiben, Tab schließen
./scripts/reset.sh            # bus/ und state/ leeren
./scripts/reset.sh --restart  # Leeren und neu starten
```

`SKIP_LMSTUDIO=1 ./scripts/start.sh` überspringt den Modellstart.

## Architektur

```
+-------------------------------------------+---------------------+
|             counter · Zähler              | control · Steuerung |
|                   (2/3)                   |        (1/3)        |
+---------------------+---------------------+---------------------+
|   odd · Ungerade    |    even · Gerade    | prime · Primzahlen  |
+---------------------+---------------------+---------------------+
```

Jeder Agent läuft in einer Shell-Schleife (`run-agent.sh`), die pro Zyklus
einmal `opencode run --agent <name>` aufruft. Kommunikation ausschließlich über
zwei Append-only-JSONL-Dateien:

| Datei | Inhalt |
|---|---|
| `bus/numbers.log` | Zahlen-Events des Counters |
| `bus/control.log` | Steuerbefehle: `pause`, `resume`, `stop`, `reset`, `verbose`, `quiet` |
| `state/<agent>.json` | Was ein Agent sich gemerkt hat |

```json
{"type":"number","seq":1,"value":1,"timestamp":"2025-01-01T00:00:00Z"}
{"type":"control","target":"all","command":"stop","timestamp":"2025-01-01T00:00:00Z"}
```

`bus/` und `state/` sind gitignored (nur `.gitkeep` versioniert).

## Agenten: .opencode/agents/

Fünf Markdown-Dateien mit YAML-Frontmatter (`description`, `model`, `tools`).
Die Agenten arbeiten mit den **allgemeinen** OpenCode-Werkzeugen `bash`, `read`
und `write` — sie bauen ihr JSON selbst zusammen. Genau das ist der Kontrast
zum pi-Projekt, das dafür eigene Werkzeuge hat.

| Agent | Aufgabe |
|---|---|
| `counter` | Erzeugt fortlaufende Zahlen, ein Event pro Durchlauf |
| `odd` / `even` | Filtern und sammeln ungerade bzw. gerade Zahlen |
| `prime` | Erkennt Primzahlen, hinkt absichtlich hinterher |
| `control` | Status-Dashboard und Steuerbefehle |

**Beim Ändern eines Systemprompts sind vier Dinge kritisch** — sie stehen so in
den Agentendateien, weil ohne sie Durchläufe reihenweise scheitern:

- **Relative Pfade, nie mit führendem Schrägstrich.** `state/counter.json` ist
  richtig, `/state/counter.json` wird abgewiesen.
- **Anhängen nur per `bash` mit `echo '...' >> bus/numbers.log`.** Das Werkzeug
  `write` überschreibt und zerstört den Bus.
- **Leere Dateien (0 Bytes) vorher mit `wc -c` prüfen** — das Read-Werkzeug
  läuft sonst in einen Offset-Fehler.
- **BSD-`date`**, nicht GNU: `date -u +%Y-%m-%dT%H:%M:%SZ`. Formate wie `%3N`
  landen wörtlich im Log.

Die Prompts sind lang und defensiv. Das ist kein Aufräumbedarf, sondern der
Preis dafür, dass die Agenten nur generische Werkzeuge haben.

## Skripte: scripts/

Ausführliche Fassung: [`docs/scripts_de.md`](docs/scripts_de.md).

| Skript | Zweck |
|---|---|
| `start.sh` | Herdr-Tab aufbauen, Panes benennen, Agenten starten |
| `stop.sh` / `reset.sh` | Stoppen, zurücksetzen |
| `run-agent.sh <name> [intervall]` | Schleifenwrapper für counter/odd/even/prime |
| `run-control.sh` | Interaktives Steuermenü (Pfeiltasten, Enter, `q`) |
| `start-lmstudio.sh` | LM-Studio-Server starten, Modell laden |
| `herdr-lib.sh` | Helfer für die Herdr-CLI, per `source` eingebunden |

Zwei Details in `run-agent.sh`, die nicht offensichtlich sind:

- **`XDG_DATA_HOME` je Agent** auf `.opencode-data/<agent>`. Ohne das teilen
  sich alle fünf Prozesse dieselbe SQLite-Datei und vier brechen sofort mit
  `database is locked` ab.
- **Wachhund `COUNTING_AGENTS_TIMEOUT`** (Standard 240s). Gegen ein lokales
  Modell bleibt `opencode` gelegentlich hängen. Ein normaler Durchlauf dauert
  bei fünf gleichzeitigen Agenten 85–115s — die Grenze muss deutlich darüber
  liegen.

`run-control.sh` schreibt einfache Befehle (Pause, Stop, Reset, Verbose)
**direkt** in `bus/control.log`, ohne Modellaufruf. Nur Dashboard und Freitext
gehen über `opencode run`.

## Modell und Konfiguration

Voreingestellt ist `lmstudio/qwen/qwen3.6-35b-a3b` über die
OpenAI-kompatible API von LM Studio (`http://127.0.0.1:1234/v1`).

**Das Modell steht an drei Stellen** — wer es wechselt, ändert alle drei:

1. `opencode.json` (Default-Modell und Provider)
2. Frontmatter jeder Datei in `.opencode/agents/`
3. `COUNTING_AGENTS_MODEL` für `start-lmstudio.sh`

`start-lmstudio.sh` liest vier Variablen:

| Variable | Standard |
|---|---|
| `COUNTING_AGENTS_MODEL` | `qwen/qwen3.6-35b-a3b` |
| `COUNTING_AGENTS_PARALLEL` | `5` |
| `COUNTING_AGENTS_CONTEXT_PER_AGENT` | `16384` |
| `COUNTING_AGENTS_CONTEXT` | pro Agent × parallel (`81920`) |

`--context-length` bemisst das **gesamte** Modell, LM Studio teilt es auf die
parallelen Slots auf. Deshalb wird der Gesamtwert hochgerechnet statt fest
gesetzt — sonst bricht jeder Durchlauf mit „Context size has been exceeded" ab.

## Konventionen

- **Sprache Deutsch** in Code-Kommentaren, Agent-Prompts, Ausgaben und
  Commit-Messages.
- **Doku zweisprachig**: zu jeder `*.md` in `docs/` und zur `README.md` gehört
  eine deutsche Fassung `*_de.md`. **Beide Fassungen zusammen ändern.**
- **Bash mit `set -euo pipefail`**, keine externen Abhängigkeiten. Die
  Herdr-CLI antwortet in einzeiligem JSON, das mit `tr`/`grep`/`sed`
  ausgewertet wird — `jq` wird bewusst nicht vorausgesetzt.
- **Vorführbarkeit vor Eleganz.** Sichtbare Zwischenschritte und Wartezeiten
  sind der Zweck, nicht das Problem.

## Absichtliche Einfachheit

[`docs/experiment_de.md`](docs/experiment_de.md) begründet die
Architekturentscheidungen — vollständiges Lesen der Logs, keine
Acknowledgements, kein Locking, keine Log-Rotation, kein Schema. Das sind
bewusste Entscheidungen, keine offenen Aufgaben. **Vor einem „Aufräumen" dort
nachlesen.**

`spec/Shell-Script-Variant-*.md` beschreibt eine geplante LLM-freie Variante —
Planung, nicht Rückstand.
