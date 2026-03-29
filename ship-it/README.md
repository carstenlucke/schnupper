# Ship It!

Live-Demo für eine Schnuppervorlesung (90 Min, 12. Klasse FOS). Schüler wählen ein Produkt, 6 KI-Agenten erledigen den kompletten Produktlaunch – von der Zielgruppenanalyse bis zum funktionalen App-Prototyp.

## Quickstart

```bash
./start.sh
```

Öffnet das Dashboard unter [http://localhost:8000](http://localhost:8000). Beim ersten Start erscheint ein Willkommens-Screen zur Eingabe der ersten Produktidee.

### Voraussetzungen

- Python 3 (keine externen Dependencies)
- [OpenCode CLI](https://opencode.ai) installiert und konfiguriert
- Anthropic API-Key (in OpenCode konfiguriert)

## Ablauf

```
1. Neues Projekt anlegen        → "Nachhaltige Sneaker aus Apfelleder"
2. [Start Zielgruppe]           → Terminal zeigt Live-Arbeit
3. Review → OK oder Nacharbeiten
4. [Start Marketing + Kalkulation] → parallel
5. Review
6. [Start Social Media]         → drei Posts entstehen
7. Review
8. [Start Website + App-Prototyp]  → parallel
9. Website + App im Browser öffnen → Wow-Effekt
```

Mehrere Produkte können parallel existieren – im Header zwischen Projekten umschalten.

## Die 6 Agenten

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | **Zielgruppen-Agent** | Produktbeschreibung | Personas, Marktsegmente, Kaufkraft |
| 2 | **Marketing-Agent** | Produkt + Zielgruppe | Produktname, Slogan, Positionierung, Werbetext |
| 3 | **Social-Media-Agent** | Produkt + Zielgruppe + Marketing | Posts für Instagram, LinkedIn, TikTok |
| 4 | **Kalkulations-Agent** | Produktbeschreibung | Kostenaufstellung, Preisstrategien, Break-Even |
| 5 | **Website-Agent** | Alle bisherigen Outputs | Responsive One-Page-Landingpage (HTML) |
| 6 | **App-Prototyp-Agent** | Alle bisherigen Outputs | Interaktive Web-App (HTML/CSS/JS) |

### Abhängigkeiten

```
Zielgruppe ──→ Marketing ──→ Social Media
                  │
Kalkulation ─────┤
                  ↓
              Website / App-Prototyp
```

Zielgruppe und Kalkulation sind sofort startbar, alle anderen warten auf ihre Vorgänger.

## Architektur

```
Browser (Dashboard)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess + pty
OpenCode CLI (opencode run --agent <name> <prompt>)
    ↕ Datei-I/O
projekte/<slug>/
```

- **Null externe Python-Dependencies** – `http.server` + `subprocess` + `pty`
- **Agent-Status aus dem Dateisystem abgeleitet** – kein State-File, crash-sicher
- **PTY-Subprozesse** – ANSI-Farben bleiben erhalten, xterm.js rendert sie im Browser
- **Projekt-Isolation** – jedes Produkt unter `projekte/<slug>/` mit eigenen Agent-Outputs

## Projektstruktur

```
ship-it/
├── opencode.json              # OpenCode-Konfiguration
├── .opencode/agents/          # 6 Agent-Systemprompts
├── server.py                  # Python-Backend (stdlib only)
├── dashboard/
│   ├── index.html             # Dashboard SPA
│   ├── style.css              # THM-Corporate-Design
│   └── app.js                 # Frontend-Logik
├── projekte/                  # Runtime: ein Ordner pro Produktidee
├── start.sh                   # Ein-Klick-Start
└── spec/                      # Spezifikation + UI-Mockup
```

## Dashboard-Features

- **Projekt-Selector** im Header mit Farbstatus (grau/gelb/grün)
- **Agent-Steuerung** mit Abhängigkeitslogik und Start-Buttons
- **Live-Terminal** (xterm.js) mit SSE-Streaming der Agent-Ausgabe
- **Ergebnis-Tab** rendert Markdown-Artefakte
- **Vorschau-Tab** zeigt HTML-Artefakte (Website, App) im iframe
- **Feedback-Input** zum Überarbeiten von Agent-Outputs

## Lizenz

Lehrmaterial der THM – Technische Hochschule Mittelhessen.
