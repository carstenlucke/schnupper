# Ship It! – Implementierungsplan

## Context

Live-Demo für eine Schnuppervorlesung (90 Min, 12. Klasse FOS). Schüler wählen ein Produkt, 6 KI-Agenten erledigen den Produktlaunch. Das Dashboard ist die zentrale Steuer- und Beobachtungsoberfläche – kein tmux nötig. Agenten werden on-demand gestartet (nicht als Dauer-Loop), mit manuellem Review zwischen den Stufen.

Referenzprojekt: `the-counting-agents` liefert das OpenCode-Agent-Pattern (`.opencode/agents/*.md`, `opencode run --agent`).

---

## Architektur

```
Browser (Dashboard)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess + pty
OpenCode CLI (opencode run --agent <name> <prompt>)
    ↕ Datei-I/O
produktlaunch/ (gemeinsames Output-Verzeichnis)
```

**Null externe Python-Dependencies.** Server nutzt `http.server.ThreadingHTTPServer` + `subprocess` + `pty` (alles stdlib). Frontend-Libraries (xterm.js, marked.js) via CDN.

---

## Projektstruktur (Ziel)

```
ship-it/
├── opencode.json                    # OpenCode-Konfiguration
├── .opencode/
│   └── agents/
│       ├── zielgruppe.md            # Agent 1: Zielgruppenanalyse
│       ├── marketing.md             # Agent 2: Marketingkonzept
│       ├── social-media.md          # Agent 3: Social-Media-Posts
│       ├── kalkulation.md           # Agent 4: Preiskalkulation
│       ├── website.md               # Agent 5: Landingpage
│       └── app-prototyp.md          # Agent 6: Web-Prototyp
├── server.py                        # Python-Backend (stdlib only)
├── dashboard/
│   ├── index.html                   # Dashboard SPA
│   ├── style.css                    # THM-Corporate-Design Styles
│   └── app.js                       # Frontend-Logik
├── produktlaunch/                   # Runtime: Agent-Outputs
│   ├── input/
│   │   └── produkt.md
│   ├── zielgruppe/
│   ├── marketing/
│   ├── social-media/
│   ├── kalkulation/
│   ├── website/
│   └── app-prototyp/
├── start.sh                         # Einziges Start-Skript
├── spec/                            # Bestehende Spec + Mockup
└── .gitignore
```

---

## Schritt-für-Schritt-Umsetzung

### Schritt 1: Grundgerüst & OpenCode-Konfiguration

**Dateien:**
- `opencode.json` – Provider + Modellkonfiguration
- `.opencode/agents/` – Verzeichnis für Agent-Definitionen
- `.gitignore` – produktlaunch/, node_modules, .opencode/node_modules, etc.

### Schritt 2: Agent-Systemprompts (6 Dateien)

Jeder Agent als `.opencode/agents/<name>.md` mit YAML-Frontmatter:

```yaml
---
description: <Kurzbeschreibung>
model: <konfigurierbar>
tools:
  bash: true
  read: true
  write: true
---
```

#### Agent 1: Zielgruppen-Agent (`zielgruppe.md`)
- **Liest:** `produktlaunch/input/produkt.md`
- **Schreibt:** `produktlaunch/zielgruppe/analyse.md`
- **Aufgabe:** Zielgruppenanalyse mit Personas (Name, Alter, Beruf, Interessen, Kaufmotivation, Schmerzpunkte), Marktsegmenten, Kaufkrafteinschätzung
- **Stil:** Strukturiertes Markdown mit Überschriften, Listen, ggf. Tabellen
- **Sprache:** Deutsch

#### Agent 2: Marketing-Agent (`marketing.md`)
- **Liest:** `produktlaunch/input/produkt.md` + `produktlaunch/zielgruppe/analyse.md`
- **Schreibt:** `produktlaunch/marketing/konzept.md`
- **Aufgabe:** Produktname (3 Vorschläge + Empfehlung), Slogan, Kernbotschaft, Positionierung, Elevator Pitch, Werbetext (ca. 150 Wörter)
- **Bezug:** Muss auf die Personas und Segmente der Zielgruppenanalyse eingehen

#### Agent 3: Social-Media-Agent (`social-media.md`)
- **Liest:** `produktlaunch/input/produkt.md` + `produktlaunch/zielgruppe/analyse.md` + `produktlaunch/marketing/konzept.md`
- **Schreibt:** `produktlaunch/social-media/instagram.md`, `linkedin.md`, `tiktok.md`
- **Aufgabe:** Je ein plattformspezifischer Post:
  - Instagram: visuell beschrieben, Hashtags, Story-Idee, Bildvorschlag
  - LinkedIn: professionell, B2B-Perspektive, Thought-Leadership
  - TikTok: kurz, catchy, Trend-Hook, Skript für 30s-Video
- **Bezug:** Nutzt Produktname/Slogan aus Marketing, spricht Personas gezielt an

#### Agent 4: Kalkulations-Agent (`kalkulation.md`)
- **Liest:** `produktlaunch/input/produkt.md`
- **Schreibt:** `produktlaunch/kalkulation/preiskalkulation.md`
- **Aufgabe:** Geschätzte Produktionskosten (Material, Fertigung, Verpackung), Vertriebskosten, Marge, Break-Even-Analyse, 3 Preisstrategien (Penetration, Skimming, Wettbewerb) mit Empfehlung
- **Format:** Markdown-Tabellen für Kostenaufstellung, Fließtext für Strategieempfehlung

#### Agent 5: Website-Agent (`website.md`)
- **Liest:** `produktlaunch/input/produkt.md` + `produktlaunch/zielgruppe/analyse.md` + `produktlaunch/marketing/konzept.md` + `produktlaunch/kalkulation/preiskalkulation.md`
- **Schreibt:** `produktlaunch/website/index.html` (+ ggf. `style.css`)
- **Aufgabe:** One-Page-Landingpage mit Hero, Features, Pricing, Testimonial-Platzhalter, CTA
- **Constraint:** Selbstständig lauffähiges HTML, modernes Design, responsive, Platzhalter-Bilder via CSS-Gradienten oder Emoji

#### Agent 6: App-Prototyp-Agent (`app-prototyp.md`)
- **Liest:** `produktlaunch/input/produkt.md` + alle bisherigen Outputs
- **Schreibt:** `produktlaunch/app-prototyp/spec.md` + `produktlaunch/app-prototyp/index.html` (+ weitere Dateien)
- **Aufgabe:** Erst eine kurze Spec (was die App kann), dann Implementierung als interaktiver Web-Prototyp (z.B. Konfigurator, Warenkorb, Rechner)
- **Constraint:** Rein Frontend (HTML/CSS/JS), alle Daten in-memory/LocalStorage, visuell ansprechend

### Schritt 3: Python-Backend (`server.py`)

**Eine einzige Datei, ~250-350 Zeilen, null Dependencies.**

Kern-Komponenten:

1. **Statischer Dateiserver** – liefert `dashboard/*` aus
2. **API-Endpunkte:**
   - `GET  /api/agents` – Liste aller Agenten mit Status + Dateianzahl
   - `POST /api/product` – Produktidee speichern → `produktlaunch/input/produkt.md`
   - `POST /api/agents/<name>/run` – Agent starten (optionaler Body: Refinement-Prompt)
   - `GET  /api/agents/<name>/stream` – SSE-Stream des laufenden Agent-Prozesses
   - `GET  /api/files/<agent>` – Liste der Artefakte eines Agenten
   - `GET  /api/files/<agent>/<datei>` – Dateiinhalt
3. **Prozess-Management:**
   - Pro Agent max. 1 laufender Prozess (dict: `agent_name → subprocess`)
   - Status-Tracking: `idle` | `running` | `done` | `error`
   - PTY für Subprocess → ANSI-Codes bleiben erhalten → xterm.js rendert Farben
4. **SSE-Streaming:**
   - Agent-stdout wird zeilenweise gelesen
   - Jede Zeile als `data: ...\n\n` an den SSE-Client gesendet
   - Bei Prozessende: `event: done\ndata: {exit_code}\n\n`

**Agent-Aufruf intern:**
```python
# Initialer Lauf
opencode run --agent zielgruppe "Analysiere die Zielgruppe für das Produkt."

# Nacharbeiten
opencode run --agent zielgruppe "Überarbeite deine Analyse. Feedback: <user input>"
```

### Schritt 4: Dashboard-Frontend (`dashboard/`)

Basiert auf dem bestehenden Mockup in `spec/ui-proto/dashboard.html` (THM-Design, 3-Spalten-Layout).

**Erweiterungen gegenüber dem Mockup:**

1. **Produkteingabe-Screen** (Startansicht)
   - Großes Eingabefeld für die Produktidee
   - "Los geht's!"-Button → speichert Produkt via API

2. **Agent-Steuerung** (linke Spalte)
   - Status-Dots: grau=idle, gelb-pulsierend=running, grün=done, rot=error
   - "Start"-Button pro Agent (nur klickbar wenn Abhängigkeiten erfüllt)
   - Abhängigkeitslogik im Frontend:
     - Zielgruppe + Kalkulation: sofort startbar
     - Marketing: nach Zielgruppe
     - Social Media: nach Marketing
     - Website: nach Zielgruppe + Marketing + Kalkulation
     - App-Prototyp: nach Produkteingabe (Spec), dann nach weiteren Outputs (Impl.)

3. **Terminal-View** (Hauptbereich, Tab 1)
   - xterm.js-Instanz pro Agent
   - SSE-Stream wird live in xterm.js geschrieben
   - Auto-Scroll, dunkles Theme passend zum Dashboard

4. **Ergebnis-View** (Hauptbereich, Tab 2)
   - marked.js rendert Markdown-Artefakte
   - Styling passend zum THM-Design (wie im Mockup)
   - Für `.html`-Artefakte: iframe mit "Im Browser öffnen"-Button

5. **Nacharbeiten-Input** (unterhalb des Hauptbereichs)
   - Textfeld + "Überarbeiten"-Button
   - Sendet Refinement-Prompt an denselben Agenten

**CDN-Dependencies (kein lokaler Download nötig):**
- Tailwind CSS (wie im Mockup)
- xterm.js + xterm-addon-fit
- marked.js
- Google Fonts (Inter, Space Grotesk)
- Material Symbols

### Schritt 5: Start-Skript (`start.sh`)

```bash
#!/bin/bash
set -euo pipefail

# Output-Verzeichnisse anlegen
mkdir -p produktlaunch/{input,zielgruppe,marketing,social-media,kalkulation,website,app-prototyp}

# Server starten
echo "Starting Ship It! Dashboard on http://localhost:8000"
python3 server.py &
SERVER_PID=$!

# Browser öffnen (macOS)
sleep 1
open http://localhost:8000

# Auf Ctrl+C warten, dann aufräumen
trap "kill $SERVER_PID 2>/dev/null; exit" INT TERM
wait $SERVER_PID
```

---

## Ablauf in der Demo

```
1. ./start.sh                    → Server + Browser
2. Produktidee eingeben           → "Nachhaltige Sneaker aus Apfelleder"
3. [Start Zielgruppe]             → Terminal zeigt Live-Arbeit
4. Review → OK oder Nacharbeiten
5. [Start Marketing + Kalkulation] → parallel, zwei Terminal-Tabs
6. Review
7. [Start Social Media]           → drei Posts entstehen
8. Review
9. [Start Website + App-Prototyp] → parallel
10. Website + App im Browser öffnen → Wow-Effekt
```

---

## Umsetzungsreihenfolge

| # | Was | Aufwand |
|---|-----|---------|
| 1 | `opencode.json` + `.opencode/agents/` (6 Prompts) | mittel |
| 2 | `server.py` (Backend) | mittel |
| 3 | `dashboard/` (Frontend, basierend auf Mockup) | mittel-groß |
| 4 | `start.sh` + `.gitignore` | klein |
| 5 | Integrations-Test (ein Produkt durchspielen) | test |

---

## Verifikation

1. `./start.sh` ausführen → Browser öffnet Dashboard
2. Produktidee eingeben → erscheint in `produktlaunch/input/produkt.md`
3. Zielgruppen-Agent starten → Terminal-Stream sichtbar, Output in `produktlaunch/zielgruppe/analyse.md`
4. Ergebnis-Tab zeigt gerendertes Markdown
5. Nacharbeiten testen → Agent überarbeitet Output
6. Alle 6 Agenten durchspielen → Website + App im iframe/Browser öffnen
