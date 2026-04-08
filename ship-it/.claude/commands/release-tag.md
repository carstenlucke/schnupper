---
description: "Tags a release version, ensures everything is committed and pushed, and pushes the tag to GitHub to trigger the release workflow."
argument-hint: "[version]"
---

Du bist Release-Engineer für das Projekt **Ship It!**.

Deine Aufgabe ist es, ein **Release zu taggen und zu veröffentlichen**, damit der GitHub-Actions-Release-Workflow ausgelöst wird.

Der User hat folgendes Versions-Argument übergeben (kann leer sein): $ARGUMENTS

## Workflow

Folge diesen Schritten **der Reihe nach**. Überspringe keine Schritte.

### Step 1 — Versionsnummer bestimmen

- Prüfe, ob Git-Tags im Format `v<major>.<minor>.<patch>` existieren (`git tag --sort=-v:refname`).
- **Falls der User eine Version als Argument übergeben hat**: Verwende diese Version.
- **Falls kein Argument übergeben wurde**:
  - Falls Tags vorhanden: Schlage die nächste Version basierend auf dem letzten Tag vor.
  - Falls keine Tags vorhanden: Schlage `v1.0.0` vor.
  - Frage den User, ob die vorgeschlagene Version korrekt ist oder angepasst werden soll.

Speichere die festgelegte Versionsnummer für alle weiteren Schritte.

### Step 2 — Release letter

Ask the user:

> Should I generate a release letter now (via `/release-letter`), or has one already been created?

- If the user wants generation: invoke the `/release-letter` command and wait for it to complete.
- If the user says it already exists: continue.

### Step 3 — Review release letter

After the release letter exists, ask the user:

> Do you want to review or edit the release letter before continuing?

- If **yes**: pause and tell the user to edit and save the file. Wait for the user to confirm they are done.
- If **no**: continue.

### Step 4 — Git status check

Run `git status` and `git log origin/main..HEAD` to determine:

1. Whether there are **uncommitted changes** (staged or unstaged).
2. Whether there are **unpushed commits**.

**If the working tree is clean and up-to-date with the remote**: continue to Step 5.

**If there are uncommitted changes or unpushed commits**:

- Show the user the current status.
- Offer to create a conventional commit message, commit, and push. For example:
  ```
  chore(release): prepare v<version>
  ```
- If the user declines the commit/push, ask whether to **continue anyway** or **abort** the release process.

### Step 5 — Create and push the version tag

Create and push the tag:

```bash
git tag v<version>
git push origin v<version>
```

Where `<version>` is the version resolved in Step 1 (e.g. `1.7.0` produces tag `v1.7.0`).

### Step 6 — Done

Confirm that the tag has been pushed and inform the user that the GitHub Actions release workflow should now be triggered.

## Rules

- Always use the tag format `v<major>.<minor>.<patch>`.
- Never force-push tags.
- If any step fails, stop and report the error clearly. Do not continue.
- Keep console output concise — no unnecessary logs or summaries.