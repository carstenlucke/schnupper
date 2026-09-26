---
theme: ./theme-thm
title: 'Vom Chatbot zum KI-Agenten'
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
bild: /studiumplus-campus.jpg
rubrik: Schnuppervorlesung · Duales Studium
---

# Vom Chatbot<br>zum KI-Agenten

<div class="cover-meta">

Prof. Dr. Carsten Lucke

</div>

<!--
- Willkommen, kurze Vorstellung
- Thema: KI in der Praxis, nicht nur Theorie
- Später: Live-Demo, bei der IHR mitbestimmt
-->

---
layout: question
class: text-xl
hideInToc: true
---

Wo seid ihr **heute** <br>schon KI begegnet?

<!--
- Offene Frage, Antworten zurufen lassen und sammeln
- "Heute" betonen: Es geht um den Alltag, nicht nur um Chatbots
- Nennt jemand ChatGPT: parken — "Dazu gleich mehr"
- Nachhaken, falls es stockt: Wecker, Handy entsperren, Feed, Navi, Musik
- Überleitung: "Und was ist mit …?" — nächste Folie löst auf
-->

---
rubrik: Einstieg
titel: KI ist schon überall
class: text-xl
---

<div class="thm-center thm-gruppe">
<div class="thm-lead">Ihr nutzt täglich KI — oft ohne es zu merken:</div>
<CardGrid :cols="2">
  <Card icon="music" titel="Spotify & YouTube" kompakt>
    Empfehlungen basierend auf eurem Verhalten&nbsp;—&nbsp;das&nbsp;ist&nbsp;KI
  </Card>
  <Card icon="smartphone" titel="TikTok & Instagram" kompakt>
    Der Algorithmus entscheidet, was ihr seht&nbsp;—&nbsp;das&nbsp;ist&nbsp;KI
  </Card>
  <Card icon="languages" titel="DeepL & Google Translate" kompakt>
    Übersetzungen in Echtzeit&nbsp;—&nbsp;das&nbsp;ist&nbsp;KI
  </Card>
  <Card icon="message-square" titel="ChatGPT & Co." kompakt>
    Texte schreiben, Fragen beantworten — und jetzt: auch <strong>handeln</strong>
  </Card>
</CardGrid>
</div>

<!--
- Bezug zur Lebenswelt der Schüler
- Mit den Zurufen abgleichen: Was wurde genannt, was nicht?
- KI ist kein Zukunftsthema — es ist Gegenwart
- Die Frage ist nicht OB KI kommt, sondern wie wir damit umgehen
- Überleitung zur Umfrage: Beim letzten Punkt bleiben wir — wer von euch
  hat so etwas schon benutzt?
-->

---
layout: question
titel: Kurze Umfrage
class: text-xl
hideInToc: true
---

Wer von euch hat schon mal <br>**Claude, ChatGPT, Gemini <br>oder Copilot** benutzt?

<!--
- Hände hoch! (Erwartung: fast alle)
- Nur Handzeichen — wofür ihr das nutzt, fragen wir später
- "Fast alle also. Dann schauen wir uns jetzt an, womit ihr da eigentlich
  redet."
-->

---
rubrik: Einstieg
titel: Was steckt hinter ChatGPT & Co.?
untertitel: Ein Large Language Model, kurz LLM
class: text-l
---

<div class="thm-center thm-gruppe">
<div class="thm-cols thm-cols-2 llm-oben">
  <div class="llm-begriffe">
    <div class="llm-begriff"><span class="llm-buchstabe">L</span><div><strong>Large</strong> <em>groß</em><br>hat riesige Mengen Text gelesen: Bücher, Websites, Chats</div></div>
    <div class="llm-begriff"><span class="llm-buchstabe">L</span><div><strong>Language</strong> <em>Sprache</em><br>hat dabei gelernt, wie Sprache funktioniert</div></div>
    <div class="llm-begriff"><span class="llm-buchstabe">M</span><div><strong>Model</strong> <em>Modell</em><br>sagt vorher, welches Wort als Nächstes kommt</div></div>
  </div>
  <NaechstesWort />
</div>

<div class="llm-modelle">
  <span class="llm-label">Modelle</span>
  <div class="llm-reihe">
    <span class="llm-familie"><strong>GPT-5.6</strong> Sol · Terra · Luna</span>
    <span class="llm-familie"><strong>Claude</strong> Opus · Fable · Mythos</span>
    <span class="llm-familie"><strong>Gemini</strong></span>
    <span class="llm-familie"><strong>Mistral</strong></span>
    <span class="llm-familie"><strong>Llama</strong></span>
    <span class="llm-familie"><strong>DeepSeek</strong></span>
  </div>
  <span class="llm-label">Apps</span>
  <div class="llm-reihe">
    <span class="llm-familie app">ChatGPT</span>
    <span class="llm-familie app">Claude</span>
    <span class="llm-familie app">Gemini</span>
    <span class="llm-familie app">Copilot</span>
    <span class="llm-familie app">Le Chat</span>
  </div>
</div>
</div>

<style>
.llm-oben { flex: none; align-items: center; gap: 2.4rem; }

.llm-begriffe {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.llm-begriff {
  display: flex;
  align-items: flex-start;
  gap: 0.9rem;
  line-height: 1.35;
  color: var(--thm-grey-600);
}

.llm-begriff strong { color: var(--text-strong); font-size: 1.1em; }
.llm-begriff em { font-style: normal; color: var(--thm-green-700); margin-left: 0.3rem; }

.llm-buchstabe {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.4rem;
  height: 2.4rem;
  background: var(--thm-green-500);
  color: var(--white);
  font-size: 1.4rem;
  font-weight: var(--fw-bold);
}

.llm-modelle {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 0.5rem 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-default);
}

.llm-reihe {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.llm-label {
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.llm-familie {
  padding: 0.3rem 0.8rem;
  background: var(--thm-grey-50);
  font-size: 0.9em;
  color: var(--thm-grey-600);
}

.llm-familie strong { color: var(--text-strong); margin-right: 0.2rem; }

/* Apps: nur der Rahmen, damit sie sich sichtbar von den Modellen abheben */
.llm-familie.app {
  background: none;
  border: 1px solid var(--thm-grey-200);
}
</style>

<!--
- "Wir haben jetzt schon ein paarmal ChatGPT gesagt. Was steckt da
  eigentlich drin?" — ein Large Language Model, ein großes Sprachmodell
- Large: Es hat mehr Text gelesen, als ein Mensch in tausend Leben lesen
  könnte
- Language: Dabei hat es gelernt, wie Sprache funktioniert — Grammatik,
  Fakten, Stil, sogar Programmiersprachen
- Model: Im Kern macht es etwas erstaunlich Einfaches: Es sagt vorher,
  welches Wort als Nächstes kommt. Dann hängt es das Wort an und macht
  weiter — Wort für Wort
- Rechts ausprobieren lassen: "Wie geht der Satz weiter?" Die meisten
  sagen Bäcker oder Training — genau wie das Modell. Mond ist möglich,
  aber sehr unwahrscheinlich (Zahlen sind ausgedacht)
- Unten zwei Reihen: MODELLE sind das Gehirn, APPS das Fenster, in dem
  ihr mit ihnen redet. ChatGPT ist die App, das Modell darin heißt z. B.
  GPT-5.6. Copilot von Microsoft ist auch eine App — darin arbeiten vor
  allem GPT-Modelle. Le Chat ist die App von Mistral, einem Anbieter aus
  Frankreich. Claude und Gemini heißen als App und als Modell gleich
- Die Namen hinter dem Punkt sind Varianten: größer und klüger oder
  kleiner und schneller
- Llama (Meta), Mistral und DeepSeek gibt es auch zum Herunterladen — die
  laufen dann sogar auf dem eigenen Rechner
- Dieses Wort "Modell" kommt ab jetzt immer wieder vor
-->

---
rubrik: Einstieg
titel: 'Die große Veränderung: Vom Code zur Sprache'
class: text-xl
---

<div class="thm-center thm-gruppe">
<div class="thm-flow">
  <Card icon="code" icon-ton="grau" titel="Früher">
    Um mit digitalen Daten zu arbeiten, brauchte man <strong>Programmiersprachen</strong>.
    <div class="thm-sample">SELECT * FROM kunden<br>WHERE alter &gt; 18</div>
    <CodeKlappe />
  </Card>
  <FlowArrow />
  <Card icon="message-square" titel="Heute" tone="tint">
    LLMs erlauben es, mit Daten und Systemen in <strong>natürlicher Sprache</strong> zu arbeiten.
    <div class="thm-sample sprache">„Zeig mir alle Kunden über 18 Jahre“</div>
  </Card>
</div>

<Callout icon="rocket"><strong>Genau das werden wir gleich sehen:</strong> Unsere KI-Agenten bekommen ihre Aufträge in ganz normalem Deutsch — kein Code, keine Programmierung.</Callout>
</div>

<!--
- DAS ist der Paradigmenwechsel den LLMs gebracht haben
- Früher: Nur wer programmieren konnte, konnte digitale Systeme steuern
- Heute: Natürliche Sprache reicht — LLMs sind der "Dolmetscher"
- Bezug zu den Demos: Die Agenten verstehen deutsche Aufträge
- Knopf "Und wenn es komplizierter wird?": zeigt 25 Zeilen TypeScript, die
  Primzahlen aus einem Zahlenstrom sammeln — gegen zwei Sätze an einen
  Agenten. Nicht vorlesen, nur wirken lassen. Schließen mit Klick daneben
  oder Esc. (Genau diese Aufgabe hat bei den Counting Agents der
  Primzahl-Agent.)
- "Aber es gibt noch ein Problem..."
-->

---
layout: agenda
punkte:
  - Vom Chatbot zum KI-Agenten
  - Agenten live erleben
  - Was nehmen wir mit?
icons: [bot, circle-play, target]
aktiv: 1
---

<!--
- Jetzt: Was ist der Unterschied?
- Einfach erklärt, ohne Technik-Jargon
-->

---
layout: question
titel: Kurze Rufrunde
class: text-xl
hideInToc: true
---

Wofür nutzt **ihr** <br>ChatGPT & Co.?

<!--
- Antworten zurufen lassen und sammeln, noch nicht kommentieren
- Erwartet: Hausaufgaben, Texte schreiben, Fragen beantworten, Übersetzen,
  Ideen sammeln
- Nachhaken, falls es stockt: Referat, Bewerbung, Lernen für eine Klausur
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Wofür ihr ChatGPT nutzt
class: text-xl
---

<div class="thm-center thm-gruppe">
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

<Callout v-click><strong>Fällt euch was auf?</strong> Bei allem davon <em>antwortet</em> ChatGPT. <em>Getan</em> wird es danach — von euch.</Callout>
</div>

<!--
- Mit den Zurufen abgleichen: Was davon wurde genannt? Was fehlt?
- Kurz halten, das kennen alle
- Dann fragen: "Fällt euch was auf?" — kurz warten, dann per Klick den
  Merksatz aufdecken
- Pointe: Bei allem, was ihr genannt habt, schreibt ChatGPT eine Antwort.
  Abgeben, abschicken, einbauen — das macht ihr
- Überleitung: "Warum ist das so? Schauen wir uns die Grenzen an."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Wo stößt ChatGPT an Grenzen?
class: text-xl
---

<div class="thm-center thm-gruppe">
<CardGrid :cols="2">
  <Card icon="folder-open" icon-ton="rot" titel="Bleibt in seinem Fenster" kompakt>
    Es kommt nicht an eure Dateien und Programme.
  </Card>
  <Card icon="timer" icon-ton="rot" titel="Wartet auf euch" kompakt>
    Nach jeder Antwort ist Schluss — bis ihr weiterfragt.
  </Card>
  <Card icon="plug" icon-ton="rot" titel="Hat nur, was eingebaut ist" kompakt>
    Eure eigenen Systeme kann es nicht bedienen.
  </Card>
  <Card icon="refresh-cw" icon-ton="rot" titel="Sieht das Ergebnis nicht" kompakt>
    Ob es geklappt hat, erfährt es nur von euch.
  </Card>
</CardGrid>

<Callout icon="info" ton="hell"><strong>To be fair:</strong> Die Grenze verschwimmt. ChatGPT &amp; Co. bekommen laufend neue Werkzeuge.</Callout>
</div>

<!--
- Kernpunkt: Nicht "ChatGPT kann nichts", sondern: Es arbeitet in seinem
  eigenen Fenster, Frage für Frage, und ihr seid die Brücke zur echten Welt
- Wer einwirft "ChatGPT kann doch Dateien machen / im Web suchen / Code
  ausführen": stimmt! Genau das ist der Merksatz unten — die Anbieter bauen
  Werkzeuge ein, die Chatbots wachsen in Richtung Agent
- Der Unterschied liegt nicht im Wissen, sondern darin, wer den nächsten
  Schritt macht und wie weit die Hände reichen
- "Stellt euch vor, ihr ruft einen Experten an..."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: 'Der Alltag mit Chatbots: Copy & Paste'
class: text-l
---

<div class="thm-center thm-gruppe">
  <CopyPasteSchleife />

  <Callout icon="user"><strong>Ihr seid die Brücke.</strong> Der Chatbot sieht nur den Schnipsel, den ihr ihm hineinkopiert — nicht eure ganze Arbeit.</Callout>
</div>

<!--
- "Wer kennt's?" — Referat, Hausaufgabe, Bewerbung: Absatz rüber in
  ChatGPT, Antwort zurück ins Dokument, nächster Absatz, wieder rüber …
- IHR tragt die Informationen hin und her. Der Chatbot kennt nur, was ihr
  ihm gebt — nicht das ganze Referat, nicht die Aufgabenstellung, nicht
  eure Quellen
- Irgendwann nervt das. Die Frage ist: Geht das auch ohne uns als
  Zwischenhändler?
- Überleitung: "Genau da kommen Agenten ins Spiel."
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Der Unterschied
class: text-xl
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
  font-size: 1.2em;
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
class: text-l
---

<div class="thm-center">
  <AgentKreislauf />
</div>

<!--
- DAS ist der zentrale Unterschied: die Feedback-Schleife
- Ein Chatbot gibt EINE Antwort. Ein Agent arbeitet ITERATIV.
- Analogie Praktikant: Ihr gebt ihm eine Aufgabe, er arbeitet eigenständig
- Überleitung: "Aber wie wird aus einem Sprachmodell so ein Agent? Was steckt
  da drin?"
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Was macht aus einem Modell einen Agenten?
class: text-l
---

<div class="thm-center thm-gruppe">
  <AgentAnatomie />
</div>

<!--
- Zwei Teile: Das MODELL (das Sprachmodell, z. B. GPT oder Claude) ist das
  Gehirn — es denkt, plant und entscheidet
- Das HARNESS (engl. Geschirr, wie beim Pferd: Das Pferd hat die Kraft,
  das Geschirr macht sie nutzbar) ist alles drumherum. Zwei Seiten:
- Links die WERKZEUGE — Hände und Augen: Dateien lesen und schreiben,
  Programme starten, im Web suchen
- Rechts die STEUERUNG — was das Harness selbst leistet:
  - Schleife: der Kreislauf von eben. Ruft das Modell immer wieder auf,
    führt aus, was es sich wünscht, und gibt ihm das Ergebnis zurück — bis
    die Aufgabe fertig ist
  - Anweisungen: Rolle und Aufgabe, in unseren Demos eine Textdatei
  - Gedächtnis: der Verlauf, und wenn er zu lang wird, eine Zusammenfassung
  - Leitplanken: was der Agent ohne Nachfrage darf und was nicht
- Entscheiden tut immer das Modell, das Harness führt aus
- Fun Fact: Ein mittelmäßiges Modell mit gutem Harness schlägt oft ein
  besseres Modell mit schlechtem Harness
- Rückbezug auf "Die Grenze verschwimmt": Die Anbieter bauen ihren
  Chatbots Stück für Stück ein größeres Harness
- Überleitung: "Und warum reden gerade alle über Agenten?"
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

<Callout icon="circle-play" class="mt-4"><strong>Genau das schauen wir uns jetzt live an:</strong> mehrere Agenten, eine gemeinsame Aufgabe — und ihr seid dabei.</Callout>

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
  - Agenten live erleben
  - Was nehmen wir mit?
icons: [bot, circle-play, target]
aktiv: 2
---

<!--
- Jetzt: Agenten live — die heute ausgewählte Demo (oder zwei)
-->

---
rubrik: Agenten live erleben
titel: Welche Demo schauen wir uns an?
routeAlias: demos
hideInToc: true
---

<div class="thm-center">
  <DemoUebersicht />
</div>

<div class="thm-note">Karte anklicken, um in die Demo zu springen. Von jeder Demo-Folie führt „Demos“ unten in der Mitte hierher zurück.</div>

<!--
- Heute eine Demo, manchmal zwei — Karte anklicken, um hineinzuspringen
- Am Ende jeder Demo: "Noch eine Demo" führt hierher zurück, "Was nehmen wir
  mit?" (oder einfach →) weiter zum Schluss
- Alternative: die Klasse abstimmen lassen, welche Demo sie sehen will
-->

---
# Demo-Blöcke, erreichbar über die Übersicht davor. `demo:` kennzeichnet
# alle Folien eines Blocks (Zurück-Link, Navigation in setup/main.ts);
# `hide: true` nähme einen Block ganz heraus.
src: ./demos/ship-it.md
demo: ship-it
---

---
src: ./demos/counting-agents.md
demo: counting-agents
---

---
src: ./demos/agent-party.md
demo: agent-party
---

---
layout: agenda
punkte:
  - Vom Chatbot zum KI-Agenten
  - Agenten live erleben
  - Was nehmen wir mit?
icons: [bot, circle-play, target]
aktiv: 3
routeAlias: nach-demos
---

<!--
- Übergang zu den Kern-Learnings
- Erst der Reality Check, der für alle Demos gilt, dann die größere Botschaft
-->


---
rubrik: Was nehmen wir mit?
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
- Kein Hype ohne Reality Check — gilt für jede Demo, die wir gesehen haben
- Kosten: Agenten verbrauchen VIELE Tokens, große Modelle ca. 100x teurer als kleine
  - Counting Agents: ~90 Anfragen pro Minute — nur fürs Zählen
  - Ship It!: fünf Agenten, jeder mit mehreren Durchläufen
- Qualität: Der Prüfschritt im Agent-Kreislauf ist entscheidend. Automatische Tests, Validierung
  - Counting Agents: Das Dashboard rechnet selbst nach und färbt Fehler rot
  - Ship It!: Wer prüft Website, Preis und Posts, bevor sie rausgehen?
- Halluzinationen: Gerade bei Fakten, Zahlen, Quellen kritisch. Immer gegenchecken!
  - Counting Agents: rote Kachel — falsche Primzahl, selbstbewusst eingesammelt
  - Ship It!: Zahlen in der Preiskalkulation
  - Agent Party: überzeugend klingende, aber erfundene Größenordnungen
- Datenschutz: DSGVO, Betriebsgeheimnisse, personenbezogene Daten
  - Ship It! / Counting Agents: alles geht an ein Modell in der Cloud
  - Agent Party: Umschalten auf das lokale Modell in LM Studio zeigt die Alternative
- "Diese Herausforderungen muss man kennen — aber sie sind lösbar."
-->

---
rubrik: Was nehmen wir mit?
titel: Der rote Faden
---

<div class="thm-flow">
  <Card icon="brain" icon-ton="grau" titel="LLM" kompakt>das Modell: sagt Wörter vorher</Card>
  <FlowArrow />
  <Card icon="message-square" titel="Chatbot" kompakt>Modell + Chatfenster: antwortet</Card>
  <FlowArrow />
  <Card icon="bot" titel="KI-Agent" tone="tint" kompakt>Modell + Harness: handelt</Card>
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
- LLM -> Chatbot -> Agent: drei aufeinander aufbauende Schritte. Das
  Modell ist immer dasselbe Gehirn — was sich ändert, ist, was drumherum
  gebaut ist: erst ein Chatfenster, dann ein ganzes Harness
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
