# Release v1.0.0 – Schnupper

Erstes gemeinsames Release des Repositorys. Es umfasst die Präsentation „Vom Chatbot zum KI-Agenten“ und die drei Demos, welche sich aus ihr heraus zeigen lassen. Bisher erhielt jedes Projekt eigene Releases, zuletzt `ship-it/v1.0.1`; ab dieser Version gibt es eine Versionsnummer für alles, und derselbe Tag veröffentlicht zugleich die Präsentation als Web-App und als PDF.

## Präsentation

- Foliensatz für eine Schnuppervorlesung von 90 Minuten, gestaltet nach dem Design-System „THM & StudiumPlus“.
- Eine Übersichtsfolie führt in die gewünschte Demo. Am Ende einer Demo geht es zurück zur Übersicht oder weiter zum Schluss.
- Die Folien laufen als Web-App unter [carstenlucke.github.io/schnupper](https://carstenlucke.github.io/schnupper/). Die Schlussfolie führt per QR-Code dorthin und zum Repository; das PDF hängt an diesem Release.

## Demos

### Ship It!

Fünf Agenten führen einen Produktlaunch durch, von der Zielgruppe bis zur Website.

- Die Agenten laufen über die pi CLI statt über OpenCode.
- Vor dem Start der Website lässt sich eine von 54 Design-Vorlagen wählen oder die Gestaltung freigeben.
- Die Website zeigt nur öffentliche Inhalte, d.h. Kalkulation, Preisstrategie und Marktanalyse bleiben intern.
- Das Instagram-Bild übernimmt das Logo aus dem Marketingkonzept.
- Hell- und Dunkelmodus folgen dem THM-Corporate-Design.

### The Counting Agents

Fünf Agenten zählen gemeinsam und verständigen sich dabei nur über Dateien.

- Neue Fassung mit der pi CLI und einem Modell in der Cloud; jeder Agent läuft in einem eigenen Pane eines Herdr-Tabs.
- Die Agenten haben keine allgemeinen Werkzeuge wie `bash`, sondern nur solche, die ihre Rolle verlangt.
- Ein Dashboard für den Beamer zeigt den Ablauf und auf Knopfdruck den Prompt jedes Agenten im Wortlaut.

### Agent Party (neu)

Die Teilnehmenden schreiben die Agenten selbst: Rollenprofile in normalem Deutsch, daraus eine Besetzung, dazu ein Thema. Die Profile diskutieren anschließend reihum.

- Die Gesprächsleitung kann eingreifen – per Zwischenruf, weiterer Runde oder Fazit.
- Partys lassen sich bearbeiten und auf den Start zurücksetzen; Profile sind in Gruppen geordnet.
- Mitgeliefert sind u.a. drei Profile für ein Vorstellungsgespräch um einen dualen Studienplatz.

## Für den Vortrag

- `./start-all.sh` startet alle drei Demos und die Präsentation mit einem Aufruf; Ctrl+C beendet alles wieder.
