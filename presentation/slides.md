---
theme: ./theme-thm
title: 'Digitalisierung und KI'
titleTemplate: '%s — Schnuppervorlesung'
author: 'Prof. Dr. Carsten Lucke'
veranstaltung: Schnuppervorlesung · StudiumPlus
dozent: Prof. Dr. Carsten Lucke
info: |
  Schnuppervorlesung — Technische Hochschule Mittelhessen
  Prof. Dr. Carsten Lucke
transition: fade
colorSchema: light
drawings:
  persist: false
layout: cover
rubrik: Schnuppervorlesung · Duales Studium
---

# Digitalisierung und KI

<div class="cover-sub">Was Maschinen schon können</div>

<div class="cover-meta">

Prof. Dr. Carsten Lucke

</div>

<style>
.cover-sub {
  margin-top: 0.9rem;
  font-size: 1.35rem;
  color: var(--thm-grey-100);
}
</style>

<!--
- Willkommen, kurze Vorstellung
- Thema: KI in der Praxis, nicht nur Theorie
- Am Ende: Live-Demo, bei der IHR das Produkt bestimmt
-->

---
layout: question
titel: Kurze Umfrage
hideInToc: true
---

Wer von euch hat schon mal **ChatGPT, Gemini oder Copilot** benutzt?

<!--
- Hände hoch! (Erwartung: fast alle)
- Kurze Rufrunde: Wofür nutzt ihr das?
- Typische Antworten: Hausaufgaben, Texte schreiben, Fragen beantworten, Übersetzen
- "Spannend. Und genau da setzen wir heute an."
-->

---
rubrik: Einstieg
titel: Digitalisierung und KI — wie hängt das zusammen?
class: text-l
---

<div class="thm-center"><div class="thm-flow">
  <Card icon="database" icon-ton="grau" titel="Digitalisierung">
    <p><strong>Sammeln und Speichern</strong></p>
    <p>Aus Aktenordnern wurden Datenbanken, aus Briefen wurden E&#8209;Mails, aus Papier wurden PDFs.</p>
  </Card>
  <FlowArrow />
  <Card icon="brain" titel="Künstliche Intelligenz" tone="tint">
    <p><strong>Verstehen und Nutzen</strong></p>
    <p>KI zieht Schlüsse aus den digitalisierten Daten — und handelt eigenständig.</p>
  </Card>
</div></div>

<Callout class="mt-4"><strong>Ohne Digitalisierung hätte KI kein Futter.</strong> Die Digitalisierung hat die Welt für Maschinen lesbar gemacht — KI ist die Intelligenzschicht, die jetzt darauf aufsetzt.</Callout>

<!--
- Digitalisierung ist die Infrastruktur, KI die Intelligenz
- Passive Digitalisierung: Daten liegen nur herum (Excel, PDFs)
- Aktive Digitalisierung: Daten ARBEITEN für uns
- "KI ohne Digitalisierung wäre ein Gehirn ohne Augen und Ohren"
- "Und ihr nutzt das längst, ohne darüber nachzudenken..."
-->

---
rubrik: Einstieg
titel: KI ist schon überall
class: text-l
---

<div class="thm-lead">Ihr nutzt täglich KI — oft ohne es zu merken:</div>

<div class="thm-center">
<CardGrid :cols="2">
  <Card icon="music" titel="Spotify & YouTube" kompakt>
    Empfehlungen basierend auf eurem Verhalten — das ist KI
  </Card>
  <Card icon="smartphone" titel="TikTok & Instagram" kompakt>
    Der Algorithmus entscheidet, was ihr seht — das ist KI
  </Card>
  <Card icon="languages" titel="DeepL & Google Translate" kompakt>
    Übersetzungen in Echtzeit — das ist KI
  </Card>
  <Card icon="message-square" titel="ChatGPT & Co." kompakt>
    Texte schreiben, Fragen beantworten — und jetzt: auch <strong>handeln</strong>
  </Card>
</CardGrid>
</div>

<!--
- Bezug zur Lebenswelt der Schüler
- KI ist kein Zukunftsthema — es ist Gegenwart
- Die Frage ist nicht OB KI kommt, sondern wie wir damit umgehen
- Überleitung: "Und genau beim letzten Punkt wird es jetzt spannend..."
-->

---
rubrik: Einstieg
titel: 'Die große Veränderung: Vom Code zur Sprache'
class: text-l
---

<div class="thm-center"><div class="thm-flow">
  <Card icon="code" icon-ton="grau" titel="Früher">
    Um mit digitalen Daten zu arbeiten, brauchte man <strong>Programmiersprachen</strong>.
    <div class="thm-sample">SELECT * FROM kunden<br>WHERE alter &gt; 18</div>
  </Card>
  <FlowArrow />
  <Card icon="message-square" titel="Heute" tone="tint">
    LLMs erlauben es, mit Daten und Systemen in <strong>natürlicher Sprache</strong> zu arbeiten.
    <div class="thm-sample sprache">„Zeig mir alle Kunden über 18 Jahre“</div>
  </Card>
</div></div>

<Callout icon="rocket" class="mt-4"><strong>Genau das werden wir gleich sehen:</strong> Unsere KI-Agenten bekommen ihre Aufträge in ganz normalem Deutsch — kein Code, keine Programmierung.</Callout>

<!--
- DAS ist der Paradigmenwechsel den LLMs gebracht haben
- Früher: Nur wer programmieren konnte, konnte digitale Systeme steuern
- Heute: Natürliche Sprache reicht — LLMs sind der "Dolmetscher"
- Bezug zu Ship It!: Die Agenten verstehen deutsche Aufträge
- "Aber es gibt noch ein Problem..."
-->

---
layout: agenda
punkte:
  - Vom Chatbot zum KI-Agenten
  - Ship It! — fünf Agenten live
  - Was nehmen wir mit?
icons: [bot, rocket, target]
aktiv: 1
---

<!--
- Jetzt: Was ist der Unterschied?
- Einfach erklärt, ohne Technik-Jargon
-->

---
layout: question
titel: Reden vs. Handeln
hideInToc: true
---

ChatGPT kann mit euch **reden**.

Aber kann es auch **handeln**?

<!--
- Provokante Frage
- ChatGPT schreibt Texte, beantwortet Fragen — aber TUT es etwas?
- Es ist wie ein Gehirn im Glas: Es kann denken und reden, aber es hat keine Hände
- "Genau das schauen wir uns heute an."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Was kann ChatGPT?
class: text-l
---

<div class="thm-center">
<CardGrid :cols="2">
  <Card icon="pen-line" titel="Texte schreiben" kompakt>
    Aufsätze, E-Mails, Zusammenfassungen, Gedichte...
  </Card>
  <Card icon="messages-square" titel="Fragen beantworten" kompakt>
    Erklärungen, Definitionen, Tipps und Ratschläge
  </Card>
  <Card icon="languages" titel="Übersetzen" kompakt>
    Zwischen Sprachen übersetzen, Texte umformulieren
  </Card>
  <Card icon="lightbulb" titel="Ideen entwickeln" kompakt>
    Brainstorming, kreative Vorschläge, Konzepte
  </Card>
</CardGrid>
</div>

<!--
- Das kennen die Schüler bereits
- Kurz abhaken, nicht zu lange drauf verweilen
- Überleitung: "Super. Aber jetzt kommt das Aber..."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Was kann ChatGPT nicht?
class: text-l
---

<div class="thm-center">
<CardGrid :cols="2">
  <Card icon="folder-open" icon-ton="rot" titel="Dateien erstellen" kompakt>
    Kann keine Dokumente, Tabellen oder Websites auf eurem Rechner anlegen
  </Card>
  <Card icon="cog" icon-ton="rot" titel="Aufgaben ausführen" kompakt>
    Kann nichts eigenständig erledigen — nur antworten, wenn ihr fragt
  </Card>
  <Card icon="plug" icon-ton="rot" titel="Mit Systemen arbeiten" kompakt>
    Kann nicht auf Datenbanken, APIs oder andere Programme zugreifen
  </Card>
  <Card icon="refresh-cw" icon-ton="rot" titel="Sich selbst prüfen" kompakt>
    Kann nicht testen, ob seine Antwort wirklich stimmt oder funktioniert
  </Card>
</CardGrid>
</div>

<!--
- Kernpunkt: ChatGPT ist "nur" ein Gesprächspartner
- Es WEISS viel, aber es KANN nichts tun
- "Stellt euch vor, ihr ruft einen Experten an..."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Der Unterschied
class: text-l
---

<div class="thm-center"><div class="thm-flow">
  <Card band="grau" icon="phone" titel="Chatbot">
    <div class="vs-kern">Ein Experte <strong>am Telefon</strong></div>
    Weiß alles, kann aber nichts anfassen. Ihr müsst alles selbst umsetzen.
  </Card>
  <FlowArrow text="vs." />
  <Card band="gruen" icon="user-cog" titel="KI-Agent">
    <div class="vs-kern">Ein Experte <strong>bei euch im Büro</strong></div>
    Weiß alles UND legt direkt los. Liest Dateien, schreibt Ergebnisse, nutzt Werkzeuge.
  </Card>
</div></div>

<style>
.vs-kern {
  font-size: 1.3rem;
  line-height: 1.3;
  color: var(--text-strong);
  margin: 0.2rem 0 0.8rem;
}
</style>

<!--
- Analogie ist der Schlüssel zum Verständnis
- Chatbot = passiver Berater, Agent = aktiver Macher
- "Und wie macht der Agent das? Dazu gibt es ein einfaches Prinzip..."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Wie arbeitet ein KI-Agent?
untertitel: 'Der Agent-Kreislauf: Denken, Handeln, Prüfen'
---

<div class="thm-center">
  <AgentKreislauf />
</div>

<Callout><strong>Wie ein guter Praktikant:</strong> Aufgabe lesen, Plan machen, umsetzen, prüfen, ob alles stimmt — und nachbessern, wenn nötig.</Callout>

<!--
- DAS ist der zentrale Unterschied: die Feedback-Schleife
- Ein Chatbot gibt EINE Antwort. Ein Agent arbeitet ITERATIV.
- Analogie Praktikant: Ihr gebt ihm eine Aufgabe, er arbeitet eigenständig
- "Und jetzt wird's richtig spannend: Was wenn MEHRERE Agenten zusammenarbeiten?"
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Warum Agenten gerade so gefragt sind
class: text-l
---

<div class="thm-center">
<CardGrid :cols="3">
  <Card icon="trending-up" titel="Von Assistenz zu Autonomie">
    Heute: „KI hilft mir beim Schreiben.“<br>Morgen: <strong>„KI erledigt den Prozess.“</strong>
  </Card>
  <Card icon="copy" titel="Skalierbarkeit">
    Ein Unternehmen kann <strong>100 digitale Agenten</strong> gleichzeitig arbeiten lassen — rund um die Uhr.
  </Card>
  <Card icon="refresh-cw" titel="Selbstkorrektur">
    Agenten <strong>prüfen ihre Ergebnisse</strong> und verbessern sich selbst — ohne dass jemand eingreifen muss.
  </Card>
</CardGrid>
</div>

<Callout icon="circle-play" class="mt-4"><strong>Genau das testen wir jetzt live:</strong> 5 Agenten, ein Produktlaunch — in Minuten statt Wochen.</Callout>

<!--
- Ausblick in die Arbeitswelt der Schüler
- Assistenz -> Autonomie: Der Shift der gerade passiert
- Skalierbarkeit: 100 Agenten für Marktforschung, Kundenservice, Buchhaltung
- Selbstkorrektur: Fehlertoleranz durch Iteration (wie beim Agent-Kreislauf)
- "Und jetzt schauen wir uns das in der Praxis an!"
-->

---
layout: agenda
punkte:
  - Vom Chatbot zum KI-Agenten
  - Ship It! — fünf Agenten live
  - Was nehmen wir mit?
icons: [bot, rocket, target]
aktiv: 2
---

<!--
- Jetzt: Ship It! — fünf Agenten bringen ein Produkt auf den Markt
-->

---
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
rubrik: Ship It! · Live-Demo
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
-->

---
rubrik: Ship It!
titel: 'Reality Check: Worauf muss man achten?'
class: text-l
---

<div class="thm-center">
<CardGrid :cols="2">
  <Card icon="coins" titel="Kosten" kompakt>
    KI arbeitet mit <strong>Tokens</strong> — das ist ihre Währung. Wer Agenten einsetzt, muss die Kosten im Blick behalten.
  </Card>
  <Card icon="clipboard-check" titel="Qualitätskontrolle" kompakt>
    Wenn alles manuell geprüft werden muss, wird <strong>der Mensch zum Engpass</strong> — man braucht automatische Prüfmechanismen.
  </Card>
  <Card icon="ghost" icon-ton="rot" titel="Halluzinationen" kompakt>
    KI (LLM) kann <strong>überzeugend falsche Dinge</strong> behaupten — erfundene Fakten, falsche Zahlen, nicht existierende Quellen.
  </Card>
  <Card icon="shield-check" icon-ton="grau" titel="Datenschutz" kompakt>
    Daten, die an KI-Dienste gesendet werden, <strong>verlassen das Unternehmen</strong>. Man muss prüfen, ob eine Verarbeitung in externen KI-Diensten zulässig ist.
  </Card>
</CardGrid>
</div>

<!--
- Kein Hype ohne Reality Check
- Kosten: GPT-4 ca. 100x teurer als kleine Modelle. Agenten verbrauchen VIELE Tokens
- Qualität: Der Prüfschritt im Agent-Kreislauf ist entscheidend. Automatische Tests, Validierung
- Halluzinationen: Gerade bei Fakten, Zahlen, Quellen kritisch. Immer gegenchecken!
- Datenschutz: DSGVO, Betriebsgeheimnisse, personenbezogene Daten
- "Diese Herausforderungen muss man kennen — aber sie sind lösbar."
-->

---
layout: agenda
punkte:
  - Vom Chatbot zum KI-Agenten
  - Ship It! — fünf Agenten live
  - Was nehmen wir mit?
icons: [bot, rocket, target]
aktiv: 3
---

<!--
- Übergang zu den Kern-Learnings
- Von der Demo zur größeren Botschaft
-->

---
rubrik: Was nehmen wir mit?
titel: Der rote Faden
---

<div class="thm-flow">
  <Card icon="database" icon-ton="grau" titel="Digitalisierung" kompakt />
  <FlowArrow />
  <Card icon="message-square" titel="LLMs" kompakt />
  <FlowArrow />
  <Card icon="bot" titel="KI-Agenten" tone="tint" kompakt />
</div>

<CardGrid :cols="2" fill class="mt-4">
  <Card icon="target" titel="Intent spezifizieren">
    Nach Prompting kommt der nächste Schritt: <strong>präzise spezifizieren, was man will</strong> — Rolle, Ziel, Qualität, Prüfkriterien. Nicht nur fragen, sondern <strong>beauftragen</strong>.
  </Card>
  <Card icon="search-check" titel="Kritisch prüfen">
    Der Mensch prüft die Ergebnisse — oder <strong>spezifiziert, wie die KI sich selbst prüfen soll</strong>. Wer das beherrscht, kann massiv skalieren.
  </Card>
</CardGrid>

<Callout class="mt-4">Ihr werdet in einer Welt arbeiten, in der ihr nicht mehr nur lernt, wie man Aufgaben <em>selbst ausführt</em> — sondern wie man <strong>präzise spezifiziert</strong>, was Agenten <em>für euch lösen</em> sollen.</Callout>

<!--
- Den roten Faden der Vorlesung zusammenfassen
- Digitalisierung -> LLMs -> Agenten: drei aufeinander aufbauende Schritte
- Intent spezifizieren: Das ist der nächste Schritt nach Prompt Engineering
  - Nicht nur "Schreib mir einen Text" sondern "Du bist Marketing-Experte, erstelle ein Konzept mit Slogan, Zielgruppe, Tonalität..."
  - Genau das haben wir in der Demo gesehen: Die Agent-Definitionen sind präzise Spezifikationen
- Kritisch prüfen: Entweder Mensch prüft, oder man definiert Prüfkriterien für die KI
  - Skalierungseffekt: Wenn KI sich selbst prüfen kann, braucht man keinen Menschen pro Ergebnis
- Die zentrale Botschaft kurz wirken lassen
-->

---
rubrik: Was nehmen wir mit?
titel: Euer nächster Schritt?
class: text-l
---

<div class="thm-center">
<CardGrid :cols="2">
  <Card band="gruen" icon="chart-line" titel="BWL — Wirtschaftsinformatik">
    <p>Betriebswirtschaft trifft IT — duales Studium mit Praxis von Anfang an.</p>
    <p><a href="https://studiumplus.de/studiengaenge/betriebswirtschaft/betriebswirtschaft-wirtschaftsinformatik/" target="_blank">Bachelor of Arts (B.A.)</a></p>
  </Card>
  <Card band="grau" icon="laptop" titel="Softwaretechnologie">
    <p>Softwareentwicklung, Data Science oder IT-Security — dual studieren.</p>
    <p><a href="https://studiumplus.de/studiengaenge/softwaretechnologie/" target="_blank">Bachelor of Science (B.Sc.)</a></p>
  </Card>
</CardGrid>
</div>

<Callout ton="hell" icon="graduation-cap" class="mt-4">Wenn euch das heute gefallen hat — studiert doch bei uns dual. :)</Callout>

<!--
- Kurzer Studien-Teaser, nicht zu werblich
- Wirtschaftsinformatik verbindet beide Welten
- StudiumPlus als Option erwähnen
- "Wenn euch das heute gefallen hat, könnt ihr sowas auch studieren!"
-->

---
layout: end
rubrik: Noch Fragen?
---

# Danke für eure Aufmerksamkeit!

<div class="end-kontakt">
  <div class="ek-name">Prof. Dr. Carsten Lucke</div>
  <div>Studiengangsleiter BWL-Wirtschaftsinformatik & Softwaretechnologie</div>
  <div>StudiumPlus · Technische Hochschule Mittelhessen</div>
  <div class="ek-mail"><ThmIcon name="mail" ton="gruen" :size="1" /> <a href="mailto:carsten.lucke@studiumplus.de">carsten.lucke@studiumplus.de</a></div>
</div>

<style>
.end-kontakt {
  margin-top: 1.6rem;
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--thm-grey-100);
}
.end-kontakt .ek-name {
  font-size: 1.05rem;
  font-weight: var(--fw-bold);
  color: var(--white);
}
.end-kontakt .ek-mail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.6rem;
}
.end-kontakt a {
  color: var(--white);
  border-bottom-color: var(--thm-green-400);
}
</style>

<!--
- Offene Fragerunde
- Ggf. nochmal Dashboard zeigen wenn Fragen zur Demo kommen
- Visitenkarten / Kontaktdaten bereithalten
- Diskussionsfragen (falls Zeit):
  - "Verändert KI eure zukünftigen Berufe? Wie?"
  - "Was kann KI gut — und was wird sie nie können?"
  - "Wem gehören die Ergebnisse, die eine KI erstellt?"
- Offene Diskussion, 5-8 Minuten
- Keine "richtige" Antwort — es geht ums Nachdenken
- Bei Frage 1: Berufe verändern sich, aber verschwinden selten komplett
- Bei Frage 2: Kreativität, Empathie, ethische Entscheidungen
- Bei Frage 3: Urheberrecht, wer ist verantwortlich?
- Schüler zum Sprechen ermutigen
-->
