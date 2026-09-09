# CLAUDE.md

Monorepo mit eigenständigen Demo-Projekten für **Schnuppervorlesungen** bei
StudiumPlus (THM) — Schülerinnen und Schüler der Oberstufe, ca. 90 Minuten,
Thema KI und KI-Agenten.

## Projekte

| Verzeichnis | Was es ist | Start |
|---|---|---|
| `ship-it/` | Web-Dashboard, 5 KI-Agenten führen einen Produktlaunch durch. Python-stdlib-Server + SPA. | `./start.sh` |
| `the-counting-agents/` | Terminal-Demo, 5 Agenten kommunizieren über dateibasierte Event-Logs, je ein benanntes Pane in einem Herdr-Tab. | `./scripts/start.sh` (aus einem Herdr-Pane heraus) |

**`ship-it/` hat eine eigene, ausführliche `CLAUDE.md`** — sie ist für alles
maßgeblich, was dieses Projekt betrifft. Diese Datei hier regelt nur, was
projektübergreifend gilt.

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

Beide Projekte nutzen die **OpenCode CLI** als Agenten-Runtime. Agenten sind
Markdown-Dateien mit YAML-Frontmatter unter `.opencode/agents/`, gestartet per
`opencode run --agent <name>`. Wer einen Agenten anlegt oder ändert, folgt dem
Muster des jeweiligen Projekts — die Modellwahl steht in `opencode.json` und
kann pro Agent im Frontmatter überschrieben werden.

## Konventionen

- **Sprache: Deutsch.** Code-Kommentare, UI-Texte, Agent-Outputs, Commit-
  Messages und Dokumentation. Ausnahme: `the-counting-agents` pflegt englische
  Doku mit deutscher Fassung als `*_de.md` — beide Fassungen zusammen ändern.
- **Secrets** liegen in projektlokalen `.env`-Dateien, nie im Repo.
  `ship-it/.env.example` ist die Vorlage.
- **Runtime-Artefakte** sind gitignored und werden nicht versioniert:
  `ship-it/projekte/` sowie die Logs und Zustandsdateien in
  `the-counting-agents/bus/` und `state/`.

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
