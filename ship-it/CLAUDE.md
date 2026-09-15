# CLAUDE.md

**Ship It!** – Live-Demo-App für eine Schnuppervorlesung bei StudiumPlus (90 Min, 12. Klasse FOS). Schüler wählen ein Produkt, 5 KI-Agenten erledigen den Produktlaunch über ein Web-Dashboard.

## Starten & Stoppen

```bash
./start.sh              # Server + Browser auf http://localhost:8000
./start.sh --force      # Port 8000 vorher freigeben, dann starten
```

## Architektur

```
Browser (Dashboard SPA)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess, JSON-Ereignisse auf stdout
pi CLI (pi --mode json --model … --tools … --system-prompt <agents/name.md>)
    ↕ Datei-I/O
projekte/<slug>/
```

**Null externe Python-Dependencies.** Frontend-Libraries (Tailwind, xterm.js, marked.js) via CDN.

## Backend: server.py

- `ThreadingHTTPServer` auf Port 8000
- Statische Dateien aus `dashboard/`
- Agent-Prozesse via `pi --mode json`; `PiAusgabe` übersetzt die Ereignisse
  (Denken, Werkzeugaufrufe, Text, Tokenverbrauch) in farbigen Terminal-Text.
  `pi -p` wäre einfacher, zeigt aber nur die Schlussantwort – das Terminal
  bliebe während des Laufs leer.
- **Status aus Dateisystem abgeleitet** (kein State-File): `done` = alle erwarteten Output-Dateien existieren, `running` = Prozess aktiv, `error` = Prozess beendet aber Outputs fehlen, `idle` = sonst

### API-Endpunkte

| Method | Pfad | Zweck |
|--------|------|-------|
| GET | `/api/projekte` | Projektliste mit Gesamtstatus |
| POST | `/api/projekte` | Neues Projekt (`{name, beschreibung}`) |
| GET | `/api/projekte/<slug>/agents` | Agenten + Status |
| POST | `/api/projekte/<slug>/agents/<name>/run` | Agent starten (opt. `{feedback}`) |
| GET | `/api/projekte/<slug>/agents/<name>/stream` | SSE-Stream |
| GET | `/api/projekte/<slug>/files/<agent>` | Dateiliste |
| GET | `/api/projekte/<slug>/files/<agent>/<datei>` | Dateiinhalt |
| DELETE | `/api/projekte/<slug>/files/<agent>` | Alle Agent-Outputs löschen |
| DELETE | `/api/projekte/<slug>/files/<agent>/<datei>` | Einzelne Datei löschen |

### Prompt-Generierung

`build_run_prompt(slug, agent, feedback)` erzeugt den Run-Prompt mit expliziten EINGABE/AUSGABE-Pfaden. Bei Feedback (Refinement) werden die bisherigen Outputs als zusätzliche Eingaben aufgelistet.

`AGENT_PATHS` definiert pro Agent die Input-/Output-Dateien. Das Backend verifiziert nach Abschluss ob die erwarteten Outputs existieren.

## Frontend: dashboard/

3-Spalten-Layout: Agent-Liste | Artefakt-Liste | Content-Area.

- **app.js**: State-Management, API-Calls, xterm.js-Terminals, SSE-Streaming, Polling (3s)
- **style.css**: THM-Corporate-Design, Markdown-Rendering, Animationen
- **Tabs**: Terminal (xterm.js), Ergebnis (marked.js Markdown), Vorschau (iframe für HTML)
- **Terminals**: Pro Agent ein persistentes xterm.js-Div (show/hide, nicht destroy/recreate – xterm.js unterstützt `open()` nur einmal)

### Agent-Abhängigkeiten (Frontend-enforced)

```
Zielgruppe (sofort) ──→ Marketing ──→ Social Media
Kalkulation (sofort) ─────┤
                          ↓
                       Website
```

## Agenten: agents/

pi hat **kein eingebautes Agenten-Konzept**. Ein Agent ist eine Markdown-Datei;
`build_pi_command()` in `server.py` liest das Frontmatter und baut daraus den
pi-Aufruf, der Text darunter wird zum Systemprompt.

```markdown
---
description: Zielgruppenanalyse – identifiziert Personas, Marktsegmente und Kaufkraft
model: openai-codex/gpt-5.6-luna
thinking: medium
tools: read,write,bash,webfetch
skills: popular-web-designs
---
```

Das Frontmatter ist bewusst flach: eine Zeile je Feld, Listen kommagetrennt,
keine Kommentare – der Parser in `read_agent()` liest `schlüssel: wert`.

| Feld | Wird zu |
|---|---|
| `model` | `--model` (außer `SHIP_IT_MODEL` in `.env` ist gesetzt) |
| `thinking` | `--thinking` (`off`, `minimal`, `low`, `medium`, `high`, `xhigh`) |
| `tools` | `--tools` – Allowlist, andere Werkzeuge gibt es für den Agenten nicht |
| `skills` | optional; je Name ein `--skill .pi/skills/<name>` |
| `description` | nur Anzeige im Dashboard |

Ein neuer Agent braucht außer der Datei einen Eintrag in `AGENT_PATHS`,
`AGENT_ORDER` und `AGENT_LABELS` in `server.py` sowie die
Abhängigkeitslogik im Frontend.

| Agent | Liest | Schreibt |
|-------|-------|----------|
| zielgruppe | produkt.md | zielgruppe/analyse.md |
| marketing | produkt.md, analyse.md | marketing/konzept.md |
| social-media | produkt.md, analyse.md, konzept.md | social-media/{instagram,linkedin,tiktok}.md |
| kalkulation | produkt.md | kalkulation/preiskalkulation.md |
| website | produkt.md, analyse.md, konzept.md, preiskalkulation.md | website/{website-prompt.md,index.html} |

Der Website-Agent erstellt zuerst `website-prompt.md` (alle Infos inline zusammengefasst), dann `index.html`.

Systemprompts definieren Rolle und Output-Format, aber **keine konkreten Dateipfade** – die kommen vom Backend im Run-Prompt.

## Konfiguration

- Modell je Agent im Frontmatter; `SHIP_IT_MODEL` in `.env` schlägt alle
  zugleich – der Weg, im Hörsaal den Anbieter zu wechseln. Die Anmeldung beim
  Anbieter erledigt pi selbst (`pi` → `/login`); in `.env` steht nur der
  `OPENAI_API_KEY` für die Bildgenerierung
- `.pi/extensions/webfetch.ts`: Werkzeug `webfetch` – pi bringt keins fürs
  Internet mit. Alle `.ts` dort bekommt jeder Agent per `-e`, freigeschaltet
  ist aber nur, was in seinem `tools:` steht
- `.pi/skills/popular-web-designs`: Design-Vorlagen, per `skills:` nur beim
  Website-Agenten
- Globale pi-Extensions, -Skills und CLAUDE.md erreichen die Agenten **nicht**
  (`-ne -ns -nc`) – die Demo läuft auf jedem Rechner gleich
- Projekte unter `projekte/<slug>/` (gitignored, runtime-only)

## Konventionen

- **Sprache**: Alle Agent-Outputs, UI-Texte, HTML-Kommentare und JS-Kommentare auf **Deutsch**. Keine englischen Kommentare im Code.
- **Kein Inline-CSS**: Styling ausschließlich über Tailwind-Klassen oder `style.css` – keine `style="..."`-Attribute im HTML, wenn es per Tailwind (z.B. `bg-[#181f23]`) oder CSS-Klasse lösbar ist.
- **Accessibility**: Icon-Only-Buttons brauchen immer ein `aria-label` (und/oder `title`).
- **Slugs**: lowercase + Bindestriche, Umlaute werden ersetzt (ä→ae etc.)
- **Keine Build-Pipeline**: Kein npm, kein Bundler – CDN + Python stdlib
- **THM-Farben**: `thm-green: #80ba24`, `thm-gray: #4a5c66`, `thm-red: #9c132e`, `thm-yellow: #f4aa00`, `thm-light-blue: #00b8e4`, `thm-blue: #002878` (CD-Manual, `go.thm.de/cd`)
- **Farbthema**: Hell = CD-Standard (Weiß/Hellgrau, Text THM Grau), Dunkel = aus den Negativ-Regeln abgeleitet (`#2A3840`, `#344750`, `#1A252B`). Beide Paletten stehen als CSS-Variablen in `style.css`; Tailwind greift per `rgb(var(--…) / <alpha-value>)` darauf zu. Neue Farben dort ergänzen, keine Tailwind-Standardfarben wie `text-red-400`. **Fläche und Schrift sind getrennt**: `accent`, `warning` und `error` füllen Flächen, Icons, Ränder und Statuspunkte; für Text gelten `accent-text` und `warning-text`, für weiße Schrift auf Rot `error-strong`. Reines THM Grün oder Gelb als Textfarbe auf hellem Grund verfehlt WCAG AA (2,3:1 bzw. 2,0:1) — neue Textfarben vor dem Einbau gegen die hellste bzw. dunkelste Fläche durchrechnen, auf der sie landen können. Der Umschalter im Header speichert die Wahl in `localStorage` (`ship-it-theme`), ohne Wahl gilt die Systemeinstellung. Terminal und Kopfleiste sind in beiden Themen gleich.

## Nicht anfassen

`.github/workflows/release.yml` ist **bewusst inaktiv**. GitHub Actions liest
nur `.github/workflows/` im Repo-Root, und der Tag-Trigger passt nicht mehr zum
Namespace-Schema (`ship-it/vX.Y.Z`). Der Workflow bleibt als Referenz liegen —
nicht verschieben, nicht „reparieren", nur auf ausdrückliche Anweisung
reaktivieren.
