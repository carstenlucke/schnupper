# Opencode als Custom-Agent-Plattform

Dieses Dokument beschreibt, wie [opencode](https://github.com/opencode-ai/opencode) als Laufzeitumgebung für eigene, spezialisierte KI-Agenten genutzt werden kann — und warum sich das lohnt.

## Was ist opencode?

Opencode ist ein Open-Source-KI-Coding-Agent für das Terminal. Es bietet eine interaktive TUI (Text User Interface), kann aber auch nicht-interaktiv über die CLI genutzt werden. Genau diese nicht-interaktive Nutzung macht opencode zu einer idealen Plattform für autonome Agenten.

Offizielle Dokumentation: [opencode.ai/docs](https://opencode.ai/docs/)

## Warum opencode für Custom Agents?

### Kein eigener Code nötig

Der entscheidende Vorteil: Man braucht **keinen Anwendungscode** zu schreiben. Agenten werden rein deklarativ in Markdown definiert — Systemprompt, erlaubte Tools, Modellauswahl. Opencode übernimmt die gesamte Ausführung: Modellaufrufe, Tool-Nutzung, Dateizugriff, Shell-Befehle.

### LLM-Anbindung inklusive

Opencode unterstützt verschiedene LLM-Provider (Anthropic, OpenAI, GitHub Copilot, u.a.) und abstrahiert die Anbindung vollständig. Ein Modellwechsel ist eine einzige Zeile in der Konfiguration.

### Eingebauter Tool-Zugriff

Jeder Agent hat Zugriff auf mächtige, eingebaute Tools:
- **Bash** — Shell-Befehle ausführen
- **Read** — Dateien lesen
- **Write** — Dateien schreiben
- **Edit** — Dateien bearbeiten
- **Glob/Grep** — Dateien suchen

Diese Tools können pro Agent aktiviert oder deaktiviert werden, um den Handlungsspielraum gezielt einzuschränken.

## Custom Agents definieren

Es gibt zwei Wege, eigene Agenten zu definieren:

### 1. Markdown-Dateien (empfohlen)

Agenten werden als Markdown-Dateien mit YAML-Frontmatter abgelegt:

- **Projektspezifisch:** `.opencode/agents/` im Projektverzeichnis
- **Global:** `~/.config/opencode/agents/`

Offizielle Dokumentation: [opencode.ai/docs/agents](https://opencode.ai/docs/agents/)

#### Beispiel aus diesem Projekt

So ist der Counter-Agent in `.opencode/agents/counter.md` definiert:

```markdown
---
description: Counter agent that generates sequential numbers into the event bus
model: github-copilot/gpt-4o
tools:
  bash: true
  read: true
  write: true
---

# Counter Agent

Du bist der **Counter-Agent** in einem Multi-Agent-System.
Deine einzige Aufgabe ist es, fortlaufende Zahlen zu erzeugen
und als Events in den Event-Bus zu schreiben.

## Dein Verhalten
1. State lesen: Lies `state/counter.json` ...
2. Control-Events prüfen: Lies `bus/control.log` ...
3. Wenn Status "running": Erhöhe `last_value` um 1 ...
...
```

Das Frontmatter definiert die Metadaten, der Markdown-Body ist der Systemprompt.

### 2. JSON-Konfiguration in opencode.json

Alternativ können Agenten direkt in der `opencode.json` definiert werden:

```json
{
  "agent": {
    "counter": {
      "description": "Counter agent that generates sequential numbers",
      "model": "github-copilot/gpt-4o",
      "prompt": "Du bist der Counter-Agent ...",
      "tools": {
        "bash": true,
        "read": true,
        "write": true
      }
    }
  }
}
```

Offizielle Dokumentation: [opencode.ai/docs/config](https://opencode.ai/docs/config/)

## Konfigurationsoptionen

Jeder Agent unterstützt diese Optionen im Frontmatter bzw. in der JSON-Konfiguration:

| Option | Beschreibung |
|--------|-------------|
| `description` | Kurzbeschreibung des Agenten (Pflicht) |
| `model` | Modell-Override (z.B. `anthropic/claude-sonnet-4-5`) |
| `mode` | `primary`, `subagent` oder `all` |
| `prompt` | Systemprompt (Markdown-Body oder Textreferenz) |
| `temperature` | Kreativität der Antworten (0.0–1.0) |
| `tools` | Tool-Zugriff aktivieren/deaktivieren |
| `permission` | Granulare Berechtigungen (`ask`, `allow`, `deny`) |
| `steps` | Maximale Iterationen pro Aufruf |

Offizielle Dokumentation: [opencode.ai/docs/agents](https://opencode.ai/docs/agents/)

## Agenten ausführen

### Nicht-interaktiv (für Automatisierung)

Der Befehl `opencode run` führt einen Agenten nicht-interaktiv aus — ideal für Schleifen und Skripte:

```bash
opencode run --agent counter "Execute your next step."
```

Offizielle Dokumentation: [opencode.ai/docs/cli](https://opencode.ai/docs/cli/)

### Wichtige Flags

| Flag | Beschreibung |
|------|-------------|
| `--agent <name>` | Wählt den auszuführenden Agenten |
| `--model <provider/model>` | Überschreibt das Modell |
| `--file <path>` | Hängt eine Datei an die Nachricht an |
| `--session <id>` | Setzt eine bestehende Session fort |
| `--format <json\|text>` | Ausgabeformat |

### Persistenter Server (reduzierte Latenz)

Für häufige Aufrufe kann ein persistenter Server gestartet werden, der die Initialisierung nur einmal durchführt:

```bash
# Server starten
opencode serve

# Agenten über den Server ausführen
opencode run --attach http://localhost:4096 --agent counter "Execute your next step."
```

Dies vermeidet den Cold-Start bei jedem Aufruf — besonders nützlich bei schnellen Agentenzyklen.

Offizielle Dokumentation: [opencode.ai/docs/cli](https://opencode.ai/docs/cli/)

## Berechtigungen und Sicherheit

Opencode bietet granulare Kontrolle darüber, welche Tools ein Agent nutzen darf:

```json
{
  "agent": {
    "reviewer": {
      "permission": {
        "edit": "deny",
        "write": "deny",
        "bash": {
          "git *": "allow",
          "rm *": "deny"
        }
      }
    }
  }
}
```

So kann ein Review-Agent Code lesen, aber nicht verändern — ein Sicherheitsprinzip, das bei autonomen Agenten besonders wichtig ist.

## Praxisbeispiel: Dieses Projekt

*The Counting Agents* nutzt opencode als reine Agenten-Laufzeitumgebung. Fünf Agenten sind als Markdown-Dateien in `.opencode/agents/` definiert und werden über Shell-Skripte in Schleifen ausgeführt:

```bash
# Aus scripts/run-agent.sh (vereinfacht)
while true; do
    opencode run --agent "$AGENT_NAME" "Execute your next step."
    sleep "$INTERVAL"
done
```

Die Agenten:
- **Lesen und schreiben Dateien** (Event-Bus, State)
- **Führen Shell-Befehle aus** (Append an Log-Dateien)
- **Treffen autonome Entscheidungen** (auf Basis ihres Systemprompts)
- **Koordinieren sich untereinander** (über das Dateisystem)

Das Ergebnis: Ein vollständiges Multi-Agenten-System ohne eine einzige Zeile Anwendungscode.

## Ideen für eigene Custom Agents

Die Mechanik eignet sich für viele Szenarien jenseits von Zählagenten:

- **Code-Reviewer** — Überwacht ein Verzeichnis und gibt Feedback zu geänderten Dateien
- **Testläufer** — Führt Tests aus und dokumentiert Ergebnisse
- **Doku-Generator** — Liest Quellcode und aktualisiert Dokumentation
- **Log-Analyst** — Überwacht Log-Dateien und erstellt Zusammenfassungen
- **Deployment-Agent** — Führt Deployments nach definierten Regeln durch

Der Schlüssel liegt darin, dem Agenten über den Systemprompt eine klare Rolle, definierte Dateipfade und ein konsistentes Verhaltensmuster zu geben.

## Weiterführende Links

- [Opencode — Offizielle Dokumentation](https://opencode.ai/docs/)
- [Opencode — Agents](https://opencode.ai/docs/agents/)
- [Opencode — CLI-Referenz](https://opencode.ai/docs/cli/)
- [Opencode — Konfiguration](https://opencode.ai/docs/config/)
- [Opencode — Rules (Custom Instructions)](https://opencode.ai/docs/rules/)
- [Opencode — GitHub Repository](https://github.com/opencode-ai/opencode)
