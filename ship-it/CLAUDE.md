# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt

**Ship It!** – Live-Demo-App für eine Schnuppervorlesung (90 Min, 12. Klasse FOS/THM). Schüler wählen ein Produkt, 5 KI-Agenten erledigen den Produktlaunch über ein Web-Dashboard.

## Starten & Stoppen

```bash
./start.sh              # Server + Browser auf http://localhost:8000
# Ctrl+C zum Stoppen, bei Port-Konflikt:
lsof -ti :8000 | xargs kill -9
```

## Architektur

```
Browser (Dashboard SPA)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess + PTY
OpenCode CLI (opencode run --agent <name> <prompt>)
    ↕ Datei-I/O
projekte/<slug>/
```

**Null externe Python-Dependencies.** Frontend-Libraries (Tailwind, xterm.js, marked.js) via CDN.

## Backend: server.py

- `ThreadingHTTPServer` auf Port 8000
- Statische Dateien aus `dashboard/`
- Agent-Prozesse via PTY-Subprocess (ANSI-Farben erhalten)
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

3-Spalten-Layout: Agent-Liste (220px) | Artefakt-Liste (250px) | Content-Area (flex).

- **app.js**: State-Management, API-Calls, xterm.js-Terminals, SSE-Streaming, Polling (3s)
- **style.css**: THM-Corporate-Design (grün #80ba24, blau #002878), Markdown-Rendering, Animationen
- **Tabs**: Terminal (xterm.js), Ergebnis (marked.js Markdown), Vorschau (iframe für HTML)
- **Terminals**: Pro Agent ein persistentes xterm.js-Div (show/hide, nicht destroy/recreate – xterm.js unterstützt `open()` nur einmal)

### Abhängigkeiten (Frontend-enforced)

```
Zielgruppe (sofort) ──→ Marketing ──→ Social Media
Kalkulation (sofort) ─────┤
                          ↓
                       Website
```

## Agenten: .opencode/agents/

5 Agent-Definitionen mit YAML-Frontmatter (`description`, `model`, `thinking`, `tools`).

| Agent | Liest | Schreibt | Model |
|-------|-------|----------|-------|
| zielgruppe | produkt.md | zielgruppe/analyse.md | github-copilot/gpt-4o |
| marketing | produkt.md, analyse.md | marketing/konzept.md | github-copilot/gpt-4o |
| social-media | produkt.md, analyse.md, konzept.md | social-media/{instagram,linkedin,tiktok}.md | github-copilot/gpt-4o |
| kalkulation | produkt.md | kalkulation/preiskalkulation.md | github-copilot/gpt-4o |
| website | produkt.md, analyse.md, konzept.md, preiskalkulation.md | website/{website-prompt.md,index.html} | github-copilot/claude-sonnet-4.6 |

Der Website-Agent erstellt zuerst `website-prompt.md` (alle Infos inline zusammengefasst), dann `index.html`.

Systemprompts definieren Rolle und Output-Format, aber **keine konkreten Dateipfade** – die kommen vom Backend im Run-Prompt.

## Konfiguration

- `opencode.json`: Provider (`github-copilot`, `openai`) + Default-Model
- Agenten können das Model per Frontmatter überschreiben
- Projekte unter `projekte/<slug>/` (gitignored, runtime-only)

## Veraltete Dateien

- `spec/intent-and-1stidea.md` – Frühes Konzeptdokument, veraltet.
- `spec/implementation-plan.md` – Ursprünglicher Implementierungsplan, veraltet (beschreibt z.B. noch 6 Agenten).

**Beide nicht als Kontext verwenden.** Die aktuelle Architektur ist in dieser CLAUDE.md beschrieben.

## Konventionen

- **Sprache**: Alle Agent-Outputs, UI-Texte und Kommentare auf Deutsch
- **Slugs**: lowercase + Bindestriche, Umlaute werden ersetzt (ä→ae etc.)
- **Keine Build-Pipeline**: Kein npm, kein Bundler – CDN + Python stdlib
- **THM-Farben**: `thm-green: #80ba24`, `thm-blue: #002878`, `thm-gray: #4a5c66`, `thm-yellow: #f4aa00`, `thm-light-blue: #00b8e4`
