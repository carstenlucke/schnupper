# The Counting Agents (pi)

Fünf Agenten zählen gemeinsam. Einer erzeugt Zahlen, drei schauen sie sich an,
einer steuert das Ganze. Sie reden nicht miteinander — sie legen Nachrichten in
eine gemeinsame Datei, und jeder liest, was ihn angeht.

Die Demo läuft in einem Herdr-Tab mit fünf Panes und ist für eine
Schnuppervorlesung gebaut: Man sieht in Echtzeit, wie Agenten arbeiten,
aufeinander warten, sich pausieren lassen und wieder anlaufen.

> Englische Fassung: [README.md](README.md)

## Was hier anders ist als in `the-counting-agents`

Das Schwesterprojekt macht dasselbe mit der **OpenCode CLI** und einem lokal
über LM Studio bereitgestellten Modell. Dieses Projekt nutzt die **pi CLI** und
ein Modell in der Cloud — und vor allem: **eigene Werkzeuge**.

Bei OpenCode erledigen die Agenten ihre Arbeit mit den allgemeinen Werkzeugen
`bash`, `read` und `write`. Sie bauen JSON von Hand zusammen, hängen es per
`echo >>` an eine Datei an, erzeugen Zeitstempel, fangen leere Dateien ab. Was
im Pane erscheint, ist eine Shell-Zeile.

Hier bekommt jeder Handgriff ein eigenes Werkzeug mit sprechendem Namen:

```
bus_publish {"value": 42}
```

Statt:

```
bash echo '{"type":"number","seq":42,"value":42,"timestamp":"..."}' >> _bus/numbers.log
```

Für ein Publikum ohne Programmiererfahrung ist das der ganze Unterschied. Und
die Agent-Prompts schrumpfen von zwei Seiten Fehlerbehandlung auf zwölf Zeilen
Aufgabenbeschreibung.

Zweiter Unterschied: Die Agenten haben **keine** eingebauten Werkzeuge. Kein
`bash`, kein `read`, kein `write`. Jeder kann genau das, was seine Rolle
verlangt — der Counter darf veröffentlichen, die Sammler dürfen nur lesen.
Das lässt sich im Vortrag vorführen: einem Agenten ein Werkzeug wegnehmen und
zusehen, was passiert.

## Aufbau

```
+--------------------+----------+
|  counter · Zähler  | control ·|
|                    | Steuerung|
+----------+---------+----------+
|   odd ·  | even ·  | prime ·  |
| Ungerade | Gerade  |Primzahlen|
+----------+---------+----------+
```

| Agent | Aufgabe | Werkzeuge |
|---|---|---|
| `counter` | Erzeugt fortlaufende Zahlen | `bus_publish`, `control_read`, `state_read`, `state_write` |
| `odd` | Sammelt die ungeraden | `bus_read`, `control_read`, `state_read`, `state_write` |
| `even` | Sammelt die geraden | `bus_read`, `control_read`, `state_read`, `state_write` |
| `prime` | Prüft auf Primzahlen, eine pro Durchlauf | `bus_read`, `control_read`, `state_read`, `state_write` |
| `control` | Zeigt den Zustand, schickt Befehle | `state_read`, `bus_read`, `control_send` |

Kommuniziert wird über zwei Dateien, an die nur angehängt wird:

- `_bus/numbers.log` — die Zahlen, die der Counter veröffentlicht
- `_bus/control.log` — Steuerbefehle (pause, resume, stop, reset, verbose, quiet)

Was jeder Agent sich gemerkt hat, steht in `_state/<agent>.json`.

Beide Verzeichnisse beginnen mit einem Unterstrich: Sie entstehen erst zur
Laufzeit, gehören nicht ins Repository und sortieren sich so von selbst über
die Verzeichnisse, die man tatsächlich bearbeitet.

## Voraussetzungen

- [Herdr](https://herdr.dev) — die Demo läuft in einem Herdr-Tab
- [pi](https://pi.dev) — die Agenten-Laufzeit (`pi --version`)
- Ein TensorX-Schlüssel für das Modell `qwen/qwen3.8-flash-next`

## Einrichten

```bash
cp .env.example .env
# SCHNUPPER_TENSORX_API_KEY eintragen
```

Der Schlüssel gilt nur für dieses Projekt. Ein global in pi hinterlegter
TensorX-Zugang bleibt unberührt: Die Demo meldet denselben Endpunkt unter
eigenem Namen an (`tensorx-schnupper`, siehe
[`.pi/extensions/tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts)).
So sind Vorlesungs- und Alltagskosten getrennt, und der Schlüssel lässt sich
nach dem Semester einzeln zurückziehen.

Vor der Vorlesung einmal prüfen, ob die Werkzeuge tun, was sie sollen — ohne
Modell, ohne Netz, ohne Kosten:

```bash
node scripts/test-tools.mjs
```

## Starten

Aus einem Herdr-Pane heraus, im Projektverzeichnis:

```bash
./scripts/start.sh
```

Das legt den Tab „Counting Agents (pi)" mit fünf Panes an und startet in jedem
einen Agenten. Der Fokus landet auf der Steuerung.

| Befehl | Wirkung |
|---|---|
| `./scripts/start.sh` | Tab anlegen, Agenten starten |
| `./scripts/stop.sh` | Alle stoppen, Tab schließen |
| `./scripts/reset.sh` | Bus und Zustand leeren |
| `./scripts/reset.sh --restart` | Leeren und neu starten |

Im Steuerungs-Pane: Pfeiltasten zur Auswahl, Enter zum Ausführen, `q` beendet
die Demo.

## Was ein Agent ist

Eine Textdatei. Mehr nicht.

```markdown
---
description: Erzeugt fortlaufende Zahlen und stellt sie in den Event-Bus
model: tensorx-schnupper/qwen/qwen3.8-flash-next
tools: bus_publish,control_read,state_read,state_write
thinking: off
interval: 3
---

# Counter-Agent

Du bist der **Counter**. Du erzeugst fortlaufende Zahlen — sonst nichts.
...
```

Der Kopf sagt, welches Modell rechnet, welche Werkzeuge erlaubt sind, wie oft
der Agent aufgerufen wird und ob er nachdenken darf. Darunter steht in
normalem Deutsch, was er tun soll. `scripts/run-agent.sh` liest die Datei und
baut daraus den pi-Aufruf.

Der `prime`-Agent ist der einzige mit `thinking: low` — man soll sehen, wie er
bei der Primzahlprüfung überlegt, während die anderen einfach durchlaufen.

## Weiterlesen

- [`docs/pi-custom-tools_de.md`](docs/pi-custom-tools_de.md) — wie die
  Werkzeuge gebaut sind und wie man eigene ergänzt
- [`docs/experiment_de.md`](docs/experiment_de.md) — warum die Architektur so
  aussieht, wie sie aussieht
