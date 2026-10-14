---
routeAlias: demo-counting-agents
rubrik: The Counting Agents
titel: Fünf Agenten zählen gemeinsam
class: text-xl
---

<div class="thm-center thm-gruppe">
<div class="thm-lead">Eine <strong>absichtlich einfache Aufgabe</strong> — damit wir nicht auf das Ergebnis schauen, sondern darauf, <strong>wie Agenten zusammenarbeiten</strong>.</div>

<CardGrid :cols="5">
  <Card icon="list-ordered" titel="Zähler">Erzeugt fortlaufend Zahlen: 1, 2, 3 …</Card>
  <Card icon="filter" titel="Ungerade">Sammelt die ungeraden Zahlen ein</Card>
  <Card icon="filter" titel="Gerade">Sammelt die geraden Zahlen ein</Card>
  <Card icon="brain" titel="Primzahlen">Prüft jede Zahl&nbsp;— und denkt dabei nach</Card>
  <Card icon="sliders-horizontal" titel="Steuerung">Pausiert, setzt fort, startet neu</Card>
</CardGrid>
</div>

<!--
Zählen kann jeder Taschenrechner, darum geht es in dieser Demo nicht. Die
Aufgabe ist so einfach gewählt, damit ihr den Agenten bei der Arbeit
zuschauen könnt: Wer wartet auf wen, wer hinkt hinterher, wer macht Fehler?

Der Primzahl-Agent ist als einziger so eingestellt, dass er „nachdenken“
darf. Das wirkt sich in der Demo sichtbar aus.
-->

---
rubrik: The Counting Agents
titel: Wie reden die Agenten miteinander?
untertitel: Gar nicht direkt — sie legen Nachrichten in gemeinsame Dateien.
---

<div class="bus-rahmen">
  <CountingBus />
</div>

<Callout icon="info"><strong>Jede Datei ist wie ein schwarzes Brett:</strong> Einer hängt etwas aus, die anderen lesen nach — jeder in seinem eigenen Takt.</Callout>

<style>
.bus-rahmen {
  flex: 1;
  min-height: 0;
  display: flex;
  justify-content: center;
  padding: 0 0 2.4rem;
}
</style>

<!--
Der Zähler schreibt seine Zahlen in eine Datei, die drei Sammler lesen sie
dort. Niemand wartet auf eine Antwort: Jeder Agent merkt sich, bis wohin er
schon gelesen hat, und liest beim nächsten Mal ab dort weiter.

Die Steuerung schreibt ihre Befehle in eine zweite Datei. Dort schauen alle
Agenten zuerst nach, bevor sie weiterarbeiten.

Die Dateien enthalten ganz normalen Text. Man kann sie während der Demo
jederzeit anzeigen lassen, etwa mit dem Befehl `cat`, und mitlesen — kein
Zauber, nur Text.
-->

---
rubrik: The Counting Agents
titel: Was ein Agent kann, bestimmt sein Werkzeugkasten
untertitel: Jeder bekommt genau die Werkzeuge, die seine Aufgabe braucht — nicht mehr.
---

<div class="thm-center">
  <WerkzeugMatrix />
</div>

<!--
Auf der Folie „Aufbau eines KI-Agenten“ standen im Harness links die
Werkzeuge. Hier seht ihr, dass jeder Agent andere bekommt. Alle fünf nutzen
dasselbe Modell, verschieden sind nur Aufgabe und Werkzeugkasten. Welche
Werkzeuge ein Agent braucht, entscheidet seine Aufgabe.

Die Tabelle liest man am besten Zeile für Zeile: Nur der Zähler darf Zahlen
veröffentlichen, nur die Steuerung darf Befehle schicken. Ein Sammler kann
nicht in den Bus schreiben — nicht, weil es ihm verboten ist, sondern weil
ihm das Werkzeug dafür fehlt.

Die letzte Zeile betrifft die allgemeinen Werkzeuge wie die Shell oder das
Lesen und Schreiben beliebiger Dateien. Die hat keiner der Agenten, sie
werden ihnen beim Start weggenommen. Warum nicht einfach im Text der Aufgabe
verbieten? Weil die Werkzeuge dann zwar verboten, aber noch da wären. So
sind sie gar nicht da, und das wirkt stärker als jedes Verbot im Text.

Die Aufgabe selbst steht in normalem Deutsch in einer Textdatei, beim
Primzahl-Agenten zum Beispiel in `agents/prime.md`.
-->

---
rubrik: The Counting Agents · Live-Demo
titel: Eure Vorhersage
untertitel: Bevor es losgeht — was glaubt ihr?
class: text-xl
hideInToc: true
---

<div class="thm-center thm-stack">
  <QuestionItem>Alle Agenten haben <strong>denselben Takt</strong>. Laufen sie im Gleichschritt?</QuestionItem>
  <QuestionItem>Wer wird am weitesten <strong>hinterherhinken</strong> — und warum?</QuestionItem>
  <QuestionItem>Macht die KI beim <strong>Primzahlen-Prüfen</strong> Fehler?</QuestionItem>
</div>

<!--
Die Antworten zeigt die Demo. Aufgelöst werden die Fragen auf der Folie
„Was haben wir gesehen?“ am Ende dieses Blocks.
-->

---
layout: statement
rubrik: The Counting Agents · Live-Demo
titel: Los geht's!
zitat: false
class: text-xl
hideInToc: true
---

Wechsel zu den **Counting Agents**

<span class="st-note">Herdr-Tab mit den fünf Agenten, Übersicht unter <a href="http://localhost:8777" target="_blank">localhost:8777</a></span>

<!--
In der Demo läuft jeder Agent in einem eigenen Fenster, sodass jeder
Handgriff sichtbar ist. Die Übersicht zeigt das Zahlenband und wie weit
jeder Agent zurückliegt. Eine rote Kachel markiert eine Zahl, die der
Primzahl-Agent falsch eingeordnet hat.
-->

---
rubrik: The Counting Agents · Bewertung
titel: Was haben wir gesehen?
untertitel: Zurück zu euren Vorhersagen.
hideInToc: true
---

<div class="thm-stack">
  <QuestionItem>Warum hinkt der <strong>Primzahl-Agent</strong> hinterher, obwohl alle denselben Takt haben?</QuestionItem>
  <QuestionItem>Gab es eine <strong>rote Kachel</strong>? Was ist da passiert?</QuestionItem>
  <QuestionItem>Rund <strong>90 Anfragen pro Minute</strong> an die KI — nur fürs Zählen. Lohnt sich das?</QuestionItem>
  <QuestionItem>Ehrlich: Braucht man für diese Aufgabe <strong>überhaupt eine KI</strong>?</QuestionItem>
</div>

<!--
**Warum hinkt der Primzahl-Agent hinterher?** Alle Agenten haben denselben
Takt von drei Sekunden. Der Takt ist aber nur die Pause zwischen zwei
Durchläufen. Wie lange ein Durchlauf selbst dauert, hängt davon ab, was das
Modell darin zu tun hat. Die Sammler für ungerade und gerade Zahlen nehmen
alles Neue auf einmal auf und holen so jeden Rückstand wieder auf. Der
Primzahl-Agent darf pro Durchlauf nur eine Zahl prüfen und denkt dabei
nach. Jeder seiner Durchläufe dauert etwas länger als beim Zähler, und der
Abstand wächst. Gleicher Takt heißt also nicht gleiches Tempo: Nachdenken
kostet Zeit.

**Die rote Kachel:** Das Modell hat eine Zahl für eine Primzahl gehalten,
die keine ist. Typisch sind Zahlen, die prim aussehen, etwa 51 = 3·17,
57 = 3·19 oder 91 = 7·13. Das Modell rechnet nicht, es schätzt, was
plausibel klingt — wie auf der Folie „Was steckt hinter ChatGPT & Co.?“:
das wahrscheinlichste nächste Wort. Gab es keine rote Kachel, ist es
diesmal gut gegangen, aber ohne Garantie. Dass die Kachel rot wird, liegt
am Dashboard: Es rechnet selbst nach. Das ist eine automatische Prüfung,
kein Mensch muss jede Zahl kontrollieren.

**90 Anfragen pro Minute:** Ein Durchlauf besteht aus etwa fünf Anfragen an
das Modell, eine pro Werkzeug plus die Antwort. Er dauert rund zehn
Sekunden, dazu kommen drei Sekunden Takt — macht gut vier Durchläufe pro
Minute. Vier Agenten mit je fünf Anfragen und etwa 4,5 Durchläufen ergeben
rund 90 Anfragen pro Minute. Jede Anfrage kostet Geld, Strom und Zeit.
Manche Anbieter erlauben nur 60 Anfragen pro Minute, dann bricht die Demo
am Limit ab. Ihr seht eine Zahl, dahinter stecken fünf Gespräche mit einem
Modell.

**Braucht man dafür überhaupt eine KI?** Nein. Aufgaben mit genau einer
richtigen Antwort erledigt ein normales Programm fehlerfrei und kostenlos,
Millionen Zahlen pro Sekunde. Die Aufgabe ist absichtlich banal, damit man
aufs Zusammenspiel schaut und nicht aufs Ergebnis. Spannend wird derselbe
Aufbau, wenn statt Zahlen E-Mails ankommen und die Agenten sie nach
Beschwerde, Bestellung und Frage sortieren. Da gibt es nicht die eine
richtige Antwort. KI lohnt sich dort, wo Sprache, Urteil und Unschärfe ins
Spiel kommen.

Drei Beobachtungen aus dieser Demo gelten für Agenten allgemein: Anfragen
kosten Geld, die rote Kachel ist eine Halluzination, und dass das Dashboard
nachrechnet, ist Qualitätskontrolle.
-->

---
rubrik: The Counting Agents
titel: Das war The Counting Agents
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>
