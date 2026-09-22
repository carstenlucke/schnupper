# CLAUDE.md — Präsentation

Slidev-Foliensatz der Schnuppervorlesung „Digitalisierung und KI". Liegt auf
oberster Ebene, weil er die Demos des Repositorys einbettet — Folien zu einer
Demo gehören hierher, nicht in das Demo-Projekt.

## Aufbau: gemeinsamer Strang mit Abzweigen

`slides.md` ist der gemeinsame Handlungsstrang: Einstieg, „Vom Chatbot zum
KI-Agenten", die Übersicht der Demos, danach „Was nehmen wir mit?". Die
Demo-Blöcke liegen in `demos/` und werden per `src:` eingebunden; das `demo:`
am Eintrag vererbt sich auf alle Folien des Blocks.

Die Demos sind Abzweige von der Übersicht, keine Folge:

- `<DemoUebersicht>` auf der Übersichtsfolie (routeAlias `demos`) springt per
  Link auf die erste Folie einer Demo (routeAlias `demo-<id>`).
- `slide-bottom.vue` zeigt auf jeder Folie mit `demo:` den Link „Demos"
  zurück zur Übersicht, mittig in der Fußzeile.
- Jeder Block endet mit einer Folie mit `<DemoEnde>`: zur Übersicht oder
  weiter zu „Was nehmen wir mit?" (routeAlias `nach-demos`).
- `setup/main.ts` hängt einen Router-Guard ein, der nur beim Blättern um eine
  Folie greift: vorwärts aus einer Demo heraus nach `nach-demos`, rückwärts
  in eine andere Demo hinein zur Übersicht. Links und `G` bleiben
  unberührt; Übersicht und Export zeigen alles.

Eine neue Demo braucht: einen Block in `demos/` mit `routeAlias: demo-<id>`
auf der ersten Folie und einer Abschlussfolie, einen `src:`-Eintrag mit
`demo: <id>` und eine Karte in `DemoUebersicht.vue`.

Daraus folgen Regeln:

- **Der gemeinsame Strang nennt keine einzelne Demo.** Er muss stimmen, egal
  welche Demo gezeigt wurde — auch bei zweien. Was nur zu einer Demo passt, gehört in
  deren Datei.
- **Jeder Demo-Block ist gleich gebaut:** Vorstellung, Aufbau, Mitmachfrage,
  „Los geht's!" mit Adresse, Bewertung, Abschlussfolie. Rubriken `<Demo>`, `<Demo> · Live-Demo`,
  `<Demo> · Bewertung`.
- **Reflexion ist zweigeteilt.** Die Bewertung („was haben wir gesehen?") ist
  demo-spezifisch und steht im Block. Der Reality Check ist gemeinsam; neue
  Demos tragen ihre Beispiele in dessen Sprecher-Notizen ein, nicht als
  eigene Folie.
- **Blöcke sind unabhängig voneinander.** Kein Block verweist auf einen
  anderen — welche gezeigt werden und in welcher Reihenfolge, wechselt.

Der Export enthält immer alle Demos. Die Navigation lässt sich nur im
laufenden Dev-Server prüfen: von der Übersicht in jede Demo springen, bis zum
Ende und über das Ende hinaus blättern, rückwärts aus der Demo heraus, den
Link „Demos" anklicken.

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
| `<DemoUebersicht>` | Karten der Übersichtsfolie, springen auf `demo-<id>` |
| `<DemoEnde>` | Abschlussfolie eines Demo-Blocks: zur Übersicht oder weiter |
| `<WerkzeugMatrix>` | Wer darf was bei den Counting Agents; Zeilen nach den `tools:`-Zeilen in `the-counting-agents/agents/*.md` |
| `<CountingBus>` | Nachrichtenwege der Counting Agents: Zähler → Zahlen-Datei → Sammler, Steuerung → Befehls-Datei |

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
