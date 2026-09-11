# CLAUDE.md

**The Counting Agents (pi)** — Terminal-Demo für eine Schnuppervorlesung, mit
der **pi CLI**, **eigenen Werkzeugen** (Custom Tools) und einem **Modell in der
Cloud**. Fünf Agenten koordinieren sich über dateibasierte Event-Logs in einem
[Herdr](https://herdr.dev)-Tab, darunter ein Dashboard für den Beamer.

> Hervorgegangen aus der OpenCode-Fassung `the-counting-agents/`, die aus dem
> Repo entfernt ist (letzter Stand: Commit `4d77661`). Der Vergleich mit ihr
> bleibt der didaktische Gegenstand — die Doku bezieht sich weiter darauf.

## Der Unterschied zur OpenCode-Fassung

Das ist kein Implementierungsdetail, sondern der Zweck des Projekts — beim
Ändern nicht wegoptimieren:

- **Eigene Werkzeuge statt generischer.** `bus_publish {"value": 42}` statt
  `bash echo '{"type":"number",...}' >> _bus/numbers.log`. Dadurch schrumpfen
  die Agent-Prompts von zwei Seiten Fehlerbehandlung auf ein Dutzend Zeilen
  Aufgabenbeschreibung.
- **Keine eingebauten Werkzeuge.** Kein `bash`, kein `read`, kein `write`
  (Flag `-nbt`). Jeder Agent kann genau das, was seine Rolle verlangt — der
  Counter darf veröffentlichen, die Sammler dürfen nur lesen. Einem Agenten im
  Vortrag ein Werkzeug wegzunehmen und zuzusehen, was passiert, ist Teil der
  Demo.

## Einrichten

```bash
cp .env.example .env          # COUNTING_AGENTS_MODEL eintragen
node scripts/test-tools.mjs   # Werkzeuge prüfen — ohne Modell, ohne Netz, ohne Kosten
./scripts/dev-typen.sh        # optional: Typen für den Editor auflösen
```

`dev-typen.sh` legt nur Verweise auf Pakete an, die in der installierten pi-CLI
ohnehin liegen. Das Projekt bringt **absichtlich kein `node_modules`** mit; rote
Fehler im Editor sind erwartbar, pi löst die Importe mit eigenem
TypeScript-Lader auf.

## Starten & Stoppen

Aus einem Herdr-Pane heraus, im Projektverzeichnis:

| Befehl | Wirkung |
|---|---|
| `./scripts/start.sh` | Tab anlegen, fünf Agenten und Dashboard starten |
| `./scripts/start.sh --ohne-dashboard` | Nur die fünf Agenten-Panes |
| `./scripts/start.sh --speed 1.5` | Anderthalbfaches Tempo, `0.5` halbes |
| `./scripts/stop.sh` | Alle stoppen, Tab schließen |
| `./scripts/reset.sh [--restart]` | Bus und Zustand leeren, optional neu starten |

Im Steuerungs-Pane: Pfeiltasten wählen, Enter führt aus, `q` beendet.

## Architektur

```
+--------------------+----------+
|  counter · Zähler  | control ·|
|                    | Steuerung|
+----------+---------+----------+
|   odd ·  | even ·  | prime ·  |
| Ungerade | Gerade  |Primzahlen|
+----------+---------+----------+
|     dashboard · Übersicht     |
+-------------------------------+
```

| Datei | Inhalt |
|---|---|
| `_bus/numbers.log` | Zahlen-Events des Counters (append-only) |
| `_bus/control.log` | Steuerbefehle: `pause`, `resume`, `stop`, `reset`, `verbose`, `quiet` |
| `_state/<agent>.json` | Was ein Agent sich gemerkt hat |

Der **Unterstrich** ist Absicht: Die Verzeichnisse entstehen zur Laufzeit, sind
gitignored (nur `.gitkeep` versioniert) und sortieren sich so von den
bearbeiteten Verzeichnissen ab.

## Agenten: agents/

pi hat **kein eingebautes Agenten-Konzept**. Ein Agent ist eine Markdown-Datei;
`scripts/run-agent.sh` liest das Frontmatter und baut daraus den Aufruf.

```markdown
---
description: Erzeugt fortlaufende Zahlen und stellt sie in den Event-Bus
model: openai-codex/gpt-5.6-luna
tools: bus_publish,control_read,state_read,state_write
thinking: off
interval: 3
---
```

| Agent | Werkzeuge | Besonderheit |
|---|---|---|
| `counter` | `bus_publish`, `control_read`, `state_read`, `state_write` | Eine Zahl pro Durchlauf |
| `odd` / `even` | `bus_read`, `control_read`, `state_read`, `state_write` | Nur lesend auf dem Bus |
| `prime` | wie odd/even | Einziger mit `thinking: low` — man soll ihn überlegen sehen |
| `control` | `state_read`, `bus_read`, `control_send` | Kein `interval`, läuft im Menü |

Die Werkzeug-Allowlist je Agent ist **didaktisch gemeint** — nicht großzügiger
setzen, um einen Durchlauf zu retten.

## Werkzeuge: .pi/extensions/

| Datei | Zweck |
|---|---|
| `counting-tools.ts` | Die sechs Werkzeuge: `bus_publish`, `bus_read`, `control_read`, `control_send`, `state_read`, `state_write` |
| `tensorx-schnupper.ts` | Meldet TensorX unter eigenem Namen an, mit eigenem Schlüssel und `max_tokens: 4096` |

Nach Änderungen an den Werkzeugen `node scripts/test-tools.mjs` laufen lassen —
prüft sie direkt, ohne Modell und ohne Kosten. Hintergrund:
[`docs/pi-custom-tools_de.md`](docs/pi-custom-tools_de.md).

## Modell und Rate-Limits

`COUNTING_AGENTS_MODEL` in der `.env` **schlägt den `model:`-Eintrag aller
Agenten zugleich** — der Weg, im Hörsaal den Anbieter zu wechseln, wenn einer
bremst. Voreinstellung `openai-codex/gpt-5.6-luna`.

- Steht dort ein `tensorx-schnupper/...`-Modell, braucht es zusätzlich
  `SCHNUPPER_TENSORX_API_KEY`. Das ist **bewusst ein eigener, vom global in pi
  hinterlegten Zugang getrennter Schlüssel** — Vorlesungs- und Alltagskosten
  bleiben auseinander.
- Nicht jedes Modell aus `pi --list-models` ist freigegeben. Vor der Vorlesung
  einmal starten und zusehen, ob Zahlen erscheinen.
- **Ein Durchlauf ist nicht eine Anfrage**, sondern eine je Werkzeugaufruf plus
  eine für die Abschlussantwort — rund fünf für die eine Zeile `→ 42`. Vier
  Agenten im Dauerlauf erzeugen etwa **90 Anfragen pro Minute**; das
  Standard-Kontingent von TensorX erlaubt 60. Gegenmittel: Anbieter wechseln,
  `--speed` strecken, oder weniger Agenten laufen lassen. Details in
  `readme_de.md`, Abschnitt „Anfragen zählen".

`AGENT_SPEED` (Umgebung oder `.env`) staucht den Takt aller Agenten gemeinsam;
`--speed` im Aufruf hat Vorrang. Dass `prime` hinterherhinkt, liegt an seinem
Nachdenken, nicht am Intervall.

## Skripte: scripts/

| Skript | Zweck |
|---|---|
| `start.sh` / `stop.sh` / `reset.sh` | Tab aufbauen, stoppen, zurücksetzen |
| `run-agent.sh <name>` | Schleifenwrapper: Frontmatter lesen, pi aufrufen |
| `run-control.sh` | Interaktives Steuermenü |
| `agents-lib.sh` | `load_env`, `agent_meta`, `agent_interval`, `run_pi` — per `source` |
| `herdr-lib.sh` | Helfer für die Herdr-CLI |
| `dashboard.py` | Dashboard-Server für den Beamer |
| `dashboard-probelauf.py` | Simulator für die Generalprobe ohne Modell |
| `test-tools.mjs` | Werkzeuge ohne Modell prüfen |
| `dev-typen.sh` | Typen für den Editor auflösen |

Der pi-Aufruf in `run_pi` (agents-lib.sh) hängt an fünf Flags:

| Flag | Wirkung |
|---|---|
| `-p` | Einmal antworten und beenden, kein interaktives Fenster |
| `-nc` | CLAUDE.md/AGENTS.md ignorieren — der Agent kennt nur seinen Prompt |
| `-nbt` | Keine eingebauten Werkzeuge (siehe oben) |
| `-a` | Die projektlokale `.pi/` als vertrauenswürdig behandeln, damit die Extensions laden |
| `--no-session` | Kein Gesprächsverlauf; jeder Durchlauf beginnt bei null |

**`-nc` heißt: Diese Datei hier erreicht die Demo-Agenten nicht.** Sie ist für
Coding-Agenten gedacht, die am Projekt arbeiten — die Demo-Agenten bekommen
ausschließlich den Text unter dem Frontmatter ihrer Datei.

Die Schleife wertet `pause`/`stop` **selbst** aus, statt dafür das Modell zu
fragen — ein pausierter Agent soll nichts kosten. Der Wachhund
(`COUNTING_AGENTS_TIMEOUT`, Standard 60s) killt erst das pi-Kind, dann die
Subshell; andernfalls schreibt ein Nachzügler Minuten später einen überholten
Stand in den Bus.

## Dashboard

`scripts/dashboard.py` (Port 8777, `--kein-browser`, Port als Argument) liest
Bus und Zustand und **schreibt nie** — es kann die Demo nicht stören.
Server-Sent Events, nur Standardbibliothek, kein Build. Farben nach dem
[Corporate Design der THM](https://go.thm.de/cd).

Das Dashboard rechnet **selbst nach**, welche Zahlen prim sind, und färbt
Fehlgriffe des Prim-Agenten rot. Dieser Fall ist der beste Moment der
Vorlesung — nicht wegkürzen.

`dashboard-probelauf.py` schreibt in dieselben Dateien wie die echten Agenten
und darf **nicht parallel zu `./scripts/start.sh`** laufen.

## Konventionen

- **Sprache Deutsch** in Code-Kommentaren, Agent-Prompts, Ausgaben und
  Commit-Messages.
- **Doku zweisprachig**: zu jeder `*.md` in `docs/` und zur `README.md` gehört
  eine deutsche Fassung `*_de.md`. **Beide Fassungen zusammen ändern.**
- **Secrets nur in `.env`**, nie im Repo. `.env.example` ist die Vorlage.
- **Bash mit `set -euo pipefail`**, kein `jq`, keine npm-Abhängigkeiten.
- **Vorführbarkeit vor Eleganz.** Sichtbare Zwischenschritte und Wartezeiten
  sind der Zweck, nicht das Problem.

## Weiterlesen

- [`docs/experiment_de.md`](docs/experiment_de.md) — warum die Architektur so
  aussieht; bewusste Entscheidungen, keine offenen Aufgaben
- [`docs/Trajectory_de.md`](docs/Trajectory_de.md) — was bei einem Durchlauf
  wirklich passiert: Anfragen, Werkzeugaufrufe, wachsender Kontext
- [`docs/pi-custom-tools_de.md`](docs/pi-custom-tools_de.md) — wie die
  Werkzeuge gebaut sind
