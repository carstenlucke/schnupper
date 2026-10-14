---
routeAlias: demo-ship-it
rubrik: Ship It!
titel: Fünf Agenten, ein Produktlaunch
class: text-l
---

<div class="thm-center">
<div class="si-lead">
  <img src="/ship-it-logo.png" alt="Ship It!">
  <p><strong>Ship It!</strong> ist ein Dashboard, in dem <strong>5 KI-Agenten</strong> zusammenarbeiten, um ein Produkt auf den Markt zu bringen — Zielgruppenanalyse, Marketing, Social Media, Preiskalkulation und sogar eine fertige Website.</p>
</div>

<CardGrid :cols="5">
  <Card icon="users" titel="Zielgruppen-Analyst">Wer kauft das Produkt? Personas erstellen</Card>
  <Card icon="megaphone" titel="Marketing-Experte">Name, Slogan, Werbetexte entwickeln</Card>
  <Card icon="hash" titel="Social-Media-Manager">Posts für Instagram, LinkedIn, TikTok</Card>
  <Card icon="calculator" titel="Controller">Preiskalkulation und Preisstrategie</Card>
  <Card icon="code" titel="Web-Entwickler">Produkt-Website mit HTML, CSS, JS</Card>
</CardGrid>
</div>

<style>
.si-lead {
  display: flex;
  align-items: center;
  gap: 1.4rem;
  margin-bottom: 1rem;
}
.si-lead img { height: 4.2rem; flex: none; }
.si-lead p { margin: 0; line-height: var(--lh-snug); }
</style>

<!--
Die fünf Agenten arbeiten wie Abteilungen in einem Unternehmen: Jeder hat
eine eigene Rolle und liefert seinen Teil zum Produktlaunch, von der
Zielgruppe über Werbetexte und Posts bis zum Preis.

Der Web-Entwickler fällt aus der Reihe. Er schreibt nicht nur Texte,
sondern baut etwas, das man im Browser öffnen kann: eine fertige Website
für das Produkt.
-->

---
rubrik: Ship It!
titel: Wer wartet auf wen?
untertitel: Manche Agenten brauchen die Ergebnisse anderer, bevor sie starten können.
---

<div class="abh-rahmen">
  <AgentAbhaengigkeiten />
</div>

<Callout icon="circle-play"><strong>Zielgruppe</strong> und <strong>Kalkulation</strong> starten sofort — sie brauchen nur die Produktbeschreibung.</Callout>

<style>
.abh-rahmen {
  flex: 1;
  min-height: 0;
  display: flex;
  justify-content: center;
  padding: 0.2rem 0 0.8rem;
}
</style>

<!--
Wie in einem echten Projekt hängen die Aufgaben voneinander ab. Zielgruppe
und Kalkulation brauchen nur die Produktbeschreibung und können sofort und
gleichzeitig loslegen.

Alle anderen warten auf Ergebnisse: Das Marketing braucht die Zielgruppe,
Social Media braucht das Marketing. Die Website kommt erst, wenn
Zielgruppe, Marketing und Kalkulation fertig sind, denn sie setzt deren
Ergebnisse zusammen.
-->

---
rubrik: Ship It! · Live-Demo
titel: Jetzt seid ihr dran!
class: text-xl
hideInToc: true
---

<div class="thm-center thm-gruppe">
<QuestionItem>Welches Produkt sollen unsere KI-Agenten auf den Markt bringen?</QuestionItem>

<div class="thm-lead">Das Einzige, was die Agenten von euch brauchen: <strong>eine Produktidee in ganz normalem Deutsch.</strong></div>

<CardGrid :cols="4">
  <Card icon="camera" icon-ton="gelb" center>Drohnen-Foto-Service für Events</Card>
  <Card icon="zap" icon-ton="gelb" center>Energy Drink für Klausurphasen</Card>
  <Card icon="book-open" icon-ton="gelb" center>App zum Tauschen von Schulbüchern</Card>
  <Card icon="headphones" icon-ton="gelb" center>KI-Kopfhörer, der Stimmung erkennt</Card>
</CardGrid>

<div class="thm-note">...oder eure eigene Idee! Ruft rein — wir stimmen ab.</div>
</div>

<!--
Die vier Ideen sind nur Anregungen, jede andere Produktidee funktioniert
genauso. Mehr als eine kurze Beschreibung in ganz normalem Deutsch
brauchen die Agenten nicht: Alles Weitere, von der Zielgruppe bis zur
Website, erarbeiten sie selbst.
-->

---
layout: statement
rubrik: Ship It! · Live-Demo
titel: Los geht's!
zitat: false
class: text-xl
hideInToc: true
---

Wechsel zum **Ship It! Dashboard**

<span class="st-note"><a href="http://localhost:8000" target="_blank">localhost:8000</a> im Browser öffnen</span>

<!--
Im Dashboard laufen die Agenten nacheinander los, und ihre Ergebnisse
erscheinen nach und nach.

Bemerkenswert ist, wie die Agenten selbst aussehen: Sie sind nicht
programmiert, sondern in natürlicher Sprache beschrieben. Jeder Agent ist
eine Markdown-Datei. Oben stehen das Modell und die Werkzeuge, darunter
die Aufgabe in ganz normalem Deutsch. Das ist kein Code, so sagt man der
KI, was sie tun soll.
-->

---
rubrik: Ship It! · Bewertung
titel: Wie gut war die KI?
untertitel: Zeit für eine ehrliche Bewertung — Daumen hoch oder runter?
hideInToc: true
---

<div class="thm-stack">
  <QuestionItem>Würdet ihr diesen <strong>Instagram-Post</strong> liken?</QuestionItem>
  <QuestionItem>Ist die <strong>Preiskalkulation</strong> realistisch?</QuestionItem>
  <QuestionItem>Spricht euch die <strong>Website</strong> an?</QuestionItem>
  <QuestionItem>Welcher Agent hat <strong>am besten</strong> gearbeitet?</QuestionItem>
</div>

<!--
Die Ergebnisse sehen auf den ersten Blick beeindruckend aus. Ein
kritischer Blick lohnt sich trotzdem, und das Daumen hoch oder runter ist
erst der Anfang. Spannender ist das Warum: Was genau überzeugt, was stört?
Was hat überrascht, was fehlt offensichtlich? Und würde ein echtes
Unternehmen das so verwenden?

Zwei Dinge fallen dabei oft auf. Die Zahlen in der Kalkulation klingen
plausibel, sind aber teils fragwürdig, denn die KI hat sie sich
ausgedacht. Das nennt man Halluzination. Außerdem ging eure Produktidee
an einen Cloud-Dienst, und damit stellt sich die Frage nach dem
Datenschutz.
-->

---
rubrik: Ship It!
titel: Das war Ship It!
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>

