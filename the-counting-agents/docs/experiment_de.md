# Das Experiment: eigene Werkzeuge statt allgemeiner

Diese Demo zeigt fünf Agenten, die über Dateien zusammenarbeiten. Das ginge auch mit den allgemeinen Werkzeugen, die pi mitbringt — `bash`, `read`, `write`. Die Demo gibt ihren Agenten stattdessen eigene, passgenaue Werkzeuge und nimmt ihnen die allgemeinen weg.

Der Vergleich ist der eigentliche Ertrag. Was ändert sich, wenn Agenten passendes Werkzeug bekommen statt allgemeines?

> English version: [experiment.md](experiment.md)

## Das Problem mit allgemeinen Werkzeugen

Mit allgemeinen Werkzeugen bestehen die Agent-Prompts bald zu mehr als der Hälfte aus Anweisungen, die mit der Aufgabe nichts zu tun haben:

- Zeitstempel mit `date -u +%Y-%m-%dT%H:%M:%SZ` erzeugen, weil BSD-`date` das Format für Millisekunden nicht kennt
- Leere Dateien nicht mit dem Read-Werkzeug öffnen, weil das einen Offset-Fehler auslösen kann
- Log-Dateien mit `bash` und `echo >>` beschreiben, nie mit `write`, weil `write` die Datei ersetzt
- keine absoluten Pfade, keine führenden Schrägstriche
- `_bus/numbers.log` immer vollständig lesen, weil der Offset-Parameter des Read-Werkzeugs Zeilen zählt und nicht Sequenznummern

Jede dieser Zeilen kommt hinzu, weil ein Durchlauf daran scheitert. Sie sind nicht falsch — sie sind nur an der falschen Stelle. Es ist Wissen über Werkzeuge, abgelegt im Prompt, wiederholt in fünf Dateien, und jedes Modell muss es bei jedem Durchlauf neu lesen und befolgen.

## Die Gegenprobe

Hier steht dieses Wissen einmal im Code der Werkzeuge. Der Prompt des Odd-Agenten ist dreißig Zeilen lang, nennt kein einziges Werkzeug beim Namen und enthält nur, was er tun soll — mit einer einzigen Regel zur Mechanik: Am Ende jedes Durchlaufs merkt er sich, wie weit er ist, sonst bekommt er beim nächsten Mal dieselben Zahlen noch einmal vorgelegt. Welches Werkzeug das erledigt, steht in dessen Beschreibung, nicht im Prompt.

Was dabei sichtbar wird:

### Fehler wandern von der Laufzeit in den Entwurf

Ein Agent kann eine leere Datei nicht falsch öffnen, weil er Dateien gar nicht öffnet. Übrig bleiben Fehler anderer Art: Ein Werkzeug wird zur falschen Zeit aufgerufen, oder gar nicht. Das ist die interessantere Sorte — sie handelt von der Aufgabe, nicht vom Werkzeugkasten.

Und sie lässt sich beheben, ohne das Modell zu wechseln. Als ein Modell in einem Testlauf das abschließende Merken ausließ, half kein besseres Modell, sondern ein Satz im Prompt, der sagt, warum dieser Schritt nicht optional ist.

### Was man wegnimmt, ist wirksamer als was man verbietet

Die Sammler-Agenten dürfen nicht in den Bus schreiben. Mit allgemeinen Werkzeugen stünde das als Regel im Prompt — und ein Modell, das sich verrennt, könnte sie brechen, denn `bash` läge griffbereit. Hier fehlt ihnen schlicht das Werkzeug. `--no-builtin-tools` nimmt ihnen `bash`, `read` und `write`, `--tools` gibt genau vier Namen frei.

Für die Vorlesung ist das der greifbarste Punkt: Ein Agent ist nicht dasselbe wie ein Modell. Ein Agent ist ein Modell, eine Aufgabe und ein Werkzeugkasten — und der Werkzeugkasten entscheidet, was überhaupt geschehen kann.

### Die Buchhaltung gehört nicht ins Modell

Sequenznummern vergeben, Zeitstempel setzen, Listen zählen, den zuletzt geltenden Steuerbefehl bestimmen: Das sind Aufgaben mit genau einer richtigen Antwort. Ein Sprachmodell findet sie meistens — meistens reicht nicht, wenn alle drei Sekunden ein Durchlauf startet und im Hörsaal jemand zusieht.

Die Grenze verläuft dort, wo es interessant wird: Ob 91 eine Primzahl ist, entscheidet weiterhin das Modell. Ein `is_prime`-Werkzeug wäre zuverlässiger und würde die Demo ihres Gegenstands berauben.

## Was bewusst einfach bleibt

Die Architektur ist auf den Hörsaal zugeschnitten:

- **Zwei Dateien als Bus**, an die nur angehängt wird. Kein Broker, keine Warteschlange, kein Netzwerk. Man kann sie mit `cat` lesen — im Vortrag ein unschätzbarer Vorteil.
- **Kein Locking, keine Bestätigungen.** Jeder Agent merkt sich, bis wohin er gelesen hat, und holt beim nächsten Durchlauf den Rest. Verpasst er einen Durchlauf, holt er auf.
- **Kein Aufräumen, keine Rotation.** Eine Vorführung dauert 90 Minuten; die Dateien bleiben klein.
- **Der Prime-Agent ist absichtlich langsam.** Eine Zahl pro Durchlauf, damit im Pane sichtbar wird, wie er zurückfällt, während die anderen weiterlaufen.

## Was das Modell in der Cloud kostet

Ehrlichkeit gehört dazu: Das Modell läuft in der Cloud. Das ist schnell — ein Durchlauf dauert Sekunden, mit einem lokalen Modell eher eineinhalb Minuten — und kostet Geld, wenn auch wenig. Fünf Agenten über eine Vorlesung hinweg bleiben im Cent-Bereich; pi zeigt die Kosten je Durchlauf im Pane an.

Dafür entfällt das Setup im Hörsaal: kein LM Studio, kein geladenes Modell, keine Wartezeit beim ersten Durchlauf. Wer die Demo ohne Netz zeigen will, trägt in den Frontmatter-Zeilen der Agenten ein lokales Modell ein — die Werkzeuge bleiben dieselben.

## Wann man es anders machen sollte

Alles hier ist auf Vorführbarkeit gebaut, nicht auf Betrieb. Sobald Agenten Arbeit erledigen, die jemand braucht, gelten andere Regeln: eine Warteschlange mit Zustellgarantie, Wiederholungen mit Backoff, Schemaversionen für Ereignisse, Beobachtbarkeit, die den Namen verdient. Nichts davon steht hier — und das ist kein Versäumnis, sondern der Punkt.
