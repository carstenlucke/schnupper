---
routeAlias: demo-agent-party
rubrik: Agent Party
titel: Ihr baut die Agenten selbst
---

<div class="thm-center">
<div class="thm-lead">Eine Diskussionsrunde aus KI-Agenten. <strong>Wer mitdiskutiert und wie</strong>, bestimmt ihr — mit einer Rollenbeschreibung in ganz normalem Deutsch.</div>

<CardGrid :cols="5" class="mt-4">
  <Card icon="coins" titel="Skeptische Ökonomin">Rechnet jede Idee auf Kosten und Nutzen herunter</Card>
  <Card icon="rocket" titel="Technik-Optimist">Sieht zuerst die Möglichkeiten</Card>
  <Card icon="scale" titel="Ethikerin">Fragt, wer profitiert und wer die Rechnung zahlt</Card>
  <Card icon="wrench" titel="Praktiker">Will wissen, wer es am Montag macht</Card>
  <Card icon="swords" titel="Advocatus Diaboli">Widerspricht grundsätzlich der Mehrheit</Card>
</CardGrid>
</div>

<!--
- Fünf Profile sind mitgeliefert — gleich schreiben wir eigene
- "Ein KI-Agent ist nichts Magisches: eine Rollenbeschreibung plus ein
  Sprachmodell."
- Wer die Beschreibung ändert, sieht das Verhalten sofort kippen
-->

---
rubrik: Agent Party
titel: Ein Agent ist eine Textdatei
class: text-l
---

<div class="thm-center"><div class="thm-flow">
  <Card icon="cog" icon-ton="grau" titel="Oben: die Technik">
    Welches Modell, wie viel Nachdenken, welche Farbe.
    <div class="thm-sample">model: gpt-5.6-luna<br>thinking: low<br>farbe: hellblau</div>
  </Card>
  <FlowArrow />
  <Card icon="pen-line" titel="Darunter: die Rolle" tone="tint">
    In ganz normalem Deutsch.
    <div class="thm-sample sprache">„Du bist Wirtschaftswissenschaftlerin und sitzt in dieser Runde als die Stimme, die nach Zahlen fragt …“</div>
  </Card>
</div></div>

<Callout icon="info" class="mt-4"><strong>Dieser Text geht wörtlich an die KI</strong> — keine versteckte Zusatzanweisung, kein Code.</Callout>

<!--
- Im Dashboard ein Profil öffnen und zeigen: Das ist der ganze Agent
- Frontmatter = Technik, darunter = Rolle
- Überleitung: "Und so eine Datei schreibt ihr gleich selbst."
-->

---
rubrik: Agent Party
titel: So läuft die Party
class: text-l
---

<div class="thm-center"><div class="thm-flow">
  <Card icon="user-pen" titel="Rolle beschreiben">Ein Satz genügt — die KI arbeitet das Profil aus</Card>
  <FlowArrow />
  <Card icon="users" titel="Besetzung wählen">Drei Profile, Reihenfolge festlegen</Card>
  <FlowArrow />
  <Card icon="message-square" titel="Thema geben">Eine Frage, über die man streiten kann</Card>
  <FlowArrow />
  <Card icon="messages-square" titel="Reihum diskutieren" tone="tint">Beitrag für Beitrag, live</Card>
</div></div>

<Callout icon="megaphone" class="mt-4"><strong>Ihr könnt jederzeit eingreifen:</strong> ein Zwischenruf, eine weitere Runde, ein Fazit zum Schluss.</Callout>

<!--
- Den Ablauf einmal durchgehen, bevor die Klasse mitmacht
- Zwischenruf: ist nur eine Zeile mehr im Verlauf, die beim nächsten Beitrag
  mitgeschickt wird — die KI hat kein Gedächtnis, sie bekommt jedes Mal das
  ganze Gespräch neu
-->

---
rubrik: Agent Party · Live-Demo
titel: Jetzt seid ihr dran!
class: text-l
hideInToc: true
---

<div class="thm-stack">
  <QuestionItem>Welche <strong>Rolle</strong> fehlt noch am Tisch? Beschreibt sie in einem Satz.</QuestionItem>
  <QuestionItem>Worüber soll die Runde <strong>streiten</strong>?</QuestionItem>
</div>

<div class="thm-center">
<CardGrid :cols="4">
  <Card icon="bot" icon-ton="gelb" center>Sollen Schulen KI verbieten?</Card>
  <Card icon="smartphone" icon-ton="gelb" center>Handys im Unterricht erlauben?</Card>
  <Card icon="book-open" icon-ton="gelb" center>Hausaufgaben abschaffen?</Card>
  <Card icon="vote" icon-ton="gelb" center>Wahlrecht ab 16?</Card>
</CardGrid>
</div>

<div class="thm-note">...oder euer eigenes Thema! Ruft rein — wir stimmen ab.</div>

<!--
- Erst die Rolle: Vorschläge sammeln, einen auswählen, Satz eintippen,
  "Ausarbeiten lassen"
- Dann das Thema: Starter zeigen, eigene Ideen zulassen, Handzeichen
- Besetzung: das neue Profil plus zwei mitgelieferte
-->

---
layout: statement
rubrik: Agent Party · Live-Demo
titel: Los geht's!
zitat: false
hideInToc: true
---

Wechsel zur **Agent Party**

<span class="st-note"><a href="http://localhost:8100" target="_blank">localhost:8100</a> im Browser öffnen</span>

<!--
- Neues Profil ausarbeiten lassen, Entwurf zeigen, ein Wort ändern, speichern
- Besetzung wählen, Thema eintragen, Party starten
- Denkbereich aufklappen: "Was das Modell gedacht hat"
- Zwischenruf einwerfen, z. B. "Bleibt konkret: Nennt Zahlen."
- Höhepunkt: einen Satz in einem Profil ändern, dieselbe Party neu starten —
  die Diskussion dreht sich
- Ggf. zum Schluss "Fazit erstellen"
-->

---
rubrik: Agent Party · Bewertung
titel: Wie echt war die Diskussion?
hideInToc: true
---

<div class="thm-stack">
  <QuestionItem>Wer hat euch am meisten <strong>überzeugt</strong> — und warum?</QuestionItem>
  <QuestionItem>Ein Satz im Profil geändert — <strong>was hat sich gedreht</strong>?</QuestionItem>
  <QuestionItem>Wer hat bestimmt, was die KI <strong>„meint“</strong>?</QuestionItem>
  <QuestionItem>Ehrlich: Waren das überhaupt <strong>Agenten</strong>?</QuestionItem>
</div>

<!--
- Überzeugung: Die KI klingt souverän, egal ob das Argument trägt
- Profiländerung: gleiche Frage, gleiche Besetzung, ein Satz anders — und
  die Runde kommt woanders an
- Wer bestimmt die Meinung? Wer die Rolle schreibt. Die KI hat keine eigene
- Waren das Agenten? Eher nicht: Die Profile haben bewusst KEINE Werkzeuge —
  sie können nur reden, nicht handeln. Rückbezug auf "Reden vs. Handeln":
  Das waren Chatbots mit einer Rolle. Ein Agent würde z. B. Quellen
  nachschlagen oder ein Protokoll schreiben
- Beispiele für den Reality Check merken: überzeugend klingende, aber
  erfundene Zahlen (Halluzination); lokales Modell in LM Studio statt Cloud
  (Datenschutz)
-->

---
layout: statement
rubrik: Agent Party · Bewertung
zitat: false
hideInToc: true
---

Die KI hat keine Meinung — sie hat eine **Rolle**.

<span class="st-note">Und die schreibt jemand. Wer die Rolle schreibt, lenkt die Diskussion.</span>

<!--
- Kurz wirken lassen
- Übertragen: Chatbots in Apps, Kundenservice, Social Media — auch dort hat
  jemand eine Rolle geschrieben, die ihr nicht seht
- Deshalb: Bei KI-Antworten immer fragen, wer sie so eingestellt hat
-->

---
rubrik: Agent Party
titel: Das war Agent Party
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>

<!--
- Noch Zeit? "Noch eine Demo" führt zur Übersicht
- Sonst weiter (→) zu "Was nehmen wir mit?"
-->
