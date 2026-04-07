---
theme: default
title: 'Digitalisierung und KI'
titleTemplate: '%s — Schnuppervorlesung'
author: 'Prof. Dr. Carsten Lucke'
info: |
  Schnuppervorlesung — Technische Hochschule Mittelhessen
  Prof. Dr. Carsten Lucke
transition: fade
class: text-left
canvasWidth: 980
drawings:
  persist: false
---

<!-- ==================== TITELFOLIE ==================== -->

<div class="subtitle">Was Maschinen schon koennen</div>

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
class: interactive-slide
---

<div class="emoji">🙋</div>

## Kurze Umfrage

<p style="font-size: 1.3em; margin-top: 30px;">Wer von euch hat schon mal<br><strong style="color: var(--thm-gruen);">ChatGPT, Gemini oder Copilot</strong> benutzt?</p>

<!--
- Haende hoch! (Erwartung: fast alle)
- Kurze Rufrunde: Wofuer nutzt ihr das?
- Typische Antworten: Hausaufgaben, Texte schreiben, Fragen beantworten, Uebersetzen
- "Spannend. Und genau da setzen wir heute an."
-->

---

## Digitalisierung und KI — wie haengt das zusammen?

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
    <h3>Kuenstliche Intelligenz</h3>
    <p><strong>Verstehen und Nutzen</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">KI zieht Schluesse aus den digitalisierten Daten — und handelt eigenstaendig.</p>
  </div>
</div>
<div class="callout" style="margin-top: 25px;">
  <p><i class="fa-solid fa-lightbulb"></i> <strong>Ohne Digitalisierung haette KI kein Futter.</strong> Die Digitalisierung hat die Welt fuer Maschinen lesbar gemacht — KI ist die Intelligenzschicht, die jetzt darauf aufsetzt.</p>
</div>

<!--
- Digitalisierung ist die Infrastruktur, KI die Intelligenz
- Passive Digitalisierung: Daten liegen nur herum (Excel, PDFs)
- Aktive Digitalisierung: Daten ARBEITEN fuer uns
- "KI ohne Digitalisierung waere ein Gehirn ohne Augen und Ohren"
- "Und ihr nutzt das laengst, ohne darueber nachzudenken..."
-->

---

## KI ist schon ueberall

<p style="margin-bottom: 15px;">Ihr nutzt taeglich KI — oft ohne es zu merken:</p>

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
    <p>Uebersetzungen in Echtzeit — das ist KI</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-comment-dots"></i></div>
    <h3>ChatGPT & Co.</h3>
    <p>Texte schreiben, Fragen beantworten — und jetzt: auch <strong>handeln</strong></p>
  </div>
</div>

<!--
- Bezug zur Lebenswelt der Schueler
- KI ist kein Zukunftsthema — es ist Gegenwart
- Die Frage ist nicht OB KI kommt, sondern wie wir damit umgehen
- Ueberleitung: "Und genau beim letzten Punkt wird es jetzt spannend..."
-->

---

## Die grosse Veraenderung: Vom Code zur Sprache

<div class="vs-container" style="margin-top: 30px;">
  <div class="card card-grau" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em; color: var(--thm-mittelgrau);"><i class="fa-solid fa-code"></i></div>
    <h3>Frueher</h3>
    <p style="font-size: 0.7em;">Um mit digitalen Daten zu arbeiten, brauchte man <strong style="color: var(--thm-mittelgrau);">Programmiersprachen</strong>.</p>
    <p style="font-size: 0.65em; font-family: 'Courier New', monospace; color: var(--thm-mittelgrau); margin-top: 8px; background: #eee; padding: 6px; border-radius: 4px;">SELECT * FROM kunden<br>WHERE alter &gt; 18</p>
  </div>
  <div class="vs-label"><i class="fa-solid fa-arrow-right" style="color: var(--thm-gruen);"></i></div>
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 1.8em;"><i class="fa-solid fa-comment-dots"></i></div>
    <h3>Heute</h3>
    <p style="font-size: 0.7em;">LLMs erlauben es, mit Daten und Systemen in <strong>natuerlicher Sprache</strong> zu arbeiten.</p>
    <p style="font-size: 0.65em; margin-top: 8px; background: #edf7e0; padding: 6px; border-radius: 4px; color: var(--thm-grau);">"Zeig mir alle Kunden<br>ueber 18 Jahre"</p>
  </div>
</div>
<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-rocket"></i> <strong>Genau das werden wir gleich sehen:</strong> Unsere KI-Agenten bekommen ihre Auftraege in ganz normalem Deutsch — kein Code, keine Programmierung.</p>
</div>

<!--
- DAS ist der Paradigmenwechsel den LLMs gebracht haben
- Frueher: Nur wer programmieren konnte, konnte digitale Systeme steuern
- Heute: Natuerliche Sprache reicht — LLMs sind der "Dolmetscher"
- Bezug zu Ship It!: Die Agenten verstehen deutsche Auftraege
- "Aber es gibt noch ein Problem..."
-->

---
class: statement-slide
---

<div class="big-text">ChatGPT kann mit euch <em>reden</em>.<br><br>Aber kann es auch <em>handeln</em>?</div>

<!--
- Provokante Frage
- ChatGPT schreibt Texte, beantwortet Fragen — aber TUT es etwas?
- Es ist wie ein Gehirn im Glas: Es kann denken und reden, aber es hat keine Haende
- "Genau das schauen wir uns heute an."
-->

---
class: section-divider
---

## Vom Chatbot zum KI-Agenten

<!--
- Jetzt: Was ist der Unterschied?
- Einfach erklaert, ohne Technik-Jargon
-->

---

## Was kann ChatGPT?

<div class="card-grid cols-2" style="margin-top: 30px;">
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-pen-fancy"></i></div>
    <h3>Texte schreiben</h3>
    <p>Aufsaetze, E-Mails, Zusammenfassungen, Gedichte...</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-comments"></i></div>
    <h3>Fragen beantworten</h3>
    <p>Erklaerungen, Definitionen, Tipps und Ratschlaege</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-language"></i></div>
    <h3>Uebersetzen</h3>
    <p>Zwischen Sprachen uebersetzen, Texte umformulieren</p>
  </div>
  <div class="card">
    <div class="card-icon"><i class="fa-solid fa-lightbulb"></i></div>
    <h3>Ideen entwickeln</h3>
    <p>Brainstorming, kreative Vorschlaege, Konzepte</p>
  </div>
</div>

<!--
- Das kennen die Schueler bereits
- Kurz abhaken, nicht zu lange drauf verweilen
- Ueberleitung: "Super. Aber jetzt kommt das Aber..."
-->

---

## Was kann ChatGPT <span class="text-rot">nicht</span>?

<div class="card-grid cols-2" style="margin-top: 30px;">
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-folder-open"></i></div>
    <h3>Dateien erstellen</h3>
    <p>Kann keine Dokumente, Tabellen oder Websites auf eurem Rechner anlegen</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-gears"></i></div>
    <h3>Aufgaben ausfuehren</h3>
    <p>Kann nichts eigenstaendig erledigen — nur antworten, wenn ihr fragt</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-plug"></i></div>
    <h3>Mit Systemen arbeiten</h3>
    <p>Kann nicht auf Datenbanken, APIs oder andere Programme zugreifen</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-rotate"></i></div>
    <h3>Sich selbst pruefen</h3>
    <p>Kann nicht testen ob seine Antwort wirklich stimmt oder funktioniert</p>
  </div>
</div>

<!--
- Kernpunkt: ChatGPT ist "nur" ein Gespraechspartner
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
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">Weiss alles, kann aber nichts anfassen.<br>Ihr muesst alles selbst umsetzen.</p>
  </div>
  <div class="vs-label">vs.</div>
  <div class="card" style="text-align: center;">
    <div class="card-icon" style="font-size: 2.5em;"><i class="fa-solid fa-user-gear"></i></div>
    <h3>KI-Agent</h3>
    <p style="font-size: 0.85em;">Ein Experte <strong>bei euch im Buero</strong></p>
    <p style="font-size: 0.7em; color: var(--thm-mittelgrau);">Weiss alles UND legt direkt los.<br>Liest Dateien, schreibt Ergebnisse, nutzt Werkzeuge.</p>
  </div>
</div>

<!--
- Analogie ist der Schluessel zum Verstaendnis
- Chatbot = passiver Berater, Agent = aktiver Macher
- "Und wie macht der Agent das? Dazu gibt es ein einfaches Prinzip..."
-->

---

## Wie arbeitet ein KI-Agent?

<p class="text-large" style="margin-top: 10px;">Der Agent-Kreislauf: Denken, Handeln, Pruefen</p>

<div class="cycle-diagram">
  <div class="cycle-step">
    <span class="step-icon"><i class="fa-solid fa-clipboard-question"></i></span>
    <span class="step-label">Verstehen</span>
  </div>
  <span class="cycle-arrow"><i class="fa-solid fa-arrow-right"></i></span>
  <div class="cycle-step">
    <span class="step-icon"><i class="fa-solid fa-list-check"></i></span>
    <span class="step-label">Planen</span>
  </div>
  <span class="cycle-arrow"><i class="fa-solid fa-arrow-right"></i></span>
  <div class="cycle-step">
    <span class="step-icon"><i class="fa-solid fa-hammer"></i></span>
    <span class="step-label">Handeln</span>
  </div>
  <span class="cycle-arrow"><i class="fa-solid fa-arrow-right"></i></span>
  <div class="cycle-step">
    <span class="step-icon"><i class="fa-solid fa-magnifying-glass-chart"></i></span>
    <span class="step-label">Pruefen</span>
  </div>
</div>

<svg viewBox="0 0 800 50" style="width: 690px; height: 50px; display: block; margin: -5px auto 0;">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#80BA24"/>
    </marker>
  </defs>
  <path d="M 680 5 C 700 40, 700 45, 400 45 C 100 45, 100 40, 120 5"
        stroke="#80BA24" stroke-width="2.5" fill="none" marker-end="url(#arrowhead)" stroke-dasharray="8 4"/>
  <text x="400" y="38" text-anchor="middle" fill="#8FA0AA" font-size="13" font-family="Arial, sans-serif">Nicht gut genug? Nochmal von vorne</text>
</svg>

<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-lightbulb"></i> <strong>Wie ein guter Praktikant:</strong> Aufgabe lesen, Plan machen, umsetzen, pruefen ob alles stimmt — und nachbessern wenn noetig.</p>
</div>

<!--
- DAS ist der zentrale Unterschied: die Feedback-Schleife
- Ein Chatbot gibt EINE Antwort. Ein Agent arbeitet ITERATIV.
- Analogie Praktikant: Ihr gebt ihm eine Aufgabe, er arbeitet eigenstaendig
- "Und jetzt wird's richtig spannend: Was wenn MEHRERE Agenten zusammenarbeiten?"
-->

---

## Was wenn mehrere Agenten zusammenarbeiten?

<div class="card-grid cols-2" style="margin-top: 25px;">
  <div class="card card-grau" style="text-align: center;">
    <div class="card-icon" style="color: var(--thm-mittelgrau);"><i class="fa-solid fa-user"></i></div>
    <h3>Ein Alleskoenner</h3>
    <p>Eine KI soll alles allein machen: Marketing, Finanzen, Design, Technik...</p>
    <p style="font-size: 0.7em; color: var(--thm-rot); margin-top: 10px;"><i class="fa-solid fa-triangle-exclamation" style="color: var(--thm-rot);"></i> Ueberfordert, ungenau, langsam</p>
  </div>
  <div class="card" style="text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-users"></i></div>
    <h3>Ein Team von Spezialisten</h3>
    <p>Jeder Agent hat <strong>eine Rolle</strong> und ist darin richtig gut.</p>
    <p style="font-size: 0.7em; color: var(--thm-gruen); margin-top: 10px;"><i class="fa-solid fa-check-circle"></i> Wie in einem echten Unternehmen!</p>
  </div>
</div>

<div class="callout callout-blue" style="margin-top: 25px;">
  <p><i class="fa-solid fa-building" style="color: var(--thm-hellblau);"></i> <strong style="color: var(--thm-hellblau);">Genau wie in der Wirtschaft:</strong> Marketing-Abteilung, Finanzabteilung, Entwicklung — jeder macht das, was er am besten kann.</p>
</div>

<!--
- Analogie zum Unternehmen — das kennen die Schueler aus dem Wirtschaftsunterricht
- Arbeitsteilung ist ein Grundprinzip der Betriebswirtschaft
- "Und genau das machen wir jetzt live: 5 KI-Agenten, ein Produktlaunch!"
-->

---

## Warum ist das die Zukunft?

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
    <p>Agenten <strong>pruefen ihre Ergebnisse</strong> und verbessern sich selbst — ohne dass jemand eingreifen muss.</p>
  </div>
</div>
<div class="callout" style="margin-top: 20px;">
  <p><i class="fa-solid fa-forward"></i> <strong>Genau das testen wir jetzt live:</strong> 5 Agenten, ein Produktlaunch — in Minuten statt Wochen.</p>
</div>

<!--
- Ausblick in die Arbeitswelt der Schueler
- Assistenz -> Autonomie: Der Shift der gerade passiert
- Skalierbarkeit: 100 Agenten fuer Marktforschung, Kundenservice, Buchhaltung
- Selbstkorrektur: Fehlertoleranz durch Iteration (wie beim Agent-Kreislauf)
- "Und jetzt schauen wir uns das in der Praxis an!"
-->

---

## Das Experiment: Ship It!

<p class="text-large" style="margin-top: 10px;">Wir testen das jetzt live — mit einer App, die ich mitgebracht habe.</p>

<div class="callout" style="margin-top: 25px;">
  <p><i class="fa-solid fa-rocket"></i> <strong>Ship It!</strong> ist ein Dashboard, in dem <strong>5 KI-Agenten</strong> zusammenarbeiten, um ein Produkt auf den Markt zu bringen — Zielgruppenanalyse, Marketing, Social Media, Preiskalkulation und sogar eine fertige Website.</p>
</div>

<div style="margin-top: 25px;">
  <p style="font-size: 0.85em; margin-bottom: 12px;">So funktioniert es:</p>
  <ol>
    <li><strong>Ihr</strong> waehlt ein Produkt</li>
    <li>Die <strong>KI-Agenten</strong> uebernehmen den kompletten Produktlaunch</li>
    <li><strong>Wir</strong> schauen live zu und bewerten die Ergebnisse</li>
  </ol>
</div>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 25px;"><i class="fa-solid fa-comment-dots" style="color: var(--thm-mittelgrau);"></i> Das Einzige was die Agenten von euch brauchen: eine Produktidee in ganz normalem Deutsch.</p>

<!--
- Ship It! kurz erklaeren: Was ist das? Was passiert gleich?
- Keine Programmierung noetig — alles in natuerlicher Sprache (Bezug zur vorherigen Folie!)
- Die Agenten arbeiten eigenstaendig, wir schauen ihnen dabei zu
- "Also: Welches Produkt soll es sein?"
-->

---
class: interactive-slide
---

<div class="emoji">🚀</div>

## Jetzt seid ihr dran!

<p style="font-size: 1.1em; margin-top: 20px;">Welches Produkt sollen unsere<br>KI-Agenten auf den Markt bringen?</p>

<div class="product-grid">
  <div class="product-item">
    <div class="product-emoji">👟</div>
    <p>Nachhaltige Sneaker aus Apfelleder</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">⚡</div>
    <p>Energy Drink fuer Klausurphasen</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">📱</div>
    <p>App zum Tauschen von Schulbuechern</p>
  </div>
  <div class="product-item">
    <div class="product-emoji">🎧</div>
    <p>KI-Kopfhoerer, der Stimmung erkennt</p>
  </div>
</div>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 25px;">
  ...oder eure eigene Idee! Ruft rein — wir stimmen ab.
</p>

<!--
- Die 4 Starter-Ideen als Inspiration zeigen
- Schueler koennen eigene Ideen einbringen
- 2-3 Minuten Brainstorming, dann Abstimmung per Handzeichen
- Gewahltes Produkt in Ship It! eingeben (kurze Beschreibung tippen)
-->

---
class: section-divider
---

## Ship It!

<p style="font-size: 1.1em; margin-top: 15px;">Live-Demo: 5 KI-Agenten, 1 Produktlaunch</p>

<!--
- Ueberleitung zur Demo
- "Jetzt zeige ich euch, wie 5 KI-Agenten euer Produkt auf den Markt bringen."
-->

---

## Unsere 5 KI-Agenten

<div class="card-grid cols-5" style="margin-top: 25px;">
  <div class="card" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-users-viewfinder"></i></div>
    <h3 style="font-size: 0.75em;">Zielgruppen-Analyst</h3>
    <p style="font-size: 0.65em;">Wer kauft das Produkt? Personas erstellen</p>
  </div>
  <div class="card" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-bullhorn"></i></div>
    <h3 style="font-size: 0.75em;">Marketing-Experte</h3>
    <p style="font-size: 0.65em;">Name, Slogan, Werbetexte entwickeln</p>
  </div>
  <div class="card" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-hashtag"></i></div>
    <h3 style="font-size: 0.75em;">Social-Media-Manager</h3>
    <p style="font-size: 0.65em;">Posts fuer Instagram, LinkedIn, TikTok</p>
  </div>
  <div class="card" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-calculator"></i></div>
    <h3 style="font-size: 0.75em;">Controller</h3>
    <p style="font-size: 0.65em;">Preiskalkulation und Preisstrategie</p>
  </div>
  <div class="card" style="padding: 16px; text-align: center;">
    <div class="card-icon"><i class="fa-solid fa-code"></i></div>
    <h3 style="font-size: 0.75em;">Web-Entwickler</h3>
    <p style="font-size: 0.65em;">Produkt-Website mit HTML, CSS, JS</p>
  </div>
</div>

<!--
- Jeden Agenten kurz vorstellen, Rolle erklaeren
- "Die arbeiten wie Abteilungen in einem Unternehmen"
- Website-Agent ist besonders: baut etwas, das man im Browser oeffnen kann
-->

---

## Wer wartet auf wen?

<p style="margin-bottom: 20px;">Manche Agenten brauchen die Ergebnisse anderer, bevor sie starten koennen.</p>

<svg viewBox="0 0 900 310" style="width: 100%; max-width: 850px; height: auto; margin: 15px auto; display: block;">
  <defs>
    <marker id="dep-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#80BA24"/>
    </marker>
  </defs>
  <rect x="40" y="30" width="190" height="55" rx="10" fill="white" stroke="#80BA24" stroke-width="2"/>
  <text x="135" y="63" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#4A5C66">🎯 Zielgruppe</text>
  <line x1="230" y1="57" x2="295" y2="57" stroke="#80BA24" stroke-width="2.5" marker-end="url(#dep-arrow)"/>
  <rect x="300" y="30" width="190" height="55" rx="10" fill="white" stroke="#80BA24" stroke-width="2"/>
  <text x="395" y="63" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#4A5C66">📢 Marketing</text>
  <line x1="490" y1="57" x2="555" y2="57" stroke="#80BA24" stroke-width="2.5" marker-end="url(#dep-arrow)"/>
  <rect x="560" y="30" width="190" height="55" rx="10" fill="white" stroke="#80BA24" stroke-width="2"/>
  <text x="655" y="63" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#4A5C66"># Social Media</text>
  <rect x="40" y="150" width="190" height="55" rx="10" fill="white" stroke="#80BA24" stroke-width="2"/>
  <text x="135" y="183" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#4A5C66">🧮 Kalkulation</text>
  <text x="25" y="128" font-family="Arial" font-size="12" fill="#8FA0AA">starten sofort</text>
  <line x1="25" y1="132" x2="230" y2="132" stroke="#8FA0AA" stroke-width="1" stroke-dasharray="4 3"/>
  <rect x="340" y="230" width="210" height="55" rx="10" fill="white" stroke="#80BA24" stroke-width="3"/>
  <text x="445" y="263" text-anchor="middle" font-family="Arial" font-size="15" font-weight="bold" fill="#4A5C66">💻 Website</text>
  <path d="M 35 57 L 18 57 Q 8 57 8 67 L 8 250 Q 8 260 18 260 L 340 260"
        stroke="#80BA24" stroke-width="2" fill="none" marker-end="url(#dep-arrow)"/>
  <line x1="395" y1="85" x2="430" y2="230" stroke="#80BA24" stroke-width="2" marker-end="url(#dep-arrow)"/>
  <path d="M 230 190 Q 300 225 340 252"
        stroke="#80BA24" stroke-width="2" fill="none" marker-end="url(#dep-arrow)"/>
  <text x="570" y="263" font-family="Arial" font-size="12" fill="#8FA0AA">braucht alle Ergebnisse</text>
</svg>

<div class="callout" style="margin-top: 15px;">
  <p><i class="fa-solid fa-play-circle"></i> <strong>Zielgruppe</strong> und <strong>Kalkulation</strong> starten sofort — sie brauchen nur die Produktbeschreibung.</p>
</div>

<!--
- Zeigen: Abhaengigkeiten wie in einem echten Projekt
- Zielgruppe + Kalkulation starten parallel (sofort)
- Marketing wartet auf Zielgruppe
- Social Media wartet auf Marketing
- Website wartet auf alle
- "Jetzt starten wir! Dashboard oeffnen..."
-->

---
class: interactive-slide
---

<div class="emoji">🎬</div>

## Los geht's!

<p style="font-size: 1.1em; margin-top: 20px;">Wechsel zum <strong style="color: var(--thm-gruen);">Ship It! Dashboard</strong></p>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 30px;">
  <i class="fa-solid fa-arrow-right" style="color: var(--thm-mittelgrau);"></i> http://localhost:8000
</p>

<!--
- Browser wechseln, Dashboard zeigen
- Produkt eingeben
- Agenten nacheinander starten
- Zwischen den Ergebnissen: Vorhersage-Spiel (naechste Folien)
-->

---
class: interactive-slide
---

<div class="emoji">🤔</div>

## Vorhersage-Spiel

<div class="question-list">
  <ul>
    <li>Welche <strong style="color: var(--thm-gruen);">Zielgruppe</strong> wird die KI identifizieren?</li>
    <li>Welchen <strong style="color: var(--thm-gruen);">Slogan</strong> wuerdet IHR waehlen?</li>
    <li>Was schaetzt ihr als <strong style="color: var(--thm-gruen);">fairen Preis</strong>?</li>
  </ul>
</div>

<p style="font-size: 0.8em; color: var(--thm-mittelgrau); margin-top: 30px;">
  Mal sehen, ob die KI auf etwas Aehnliches kommt...
</p>

<!--
- Vorhersagen einsammeln BEVOR die Ergebnisse angeschaut werden
- Ggf. an die Tafel schreiben
- Dann: Ergebnisse im Dashboard aufrufen und vergleichen
- Erzeugt Spannung und Engagement
-->

---
class: section-divider
---

## Wie gut war die KI?

<p style="font-size: 1.1em; margin-top: 15px;">Zeit fuer eine ehrliche Bewertung</p>

<!--
- Uebergang zur kritischen Bewertung
- "Jetzt schauen wir mal genauer hin."
-->

---
class: interactive-slide
---

## Daumen hoch oder runter?

<div class="question-list">
  <ul>
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> Wuerdet ihr diesen <strong style="color: var(--thm-gruen);">Instagram-Post</strong> liken?</li>
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> Ist die <strong style="color: var(--thm-gruen);">Preiskalkulation</strong> realistisch?</li>
    <li><i class="fa-solid fa-thumbs-up" style="color: var(--thm-gruen);"></i> Wuerdet ihr auf dieser <strong style="color: var(--thm-gruen);">Website</strong> einkaufen?</li>
    <li><i class="fa-solid fa-trophy" style="color: var(--thm-gelb);"></i> Welcher Agent hat <strong style="color: var(--thm-gelb);">am besten</strong> gearbeitet?</li>
  </ul>
</div>

<!--
- Jede Frage einzeln durchgehen, Daumen hoch/runter
- Nachfragen: WARUM? Was genau stoert euch?
- "Was hat ueberrascht?"
- "Was fehlt offensichtlich?"
- "Wuerde ein echtes Unternehmen das so verwenden?"
-->

---

## Reality Check: Worauf muss man achten?

<div class="card-grid cols-2" style="margin-top: 25px;">
  <div class="card card-yellow">
    <div class="card-icon"><i class="fa-solid fa-coins" style="color: var(--thm-gelb);"></i></div>
    <h3>Kosten</h3>
    <p>KI arbeitet mit <strong style="color: var(--thm-gelb);">Tokens</strong> — das ist ihre Waehrung. Je nach Modell kostet das wenig oder richtig viel. Wer Agenten einsetzt, muss die Kosten im Blick behalten.</p>
  </div>
  <div class="card" style="border-top-color: var(--thm-hellblau);">
    <div class="card-icon" style="color: var(--thm-hellblau);"><i class="fa-solid fa-clipboard-check"></i></div>
    <h3 style="color: var(--thm-hellblau);">Qualitaetskontrolle</h3>
    <p>Wie stellt man sicher, dass die Ergebnisse <strong style="color: var(--thm-hellblau);">korrekt</strong> sind? Wenn alles manuell geprueft werden muss, wird <strong style="color: var(--thm-hellblau);">der Mensch zum Engpass</strong> — man braucht automatische Pruefmechanismen.</p>
  </div>
  <div class="card card-rot">
    <div class="card-icon"><i class="fa-solid fa-ghost"></i></div>
    <h3>Halluzinationen</h3>
    <p>KI kann <strong style="color: var(--thm-rot);">ueberzeugend falsche Dinge</strong> behaupten — erfundene Fakten, falsche Zahlen, nicht existierende Quellen. Das klingt plausibel, ist aber frei erfunden.</p>
  </div>
  <div class="card" style="border-top-color: var(--thm-grau);">
    <div class="card-icon"><i class="fa-solid fa-shield-halved"></i></div>
    <h3>Datenschutz</h3>
    <p>Daten, die an KI-Dienste gesendet werden, <strong>verlassen das Unternehmen</strong>. Vertrauliche Informationen gehoeren nicht in einen externen KI-Chat.</p>
  </div>
</div>

<!--
- Kein Hype ohne Reality Check
- Kosten: GPT-4 ca. 100x teurer als kleine Modelle. Agenten verbrauchen VIELE Tokens
- Qualitaet: Der Pruefschritt im Agent-Kreislauf ist entscheidend. Automatische Tests, Validierung
- Halluzinationen: Gerade bei Fakten, Zahlen, Quellen kritisch. Immer gegenchecken!
- Datenschutz: DSGVO, Betriebsgeheimnisse, personenbezogene Daten
- "Diese Herausforderungen muss man kennen — aber sie sind loesbar."
-->

---
class: section-divider
---

## Was nehmen wir mit?

<!--
- Uebergang zu den Kern-Learnings
- Von der Demo zur groesseren Botschaft
-->

---

## Der rote Faden

<div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-top: 35px;">
  <div class="card card-grau" style="text-align: center; flex: 1;">
    <div class="card-icon" style="font-size: 1.5em; color: var(--thm-mittelgrau);"><i class="fa-solid fa-database"></i></div>
    <h3 style="font-size: 0.85em;">Digitalisierung</h3>
    <p style="font-size: 0.7em;">...hat die Welt in Daten uebersetzt</p>
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
    <p style="font-size: 0.7em;">...handeln jetzt selbststaendig in dieser Welt</p>
  </div>
</div>

<div class="card-grid cols-3" style="margin-top: 25px;">
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-screwdriver-wrench"></i> Werkzeug, kein Ersatz</h3>
    <p style="font-size: 0.7em;">Der Mensch bleibt verantwortlich — <strong>jemand muss pruefen</strong>.</p>
  </div>
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-people-group"></i> Arbeitsteilung</h3>
    <p style="font-size: 0.7em;">Spezialisierte Agenten — <strong>wie in echten Unternehmen</strong>.</p>
  </div>
  <div class="card" style="text-align: center; padding: 16px;">
    <h3 style="font-size: 0.8em;"><i class="fa-solid fa-gauge-high"></i> Schnell ≠ gut</h3>
    <p style="font-size: 0.7em;">Qualitaet braucht <strong>menschliches Urteil</strong>.</p>
  </div>
</div>

<!--
- Den roten Faden der Vorlesung zusammenfassen
- Digitalisierung -> LLMs -> Agenten: drei aufeinander aufbauende Schritte
- Die drei Learnings aus der Demo nochmal kurz
- Ueberleitung: "Und was bedeutet das fuer EUCH?"
-->

---
class: statement-slide
---

<div class="big-text" style="font-size: 1.4em;">Ihr werdet in einer Welt arbeiten, in der ihr nicht mehr nur lernt, wie man Aufgaben <em>selbst ausfuehrt</em> —<br><br>sondern wie man Agenten steuert, die diese Aufgaben <em>fuer euch loesen</em>.</div>

<!--
- Die zentrale Botschaft der Vorlesung
- Kurz wirken lassen, nicht sofort weiterreden
- Dann: "Was denkt ihr darueber?"
-->

---
class: interactive-slide
---

## Was denkt ihr?

<div class="question-list">
  <ul>
    <li>Veraendert KI eure <strong style="color: var(--thm-gruen);">zukuenftigen Berufe</strong>? Wie?</li>
    <li>Was kann KI gut — und was wird sie <strong style="color: var(--thm-gruen);">nie koennen</strong>?</li>
    <li>Wem <strong style="color: var(--thm-gruen);">gehoeren</strong> die Ergebnisse, die eine KI erstellt?</li>
  </ul>
</div>

<!--
- Offene Diskussion, 5-8 Minuten
- Keine "richtige" Antwort — es geht ums Nachdenken
- Bei Frage 1: Berufe veraendern sich, aber verschwinden selten komplett
- Bei Frage 2: Kreativitaet, Empathie, ethische Entscheidungen
- Bei Frage 3: Urheberrecht, wer ist verantwortlich?
- Schueler zum Sprechen ermutigen
-->

---

## Euer naechster Schritt?

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
- StudiumPlus als Option erwaehnen
- "Wenn euch das heute gefallen hat, koennt ihr sowas auch studieren!"
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
