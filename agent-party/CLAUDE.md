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
- **Status aus dem Dateisystem abgeleitet** (kein State-File): Zeilen in
  `verlauf.jsonl` gegen `runden × len(teilnehmer)` ergeben
  `neu` / `laeuft` / `pausiert` / `fertig` / `fehler`. Ein Serverneustart
  mitten in der Party führt auf `pausiert`; „Fortsetzen" macht dort weiter, wo
  die Datei aufhört.
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

### SSE

Der Stream liefert zuerst den gespeicherten Verlauf nach (je Beitrag ein
`beitrag_start` / `text` / `beitrag_ende` mit `nachgeliefert: true`) und hängt
sich danach an den Ereignispuffer des laufenden Threads. Die Reihenfolge ist
Teil des Vertrags: erst die Datei lesen (ergibt `n`), dann nachliefern, dann die
Registry — und aus dem Puffer nur, was `beitrag_nr >= n` hat. So gibt es weder
Lücke noch Dopplung, ganz ohne Lock, weil die Ereignisliste nur wächst.

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

Zwei Aufrufarten, derselbe Code:

1. **Party-Beitrag** — Systemprompt ist der Rollentext, der Prompt enthält
   Thema, Teilnehmerliste, bisherigen Verlauf und die Aufforderung zu antworten.
2. **Profil ausarbeiten** — Systemprompt ist `SYSTEMPROMPT_ENTWURF` mit dem
   gewünschten Ausgabeformat, der Prompt ist die Stichwortidee. Die Lebensdauer
   des Prozesses ist exakt die des Requests: bricht der Browser ab, räumt der
   `finally`-Block pi weg. Deshalb braucht dieser Weg keinen Stop-Endpunkt.

## Frontend: dashboard/

SPA ohne Build, ein klassisches Skript im globalen Scope. Drei Ansichten über
eine Tab-Leiste, verlinkbar über `#profile`, `#einrichten`, `#party/<slug>`.

- **Profile** — Kachelraster links, Editor rechts. Zweiter Weg zum Profil: „Rolle
  in einem Satz beschreiben" → „Ausarbeiten lassen" → der Entwurf läuft live in
  die Textarea und ist vor dem Speichern änderbar.
- **Party einrichten** — Profile anklicken (Mehrfachnennung erlaubt, dasselbe
  Profil darf zweimal am Tisch sitzen), Reihenfolge per Hoch/Runter, Thema,
  Einstiegsfrage, Runden 1–5, Modell.
- **Party läuft** — je Beitrag eine Sprechblase mit Farbbalken, darunter ein
  aufklappbarer Bereich „Was das Modell gedacht hat".

**Die Sprechblase wächst inkrementell.** `beitrag_start` legt einen DOM-Knoten
an, jedes Delta hängt per `append()` einen Textknoten an, und erst bei
`beitrag_ende` geht der fertige Text einmal durch `marked`. Wer das durch
`innerHTML` pro Delta ersetzt, lässt die Ansicht bei jedem Zeichen flackern und
zerstört die Textauswahl — nicht „vereinfachen".

Die Besetzung wird durchgehend über den **Index** angesprochen, nie über den
Slug: dasselbe Profil darf mehrfach in der Runde sitzen, ein Zugriff über den
Slug träfe dann den falschen Platz.

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

**Fläche und Schrift sind getrennt.** THM Grün und Gelb verfehlen in Reinform
als Textfarbe auf hellem Grund WCAG AA (2,3:1 bzw. 2,0:1). Sie füllen darum
Flächen (`--accent`, `--warning`), für Text gelten `--accent-text` und
`--warning-text`.

Dasselbe gilt für die sechs Profilfarben: `--profil` füllt den 4px-Balken und
den Punkt, `--profil-text` beschriftet den Namen. Alle Textwerte sind gegen die
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
- **Keine Build-Pipeline**: kein npm, kein Bundler — CDN + Python stdlib.

## Nicht wegoptimieren

- Die **sequenzielle Runde**. Parallele Beiträge wären schneller und würden die
  Demo zerstören: die Profile könnten nicht mehr aufeinander antworten.
- Der **sichtbare Denkbereich**. Er ist der Grund für `--mode json` statt `-p`.
- Das **Fehlen von Werkzeugen** (`-nt`). Ein Profil, das lesen oder schreiben
  darf, ist eine andere Demo.
- Der **Verlauf im Prompt** statt einer pi-Session. Dass das Modell kein
  Gedächtnis hat und wir es ihm jedes Mal neu mitgeben, wird im Vortrag erzählt.
