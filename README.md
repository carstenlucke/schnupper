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

### [`the-counting-agents/`](the-counting-agents/)

Terminalbasierte Demo eines Multi-Agenten-Systems. Fünf autonome Agenten
(Counter, Odd, Even, Prime, Control) kommunizieren ausschließlich über
dateibasierte Append-only-Event-Logs und laufen nebeneinander in einer
tmux-Session — das Zusammenspiel wird dadurch direkt sichtbar.

```bash
cd the-counting-agents && ./scripts/start.sh
```

## Aufbau

Jedes Projekt ist eigenständig: eigenes README, eigene Konfiguration, eigene
Skripte. Es gibt keinen gemeinsamen Build und keine geteilten Dependencies —
ein Projekt lässt sich unabhängig von den anderen starten.

## Historie

Beide Projekte wurden aus eigenständigen Repositories übernommen; ihre
vollständige Git-Historie ist erhalten und auf die neuen Pfade umgeschrieben:

```bash
git log -- ship-it/
git log --follow -- ship-it/server.py
```
