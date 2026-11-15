# Release v1.2.0 – Schnupper

Dieses Release stellt alle Demos auf die Modellgeneration GPT-6.1 um, bringt The Counting Agents in die Herdr-App und lässt „Aufbau eines KI-Agenten“ Klick für Klick entstehen.

## Präsentation

- **Aufbau eines KI-Agenten Klick für Klick:** Das Bild entsteht jetzt in sieben Klicks. Zuerst steht das Modell in der Mitte, dann legt sich das Harness darum, danach kommen die Werkzeuge und einzeln die vier Bausteine der Steuerung. Eine Zeile darunter erklärt, was gerade dazukommt; am Ende wird sie zum Merksatz „Das Harness macht den Unterschied.“ Unter den Werkzeugen steht nun „und viele mehr: E-Mail, Kalender …“, denn die vier gezeigten sind nur Beispiele.
- **„Vom Code zur Sprache“ eröffnet den ersten Teil:** Die Folie folgt jetzt auf die Agenda und trägt die Rubrik „Vom Chatbot zum KI-Agenten“.
- **Vom Absatz zum ganzen Referat:** Ein gemeinsamer Rahmen fasst die beiden Runden ein, die schon beim Kürzen von Absatz 3 zu sehen waren. Die Beschriftung lautet „wie beim Absatz kürzen“ und verweist so auf die Folie „Ein Agent bei der Arbeit“.
- **Warum Agenten gerade so gefragt sind:** Die Selbstkorrektur rückt an die zweite Stelle. Agenten prüfen ihre Ergebnisse und bessern nach, bevor sie sie vorlegen – die Prüfung durch euch entfällt dadurch nicht.
- **Aktuelle Modellnamen:** Die Folie zu Modellen und Apps nennt GPT-6.1 mit den Varianten Sol und Terra.
- **Neue Frage zur Agent Party:** In der Nachbesprechung heißt es jetzt „Wer hält die Fäden in der Hand – die KI oder wer das Profil schreibt?“

## Demos

### Ship It!

- **Neue Modelle:** Vier Agenten arbeiten mit GPT-6.1 Terra, der Website-Agent mit dem größeren GPT-6.1 Sol. Logo und Instagram-Bild entstehen mit `gpt-image-2.6-sunburst`.
- **Agentendatei hat Vorrang:** Das Modell eines Agenten steht in seiner Datei und gilt auch dann, wenn in der `.env` ein Modell eingetragen ist. `SHIP_IT_MODEL` greift nur noch für Agenten ohne eigenen Eintrag.
- **Kosten neu gemessen:** Die Kostentabelle im README beruht auf gemessenen Tokens. Ein Projekt mit Logo und Instagram-Bild kostet rund $0.06, eine Vorlesung mit etwa zehn Projekten rund $0.60.

### The Counting Agents

- **Herdr-App und Herdr-TUI:** Die Demo läuft in beiden und erkennt selbst, wo sie gestartet wurde. In der App sieht der Tab etwas anders aus, weil sich Panes dort nur halbieren lassen.
- **Robusterer Start:** Bricht der Aufbau ab, wird der halb angelegte Tab wieder geschlossen.
- **Neues Modell:** Voreingestellt ist GPT-6.1 Terra.

### Agent Party

- **Neues Modell:** Die mitgelieferten Profile und neu angelegte Profile nutzen GPT-6.1 Terra.

## Für den Vortrag

- `./start-all.sh` lässt seinen eigenen Tab vorne, während The Counting Agents im Hintergrund startet, auch in der Herdr-App. Die Übersicht bleibt sichtbar und Ctrl+C beendet weiterhin alles.
