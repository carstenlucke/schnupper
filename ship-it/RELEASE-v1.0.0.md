# Release v1.0.0 — Ship It!

**Ship It!** ist eine Live-Demo-Anwendung für eine Schnuppervorlesung bei StudiumPlus. Schülerinnen und Schüler wählen ein Produkt, 5 KI-Agenten übernehmen den kompletten Produktlaunch — von der Zielgruppenanalyse bis zur fertigen Website. Dieses Release umfasst die vollständige App sowie die begleitende Präsentation.

## Highlights

- **5 KI-Agenten im Zusammenspiel**: Zielgruppen-Analyst, Marketing-Experte, Social-Media-Manager, Controller und Web-Entwickler arbeiten koordiniert an einem Produktlaunch — mit automatischer Abhängigkeitssteuerung.
- **Live-Terminal im Browser**: Die Arbeit der Agenten wird in Echtzeit per SSE und xterm.js im Dashboard sichtbar — inklusive ANSI-Farben.
- **Schlüsselfertige Präsentation**: 90-Minuten-Slidev-Präsentation zum Thema „Digitalisierung und KI", inkl. interaktiver Elemente und PDF-Export.

## Ship It! App

### Dashboard

- 3-Spalten-Layout (Agent-Liste, Artefakt-Liste, Content-Area) für übersichtliche Navigation
- Drei Ansichtsmodi pro Agent: Terminal (Live-Output), Ergebnis (Markdown-Rendering) und Vorschau (HTML-iframe für die generierte Website)
- Persistente xterm.js-Terminals — Agentwechsel ohne Outputverlust
- Feedback-Workflow: Ergebnisse bewerten und Agenten mit gezieltem Feedback erneut starten
- Dateiverwaltung: Agent-Outputs einsehen, einzeln oder vollständig löschen
- THM-Corporate-Design mit Dark Mode

### Backend & Server

- Reines Python-Backend ohne externe Abhängigkeiten (nur stdlib)
- PTY-basierte Subprocess-Verwaltung für native Terminal-Ausgabe mit ANSI-Farben
- SSE-Streaming für Echtzeit-Updates im Browser
- Statusermittlung aus dem Dateisystem: kein State-File, Status wird aus Prozessliste und vorhandenen Output-Dateien abgeleitet
- Ein-Klick-Start über `start.sh` (Server + Browser)
- `.env`-Unterstützung für API-Keys

### KI-Agenten

- **Zielgruppen-Analyst**: Erstellt Personas und Zielgruppenanalyse aus der Produktbeschreibung
- **Marketing-Experte**: Entwickelt Marketingkonzept mit Name, Slogan und Werbetexten
- **Social-Media-Manager**: Generiert Posts für Instagram, LinkedIn und TikTok
- **Controller**: Erstellt Preiskalkulation und Preisstrategie
- **Web-Entwickler**: Baut eine responsive Produkt-Website (HTML/CSS/JS) auf Basis aller vorherigen Ergebnisse
- Automatische Abhängigkeitssteuerung: Zielgruppe und Kalkulation starten sofort, Marketing wartet auf Zielgruppe, Social Media auf Marketing, Website auf alle
- Prompt-Generierung mit expliziten Eingabe-/Ausgabe-Pfaden und optionalen Inputs (z.B. Logo, Instagram-Bild)

## Präsentation

### Inhalte & Didaktik

- Thema: „Digitalisierung und KI: Was Maschinen schon können" — für Schülerinnen und Schüler der 12. Klasse (FOS)
- Aufbau vom Bekannten zum Neuen: Alltags-KI (Spotify, TikTok, DeepL) → LLMs als Paradigmenwechsel → Chatbot vs. KI-Agent → Live-Demo
- Zentrale Analogie: Chatbot = Experte am Telefon, KI-Agent = Experte im Büro
- Agent-Kreislauf (Denken → Handeln → Prüfen) als didaktisches Kernmodell
- Interaktive Elemente: Umfragen, Produktwahl durch das Publikum, Bewertung der KI-Ergebnisse
- Reality Check: Kosten, Qualitätskontrolle, Halluzinationen und Datenschutz
- Abschluss mit Studienangeboten (BWL-Wirtschaftsinformatik, Softwaretechnologie bei StudiumPlus)

### Design & Technik

- Slidev-basierte Präsentation mit Dark Mode im THM-Corporate-Design
- Eigene SVG-Diagramme: Agent-Kreislauf und Agent-Abhängigkeiten
- Card-basiertes Layout-System mit farbcodierten Varianten
- PDF-Export über Playwright-Chromium
