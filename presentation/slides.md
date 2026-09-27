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
clicks: 2
---

<div class="thm-center thm-gruppe">
<BeispielKarussell :titel="['Daten abfragen', 'Skizze → 3D-Modell', 'Notizen → Quiz-App']">
<template #1>
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
</template>
<template #2>
<div class="thm-flow">
  <Card icon="code" icon-ton="grau" titel="Früher">
    Für ein 3D-Modell brauchte man ein <strong class="nw">3D-Programm</strong> und viel Übung — oder Code.
    <div class="thm-sample">cube([80, 30, 25]);<br>translate([60, 15, 25])<br>&nbsp;&nbsp;cylinder(h = 18, r = 5);</div>
  </Card>
  <FlowArrow />
  <Card icon="message-square" titel="Heute" tone="tint">
    Man zeigt dem LLM eine <strong>Skizze</strong> und sagt, was man haben will.
    <div class="thm-sample sprache mit-bild"><LokSkizze /><span>„Mach aus meiner Skizze ein 3D-Modell, das ich ausdrucken kann.“</span></div>
  </Card>
</div>
</template>
<template #3>
<div class="thm-flow">
  <Card icon="code" icon-ton="grau" titel="Früher">
    Für eine eigene App brauchte man <strong>HTML und JavaScript</strong>.
    <div class="thm-sample">&lt;button onclick="pruefe(2)"&gt;<br>&nbsp;&nbsp;Mitochondrium<br>&lt;/button&gt;</div>
  </Card>
  <FlowArrow />
  <Card icon="message-square" titel="Heute" tone="tint">
    Man beschreibt, <strong>was die App können soll</strong>.
    <div class="thm-sample sprache">„Mach aus meinen Bio-Notizen ein Quiz mit zehn Fragen, das ich auf dem Handy spielen kann.“</div>
  </Card>
</div>
</template>
</BeispielKarussell>

<Callout icon="rocket"><strong>Genau das werden wir gleich sehen:</strong> Unsere KI-Agenten bekommen ihre Aufträge in ganz normalem Deutsch — kein Code, keine Programmierung.</Callout>
</div>

<style>
.mit-bild {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.mit-bild .lok { flex: none; width: 9rem; }

.nw { white-space: nowrap; }
</style>

<!--
- DAS ist der Paradigmenwechsel den LLMs gebracht haben
- Früher: Nur wer programmieren konnte, konnte digitale Systeme steuern
- Heute: Natürliche Sprache reicht — LLMs sind der "Dolmetscher"
- Bezug zu den Demos: Die Agenten verstehen deutsche Aufträge
- Mit → durch die drei Beispiele blättern; die Punkte unten zeigen, wo wir
  stehen. Nach dem dritten geht es zur nächsten Folie
- Beispiel 1, Daten: Knopf "Und wenn es komplizierter wird?" zeigt 25
  Zeilen TypeScript, die Primzahlen aus einem Zahlenstrom sammeln — gegen
  zwei Sätze an einen Agenten. Nicht vorlesen, nur wirken lassen.
  Schließen mit Klick daneben oder Esc. (Genau diese Aufgabe hat bei den
  Counting Agents der Primzahl-Agent.)
- Beispiel 2, Skizze: Früher ein 3D-Programm wie Blender oder Code wie
  hier (OpenSCAD: ein Quader mit einem Zylinder obendrauf — von einer
  Lok ist das noch weit entfernt). Heute: Foto der Skizze an das LLM,
  dazu ein Satz. Heraus kommt eine Datei für den 3D-Drucker. Die Sprache
  ist nicht mehr nur Text — das Modell versteht auch Bilder
- Beispiel 3, App: Früher HTML und JavaScript, hier nur ein einziger
  Antwortknopf. Heute: Notizen abfotografieren, einen Satz dazu — fertig
  ist ein Quiz im Browser. Frage ans Publikum: "Wer hat so was schon
  mal gemacht?"
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

  <Callout v-click="2" icon="user"><strong>Ihr seid die Brücke.</strong> Das Modell sieht nur den Schnipsel, den ihr hineinkopiert — nicht eure ganze Arbeit.</Callout>
</div>

<!--
- "Wer kennt's?" — Referat, Hausaufgabe, Bewerbung: Absatz rüber in
  ChatGPT, Antwort zurück ins Dokument, nächster Absatz, wieder rüber …
- IHR tragt die Informationen zwischen Dokument und Chat hin und her

[click] Modell einblenden:

- Dahinter steckt eigentlich ein Modell — das LLM von vorhin
- ChatGPT selbst ist nur die App: Sie nimmt eure Eingabe, schickt sie an
  das Modell und zeigt dessen Antwort an. Das passiert automatisch, bei
  jedem Absatz aufs Neue
- Merken für später: Die App ist schon ein kleiner Rahmen um das Modell.
  Ein Agent bekommt einen größeren

[click] Merksatz einblenden:

- Das Modell kennt nur, was ihr ihm gebt — nicht das ganze Referat, nicht
  die Aufgabenstellung, nicht eure Quellen
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
class: text-xl
---

<div class="thm-center thm-gruppe">
<CardGrid :cols="3">
  <Card icon="trending-up" titel="Von Assistenz zu Autonomie" kompakt>
    Heute: „KI hilft mir beim Schreiben.“<br>Morgen: <strong>„KI erledigt den Prozess.“</strong>
  </Card>
  <Card icon="copy" titel="Skalierbarkeit" kompakt>
    Ein Unternehmen kann <strong>100 digitale Agenten</strong> gleichzeitig arbeiten lassen — rund um die Uhr.
  </Card>
  <Card icon="refresh-cw" titel="Selbstkorrektur" kompakt>
    Agenten <strong>prüfen ihre Ergebnisse</strong> und verbessern sich selbst — ohne dass jemand eingreifen muss.
  </Card>
</CardGrid>

<Callout icon="circle-play"><strong>Genau das schauen wir uns jetzt live an:</strong> mehrere Agenten, eine gemeinsame Aufgabe — und ihr seid dabei.</Callout>
</div>

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
class: text-xl
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
- Erst der Rückblick, der für alle Demos gilt, dann der Blick nach vorn
-->

---
rubrik: Was nehmen wir mit?
titel: Das haben wir heute gesehen
class: text-l
---

<div class="thm-center thm-gruppe">
<div class="thm-flow">
  <Card icon="brain" icon-ton="grau" titel="LLM" kompakt>Das Modell: sagt Wörter vorher</Card>
  <FlowArrow />
  <Card icon="message-square" titel="Chatbot" kompakt>Modell + Chatfenster: antwortet</Card>
  <FlowArrow />
  <Card icon="bot" titel="KI-Agent" tone="tint" kompakt>Modell + Harness: handelt</Card>
</div>

<div class="gesehen-trenner"></div>

<CardGrid :cols="3">
  <Card icon="file-text" titel="Der Auftrag ist Text" kompakt>
    Rolle und Aufgabe stehen in <strong>normalem Deutsch</strong> — kein Code.
  </Card>
  <Card icon="users" titel="Agenten im Team" kompakt>
    Mehrere Agenten teilen sich <strong>eine gemeinsame Aufgabe</strong>.
  </Card>
  <Card icon="ghost" icon-ton="rot" titel="Fleißig, nicht fehlerfrei" kompakt>
    Agenten arbeiten schnell — und irren sich <strong>mit voller Überzeugung</strong>.
  </Card>
</CardGrid>
</div>

<style>
/* Trennt den roten Faden oben von den Beobachtungen darunter */
.gesehen-trenner { border-top: 1px solid var(--border-default); }
</style>

<!--
- Kurz zurückschauen, egal welche Demo wir heute gesehen haben
- Oben der rote Faden: LLM -> Chatbot -> Agent. Das Modell ist immer
  dasselbe Gehirn — was sich ändert, ist, was drumherum gebaut ist: erst ein
  Chatfenster, dann ein ganzes Harness mit Werkzeugen und Schleife
- Der Auftrag ist Text: Niemand hat programmiert, was die Agenten sagen oder
  tun. Es stand in einer Textdatei, auf Deutsch
- Agenten im Team: In der Demo waren es mehrere, jeder mit seiner Rolle —
  zusammen ergibt sich etwas, das keiner allein gemacht hätte
- Fleißig, nicht fehlerfrei: Fehler sind uns begegnet, und sie klingen
  genauso sicher wie die richtigen Antworten (Halluzination). Beispiel je
  nach Demo:
  - Ship It!: fragwürdige Zahlen in der Preiskalkulation
  - Counting Agents: rote Kachel — falsche Primzahl, selbstbewusst
    eingesammelt; das Dashboard rechnet nach und fällt darauf nicht rein
  - Agent Party: überzeugend klingende, aber erfundene Größenordnungen
- Falls Zeit ist, zwei weitere Haken:
  - Kosten: Agenten verbrauchen viele Tokens, die Währung der KI (Counting
    Agents: ~90 Anfragen pro Minute — nur fürs Zählen)
  - Datenschutz: Was an einen KI-Dienst geht, verlässt das Haus (Ship It! /
    Counting Agents: Modell in der Cloud; Agent Party: lokales Modell in
    LM Studio als Alternative)
- Überleitung: "Was heißt das jetzt für euch?"
-->

---
rubrik: Was nehmen wir mit?
titel: Was ihr in Zukunft können solltet
untertitel: Keine Vorhersage — aber so viel zeichnet sich ab
class: text-l
---

<div class="thm-center thm-gruppe">
<div class="thm-flow">
  <Card nummer="01" icon="scan-search" titel="Erkennen">
    Welche Aufgabe kann ein Agent <strong>übernehmen</strong> — und welche besser nicht?
  </Card>
  <FlowArrow />
  <Card nummer="02" icon="file-text" titel="Spezifizieren">
    Ziele und Anforderungen so <strong>aufschreiben</strong>, dass ein Agent ohne Rückfrage loslegen kann.
  </Card>
  <FlowArrow />
  <Card nummer="03" icon="target" titel="Prüfbar machen" tone="tint">
    Sagen, woran man <strong>„fertig“</strong> erkennt — dann prüft sich der Agent selbst und bessert nach.
  </Card>
</div>

<Callout icon="user-cog">Nicht mehr jeden Schritt selbst machen — sondern <strong>gut beauftragen</strong>.</Callout>
</div>

<!--
- Niemand weiß, wie die Arbeitswelt in zehn Jahren genau aussieht. Aber
  eins ist absehbar: Mit KI-Agenten umgehen zu können, wird so normal wie
  heute der Umgang mit dem Smartphone
- Drei Fähigkeiten zeichnen sich ab:
- Erkennen: Nicht alles eignet sich. Gut: Aufgaben mit klarem Ziel, die man
  in Schritte zerlegen und überprüfen kann. Schlecht: Entscheidungen, für
  die jemand geradestehen muss, oder wo niemand sagen kann, was "gut" ist
- Spezifizieren: Aus "Ich hätte gern irgendwas" wird ein Auftrag — Ziel,
  Rahmen, Anforderungen. Wie bei einer neuen Kollegin, die euch nicht
  fragen kann, was ihr gemeint habt
- Prüfbar machen: Erinnert euch an den Agent-Kreislauf. Der letzte Schritt
  war Prüfen. Prüfen kann ein Agent aber nur, wenn er weiß, WOGEGEN. Wer
  ein klares Ziel vorgibt, bekommt einen Agenten, der so lange nachbessert,
  bis es erreicht ist — ohne dass ein Mensch jedes Zwischenergebnis ansieht
- Das ist der Unterschied zwischen Prompting ("Frag mal") und Beauftragen
- Überleitung: "Klingt abstrakt? Probieren wir es aus."
-->

---
layout: question
hideInToc: true
---

Welche Aufgabe würdet **ihr** einem Agenten geben — und woran merkt er, dass er **fertig** ist?

<!--
- Kurz sammeln, 2–3 Antworten reichen
- Erster Teil trainiert "Erkennen", zweiter Teil "Prüfbar machen" — der ist
  schwerer, und genau darum geht es
- Bei einer Antwort nachhaken: "Woran genau erkennt der Agent, dass das
  gut ist?" Meist wird die Antwort dann erst konkret
- Falls es stockt: Klassenfahrt planen, Lernplan für die Abiprüfungen,
  Ferienjob finden, Geburtstagsparty organisieren
- Überleitung: "Schauen wir uns ein Beispiel an."
-->

---
rubrik: Was nehmen wir mit?
titel: Vom Wunsch zum Auftrag
class: text-xl
---

<div class="thm-center"><div class="thm-flow">
  <Card band="grau" icon="message-square" titel="Wunsch">
    <div class="thm-sample sprache">„Plan mal unsere Klassenfahrt.“</div>
    <p class="auftrag-folge">Wohin? Wie teuer? Wann ist es gut genug? — Der Agent muss <strong>raten</strong>.</p>
  </Card>
  <FlowArrow />
  <Card band="gruen" icon="list-checks" titel="Auftrag">
    <dl class="auftrag">
      <dt>Ziel</dt>
      <dd>Schlag drei Orte für unsere Klassenfahrt vor.</dd>
      <dt>Rahmen</dt>
      <dd>24 Leute, fünf Tage im Mai, höchstens 300 € pro Kopf, mit der Bahn in unter fünf Stunden.</dd>
      <dt>Fertig, wenn</dt>
      <dd>für jeden Ort Anreise, Unterkunft und Gesamtpreis mit Link belegt sind — und alle im Budget liegen.</dd>
    </dl>
  </Card>
</div></div>

<style>
.auftrag-folge { margin-top: 1em; }

.auftrag {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5em 0.9em;
  margin: 0;
}

.auftrag dt {
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--thm-green-700);
  padding-top: 0.3em;
}

.auftrag dd {
  margin: 0;
  color: var(--text-strong);
  line-height: var(--lh-snug);
}

/* Das Prüfkriterium ist der Kern der Folie */
.auftrag dd:last-child {
  padding-left: 0.6em;
  border-left: 0.2rem solid var(--thm-green-500);
}
</style>

<!--
- Links, wie wir mit Chatbots reden: ein Satz, der Rest ist Raterei. Das
  Ergebnis ist irgendwas — und ob es passt, merkt ihr erst hinterher
- Rechts ein Auftrag, mit dem ein Agent arbeiten kann:
  - Ziel: was am Ende herauskommen soll
  - Rahmen: die Anforderungen, die nicht verhandelbar sind
  - Fertig, wenn: das Prüfkriterium. Das kann der Agent selbst nachprüfen —
    Links aufrufen, Preise zusammenrechnen, mit dem Budget vergleichen. Liegt
    ein Ort drüber, sucht er einen neuen
- Genau das ist der Agent-Kreislauf: Handeln, Prüfen, nochmal — bis das Ziel
  erreicht ist
- Beachten: Der Auftrag rechts ist nicht länger, weil er höflicher ist,
  sondern weil jemand vorher nachgedacht hat, was er eigentlich will
-->

---
layout: statement
rubrik: Was nehmen wir mit?
titel: Und wozu dann noch lernen?
zitat: false
---

Beauftragen und prüfen kann nur, wer **selbst versteht**, worum es geht.

<span class="st-note">Wissen und Urteilsvermögen werden wichtiger, nicht unwichtiger.</span>

<!--
- Naheliegende Frage: Wenn Agenten so viel können — wozu dann noch Mathe,
  Deutsch, BWL, Programmieren lernen?
- Antwort: Einen guten Auftrag schreibt nur, wer weiß, was "gut" in diesem
  Fach heißt. Und einen Fehler bemerkt nur, wer es besser weiß — die Fehler
  der Agenten klingen genauso überzeugend wie die richtigen Antworten
- Die Verantwortung bleibt beim Menschen. "Das hat die KI gemacht" zählt
  nicht als Ausrede — nicht in der Schule, nicht im Job
- Kurz wirken lassen
-->


---
rubrik: Was nehmen wir mit?
titel: Werbung in eigener Sache
class: text-l
dunkel: true
---

<div class="thm-center thm-gruppe">
<CardGrid :cols="2">
  <Card band="gruen" icon="chart-line" titel="BWL — Wirtschaftsinformatik">
    <p>Betriebswirtschaft trifft IT — duales Studium mit Praxis von Anfang an.</p>
    <p><a href="https://studiumplus.de/studiengaenge/betriebswirtschaft/betriebswirtschaft-wirtschaftsinformatik/" target="_blank">Bachelor of Arts (B.A.)</a></p>
  </Card>
  <Card band="grau" icon="laptop" titel="Softwaretechnologie">
    <p>Softwareentwicklung, Data Science oder IT&#8209;Security — dual studieren.</p>
    <p><a href="https://studiumplus.de/studiengaenge/softwaretechnologie/" target="_blank">Bachelor of Science (B.Sc.)</a></p>
  </Card>
</CardGrid>

<Callout ton="hell" icon="graduation-cap">Wenn euch das heute gefallen hat — studiert doch bei uns dual. :)</Callout>
</div>

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
.end-kontakt a,
.end-qr a {
  color: var(--white);
  border-bottom-color: var(--thm-green-400);
}
.end-qr {
  display: flex;
  gap: 2.4rem;
  font-size: 0.95rem;
  line-height: 1.45;
}
.end-qr .eq-titel {
  margin-top: 1rem;
  font-size: 1.2rem;
  line-height: 1.2;
  font-weight: var(--fw-bold);
  color: var(--white);
}
</style>

::right::

<div class="end-qr">
  <div>
    <QrCode url="https://carstenlucke.github.io/schnupper/" :size="10" />
    <div class="eq-titel">Die Folien</div>
    <a href="https://carstenlucke.github.io/schnupper/">carstenlucke.github.io/<wbr>schnupper</a>
  </div>
  <div>
    <QrCode url="https://github.com/carstenlucke/schnupper" :size="10" />
    <div class="eq-titel">Der Quellcode</div>
    <a href="https://github.com/carstenlucke/schnupper">github.com/carstenlucke/<wbr>schnupper</a>
  </div>
</div>

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
