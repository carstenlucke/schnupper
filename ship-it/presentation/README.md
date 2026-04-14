# Präsentation — Schnuppervorlesung "Digitalisierung und KI"

Slidev-Präsentation für die 90-minütige Schnuppervorlesung bei StudiumPlus (12. Klasse FOS). Begleitet die Live-Demo von **Ship It!** im Elternverzeichnis.

## Voraussetzungen

- **Node.js** (≥ 18)
- **npm**
- Beim ersten Start einmalig Abhängigkeiten installieren:

  ```bash
  npm install
  ```

  Installiert Slidev + `playwright-chromium` (letzteres wird nur für den PDF-Export benötigt).

## Starten

```bash
npm run dev
```

Startet den Slidev-Dev-Server und öffnet die Präsentation automatisch im Browser (Standard: <http://localhost:3030>). Änderungen an `slides.md` / `style.css` werden live neu geladen.

### Stoppen

Im Terminal `Ctrl+C` drücken. Der Dev-Server läuft nicht als Hintergrundprozess — schließt sich sauber mit dem Terminal.

## Build & Export

```bash
npm run build    # statische HTML-Version in dist/
npm run export   # PDF nach schnuppervorlesung-ki.pdf
```

Die aktuelle exportierte PDF liegt bereits als `schnuppervorlesung-ki.pdf` im Verzeichnis und kann als Fallback ohne laufenden Dev-Server gezeigt werden.

## Präsentationsdurchführung

### Vor der Vorlesung

1. **Ship It!-Dashboard** im Elternverzeichnis starten:

   ```bash
   cd ..
   ./start.sh
   ```

   Läuft auf <http://localhost:8000> und ist für die Live-Demo-Folien am Ende der Präsentation nötig.

2. **Slidev** in einem zweiten Terminal starten:

   ```bash
   npm run dev
   ```

3. Browser-Tabs vorbereiten:
   - Tab 1: Slidev-Präsentation (<http://localhost:3030>)
   - Tab 2: Ship It!-Dashboard (<http://localhost:8000>)
   - Beide Tabs auf den gleichen Bildschirm legen, damit der Wechsel flüssig bleibt.

4. **Vollbild** aktivieren: `F` in der Slidev-Ansicht.

### Während der Vorlesung

- **Navigation**: `→` / `Space` weiter, `←` zurück, `O` Folienübersicht, `D` Dark-/Light-Mode.
- **Presenter-Modus**: `P` öffnet die Moderatoransicht mit Sprecher-Notizen (Notizen stehen als HTML-Kommentare in `slides.md`).
- **Zeichnen**: `D` aktiviert das Whiteboard-Overlay (`drawings.persist: false` — Zeichnungen werden beim Neuladen verworfen).
- **Umfrage-Folien** (Icon 🙋): Hände hochheben lassen, kurze Rufrunde.
- **Live-Demo-Übergang**: Bei der Demo-Folie auf den Ship It!-Tab wechseln, Produkt von den Schülern vorschlagen lassen, die 5 Agenten durchlaufen.

### Nach der Vorlesung

- Slidev-Dev-Server mit `Ctrl+C` beenden.
- Ship It!-Server mit `Ctrl+C` beenden (oder `./start.sh --force` beim nächsten Start, falls Port 8000 blockiert ist).

## Dateien

| Datei / Ordner | Inhalt |
|---|---|
| `slides.md` | Folieninhalte (Markdown + Vue/HTML-Snippets), Sprecher-Notizen als HTML-Kommentare |
| `style.css` | THM-Corporate-Design, Karten, Layouts, Animationen |
| `global-top.vue` | Slidev-Global-Komponente (Font-Awesome o.ä.) |
| `public/` | Logos (THM, StudiumPlus, Ship It!) und SVG-Grafiken |
| `schnuppervorlesung-ki.pdf` | Exportierte PDF-Version als Fallback |
| `package.json` | Slidev-Scripts (`dev`, `build`, `export`) |

## Troubleshooting

- **Port 3030 belegt**: Slidev startet automatisch auf dem nächsten freien Port — Konsolenausgabe beachten.
- **PDF-Export schlägt fehl**: `npx playwright install chromium` ausführen, falls die Browser-Binaries fehlen.
- **Schriften / Icons fehlen**: Browser-Cache leeren und Dev-Server neu starten.
