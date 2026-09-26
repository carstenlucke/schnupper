---
routeAlias: demo-agent-party
rubrik: Agent Party
titel: Wenn KI-Agenten miteinander reden
untertitel: Eine Gesprächsrunde, in der an jedem Platz eine KI sitzt
---

<AgentRunde />

<!--
- Worum es geht: Nicht wir reden mit der KI — die KIs reden miteinander
- Jeder Agent ist ein Sprachmodell mit einer Rolle; alle bekommen dasselbe
  Thema und sprechen reihum, einer nach dem anderen
- Jeder hört, was vorher gesagt wurde, und reagiert darauf — so entsteht
  ein Gespräch, das niemand vorher geschrieben hat
- Überleitung: "Klingt nach Spielerei? Wofür man so eine Runde wirklich
  brauchen kann, zeigt ein Fundstück von LinkedIn …"
-->

---
rubrik: Agent Party
titel: 'Wofür das gut ist: ein Vorstellungsgespräch proben'
routeAlias: agent-party-fundstueck
---

<div class="thm-cols thm-cols-2-3">
  <div class="thm-stack motiv-post">
    <SocialPost autor="Alex Wang" foto="/linkedin-alex-wang.jpg" zeile="Learn AI Together · I explain practical AI, real workflows …"
                datum="25.09.2026" bild="/linkedin-jobsuche-2026.jpg"
                bild-alt="Grafik „How I’d job hunt in 2026“: Old Way gegen New Way in fünf Schritten"
                reaktionen="1.023" kommentare="51">
      Nice visual - I’ve actually used most of these. […] YouTube is still one of my favorite ways to understand a role I’m unfamiliar with. … mehr
    </SocialPost>
    <div class="thm-note">Alex Wang auf LinkedIn, 25.09.2026 · Grafik: GenAI.works</div>
  </div>
  <div class="thm-stack">
    <div>
      <div class="motiv-kopf">
        <div class="thm-eyebrow">Jobsuche mit KI, Schritt 04: üben</div>
        <Abstecher to="agent-party-ki-gegen-ki">KI gegen KI?</Abstecher>
      </div>
      <img class="motiv-schritt" src="/linkedin-jobsuche-2026-practice.jpg" alt="Old Way: YouTube-Videos zu typischen Interviewfragen. New Way: Probeinterview mit einer KI, die nachfragt" />
    </div>
    <div class="thm-lead">Ein Probeinterview mit einer KI, die nachhakt — das bauen wir nach. Nur sitzt bei uns <strong>an allen drei Plätzen</strong> eine KI:</div>
    <CardGrid :cols="3">
      <Card icon="handshake" titel="Personalreferentin">Lebenslauf, Eignung, Soft Skills</Card>
      <Card icon="laptop" titel="Teamleiter IT">Hakt fachlich nach</Card>
      <Card icon="graduation-cap" icon-ton="grau" titel="Bewerberin">Macht Abitur, will dual studieren</Card>
    </CardGrid>
    <Callout icon="target"><strong>Die Stelle:</strong> duales Studium Wirtschaftsinformatik bei der Lahnblick Optronik GmbH in Wetzlar — ausgedacht.</Callout>
  </div>
</div>

<style>
.motiv-post { gap: 0; }
.motiv-post :deep(.sp) { flex: 1; }
.motiv-kopf {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1rem;
}
.motiv-schritt {
  width: 100%;
  border: 1px solid var(--border-default);
}
</style>

<!--
- Kein Gedankenspiel: Leute nutzen genau so etwas schon — hier der Beleg
- Fundstück von LinkedIn: Alex Wang, gut 1,1 Mio. Follower, teilt eine
  Grafik von GenAI.works — Jobsuche 2026, fünf Schritte, links der alte Weg,
  rechts der mit KI
- Frage in die Runde: "Wer hat schon mal ein Vorstellungsgespräch geführt?
  Wie habt ihr euch vorbereitet?"
- Schritt 04: Früher YouTube-Videos mit typischen Fragen, heute ein
  Probeinterview mit einer KI, die nachfragt (Yoodli)
- Genau das bauen wir mit Agent Party selbst, ohne fertige App: drei
  Rollenbeschreibungen in normalem Deutsch
- Die Stelle ist erfunden, aber realistisch: duales Studium mit StudiumPlus —
  also genau das, worauf ihr euch in ein, zwei Jahren bewerben könntet
- Alex Wang schreibt im Post auch: "Die letzten Anpassungen mache ich
  selbst — damit es noch nach mir klingt"
- Falls jemand fragt, ob KI bei Bewerbungen nicht fragwürdig ist: "KI gegen
  KI?" oben rechts springt auf die Zusatzfolie dazu
- Überleitung: "Wie so eine Runde entsteht, zeige ich euch jetzt."
-->

---
rubrik: Agent Party
titel: So läuft die Party
class: text-xl
---

<div class="thm-center thm-gruppe">
<div class="thm-flow">
  <Card icon="user-pen" titel="Rolle beschreiben" kompakt>Ein Satz genügt — die KI arbeitet das Profil aus</Card>
  <FlowArrow />
  <Card icon="users" titel="Besetzung wählen" kompakt>Drei Profile, Reihenfolge festlegen</Card>
  <FlowArrow />
  <Card icon="message-square" titel="Thema geben" kompakt>Eine Frage, über die man streiten kann</Card>
  <FlowArrow />
  <Card icon="messages-square" titel="Reihum diskutieren" tone="tint" kompakt>Beitrag für Beitrag, live</Card>
</div>

<Callout icon="megaphone"><strong>Ihr könnt jederzeit eingreifen:</strong> ein Zwischenruf, eine weitere Runde, ein Fazit zum Schluss.</Callout>
</div>

<style>
/* vier Karten nebeneinander: etwas kleiner als der Rest der Folie */
.thm-flow { font-size: 0.85em; }
</style>

<!--
- Den Ablauf einmal durchgehen, bevor die Klasse mitmacht
- Acht Profile sind mitgeliefert — eine Diskussionsrunde (Ökonomin,
  Technik-Optimist, Ethikerin, Praktiker, Advocatus Diaboli) und das
  Vorstellungsgespräch von eben; gleich schreiben wir eigene
- Zwischenruf: ist nur eine Zeile mehr im Verlauf, die beim nächsten Beitrag
  mitgeschickt wird — die KI hat kein Gedächtnis, sie bekommt jedes Mal das
  ganze Gespräch neu
-->

---
rubrik: Agent Party
titel: Ein Agent ist eine Textdatei
class: text-xl
---

<div class="thm-center thm-gruppe">
<div class="thm-flow">
  <Card icon="cog" icon-ton="grau" titel="Oben: die Technik" kompakt>
    Welches Modell, wie viel Nachdenken, welche Farbe.
    <div class="thm-sample">model: gpt-5.6-luna<br>thinking: low<br>farbe: hellblau</div>
  </Card>
  <FlowArrow />
  <Card icon="pen-line" titel="Darunter: die Rolle" tone="tint" kompakt>
    In ganz normalem Deutsch.
    <div class="thm-sample sprache">„Du bist Wirtschaftswissenschaftlerin und sitzt in dieser Runde als die Stimme, die nach Zahlen fragt …“</div>
  </Card>
</div>

<Callout icon="info"><strong>Dieser Text geht wörtlich an die KI</strong> — keine versteckte Zusatzanweisung, kein Code.</Callout>
</div>

<!--
- Im Dashboard ein Profil öffnen und zeigen: Das ist der ganze Agent
- Frontmatter = Technik, darunter = Rolle
- Wer die Beschreibung ändert, sieht das Verhalten sofort kippen
- Überleitung: "Und jetzt seid ihr dran."
-->

---
rubrik: Agent Party · Live-Demo
titel: Jetzt seid ihr dran!
class: text-xl
hideInToc: true
---

<div class="thm-center thm-gruppe">
<div class="thm-stack">
  <QuestionItem>Welche <strong>Rolle</strong> fehlt noch am Tisch? Beschreibt sie in einem Satz.</QuestionItem>
  <QuestionItem>Worüber soll die Runde <strong>streiten</strong>?</QuestionItem>
</div>

<CardGrid :cols="4">
  <Card icon="bot" icon-ton="gelb" center>Sollen Schulen KI verbieten?</Card>
  <Card icon="smartphone" icon-ton="gelb" center>Handys im Unterricht erlauben?</Card>
  <Card icon="book-open" icon-ton="gelb" center>Hausaufgaben abschaffen?</Card>
  <Card icon="vote" icon-ton="gelb" center>Wahlrecht ab 16?</Card>
</CardGrid>

<div class="thm-note">...oder euer eigenes Thema! Ruft rein — wir stimmen ab.</div>
</div>

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
class: text-xl
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
- Variante Vorstellungsgespräch (knüpft an „Wofür das gut ist“ an): Besetzung
  Personalreferentin, Teamleiter IT, Bewerberin — genau in dieser
  Reihenfolge; Thema "Vorstellungsgespräch: Duales Studium
  Wirtschaftsinformatik bei der Lahnblick Optronik GmbH"; Einstiegsfrage
  "Erzählen Sie doch mal: Warum ein duales Studium – und warum bei uns?";
  2 Runden
- Hebel dafür: im Profil der Bewerberin "sagst du das ehrlich" durch "Du
  übertreibst gern, um gut dazustehen" ersetzen — der Teamleiter bohrt nach
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
  — sie hat eine Rolle. Übertragen: Chatbots in Apps, Kundenservice, Social
  Media — auch dort hat jemand eine Rolle geschrieben, die ihr nicht seht
- Waren das Agenten? Eher nicht: Die Profile haben bewusst KEINE Werkzeuge —
  sie können nur reden, nicht handeln. Rückbezug auf "Wofür ihr ChatGPT
  nutzt": Auch hier wurde nur geantwortet, getan hat niemand etwas. Das
  waren Chatbots mit einer Rolle. Ein Agent würde z. B. Quellen
  nachschlagen oder ein Protokoll schreiben
- Beispiele für den Reality Check merken: überzeugend klingende, aber
  erfundene Zahlen (Halluzination); lokales Modell in LM Studio statt Cloud
  (Datenschutz)
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

---
rubrik: Agent Party · Zusatzfolie
titel: KI gegen KI?
routeAlias: agent-party-ki-gegen-ki
zusatz: agent-party-fundstueck
hideInToc: true
---

<div class="thm-lead">In unserem Vorstellungsgespräch sitzt <strong>an allen drei Plätzen</strong> eine KI. Bei echten Bewerbungen passiert gerade etwas Ähnliches:</div>

<div class="thm-cols thm-cols-3-2">
  <div class="thm-center"><div class="thm-flow">
    <Card icon="pen-line" icon-ton="grau" titel="Bewerbende">KI schreibt die Bewerbung, für jede Stelle passend gemacht</Card>
    <FlowArrow />
    <Card icon="file-text" icon-ton="grau" titel="Die Flut">Hunderte glatt polierte Lebensläufe, die alle ähnlich klingen</Card>
    <FlowArrow />
    <Card icon="filter" icon-ton="rot" titel="Arbeitgeber">KI sortiert aus, was KI geschrieben hat</Card>
  </div></div>
  <div class="thm-stack reflex-kommentar">
    <SocialPost kommentar autor="Kal Makwana" zeile="CEO @ ApplyPal & ReferPool" datum="25.09.2026" reaktionen="9">
      Using AI on one side to beat the AI on the other side is a fools errand. Tools like these is exactly why recruitment is broken. […] more companies are now using their existing employees network instead of sifting through 800+ AI polished CVs.
    </SocialPost>
    <div class="thm-note">Kommentar zum Beitrag von Alex Wang, LinkedIn, 25.09.2026</div>
  </div>
</div>

<Callout icon="messages-square" class="mt-4"><strong>Zum Üben ja, als Ersatz nein.</strong> Die KI darf euch Fragen stellen — antworten müsst ihr im echten Gespräch selbst.</Callout>

<div class="reflex-zurueck"><Abstecher to="agent-party-fundstueck" zurueck>Zurück zum Fundstück</Abstecher></div>

<style>
.reflex-kommentar { gap: 0; justify-content: center; }
.reflex-zurueck { margin-top: 0.8rem; }
</style>

<!--
- Zusatzfolie, nicht im Folienverlauf: erreichbar über "KI gegen KI?" auf
  "Wofür das gut ist", für die Frage, ob KI bei Bewerbungen nicht
  gesellschaftlich fragwürdig ist. Pfeiltasten oder "Zurück zum Fundstück"
  führen wieder in den Verlauf
- Die Grafik zeigt fünf Schritte, in denen KI hilft. Zu Ende gedacht heißt
  das: KI schreibt, KI liest — und kein Mensch lernt den anderen kennen
- In unserer Demo ist das sogar wörtlich so: Auch die Bewerberin ist eine KI.
  Frage in die Runde: "Hat sich da eigentlich noch jemand beworben?"
- Kal Makwana: "Mit KI auf der einen Seite die KI auf der anderen Seite
  schlagen zu wollen, ist ein aussichtsloses Unterfangen." Firmen weichen
  deshalb auf Empfehlungen aus dem eigenen Team aus. Einordnen: Kal Makwana
  leitet selbst eine Plattform für solche Empfehlungen — auch ein Kommentar hat
  eine Rolle, wie unsere Profile
- Die Personalabteilung ist nicht der Gegner: Wer 800 Bewerbungen auf eine
  Stelle bekommt, greift zur Maschine. Das Wettrüsten hat zwei Seiten
- Der Unterschied: Üben macht euch besser, im echten Gespräch sitzt ihr
  selbst. Ein generiertes Anschreiben ersetzt euch — und klingt wie alle
  anderen. Alex Wang schreibt es im Post selbst: "Die letzten Anpassungen
  mache ich von Hand — damit es noch nach mir klingt"
-->
