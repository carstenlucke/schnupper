# Scripts-Dokumentation

Alle Skripte befinden sich in `scripts/` und sind als ausführbare Bash-Skripte mit `set -euo pipefail` implementiert.

## start.sh

Erstellt und startet die tmux-Session `agents` mit 5 Panes (siehe Layout in der README).

**Was passiert beim Start:**
1. Prüft, ob `tmux` und `opencode` installiert sind
2. Beendet eine evtl. vorhandene alte Session
3. Erstellt `bus/` und `state/`-Verzeichnisse, leert die Log-Dateien
4. Initialisiert State-Dateien (`state/*.json`) mit Standardwerten
5. Erstellt das tmux-Layout (4 Agent-Panes links, Control-Pane rechts)
6. Startet die Agents:
   - Pane 0–3: `run-agent.sh <name> <interval>` für counter, odd, even, prime
   - Pane 4: `run-control.sh` (interaktives Menü)

**Verwendung:**
```bash
./scripts/start.sh
tmux attach -t agents
```

## stop.sh

Beendet alle Agents und die tmux-Session.

1. Schreibt ein `{"command":"stop","target":"all"}` Event in `bus/control.log`
2. Wartet 2 Sekunden, damit Agents das Stop-Event erkennen
3. Beendet die tmux-Session `agents`

**Verwendung:**
```bash
./scripts/stop.sh
```

## reset.sh

Setzt Logs und State-Dateien zurück.

1. Leert `bus/numbers.log` und `bus/control.log`
2. Löscht alle State-Dateien (`state/*.json`)

Mit `--restart` wird zusätzlich die Session gestoppt und neu gestartet.

**Verwendung:**
```bash
./scripts/reset.sh            # Nur Reset
./scripts/reset.sh --restart  # Reset + Neustart
```

## run-agent.sh

Generischer Loop-Wrapper für die Filter-Agents (counter, odd, even, prime).

**Parameter:**
- `$1` — Agent-Name (z.B. `counter`, `odd`)
- `$2` — Interval in Sekunden (Standard: 3)

**Verhalten:**
1. Prüft vor jedem Durchlauf, ob ein Stop-Befehl in `bus/control.log` steht (für `all` oder den eigenen Agent-Namen)
2. Ruft `opencode run --agent <name> "Führe deinen nächsten Schritt aus."` auf
3. Wartet das konfigurierte Intervall, dann nächster Durchlauf

**Verwendung:**
```bash
./scripts/run-agent.sh counter 3
./scripts/run-agent.sh prime 5
```

## run-control.sh

Interaktives Steuerungsmenü für den Control-Pane. Ersetzt den generischen `run-agent.sh`-Wrapper für den Control-Agent.

**Menüpunkte:**
| # | Aktion | Implementierung |
|---|--------|-----------------|
| 1 | Status Dashboard anzeigen | `opencode run --agent control` |
| 2 | Counter pausieren | Direktes Schreiben in `bus/control.log` |
| 3 | Counter fortsetzen | Direktes Schreiben in `bus/control.log` |
| 4 | Alle Agents stoppen | Direktes Schreiben in `bus/control.log` |
| 5 | Alle Agents zurücksetzen | Direktes Schreiben in `bus/control.log` |
| 6 | Verbose/Quiet umschalten | Submenu: Agent + Modus wählen, dann in `bus/control.log` |
| 7 | Custom-Anweisung eingeben | Freies Textfeld, wird an `opencode run --agent control` weitergeleitet |

**Bedienung:**
- Pfeiltasten hoch/runter: Auswahl bewegen
- Enter: Aktion ausführen
- `q`: Menü beenden

**Design-Entscheidung:** Einfache Befehle (pause, resume, stop, reset, verbose, quiet) werden direkt per `echo` in `bus/control.log` geschrieben, ohne einen LLM-Aufruf. Nur das Status-Dashboard und Custom-Anweisungen nutzen `opencode run`.
