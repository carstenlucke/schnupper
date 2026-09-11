# Was bei einem Agentendurchlauf wirklich passiert

Im Pane erscheint eine Zeile: `→ 42`. Diese Seite erklärt, was dazwischen liegt — die **Trajektorie**, also die Folge von Anfragen, Werkzeugaufrufen und Ergebnissen, aus der diese eine Zeile entsteht.

> English version: [Trajectory.md](Trajectory.md)

## Die Grundfigur

Ein Sprachmodell kann nichts tun. Es bekommt Text und erzeugt Text. Damit ein Agent daraus wird, braucht es drei Zutaten und eine Schleife:

1. **Der Systemprompt** sagt, wer der Agent ist und was er tun soll — bei uns der Text unterhalb des Frontmatters in `agents/<name>.md`.
2. **Die Werkzeugliste** wird als Schema mitgeschickt: Name, Beschreibung und erwartete Parameter jedes erlaubten Werkzeugs. Das Modell sieht damit, was es anfordern kann.
3. **Der Auftrag** ist die Nachricht, mit der der Durchlauf beginnt: „Führe deinen nächsten Schritt aus."

Dann läuft die Schleife: Das Modell antwortet entweder mit **Text** — dann ist der Durchlauf zu Ende — oder mit einem **Werkzeugaufruf**. Im zweiten Fall führt pi das Werkzeug aus, hängt das Ergebnis an das Gespräch an und schickt alles erneut zum Modell. Das Modell entscheidet in jedem Schritt neu.

Entscheidend ist: **Das Modell führt nichts aus.** Es formuliert eine Bitte („ruf `bus_publish` mit `value: 1` auf"), und pi entscheidet, ob und wie diese Bitte ausgeführt wird. Genau an dieser Stelle wirkt die Werkzeug-Allowlist — was nicht in `--tools` steht, kann das Modell nicht einmal anfordern.

## Eine echte Trajektorie

Aufgezeichnet mit `pi --mode json` bei einem Durchlauf des Counter-Agenten, gekürzt auf das Wesentliche:

```
Anfrage 1  →  Modell: toolCall control_read {"agent": "counter"}      762 ein / 33 aus
           ←  pi:     {"status":"running","verbose":false,"reset_requested":false}

Anfrage 2  →  Modell: toolCall state_read {"agent": "counter"}        820 ein / 18 aus
           ←  pi:     {"agent":"counter","last_value":0,"status":"running",...}

Anfrage 3  →  Modell: toolCall bus_publish {"value": 1}               868 ein / 18 aus
           ←  pi:     {"published":{"seq":1,"value":1}}

Anfrage 4  →  Modell: toolCall state_write {"agent":"counter",...}    908 ein / 32 aus
           ←  pi:     {"agent":"counter","last_value":1,...,"updated_at":"..."}

Anfrage 5  →  Modell: "→ 1"                                           989 ein /  7 aus
              kein Werkzeug mehr, Durchlauf zu Ende
```

Vier Werkzeugaufrufe, **fünf Anfragen an das Modell**, eine Zeile Ausgabe. Die Schrittfolge stammt aus dem Prompt — dort steht sie allerdings nicht als Liste von Werkzeugnamen, sondern als Satz: nachsehen, ob es Anweisungen gibt; nachsehen, wo man steht; die nächste Zahl in den Bus stellen; sich merken, wie weit man ist. Welches Werkzeug zu welchem Halbsatz gehört, entnimmt das Modell den Werkzeugbeschreibungen. Es hält sich an die Reihenfolge, weil sie dort steht, nicht weil irgendetwas sie erzwingt.

Nachrechnen kann man das jederzeit selbst:

```bash
pi -p --mode json -nc -nbt -a --no-session \
   --model "$COUNTING_AGENTS_MODEL" \
   --tools bus_publish,control_read,state_read,state_write \
   --system-prompt "$(sed '1,/^---$/d;1,/^---$/d' agents/counter.md)" \
   "Führe deinen nächsten Schritt aus." < /dev/null \
   | grep -c '"type":"turn_start"'
```

Das `< /dev/null` gehört dazu: Im Druckmodus liest pi auch von der Standardeingabe, um sie an den Auftrag anzuhängen. Ohne diese Umleitung wartet der Befehl darauf, dass jemand etwas eintippt — und sieht aus, als hinge er.

## Warum jede Anfrage teurer wird als die vorige

Das Modell hat kein Gedächtnis. Damit es in Anfrage 4 noch weiß, was in Anfrage 1 geschah, wird **das gesamte bisherige Gespräch jedes Mal komplett mitgeschickt**: Systemprompt, Werkzeugschemata, Auftrag, alle bisherigen Werkzeugaufrufe und deren Ergebnisse.

```
Anfrage 1:  System + Werkzeuge + Auftrag
Anfrage 2:  ... + Aufruf 1 + Ergebnis 1
Anfrage 3:  ... + Aufruf 1 + Ergebnis 1 + Aufruf 2 + Ergebnis 2
Anfrage 4:  ... und so weiter
```

Genau das zeigen die Zahlen oben: Die Eingabe wächst von 762 auf 989 Token, während die Ausgabe klein bleibt. Für die eine Zeile `→ 1` werden in Summe **4347 Token gelesen und 108 geschrieben** — das Vierzigfache an Eingabe.

Daher zwei Beobachtungen, die im Vortrag gut ankommen:

- **Kurze Werkzeugergebnisse sind bares Geld.** Unsere Werkzeuge antworten mit einer Zeile kompaktem JSON, nicht mit ganzen Dateien. Ein `bus_read`, das alle Ereignisse zurückgäbe statt nur der neuen, würde diese Zeile in jeder weiteren Anfrage erneut bezahlen.
- **Der Systemprompt wird bei jeder Anfrage mitbezahlt.** Ein Prompt mit zwei Seiten Fehlerbehandlung kostet nicht einmal, sondern fünfmal pro Durchlauf. Dass die Werkzeuge diese Sorgfalt übernommen haben, spart also nicht nur Verständlichkeit, sondern auch Tokens.

Anbieter rechnen deshalb mit **Prompt-Caching** gegen: Der unveränderte Anfang des Gesprächs wird wiederverwendet und günstiger abgerechnet. In der Anzeige von pi taucht das als `cacheRead` auf.

## Jeder Durchlauf beginnt bei null

Die Startskripte rufen pi mit `--no-session` auf. Zwischen zwei Durchläufen bleibt vom Gespräch **nichts** übrig — kein Verlauf, keine Erinnerung.

Was der Agent trotzdem weiß, weiß er aus zwei Dateien: `_state/<agent>.json` sagt ihm, wo er stehengeblieben ist, `_bus/numbers.log`, was inzwischen passiert ist. Sein Gedächtnis liegt also nicht im Modell, sondern auf der Platte — nachlesbar mit `cat`, für jeden im Hörsaal sichtbar.

Das hat einen praktischen Nebeneffekt: Ein abgestürzter oder abgewürgter Durchlauf hinterlässt keinen Scherbenhaufen. Der nächste liest den Zustand und macht weiter.

## Was schiefgehen kann

| Beobachtung im Pane | Was dahintersteckt |
|---|---|
| Der Agent beschreibt, was er tun würde, statt es zu tun | Das Modell hat Text statt eines Werkzeugaufrufs erzeugt. Meist hilft ein deutlicherer Prompt („ruf die Werkzeuge auf") |
| Derselbe Wert erscheint immer wieder | Der abschließende `state_write` fehlt, `last_seq` bleibt stehen |
| Der Durchlauf bricht nach 60 Sekunden ab | Der Wachhund in `run-agent.sh` — das Modell antwortet nicht oder dreht sich im Kreis |
| HTTP 429 | Rate-Limit. Fünf Anfragen je Durchlauf summieren sich schnell, siehe „Anfragen zählen" in der [readme_de.md](../readme_de.md) |

## Die Ereignisse in pi

Wer genauer hinsehen will, bekommt mit `--mode json` je Zeile ein Ereignis:

| Ereignis | Bedeutung |
|---|---|
| `agent_start` / `agent_end` | Klammer um den gesamten Durchlauf |
| `turn_start` / `turn_end` | Eine Anfrage an das Modell — diese zählt man |
| `message_start` / `message_update` / `message_end` | Die Antwort, tröpfchenweise und am Ende vollständig |
| `tool_execution_start` / `tool_execution_end` | pi führt ein Werkzeug aus |

`turn_start` zu zählen ist die ehrlichste Messung dessen, was ein Agent tatsächlich kostet.

## Weiterlesen

- [`pi-custom-tools_de.md`](pi-custom-tools_de.md) — wie die Werkzeuge gebaut sind, die hier aufgerufen werden
- [`experiment_de.md`](experiment_de.md) — warum die Architektur so aussieht
