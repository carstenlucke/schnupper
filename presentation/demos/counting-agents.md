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
- Jeden Agenten kurz vorstellen
- Pointe vorwegnehmen: Zählen kann jeder Taschenrechner — darum geht es nicht
- Wir schauen den Agenten bei der Arbeit zu: Wer wartet, wer hinkt hinterher,
  wer macht Fehler?
- Primzahl-Agent ist der einzige, der "nachdenken" darf — das wird man sehen
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
- Zähler schreibt Zahlen in eine Datei, die drei Sammler lesen sie dort
- Niemand wartet auf eine Antwort — jeder merkt sich, bis wohin er gelesen hat
- Steuerung schreibt Befehle in eine zweite Datei; alle schauen dort zuerst
  nach
- Die Dateien kann man live mit cat anschauen — kein Zauber, nur Text
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
- Rückbezug auf "Was macht aus einem Modell einen Agenten?": Im Harness
  links die Werkzeuge — hier sieht man, dass jeder Agent andere bekommt
- Alle fünf nutzen dasselbe Modell. Verschieden sind Aufgabe und
  Werkzeugkasten — und die Aufgabe entscheidet, welche Werkzeuge ein Agent
  braucht
- Tabelle zeilenweise lesen: Nur der Zähler darf veröffentlichen, nur die
  Steuerung Befehle schicken
- Ein Sammler KANN nicht in den Bus schreiben — nicht, weil es ihm verboten
  ist, sondern weil das Werkzeug fehlt
- Letzte Zeile: Die allgemeinen Werkzeuge (Shell, Dateien lesen/schreiben)
  hat keiner — sie werden beim Start weggenommen
- Maus auf "Alles andere" zeigt den Merksatz: nicht verboten, sondern gar
  nicht da — erst fragen "Warum nicht einfach im Text verbieten?", dann
  aufdecken
- Die Aufgabe selbst steht wieder in normalem Deutsch in einer Textdatei
  (ggf. agents/prime.md zeigen)
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
- Handzeichen bei jeder Frage, Tipps an der Tafel festhalten
- Nicht auflösen — das macht gleich die Demo
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
- Im Herdr-Pane: ./scripts/start.sh (vorher gestartet oder jetzt)
- Erst die Panes zeigen: jeder Handgriff sichtbar
- Dann das Dashboard: Zahlenband und Rückstand
- Einen Agenten anklicken, um nur seine Zahlen zu zeigen
- In der Steuerung: prime pausieren, wieder anlaufen lassen
- Nach einer Rot-Kachel Ausschau halten — wenn sie kommt, sofort zeigen
- Ggf. agents/prime.md öffnen: "Das ist der ganze Agent."
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
- Vorhersagen von vorhin auflösen
- Rückstand: Der Takt (3 s) ist nur die Pause zwischen zwei Durchläufen —
  wie lange ein Durchlauf dauert, hängt davon ab, was das Modell zu tun hat
  - odd und even nehmen alles Neue auf einmal und holen jeden Rückstand auf
  - prime darf nur eine Zahl pro Durchlauf prüfen und denkt dabei nach —
    jeder Durchlauf etwas länger als beim Zähler, der Abstand wächst
  - Merksatz: Gleicher Takt heißt nicht gleiches Tempo. Nachdenken kostet Zeit
- Rote Kachel: Das Modell hat eine Zahl für prim gehalten, die es nicht ist
  - Typisch sind Zahlen, die prim aussehen: 51 = 3·17, 57 = 3·19, 91 = 7·13
  - Das Modell rechnet nicht, es schätzt, was plausibel klingt (Rückbezug auf
    "Was steckt hinter ChatGPT & Co.?": das wahrscheinlichste nächste Wort)
  - Keine rote Kachel? Diesmal gut gegangen — aber ohne Garantie
  - Das Dashboard rechnet selbst nach — eine automatische Prüfung, kein Mensch
    muss jede Zahl kontrollieren
- Anfragen: Ein Durchlauf sind ~5 Anfragen (eine pro Werkzeug plus Antwort)
  - Ein Durchlauf ~10 s plus 3 s Takt → gut 4 Durchläufe pro Minute
  - 4 Agenten × 5 Anfragen × ~4,5 Durchläufe ≈ 90 Anfragen pro Minute
  - Jede Anfrage kostet Geld, Strom und Zeit; manche Anbieter erlauben nur
    60 pro Minute — dann bricht die Demo am Limit ab
  - Man sieht eine Zahl — dahinter stecken fünf Gespräche mit einem Modell
- Die Pointe: Nein! Aufgaben mit genau einer richtigen Antwort erledigt ein
  normales Programm fehlerfrei und kostenlos — Millionen Zahlen pro Sekunde
  - Die Aufgabe ist absichtlich banal: So schaut man aufs Zusammenspiel,
    nicht aufs Ergebnis
  - Weiterdenken: gleicher Aufbau, aber statt Zahlen kommen E-Mails, und die
    Agenten sortieren nach Beschwerde, Bestellung, Frage — da gibt es nicht
    die eine richtige Antwort
  - KI lohnt sich dort, wo Sprache, Urteil und Unschärfe ins Spiel kommen
- Beispiele für den Reality Check merken: Anfragen = Kosten, rote Kachel =
  Halluzination, Dashboard rechnet nach = Qualitätskontrolle
-->

---
rubrik: The Counting Agents
titel: Das war The Counting Agents
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>

<!--
- Noch Zeit? "Noch eine Demo" führt zur Übersicht
- Sonst weiter (→) zu "Was nehmen wir mit?"
-->
