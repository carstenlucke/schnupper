# Schnupper

Monorepo mit Projekten für Schnuppervorlesungen — Demonstrationen zu KI und
KI-Agenten für Schülerinnen und Schüler.

## Projekte

### [`ship-it/`](ship-it/)

Live-Demo für eine 90-minütige Schnuppervorlesung bei StudiumPlus. Die
Teilnehmenden wählen ein Produkt, fünf KI-Agenten erledigen den kompletten
Produktlaunch — von der Zielgruppenanalyse bis zur fertigen Landingpage.
Enthält die Web-App (Python, ohne externe Dependencies) sowie eine begleitende
Slidev-Präsentation.

```bash
cd ship-it && ./start.sh
```

### [`the-counting-agents-pi-herdr/`](the-counting-agents-pi-herdr/)

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
cd the-counting-agents-pi-herdr && ./scripts/start.sh
```

## Aufbau

Jedes Projekt ist eigenständig: eigenes README, eigene Konfiguration, eigene
Skripte. Es gibt keinen gemeinsamen Build und keine geteilten Dependencies —
ein Projekt lässt sich unabhängig von den anderen starten.

## Historie

`ship-it/` und `the-counting-agents/` wurden aus eigenständigen Repositories
übernommen; ihre vollständige Git-Historie ist erhalten und auf die neuen Pfade umgeschrieben:

```bash
git log -- ship-it/
git log --follow -- ship-it/server.py
```

`the-counting-agents/`, die ursprüngliche Fassung der Counting-Agents-Demo mit
OpenCode und einem lokalen Modell in LM Studio, ist inzwischen entfernt. Code
und Tags `the-counting-agents/v*` bleiben in der Historie; der letzte Stand
liegt in Commit `4d77661`:

```bash
git log -- the-counting-agents/
git show 4d77661:the-counting-agents/README.md
```
