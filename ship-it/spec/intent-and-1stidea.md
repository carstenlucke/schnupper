
# Ship It! – Produktlaunch Multi-Agenten-Demo

## Kurzbeschreibung

Live-Demo für eine Schnuppervorlesung an der Theodor-Heuss-Schule Wetzlar (12. Klasse Fachoberschule, Fach: wirtschaftsbezogene Planspiele). Mehrere KI-Agenten arbeiten parallel an einem Produktlaunch – von der Zielgruppenanalyse über Marketing-Texte und Social-Media-Posts bis hin zu Preiskalkulation und einem funktionsfähigen Web-Prototyp. Die Schülerinnen und Schüler wählen das Produkt selbst und verfolgen live, wie die Agenten arbeiten.

---

## Kontext

- **Anfrage:** Lehrkraft Tobias Möglich, Theodor-Heuss-Schule Wetzlar
- **Zielgruppe:** 12. Klasse FOS, Schwerpunkt Wirtschaft/Informatik
- **Unterrichtsfach:** wirtschaftsbezogene Planspiele
- **Zeitrahmen:** Mittwoch, 9:45–11:15 Uhr (90 Minuten)
- **Deadline:** Ende April 2026 (Abschlussprüfungen)
- **Thema:** Digitalisierung und KI-Einsatz in Unternehmen

---

## Szenario

Die Schülerinnen und Schüler nennen ein Produkt (z.B. "nachhaltige Sneaker aus Apfelleder", "eine App zum Tauschen von Schulbüchern", "ein Energy Drink für Lernphasen"). Ein Team aus KI-Agenten übernimmt daraufhin den kompletten Produktlaunch – jeder Agent aus seiner fachlichen Rolle heraus, parallel und live beobachtbar.

---

## Beteiligte Agenten

### 1. Zielgruppen-Agent

- Analysiert, wer das Produkt kaufen würde
- Erstellt Personas (Alter, Interessen, Kaufmotivation, Schmerzpunkte)
- Identifiziert Marktsegmente
- Output: strukturierte Zielgruppenanalyse (Markdown)

### 2. Marketing-Agent

- Liest die Zielgruppenanalyse
- Entwickelt Produktname, Slogan, Kernbotschaft
- Verfasst einen Werbetext / eine Produktbeschreibung
- Output: Marketingkonzept mit Texten (Markdown)

### 3. Social-Media-Agent

- Liest Zielgruppenanalyse + Marketingkonzept
- Erstellt plattformspezifische Posts:
  - **Instagram:** visuell, Hashtags, Story-Idee
  - **LinkedIn:** professionell, B2B-Perspektive
  - **TikTok:** kurz, catchy, Trend-orientiert
- Output: fertige Posts pro Plattform (Markdown)

### 4. Kalkulations-Agent

- Schätzt Produktionskosten, Vertriebskosten, Marge
- Erstellt eine einfache Preiskalkulation
- Schlägt Preisstrategien vor (Penetration, Skimming, etc.)
- Output: Kalkulationstabelle + Preisempfehlung (Markdown)

### 5. Website-Agent

- Erstellt eine **One-Page-Website** für das Produkt (Landingpage / Produktseite)
- Reines HTML + CSS + JavaScript, ggf. mit eingebettetem Bild-Platzhalter
- Kann direkt als `index.html` im Browser geöffnet werden; falls nötig (z.B. bei Fetch-Aufrufen oder ES-Modulen) via `python -m http.server`
- Inhalt: Hero-Section, Produktbeschreibung, Features, Pricing, Call-to-Action
- Greift auf Outputs von Zielgruppen-, Marketing- und Kalkulations-Agent zurück
- Output: lauffähige `index.html` (+ ggf. `style.css`)

### 6. App-Prototyp-Agent `[experimental – nice to have]`

- Erstellt zunächst eine kurze **Spezifikation**: Was soll die App können? (z.B. Produktkonfigurator, Warenkorbsimulation, Preisrechner)
- Implementiert anschließend einen **funktionsfähigen Web-Prototyp**
- **Rein Frontend-basiert:** HTML + CSS + JavaScript, kein echtes Backend
- Alle Datenhaltung **lokal im Browser** (z.B. LocalStorage, In-Memory)
- Auslieferung via `python -m http.server` (kein App-Server, kein Build-Prozess)
- Im Sinne eines Prototyps: visuell ansprechend, interaktiv, aber ohne echte Datenverarbeitung
- Output: Spezifikation (Markdown) + lauffähige App-Dateien

---

## Ablauf der Demo

```
Phase 1: Produktidee einsammeln
  └─ Schüler nennen ein Produkt
  └─ Kurze Klärung: Was ist das? Für wen?

Phase 2: Agenten starten (tmux)
  └─ Alle 6 Agenten bekommen das Produkt als Input
  └─ Agenten 1 (Zielgruppe) und 4 (Kalkulation) starten sofort
  └─ Agent 6 (App-Prototyp) startet mit Spezifikation

Phase 3: Abhängige Agenten arbeiten
  └─ Agent 2 (Marketing) startet nach Zielgruppenanalyse
  └─ Agent 3 (Social Media) startet nach Marketing
  └─ Agent 5 (Website) startet nach Zielgruppe + Marketing + Kalkulation
  └─ Agent 6 beginnt Implementierung nach Spezifikation

Phase 4: Ergebnisse präsentieren
  └─ Alle Outputs durchgehen
  └─ Website + App-Prototyp im Browser öffnen
  └─ Diskussion mit den Schülern
```

---

## Technische Umsetzung

### tmux-Layout

```
+---------------------+---------------------+
| Zielgruppen-Agent   | Marketing-Agent     |
+---------------------+---------------------+
| Social-Media-Agent  | Kalkulations-Agent  |
+---------------------+---------------------+
| Website-Agent       | App-Prototyp-Agent  |
+---------------------+---------------------+
```

Jeder Pane zeigt einen Agenten (z.B. als OpenCode- oder Claude-CLI-Instanz). Die Agenten laufen als LLM-gestützte Prozesse mit jeweils eigenem Systemprompt.

### Dashboard-App (Ergebnis-Viewer)

Zusätzlich zur tmux-Ansicht (die den Arbeitsprozess zeigt) gibt es eine **dedizierte Web-App**, die die fertigen Ergebnisse übersichtlich darstellt. Diese App läuft parallel auf einem eigenen Port und wird z.B. auf einem zweiten Bildschirm oder per Beamer gezeigt.

**Layout (3-Spalten):**

```
+----------------+--------------------+------------------------------+
| Agenten        | Artefakte          | Hauptbereich                 |
|                |                    |                              |
| ● Zielgruppe   | analyse.md        |  ┌──────────────────────┐    |
| ○ Marketing    |                    |  │                      │    |
| ○ Social Media |                    |  │  Markdown-Rendered   │    |
| ○ Kalkulation  |                    |  │  Leseansicht         │    |
| ○ Website      |                    |  │                      │    |
| ○ App-Prototyp |                    |  │                      │    |
|                |                    |  └──────────────────────┘    |
+----------------+--------------------+------------------------------+
  Navigation        Dateiliste           Markdown-Viewer
```

- **Linke Spalte:** Navigation der Agenten. Klick auf einen Agenten zeigt dessen Artefakte in der mittleren Spalte.
- **Mittlere Spalte:** Liste der erzeugten Dateien des gewählten Agenten (`.md`, `.html`, etc.). Klick auf eine Datei öffnet sie im Hauptbereich.
- **Rechte Spalte (Hauptbereich):** Markdown-Viewer, der `.md`-Dateien gerendert darstellt. Für `.html`-Artefakte (Website, App-Prototyp) ggf. ein eingebetteter iframe oder ein "Im Browser öffnen"-Link.

**Technischer Ansatz:**

- Rein frontend-basiert (HTML + CSS + JS)
- Markdown-Rendering via JavaScript-Bibliothek (z.B. marked.js oder markdown-it)
- Ein minimaler Python-Server liefert die App aus und stellt eine einfache API bereit:
  - `GET /api/agents` – Liste der Agenten mit ihren Output-Verzeichnissen
  - `GET /api/files/<agent>` – Liste der Artefakte eines Agenten
  - `GET /api/content/<agent>/<datei>` – Inhalt einer Datei
- Alternativ: ein Watcher-Skript, das periodisch eine `index.json` mit der aktuellen Verzeichnisstruktur erzeugt, sodass das Frontend ohne echte API auskommt
- **Live-Aktualisierung:** Polling oder einfacher Refresh-Button, damit neue Ergebnisse sichtbar werden, sobald ein Agent fertig ist

**UI-Design-Beschreibung (Google Stitch Prompt):**

~~~markdown
A full-screen, dark-themed web dashboard (no scrolling on the outer shell) with a fixed 3-column layout for monitoring AI agent outputs in real time. The design follows the THM (Technische Hochschule Mittelhessen) corporate design color scheme.

STRICT COLOR RULES – THM Corporate Design:
- Primary brand color (THM Grün): #80BA24 – use for primary accents, active states, "done" status, header highlights
- Primary neutral (THM Grau): #4A5C66 – use for sidebar backgrounds, muted elements, inactive states
- Secondary Red (THM Rot): #9C132E – use for error states or critical badges
- Secondary Yellow (THM Gelb): #F4AA00 – use for "working/in progress" status indicators
- Secondary Light Blue (THM Hellblau): #00B8E4 – use for selected/active accent borders and interactive highlights
- Secondary Blue (THM Blau): #002878 – use for dark backgrounds, header bar, deep UI surfaces
- Derive all other shades (dark backgrounds, hover states, muted text) from these base colors. Do NOT use arbitrary colors outside this palette.

Header bar (top, full width, ~48px height, background THM Blau #002878):
- Left: App title "Ship It! Dashboard" in bold, white, 18px. Optionally a small THM Grün accent line below the title.
- Right: a small circular refresh icon button and a THM Grün #80BA24 pulsing dot labeled "Live" when agents are still working, or a THM Grau #4A5C66 dot labeled "Fertig" when done

Column 1 – Agent Navigation (left sidebar, fixed width ~220px, full height below header, dark background derived from THM Grau, e.g. #2e3a40):
- Section label "Agenten" at the top, muted (lighter THM Grau), uppercase, small font
- Below: a vertical list of 6 agent entries, each as a card-like row with:
  - A colored status dot on the left: THM Grün #80BA24 = done, THM Gelb #F4AA00 animated spinner = working, THM Grau #4A5C66 = waiting
  - Agent name in white, 14px, medium weight
  - A small badge below the name showing the number of generated artifacts, e.g. "2 Dateien"
- The agents in order:
  1. Zielgruppen-Agent
  2. Marketing-Agent
  3. Social-Media-Agent
  4. Kalkulations-Agent
  5. Website-Agent
  6. App-Prototyp-Agent (with a small "experimental" pill badge in THM Gelb #F4AA00 next to the name)
- The currently selected agent has a slightly lighter background and a left accent border (4px, THM Hellblau #00B8E4)
- Hover: subtle background lighten

Column 2 – Artifact List (middle panel, fixed width ~250px, background slightly lighter than column 1, e.g. #354850):
- Section label showing the selected agent's name, e.g. "Marketing-Agent", bold white, 16px, at the top
- Below: a vertical list of files produced by that agent. Each file entry shows:
  - A file type icon on the left (document icon for .md, code icon for .html, table icon for .csv)
  - Filename in white, 14px, e.g. "konzept.md"
  - A secondary line in muted gray showing file size or last modified time, e.g. "vor 2 Min."
- The currently selected file has a highlighted background and left accent border (THM Hellblau #00B8E4)
- If the agent has no output yet: a centered muted message "Noch keine Ergebnisse…" with a subtle loading animation

Column 3 – Main Content Area (right, takes remaining width, background very dark, e.g. #1a2530):
- When a .md file is selected: rendered Markdown content in a readable, well-spaced layout. White text on dark background. Headings in white with THM Grün underline accent. Body text in light gray (#d0d8dd). Code blocks with a slightly lighter background. Tables with subtle borders using THM Grau. Generous padding (40px horizontal, 24px vertical).
- When an .html file is selected: an embedded iframe showing the rendered HTML page, with a floating action button in the top-right corner labeled "Im Browser öffnen" (styled with THM Grün background, white text)
- When nothing is selected: a large centered placeholder with a muted rocket icon (THM Grau) and the text "Wähle einen Agenten und ein Artefakt aus"

Typography: Inter or system sans-serif. Clean, modern.

Color palette summary (THM Corporate Design):
- THM Grün #80BA24 – primary accent, done status, buttons, active highlights
- THM Grau #4A5C66 – neutral, sidebar base, inactive/waiting, muted text base
- THM Blau #002878 – header, deep backgrounds
- THM Hellblau #00B8E4 – selection borders, interactive accents
- THM Gelb #F4AA00 – working/progress status, experimental badge
- THM Rot #9C132E – reserved for errors/warnings
- Text white #f1f1f1, body text #d0d8dd, muted text derived from THM Grau lightened

Sample data to show in the prototype:
- Zielgruppen-Agent (status: done, 1 file): "analyse.md" → rendered Markdown with headings "Primäre Zielgruppe", "Personas", "Marktsegmente"
- Marketing-Agent (status: done, 1 file): "konzept.md" → rendered Markdown with product name, slogan, copy text
- Social-Media-Agent (status: working, 3 files): "instagram.md", "linkedin.md", "tiktok.md"
- Kalkulations-Agent (status: done, 1 file): "preiskalkulation.md" → Markdown with a pricing table
- Website-Agent (status: working, 0 files)
- App-Prototyp-Agent (status: waiting, 0 files, THM Gelb "experimental" badge)
~~~

**Didaktischer Mehrwert:**

- tmux zeigt den **Prozess** (wie Agenten arbeiten)
- Dashboard zeigt die **Ergebnisse** (was Agenten produziert haben)
- Zwei komplementäre Perspektiven auf dasselbe System

### Kommunikation zwischen Agenten

- Verzeichnisbasiert: ein gemeinsames Projektverzeichnis
- Unterordner pro Agent für Outputs
- Abhängige Agenten pollen oder watchen auf Dateien der Vorgänger-Agenten
- Alternativ: einfaches Skript, das Agenten sequenziell/parallel orchestriert

### Ordnerstruktur

```
produktlaunch/
├── input/
│   └── produkt.md              ← Produktbeschreibung
├── zielgruppe/
│   └── analyse.md              ← Output Agent 1
├── marketing/
│   └── konzept.md              ← Output Agent 2
├── social-media/
│   ├── instagram.md
│   ├── linkedin.md
│   └── tiktok.md               ← Output Agent 3
├── kalkulation/
│   └── preiskalkulation.md     ← Output Agent 4
├── app-prototyp/
│   ├── spec.md                 ← Spezifikation Agent 5
│   ├── index.html              ← Prototyp Agent 5
│   └── ...                     ← weitere App-Dateien
├── website/
│   ├── index.html              ← Landingpage Agent 6
│   └── style.css               ← (optional)
└── systemprompts/
    ├── zielgruppe.md
    ├── marketing.md
    ├── social-media.md
    ├── kalkulation.md
    ├── app-prototyp.md
    └── website.md
```

---

## Zeitplan (90 Minuten)

| Zeit | Phase | Inhalt |
|---|---|---|
| 0:00–0:10 | Intro | Vorstellung, Was sind KI-Agenten?, Was passiert heute? |
| 0:10–0:15 | Produktwahl | Schüler schlagen Produkte vor, Abstimmung |
| 0:15–0:20 | Setup | Produkt als Input einspeisen, tmux-Session zeigen |
| 0:20–0:45 | Live-Demo | Agenten arbeiten, Kommentierung, Zwischenfragen |
| 0:45–0:55 | Ergebnisse | Outputs durchgehen, Website + App-Prototyp im Browser zeigen |
| 0:55–1:15 | Diskussion | Was hat gut funktioniert? Was nicht? Wo liegen Grenzen? |
| 1:15–1:30 | Ausblick | Studium, Wirtschaftsinformatik, Fragen |

---

## Didaktischer Fokus

- **Digitalisierung greifbar machen:** Schüler sehen live, wie KI-Werkzeuge in Unternehmensprozesse eingebettet werden können
- **Arbeitsteilung durch Agenten:** Parallele Spezialisierung statt eines Alleskönnners
- **Vom Konzept zum Prototyp:** Der gesamte Weg vom Produktnamen bis zur lauffähigen Web-App in Minuten
- **Kritische Reflexion:** Was kann KI gut? Wo sind Grenzen? Würdet ihr dem Ergebnis vertrauen?
- **Bezug zum Planspiel:** Investitionsentscheidung, Markteinführung, Wettbewerbsstrategie

---

## Erweiterungsmöglichkeiten

- Zweite Runde mit anderem Produkt (zeigt Flexibilität)
- Schüler bewerten die Agenten-Outputs (Welcher Post ist am besten?)
- Vergleich: Was würdet ihr anders machen als die KI?
- Ein Agent erstellt eine Pitch-Präsentation als Zusammenfassung

---

## Siehe auch

- [[KI-Agenten Demo-Projekte – Übersicht]] – Übersicht aller Agenten-Demo-Projekte
- [[Multi-Agenten-System zur Verarbeitung von Rezensionen]] – alternatives Demo-Szenario mit Rezensionsverarbeitung
- [[Zählende Agenten - Simulation im Terminal (Tmux)]] – einfachere technische Demo, bereits implementiert
