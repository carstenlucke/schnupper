# CLAUDE.md — Präsentation

Slidev-Foliensatz der Schnuppervorlesung „Digitalisierung und KI". Liegt auf
oberster Ebene, weil er die Demos des Repositorys einbettet — neue Folien zu
`the-counting-agents/` oder `agent-party/` gehören hierher, nicht in die
Demo-Projekte.

## Design-System

Die Gestaltung folgt dem Claude-Design-System **„THM & StudiumPlus"**. Es liegt
als lokales Theme unter `theme-thm/` (eingebunden mit `theme: ./theme-thm`).
Das Theme ist aus dem Vorlesungsprojekt
`~/Development/thm-lectures/WK_1208-Softwaretechnik/theme-thm/` übernommen und
für StudiumPlus angepasst:

- **Logos**: THM-Logo oben rechts (`ThmLockup.vue`), StudiumPlus-Marke unten
  rechts in der Fußzeile (`SlideFooter.vue`) — wie in den StudiumPlus-Folien
  des Design-Systems. Keine Campus-/Fachbereichs-Lockup.
- **Titel- und Schlussfolie** kommen ohne Foto aus: `cover` zeigt ohne `bild`
  ein kleines neuronales Netz, `end` gibt dem Text die volle Breite.
- **Fragefolien** tragen per Voreinstellung die Rubrik „Frage an euch".
- **Neu**: `<FlowArrow>` und die Klassen `.thm-flow` / `.thm-sample`.
- Übernommen sind die allgemeinen Layouts und Komponenten (auch derzeit
  ungenutzte wie `two-cols`, `split`, `quote`, `<BigStat>`, `<Figure>`), nicht
  die fachspezifischen Diagramme der Softwaretechnik-Vorlesung.

Das Theme ist die einzige Stelle für Gestaltung. In `slides.md` steht Inhalt —
Ausnahme sind kleine, folienspezifische `<style>`-Blöcke. Wiederkehrende Muster
gehören ins Theme.

## Farben

Tokens in `theme-thm/styles/tokens.css`, immer über Variablen, nie als
Hex-Wert.

| Rolle | Farbe | Variable |
|---|---|---|
| Primärakzent, Icons, Balken | THM Grün `#80ba24` | `--thm-green-500` |
| Fließtext, dunkle Flächen | THM Grau `#4a5c66` | `--thm-grey-600` |
| **Interaktion** — Frage an das Publikum | Gelb `#f4aa00` | `--role-ask` |
| Negativbefund, Warnung | Rot `#9c132e` | `--thm-red` |

Gelb heißt immer „hier seid ihr gefragt": `layout: question`,
`<QuestionItem>`, gelbe Icon-Quadrate bei den Produktideen. Nicht dekorativ
einsetzen.

## Bausteine

| Baustein | Wofür |
|---|---|
| `layout: cover` | Titelfolie, dunkle Rasterfläche |
| `layout: agenda` + `aktiv: n` | Abschnittstrenner; `punkte` und `icons` auf allen Trennern gleich halten |
| `layout: default` | Folienkopf (`rubrik`, `titel`, `untertitel`) plus freier Inhalt |
| `layout: question` | Eine Frage, vollflächig Gelb |
| `layout: statement` | Große Aussage; `zitat: false` ohne Kasten |
| `layout: end` | Schlussfolie |
| `<Card>` / `<CardGrid>` | Inhaltskarten mit Icon im grünen Quadrat; `kompakt`, `band`, `tone`, `icon-ton` |
| `<Callout>` | Merksatz-Band am Folienfuß |
| `<QuestionItem>` | Einzelne Frage, für Folien mit mehreren Fragen |
| `.thm-flow` + `<FlowArrow>` | Karten nebeneinander mit Pfeil oder `text="vs."` dazwischen |
| `.thm-sample` (`.sprache`) | Beispiel in einer Karte: Code bzw. Satz in Alltagssprache |
| `.thm-center` | Inhalt vertikal mittig statt gestreckt — für Folien mit wenig Text |
| `class: text-l` | Folienweit größere Schrift, für dünn besetzte Folien |
| `<AgentKreislauf>` | Verstehen → Planen → Handeln → Prüfen mit Rückweg |
| `<AgentAbhaengigkeiten>` | Wer wartet auf wen bei Ship It!; Kanten nach `AGENT_PATHS` in `ship-it/server.py` |

Icons kommen aus Lucide (`@iconify-json/lucide`) und müssen in
`theme-thm/icons.ts` eingetragen sein, bevor sie per Name (`icon="bot"`)
funktionieren. Ein fehlendes Icon meldet `ThmIcon` in der Browser-Konsole.

Diagramme werden als Vue-Komponenten gebaut, nicht als SVG-Datei mit fest
eingetragenen Farben — so stehen sie im CD und bleiben am Beamer scharf.

## Fallstricke

Die Fallstricke aus dem Ursprungsprojekt gelten weiter, vor allem:

- **`<style>` in einer Folie ist scoped.** Selektoren ins Innere einer
  Komponente brauchen `:deep()`.
- **`fill` an `<CardGrid>` streckt die Karten** auf die Resthöhe. Bei wenig
  Text entstehen dadurch leere Flächen — dann lieber `.thm-center`.
- **Nackte URLs werden verlinkt.** Eine URL als Linktext in `<a>` erzeugt
  verschachtelte Links; Linktext ohne `http://` schreiben.
- **Barlow kommt von Google Fonts.** Ohne Netz (auch im sandboxed Export)
  rendern die Folien in der Ersatzschrift.

## Prüfen, bevor etwas als fertig gilt

```bash
npx slidev export --format png --output /tmp/check --dark false
```

Alle Folien als Bild durchsehen: nichts läuft unten über, nichts kollidiert
mit Logo oder Fußzeile.
