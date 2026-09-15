# CLAUDE.md

Monorepo mit eigenständigen Demo-Projekten für **Schnuppervorlesungen** bei
StudiumPlus (THM) — Schülerinnen und Schüler der Oberstufe, ca. 90 Minuten,
Thema KI und KI-Agenten.

## Projekte

| Verzeichnis | Was es ist | Start |
|---|---|---|
| `ship-it/` | Web-Dashboard, 5 KI-Agenten führen einen Produktlaunch durch. Python-stdlib-Server + SPA. | `./start.sh` |
| `the-counting-agents/` | Terminal-Demo, 5 Agenten kommunizieren über dateibasierte Event-Logs, je ein benanntes Pane in einem Herdr-Tab. Läuft mit der pi CLI, eigenen Werkzeugen und einem Modell in der Cloud. | `./scripts/start.sh` |
| `agent-party/` | Web-Dashboard, in dem die Teilnehmenden die Agenten selbst schreiben: Rollenprofile anlegen, Besetzung wählen, Thema geben — die Profile diskutieren reihum. Python-stdlib-Server + SPA. | `./start.sh` |

**Jedes Projekt hat eine eigene `CLAUDE.md`** — sie ist für alles maßgeblich,
was das jeweilige Projekt betrifft. Diese Datei hier regelt nur, was
projektübergreifend gilt. Vor der Arbeit an einem Projekt dessen `CLAUDE.md`
lesen.

## Struktur

Die Projekte sind vollständig unabhängig: eigene Konfiguration, eigene Skripte,
eigene Doku, keine geteilten Dependencies, kein gemeinsamer Build. Ein Projekt
läuft ohne die anderen.

**Nie projektübergreifend refaktorieren.** Keine gemeinsamen Utilities
extrahieren, keine Konfiguration nach oben ziehen. Die Duplikation ist gewollt —
jedes Projekt muss für sich allein erklärbar und startbar sein.

Immer im jeweiligen Projektverzeichnis arbeiten, nicht im Repo-Root.

## Didaktischer Rahmen

Zielgruppe ist ein Publikum ohne Programmiererfahrung. Das prägt den Code:

- **Vorführbarkeit vor Eleganz.** Was im Vortrag sichtbar sein soll (Agenten-
  ausgaben, Zwischenschritte, Wartezeiten), bleibt sichtbar. Nichts wegkapseln,
  was gerade die Demo ausmacht.
- **Minimale Abhängigkeiten.** Neue Dependencies brauchen einen guten Grund —
  sie sind Setup-Aufwand im Hörsaal.
- **Absichtliche Einfachheit ist kein Defekt.** Vor dem „Aufräumen" prüfen, ob
  eine Entscheidung didaktisch gemeint ist; die Projekte begründen ihre
  Architekturentscheidungen in der eigenen Doku.

## Gemeinsames Muster

In allen drei Projekten ist ein Agent eine **Markdown-Datei mit
YAML-Frontmatter**: oben Modell und Werkzeuge, darunter die Aufgabe in normalem
Deutsch. Wer einen Agenten anlegt oder ändert, folgt dem Muster des jeweiligen
Projekts — Ablageort, Frontmatter-Felder und Modellwahl stehen in dessen
`CLAUDE.md`. In `agent-party/` heißt die Datei Rollenprofil und hat keine
Werkzeugzeile — die Profile dort haben bewusst keine Werkzeuge.

## Konventionen

- **Sprache: Deutsch.** Code-Kommentare, UI-Texte, Agent-Outputs, Commit-
  Messages und Dokumentation. Ausnahme: `the-counting-agents/` pflegt
  englische Doku mit deutscher Fassung als `*_de.md` — beide Fassungen
  zusammen ändern.
- **Secrets** liegen in projektlokalen `.env`-Dateien, nie im Repo. Die
  `.env.example` des Projekts ist die Vorlage.
- **Runtime-Artefakte** sind gitignored und werden nicht versioniert. Welche
  das sind, steht in der jeweiligen `.gitignore`.

## Git

- **Tags sind namespaced** nach Projektverzeichnis, z. B. `ship-it/v1.0.1`.
  Ein Release betrifft immer nur ein Projekt.
- Zu jedem Tag gehört ein Release Letter `RELEASE-vX.Y.Z.md` im jeweiligen
  Projektverzeichnis.
- Die Historie von `ship-it/` wurde bei der Migration auf die neuen Pfade
  umgeschrieben — `git log -- ship-it/` und `git blame` funktionieren über den
  gesamten Verlauf.
- Unter `the-counting-agents/` lag früher die OpenCode-Fassung der
  Counting-Agents-Demo; ihr letzter Stand liegt in Commit `4d77661`. Die heutige
  pi-Fassung hieß bis dahin `the-counting-agents-pi-herdr/` und trägt seither
  den frei gewordenen Namen. Folgen:
  - `git log -- the-counting-agents/` mischt beide Fassungen. Den Verlauf der
    pi-Fassung liefert `git log --follow` auf eine einzelne Datei.
  - Die Tags `the-counting-agents/v0.1.0` und `v0.1.1` gehören zur
    OpenCode-Fassung. Releases der pi-Fassung brauchen eine höhere Nummer.
