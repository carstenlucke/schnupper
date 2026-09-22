---
routeAlias: demo-counting-agents
rubrik: The Counting Agents
titel: Fünf Agenten zählen gemeinsam
---

<div class="thm-center">
<div class="thm-lead">Eine <strong>absichtlich einfache Aufgabe</strong> — damit wir nicht auf das Ergebnis schauen, sondern darauf, <strong>wie Agenten zusammenarbeiten</strong>.</div>

<CardGrid :cols="5" class="mt-4">
  <Card icon="list-ordered" titel="Zähler">Erzeugt fortlaufend Zahlen: 1, 2, 3 …</Card>
  <Card icon="filter" titel="Ungerade">Sammelt die ungeraden Zahlen ein</Card>
  <Card icon="filter" titel="Gerade">Sammelt die geraden Zahlen ein</Card>
  <Card icon="brain" titel="Primzahlen">Prüft jede Zahl — und denkt dabei nach</Card>
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

<Callout icon="info"><strong>Wie ein schwarzes Brett:</strong> Einer hängt etwas aus, die anderen lesen nach, was sie betrifft — jeder in seinem eigenen Takt.</Callout>

<style>
.bus-rahmen {
  flex: 1;
  min-height: 0;
  display: flex;
  justify-content: center;
  padding: 0.2rem 0 0.8rem;
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
---

<div class="gleichung">
  <span class="g-teil g-agent"><ThmIcon name="bot" ton="weiss" :size="1.25" /> KI-Agent</span>
  <span class="g-op">=</span>
  <span class="g-teil"><ThmIcon name="brain" :size="1.25" /> Modell</span>
  <span class="g-op">+</span>
  <span class="g-teil"><ThmIcon name="pen-line" :size="1.25" /> Aufgabe</span>
  <span class="g-op">+</span>
  <span class="g-teil g-kasten"><ThmIcon name="wrench" ton="weiss" :size="1.25" /> Werkzeugkasten</span>
</div>

<div class="thm-center">
  <WerkzeugMatrix />
</div>

<Callout icon="info" ton="hell">„Alles andere“ ist <strong>nicht verboten</strong> — die Werkzeuge sind <strong>gar nicht da</strong>. Das wirkt stärker als jedes Verbot im Text.</Callout>

<style>
.gleichung {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin: 0 0 0.6rem;
  font-size: 1.2rem;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}
.g-teil {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.3rem 0.85rem;
  background: var(--thm-grey-50);
}
.g-agent { background: var(--thm-grey-600); color: var(--white); }
.g-kasten { background: var(--thm-green-500); color: var(--white); }
.g-op { font-size: 1.5rem; color: var(--thm-green-600); }
</style>

<!--
- Rückbezug auf "Der Unterschied": Agenten handeln — mit Werkzeugen
- Die Gleichung oben: Modell und Aufgabe haben alle gleich, der
  Werkzeugkasten macht den Unterschied
- Tabelle zeilenweise lesen: Nur der Zähler darf veröffentlichen, nur die
  Steuerung Befehle schicken
- Ein Sammler KANN nicht in den Bus schreiben — nicht, weil es ihm verboten
  ist, sondern weil das Werkzeug fehlt
- Letzte Zeile: Die allgemeinen Werkzeuge (Shell, Dateien lesen/schreiben)
  hat keiner — sie werden beim Start weggenommen
- Die Aufgabe selbst steht wieder in normalem Deutsch in einer Textdatei
  (ggf. agents/prime.md zeigen)
-->

---
rubrik: The Counting Agents · Live-Demo
titel: Eure Vorhersage
untertitel: Bevor es losgeht — was glaubt ihr?
hideInToc: true
---

<div class="thm-stack">
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
- Rückstand: prime prüft eine Zahl pro Durchlauf und denkt nach — Nachdenken
  kostet Zeit
- Rote Kachel: Das Modell hat eine Zahl für prim gehalten, die es nicht ist.
  Das Dashboard rechnet selbst nach — eine automatische Prüfung, kein Mensch
  muss jede Zahl kontrollieren
- Anfragen: Ein Durchlauf sind ~5 Anfragen (eine pro Werkzeug plus Antwort).
  Man sieht eine Zahl — dahinter stecken fünf Gespräche mit einem Modell
- Die Pointe: Nein! Aufgaben mit genau einer richtigen Antwort erledigt ein
  normales Programm fehlerfrei und kostenlos. KI lohnt sich dort, wo Sprache,
  Urteil und Unschärfe ins Spiel kommen
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
