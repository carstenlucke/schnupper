# Präsentation — Schnuppervorlesung „Digitalisierung und KI"

Slidev-Präsentation für die 90-minütige Schnuppervorlesung bei StudiumPlus
(Oberstufe). Sie liegt auf oberster Ebene des Repositorys, weil jede der Demos
— [`ship-it/`](../ship-it/), [`the-counting-agents/`](../the-counting-agents/),
[`agent-party/`](../agent-party/) — darin ihren Platz haben kann. Welche Demo eine
Vorlesung zeigt, entscheidet man auf der Übersichtsfolie per Klick (siehe
[Demos auswählen](#demos-auswählen)).

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

## Demos auswählen

Die Folie **„Welche Demo schauen wir uns an?"** am Anfang des Abschnitts
„Agenten live erleben" ist die Übersicht: drei Karten, ein Klick springt an
den Anfang der Demo. Die Demos sind Abzweige von dieser Folie, keine Folge:

- Auf jeder Demo-Folie führt **„Demos"** unten in der Mitte der Fußzeile
  zurück zur Übersicht.
- Jede Demo endet mit einer Abschlussfolie: **„Noch eine Demo"** führt zur
  Übersicht, **„Was nehmen wir mit?"** weiter zum Schluss.
- Mit der Pfeiltaste geht es am Ende einer Demo ebenfalls zum Schluss, nicht
  in die nächste Demo. Rückwärts aus einer Demo heraus geht es zur Übersicht.
- Ohne Klick führt `→` von der Übersicht in die erste Demo (Ship It!).

Grenzen: Folienübersicht (`O`), das Vorschaubild „nächste Folie" in der
Moderatoransicht und der PDF-Export zeigen alle Folien in ihrer Reihenfolge.
Die Seitenzahlen sind die durchgehenden Foliennummern.

Die Demo-Blöcke liegen je als eigener Foliensatz unter [`demos/`](demos/);
`slides.md` bindet sie per `src:` ein und kennzeichnet sie mit `demo:`.
`hide: true` an einem Eintrag nimmt eine Demo ganz heraus.

**Die Reflexion ist zweigeteilt.** Jeder Demo-Block endet mit einer eigenen
Bewertung dessen, was man gerade gesehen hat — die Fragen unterscheiden sich
je Demo grundlegend. Der Reality Check (Kosten, Qualitätskontrolle,
Halluzinationen, Datenschutz) gilt für alle und kommt einmal im gemeinsamen
Schluss; seine Sprecher-Notizen nennen für jede Demo das passende Beispiel.

## Präsentationsdurchführung

### Vor der Vorlesung

1. **Die ausgewählten Demos** starten — jede nach ihrer eigenen README:

   | Demo | Start | Adresse |
   |---|---|---|
   | Ship It! | `cd ../ship-it && ./start.sh` | <http://localhost:8000> |
   | The Counting Agents | aus einem Herdr-Pane: `cd ../the-counting-agents && ./scripts/start.sh` | Dashboard <http://localhost:8777> |
   | Agent Party | `cd ../agent-party && ./start.sh` | <http://localhost:8100> |

2. **Slidev** in einem weiteren Terminal starten: `npm run dev`.

3. Browser-Tabs vorbereiten: Slidev-Präsentation (<http://localhost:3030>)
   und je ein Tab pro Demo.

4. **Vollbild** aktivieren: `F` in der Slidev-Ansicht.

### Während der Vorlesung

- **Navigation**: `→` / `Space` weiter, `←` zurück, `O` Folienübersicht.
- **Presenter-Modus**: `P` öffnet die Moderatoransicht mit Sprecher-Notizen
  (Notizen stehen als HTML-Kommentare in `slides.md`).
- **Zeichnen**: `D` aktiviert das Whiteboard-Overlay
  (`drawings.persist: false` — Zeichnungen werden beim Neuladen verworfen).
- **Gelbe Folien** sind Fragen an das Publikum: Hände hochheben lassen, kurze
  Rufrunde.
- **Demo wählen**: Auf der Übersichtsfolie die Karte der Demo anklicken.
- **Live-Demo-Übergang**: Bei „Los geht's!" auf den Tab der Demo wechseln.
  Was dort zu zeigen ist, steht in den Sprecher-Notizen dieser Folie.

## Dateien

| Datei / Ordner | Inhalt |
|---|---|
| `slides.md` | Gemeinsamer Handlungsstrang mit der Übersicht der Demos; Sprecher-Notizen als HTML-Kommentare |
| `demos/` | Ein Foliensatz je Demo: Vorstellung, Aufbau, Mitmachfrage, Übergang, Bewertung |
| `setup/main.ts` | Blättern an den Rändern der Demos: am Ende weiter zum Schluss, rückwärts zur Übersicht |
| `slide-bottom.vue` | Der Link „Demos" in der Fußzeile jeder Demo-Folie |
| `theme-thm/` | Lokales Slidev-Theme nach dem Design-System „THM & StudiumPlus": Layouts, Karten, Farben, Logos |
| `components/` | Folienspezifische Bausteine: Demo-Übersicht und -Abschluss, Werkzeug-Übersicht, Agent-Kreislauf, Abhängigkeiten der Ship-It!-Agenten, Nachrichtenwege der Counting Agents |
| `global-top.vue` | Korrektur der Position des Slidev-Goto-Dialogs |
| `public/` | Logo von Ship It! |

Gestaltungsregeln und die Bedeutung der Bausteine stehen in
[CLAUDE.md](CLAUDE.md).

## Troubleshooting

- **Port 3030 belegt**: Slidev nimmt automatisch den nächsten freien Port —
  Konsolenausgabe beachten.
- **PDF-Export schlägt fehl**: `npx playwright install chromium` ausführen,
  falls die Browser-Binaries fehlen.
