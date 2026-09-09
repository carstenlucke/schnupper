# Eigene Werkzeuge für pi

Diese Demo bringt ihre eigenen Werkzeuge mit. Was das ist, wie es gebaut wird
und woran man beim Erweitern denken muss.

> English version: [pi-custom-tools.md](pi-custom-tools.md)

## Warum überhaupt eigene Werkzeuge?

Ein Sprachmodell kann von sich aus nichts tun. Es kann Text erzeugen — und es
kann darum bitten, ein Werkzeug zu benutzen. Welche Werkzeuge das sind, legt
der Betreiber fest.

pi bringt allgemeine Werkzeuge mit: `bash`, `read`, `write`, `edit`, `grep`,
`find`, `ls`. Damit lässt sich alles machen, aber nichts gut zeigen. Wenn der
Counter-Agent eine Zahl veröffentlicht, sieht das Publikum:

```
bash echo '{"type":"number","seq":42,"value":42,"timestamp":"2026-09-09T21:15:03.412Z"}' >> _bus/numbers.log
```

Mit einem eigenen Werkzeug sieht es so aus:

```
bus_publish {"value": 42}
```

Der zweite Unterschied ist der wichtigere: **Was ein Werkzeug erledigt, muss
der Prompt nicht mehr erklären.** In der OpenCode-Fassung dieses Projekts stand
in jedem Agent-Prompt eine halbe Seite Fehlerbehandlung — leere Dateien nicht
mit dem Read-Tool öffnen, Zeitstempel ohne Millisekunden erzeugen, keine
absoluten Pfade schreiben, `write` nicht für Log-Dateien verwenden. Das war
keine Aufgabenbeschreibung, sondern eine Bedienungsanleitung für Werkzeuge, die
für etwas anderes gedacht sind.

Jetzt steht diese Sorgfalt einmal im Code, und der Prompt beschreibt die
Aufgabe.

## Wo die Werkzeuge liegen

pi lädt Extensions aus mehreren Orten:

| Ort | Geltung |
|---|---|
| `~/.pi/agent/extensions/*.ts` | überall |
| `.pi/extensions/*.ts` | nur in diesem Projekt |

Diese Demo nutzt den projektlokalen Ort:

```
.pi/extensions/
├── counting-tools.ts       die sechs Werkzeuge
└── tensorx-schnupper.ts    ein eigener Modell-Zugang (optional)
```

TypeScript wird direkt geladen, ohne Übersetzungsschritt und ohne
`node_modules` im Projekt — pi bringt den Lader mit.

**Projektlokale Extensions laufen nur, wenn dem Projekt vertraut wird.** Das
ist eine Sicherheitsschranke: Eine Extension kann beliebigen Code ausführen,
also fragt pi beim ersten interaktiven Start nach. Im nicht-interaktiven
Betrieb (`-p`), in dem die Agenten laufen, wird nicht gefragt — deshalb geben
die Skripte `-a` mit, was dem Projekt für diesen einen Aufruf vertraut.

## Wie ein Werkzeug aussieht

Der Kern von [`counting-tools.ts`](../.pi/extensions/counting-tools.ts),
verkürzt:

```typescript
import { Type } from "typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "bus_publish",
    label: "Bus · veröffentlichen",
    description:
      "Stellt eine Zahl als Ereignis in den Event-Bus (_bus/numbers.log). " +
      "Die fortlaufende Sequenznummer und der Zeitstempel werden automatisch vergeben.",
    parameters: Type.Object({
      value: Type.Number({ description: "Die zu veröffentlichende Zahl" }),
    }),
    async execute(_toolCallId, params) {
      // ... Sequenznummer bestimmen, Zeile anhängen ...
      return { content: [{ type: "text", text: JSON.stringify(result) }], details: result };
    },
  });
}
```

Vier Dinge sind wichtig:

- **`name`** ist das, was das Modell aufruft, und das, was im Pane erscheint.
  Kurz und sprechend.
- **`description`** ist kein Kommentar für Menschen, sondern die
  Gebrauchsanweisung für das Modell. Sie entscheidet, ob das Werkzeug richtig
  benutzt wird. Was ein Werkzeug automatisch erledigt, gehört hier hinein —
  sonst versucht das Modell, es selbst zu tun.
- **`parameters`** beschreibt die Eingaben als Schema. pi prüft sie, bevor
  `execute` läuft; falsche Typen erreichen den Code nie.
- **`execute`** gibt Text zurück, den das Modell zu sehen bekommt. Bei uns
  kompaktes JSON: wenig Tokens, eindeutig zu lesen.

## Die sechs Werkzeuge dieser Demo

| Werkzeug | Was es tut |
|---|---|
| `bus_publish` | Hängt eine Zahl an `_bus/numbers.log` an; vergibt Sequenznummer und Zeitstempel |
| `bus_read` | Liefert die Ereignisse mit `seq > since`, dazu `latest_seq` und wie viele noch ausstehen |
| `control_read` | Sagt einem Agenten, was für ihn gilt: `status`, `verbose`, `reset_requested` |
| `control_send` | Schreibt einen Steuerbefehl nach `_bus/control.log` |
| `state_read` | Liest `_state/<agent>.json`, mit `all` alle vier auf einmal |
| `state_write` | Schreibt den Zustand fort; setzt `count` und `updated_at` selbst |

Drei Entwurfsentscheidungen lohnen einen Blick:

**Die Werkzeuge rechnen nicht.** Ob eine Zahl gerade oder prim ist, entscheidet
das Modell. Ein `is_prime`-Werkzeug wäre zuverlässiger — und würde genau das
wegnehmen, was in der Vorlesung zu sehen sein soll. Die Werkzeuge machen die
Buchhaltung, das Modell die Arbeit.

**`control_read` liefert kein Rohmaterial, sondern eine Antwort.** Es könnte
die Zeilen aus `control.log` zurückgeben und den Agenten auswerten lassen: Was
gilt, wenn erst „pause an alle" und später „resume an odd" kam? Diese
Auswertung ist immer dieselbe und immer fehleranfällig, also steht sie im Code.
Der Agent fragt „was gilt für mich?" und bekommt `{"status":"running",...}`.

**`state_write` ändert nur, was übergeben wird.** Ein Agent, der beim Schreiben
seine gesammelten Zahlen vergisst, verliert sie nicht. Das ist bewusst
nachsichtig: Ein Modell, das im dritten Durchlauf ein Feld weglässt, soll die
Demo nicht kippen.

## Wer welches Werkzeug bekommt

Registriert heißt nicht verfügbar. Welche Werkzeuge ein Agent bekommt, steht in
seinem Frontmatter und landet als `--tools` im pi-Aufruf:

```yaml
tools: bus_read,control_read,state_read,state_write
```

Dazu kommt `-nbt` (`--no-builtin-tools`): kein `bash`, kein `read`, kein
`write`. Die Sammler-Agenten können nichts in den Bus schreiben — nicht, weil
der Prompt es verbietet, sondern weil ihnen das Werkzeug fehlt.

Das ist der Punkt, an dem sich in der Vorlesung gut anhalten lässt: Ein Agent
ist nicht das Modell. Ein Agent ist ein Modell **plus** eine Aufgabe **plus**
eine Menge von Werkzeugen — und die letzte Zutat bestimmt, was überhaupt
passieren kann.

## Ein Werkzeug ergänzen

1. In `counting-tools.ts` ein weiteres `pi.registerTool({...})` anlegen.
2. In `scripts/test-tools.mjs` eine Prüfung dafür ergänzen und
   `node scripts/test-tools.mjs` laufen lassen — das braucht weder Modell noch
   Netz und kostet nichts.
3. Den Werkzeugnamen im Frontmatter der Agenten eintragen, die es benutzen
   dürfen.
4. Im Prompt des Agenten beschreiben, **wann** er es benutzen soll. Das *Wie*
   steht in der `description` des Werkzeugs.

Läuft ein Agent in eine Endlosschleife oder ruft er dasselbe Werkzeug immer
wieder auf, liegt es fast immer an der `description` — und fast nie am Prompt.

## Weiterlesen

[`Trajectory_de.md`](Trajectory_de.md) zeigt, wie diese Werkzeuge im Durchlauf
tatsächlich aufgerufen werden — mit einer aufgezeichneten Trajektorie.

Die pi-Dokumentation liegt beim installierten Paket und ist ausführlich:

```bash
open "$(dirname "$(dirname "$(readlink -f "$(which pi)")")")/../docs"
```

Einschlägig sind `extensions.md` (Werkzeuge, Ereignisse, Kommandos),
`custom-provider.md` (eigene Modell-Zugänge) und `usage.md` (die Flags, die die
Startskripte verwenden).
