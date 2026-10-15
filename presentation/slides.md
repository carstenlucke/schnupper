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
Willkommen zur Schnuppervorlesung „Vom Chatbot zum KI-Agenten“. Es geht um
KI in der Praxis, nicht nur um Theorie: was hinter ChatGPT & Co. steckt, was
einen KI-Agenten davon unterscheidet und was Agenten heute schon können.

Im Mittelteil steht eine Live-Demo, bei der das Publikum mitbestimmt.
-->

---
layout: question
class: text-xl
hideInToc: true
---

Wo seid ihr **heute** <br>schon KI begegnet?

<!--
Die Frage zielt auf den Alltag, nicht nur auf Chatbots. KI steckt in vielen
Dingen, die man kaum noch bemerkt: im Wecker, beim Entsperren des Handys, im
Feed, im Navi, bei der Musik. ChatGPT ist nur das bekannteste Beispiel, dazu
gleich mehr.
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
Die vier Beispiele stammen aus eurem Alltag. Empfehlungen, Feeds und
Übersetzungen laufen so selbstverständlich, dass man kaum merkt, dass KI
dahintersteckt.

KI ist also kein Zukunftsthema, sondern Gegenwart. Die Frage ist nicht, ob
KI kommt, sondern wie wir damit umgehen.

Für den Rest der Vorlesung ist die letzte Karte die wichtigste: ChatGPT &
Co. schreiben Texte und beantworten Fragen — und fangen gerade an, auch zu
handeln.
-->

---
layout: question
titel: Kurze Umfrage
class: text-xl
hideInToc: true
---

Wer von euch hat schon mal <br>**Claude, ChatGPT, Gemini <br>oder Copilot** benutzt?

<!--
Fast alle haben einen dieser Chatbots schon benutzt. Wofür, kommt etwas
später. Zuerst geht es darum, womit man da eigentlich redet.
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
Hinter ChatGPT & Co. steckt ein Large Language Model, kurz LLM, auf Deutsch
ein großes Sprachmodell. Die drei Wörter beschreiben, was es ist:

- **Large:** Es hat mehr Text gelesen, als ein Mensch in tausend Leben lesen
  könnte.
- **Language:** Dabei hat es gelernt, wie Sprache funktioniert — Grammatik,
  Fakten, Stil, sogar Programmiersprachen.
- **Model:** Im Kern macht es etwas erstaunlich Einfaches. Es sagt vorher,
  welches Wort als Nächstes kommt, hängt das Wort an und macht weiter — Wort
  für Wort.

Rechts könnt ihr das selbst ausprobieren: Wie geht der Satz weiter? Die
meisten tippen auf Bäcker oder Training, genau wie das Modell. Mond ist
möglich, aber sehr unwahrscheinlich. Die Zahlen auf der Folie sind
ausgedacht und dienen nur der Veranschaulichung.

Unten stehen zwei Reihen. Die Modelle sind das Gehirn, die Apps das Fenster,
in dem ihr mit ihnen redet. ChatGPT ist die App, das Modell darin heißt zum
Beispiel GPT-5.6. Copilot von Microsoft ist ebenfalls eine App, darin
arbeiten vor allem GPT-Modelle. Le Chat ist die App von Mistral, einem
Anbieter aus Frankreich. Claude und Gemini heißen als App und als Modell
gleich.

Die Namen hinter einem Modell, etwa Sol, Terra und Luna bei GPT-5.6, sind
Varianten: größer und klüger oder kleiner und schneller. Llama (von Meta),
Mistral und DeepSeek gibt es auch zum Herunterladen, sie laufen dann sogar
auf dem eigenen Rechner.

Das Wort „Modell“ kommt im weiteren Verlauf immer wieder vor.
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
Die großen Sprachmodelle haben grundlegend verändert, wie Menschen digitale
Systeme steuern. Früher konnte das nur, wer programmieren konnte. Heute
reicht natürliche Sprache, das LLM übernimmt die Rolle des Dolmetschers.
Darauf bauen auch die Demos auf: Die Agenten dort bekommen ihre Aufträge auf
Deutsch.

Die Folie zeigt drei Beispiele nacheinander, die Punkte unten zeigen,
welches gerade zu sehen ist.

**Daten abfragen:** Hinter dem Knopf „Und wenn es komplizierter wird?“
stecken 25 Zeilen TypeScript, die Primzahlen aus einem Zahlenstrom sammeln.
Einem Agenten genügen dafür zwei Sätze. Genau diese Aufgabe hat in der Demo
„The Counting Agents“ der Primzahl-Agent.

**Skizze → 3D-Modell:** Früher brauchte man ein 3D-Programm wie Blender oder
Code wie den auf der Folie. Er ist in OpenSCAD geschrieben und beschreibt
einen Quader mit einem Zylinder obendrauf — von einer Lok ist das noch weit
entfernt. Heute reichen ein Foto der Skizze und ein Satz dazu, heraus kommt
eine Datei für den 3D-Drucker. Die Sprache ist dabei nicht mehr nur Text,
das Modell versteht auch Bilder.

**Notizen → Quiz-App:** Früher brauchte man HTML und JavaScript, und der
Code auf der Folie ergibt gerade einmal einen einzigen Antwortknopf. Heute
fotografiert man seine Notizen ab, schreibt einen Satz dazu, und fertig ist
ein Quiz im Browser.
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
Der erste Teil klärt, was einen KI-Agenten von einem Chatbot wie ChatGPT
unterscheidet — einfach erklärt, ohne Fachjargon.
-->

---
layout: question
titel: Kurze Rufrunde
class: text-xl
hideInToc: true
---

Wofür nutzt **ihr** <br>ChatGPT & Co.?

<!--
Typische Antworten sind Hausaufgaben, Texte schreiben, Fragen beantworten,
Übersetzen und Ideen sammeln, oft auch ein Referat, eine Bewerbung oder das
Lernen für eine Klausur. Die nächste Folie sortiert sie.
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
Die vier Karten fassen zusammen, wofür die meisten ChatGPT nutzen.

Interessant ist, was alle vier gemeinsam haben: ChatGPT schreibt eine
Antwort. Abgeben, abschicken, einbauen — das macht ihr danach selbst. Warum
das so ist, zeigen die Grenzen auf der nächsten Folie.
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
Der Kern dieser Folie: ChatGPT kann durchaus etwas, aber es arbeitet in
seinem eigenen Fenster, Frage für Frage, und ihr seid die Brücke zur echten
Welt.

Der Einwand liegt nahe, dass ChatGPT doch Dateien erzeugen, im Web suchen
oder Code ausführen kann. Das stimmt, und genau das meint der Hinweis unten:
Die Anbieter bauen laufend Werkzeuge ein, die Chatbots wachsen in Richtung
Agent.

Der Unterschied liegt also nicht im Wissen, sondern darin, wer den nächsten
Schritt macht und wie weit die Hände reichen.
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: 'Der Alltag mit Chatbots: Copy & Paste'
class: text-l
clicks: 5
---

<div class="thm-center">
  <CopyPasteSchleife />
</div>

<!--
Kaum ein Referat entsteht heute ganz ohne ChatGPT. Meist läuft es so: Ihr
kopiert einen Absatz in den Chat, holt die Antwort zurück ins Dokument und
macht mit dem nächsten Absatz weiter. In fünf Schritten läuft ein Absatz
einmal durch, die Zeile unten sagt, was gerade passiert.

[click] Ihr markiert Absatz 3 im Referat, kopiert ihn und fügt ihn in den
Chat ein. Die Informationen zwischen Dokument und Chat tragt dabei ihr hin
und her.

[click] Hinter ChatGPT steckt ein Modell, das Sprachmodell aus dem ersten
Teil. ChatGPT selbst ist nur die App drumherum: Sie nimmt eure Eingabe und
schickt sie an das Modell, bei jedem Absatz aufs Neue. Diese App ist schon
ein kleiner Rahmen um das Modell, ein Agent bekommt später einen deutlich
größeren.

[click] Das Modell schreibt eine bessere Fassung, und die App zeigt sie im
Chat an.

[click] Ihr kopiert die Antwort zurück ins Referat. Absatz 3 ist jetzt neu
und färbt sich grün.

[click] Mit dem nächsten Absatz geht alles von vorn los. Das Modell kennt
nur, was ihr ihm gebt: den einen Absatz, nicht das ganze Referat, nicht die
Aufgabenstellung, nicht eure Quellen. Genau hier setzen Agenten an, denn sie
holen sich selbst, was sie brauchen.
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
Die Analogie fasst den Unterschied zusammen: Ein Chatbot ist ein passiver
Berater, ein Agent ein aktiver Macher. Beide wissen viel, aber nur der
Experte im Büro legt selbst Hand an.
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
Ein Chatbot gibt eine Antwort. Ein Agent arbeitet iterativ: Er dreht Runde
um Runde, bis die Aufgabe erledigt ist.

Aufs Referat übertragen heißt das: den Auftrag lesen (Verstehen), überlegen,
was zu tun ist (Planen), die Datei lesen und schreiben (Handeln), das
Ergebnis ansehen und entscheiden, ob es fertig ist oder noch eine Runde
braucht (Prüfen).

Man kann sich das vorstellen wie bei einem Praktikanten: Ihr gebt ihm eine
Aufgabe, und er arbeitet sie eigenständig ab. Wie das bei einem echten
Agenten aussieht, zeigt die nächste Folie am Referat von vorhin.
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Ein Agent bei der Arbeit
untertitel: Wie Harness, Modell und Werkzeuge zusammenspielen
class: text-l
clicks: 10
---

<div class="thm-center">
  <AgentDurchlauf />
</div>

<!--
Es geht um dasselbe Referat wie beim Copy & Paste, diesmal erledigt die
Arbeit ein Agent. In zehn Schritten läuft ein Auftrag einmal durch. Die
Zeile unten sagt, was gerade passiert, und im Harness leuchtet auf, was
dafür gebraucht wird.

Das Modell kennt ihr schon. Neu ist der grüne Kasten in der Mitte, das
Harness: alles, was um das Modell herum gebaut ist. Was genau darin steckt,
sortiert die nächste Folie. Die Schleife im Harness ist der Kreislauf von
der Folie davor, sie zählt die Runden mit.

[click] Ihr gebt den Auftrag, ein einziges Mal.

[click] Das Harness packt alles zusammen und schickt es ans Modell: euren
Auftrag, seine Anweisungen (Rolle und Aufgabe) und die Liste der Werkzeuge,
die es gibt. Die Schleife steht auf Runde 1.

[click] Das ist der wichtigste Moment: Das Modell kann nichts anfassen. Es
schreibt nur auf, welches Werkzeug es braucht, hier „Datei lesen“. Dieser
Wunsch kommt ins Gedächtnis.

[click] Das Harness prüft an den Leitplanken, ob der Agent das darf. Lesen
ist erlaubt, also führt es das Werkzeug aus und liest das Referat. Das ist
ein anderes Prüfen als im Kreislauf: Die Leitplanken prüfen vorher, ob ein
Werkzeug erlaubt ist. Im Kreislauf prüft das Modell hinterher, ob das
Ergebnis passt.

[click] Das Ergebnis geht zurück ans Modell, und alles andere geht noch
einmal mit: Anweisungen, Werkzeuge und der ganze bisherige Verlauf. Das
Modell selbst merkt sich nichts, es bekommt jedes Mal alles neu. Deshalb
leuchten die Anweisungen wieder auf. Das ist Runde 2.

[click] Jetzt kennt das Modell den Text und schreibt den neuen Absatz,
wieder als Wunsch an ein Werkzeug.

[click] Auch Schreiben ist laut den Leitplanken erlaubt. Absatz 3 im Referat
wird neu geschrieben und färbt sich grün.

[click] In Runde 3 geht die Rückmeldung, dass gespeichert wurde, ans Modell,
und wieder geht alles andere mit.

[click] Das Modell prüft: Das Ergebnis passt, es braucht kein Werkzeug mehr
und meldet, dass es fertig ist. Daran erkennt das Harness, dass die Schleife
zu Ende ist.

[click] Das Ergebnis geht an euch. Beim Copy & Paste wart ihr die Brücke
zwischen Chat und Dokument, jetzt ist es das Harness.
-->

---
rubrik: Vom Chatbot zum KI-Agenten
titel: Aufbau eines KI-Agenten
class: text-l
---

<div class="thm-center thm-gruppe">
  <AgentAnatomie />

  <Callout v-click icon="wrench"><strong>Das Harness macht den Unterschied.</strong> Ein mittelmäßiges Modell mit gutem Harness schlägt oft ein besseres Modell mit schlechtem Harness.</Callout>
</div>

<!--
Ein KI-Agent besteht aus zwei Teilen. Das Modell, also das Sprachmodell wie
GPT oder Claude, ist das Gehirn: Es denkt, plant und entscheidet.

Das Harness ist alles drumherum. Das englische Wort bedeutet Geschirr, wie
beim Pferd: Das Pferd hat die Kraft, das Geschirr macht sie nutzbar. Das
Harness hat zwei Seiten.

Links stehen die Werkzeuge, die Hände und Augen des Agenten: Dateien lesen
und schreiben, Programme starten, im Web suchen.

Rechts steht die Steuerung, also das, was das Harness selbst leistet. Alle
vier Bausteine haben auf der Folie davor schon aufgeleuchtet:

- **Schleife:** die Runden von eben. Sie ruft das Modell immer wieder auf,
  führt aus, was es sich wünscht, und gibt ihm das Ergebnis zurück, bis die
  Aufgabe fertig ist.
- **Anweisungen:** Rolle und Aufgabe des Agenten, in unseren Demos eine
  Textdatei.
- **Gedächtnis:** der Verlauf, und wenn er zu lang wird, eine
  Zusammenfassung davon.
- **Leitplanken:** was der Agent ohne Nachfrage darf und was nicht.

Entscheiden tut immer das Modell, das Harness führt aus.

[click] Ein mittelmäßiges Modell mit gutem Harness schlägt oft ein besseres
Modell mit schlechtem Harness. Das Modell ist wichtig, aber erst das Harness
macht daraus einen Agenten, der etwas erledigt.

Das erklärt auch den Hinweis „Die Grenze verschwimmt“ auf der Folie zu den
Grenzen von ChatGPT: Die Anbieter bauen ihren Chatbots Stück für Stück ein
größeres Harness.
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
Die drei Karten geben einen Ausblick auf die Arbeitswelt, in der ihr einmal
arbeiten werdet.

- **Von Assistenz zu Autonomie:** Das ist der Wandel, der gerade passiert.
  KI hilft nicht mehr nur beim Schreiben, sondern erledigt ganze Abläufe.
- **Skalierbarkeit:** Ein Unternehmen kann viele Agenten gleichzeitig
  einsetzen, etwa in Marktforschung, Kundenservice oder Buchhaltung.
- **Selbstkorrektur:** Fehler sind nicht das Ende. Ein Agent prüft sein
  Ergebnis und bessert in der nächsten Runde nach, wie im Agent-Kreislauf.
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
Im zweiten Teil arbeiten Agenten live. Gezeigt wird eine der Demos, manchmal
auch zwei.
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
Im Vortrag wird hier die Demo ausgewählt. In der Web-App führt ein Klick auf
eine Karte in die Demo. Am Ende jeder Demo geht es mit „Noch eine Demo“
hierher zurück oder mit „Was nehmen wir mit?“ weiter zum Schluss. Im PDF
folgen die drei Demos einfach nacheinander.
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
Der letzte Teil fasst zuerst zusammen, was für alle Demos gilt, und schaut
dann nach vorn: Was heißt das für euch?
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
Dieser Rückblick gilt für jede der Demos.

Oben steht der rote Faden: LLM, Chatbot, Agent. Das Modell ist immer
dasselbe Gehirn. Was sich ändert, ist, was drumherum gebaut ist: erst ein
Chatfenster, dann ein ganzes Harness mit Werkzeugen und Schleife.

**Der Auftrag ist Text:** Niemand hat programmiert, was die Agenten sagen
oder tun. Es stand in einer Textdatei, auf Deutsch.

**Agenten im Team:** In jeder Demo arbeiten mehrere Agenten, jeder mit
seiner Rolle. Zusammen ergibt sich etwas, das keiner allein gemacht hätte.

**Fleißig, nicht fehlerfrei:** Agenten machen Fehler, und die klingen
genauso sicher wie die richtigen Antworten. Man spricht von Halluzination.
Beispiele aus den Demos:

- Ship It!: fragwürdige Zahlen in der Preiskalkulation.
- The Counting Agents: eine rote Kachel, weil ein Agent eine falsche
  Primzahl selbstbewusst eingesammelt hat. Das Dashboard rechnet nach und
  fällt darauf nicht herein.
- Agent Party: überzeugend klingende, aber erfundene Größenordnungen.

Dazu kommen zwei weitere Haken:

- **Kosten:** Agenten verbrauchen viele Tokens, die Währung der KI. Die
  Counting Agents stellen rund 90 Anfragen pro Minute, nur fürs Zählen.
- **Datenschutz:** Was an einen KI-Dienst geht, verlässt das Haus. Ship It!
  und The Counting Agents nutzen ein Modell in der Cloud, Agent Party kann
  alternativ mit einem lokalen Modell in LM Studio laufen.
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
Niemand weiß, wie die Arbeitswelt in zehn Jahren genau aussieht. Eines ist
aber absehbar: Mit KI-Agenten umgehen zu können, wird so normal wie heute
der Umgang mit dem Smartphone. Drei Fähigkeiten zeichnen sich ab.

**Erkennen:** Nicht jede Aufgabe eignet sich. Gut geeignet sind Aufgaben mit
klarem Ziel, die man in Schritte zerlegen und überprüfen kann. Schlecht
geeignet sind Entscheidungen, für die jemand geradestehen muss, oder
Aufgaben, bei denen niemand sagen kann, was „gut“ ist.

**Spezifizieren:** Aus „Ich hätte gern irgendwas“ wird ein Auftrag mit Ziel,
Rahmen und Anforderungen. Das ist wie bei einer neuen Kollegin, die euch
nicht fragen kann, was ihr gemeint habt.

**Prüfbar machen:** Der letzte Schritt im Agent-Kreislauf war das Prüfen.
Prüfen kann ein Agent aber nur, wenn er weiß, wogegen. Wer ein klares Ziel
vorgibt, bekommt einen Agenten, der so lange nachbessert, bis es erreicht
ist — ohne dass ein Mensch jedes Zwischenergebnis ansieht.

Das ist der Unterschied zwischen Prompting („Frag mal“) und Beauftragen.
-->

---
layout: question
hideInToc: true
---

Welche Aufgabe würdet **ihr** einem Agenten geben — und woran merkt er, dass er **fertig** ist?

<!--
Die Frage hat zwei Teile. Der erste übt das Erkennen: Welche Aufgabe eignet
sich überhaupt für einen Agenten? Der zweite übt das Prüfbarmachen, und der
ist schwerer: Woran genau erkennt der Agent, dass sein Ergebnis gut ist? Oft
wird eine Idee erst durch diese Frage konkret.

Mögliche Aufgaben sind eine Klassenfahrt planen, einen Lernplan für die
Abiprüfungen aufstellen, einen Ferienjob finden oder eine Geburtstagsparty
organisieren. Die nächste Folie spielt das an der Klassenfahrt durch.
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
Links steht, wie wir meist mit Chatbots reden: ein Satz, der Rest ist
Raterei. Heraus kommt irgendwas, und ob es passt, merkt ihr erst hinterher.

Rechts steht ein Auftrag, mit dem ein Agent arbeiten kann:

- **Ziel:** was am Ende herauskommen soll.
- **Rahmen:** die Anforderungen, die nicht verhandelbar sind.
- **Fertig, wenn:** das Prüfkriterium. Das kann der Agent selbst nachprüfen,
  indem er Links aufruft, Preise zusammenrechnet und mit dem Budget
  vergleicht. Liegt ein Ort darüber, sucht er einen neuen.

Das ist genau der Agent-Kreislauf: handeln, prüfen, noch einmal — bis das
Ziel erreicht ist.

Der Auftrag rechts ist übrigens nicht länger, weil er höflicher ist, sondern
weil vorher jemand darüber nachgedacht hat, was er eigentlich will.
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
Die Frage liegt nahe: Wenn Agenten so viel können, wozu dann noch Mathe,
Deutsch, BWL oder Programmieren lernen?

Einen guten Auftrag schreibt nur, wer weiß, was „gut“ in diesem Fach heißt.
Und einen Fehler bemerkt nur, wer es besser weiß, denn die Fehler der
Agenten klingen genauso überzeugend wie die richtigen Antworten.

Die Verantwortung bleibt beim Menschen. „Das hat die KI gemacht“ zählt nicht
als Ausrede, weder in der Schule noch im Job.
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
Wenn euch diese Vorlesung gefallen hat: So etwas kann man bei StudiumPlus
dual studieren. Die Wirtschaftsinformatik verbindet beide Welten,
Betriebswirtschaft und IT. Die Links auf den Karten führen zu den beiden
Studiengängen.
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
Zum Weiterdenken drei Fragen, auf die es keine richtige Antwort gibt — es
geht ums Nachdenken:

- **Verändert KI eure zukünftigen Berufe? Wie?** Berufe verändern sich,
  verschwinden aber selten komplett.
- **Was kann KI gut — und was wird sie nie können?** Denkt dabei an
  Kreativität, Empathie und ethische Entscheidungen.
- **Wem gehören die Ergebnisse, die eine KI erstellt?** Hier geht es um
  Urheberrecht und darum, wer verantwortlich ist.

Die QR-Codes führen zu den Folien und zum Quellcode der Demos.
-->
