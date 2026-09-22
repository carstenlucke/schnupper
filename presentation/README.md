# Präsentation — Schnuppervorlesung „Digitalisierung und KI"

Slidev-Präsentation für die 90-minütige Schnuppervorlesung bei StudiumPlus
(Oberstufe). Sie liegt auf oberster Ebene des Repositorys, weil jede der Demos
— [`ship-it/`](../ship-it/), [`the-counting-agents/`](../the-counting-agents/),
[`agent-party/`](../agent-party/) — darin ihren Platz haben kann. Derzeit führt
sie auf die Live-Demo von **Ship It!** hin.

Gestaltet nach dem Claude-Design-System **„THM & StudiumPlus"**: helle
Inhaltsfolien mit Rubrik, Titel und grünem Balken, dunkle Rasterflächen für
Titel, Abschnitte und Schluss, gelbe Fragefolien. Das Design-System ist als
lokales Slidev-Theme unter [`theme-thm/`](theme-thm/) mitgeliefert.

## Voraussetzungen

- **Node.js** (≥ 20) und **npm**
- Internetzugang im Hörsaal für die Schrift Barlow (Google Fonts); ohne ihn
  fallen die Folien auf Helvetica/Arial zurück
- Beim ersten Start einmalig die Abhängigkeiten installieren:

  ```bash
  npm install
  ```

  Installiert Slidev, das Lucide-Icon-Set und `playwright-chromium`
  (Letzteres nur für den PDF-Export).

## Starten

```bash
npm run dev
```

Startet den Slidev-Dev-Server und öffnet die Präsentation im Browser
(Standard: <http://localhost:3030>). Änderungen an `slides.md` und am Theme
werden live neu geladen. Beenden mit `Ctrl+C`.

## Build & Export

```bash
npm run build    # statische HTML-Version in dist/
npm run export   # PDF nach schnuppervorlesung-ki.pdf
```

## Präsentationsdurchführung

### Vor der Vorlesung

1. **Ship It!-Dashboard** starten:

   ```bash
   cd ../ship-it
   ./start.sh
   ```

   Läuft auf <http://localhost:8000> und ist für die Live-Demo-Folien nötig.

2. **Slidev** in einem zweiten Terminal starten: `npm run dev`.

3. Browser-Tabs vorbereiten:
   - Tab 1: Slidev-Präsentation (<http://localhost:3030>)
   - Tab 2: Ship It!-Dashboard (<http://localhost:8000>)

4. **Vollbild** aktivieren: `F` in der Slidev-Ansicht.

### Während der Vorlesung

- **Navigation**: `→` / `Space` weiter, `←` zurück, `O` Folienübersicht.
- **Presenter-Modus**: `P` öffnet die Moderatoransicht mit Sprecher-Notizen
  (Notizen stehen als HTML-Kommentare in `slides.md`).
- **Zeichnen**: `D` aktiviert das Whiteboard-Overlay
  (`drawings.persist: false` — Zeichnungen werden beim Neuladen verworfen).
- **Gelbe Folien** sind Fragen an das Publikum: Hände hochheben lassen, kurze
  Rufrunde.
- **Live-Demo-Übergang**: Bei „Los geht's!" auf den Ship It!-Tab wechseln,
  Produkt von den Schülerinnen und Schülern vorschlagen lassen, die fünf
  Agenten durchlaufen.

## Dateien

| Datei / Ordner | Inhalt |
|---|---|
| `slides.md` | Folieninhalte, Sprecher-Notizen als HTML-Kommentare |
| `theme-thm/` | Lokales Slidev-Theme nach dem Design-System „THM & StudiumPlus": Layouts, Karten, Farben, Logos |
| `components/` | Folienspezifische Diagramme: Agent-Kreislauf, Abhängigkeiten der Ship-It!-Agenten |
| `global-top.vue` | Korrektur der Position des Slidev-Goto-Dialogs |
| `public/` | Logo von Ship It! |

Gestaltungsregeln und die Bedeutung der Bausteine stehen in
[CLAUDE.md](CLAUDE.md).

## Troubleshooting

- **Port 3030 belegt**: Slidev nimmt automatisch den nächsten freien Port —
  Konsolenausgabe beachten.
- **PDF-Export schlägt fehl**: `npx playwright install chromium` ausführen,
  falls die Browser-Binaries fehlen.
