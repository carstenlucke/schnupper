---
description: "Entfernt einen Git-Worktree aus .agents/worktrees — zeigt die vorhandenen Worktrees zur Auswahl an und räumt den Eintrag sauber ab."
argument-hint: "[branch-oder-verzeichnis]"
---

Du entfernst einen **Git-Worktree** dieses Repos. In Frage kommen nur Worktrees
unterhalb von `.agents/worktrees/` (bzw. den Symlinks `.claude/worktrees/` und
`.pi/worktrees/`).

Der User hat folgendes Argument übergeben (kann leer sein): $ARGUMENTS

## Schritt 1: Worktrees auflisten

```bash
git rev-parse --git-common-dir      # Elternverzeichnis = Haupt-Repo
git worktree list                   # alle Worktrees mit Pfad, Commit, Branch
pwd                                 # wo stehe ich gerade?
```

Filtere die Liste:

- **Der Haupt-Worktree wird nie angeboten** — er lässt sich nicht entfernen.
- Nur Einträge unterhalb von `.agents/worktrees/` sind Kandidaten. Liegt ein
  Worktree woanders, zeige ihn an, weise aber darauf hin, dass er nicht von
  diesem Command verwaltet wird.
- Einträge, die als `prunable` markiert sind (Verzeichnis von Hand gelöscht),
  gesondert kennzeichnen — die brauchen `git worktree prune`, kein `remove`.

Gibt es keine Kandidaten, sag das und beende den Command.

## Schritt 2: Auswahl treffen

**Argument übergeben:** Ordne es einem Worktree zu — es darf der Branch-Name,
der Verzeichnisname oder ein Pfad sein. Passt nichts oder passt mehr als einer,
zeige die Liste und frage nach.

**Argument leer:** Zeige die Kandidaten zur Auswahl an, mit Branch, Verzeichnis
und Zustand (siehe Schritt 3), und **warte auf die Wahl des Users**. Bei bis zu
vier Kandidaten biete sie direkt als Auswahloptionen an, sonst als nummerierte
Liste.

## Schritt 3: Zustand prüfen, bevor du fragst

Ermittle für jeden Kandidaten, ob dort **ungesicherte Arbeit** liegt:

```bash
git -C <worktree-pfad> status --porcelain          # uncommitted changes
git log <branch> --not --remotes --oneline         # nicht gepushte Commits
```

Nimm das Ergebnis in die Anzeige auf (`sauber` / `N Änderungen` / `M Commits
nicht gepusht`), damit die Auswahl informiert erfolgt.

Brich ab, wenn du dich **selbst im zu löschenden Worktree befindest** — nenne
dem User den Pfad des Haupt-Repos, aus dem heraus es funktioniert.

## Schritt 4: Entfernen

```bash
git worktree remove <worktree-pfad>
```

Verweigert Git das wegen ungesicherter Arbeit, **nutze nicht einfach `--force`**.
Zeige stattdessen, was verloren ginge (`git -C <pfad> status --short`), und lass
den User entscheiden. Erst auf ausdrückliche Bestätigung hin:

```bash
git worktree remove --force <worktree-pfad>
```

War der Eintrag verwaist (`prunable`), stattdessen:

```bash
git worktree prune
```

## Schritt 5: Zusammenfassung ausgeben

```
Worktree entfernt.
- Verzeichnis: <absoluter Pfad>
- Branch: <branch> — bleibt bestehen

Branch ebenfalls löschen:  git branch -d <branch>
Verbleibende Worktrees:    <Anzahl>
```

Der Branch bleibt stehen. **Lösche ihn nicht selbst** — nenne nur den Befehl.
