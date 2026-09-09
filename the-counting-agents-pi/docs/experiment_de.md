# Das Experiment: Was diese Fassung anders macht

Dieses Projekt gibt es zweimal. `the-counting-agents` läuft mit der OpenCode
CLI und einem Modell auf dem eigenen Rechner, diese Fassung mit der pi CLI,
einem Modell in der Cloud und eigenen Werkzeugen. Beide zeigen dasselbe: fünf
Agenten, die über Dateien zusammenarbeiten.

Der Vergleich ist der eigentliche Ertrag. Was ändert sich, wenn Agenten
passendes Werkzeug bekommen statt allgemeines?

> English version: [experiment.md](experiment.md)

## Der Ausgangsbefund

In der OpenCode-Fassung bestehen die Agent-Prompts zu mehr als der Hälfte aus
Anweisungen, die mit der Aufgabe nichts zu tun haben:

- Zeitstempel mit `date -u +%Y-%m-%dT%H:%M:%SZ` erzeugen, weil BSD-`date` das
  Format für Millisekunden nicht kennt
- Leere Dateien nicht mit dem Read-Werkzeug öffnen, weil das einen
  Offset-Fehler auslöst
- Log-Dateien mit `bash` und `echo >>` beschreiben, nie mit `write`, weil
  `write` die Datei ersetzt
- keine absoluten Pfade, keine führenden Schrägstriche
- `bus/numbers.log` immer vollständig lesen, weil der Offset-Parameter des
  Read-Werkzeugs Zeilen zählt und nicht Sequenznummern

Jede dieser Zeilen steht dort, weil ein Durchlauf daran gescheitert ist. Sie
sind nicht falsch — sie sind nur an der falschen Stelle. Es ist Wissen über
Werkzeuge, abgelegt im Prompt, wiederholt in fünf Dateien, und jedes Modell
muss es bei jedem Durchlauf neu lesen und befolgen.

## Die Gegenprobe

In dieser Fassung steht dieses Wissen einmal im Code der Werkzeuge. Der Prompt
des Odd-Agenten ist danach dreißig Zeilen lang und enthält nur noch, was er
tun soll — mit einer einzigen Regel zur Mechanik: Der Durchlauf endet mit
`state_write`.

Was dabei sichtbar wird:

### Fehler wandern von der Laufzeit in den Entwurf

Ein Agent kann eine leere Datei nicht mehr falsch öffnen, weil er Dateien gar
nicht mehr öffnet. Übrig bleiben Fehler anderer Art: Ein Werkzeug wird zur
falschen Zeit aufgerufen, oder gar nicht. Das ist die interessantere Sorte —
sie handelt von der Aufgabe, nicht vom Werkzeugkasten.

Und sie lässt sich beheben, ohne das Modell zu wechseln. Als das lokale Modell
in einem Testlauf den abschließenden `state_write` ausließ, half kein besseres
Modell, sondern ein Satz im Prompt, der sagt, warum dieser Aufruf nicht
optional ist.

### Was man wegnimmt, ist wirksamer als was man verbietet

Die Sammler-Agenten dürfen nicht in den Bus schreiben. In der OpenCode-Fassung
steht das als Regel im Prompt — und ein Modell, das sich verrennt, kann sie
brechen, denn `bash` liegt griffbereit. Hier fehlt ihnen schlicht das Werkzeug.
`--no-builtin-tools` nimmt ihnen `bash`, `read` und `write`, `--tools` gibt
genau vier Namen frei.

Für die Vorlesung ist das der greifbarste Punkt: Ein Agent ist nicht dasselbe
wie ein Modell. Ein Agent ist ein Modell, eine Aufgabe und ein Werkzeugkasten —
und der Werkzeugkasten entscheidet, was überhaupt geschehen kann.

### Die Buchhaltung gehört nicht ins Modell

Sequenznummern vergeben, Zeitstempel setzen, Listen zählen, den zuletzt
geltenden Steuerbefehl bestimmen: Das sind Aufgaben mit genau einer richtigen
Antwort. Ein Sprachmodell findet sie meistens — meistens reicht nicht, wenn
alle drei Sekunden ein Durchlauf startet und im Hörsaal jemand zusieht.

Die Grenze verläuft dort, wo es interessant wird: Ob 91 eine Primzahl ist,
entscheidet weiterhin das Modell. Ein `is_prime`-Werkzeug wäre zuverlässiger
und würde die Demo ihres Gegenstands berauben.

## Was gleich geblieben ist

Die Architektur. Beide Fassungen teilen die Entscheidungen, die
`the-counting-agents/docs/experiment_de.md` begründet:

- **Zwei Dateien als Bus**, an die nur angehängt wird. Kein Broker, keine
  Warteschlange, kein Netzwerk. Man kann sie mit `cat` lesen — im Vortrag ein
  unschätzbarer Vorteil.
- **Kein Locking, keine Bestätigungen.** Jeder Agent merkt sich, bis wohin er
  gelesen hat, und holt beim nächsten Durchlauf den Rest. Verpasst er einen
  Durchlauf, holt er auf.
- **Kein Aufräumen, keine Rotation.** Eine Vorführung dauert 90 Minuten; die
  Dateien bleiben klein.
- **Der Prime-Agent ist absichtlich langsam.** Eine Zahl pro Durchlauf, damit
  im Pane sichtbar wird, wie er zurückfällt, während die anderen weiterlaufen.

## Was diese Fassung teurer macht

Ehrlichkeit gehört dazu: Das Modell läuft jetzt in der Cloud. Das ist schnell —
ein Durchlauf dauert Sekunden statt eineinhalb Minuten — und kostet Geld,
wenn auch wenig. Fünf Agenten über eine Vorlesung hinweg bleiben im
Cent-Bereich; pi zeigt die Kosten je Durchlauf im Pane an.

Dafür entfällt das Setup im Hörsaal: kein LM Studio, kein geladenes Modell,
keine Wartezeit beim ersten Durchlauf. Wer die Demo ohne Netz zeigen will,
trägt in den Frontmatter-Zeilen der Agenten ein lokales Modell ein — die
Werkzeuge bleiben dieselben.

## Wann man es anders machen sollte

Alles hier ist auf Vorführbarkeit gebaut, nicht auf Betrieb. Sobald Agenten
Arbeit erledigen, die jemand braucht, gelten andere Regeln: eine Warteschlange
mit Zustellgarantie, Wiederholungen mit Backoff, Schemaversionen für
Ereignisse, Beobachtbarkeit, die den Namen verdient. Nichts davon steht hier —
und das ist kein Versäumnis, sondern der Punkt.
