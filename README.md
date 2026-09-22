# Schnupper

Monorepo mit Projekten für Schnuppervorlesungen — Demonstrationen zu KI und
KI-Agenten für Schülerinnen und Schüler.

## Projekte

### [`ship-it/`](ship-it/)

Live-Demo für eine 90-minütige Schnuppervorlesung bei StudiumPlus. Die
Teilnehmenden wählen ein Produkt, fünf KI-Agenten erledigen den kompletten
Produktlaunch — von der Zielgruppenanalyse bis zur fertigen Landingpage.
Web-App in Python, ohne externe Dependencies.

```bash
cd ship-it && ./start.sh
```

### [`the-counting-agents/`](the-counting-agents/)

Terminalbasierte Demo eines Multi-Agenten-Systems. Fünf autonome Agenten
(Counter, Odd, Even, Prime, Control) kommunizieren ausschließlich über
dateibasierte Append-only-Event-Logs und laufen nebeneinander in einem
Herdr-Tab, jeder in einem eigenen benannten Pane — das Zusammenspiel wird
dadurch direkt sichtbar.

Laufzeit ist die [pi CLI](https://pi.dev) mit einem Modell in der Cloud und
**eigenen Werkzeugen**: Die Agenten haben keine eingebauten Werkzeuge wie
`bash` oder `write`, sondern nur `bus_publish`, `bus_read`, `control_read`,
`control_send`, `state_read` und `state_write`. Im Pane steht dadurch
`bus_publish {"value": 42}` statt einer Shell-Zeile, und jeder Agent kann genau
das, was seine Rolle verlangt.

```bash
cd the-counting-agents && ./scripts/start.sh
```

### [`agent-party/`](agent-party/)

Web-Demo, die den Spieß umdreht: Statt fertigen Agenten zuzusehen, bauen die
Teilnehmenden sie selbst. Sie schreiben Rollenprofile — von Hand oder von einem
Sprachmodell ausarbeiten lassen —, stellen daraus eine Besetzung zusammen und
geben ihr ein Thema. Danach diskutieren die gewählten Profile reihum, Beitrag
für Beitrag im Browser sichtbar.

Ein Profil ist eine Markdown-Datei, deren Text **wörtlich** zum Systemprompt
wird. Wer im Vortrag einen Satz darin ändert und dieselbe Party neu startet,
sieht die Diskussion kippen — das ist die ganze Pointe. Die Agenten haben
bewusst **keine Werkzeuge** und **kein Gedächtnis**: Der Gesprächsverlauf geht
jedes Mal neu als Text in den Prompt.

```bash
cd agent-party && ./start.sh
```

### [`presentation/`](presentation/)

Die Slidev-Präsentation zur Schnuppervorlesung „Digitalisierung und KI — Was
Maschinen schon können". Sie liegt auf oberster Ebene, weil jede der Demos
darin ihren Platz haben kann: Von einer Übersichtsfolie aus springt man in
die Demo, die man zeigen will, und von dort wieder zurück. Gestaltet nach dem Design-System „THM & StudiumPlus", das als lokales
Slidev-Theme unter `presentation/theme-thm/` mitgeliefert wird.

```bash
cd presentation && npm install && npm run dev
```

## Aufbau

Jedes Projekt ist eigenständig: eigenes README, eigene Konfiguration, eigene
Skripte. Es gibt keinen gemeinsamen Build und keine geteilten Dependencies —
ein Projekt lässt sich unabhängig von den anderen starten.

## Historie

`ship-it/` und die ursprüngliche Fassung von `the-counting-agents/` wurden aus
eigenständigen Repositories übernommen; ihre vollständige Git-Historie ist
erhalten und auf die neuen Pfade umgeschrieben:

```bash
git log -- ship-it/
git log --follow -- ship-it/server.py
```

Die ursprüngliche Fassung der Counting-Agents-Demo lief mit OpenCode und einem
lokalen Modell in LM Studio. Sie ist entfernt; die pi-Fassung, zuvor
`the-counting-agents-pi-herdr/`, trägt jetzt ihren Namen. Code und Tags
`the-counting-agents/v0.1.x` der OpenCode-Fassung bleiben in der Historie; der
letzte Stand liegt in Commit `4d77661`:

```bash
git show 4d77661:the-counting-agents/README.md
git log --follow -- the-counting-agents/scripts/start.sh   # Verlauf der pi-Fassung
```
