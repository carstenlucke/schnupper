---
theme: default
title: 'Digitalisierung und KI'
titleTemplate: '%s — Schnuppervorlesung'
author: 'Prof. Dr. Carsten Lucke'
info: |
  Schnuppervorlesung — Technische Hochschule Mittelhessen
  Prof. Dr. Carsten Lucke
transition: fade
colorSchema: dark
class: text-left
canvasWidth: 980
drawings:
  persist: false
---

<!-- ==================== TITELFOLIE ==================== -->

<div class="logo-bar">
  <img src="/Logo-StudiumPlus_4c.png" alt="StudiumPlus" class="logo-studplus">
  <img src="/THM_Logo_4c.png" alt="THM" class="logo-thm">
</div>

<div class="subtitle">Was Maschinen schon können</div>

# Digitalisierung und KI

<div class="meta">
<p>Schnuppervorlesung — Technische Hochschule Mittelhessen</p>
<p>Prof. Dr. Carsten Lucke</p>
</div>

<!--
- Willkommen, kurze Vorstellung
- Thema: KI in der Praxis, nicht nur Theorie
- Am Ende: Live-Demo, bei der IHR das Produkt bestimmt
-->

---
layout: center
class: interactive-slide
hideInToc: true
---

<div class="emoji">🙋</div>

## Kurze Umfrage

<p style="font-size: 1.3em; margin-top: 30px;">Wer von euch hat schon mal<br><strong style="color: var(--thm-gruen);">ChatGPT, Gemini oder Copilot</strong> benutzt?</p>

<!--
- Hände hoch! (Erwartung: fast alle)
- Kurze Rufrunde: Wofür nutzt ihr das?
- Typische Antworten: Hausaufgaben, Texte schreiben, Fragen beantworten, Übersetzen
- "Spannend. Und genau da setzen wir heute an."
-->

---

## Digitalisierung und KI — wie hängt das zusammen?

<div class="vs-container" style="margin-top: 30px;">
  <div class="card card-grau" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em; color: var(--thm-mittelgrau);"><i class="fa-solid fa-database"></i></div>
    <h3>Digitalisierung</h3>
    <p><strong style="color: var(--thm-mittelgrau);">Sammeln und Speichern</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">Aus Aktenordnern wurden Datenbanken, aus Briefen wurden E-Mails, aus Papier wurden PDFs.</p>
  </div>
  <div class="vs-label"><i class="fa-solid fa-arrow-right" style="color: var(--thm-gruen);"></i></div>
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em;"><i class="fa-solid fa-brain"></i></div>
    <h3>Künstliche Intelligenz</h3>
    <p><strong>Verstehen und Nutzen</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">KI zieht Schlüsse aus den digitalisierten Daten — und handelt eigenständig.</p>
  </div>
</div>
<div class="callout" style="margin-top: 25px;">
  <p><i class="fa-solid fa-lightbulb"></i> <strong>Ohne Digitalisierung hätte KI kein Futter.</strong> Die Digitalisierung hat die Welt für Maschinen lesbar gemacht — KI ist die Intelligenzschicht, die jetzt darauf aufsetzt.</p>
</div>

<!--
- Digitalisierung ist die Infrastruktur, KI die Intelligenz
- Passive Digitalisierung: Daten liegen nur herum (Excel, PDFs)
- Aktive Digitalisierung: Daten ARBEITEN für uns
- "KI ohne Digitalisierung wäre ein Gehirn ohne Augen und Ohren"
- "Und ihr nutzt das längst, ohne darüber nachzudenken..."
-->

---

## KI ist schon überall

<p style="margin-bottom: 15px;">Ihr nutzt täglich KI — oft ohne es zu merken:</p>

<div class="card-grid cols-2" style="margin-top: 10px;">
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-music"></i></div>
    <h3>Spotify & YouTube</h3>
    <p>Empfehlungen basierend auf eurem Verhalten — das ist KI</p>
  </div>
  <div class="card card-blue">
    <div class="card-icon"><i class="fa-brands fa-tiktok" style="color: var(--thm-hellblau);"></i></div>
    <h3>TikTok & Instagram</h3>
    <p>Der Algorithmus entscheidet, was ihr seht — das ist KI</p>
  </div>
  <div class="card card-yellow">
    <div class="card-icon"><i class="fa-solid fa-language" style="color: var(--thm-gelb);"></i></div>
    <h3>DeepL & Google Translate</h3>
    <p>Übersetzungen in Echtzeit — das ist KI</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-comment-dots"></i></div>
    <h3>ChatGPT & Co.</h3>
    <p>Texte schreiben, Fragen beantworten — und jetzt: auch <strong>handeln</strong></p>
  </div>
</div>

<!--
- Bezug zur Lebenswelt der Schüler
- KI ist kein Zukunftsthema — es ist Gegenwart
- Die Frage ist nicht OB KI kommt, sondern wie wir damit umgehen
- Überleitung: "Und genau beim letzten Punkt wird es jetzt spannend..."
-->

---

## Die große Veränderung: Vom Code zur Sprache

<div class="vs-container" style="margin-top: 30px;">
  <div class="card card-grau" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em; color: var(--thm-mittelgrau);"><i class="fa-solid fa-code"></i></div>
    <h3>Früher</h3>
    <p style="font-size: 0.7em;">Um mit digitalen Daten zu arbeiten, brauchte man <strong style="color: var(--thm-mittelgrau);">Programmiersprachen</strong>.</p>
    <p style="font-size: 0.65em; font-family: 'Courier New', monospace; color: var(--thm-mittelgrau); margin-top: 8px; background: rgba(255,255,255,0.06); padding: 6px; border-radius: 4px;">SELECT * FROM kunden<br>WHERE alter &gt; 18</p>
  </div>
  <div class="vs-label"><i class="fa-solid fa-arrow-right" style="color: var(--thm-gruen);"></i></div>
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em;"><i class="fa-solid fa-comment-dots"></i></div>
    <h3>Heute</h3>
    <p style="font-size: 0.7em;">LLMs erlauben es, mit Daten und Systemen in <strong>natürlicher Sprache</strong> zu arbeiten.</p>
    <p style="font-size: 0.65em; margin-top: 8px; background: rgba(128,186,36,0.1); padding: 6px; border-radius: 4px; color: var(--text-primary);">"Zeig mir alle Kunden<br>über 18 Jahre"</p>
  </div>
</div>
<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-rocket"></i> <strong>Genau das werden wir gleich sehen:</strong> Unsere KI-Agenten bekommen ihre Aufträge in ganz normalem Deutsch — kein Code, keine Programmierung.</p>
</div>

<!--
- DAS ist der Paradigmenwechsel den LLMs gebracht haben
- Früher: Nur wer programmieren konnte, konnte digitale Systeme steuern
- Heute: Natürliche Sprache reicht — LLMs sind der "Dolmetscher"
- Bezug zu Ship It!: Die Agenten verstehen deutsche Aufträge
- "Aber es gibt noch ein Problem..."
-->

---
layout: center
class: interactive-slide
hideInToc: true
title: Reden vs. Handeln
---

<div class="emoji">🙋</div>

## Reden vs. Handeln

<p style="font-size: 1.3em; margin-top: 30px;">ChatGPT kann mit euch <strong style="color: var(--thm-gruen);">reden</strong>.<br><br>Aber kann es auch <strong style="color: var(--thm-gruen);">handeln</strong>?</p>

<!--
- Provokante Frage
- ChatGPT schreibt Texte, beantwortet Fragen — aber TUT es etwas?
- Es ist wie ein Gehirn im Glas: Es kann denken und reden, aber es hat keine Hände
- "Genau das schauen wir uns heute an."
-->

---
layout: center
class: section-divider
---

## Vom Chatbot zum KI-Agenten

<!--
- Jetzt: Was ist der Unterschied?
- Einfach erklärt, ohne Technik-Jargon
-->

---

## Was kann ChatGPT?

<div class="card-grid cols-2" style="margin-top: 30px;">
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-pen-fancy"></i></div>
    <h3>Texte schreiben</h3>
    <p>Aufsätze, E-Mails, Zusammenfassungen, Gedichte...</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-comments"></i></div>
    <h3>Fragen beantworten</h3>
    <p>Erklärungen, Definitionen, Tipps und Ratschläge</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-language"></i></div>
    <h3>Übersetzen</h3>
    <p>Zwischen Sprachen übersetzen, Texte umformulieren</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-lightbulb"></i></div>
    <h3>Ideen entwickeln</h3>
    <p>Brainstorming, kreative Vorschläge, Konzepte</p>
  </div>
</div>

<!--
- Das kennen die Schüler bereits
- Kurz abhaken, nicht zu lange drauf verweilen
- Überleitung: "Super. Aber jetzt kommt das Aber..."
-->

---

<h2 class="accent-rot">Was kann ChatGPT <span style="color: var(--thm-rot);">nicht</span>?</h2>

<div class="card-grid cols-2" style="margin-top: 30px;">
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-folder-open"></i></div>
    <h3>Dateien erstellen</h3>
    <p>Kann keine Dokumente, Tabellen oder Websites auf eurem Rechner anlegen</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-gears"></i></div>
    <h3>Aufgaben ausführen</h3>
    <p>Kann nichts eigenständig erledigen — nur antworten, wenn ihr fragt</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-plug"></i></div>
    <h3>Mit Systemen arbeiten</h3>
    <p>Kann nicht auf Datenbanken, APIs oder andere Programme zugreifen</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-rotate"></i></div>
    <h3>Sich selbst prüfen</h3>
    <p>Kann nicht testen ob seine Antwort wirklich stimmt oder funktioniert</p>
  </div>
</div>

<!--
- Kernpunkt: ChatGPT ist "nur" ein Gesprächspartner
- Es WEISS viel, aber es KANN nichts tun
- "Stellt euch vor, ihr ruft einen Experten an..."
-->

---

## Der Unterschied

<div class="vs-container" style="margin-top: 40px;">
  <div class="card card-grau" style="text-align: center;">
    <div class="card-icon" style="color: var(--thm-mittelgrau); font-size: 2.5em;"><i class="fa-solid fa-phone"></i></div>
    <h3>Chatbot</h3>
    <p style="font-size: 0.85em;">Ein Experte <strong style="color: var(--thm-mittelgrau);">am Telefon</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">Weiss alles, kann aber nichts anfassen.<br>Ihr müsst alles selbst umsetzen.</p>
  </div>
  <div class="vs-label">vs.</div>
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 2.5em;"><i class="fa-solid fa-user-gear"></i></div>
    <h3>KI-Agent</h3>
    <p style="font-size: 0.85em;">Ein Experte <strong>bei euch im Büro</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">Weiss alles UND legt direkt los.<br>Liest Dateien, schreibt Ergebnisse, nutzt Werkzeuge.</p>
  </div>
</div>

<!--
- Analogie ist der Schlüssel zum Verständnis
- Chatbot = passiver Berater, Agent = aktiver Macher
- "Und wie macht der Agent das? Dazu gibt es ein einfaches Prinzip..."
-->

---

## Wie arbeitet ein KI-Agent?

<p class="text-large" style="margin-top: 10px;">Der Agent-Kreislauf: Denken, Handeln, Prüfen</p>

<img src="/agent-kreislauf.svg" style="width: 100%; max-width: 850px; margin: 10px auto; display: block;">

<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-lightbulb"></i> <strong>Wie ein guter Praktikant:</strong> Aufgabe lesen, Plan machen, umsetzen, prüfen ob alles stimmt — und nachbessern wenn nötig.</p>
</div>

<!--
- DAS ist der zentrale Unterschied: die Feedback-Schleife
- Ein Chatbot gibt EINE Antwort. Ein Agent arbeitet ITERATIV.
- Analogie Praktikant: Ihr gebt ihm eine Aufgabe, er arbeitet eigenständig
- "Und jetzt wird's richtig spannend: Was wenn MEHRERE Agenten zusammenarbeiten?"
-->

---

## Warum Agenten gerade so gefragt sind

<div class="card-grid cols-3" style="margin-top: 25px;">
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.7em;"><i class="fa-solid fa-arrow-up-right-dots"></i></div>
    <h3>Von Assistenz zu Autonomie</h3>
    <p>Heute: "KI hilft mir beim Schreiben."<br>Morgen: <strong>"KI erledigt den Prozess."</strong></p>
  </div>
  <div class="card card-blue" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.7em;"><i class="fa-solid fa-clone"></i></div>
    <h3>Skalierbarkeit</h3>
    <p>Ein Unternehmen kann <strong>100 digitale Agenten</strong> gleichzeitig arbeiten lassen — rund um die Uhr.</p>
  </div>
  <div class="card card-yellow" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.7em;"><i class="fa-solid fa-rotate"></i></div>
    <h3>Selbstkorrektur</h3>
    <p>Agenten <strong>prüfen ihre Ergebnisse</strong> und verbessern sich selbst — ohne dass jemand eingreifen muss.</p>
  </div>
</div>
<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-forward"></i> <strong>Genau das testen wir jetzt live:</strong> 5 Agenten, ein Produktlaunch — in Minuten statt Wochen.</p>
</div>

<!--
- Ausblick in die Arbeitswelt der Schüler
- Assistenz -> Autonomie: Der Shift der gerade passiert
- Skalierbarkeit: 100 Agenten für Marktforschung, Kundenservice, Buchhaltung
- Selbstkorrektur: Fehlertoleranz durch Iteration (wie beim Agent-Kreislauf)
- "Und jetzt schauen wir uns das in der Praxis an!"
-->


---
layout: center
class: section-divider
---

<img src="/ship-it-logo.png" style="height: 120px; margin-bottom: 20px;">

## Ship It!

<!--
- Jetzt: Was ist der Unterschied?
- Einfach erklärt, ohne Technik-Jargon
-->

---

<div style="display: flex; align-items: center; justify-content: space-between;">
  <h2>Ship It!</h2>
  <img src="/ship-it-logo.png" style="height: 70px;">
</div>

<div class="callout" style="margin-top: 30px;">
  <p><i class="fa-solid fa-rocket"></i> <strong>Ship It!</strong> ist ein Dashboard, in dem <strong>5 KI-Agenten</strong> zusammenarbeiten, um ein Produkt auf den Markt zu bringen — Zielgruppenanalyse, Marketing, Social Media, Preiskalkulation und sogar eine fertige Website.</p>
</div>

<div class="card-grid cols-5" style="margin-top: 30px;">
  <div class="card card-plain" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-users-viewfinder"></i></div>
    <h3 style="font-size: 0.75em;">Zielgruppen-Analyst</h3>
    <p style="font-size: 0.65em;">Wer kauft das Produkt? Personas erstellen</p>
  </div>
  <div class="card card-plain" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-bullhorn"></i></div>
    <h3 style="font-size: 0.75em;">Marketing-Experte</h3>
    <p style="font-size: 0.65em;">Name, Slogan, Werbetexte entwickeln</p>
  </div>
  <div class="card card-plain" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-hashtag"></i></div>
    <h3 style="font-size: 0.75em;">Social-Media-Manager</h3>
    <p style="font-size: 0.65em;">Posts für Instagram, LinkedIn, TikTok</p>
  </div>
  <div class="card card-plain" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-calculator"></i></div>
    <h3 style="font-size: 0.75em;">Controller</h3>
    <p style="font-size: 0.65em;">Preiskalkulation und Preisstrategie</p>
  </div>
  <div class="card card-plain" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-code"></i></div>
    <h3 style="font-size: 0.75em;">Web-Entwickler</h3>
    <p style="font-size: 0.65em;">Produkt-Website mit HTML, CSS, JS</p>
  </div>
</div>

<!--
- Jeden Agenten kurz vorstellen, Rolle erklären
- "Die arbeiten wie Abteilungen in einem Unternehmen"
- Website-Agent ist besonders: baut etwas, das man im Browser öffnen kann
-->


---

## Wer wartet auf wen?

<p style="margin-bottom: 20px;">Manche Agenten brauchen die Ergebnisse anderer, bevor sie starten können.</p>

<img src="/agent-abhaengigkeiten.svg" style="width: 100%; max-width: 850px; margin: 15px auto; display: block; border-radius: 8px;">

<div class="callout" style="margin-top: 15px;">
  <p><i class="fa-solid fa-play-circle"></i> <strong>Zielgruppe</strong> und <strong>Kalkulation</strong> starten sofort — sie brauchen nur die Produktbeschreibung.</p>
</div>

<!--
- Zeigen: Abhängigkeiten wie in einem echten Projekt
- Zielgruppe + Kalkulation starten parallel (sofort)
- Marketing wartet auf Zielgruppe
- Social Media wartet auf Marketing
- Website wartet auf alle
- "Jetzt starten wir! Dashboard öffnen..."
-->


---
class: interactive-slide
hideInToc: true
---

## Jetzt seid ihr dran!

<div style="display: flex; align-items: center; gap: 20px; margin-top: 20px;">
  <span style="font-size: 2.5em;">🙋</span>
  <p style="font-size: 1.1em;">Welches Produkt sollen unsere<br>KI-Agenten auf den Markt bringen?</p>
</div>

<p style="font-size: 0.85em; color: var(--thm-mittelgrau); margin-top: 15px;">Das Einzige, was die Agenten von euch brauchen: <strong style="color: var(--thm-gruen);">eine Produktidee in ganz normalem Deutsch.</strong></p>

<div class="product-grid">
  <div class="product-item">
    <div class="product-emoji">🧋</div>
    <p>Bubble-Tea-Automat für Schulen</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">⚡</div>
    <p>Energy Drink für Klausurphasen</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">📱</div>
    <p>App zum Tauschen von Schulbüchern</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">🎧</div>
    <p>KI-Kopfhörer, der Stimmung erkennt</p>
  </div>
</div>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 25px;">
  ...oder eure eigene Idee! Ruft rein — wir stimmen ab.
</p>

<!--
- Die 4 Starter-Ideen als Inspiration zeigen
- Schüler können eigene Ideen einbringen
- 2-3 Minuten Brainstorming, dann Abstimmung per Handzeichen
- Gewähltes Produkt in Ship It! eingeben (kurze Beschreibung tippen)
-->


---
layout: center
class: interactive-slide
hideInToc: true
---

<div class="emoji">🎬</div>

## Los geht's!

<p style="font-size: 1.1em; margin-top: 20px;">Wechsel zum <strong style="color: var(--thm-gruen);">Ship It! Dashboard</strong></p>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 30px;">
  <i class="fa-solid fa-arrow-right" style="color: var(--thm-mittelgrau);"></i> <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>
</p>

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
layout: center
class: interactive-slide
hideInToc: true
---

<div style="text-align: center;">

## Wie gut war die KI?

<p style="font-size: 1.1em; margin-top: 15px;">Zeit für eine ehrliche Bewertung</p>

<div class="question-list">
  <ul style="list-style: none; padding-left: 0;">
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> | <i class="fa-solid fa-thumbs-down" style="color: var(--thm-rot);"></i> Würdet ihr diesen <strong style="color: var(--thm-gruen);">Instagram-Post</strong> liken?</li>
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> | <i class="fa-solid fa-thumbs-down" style="color: var(--thm-rot);"></i> Ist die <strong style="color: var(--thm-gruen);">Preiskalkulation</strong> realistisch?</li>
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> Spricht euch die <strong style="color: var(--thm-gruen);">Website</strong> an?</li>
    <li><i class="fa-solid fa-trophy" style="color: var(--thm-gelb);"></i> Welcher Agent hat <strong style="color: var(--thm-gelb);">am besten</strong> gearbeitet?</li>
  </ul>
</div>

</div>

<!--
- Übergang zur kritischen Bewertung
- Jede Frage einzeln durchgehen, Daumen hoch/runter
- Nachfragen: WARUM? Was genau stört euch?
- "Was hat überrascht?"
- "Was fehlt offensichtlich?"
- "Würde ein echtes Unternehmen das so verwenden?"
-->

<style scoped>
h2::after {
  margin-left: auto !important;
  margin-right: auto !important;
}
</style>

---

## Reality Check: Worauf muss man achten?

<div class="card-grid cols-2" style="margin-top: 25px;">
  <div class="card card-yellow">
    <div class="card-icon"><i class="fa-solid fa-coins" style="color: var(--thm-gelb);"></i></div>
    <h3>Kosten</h3>
    <p>KI arbeitet mit <strong style="color: var(--thm-gelb);">Tokens</strong> — das ist ihre Währung. Je nach Modell kostet das wenig oder richtig viel. Wer Agenten einsetzt, muss die Kosten im Blick behalten.</p>
  </div>
  <div class="card" style="border-top-color: var(--thm-hellblau);">
    <div class="card-icon" style="color: var(--thm-hellblau);"><i class="fa-solid fa-clipboard-check"></i></div>
    <h3 style="color: var(--thm-hellblau);">Qualitätskontrolle</h3>
    <p>Wie stellt man sicher, dass die Ergebnisse <strong style="color: var(--thm-hellblau);">korrekt</strong> sind? Wenn alles manuell geprüft werden muss, wird <strong style="color: var(--thm-hellblau);">der Mensch zum Engpass</strong> — man braucht automatische Prüfmechanismen.</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-ghost"></i></div>
    <h3>Halluzinationen</h3>
    <p>KI kann <strong style="color: var(--thm-rot);">überzeugend falsche Dinge</strong> behaupten — erfundene Fakten, falsche Zahlen, nicht existierende Quellen. Das klingt plausibel, ist aber frei erfunden.</p>
  </div>
  <div class="card" style="border-top-color: var(--thm-grau);">
    <div class="card-icon"><i class="fa-solid fa-shield-halved"></i></div>
    <h3>Datenschutz</h3>
    <p>Daten, die an KI-Dienste gesendet werden, <strong>verlassen das Unternehmen</strong>. Vertrauliche Informationen gehören nicht in einen externen KI-Chat.</p>
  </div>
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
layout: center
class: section-divider
---

## Was nehmen wir mit?

<!--
- Übergang zu den Kern-Learnings
- Von der Demo zur größeren Botschaft
-->

---

## Der rote Faden

<div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-top: 35px;">
  <div class="card card-grau" style="text-align: center; flex: 1;">
    <div class="card-icon" style="font-size: 1.5em; color: var(--thm-mittelgrau);"><i class="fa-solid fa-database"></i></div>
    <h3 style="font-size: 0.85em;">Digitalisierung</h3>
    <p style="font-size: 0.7em;">...hat die Welt in Daten übersetzt</p>
  </div>
  <span style="font-size: 1.3em; color: var(--thm-gruen);"><i class="fa-solid fa-arrow-right"></i></span>
  <div class="card card-blue" style="text-align: center; flex: 1;">
    <div class="card-icon" style="font-size: 1.5em;"><i class="fa-solid fa-comment-dots"></i></div>
    <h3 style="font-size: 0.85em;">LLMs</h3>
    <p style="font-size: 0.7em;">...haben gelernt, diese Daten zu verstehen</p>
  </div>
  <span style="font-size: 1.3em; color: var(--thm-gruen);"><i class="fa-solid fa-arrow-right"></i></span>
  <div class="card" style="text-align: center; flex: 1;">
    <div class="card-icon" style="font-size: 1.5em;"><i class="fa-solid fa-robot"></i></div>
    <h3 style="font-size: 0.85em;">KI-Agenten</h3>
    <p style="font-size: 0.7em;">...handeln jetzt selbstständig in dieser Welt</p>
  </div>
</div>

<div class="card-grid cols-3" style="margin-top: 25px;">
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-screwdriver-wrench"></i> Werkzeug, kein Ersatz</h3>
    <p style="font-size: 0.7em;">Der Mensch bleibt verantwortlich — <strong>jemand muss prüfen</strong>.</p>
  </div>
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-people-group"></i> Arbeitsteilung</h3>
    <p style="font-size: 0.7em;">Spezialisierte Agenten — <strong>wie in echten Unternehmen</strong>.</p>
  </div>
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-gauge-high"></i> Schnell ≠ gut</h3>
    <p style="font-size: 0.7em;">Qualität braucht <strong>menschliches Urteil</strong>.</p>
  </div>
</div>

<!--
- Den roten Faden der Vorlesung zusammenfassen
- Digitalisierung -> LLMs -> Agenten: drei aufeinander aufbauende Schritte
- Die drei Learnings aus der Demo nochmal kurz
- Überleitung: "Und was bedeutet das für EUCH?"
-->

---
class: statement-slide
hideInToc: true
title: Zentrale Botschaft
---

<div class="big-text" style="font-size: 1.4em;">Ihr werdet in einer Welt arbeiten, in der ihr nicht mehr nur lernt, wie man Aufgaben <em>selbst ausführt</em> —<br><br>sondern wie man Agenten steuert, die diese Aufgaben <em>für euch lösen</em>.</div>

<!--
- Die zentrale Botschaft der Vorlesung
- Kurz wirken lassen, nicht sofort weiterreden
- Dann: "Was denkt ihr darüber?"
-->

---
class: interactive-slide
hideInToc: true
---

## Was denkt ihr?

<div class="question-list">
  <ul>
    <li>Verändert KI eure <strong style="color: var(--thm-gruen);">zukünftigen Berufe</strong>? Wie?</li>
    <li>Was kann KI gut — und was wird sie <strong style="color: var(--thm-gruen);">nie können</strong>?</li>
    <li>Wem <strong style="color: var(--thm-gruen);">gehören</strong> die Ergebnisse, die eine KI erstellt?</li>
  </ul>
</div>

<!--
- Offene Diskussion, 5-8 Minuten
- Keine "richtige" Antwort — es geht ums Nachdenken
- Bei Frage 1: Berufe verändern sich, aber verschwinden selten komplett
- Bei Frage 2: Kreativität, Empathie, ethische Entscheidungen
- Bei Frage 3: Urheberrecht, wer ist verantwortlich?
- Schüler zum Sprechen ermutigen
-->

---

## Euer nächster Schritt?

<div class="card-grid cols-2" style="margin-top: 30px;">
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em;"><i class="fa-solid fa-graduation-cap"></i></div>
    <h3>Wirtschaftsinformatik</h3>
    <p>Technik + Wirtschaft — genau die Kombination, die ihr heute gesehen habt.</p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau); margin-top: 10px;">B.Sc. und M.Sc. an der THM</p>
  </div>
  <div class="card card-blue" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em;"><i class="fa-solid fa-laptop-code"></i></div>
    <h3>Duales Studium</h3>
    <p>Theorie an der Hochschule, Praxis im Unternehmen — von Anfang an.</p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau); margin-top: 10px;">StudiumPlus an der THM</p>
  </div>
</div>

<!--
- Kurzer Studien-Teaser, nicht zu werblich
- Wirtschaftsinformatik verbindet beide Welten
- StudiumPlus als Option erwähnen
- "Wenn euch das heute gefallen hat, könnt ihr sowas auch studieren!"
-->

---
class: end-slide
---

## Danke!

<p style="margin-top: 20px;">Noch Fragen?</p>

<p style="margin-top: 40px; font-size: 0.8em; opacity: 0.7;">
  Prof. Dr. Carsten Lucke<br>
  Technische Hochschule Mittelhessen
</p>

<!--
- Offene Fragerunde
- Ggf. nochmal Dashboard zeigen wenn Fragen zur Demo kommen
- Visitenkarten / Kontaktdaten bereithalten
-->
