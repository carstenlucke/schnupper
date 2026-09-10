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
|     dashboard · Übersicht     |
+-------------------------------+
```

Die fünf oberen Panes sind die Agenten. Der Streifen unten startet das
Dashboard für den Beamer und gibt nur seine Adresse aus — siehe
[Das Dashboard](#das-dashboard).

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
- Ein Modell, das pi erreichen kann. Voreingestellt ist
  `openai-codex/gpt-5.6-luna` (ChatGPT-Abo, in pi einmalig per `/login`
  eingerichtet). Was sonst zur Verfügung steht, zeigt `pi --list-models`.

## Einrichten

```bash
cp .env.example .env
```

In der `.env` steht eine Zeile, auf die es ankommt:

```
COUNTING_AGENTS_MODEL=openai-codex/gpt-5.6-luna
```

Sie schlägt den `model:`-Eintrag in den Agentendateien und gilt für alle fünf
zugleich. Bremst ein Anbieter mitten in der Vorlesung oder schlägt ein
Rate-Limit zu, ändert man diese eine Zeile und startet die Demo neu.

Nicht jedes Modell aus `pi --list-models` ist auch freigegeben — `gpt-5.4-mini`
etwa weist Codex mit einem ChatGPT-Konto ab. Vor der Vorlesung also einmal
starten und zusehen, ob Zahlen erscheinen.

**Alternative TensorX:** Steht in `COUNTING_AGENTS_MODEL` ein
`tensorx-schnupper/...`-Modell, braucht es zusätzlich
`SCHNUPPER_TENSORX_API_KEY` in der `.env`. Dieser Schlüssel gilt nur für dieses
Projekt; ein global in pi hinterlegter TensorX-Zugang bleibt unberührt, denn
die Demo meldet denselben Endpunkt unter eigenem Namen an (siehe
[`.pi/extensions/tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts)).
So bleiben Vorlesungs- und Alltagskosten getrennt.

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

Das legt den Tab „Counting Agents (pi)" an, startet in den fünf oberen Panes je
einen Agenten und im Streifen darunter das Dashboard, das sich von selbst im
Browser öffnet. Der Fokus landet auf der Steuerung.

| Befehl | Wirkung |
|---|---|
| `./scripts/start.sh` | Tab anlegen, Agenten und Dashboard starten |
| `./scripts/start.sh --ohne-dashboard` | Nur die fünf Agenten-Panes |
| `./scripts/stop.sh` | Alle stoppen, Tab schließen |
| `./scripts/reset.sh` | Bus und Zustand leeren |
| `./scripts/reset.sh --restart` | Leeren und neu starten |

Im Steuerungs-Pane: Pfeiltasten zur Auswahl, Enter zum Ausführen, `q` beendet
die Demo.

## Das Dashboard

Die Agenten-Panes zeigen jeden Handgriff — das ist der Punkt, aber aus der
letzten Reihe ist es viel Text. Das Dashboard zeigt daneben den Überblick:

```bash
./scripts/dashboard.py            Port 8777, öffnet den Browser
./scripts/dashboard.py 9000       anderer Port
./scripts/dashboard.py --kein-browser
```

Es liest Bus und Zustandsdateien und schreibt nie — es kann die Demo also
nicht stören. Der Server schiebt Änderungen über Server-Sent Events nach, der
Browser fragt nichts von sich aus ab. Nur Standardbibliothek, kein Build.

**Das Zahlenband.** Jede Kachel ist eine Zahl aus dem Bus. Ihre Farbe sagt, wer
sie schon eingesammelt hat:

| Farbe | Bedeutung |
|---|---|
| grau | noch niemand |
| hellblau | `odd` hat sie |
| grün | `even` hat sie |
| goldener Ring | ist eine Primzahl |
| goldener Punkt, gefüllt | `prime` hat sie |
| rot | falsch einsortiert |

Rot ist der interessanteste Fall: Das Dashboard rechnet selbst nach, welche
Zahlen prim sind. Sammelt der Prim-Agent eine Zahl ein, die keine ist, wird das
sichtbar. Das passiert nicht bei jedem Durchlauf, aber wenn es passiert, ist es
der beste Moment der Vorlesung — das Modell hat sich vertan, und man sieht es.

**Agent anklicken.** Ein Klick auf eine Agentenzeile blendet alle fremden
Zahlen aus; nur die des Agenten bleiben stehen. Damit lässt sich einer nach dem
anderen erklären, ohne dass die anderen ablenken. Nochmal klicken hebt es auf.

**Rückstand.** Jede Agentenzeile zeigt, wie weit ihr Sammler dem Zähler
hinterherhinkt. In den Panes ist das nicht zu sehen, und es ist die eigentliche
Pointe: Die Agenten laufen nicht im Gleichschritt, sondern jeder in seinem
eigenen Takt — `prime` am langsamsten, weil er nachdenkt.

Die Farben folgen dem [Corporate Design der THM](https://go.thm.de/cd).

**Generalprobe ohne Modell.** Vor der Vorlesung lässt sich das Dashboard
prüfen, ohne dass Agenten laufen und Token kosten:

```bash
./scripts/dashboard-probelauf.py     in einem Pane
./scripts/dashboard.py               in einem zweiten
```

Der Simulator zählt hoch, lässt die Sammler unterschiedlich weit
hinterherhinken, pausiert `prime` zwischendurch und vergreift sich
gelegentlich an einer Zahl. Er schreibt in dieselben Dateien wie die echten
Agenten und darf deshalb nicht parallel zu `./scripts/start.sh` laufen.

## Anfragen zählen: warum Rate-Limits so schnell greifen

Ein Agentendurchlauf ist **nicht eine Anfrage an das Modell**, sondern eine pro
Werkzeugaufruf plus eine für die Abschlussantwort. Der Counter ruft
`control_read`, `state_read`, `bus_publish` und `state_write` auf — gemessen
sind das fünf Modellanfragen für die eine Zeile `→ 42`, die im Pane erscheint.

Hochgerechnet auf die laufende Demo: vier Agenten im Dauerlauf, ein Durchlauf
dauert rund zehn Sekunden, dazu drei Sekunden Takt — das sind etwa **90
Anfragen pro Minute**.

Bei [TensorX](https://docs.tensorx.ai/api-reference/rate-limits) erlaubt das
Standard-Kontingent 60 Anfragen pro Minute je Schlüssel. Die Demo läuft also
prompt in ein Limit, erkennbar an HTTP 429 mit `"reason": "rate_limit_requests"`.

Dazu kommt eine Falle, die man leicht übersieht: TensorX reserviert für jede
Anfrage so viele Token, wie in `max_tokens` angemeldet sind — unabhängig davon,
wie kurz die Antwort ausfällt. Mit dem Katalogwert 32768 wäre das Minutenbudget
von zwei Millionen Token nach 61 Anfragen erschöpft. Deshalb meldet
[`tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts) bewusst nur 4096
Token an; für eine Zeile Ausgabe ist das reichlich.

Was hilft, wenn ein Limit zuschlägt:

- **Anbieter wechseln** — eine Zeile `COUNTING_AGENTS_MODEL` in der `.env`. Die
  Voreinstellung läuft deshalb über ein Abo-Modell und nicht über TensorX.
- **Takt strecken** — `interval` im Frontmatter der Agenten hochsetzen. Bei 20
  Sekunden bleibt die Demo unter 60 Anfragen pro Minute, wirkt im Vortrag aber
  merklich zäher.
- **Weniger Agenten laufen lassen** — für manche Abschnitte reichen Counter und
  Prime.

Für die Vorlesung ist die Rechnerei selbst ein guter Moment: Fünf Agenten, die
jeweils nur eine Zeile ausgeben, erzeugen in einer Minute rund hundert
Anfragen. Man sieht im Pane eine Zahl — dahinter stecken fünf Gespräche mit
einem Modell.

## Was ein Agent ist

Eine Textdatei. Mehr nicht.

```markdown
---
description: Erzeugt fortlaufende Zahlen und stellt sie in den Event-Bus
model: openai-codex/gpt-5.6-luna
tools: bus_publish,control_read,state_read,state_write
thinking: off
interval: 3
---

# Counter-Agent

Du bist der **Counter**. Du erzeugst fortlaufende Zahlen — sonst nichts.
...
```

Der Kopf sagt, welches Modell rechnet, welche Werkzeuge erlaubt sind, wie oft
der Agent aufgerufen wird und ob er nachdenken darf. Darunter steht in normalem
Deutsch, was er tun soll. `scripts/run-agent.sh` liest die Datei und baut
daraus den pi-Aufruf.

Steht in der `.env` ein `COUNTING_AGENTS_MODEL`, gilt es für alle fünf Agenten
und schlägt ihren Frontmatter-Eintrag.

Der `prime`-Agent ist der einzige mit `thinking: low` — man soll sehen, wie er
bei der Primzahlprüfung überlegt, während die anderen einfach durchlaufen.

## Weiterlesen

- [`docs/Trajectory_de.md`](docs/Trajectory_de.md) — was bei einem Durchlauf
  wirklich passiert: Anfragen, Werkzeugaufrufe, wachsender Kontext
- [`docs/pi-custom-tools_de.md`](docs/pi-custom-tools_de.md) — wie die
  Werkzeuge gebaut sind und wie man eigene ergänzt
- [`docs/experiment_de.md`](docs/experiment_de.md) — warum die Architektur so
  aussieht, wie sie aussieht
