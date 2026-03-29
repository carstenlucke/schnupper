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
projekte/<slug>/ (isoliertes Verzeichnis pro Produktidee)
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
├── projekte/                        # Runtime: ein Unterordner pro Produktidee
│   ├── nachhaltige-sneaker/         # Beispiel: Projekt 1
│   │   ├── produkt.md               # Produktbeschreibung (Input)
│   │   ├── zielgruppe/
│   │   │   └── analyse.md
│   │   ├── marketing/
│   │   │   └── konzept.md
│   │   ├── social-media/
│   │   │   ├── instagram.md
│   │   │   ├── linkedin.md
│   │   │   └── tiktok.md
│   │   ├── kalkulation/
│   │   │   └── preiskalkulation.md
│   │   ├── website/
│   │   │   └── index.html
│   │   └── app-prototyp/
│   │       ├── spec.md
│   │       └── index.html
│   └── lern-energy-drink/           # Beispiel: Projekt 2
│       ├── produkt.md
│       └── ...
├── start.sh                         # Einziges Start-Skript
├── spec/                            # Bestehende Spec + Mockup
└── .gitignore
```

### Projekt-/Session-Konzept

- Jede Produktidee erhält ein eigenes Verzeichnis unter `projekte/<slug>/`
- Der Slug wird beim Anlegen aus dem Produktnamen generiert (z.B. "Nachhaltige Sneaker" → `nachhaltige-sneaker`)
- `produkt.md` liegt direkt im Projektordner (kein `input/`-Unterordner nötig)
- Alle Agent-Outputs landen in ihren jeweiligen Unterordnern innerhalb des Projekts
- Projekte sind vollständig voneinander isoliert
- Im Dashboard kann man zwischen Projekten umschalten oder ein neues anlegen

---

## Schritt-für-Schritt-Umsetzung

### Schritt 1: Grundgerüst & OpenCode-Konfiguration

**Dateien:**
- `opencode.json` – Provider + Modellkonfiguration
- `.opencode/agents/` – Verzeichnis für Agent-Definitionen
- `.gitignore` – projekte/, node_modules, .opencode/node_modules, etc.

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

**Pfad-Konvention – Trennung Systemprompt vs. Run-Prompt:**

Die **Systemprompts** (`.opencode/agents/*.md`) definieren Rolle, Expertise und Output-Format – aber **keine konkreten Dateipfade**. Stattdessen enthalten sie die Anweisung:

> "Du erhältst in deiner Aufgabenstellung einen Projektordner sowie explizite EINGABE- und AUSGABE-Pfade. Verwende ausschließlich diese Pfade."

Die **Run-Prompts** (vom Backend generiert) enthalten die vollständigen, expliziten Pfade:

```
Projektordner: projekte/nachhaltige-sneaker

EINGABE:
- Produktbeschreibung: projekte/nachhaltige-sneaker/produkt.md

AUSGABE:
- Schreibe deine Analyse nach: projekte/nachhaltige-sneaker/zielgruppe/analyse.md
- Erstelle das Verzeichnis falls nötig.

Führe jetzt deine Aufgabe aus.
```

Das Backend kennt die Pfad-Templates pro Agent und setzt den Projekt-Slug ein. So gibt es keinen Interpretationsspielraum beim LLM.

**Pfad-Templates im Backend (server.py):**

```python
AGENT_PATHS = {
    "zielgruppe": {
        "inputs":  ["produkt.md"],
        "outputs": ["zielgruppe/analyse.md"],
    },
    "marketing": {
        "inputs":  ["produkt.md", "zielgruppe/analyse.md"],
        "outputs": ["marketing/konzept.md"],
    },
    "social-media": {
        "inputs":  ["produkt.md", "zielgruppe/analyse.md", "marketing/konzept.md"],
        "outputs": ["social-media/instagram.md", "social-media/linkedin.md", "social-media/tiktok.md"],
    },
    "kalkulation": {
        "inputs":  ["produkt.md"],
        "outputs": ["kalkulation/preiskalkulation.md"],
    },
    "website": {
        "inputs":  ["produkt.md", "zielgruppe/analyse.md", "marketing/konzept.md", "kalkulation/preiskalkulation.md"],
        "outputs": ["website/index.html"],
    },
    "app-prototyp": {
        "inputs":  ["produkt.md", "zielgruppe/analyse.md", "marketing/konzept.md", "kalkulation/preiskalkulation.md"],
        "outputs": ["app-prototyp/spec.md", "app-prototyp/index.html"],
    },
}
```

Das Backend baut daraus den Run-Prompt zusammen und kann nach Abschluss **verifizieren**, ob die erwarteten Output-Dateien tatsächlich erstellt wurden – und den Status entsprechend auf `done` oder `error` setzen.

#### Agent 1: Zielgruppen-Agent (`zielgruppe.md`)
- **Liest:** `{projekt}/produkt.md`
- **Schreibt:** `{projekt}/zielgruppe/analyse.md`
- **Aufgabe:** Zielgruppenanalyse mit Personas (Name, Alter, Beruf, Interessen, Kaufmotivation, Schmerzpunkte), Marktsegmenten, Kaufkrafteinschätzung
- **Stil:** Strukturiertes Markdown mit Überschriften, Listen, ggf. Tabellen
- **Sprache:** Deutsch

#### Agent 2: Marketing-Agent (`marketing.md`)
- **Liest:** `{projekt}/produkt.md` + `{projekt}/zielgruppe/analyse.md`
- **Schreibt:** `{projekt}/marketing/konzept.md`
- **Aufgabe:** Produktname (3 Vorschläge + Empfehlung), Slogan, Kernbotschaft, Positionierung, Elevator Pitch, Werbetext (ca. 150 Wörter)
- **Bezug:** Muss auf die Personas und Segmente der Zielgruppenanalyse eingehen

#### Agent 3: Social-Media-Agent (`social-media.md`)
- **Liest:** `{projekt}/produkt.md` + `{projekt}/zielgruppe/analyse.md` + `{projekt}/marketing/konzept.md`
- **Schreibt:** `{projekt}/social-media/instagram.md`, `linkedin.md`, `tiktok.md`
- **Aufgabe:** Je ein plattformspezifischer Post:
  - Instagram: visuell beschrieben, Hashtags, Story-Idee, Bildvorschlag
  - LinkedIn: professionell, B2B-Perspektive, Thought-Leadership
  - TikTok: kurz, catchy, Trend-Hook, Skript für 30s-Video
- **Bezug:** Nutzt Produktname/Slogan aus Marketing, spricht Personas gezielt an

#### Agent 4: Kalkulations-Agent (`kalkulation.md`)
- **Liest:** `{projekt}/produkt.md`
- **Schreibt:** `{projekt}/kalkulation/preiskalkulation.md`
- **Aufgabe:** Geschätzte Produktionskosten (Material, Fertigung, Verpackung), Vertriebskosten, Marge, Break-Even-Analyse, 3 Preisstrategien (Penetration, Skimming, Wettbewerb) mit Empfehlung
- **Format:** Markdown-Tabellen für Kostenaufstellung, Fließtext für Strategieempfehlung

#### Agent 5: Website-Agent (`website.md`)
- **Liest:** `{projekt}/produkt.md` + `{projekt}/zielgruppe/analyse.md` + `{projekt}/marketing/konzept.md` + `{projekt}/kalkulation/preiskalkulation.md`
- **Schreibt:** `{projekt}/website/index.html` (+ ggf. `style.css`)
- **Aufgabe:** One-Page-Landingpage mit Hero, Features, Pricing, Testimonial-Platzhalter, CTA
- **Constraint:** Selbstständig lauffähiges HTML, modernes Design, responsive, Platzhalter-Bilder via CSS-Gradienten oder Emoji

#### Agent 6: App-Prototyp-Agent (`app-prototyp.md`)
- **Liest:** `{projekt}/produkt.md` + alle bisherigen Outputs im Projektordner
- **Schreibt:** `{projekt}/app-prototyp/spec.md` + `{projekt}/app-prototyp/index.html` (+ weitere Dateien)
- **Aufgabe:** Erst eine kurze Spec (was die App kann), dann Implementierung als interaktiver Web-Prototyp (z.B. Konfigurator, Warenkorb, Rechner)
- **Constraint:** Rein Frontend (HTML/CSS/JS), alle Daten in-memory/LocalStorage, visuell ansprechend

### Schritt 3: Python-Backend (`server.py`)

**Eine einzige Datei, ~250-350 Zeilen, null Dependencies.**

Kern-Komponenten:

1. **Statischer Dateiserver** – liefert `dashboard/*` aus
2. **API-Endpunkte:**
   - `GET  /api/projekte` – Liste aller Projekte (Slug + Name)
   - `POST /api/projekte` – Neues Projekt anlegen (Body: `{name, beschreibung}`) → erzeugt Verzeichnis + `produkt.md`
   - `GET  /api/projekte/<slug>/agents` – Liste aller Agenten mit Status + Dateianzahl für dieses Projekt
   - `POST /api/projekte/<slug>/agents/<name>/run` – Agent starten (optionaler Body: Refinement-Prompt)
   - `GET  /api/projekte/<slug>/agents/<name>/stream` – SSE-Stream des laufenden Agent-Prozesses
   - `GET  /api/projekte/<slug>/files/<agent>` – Liste der Artefakte eines Agenten
   - `GET  /api/projekte/<slug>/files/<agent>/<datei>` – Dateiinhalt
3. **Prozess-Management & Status:**
   - Pro Projekt+Agent max. 1 laufender Prozess (dict: `(slug, agent_name) → subprocess`)
   - **Status wird aus dem Dateisystem abgeleitet** (kein extra State-File):
     - `done`: alle erwarteten Output-Dateien in `AGENT_PATHS[agent]["outputs"]` existieren
     - `running`: Subprocess ist aktiv (nur in-memory, geht bei Crash verloren – korrekt, weil Prozess auch weg)
     - `idle`: weder running noch done
     - `error`: Subprocess beendet, aber Output-Dateien fehlen (in-memory, fällt nach Crash zurück auf `idle`)
   - **Crash-sicher:** Nach Server-Neustart erkennt das Backend bereits fertige Agenten anhand der vorhandenen Dateien. Kein State kann veralten oder inkonsistent werden.
   - PTY für Subprocess → ANSI-Codes bleiben erhalten → xterm.js rendert Farben
4. **SSE-Streaming:**
   - Agent-stdout wird zeilenweise gelesen
   - Jede Zeile als `data: ...\n\n` an den SSE-Client gesendet
   - Bei Prozessende: `event: done\ndata: {exit_code}\n\n`

**Agent-Aufruf intern – Prompt-Generierung:**
```python
def build_run_prompt(slug: str, agent: str, feedback: str = None) -> str:
    """Baut den vollständigen Run-Prompt mit expliziten Pfaden."""
    p = f"projekte/{slug}"
    paths = AGENT_PATHS[agent]

    # Bei Refinement: eigene Outputs werden zusätzlich als Inputs aufgelistet,
    # damit der Agent seine bisherige Arbeit lesen und überarbeiten kann
    eingaben = [f"{p}/{f}" for f in paths["inputs"]]
    if feedback:
        for f in paths["outputs"]:
            full = f"{p}/{f}"
            if full not in eingaben and os.path.exists(full):
                eingaben.append(f"{full}  ← deine bisherige Ausgabe")

    eingaben_str = "\n".join(f"- {e}" for e in eingaben)
    ausgaben_str = "\n".join(f"- {p}/{f}" for f in paths["outputs"])

    if feedback:
        aufgabe = (
            "Überarbeite deine bisherige Ausgabe.\n"
            f"Feedback vom Nutzer: \"{feedback}\""
        )
    else:
        aufgabe = "Führe deine Aufgabe aus."

    return f"""Projektordner: {p}

EINGABE (lies diese Dateien):
{eingaben_str}

AUSGABE (schreibe in diese Dateien, erstelle Verzeichnisse falls nötig):
{ausgaben_str}

{aufgabe}"""

# Aufruf:
# opencode run --agent zielgruppe "<generierter prompt>"
```

**Nach Abschluss – Output-Verifikation:**
```python
def verify_outputs(slug: str, agent: str) -> bool:
    """Prüft ob die erwarteten Output-Dateien existieren."""
    for f in AGENT_PATHS[agent]["outputs"]:
        if not os.path.exists(f"projekte/{slug}/{f}"):
            return False
    return True
```

### Schritt 4: Dashboard-Frontend (`dashboard/`)

Basiert auf dem bestehenden Mockup in `spec/ui-proto/dashboard.html` (THM-Design, 3-Spalten-Layout).

**Erweiterungen gegenüber dem Mockup:**

1. **Projekt-Auswahl / Neues Projekt**

   **Header-Projekt-Selector:**
   ```
   ┌──────────────────────────────────────────────────────────────┐
   │  Ship It! Dashboard  │ 🟢 Nachhaltige Sneaker ▾ │   ● Live  │
   └──────────────────────┼──────────────────────────┼───────────┘
                          │ ✓ Nachhaltige Sneaker    │
                          │   Lern-Energy-Drink      │
                          │ ──────────────────────── │
                          │   + Neues Projekt         │
                          └──────────────────────────┘
   ```
   - Dropdown im Header zeigt alle Projekte (via `GET /api/projekte`)
   - Farbiger Dot pro Projekt: grau = frisch, gelb = in Arbeit, grün = alle Agenten fertig
   - "**+ Neues Projekt**" im Dropdown öffnet Eingabe-Dialog (Produktname + Kurzbeschreibung)
   - Projektwechsel lädt Agent-Status + Artefakte des gewählten Projekts neu
   - URL enthält den Slug als Hash (`#nachhaltige-sneaker`) → Browser-Refresh behält Projekt bei

   **Erster Start (kein Projekt vorhanden):**
   - Statt 3-Spalten-Layout: zentrierter Willkommens-Screen mit Eingabefeld für die erste Produktidee
   - Nach Anlegen des ersten Projekts: Wechsel zum normalen Dashboard-Layout

2. **Agent-Steuerung** (linke Spalte)
   - Status-Dots: grau=idle, gelb-pulsierend=running, grün=done, rot=error
   - "Start"-Button pro Agent (nur klickbar wenn Abhängigkeiten erfüllt)
   - Status ist projektspezifisch – jedes Projekt hat seinen eigenen Agent-Fortschritt
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

# Projekte-Verzeichnis anlegen (Unterordner werden pro Projekt dynamisch erstellt)
mkdir -p projekte

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
1. ./start.sh                       → Server + Browser
2. "Neues Projekt" anlegen           → "Nachhaltige Sneaker aus Apfelleder"
3. [Start Zielgruppe]                → Terminal zeigt Live-Arbeit
4. Review → OK oder Nacharbeiten
5. [Start Marketing + Kalkulation]   → parallel, zwei Terminal-Tabs
6. Review
7. [Start Social Media]              → drei Posts entstehen
8. Review
9. [Start Website + App-Prototyp]    → parallel
10. Website + App im Browser öffnen  → Wow-Effekt

--- Optional: Zweite Runde ---
11. "Neues Projekt" anlegen          → "Lern-Energy-Drink"
12. Gleicher Ablauf, altes Projekt bleibt erhalten
13. Zwischen Projekten umschalten zum Vergleichen
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
2. Neues Projekt anlegen → Verzeichnis `projekte/<slug>/` wird erstellt, `produkt.md` geschrieben
3. Zielgruppen-Agent starten → Terminal-Stream sichtbar, Output in `projekte/<slug>/zielgruppe/analyse.md`
4. Ergebnis-Tab zeigt gerendertes Markdown
5. Nacharbeiten testen → Agent überarbeitet Output
6. Alle 6 Agenten durchspielen → Website + App im iframe/Browser öffnen
7. Zweites Projekt anlegen → eigenes Verzeichnis, eigener Agent-Fortschritt
8. Zwischen Projekten umschalten → Status und Artefakte wechseln korrekt
