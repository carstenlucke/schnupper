---
routeAlias: demo-ship-it
rubrik: Ship It!
titel: Fünf Agenten, ein Produktlaunch
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
- Jeden Agenten kurz vorstellen, Rolle erklären
- "Die arbeiten wie Abteilungen in einem Unternehmen"
- Website-Agent ist besonders: baut etwas, das man im Browser öffnen kann
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
- Zeigen: Abhängigkeiten wie in einem echten Projekt
- Zielgruppe + Kalkulation starten parallel (sofort)
- Marketing wartet auf Zielgruppe
- Social Media wartet auf Marketing
- Website wartet auf alle
- "Jetzt starten wir! Dashboard öffnen..."
-->

---
rubrik: Ship It! · Live-Demo
titel: Jetzt seid ihr dran!
class: text-l
hideInToc: true
---

<QuestionItem>Welches Produkt sollen unsere KI-Agenten auf den Markt bringen?</QuestionItem>

<div class="thm-lead mt-4">Das Einzige, was die Agenten von euch brauchen: <strong>eine Produktidee in ganz normalem Deutsch.</strong></div>

<div class="thm-center">
<CardGrid :cols="4">
  <Card icon="camera" icon-ton="gelb" center>Drohnen-Foto-Service für Events</Card>
  <Card icon="zap" icon-ton="gelb" center>Energy Drink für Klausurphasen</Card>
  <Card icon="book-open" icon-ton="gelb" center>App zum Tauschen von Schulbüchern</Card>
  <Card icon="headphones" icon-ton="gelb" center>KI-Kopfhörer, der Stimmung erkennt</Card>
</CardGrid>
</div>

<div class="thm-note">...oder eure eigene Idee! Ruft rein — wir stimmen ab.</div>

<!--
- Die 4 Starter-Ideen als Inspiration zeigen
- Schüler können eigene Ideen einbringen
- 2-3 Minuten Brainstorming, dann Abstimmung per Handzeichen
- Gewähltes Produkt in Ship It! eingeben (kurze Beschreibung tippen)
-->

---
layout: statement
rubrik: Ship It! · Live-Demo
titel: Los geht's!
zitat: false
hideInToc: true
---

Wechsel zum **Ship It! Dashboard**

<span class="st-note"><a href="http://localhost:8000" target="_blank">localhost:8000</a> im Browser öffnen</span>

<!--
- Browser wechseln, Dashboard zeigen
- Produkt eingeben
- Agenten nacheinander starten
- Zwischen den Ergebnissen: Vorhersage-Spiel (nächste Folien)
- Markdown-Files von 1-2 Agenten zeigen (z.B. Zielgruppe, Marketing)
- Hinweis: Die Agenten sind nicht programmiert, sondern in natürlicher Sprache definiert
- "Schaut mal: Das ist kein Code — das ist einfach Deutsch. So sagt man der KI, was sie tun soll."
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
- Übergang zur kritischen Bewertung
- Jede Frage einzeln durchgehen, Daumen hoch/runter
- Nachfragen: WARUM? Was genau stört euch?
- "Was hat überrascht?"
- "Was fehlt offensichtlich?"
- "Würde ein echtes Unternehmen das so verwenden?"
- Beispiele für den Reality Check merken: fragwürdige Zahlen in der
  Kalkulation (Halluzination), eure Produktidee ging an einen Cloud-Dienst
  (Datenschutz)
-->

---
rubrik: Ship It!
titel: Das war Ship It!
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>

<!--
- Noch Zeit? "Noch eine Demo" führt zur Übersicht
- Sonst weiter (→) zu "Was nehmen wir mit?"
-->
