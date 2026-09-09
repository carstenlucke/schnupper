# CLAUDE.md

Monorepo mit eigenständigen Demo-Projekten für **Schnuppervorlesungen** bei
StudiumPlus (THM) — Schülerinnen und Schüler der Oberstufe, ca. 90 Minuten,
Thema KI und KI-Agenten.

## Projekte

| Verzeichnis | Was es ist | Start |
|---|---|---|
| `ship-it/` | Web-Dashboard, 5 KI-Agenten führen einen Produktlaunch durch. Python-stdlib-Server + SPA. | `./start.sh` |
| `the-counting-agents/` | Terminal-Demo, 5 Agenten kommunizieren über dateibasierte Event-Logs, je ein benanntes Pane in einem Herdr-Tab. | `./scripts/start.sh` (aus einem Herdr-Pane heraus) |
| `the-counting-agents-pi/` | Dieselbe Demo mit der **pi CLI**, eigenen Werkzeugen (Custom Tools) und einem Modell in der Cloud. | `./scripts/start.sh` (aus einem Herdr-Pane heraus) |

**`ship-it/` hat eine eigene, ausführliche `CLAUDE.md`** — sie ist für alles
maßgeblich, was dieses Projekt betrifft. Diese Datei hier regelt nur, was
projektübergreifend gilt.

`the-counting-agents/` und `the-counting-agents-pi/` zeigen dieselbe Demo mit
zwei verschiedenen Agenten-Laufzeiten. Sie sind **absichtlich getrennte
Projekte** und werden nicht zusammengeführt: Der Vergleich der beiden Fassungen
ist der didaktische Gegenstand. Eine Änderung am einen ist keine Anweisung, das
andere nachzuziehen.

## Struktur

Die Projekte sind vollständig unabhängig: eigene Konfiguration, eigene Skripte,
eigene Doku, keine geteilten Dependencies, kein gemeinsamer Build. Ein Projekt
läuft ohne das andere.

**Nie projektübergreifend refaktorieren.** Keine gemeinsamen Utilities
extrahieren, keine Konfiguration nach oben ziehen. Die Duplikation ist gewollt —
jedes Projekt muss für sich allein erklärbar und startbar sein.

Immer im jeweiligen Projektverzeichnis arbeiten, nicht im Repo-Root.

## Didaktischer Rahmen

Zielgruppe ist ein Publikum ohne Programmiererfahrung. Das prägt den Code:

- **Vorführbarkeit vor Eleganz.** Was im Vortrag sichtbar sein soll (Agenten-
  ausgaben, Zwischenschritte, Wartezeiten), bleibt sichtbar. Nichts wegkapseln,
  was gerade die Demo ausmacht.
- **Minimale Abhängigkeiten.** `ship-it` läuft ohne externe Python-Pakete und
  ohne Build-Pipeline, `the-counting-agents` mit Herdr, Shell und einem lokal
  über LM Studio bereitgestellten Modell. Neue
  Dependencies brauchen einen guten Grund — sie sind Setup-Aufwand im Hörsaal.
- **Absichtliche Einfachheit ist kein Defekt.** Vor dem „Aufräumen“ prüfen, ob
  eine Entscheidung didaktisch gemeint ist; `the-counting-agents/docs/experiment_de.md`
  begründet die dortigen Architekturentscheidungen.

## Gemeinsame Muster

In allen drei Projekten ist ein Agent eine **Markdown-Datei mit
YAML-Frontmatter**: oben Modell und Werkzeuge, darunter die Aufgabe in
normalem Deutsch. Wer einen Agenten anlegt oder ändert, folgt dem Muster des
jeweiligen Projekts. Die Laufzeit unterscheidet sich:

| Projekt | Laufzeit | Agenten liegen in | Modellwahl |
|---|---|---|---|
| `ship-it/` | OpenCode CLI | `.opencode/agents/` | `opencode.json`, je Agent überschreibbar |
| `the-counting-agents/` | OpenCode CLI | `.opencode/agents/` | `opencode.json`, je Agent überschreibbar |
| `the-counting-agents-pi/` | pi CLI | `agents/` | im Frontmatter jedes Agenten |

Bei pi gibt es kein eingebautes Agenten-Konzept: `scripts/run-agent.sh` liest
das Frontmatter und baut daraus den Aufruf (Systemprompt, Werkzeug-Allowlist,
Modell). Eigene Werkzeuge liegen dort als TypeScript unter `.pi/extensions/`.

## Konventionen

- **Sprache: Deutsch.** Code-Kommentare, UI-Texte, Agent-Outputs, Commit-
  Messages und Dokumentation. Ausnahme: die beiden Counting-Agents-Projekte
  pflegen englische Doku mit deutscher Fassung als `*_de.md` — beide Fassungen
  zusammen ändern.
- **Secrets** liegen in projektlokalen `.env`-Dateien, nie im Repo.
  `ship-it/.env.example` und `the-counting-agents-pi/.env.example` sind die
  Vorlagen. Der TensorX-Schlüssel in `the-counting-agents-pi` ist bewusst ein
  eigener, vom global in pi hinterlegten Zugang getrennter Schlüssel.
- **Runtime-Artefakte** sind gitignored und werden nicht versioniert:
  `ship-it/projekte/`, die Logs und Zustandsdateien in
  `the-counting-agents/bus/` und `state/` sowie in
  `the-counting-agents-pi/_bus/` und `_state/` — dort mit Unterstrich, damit
  sie sich von den bearbeiteten Verzeichnissen abheben.

## Git

- **Tags sind namespaced**: `ship-it/v1.0.1`, `the-counting-agents/v0.1.1`.
  Ein Release betrifft immer nur ein Projekt.
- Zu jedem Tag gehört ein Release Letter `RELEASE-vX.Y.Z.md` im jeweiligen
  Projektverzeichnis.
- Die Historie beider Projekte wurde bei der Migration auf die neuen Pfade
  umgeschrieben — `git log -- ship-it/` und `git blame` funktionieren
  über den gesamten Verlauf.

## Nicht anfassen

`ship-it/.github/workflows/release.yml` ist **bewusst inaktiv**. GitHub Actions
liest nur `.github/workflows/` im Repo-Root, und der Tag-Trigger passt nicht
mehr zum Namespace-Schema. Der Workflow bleibt als Referenz liegen — nicht
verschieben, nicht „reparieren“, nur auf ausdrückliche Anweisung reaktivieren.
