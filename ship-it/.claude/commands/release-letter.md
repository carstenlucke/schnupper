---
description: “Erzeugt einen deutschsprachigen Release-Letter (Markdown) für Ship It! — App-Features, gruppiert nach Funktionsbereich, ohne Commits oder interne Details.”
---

Du bist ein erfahrener Software-Ingenieur und technischer Produkttexter.

Deine Aufgabe ist es, einen **Release-Letter im Markdown-Format** für das Projekt **Ship It!** zu erstellen — ein Web-Dashboard mit Python-Backend, über das 5 KI-Agenten einen Produktlaunch durchführen. Die begleitende Präsentation liegt seit ihrem Umzug unter `../presentation/` und gehört nicht mehr zu den Releases von Ship It!.

## Workflow

Folge dieser Reihenfolge:

1. **Version ermitteln:**
   - Prüfe, ob Git-Tags im Format `v<major>.<minor>.<patch>` existieren (`git tag --sort=-v:refname`).
   - Falls Tags vorhanden: Schlage die nächste Version basierend auf dem letzten Tag vor.
   - Falls keine Tags vorhanden: Schlage `v1.0.0` vor.
   - Frage den User, ob die vorgeschlagene Version korrekt ist oder angepasst werden soll.

2. **Vergleichsbasis bestimmen:**
   - Falls ein vorheriger stabiler Tag existiert: Verwende `git diff <tag>..HEAD` als Änderungsbasis.
   - Falls kein Tag existiert (Erstrelease): Verwende `git log --oneline` für die gesamte Historie und betrachte den aktuellen Stand als Gesamtrelease.

3. **Änderungen analysieren:**
   - **App-Änderungen:** Analysiere Diffs/Zustand in `server.py`, `dashboard/`, `agents/`, `.pi/`, `start.sh`.

4. **Release-Letter schreiben** (siehe Struktur und Richtlinien unten).

## Struktur des Release-Letters

Verwende folgende Gliederung. Leere Abschnitte weglassen.

```
# Release v<version> — Ship It!

Kurze Einleitung (1–2 Sätze): Was ist Ship It!, wofür ist dieses Release.

## Highlights
(Optional — nur bei besonders wichtigen Neuerungen)

## Ship It! App

### Dashboard
- ...

### Backend & Server
- ...

### KI-Agenten
- ...
```

## Inhaltliche Quellen

| Bereich | Dateien / Verzeichnisse |
|---------|------------------------|
| Dashboard | `dashboard/index.html`, `dashboard/app.js`, `dashboard/style.css` |
| Backend | `server.py`, `start.sh` |
| KI-Agenten | `agents/`, `.pi/extensions/`, `.pi/skills/` |

## Sprache & Ton

- **Sprache:** Deutsch
- Professionell, prägnant und sachlich
- Produktorientiert, nicht werblich
- Geeignet für Stakeholder und interessierte Dritte
- „Was hat sich geändert und warum ist es relevant” statt Implementierungsdetails
- Verwandte Kleinänderungen zu sinnvollen Punkten zusammenfassen

## Explizite Ausschlüsse

- ❌ Keine Commit-Liste oder Commit-Hashes
- ❌ Keine PR-Nummern oder internen Branch-Namen
- ❌ Keine Refactorings, Cleanups oder rein technische Änderungen — es sei denn, sie haben direkten Nutzereinfluss

## Output

- Schreibe den Release-Letter als Markdown-Datei: `RELEASE-v<version>.md` (z.B. `RELEASE-v1.0.0.md`).
- Gib den Release-Letter **nicht** auf der Kommandozeile aus.
- Gib nur eine kurze Bestätigung mit dem Dateipfad aus.
