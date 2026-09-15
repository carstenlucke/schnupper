# Agent Party

Live-Demo für eine Schnuppervorlesung bei StudiumPlus (90 Min, Oberstufe). Die
Teilnehmenden bauen die KI-Agenten **selbst**: Sie schreiben Rollenprofile,
wählen daraus eine Besetzung und geben ihr ein Thema. Danach diskutieren die
gewählten Profile reihum, live im Browser.

Der Punkt der Demo: Ein „KI-Agent" ist nichts Magisches. Er ist eine
Rollenbeschreibung in normalem Deutsch plus ein Sprachmodell — und wer die
Beschreibung ändert, sieht das Verhalten sofort kippen.

## Quickstart

```bash
./start.sh
```

Öffnet das Dashboard unter [http://localhost:8100](http://localhost:8100). Fünf
Profile sind mitgeliefert, es lässt sich also sofort losdiskutieren.

### Voraussetzungen

- Python 3 (keine externen Dependencies)
- [pi CLI](https://pi.dev) installiert
  (`npm install -g @earendil-works/pi-coding-agent`) und einmal per `/login`
  angemeldet
- Ein Zugang zu einem Sprachmodell. Voreingestellt ist
  `openai-codex/gpt-5.6-luna` über ein ChatGPT-Abo; im Dashboard lässt sich
  mitten in der Demo auf TensorX oder ein lokales Modell in LM Studio umstellen

Kein API-Schlüssel nötig — die Anmeldung erledigt pi.

## Ablauf in der Vorlesung

```
1. Profile ansehen            → „Das hier ist der ganze Agent."
2. Rolle in einem Satz        → [Ausarbeiten lassen] → das Modell schreibt
   beschreiben                  das Profil, live sichtbar
3. Entwurf anpassen           → ein Wort ändern, speichern
4. Besetzung wählen           → drei Profile, Reihenfolge festlegen
5. Thema + Einstiegsfrage     → „Sollen Schulen KI verbieten?"
6. [Party starten]            → die Runde diskutiert, Beitrag für Beitrag
7. Denkbereich aufklappen     → „Was das Modell gedacht hat"
8. Zwischenruf einwerfen      → „Bleibt konkret: Nennt Zahlen." — der nächste
                                Beitrag geht darauf ein
9. [Weitere Runde]            → die Runden sind durch, es geht trotzdem weiter
10. [Fazit erstellen]         → die Gesprächsleitung fasst zusammen
11. Ein Profil umschreiben    → dieselbe Party neu starten, Unterschied zeigen
```

Schritt 11 ist der Höhepunkt: dieselbe Frage, dieselbe Besetzung, ein geänderter
Satz im Profil — und die Diskussion dreht sich.

Schritt 8 zeigt nebenbei, warum das Ganze funktioniert: Der Zwischenruf ist
nichts weiter als eine Zeile mehr im Verlauf, die beim nächsten Aufruf im Prompt
steht. Wer ihn einwirft, sieht dem Gespräch beim Abbiegen zu.

## Die mitgelieferten Profile

| Profil | Rolle in der Runde |
|---|---|
| **Skeptische Ökonomin** | Rechnet jede Idee auf Kosten und Nutzen herunter |
| **Technik-Optimist** | Sieht in jeder Neuerung zuerst die Möglichkeiten |
| **Ethikerin** | Fragt, wer profitiert und wer die Rechnung zahlt |
| **Praktiker** | Will wissen, wer es am Montag tatsächlich macht |
| **Advocatus Diaboli** | Widerspricht grundsätzlich der Mehrheitsmeinung |

Neu angelegte Profile landen daneben unter `profile/` und bleiben untracked.

## Ein Profil ist eine Textdatei

```markdown
---
name: Skeptische Ökonomin
beschreibung: Rechnet jede Idee auf Kosten und Nutzen herunter
model: openai-codex/gpt-5.6-luna
thinking: low
farbe: hellblau
---

Du bist Wirtschaftswissenschaftlerin und sitzt in dieser Runde als die
Stimme, die nach Zahlen fragt. …
```

Oben Modell, Denktiefe und Anzeigefarbe, darunter die Rolle in normalem
Deutsch. Dieser Text geht **wörtlich** als Systemprompt an das Modell — es gibt
keine Vorlage drumherum und keine versteckte Zusatzanweisung.

## Architektur

```
Browser (Dashboard)
    ↕ HTTP + SSE
Python-Server (server.py, nur stdlib)
    ↕ subprocess, JSON-Ereignisse
pi CLI (pi --mode json -nt --no-session --system-prompt <Rollentext> -- <Prompt>)
    ↕ Datei-I/O
profile/<slug>.md   ·   partys/<slug>/
```

- **Null externe Python-Dependencies** — `http.server` + `subprocess`
- **Keine Werkzeuge** (`-nt`) — ein Party-Agent kann antworten, sonst nichts:
  nicht lesen, nicht schreiben, nicht ins Netz
- **Kein Gedächtnis** (`--no-session`) — jeder Beitrag ist ein eigener Prozess,
  der Gesprächsverlauf geht jedes Mal neu als Text in den Prompt
- **Status aus dem Dateisystem abgeleitet** — kein State-File. Eine
  abgebrochene Party lässt sich fortsetzen, auch nach einem Serverneustart
- **Sequenzielle Runde** — die Profile antworten aufeinander, Beitrag für
  Beitrag. Im Hörsaal ist das Nacheinander der Punkt
- **Die Rundenzahl ist nur der Anfang** — eine Sitzung lässt sich beliebig oft
  verlängern, und jeder Zwischenruf wird Teil des Verlaufs, den alle folgenden
  Beiträge im Prompt bekommen
- **Live-Denkschritte** — der Server übersetzt die Ereignisse von pi in
  Sprechblasen mit aufklappbarem Denkbereich

## Projektstruktur

```
agent-party/
├── profile/         # Rollenprofile: Frontmatter + Systemprompt
├── server.py        # Python-Backend (stdlib only), baut die pi-Aufrufe
├── dashboard/
│   ├── index.html   # Dashboard SPA
│   ├── style.css    # THM-Corporate-Design, Hell- und Dunkelmodus
│   └── app.js       # Frontend-Logik
├── partys/          # Runtime: ein Ordner je Sitzung (gitignored)
└── start.sh         # Ein-Klick-Start
```

## Dashboard

- **Drei Ansichten** über die Navigation in der Kopfleiste: Agentenprofile,
  Party vorbereiten, Sitzung
- **Profil ausarbeiten lassen** — ein Satz genügt, das Modell schreibt das
  Profil, der Entwurf ist vor dem Speichern änderbar
- **Besetzung mit Reihenfolge** — jedes Profil sitzt einmal am Tisch; für zwei
  ähnliche Stimmen legt „Duplizieren" im Profil-Editor eine Kopie an
- **Modellwechsel im UI** — zwischen ChatGPT-Abo, TensorX und LM Studio, ohne
  Neustart
- **Sprechblasen** in der Profilfarbe, live per Server-Sent Events, mit
  aufklappbarem Bereich „Was das Modell gedacht hat"; rechts eine Übersicht mit
  Besetzung, Beitragszähler und Rundenstand
- **Eingreifen während der Sitzung** — ein Zwischenruf der Gesprächsleitung geht
  in den Prompt des nächsten Beitrags ein, „Weitere Runde" hängt eine Runde an,
  wenn die geplanten durch sind, und „Fazit erstellen" lässt die Sitzung
  zusammenfassen
- **Hell-/Dunkelmodus** im THM-Corporate-Design (Grün `#80BA24`, Grau
  `#4A5C66`); Umschalter im Header, Standard folgt der Systemeinstellung
- **Neuladen verliert nichts** — der gespeicherte Verlauf wird nachgeliefert

## Konfiguration

```bash
cp .env.example .env
```

| Variable | Wirkung |
|---|---|
| `AGENT_PARTY_MODEL` | Schlägt alle Profile und die Wahl im Dashboard zugleich — der Hebel, wenn ein Anbieter mitten in der Vorlesung bremst |
| `AGENT_PARTY_STANDARD_MODELL` | Voreinstellung für neue Profile |

Was zur Auswahl steht, zeigt `pi --list-models`. Das Dashboard bietet
`openai-codex`, `tensorx` und `lmstudio` an — die drei Wege der Vorlesung: Abo,
Cloud, lokal.

## Lizenz

Lehrmaterial der THM – Technische Hochschule Mittelhessen.
