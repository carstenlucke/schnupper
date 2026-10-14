---
routeAlias: demo-agent-party
rubrik: Agent Party
titel: Wenn KI-Agenten miteinander reden
untertitel: Eine Gesprächsrunde, in der an jedem Platz eine KI sitzt
---

<AgentRunde />

<!--
In dieser Demo redet nicht ihr mit der KI, sondern die KIs reden
miteinander. Jeder Agent ist ein Sprachmodell mit einer eigenen Rolle. Alle
bekommen dasselbe Thema und sprechen reihum, einer nach dem anderen.

Jeder hört, was vorher gesagt wurde, und reagiert darauf. So entsteht ein
Gespräch, das niemand vorher geschrieben hat.
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
    <div class="thm-note"><a href="https://www.linkedin.com/posts/alexwang2911_nice-visual-ive-actually-used-most-of-share-7509108760267800577-tFci/" target="_blank">Alex Wang auf LinkedIn, 25.09.2026</a> · Grafik: GenAI.works</div>
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
Eine Runde aus KIs ist kein Gedankenspiel, so etwas nutzen Leute schon
heute. Das Fundstück stammt von LinkedIn: Alex Wang, der dort gut 1,1
Millionen Follower hat, teilt eine Grafik von GenAI.works zur Jobsuche 2026.
Sie zeigt fünf Schritte, links jeweils den alten Weg, rechts den mit KI.

In Schritt 04 geht es ums Üben. Früher hat man sich YouTube-Videos mit
typischen Interviewfragen angesehen, heute führt man ein Probeinterview mit
einer KI, die nachfragt (etwa mit Yoodli). Genau das bauen wir mit Agent
Party nach, nur ohne fertige App: Es sind drei Rollenbeschreibungen in
normalem Deutsch.

Die Stelle ist erfunden, aber realistisch. Ein duales Studium mit
StudiumPlus ist genau das, worauf ihr euch in ein, zwei Jahren bewerben
könntet.

Alex Wang schreibt im Post übrigens auch, dass er die letzten Anpassungen
selbst macht, damit es noch nach ihm klingt.

Ob KI bei Bewerbungen nicht fragwürdig ist, behandelt eine Zusatzfolie. Ihr
erreicht sie über „KI gegen KI?“ oben rechts.
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
Acht Profile sind schon mitgeliefert. Fünf davon bilden eine
Diskussionsrunde: Ökonomin, Technik-Optimist, Ethikerin, Praktiker und
Advocatus Diaboli. Die übrigen drei spielen das Vorstellungsgespräch von
eben. Dazu kommen eigene Profile, die ihr selbst schreibt.

Ein Zwischenruf ist technisch nur eine Zeile mehr im Verlauf, die beim
nächsten Beitrag mitgeschickt wird. Die KI hat nämlich kein Gedächtnis: Sie
bekommt jedes Mal das ganze Gespräch neu.
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
Ein Profil ist eine einzige Textdatei, und mehr ist der ganze Agent nicht.
Der Kopf der Datei (das sogenannte Frontmatter) legt die Technik fest,
darunter steht die Rolle. Wer die Beschreibung ändert, sieht das Verhalten
sofort kippen.
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
Eine neue Rolle beginnt mit einem einzigen Satz, den Rest des Profils
arbeitet die KI aus. Die Runde besteht dann aus dem neuen Profil und zwei
mitgelieferten.
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
Zu jedem Beitrag lässt sich aufklappen, was das Modell vorher gedacht hat.
Ein Zwischenruf wie „Bleibt konkret: Nennt Zahlen.“ lenkt die Runde
spürbar um.

Am deutlichsten wird es, wenn man einen einzigen Satz in einem Profil ändert
und dieselbe Party neu startet: Die Diskussion dreht sich. Im
Vorstellungsgespräch genügt es, im Profil der Bewerberin „sagst du das
ehrlich“ durch „Du übertreibst gern, um gut dazustehen“ zu ersetzen. Dann
bohrt der Teamleiter nach.
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
Die KI klingt souverän, ganz egal, ob das Argument trägt. Wie überzeugend
ein Beitrag wirkt, sagt also wenig darüber, ob er stimmt.

Gleiche Frage, gleiche Besetzung, nur ein Satz im Profil anders, und die
Runde kommt woanders an. Die Meinung bestimmt, wer die Rolle schreibt. Die
KI hat keine eigene Meinung, sie hat eine Rolle. Das gilt auch außerhalb der
Demo: Bei Chatbots in Apps, im Kundenservice oder in sozialen Medien hat
ebenfalls jemand eine Rolle geschrieben, die ihr nicht seht.

Waren das überhaupt Agenten? Eher nicht. Die Profile haben bewusst keine
Werkzeuge, sie können nur reden, nicht handeln. Wie bei „Wofür ihr ChatGPT
nutzt“ wurde auch hier nur geantwortet, getan hat niemand etwas. Es waren
Chatbots mit einer Rolle. Ein Agent würde zum Beispiel Quellen nachschlagen
oder ein Protokoll schreiben.

Zwei Beobachtungen tauchen im Rückblick am Ende wieder auf: Zahlen, die
überzeugend klingen, aber erfunden sind (Halluzination), und die
Möglichkeit, ein Modell lokal in LM Studio laufen zu lassen statt in der
Cloud (Datenschutz).
-->

---
rubrik: Agent Party
titel: Das war Agent Party
hideInToc: true
---

<div class="thm-center">
  <DemoEnde />
</div>

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
Diese Zusatzfolie liegt außerhalb des Folienverlaufs. Sie geht der Frage
nach, ob KI bei Bewerbungen nicht gesellschaftlich fragwürdig ist. Mit den
Pfeiltasten oder über „Zurück zum Fundstück“ geht es wieder in den Verlauf.

Die Grafik zeigt fünf Schritte, in denen KI bei der Jobsuche hilft. Zu Ende
gedacht heißt das: KI schreibt, KI liest, und kein Mensch lernt den anderen
kennen. In unserer Demo ist das sogar wörtlich so, denn auch die Bewerberin
ist eine KI. Hat sich da eigentlich noch jemand beworben?

Kal Makwana schreibt dazu sinngemäß: „Mit KI auf der einen Seite die KI auf
der anderen Seite schlagen zu wollen, ist ein aussichtsloses Unterfangen.“
Firmen weichen deshalb auf Empfehlungen aus dem eigenen Team aus. Allerdings
leitet Kal Makwana selbst eine Plattform für solche Empfehlungen. Auch ein
Kommentar hat also eine Rolle, genau wie unsere Profile.

Die Personalabteilung ist dabei nicht der Gegner. Wer 800 Bewerbungen auf
eine Stelle bekommt, greift zur Maschine. Das Wettrüsten hat zwei Seiten.

Der Unterschied liegt woanders: Üben macht euch besser, und im echten
Gespräch sitzt ihr selbst. Ein generiertes Anschreiben dagegen ersetzt euch
und klingt wie alle anderen. Alex Wang schreibt es im Post selbst: Die
letzten Anpassungen macht er von Hand, damit es noch nach ihm klingt.
-->
