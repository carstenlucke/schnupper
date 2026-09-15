# CLAUDE.md

**Agent Party** — Live-Demo für eine Schnuppervorlesung bei StudiumPlus (90 Min,
Oberstufe). Die Teilnehmenden schreiben die Agenten **selbst**: Sie legen
Rollenprofile an, wählen daraus eine Besetzung und geben ihr ein Thema. Danach
diskutieren die gewählten Profile reihum in einem Web-Dashboard.

## Worum es geht: der Agent ist eine Textdatei

Das ist kein Implementierungsdetail, sondern der Zweck des Projekts — beim
Ändern nicht wegoptimieren:

- **Die Rollenbeschreibung ist der Systemprompt.** Was in `profile/<slug>.md`
  unter dem Frontmatter steht, geht wörtlich als `--system-prompt` an pi. Kein
  Zusammenbau, keine Vorlage drumherum, keine versteckte Zusatzanweisung. Wer
  im Vortrag den Text ändert und die Party neu startet, sieht das Verhalten
  sofort kippen — das ist die ganze Pointe.
- **Keine Werkzeuge.** Flag `-nt`. Ein Party-Agent kann antworten, sonst nichts:
  nicht lesen, nicht schreiben, nicht ins Netz. Der Unterschied zu `ship-it/`
  und `the-counting-agents/` ist beabsichtigt und gehört zur Erzählung.
- **Kein Gedächtnis.** Flag `--no-session`. Jeder Beitrag ist ein eigener
  Prozess; den Gesprächsverlauf geben wir jedes Mal neu als Text im Prompt mit.
  „Das Modell erinnert sich nicht" lässt sich so zeigen statt behaupten.

## Starten & Stoppen

```bash
./start.sh              # Server + Browser auf http://localhost:8100
./start.sh --force      # Port 8100 vorher freigeben, dann starten
```

Ctrl+C beendet den Server und räumt alle laufenden pi-Prozesse ab.

Voraussetzung ist die [pi CLI](https://pi.dev), einmal per `/login` angemeldet.
Ohne sie startet das Dashboard zwar, aber keine Party.

## Architektur

```
Browser (Dashboard SPA)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess, JSON-Ereignisse auf stdout
pi CLI (pi --mode json -nt --no-session --system-prompt <Rollentext> -- <Prompt>)
    ↕ Datei-I/O
profile/<slug>.md   (versioniert)
partys/<slug>/      (runtime, gitignored)
```

**Null externe Python-Dependencies.** Frontend-Libraries (Tailwind, marked.js,
Material Symbols, Barlow) via CDN. Kein npm, kein Bundler.

Port **8100** — 8000 gehört `ship-it/`, 8777 dem Dashboard von
`the-counting-agents/`. Alle drei laufen parallel.

## Backend: server.py

- `ThreadingHTTPServer` auf Port 8100, statische Dateien aus `dashboard/`
- **Status aus dem Dateisystem abgeleitet** (kein State-File): die *Beiträge*
  in `verlauf.jsonl` gegen `runden × len(teilnehmer)` ergeben
  `neu` / `laeuft` / `pausiert` / `fertig` / `fehler`. Ein Serverneustart
  mitten in der Party führt auf `pausiert`; „Fortsetzen" macht dort weiter, wo
  die Datei aufhört.
- **Die jsonl enthält dreierlei**: Beiträge (`art: beitrag`), Zwischenrufe der
  Gesprächsleitung (`art: zwischenruf`) und das Fazit (`art: fazit`). Gezählt
  wird nur das erste — `ist_beitrag()` und `nur_beitraege()` sind die einzige
  Stelle dafür, ein Zwischenruf darf keine Runde verschlucken. Einträge ohne
  `art` sind Beiträge aus einer älteren Sitzung.
- `PiStrom` übersetzt die JSON-Ereignisse von pi in Ereignisse fürs Dashboard.
  `pi -p` wäre einfacher, zeigt aber nur die Schlussantwort — die Denkschritte
  blieben unsichtbar.

### API-Endpunkte

| Method | Pfad | Zweck |
|--------|------|-------|
| GET | `/api/profile` | Alle Profile (Frontmatter + Rollentext) |
| POST | `/api/profile` | Profil anlegen |
| PUT | `/api/profile/<slug>` | Profil ändern |
| DELETE | `/api/profile/<slug>` | Profil löschen (`?force=1` trotz offener Party) |
| POST | `/api/profile/entwurf` | Profil ausarbeiten lassen, SSE |
| GET | `/api/modelle` | Modelle je Anbieter, einmal pro Serverlauf gecacht |
| GET | `/api/partys` | Sitzungsliste mit Status |
| POST | `/api/partys` | Sitzung anlegen |
| GET | `/api/partys/<slug>` | Sitzung + Status, **ohne** Verlauf |
| POST | `/api/partys/<slug>/start` | Durchlauf starten oder fortsetzen |
| POST | `/api/partys/<slug>/stop` | Durchlauf abbrechen |
| POST | `/api/partys/<slug>/zwischenruf` | Impuls der Gesprächsleitung (`{text}`) |
| POST | `/api/partys/<slug>/runde` | Eine Runde anhängen und starten |
| POST | `/api/partys/<slug>/fazit` | Die Gesprächsleitung zieht Bilanz |
| GET | `/api/partys/<slug>/stream` | SSE: Verlauf + Beiträge live |
| DELETE | `/api/partys/<slug>` | Sitzung löschen |

`GET /api/partys/<slug>` liefert bewusst **keinen** Verlauf. Die Sprechblasen
entstehen ausschließlich aus dem Stream, damit es dafür genau eine Stelle im
Frontend gibt.

### Die Party-Schleife

Ein Daemon-Thread je Sitzung, **sequenziell**: für jede Runde, für jeden
Teilnehmer in der gewählten Reihenfolge ein pi-Prozess. Nicht parallelisieren —
die Profile sollen aufeinander antworten können, und im Hörsaal ist das
Nacheinander der Punkt.

Drei Stellen, die genau so sein müssen:

1. **Prüfen und Eintragen unter einem Lock.** Ein Doppelklick auf „Start" darf
   nicht zwei Threads erzeugen, die abwechselnd in dieselbe `verlauf.jsonl`
   schreiben.
2. **`abbruch` und `prozess` unter demselben `prozess_lock`.** Sonst entsteht
   bei einem Stop während des Prozessstarts ein Waisen-pi, der im Hintergrund
   weiterredet und Geld kostet.
3. **Erst `verlauf.jsonl` schreiben, dann `beitrag_ende` senden.** Ein Browser,
   der genau dazwischen neu verbindet, bekommt den Beitrag aus der Datei statt
   gar nicht. Ein abgebrochener Teilbeitrag wird **nicht** geschrieben — ein
   halber Satz im Verlauf vergiftet alle Folgeprompts.
4. **Zwischenrufe hängt nur der Schleifen-Thread an** (`schreibe_einwuerfe()`),
   und nur zwischen zwei Beiträgen. Schriebe der Request-Thread sie sofort,
   stünde ein Zwischenruf in der Datei vor einer Blase, deren Ereignisse schon
   die Marke davor tragen — eine Verbindung, die genau dann neu aufmacht,
   bekäme den laufenden Beitrag weggefiltert.

### Eingreifen in die laufende Sitzung

Der Mensch am Rechner heißt im Prompt **Gesprächsleitung** (`LEITUNG`). Er hat
drei Griffe, alle in der Steuerleiste unter dem Verlauf:

- **Zwischenruf** (`wirf_ein`) — der Text landet als eigener Eintrag im
  Verlauf und damit im Prompt jedes folgenden Beitrags. Was seit dem letzten
  Beitrag dazukam, hebt `baue_beitrag_prompt()` zusätzlich als eigenen Block
  hervor (`offene_zwischenrufe`, `ZWISCHENRUF_VORLAGE`) — mit der Ansage, dass
  das keine Wortmeldung ist, auf die man antwortet, sondern eine Vorgabe.
  Sichtbar ist der Einwurf sofort (Ereignispuffer), geschrieben wird er, sobald
  der laufende Beitrag steht. Läuft gerade nichts, schreibt der Request-Thread
  selbst — dann gibt es keine Marke, die kaputtgehen könnte.
- **Weitere Runde** (`naechste_runde`) — erhöht `runden` in `sitzung.json` um
  eins und startet sofort. `MAX_RUNDEN` deckelt nur das Einrichten: wie oft im
  Hörsaal verlängert wird, entscheidet das Gespräch. Scheitert der Start, geht
  die Rundenzahl zurück, sonst gälte die Sitzung als unfertig.
- **Fazit** (`starte_fazit`) — ein einzelner Durchlauf über dieselbe Registry
  wie eine Party, damit währenddessen niemand eine Runde dazwischenstartet.
  Ergebnis ist ein Eintrag `art: fazit`; er zählt nicht gegen die Rundenzahl,
  und eine weitere Runde danach ist ausdrücklich möglich.

Beitrag und Fazit teilen sich `_pi_durchlauf()` — Prozessstart, Ereignisse,
Abbruch und Fehlerfall gibt es nur einmal.

### SSE

Der Stream liefert zuerst den gespeicherten Verlauf nach (je Beitrag ein
`beitrag_start` / `text` / `beitrag_ende` mit `nachgeliefert: true`, je
Zwischenruf ein `zwischenruf`) und hängt sich danach an den Ereignispuffer des
laufenden Threads. Die Reihenfolge ist Teil des Vertrags: erst die Datei lesen
(ergibt `n`), dann nachliefern, dann die Registry — und aus dem Puffer nur, was
`eintrag_nr >= n` hat. So gibt es weder Lücke noch Dopplung, ganz ohne Lock,
weil die Ereignisliste nur wächst.

`eintrag_nr` ist die **Zeilenzahl der Datei** zum Zeitpunkt des Ereignisses,
nicht die Beitragsnummer: Zwischenrufe und Fazit stehen in derselben Datei und
verschieben die Marke mit. `beitrag_start` und `beitrag_ende` tragen zusätzlich
ein `sorte`-Feld (`beitrag` oder `fazit`), damit das Frontend die Fazitkarte
anders zeichnet und nicht mitzählt.

Alle 15 s geht ein `: ping` raus. Zwischen zwei Beiträgen kann es lange still
sein.

### Pfadsicherheit

`SAFE_SEGMENT_RE` (`^[a-z0-9][a-z0-9-]*$`) plus `realpath`-Präfixprüfung vor
jedem Dateizugriff — für Profil- **und** Party-Slugs, weil hier im Gegensatz zu
den Schwesterprojekten beide aus Nutzereingaben stammen. Dieselbe Prüfung
bekommt `_serve_static()`, sonst holt `/../server.py` den Quelltext.

Die Dateiendung wird **nach** der Slug-Prüfung angehängt (`profil_pfad()`) —
ein Punkt ist im Slug nicht erlaubt, `<slug>.md` würde die Prüfung sonst nie
bestehen.

## Profile: profile/

pi hat **kein eingebautes Agenten-Konzept**. Ein Profil ist eine
Markdown-Datei; `profil_lesen()` in `server.py` liest das Frontmatter, der Text
darunter wird zum Systemprompt.

```markdown
---
name: Skeptische Ökonomin
beschreibung: Rechnet jede Idee auf Kosten und Nutzen herunter
model: openai-codex/gpt-5.6-luna
thinking: low
farbe: hellblau
---

Du bist Wirtschaftswissenschaftlerin und sitzt in dieser Runde als die
Stimme, die nach Zahlen fragt. …
```

Das Frontmatter ist bewusst flach: eine Zeile je Feld, kein YAML-Parser. Beim
Wert gewinnt der erste Doppelpunkt — eine Beschreibung darf also selbst einen
enthalten.

| Feld | Wird zu |
|---|---|
| `name` | Anzeigename, Grundlage des Slugs |
| `beschreibung` | Kachel und Teilnehmerliste im Prompt |
| `model` | `--model` (außer `AGENT_PARTY_MODEL` in `.env` ist gesetzt) |
| `thinking` | `--thinking`; bei `off` oder leer bleibt das Flag weg |
| `farbe` | Anzeigefarbe: `gruen`, `grau`, `rot`, `gelb`, `hellblau`, `blau` |

**Ungültige Werte werden repariert, nicht abgelehnt**: unbekannte Farbe →
`grau`, unbekannte Denkstufe → `medium`. Pflicht sind nur Name und Rollentext.
Im Hörsaal soll nichts an einer Kleinigkeit scheitern.

Die fünf mitgelieferten Profile sind versioniert, damit die Demo ohne Vorarbeit
startet. In der Vorlesung neu angelegte Profile landen daneben und bleiben
untracked.

## Der pi-Aufruf

```python
pi --mode json --no-session -nt -nc -ns -np -ne \
   --model <M> [--thinking <T>] --system-prompt <Rollentext> -- <Prompt>
```

| Flag | Wirkung |
|---|---|
| `--mode json` | Ereignisstrom statt Schlussantwort — Denkschritte werden sichtbar |
| `--no-session` | Kein Gesprächsverlauf; jeder Beitrag beginnt bei null |
| `-nt` | Keine Werkzeuge, weder eingebaute noch aus Extensions |
| `-nc` | CLAUDE.md/AGENTS.md ignorieren |
| `-ns` `-np` `-ne` | Keine Skills, Prompt-Vorlagen, Extensions |
| `--model` | Immer gesetzt — pi fällt sonst auf `google` als Anbieter zurück |
| `--thinking` | Nur bei einem Wert ≠ `off`; nicht jedes Modell kann denken |

`stdin=subprocess.DEVNULL` ist **Pflicht**: pi liest die Standardeingabe sonst
mit in den Auftrag ein und wartet für immer auf ihr Ende.

Drei Aufrufarten, derselbe Code:

1. **Party-Beitrag** — Systemprompt ist der Rollentext, der Prompt enthält
   Thema, Teilnehmerliste, bisherigen Verlauf und die Aufforderung zu antworten.
2. **Profil ausarbeiten** — Systemprompt ist `SYSTEMPROMPT_ENTWURF` mit dem
   gewünschten Ausgabeformat, der Prompt ist die Stichwortidee. Die Lebensdauer
   des Prozesses ist exakt die des Requests: bricht der Browser ab, räumt der
   `finally`-Block pi weg. Deshalb braucht dieser Weg keinen Stop-Endpunkt.
3. **Fazit** — Systemprompt ist `SYSTEMPROMPT_FAZIT`, der Prompt enthält Thema,
   Besetzung und den ganzen Verlauf. Das ist die einzige Rolle, die **nicht**
   aus `profile/` kommt: Die Gesprächsleitung ist keine Stimme am Tisch,
   sondern der Blick von außen, und niemand soll sie versehentlich löschen.

## Frontend: dashboard/

SPA ohne Build, ein klassisches Skript im globalen Scope. Drei Ansichten,
erreichbar über die Navigation **in der Kopfleiste** (die Ids heißen weiterhin
`tab-*`), verlinkbar über `#profile`, `#einrichten`, `#party/<slug>`.

- **Agentenprofile** — Kachelraster links, Editor rechts. Zweiter Weg zum Profil:
  „Rolle in einem Satz beschreiben" → „Ausarbeiten lassen" → der Entwurf läuft
  live in die Textarea und ist vor dem Speichern änderbar. „Duplizieren" legt eine
  Kopie mit freiem Namen in den Editor; gespeichert wird erst auf Knopfdruck.
- **Party vorbereiten** — Profile anklicken (der Klick schaltet um, jedes Profil
  sitzt höchstens einmal am Tisch), Reihenfolge per Hoch/Runter, Thema,
  Einstiegsfrage, Runden 1–5, Modell.
- **Sitzung** — oben ein dunkler Themenblock (Status, Fortschritt, Besetzung in
  Zahlen, Thema, Einstiegsfrage), darunter links der Verlauf, rechts die Karten
  „Teilnehmer" (mit Beitragszähler und „formuliert …" beim aktiven Sprecher) und
  „Sitzung" (Runde, Beiträge, Zwischenrufe). Je Beitrag ein Zeichen mit
  Initialen neben einer Karte mit Farbbalken; vor dem ersten Beitrag einer Runde
  ein Trenner.

Die **Steuerleiste** klebt unter dem Inhalt und ist nur in der Sitzungsansicht
sichtbar: Zwischenruf einwerfen, weitere Runde, Fazit erstellen, anhalten oder
fortsetzen. Steht beim Klick auf „Weitere Runde" noch Text im Zwischenruffeld,
geht der Einwurf der Runde voraus — ein Griff für „so, und jetzt redet bitte
darüber". Nach „Weitere Runde" und „Fazit erstellen" baut `oeffneParty()` die
Ansicht neu auf, damit der Strom das Neue live zeigt.

**Die Sprechblase wächst inkrementell.** `beitrag_start` legt einen DOM-Knoten
an, jedes Delta hängt per `append()` einen Textknoten an, und erst bei
`beitrag_ende` geht der fertige Text einmal durch `marked`. Wer das durch
`innerHTML` pro Delta ersetzt, lässt die Ansicht bei jedem Zeichen flackern und
zerstört die Textauswahl — nicht „vereinfachen".

**Jedes Profil sitzt höchstens einmal am Tisch.** Der Name ist die Identität
des Agenten: er steht im Teilnehmerblock, im Verlauf und in der Anweisung,
die Person beim Namen zu nennen. Profilnamen sind schon beim Anlegen eindeutig
(`_profil_anlegen` weist einen zweiten gleichen ab), und die Besetzung hält das
durch — `_party_anlegen` lehnt eine doppelte Nennung mit 400 ab, die Kachel
schaltet um statt anzuhängen. Wer zwei ähnliche Stimmen will, dupliziert das
Profil und gibt ihm einen eigenen Namen.

Angesprochen wird die Besetzung trotzdem über den **Index**: sie ist eine
Reihenfolge, keine Menge. Hoch, Runter und Wegnehmen arbeiten am Platz, und
`teilnehmer_block` markiert „(das bist du)" ebenfalls über den Platz — falls
doch einmal eine von Hand bearbeitete `sitzung.json` in die Schleife läuft.

`EventSource` kann kein POST. Der Entwurfsstrom läuft deshalb über `fetch` plus
`ReadableStream` (`sseLesen()`), der Party-Stream über `EventSource`.

### Farbthema

Vier Teile, wie in `ship-it/`:

1. Anti-Flash-Skript inline als erstes im `<head>`, Key `agent-party-theme`
2. Tailwind-Config inline, `darkMode: "class"`, Farben als
   `rgb(var(--x) / <alpha-value>)`
3. CSS-Variablen in `style.css`, je ein Block `:root` und `.dark`
4. Umschalter im Header; ohne gespeicherte Wahl folgt die App
   `prefers-color-scheme` und reagiert auf dessen Änderung

**Kopfleiste und Themenblock sind in beiden Themen dunkel** (`--header`, hell
`#1A252B`, dunkel `#10181D`) — anders als in `ship-it/`, wo die Kopfleiste THM
Grau bleibt. Die Wortmarke soll auf dem Beamer wie ein Titelbalken stehen, und
der Themenblock der Sitzung führt sie nach unten fort. Schrift darauf:
`--on-header`, gedämpft `--on-header-variant` (`#A8B4BC`).

**Fläche und Schrift sind getrennt.** THM Grün und Gelb verfehlen in Reinform
als Textfarbe auf hellem Grund WCAG AA (2,3:1 bzw. 2,0:1). Sie füllen darum
Flächen (`--accent`, `--warning`), für Text gelten `--accent-text` und
`--warning-text`.

Dasselbe gilt für die sechs Profilfarben: `--profil` füllt den 4px-Balken, den
Punkt und das Zeichen mit den Initialen, `--profil-text` beschriftet den Namen
daneben. Die Schrift **auf** der Farbfläche ist `--profil-auf` — Weiß auf Grau,
Rot und Blau, dunkles `#1A252B` auf Grün, Gelb und Hellblau, wo Weiß unter
3:1 bliebe. Alle Textwerte sind gegen die
ungünstigste Fläche des jeweiligen Themas nachgerechnet (hell `#EBEBEB`, dunkel
`#344750`) und erreichen dort mindestens 4,8:1:

| Farbe | Fläche | Text hell | Text dunkel |
|---|---|---|---|
| gruen | `#80BA24` | `#456B0D` | `#A8D86E` |
| grau | `#4A5C66` | `#4A5C66` | `#B2BEC6` |
| rot | `#9C132E` | `#9C132E` | `#F4A8B3` |
| gelb | `#F4AA00` | `#845A00` | `#FFC03D` |
| hellblau | `#00B8E4` | `#00708C` | `#5FD4F2` |
| blau | `#002878` | `#002878` | `#9DBEFF` |

Wer eine Farbe ändert, rechnet vorher nach — gegen die hellste bzw. dunkelste
Fläche, auf der sie landen kann. Das reine Hellblau etwa kommt auf `#344750`
nur auf 4,1:1 und ist deshalb im Dunkelmodus aufgehellt.

## Konfiguration

- `AGENT_PARTY_MODEL` in `.env` schlägt alle Profile und die Wahl im Dashboard
  zugleich — der Weg, im Hörsaal den Anbieter zu wechseln
- `AGENT_PARTY_STANDARD_MODELL` ist die Voreinstellung für neue Profile und für
  „Profil ausarbeiten"
- **Kein API-Schlüssel nötig.** Die Anmeldung erledigt pi selbst (`pi` →
  `/login`); `tensorx` und `lmstudio` sind global eingerichtet
- `/api/modelle` filtert `pi --list-models` auf `openai-codex`, `tensorx` und
  `lmstudio` — die drei Wege der Vorlesung (Abo, Cloud, lokal). Was pi sonst
  noch kennt, bleibt bewusst aus der Auswahl
- Partys unter `partys/<slug>/` (gitignored, runtime-only)

Eine projektlokale TensorX-Extension, wie `the-counting-agents/` sie hat, gibt
es hier **absichtlich nicht**: so einfach wie möglich lokal lauffähig.

## Konventionen

- **Sprache: Deutsch.** UI-Texte, Kommentare, Modellausgaben, Doku. Keine
  englische Doppelfassung — die führt nur `the-counting-agents/`.
- **Kein Inline-CSS**: Styling über Tailwind-Klassen oder `style.css`, keine
  `style="..."`-Attribute.
- **Accessibility**: Icon-Only-Buttons brauchen immer ein `aria-label` (und
  `title`).
- **Slugs**: Kleinbuchstaben und Bindestriche, Umlaute ersetzt (ä→ae etc.),
  serverseitig erzeugt.
- **Keine Emoji** — das Corporate Design schließt sie aus.
- **Formensprache**: 8px-Raster, Radius 2–8px (`rounded`, `rounded-md`,
  `rounded-lg`), `rounded-full` nur für Statuspunkte und den Themen-Umschalter,
  1px-Ränder, 4px-Balken als Akzentkante, keine Verläufe, Übergänge 120–180ms.
  Bewusst schärfer als `ship-it/`, das `rounded-xl` verwendet.
- **Überschriften in Versalien**, Barlow Condensed, mit grüner Unterkante
  (`.karten-titel`, `.abschnitt-titel`); dieselbe Marke wie unter dem aktiven
  Navigationspunkt. Namen von Profilen in Karten und Listen ebenso.
- **Keine Build-Pipeline**: kein npm, kein Bundler — CDN + Python stdlib.

## Nicht wegoptimieren

- Die **sequenzielle Runde**. Parallele Beiträge wären schneller und würden die
  Demo zerstören: die Profile könnten nicht mehr aufeinander antworten.
- Der **sichtbare Denkbereich**. Er ist der Grund für `--mode json` statt `-p`.
- Das **Fehlen von Werkzeugen** (`-nt`). Ein Profil, das lesen oder schreiben
  darf, ist eine andere Demo.
- Der **Verlauf im Prompt** statt einer pi-Session. Dass das Modell kein
  Gedächtnis hat und wir es ihm jedes Mal neu mitgeben, wird im Vortrag erzählt.
