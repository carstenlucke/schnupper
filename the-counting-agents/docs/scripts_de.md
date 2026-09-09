# Skript-Dokumentation

Alle Skripte befinden sich in `scripts/` und sind als ausführbare Bash-Skripte mit `set -euo pipefail` implementiert.

## start.sh

Legt im aktuellen Workspace den Herdr-Tab **Counting Agents** mit 5 Panes an (siehe Layout in der README). Muss aus einem Herdr-Pane heraus laufen — den Workspace nimmt das Skript aus `$HERDR_WORKSPACE_ID`.

**Was beim Start passiert:**
1. Prüft, ob das Skript in Herdr läuft (`$HERDR_ENV`) und ob `herdr` und `opencode` installiert sind
2. Ruft `start-lmstudio.sh` auf (überspringbar mit `SKIP_LMSTUDIO=1`)
3. Schließt einen bereits vorhandenen Tab **Counting Agents**
4. Erstellt die Verzeichnisse `bus/` und `state/` und leert die Log-Dateien
5. Initialisiert State-Dateien (`state/*.json`) mit Standardwerten
6. Baut das Layout mit `herdr pane split` auf (Counter + Control in der oberen Reihe, Odd/Even/Prime in der unteren Reihe)
7. Benennt jedes Pane per `herdr pane rename` nach dem Agenten, der darin läuft:
   - `counter · Zähler` (oben links, 2/3 breit)
   - `control · Steuerung` (oben rechts, 1/3 breit)
   - `odd · Ungerade`, `even · Gerade`, `prime · Primzahlen` (untere Reihe, je 1/3 breit)
8. Startet die Agenten mit `herdr pane run`: `run-control.sh` im Steuerungs-Pane, `run-agent.sh <name> <intervall>` in den übrigen vier
9. Holt den Tab per `herdr tab focus` nach vorn, der Fokus liegt auf dem Steuerungs-Pane

Aufruf aus einem Pane **außerhalb** des Demo-Tabs — das Skript weigert sich, den Tab zu schließen, in dem es selbst läuft.

**Verwendung:**
```bash
./scripts/start.sh
```

## stop.sh

Stoppt alle Agenten und schließt den Herdr-Tab.

1. Schreibt ein `{"command":"stop","target":"all"}`-Event nach `bus/control.log`
2. Wartet 2 Sekunden, damit die Agenten das Stop-Event aufnehmen können
3. Schließt den Tab **Counting Agents** (außerhalb von Herdr endet das Skript nach Schritt 2 mit einem Hinweis)

**Verwendung:**
```bash
./scripts/stop.sh
```

## reset.sh

Löscht Logs und State-Dateien.

1. Leert `bus/numbers.log` und `bus/control.log`
2. Löscht alle State-Dateien (`state/*.json`)

Mit `--restart` wird der Demo-Tab zusätzlich geschlossen und neu aufgebaut.

**Verwendung:**
```bash
./scripts/reset.sh            # Nur zurücksetzen
./scripts/reset.sh --restart  # Zurücksetzen + Neustart
```

## start-lmstudio.sh

Bringt das lokale Modell in Betrieb. Wird von `start.sh` aufgerufen, lohnt sich
aber auch als separater Aufruf vor einer Vorlesung — ein kaltes Modell zu laden
dauert lange genug, um auf der Bühne unangenehm zu werden.

1. Startet den LM-Studio-Server, falls er nicht schon läuft (`lms server start`)
2. Lädt das Modell beim ersten Mal herunter (`lms get`)
3. Lädt es in den Speicher, falls es nicht bereits **mit dem nötigen Kontext und der nötigen Parallelität** geladen ist (`lms load`) — ein aus einem früheren Lauf mit kleinerem Kontext übrig gebliebenes Modell wird entladen und neu geladen

Jeder Schritt ist idempotent, wiederholte Aufrufe kosten also nichts.

**Umgebungsvariablen:**
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

**Verwendung:**
```bash
./scripts/start-lmstudio.sh
```

## herdr-lib.sh

Gemeinsame Helfer für `start.sh` und `stop.sh`, per `source` eingebunden — nicht zum direkten Aufruf gedacht.

- `herdr_require` — prüft, ob `herdr` installiert ist und der Aufruf aus einem Herdr-Pane kommt
- `herdr_demo_tab_id` — ermittelt die Tab-ID des Tabs **Counting Agents** im aktuellen Workspace
- `herdr_split` — teilt ein Pane und gibt die ID des neuen Panes zurück

Die Herdr-CLI antwortet in einzeiligem JSON, das hier mit `tr`/`grep`/`sed` ausgewertet wird. `jq` wird nicht benötigt.

## run-agent.sh

Generischer Schleifenwrapper für die Filter-Agenten (counter, odd, even, prime).

**Parameter:**
- `$1` — Agentenname (z.B. `counter`, `odd`)
- `$2` — Intervall in Sekunden (Standard: 3)

**Verhalten:**
1. Prüft vor jedem Zyklus, ob ein Stop-Befehl für `all` oder den eigenen Agentennamen in `bus/control.log` vorhanden ist
2. Setzt `XDG_DATA_HOME` auf `.opencode-data/<agent>`, sodass jeder Agent seine eigene opencode-Datenbank bekommt. Teilen sich alle die Standarddatenbank in `~/.local/share/opencode`, brechen vier der fünf Prozesse sofort mit `database is locked` ab, weil sie auf dieselbe SQLite-Datei schreiben. `start.sh` räumt das Verzeichnis bei jedem Start weg.
3. Ruft `opencode run --agent <name> "Execute your next step."` auf
4. Bricht den Durchlauf nach `COUNTING_AGENTS_TIMEOUT` Sekunden ab (Standard 240) — gegen ein lokales Modell bleibt `opencode` gelegentlich hängen, ohne Wachhund stünde das Pane für den Rest der Vorführung still. Fragen alle fünf Agenten gleichzeitig an, dauert ein Durchlauf gemessen 85–115 Sekunden; die Grenze muss deutlich darüber liegen, sonst schneidet sie den Normalbetrieb ab
5. Wartet das konfigurierte Intervall, dann startet der nächste Zyklus

**Verwendung:**
```bash
./scripts/run-agent.sh counter 3
./scripts/run-agent.sh prime 5
```

## run-control.sh

Interaktives Steuermenü für das Control-Pane. Ersetzt den generischen `run-agent.sh`-Wrapper für den Control-Agenten.

**Menüpunkte:**
| # | Aktion | Implementierung |
|---|--------|-----------------|
| 1 | Status-Dashboard anzeigen | `opencode run --agent control` |
| 2 | Counter pausieren | Schreibt direkt nach `bus/control.log` |
| 3 | Counter fortsetzen | Schreibt direkt nach `bus/control.log` |
| 4 | Alle Agenten stoppen | Schreibt direkt nach `bus/control.log` |
| 5 | Alle Agenten zurücksetzen | Schreibt direkt nach `bus/control.log` |
| 6 | Verbose/Quiet umschalten | Untermenü: Agent + Modus wählen, dann nach `bus/control.log` schreiben |
| 7 | Eigene Anweisung eingeben | Freitext-Eingabe, wird an `opencode run --agent control` weitergeleitet |

**Navigation:**
- Pfeiltasten hoch/runter: Auswahl bewegen
- Enter: Aktion ausführen
- `q`: Menü verlassen

**Design-Entscheidung:** Einfache Befehle (Pause, Fortsetzen, Stoppen, Zurücksetzen, Verbose, Quiet) werden direkt per `echo` nach `bus/control.log` geschrieben, ohne LLM-Aufruf. Nur das Status-Dashboard und eigene Anweisungen verwenden `opencode run`.
