# Skript-Dokumentation

Alle Skripte befinden sich in `scripts/` und sind als ausführbare Bash-Skripte mit `set -euo pipefail` implementiert.

## start.sh

Erstellt und startet die tmux-Session `agents` mit 5 Panes (siehe Layout in der README).

**Was beim Start passiert:**
1. Prüft, ob `tmux` und `opencode` installiert sind
2. Beendet eine eventuell vorhandene Session gleichen Namens
3. Erstellt die Verzeichnisse `bus/` und `state/` und leert die Log-Dateien
4. Initialisiert State-Dateien (`state/*.json`) mit Standardwerten
5. Baut das tmux-Layout auf (Counter + Control in der oberen Reihe, Odd/Even/Prime in der unteren Reihe)
6. Startet die Agenten:
   - Pane 0: Counter (oben links, 2/3 breit)
   - Pane 1: Control (oben rechts, 1/3 breit) über `run-control.sh`
   - Panes 2–4: `run-agent.sh <name> <intervall>` für odd, even, prime (untere Reihe, je 1/3 breit)

**Verwendung:**
```bash
./scripts/start.sh
tmux attach -t agents
```

## stop.sh

Stoppt alle Agenten und beendet die tmux-Session.

1. Schreibt ein `{"command":"stop","target":"all"}`-Event nach `bus/control.log`
2. Wartet 2 Sekunden, damit die Agenten das Stop-Event aufnehmen können
3. Beendet die tmux-Session `agents`

**Verwendung:**
```bash
./scripts/stop.sh
```

## reset.sh

Löscht Logs und State-Dateien.

1. Leert `bus/numbers.log` und `bus/control.log`
2. Löscht alle State-Dateien (`state/*.json`)

Mit `--restart` wird die Session zusätzlich gestoppt und neu gestartet.

**Verwendung:**
```bash
./scripts/reset.sh            # Nur zurücksetzen
./scripts/reset.sh --restart  # Zurücksetzen + Neustart
```

## run-agent.sh

Generischer Schleifenwrapper für die Filter-Agenten (counter, odd, even, prime).

**Parameter:**
- `$1` — Agentenname (z.B. `counter`, `odd`)
- `$2` — Intervall in Sekunden (Standard: 3)

**Verhalten:**
1. Prüft vor jedem Zyklus, ob ein Stop-Befehl für `all` oder den eigenen Agentennamen in `bus/control.log` vorhanden ist
2. Ruft `opencode run --agent <name> "Execute your next step."` auf
3. Wartet das konfigurierte Intervall, dann startet der nächste Zyklus

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
