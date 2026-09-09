# Technical Debt

Bekannte Probleme, die bewusst nicht behoben wurden. Ship It! ist eine **Localhost-Demo-App für eine 90-minütige Schnuppervorlesung** – kein Produktionssystem. Die hier dokumentierten Punkte sind in diesem Kontext akzeptabel.

## 1. Unbounded Output-Buffer

**Problem:** Der Prozess-Output wird unbegrenzt in `running_processes[key]["output"]` (Liste von Strings) gesammelt und nach Prozessende nicht bereinigt. Bei vielen oder lang laufenden Agenten wächst der Speicherverbrauch stetig.

**Potentieller Fix:**
- Output als Ringbuffer mit maximaler Größe implementieren (z.B. `collections.deque(maxlen=10000)`)
- Abgeschlossene Prozesse nach einer TTL aus `running_processes` entfernen
- Output nach vollständigem Stream-Read verwerfen

**Warum nicht gefixt:** Die App läuft lokal für eine einzige Vorlesung (90 Min) mit wenigen Projekten und 5 Agenten. Der Speicherverbrauch ist in diesem Szenario vernachlässigbar – ein Agent produziert typischerweise wenige KB Output. Ein Neustart des Servers (Ctrl+C → `./start.sh`) setzt alles zurück.

## 2. CORS-Header `Access-Control-Allow-Origin: *`

**Problem:** Alle API-Endpunkte (JSON + Datei-Content) setzen `Access-Control-Allow-Origin: *`. Da das Frontend vom selben Origin (`localhost:8000`) ausgeliefert wird, ist CORS eigentlich nicht nötig. Der Wildcard-Header erlaubt es theoretisch fremden Webseiten, die API zu lesen und Aktionen auszulösen (Projekte auslesen, Agenten starten, Dateien löschen).

**Potentieller Fix:**
- CORS-Header komplett entfernen (Same-Origin braucht kein CORS)
- Oder auf den eigenen Origin beschränken: `Access-Control-Allow-Origin: http://localhost:8000`
- Zusätzlich CSRF-Token für state-changing Requests (POST, DELETE)

**Warum nicht gefixt:** Der Server läuft nur lokal auf dem Rechner des Dozenten, nicht im Netzwerk exponiert. Es gibt keine sensiblen Daten – nur von Schülern eingegebene Produktideen und KI-generierte Artefakte. Die CORS-Header können beim Debugging (z.B. Zugriff von einem anderen lokalen Port) sogar hilfreich sein.
