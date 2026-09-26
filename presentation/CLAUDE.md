# CLAUDE.md — Präsentation

Slidev-Foliensatz der Schnuppervorlesung „Vom Chatbot zum KI-Agenten". Liegt auf
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
- **Zusatzfolien** für Fragen, die vielleicht kommen, liegen außerhalb des
  Verlaufs: Frontmatter `zusatz: <routeAlias der Herkunftsfolie>`, dazu ein
  eigener `routeAlias`. Beim Blättern überspringt der Guard sie; erreichbar
  sind sie per `<Abstecher>` auf der Herkunftsfolie. Von der Zusatzfolie
  führt ← zurück zur Herkunftsfolie, → zu deren Nachfolgerin. Im Block
  stehen sie hinter der Abschlussfolie (Agent Party: „KI gegen KI?“).

Eine neue Demo braucht: einen Block in `demos/` mit `routeAlias: demo-<id>`
auf der ersten Folie und einer Abschlussfolie, einen `src:`-Eintrag mit
`demo: <id>` und eine Karte in `DemoUebersicht.vue`.

Daraus folgen Regeln:

- **Der gemeinsame Strang nennt keine einzelne Demo.** Er muss stimmen, egal
  welche Demo gezeigt wurde — auch bei zweien. Was nur zu einer Demo passt, gehört in
  deren Datei.
- **Jeder Demo-Block ist gleich gebaut:** Vorstellung, Aufbau, Mitmachfrage,
  „Los geht's!" mit Adresse, Bewertung, Abschlussfolie. Im Aufbau darf eine
  Motivationsfolie mit einem Fundstück stehen (Agent Party: ein
  LinkedIn-Beitrag, direkt nach der Vorstellung). Rubriken `<Demo>`,
  `<Demo> · Live-Demo`, `<Demo> · Bewertung`.
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

- **Logos**: THM-Logo und StudiumPlus-Marke stehen auf jeder Folie
  nebeneinander oben rechts, getrennt durch einen feinen Strich
  (`ThmLockup.vue`); auf Titel- und Schlussfolie oben links. Abweichend vom
  Design-System trägt die Fußzeile keine Marke — allein unten rechts wirkte
  sie verloren. Keine Campus-/Fachbereichs-Lockup.
- **Titelfolie** mit Foto wie im Ursprungsprojekt: `bild:
  /studiumplus-campus.jpg` (StudiumPlus-Gebäude mit Stele). Ohne `bild` zeigt
  `cover` stattdessen ein kleines neuronales Netz. Die Schlussfolie (`end`)
  kommt ohne Foto aus und gibt dem Text die volle Breite.
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
| `layout: question` | Eine Frage, vollflächig Gelb; `class: text-xl` für kurze Fragen |
| `layout: statement` | Große Aussage; `zitat: false` ohne Kasten |
| `layout: end` | Schlussfolie |
| `<Card>` / `<CardGrid>` | Inhaltskarten mit Icon im grünen Quadrat; `kompakt`, `band`, `tone`, `icon-ton` |
| `<Callout>` | Merksatz-Band am Folienfuß |
| `<QuestionItem>` | Einzelne Frage, für Folien mit mehreren Fragen |
| `.thm-flow` + `<FlowArrow>` | Karten nebeneinander mit Pfeil oder `text="vs."` dazwischen |
| `.thm-sample` (`.sprache`) | Beispiel in einer Karte: Code bzw. Satz in Alltagssprache |
| `.thm-center` | Inhalt vertikal mittig statt gestreckt — für Folien mit wenig Text |
| `class: text-l` | Folienweit größere Schrift, für dünn besetzte Folien; zieht auch `.thm-note` und `<QuestionItem>` mit |
| `class: text-xl` | Noch größer, für Folien mit wenig Text, die die Fläche füllen sollen (Einstieg); zieht auch `.thm-lead`, `.thm-note`, `<QuestionItem>` und den Text von `layout: statement` mit `zitat: false` mit |
| `.thm-center.thm-gruppe` | Einleitung, Karten und `<Callout>` als ein Block in der Folienmitte, statt den Merksatz an den Folienfuß zu schieben |
| `<AgentKreislauf>` | Verstehen → Planen → Handeln → Prüfen mit Rückweg |
| `<NaechstesWort>` | Wie ein LLM schreibt: angefangener Satz, darunter die möglichen nächsten Wörter mit (ausgedachter) Wahrscheinlichkeit |
| `<CopyPasteSchleife>` | Alltag mit Chatbots: Chatfenster, ihr, Dokument; Texte wandern per Copy & Paste hin und her. Auf Klick 1 (fest in der Komponente) gleitet das Bild nach rechts und links erscheint das Modell hinter der App; weitere Klicks auf der Folie ab 2 zählen |
| `<AgentAnatomie>` | KI-Agent = Modell + Harness: Gleichung, darunter das Modell im Rahmen des Harness — links die Werkzeuge, rechts die Steuerung (Schleife, Anweisungen, Gedächtnis, Leitplanken) |
| `<AgentAbhaengigkeiten>` | Wer wartet auf wen bei Ship It!; Kanten nach `AGENT_PATHS` in `ship-it/server.py` |
| `<DemoUebersicht>` | Karten der Übersichtsfolie, springen auf `demo-<id>` |
| `<DemoEnde>` | Abschlussfolie eines Demo-Blocks: zur Übersicht oder weiter |
| `<Abstecher>` | Kleiner Knopf auf eine Zusatzfolie (`to` = deren routeAlias); mit `zurueck` der Rückweg auf der Zusatzfolie |
| `<WerkzeugMatrix>` | Wer darf was bei den Counting Agents; Zeilen nach den `tools:`-Zeilen in `the-counting-agents/agents/*.md`; der Merksatz zu „Alles andere“ erscheint nur als Tooltip bei Hover |
| `<AgentRunde>` | Agent Party als Bild: vier Agenten im Kreis um ein Thema, reihum verbunden, je eine Sprechblase; Rollen nach `agent-party/profile/` |
| `<SocialPost>` | Beitrag oder (`kommentar`) Kommentar aus einem beruflichen Netzwerk als Karte; Profilbild per `foto`, sonst Initialen; kein Logo, Quelle als `.thm-note` darunter |
| `<CodeKlappe>` | Knopf unter dem SQL-Beispiel auf „Vom Code zur Sprache“; öffnet 25 Zeilen TypeScript (Primzahlen sammeln) neben zwei Sätzen an einen Agenten. Satz nach `the-counting-agents/agents/prime.md`, die Demo selbst bleibt ungenannt |
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
