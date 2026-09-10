---
description: "Legt einen Git-Worktree unter .agents/worktrees an — fragt nach dem Branch-Namen, leitet daraus das Verzeichnis ab und checkt den Branch dort aus."
argument-hint: "[branch]"
---

Du legst einen **Git-Worktree** für dieses Repo an. Ablageort ist immer
`.agents/worktrees/` im Haupt-Repo (gitignored, per Symlink auch unter
`.claude/worktrees/` und `.pi/worktrees/` erreichbar).

Der User hat folgenden Branch-Namen übergeben (kann leer sein): $ARGUMENTS

## Schritt 1: Branch-Namen klären

Ist das Argument leer, **frage den User nach dem Branch-Namen** und warte auf die
Antwort. Lege nichts auf Verdacht an.

Ist ein Name da, verwende ihn unverändert als Branch-Namen.

## Schritt 2: Kontext ermitteln

```bash
git rev-parse --git-common-dir      # gemeinsames .git-Verzeichnis
git worktree list                   # bestehende Worktrees
git branch --list <branch>          # existiert der Branch schon?
git branch --show-current           # aktueller Branch (Basis für neue Branches)
```

Das **Haupt-Repo** ist das Elternverzeichnis von `--git-common-dir`. Nutze das,
nicht `--show-toplevel` — der Command kann aus einem Worktree heraus aufgerufen
werden.

## Schritt 3: Verzeichnisnamen ableiten

Aus dem Branch-Namen wird der Verzeichnisname, indem `/` durch `-` ersetzt wird:

| Branch | Verzeichnis |
|---|---|
| `experiment` | `.agents/worktrees/experiment` |
| `feature/tempo-regler` | `.agents/worktrees/feature-tempo-regler` |

## Schritt 4: Vorbedingungen prüfen

Brich mit einer klaren Meldung ab, wenn:

- das Zielverzeichnis schon existiert,
- der Branch bereits in einem anderen Worktree ausgecheckt ist
  (`git worktree list` zeigt ihn),
- das Arbeitsverzeichnis ungeeignet ist (kein Git-Repo).

Bei einem belegten Branch: nenne den Pfad des bestehenden Worktrees, statt einen
zweiten anzulegen.

## Schritt 5: Worktree anlegen

**Branch existiert noch nicht** — neu anlegen, ausgehend vom aktuellen HEAD:

```bash
git worktree add <haupt-repo>/.agents/worktrees/<verzeichnis> -b <branch>
```

**Branch existiert bereits** — vorhandenen Branch auschecken:

```bash
git worktree add <haupt-repo>/.agents/worktrees/<verzeichnis> <branch>
```

## Schritt 6: Zusammenfassung ausgeben

```
Worktree angelegt.
- Branch: <branch> (neu | bestehend)
- Pfad: <absoluter Pfad>
- Basis: <Branch/Commit, von dem abgezweigt wurde>   (nur bei neuem Branch)

Reingehen:  cd <pfad>
Aufräumen:  git worktree remove <pfad>   (löscht den Branch nicht)
```

Wechsle **nicht** selbst in den Worktree und beginne dort keine Arbeit — der
Command legt ihn nur an.
