# Ship It!

Live-Demo für eine Schnuppervorlesung (90 Min, 12. Klasse FOS). Schüler wählen ein Produkt, 5 KI-Agenten erledigen den kompletten Produktlaunch – von der Zielgruppenanalyse bis zur fertigen Landingpage.

## Quickstart

```bash
./start.sh
```

Öffnet das Dashboard unter [http://localhost:8000](http://localhost:8000). Beim ersten Start erscheint ein Willkommens-Screen zur Eingabe der ersten Produktidee.

### Voraussetzungen

- Python 3 (keine externen Dependencies)
- [OpenCode CLI](https://opencode.ai) installiert und konfiguriert
- GitHub-Copilot-Zugriff (in OpenCode als Provider konfiguriert) oder OpenAI API-Key (für Agenten mit `openai/`-Modellen und Bildgenerierung)

## Ablauf

```
1. Neues Projekt anlegen        → "Nachhaltige Sneaker aus Apfelleder"
2. [Start Zielgruppe]           → Terminal zeigt Live-Arbeit
3. Review → OK oder Nacharbeiten
4. [Start Marketing + Kalkulation] → parallel
5. Review
6. [Start Social Media]         → drei Posts entstehen
7. Review
8. [Start Website]              → Landingpage entsteht
9. Website im Browser öffnen    → Wow-Effekt
```

Mehrere Produkte können parallel existieren – im Header zwischen Projekten umschalten.

## Die 5 Agenten

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | **Zielgruppen-Agent** | Produktbeschreibung | Personas, Marktsegmente, Kaufkraft |
| 2 | **Marketing-Agent** | Produkt + Zielgruppe | Produktname, Slogan, Positionierung, Werbetext |
| 3 | **Social-Media-Agent** | Produkt + Zielgruppe + Marketing | Posts für Instagram, LinkedIn, TikTok |
| 4 | **Kalkulations-Agent** | Produktbeschreibung | Kostenaufstellung, Preisstrategien, Break-Even |
| 5 | **Website-Agent** | Alle bisherigen Outputs | Responsive One-Page-Landingpage (HTML) |

### Abhängigkeiten

```
Zielgruppe ──→ Marketing ──→ Social Media
                  │
Kalkulation ─────┤
                  ↓
               Website
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
├── .opencode/agents/          # 5 Agent-Systemprompts
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

## KI-Bildgenerierung

Marketing- und Social-Media-Agent können auf Knopfdruck Bilder generieren (Logo bzw. Instagram-Post). Die Bildgenerierung nutzt die OpenAI API (`gpt-image-1`).

### Einrichtung

```bash
cp .env.example .env
# OPENAI_API_KEY in .env eintragen
```

### Kosten pro Bild (gpt-image-1, Stand März 2026)

| Bild | Quality | Größe | Kosten (ca.) |
|------|---------|-------|-------------|
| Logo (Marketing) | low | 1024x1024 | $0.02–0.04 |
| Instagram-Bild (Social Media) | low | 1024x1024 | $0.02–0.04 |
| Instagram mit Logo-Referenz | low | 1024x1024 | $0.03–0.07 |

**Pro Projekt (alle Bilder):** ~$0.04–0.11

Die Kosten sind Token-basiert und variieren je nach Prompt-Länge und Bildkomplexität. Bei `quality: "low"` und 1024x1024 bleibt man im unteren Bereich. Für eine Vorlesung mit ~10 Projekten: **unter $1 Gesamtkosten**.

## Technical Debt

Bekannte, bewusst nicht behobene Probleme sind in [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md) dokumentiert.

## Lizenz

Lehrmaterial der THM – Technische Hochschule Mittelhessen.
