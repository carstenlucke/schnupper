# Das Experiment: Warum so minimalistisch?

## Worum geht es?

Dieses Projekt ist ein **Experiment**, kein Produktivsystem. Die zentrale Frage lautet:

> Wie weit kommt man mit einem Multi-Agenten-System, das **praktisch keinen Programmieraufwand** erfordert?

Das gesamte Projekt besteht aus Markdown-Definitionen für die Agenten, einer Handvoll Shell-Skripten und JSON-Dateien. Kein Framework, keine Bibliothek, kein eigener Code, der Geschäftslogik implementiert — die LLM-Agenten **sind** die Logik. Das Setup zeigt, dass koordinierte autonome Agenten heute mit minimalem Aufwand realisierbar sind.

Gleichzeitig ist dies eine **praktische Evaluation konkreter Werkzeuge**: [opencode](https://github.com/opencode-ai/opencode) als CLI für die Agentenausführung und [tmux](https://github.com/tmux/tmux) als Laufzeitumgebung, die mehrere Agenten parallel sichtbar macht. Beide Tools werden hier gezielt auf ihre Eignung in Multi-Agenten-Szenarien getestet.

Daraus ergibt sich eine zweite Frage:

> Können sich diese Agenten sinnvoll über ein Dateisystem koordinieren — ohne Message Broker, ohne Infrastruktur?

Die Antwort auf beide Fragen lautet: Ja, für bestimmte Szenarien. Und genau das zu zeigen, ist der Zweck dieses Projekts.

## Bewusste Entscheidungen, keine Versäumnisse

Jede „technische Schuld" in diesem Projekt ist eine bewusste Entscheidung. Hier sind die wichtigsten:

### Log-Dateien vollständig lesen

Die Consumer-Agenten (odd, even, prime) lesen bei **jedem Zyklus die gesamte `bus/numbers.log`** und filtern im Speicher nach `seq > last_seq`.

**Was eine echte Message Queue anders machen würde:**
- Consumer lesen nur neue Nachrichten ab einem serververwalteten Offset
- Backpressure und Flow Control sind eingebaut
- Zustellgarantien (at-least-once, exactly-once) sind Teil des Protokolls
- Skalierung ist O(1) pro Nachricht, nicht O(n) pro Lesezyklus

**Warum wir es trotzdem so machen:**
- Maximale Transparenz — `cat bus/numbers.log` zeigt den kompletten Systemzustand
- Kein zusätzlicher Prozess (Broker) nötig, der laufen und überwacht werden muss
- Debugging ist trivial: Dateien lesen, fertig
- Das Datenvolumen ist in diesem Demo-Kontext irrelevant (hunderte Zeilen, nicht Millionen)

### Keine Acknowledgements, kein Locking

Es gibt keinen Mechanismus, der garantiert, dass eine Nachricht genau einmal verarbeitet wird. Ein Agent könnte zwischen Lesen und State-Update abstürzen — und beim Neustart Nachrichten doppelt verarbeiten oder überspringen.

**Warum das hier in Ordnung ist:** Die Agenten zählen Zahlen. Ein fehlender oder doppelter Wert ist kein Datenverlust — es ist eine Beobachtung.

### Append-Only ohne Rotation

Die Log-Dateien wachsen unbegrenzt. Es gibt keine Log-Rotation, keine Kompaktierung, kein Aufräumen.

**Warum das hier in Ordnung ist:** Ein `./scripts/reset.sh` setzt alles zurück. Das System läuft Minuten bis Stunden, nicht Wochen.

### Kein Schema Registry, keine Versionierung

Die Event-Formate sind implizit in den Agentendefinitionen definiert, nicht in einem zentralen Schema.

**Warum das hier in Ordnung ist:** Fünf Agenten, zwei Event-Typen, ein Entwickler. Die Komplexität eines Schema-Managements würde den eigentlichen Zweck des Experiments überlagern.

## Was das Experiment zeigt

### 1. LLM-Agenten brauchen weniger Infrastruktur als gedacht

Ein `echo '...' >> file.log` reicht als Kommunikationskanal. Die Agenten sind robust genug, um mit diesem primitiven Mechanismus zuverlässig zu arbeiten.

### 2. Event Sourcing funktioniert auch mit Dateien

Das Muster — unveränderliche Events, Consumer leiten ihren Zustand daraus ab — ist architektonisch solide. Ob der Speicher ein Dateisystem oder Kafka ist, ändert nichts am Prinzip.

### 3. Die Grenzen werden sichtbar

Der Prime-Agent hinkt absichtlich hinterher. Genau das macht Unterschiede in der Verarbeitungsgeschwindigkeit beobachtbar — etwas, das hinter Abstraktionen in einer echten Queue verschwinden würde.

## Was dieses Projekt nicht ist

- **Keine Architekturvorlage** für Produktivsysteme
- **Kein Beweis**, dass man keine Message Queues braucht
- **Keine Best Practice** für Agentenkommunikation

Es ist ein Experiment, das zeigt, wie wenig Infrastruktur autonome Agenten mindestens brauchen — und wo die Grenzen dieses Minimalismus liegen.

## Wann man es anders machen sollte

Sobald eines dieser Kriterien zutrifft, reicht dateibasierte Kommunikation nicht mehr aus:

- **Langlebige Systeme**: Das System soll Tage oder Wochen laufen → Log-Rotation, Kompaktierung
- **Viele Consumer**: Mehr als eine Handvoll Agenten lesen denselben Bus → Broker mit Fan-out
- **Zuverlässigkeit**: Nachrichtenverlust ist nicht tolerierbar → Acknowledgements, Idempotenz
- **Verteilte Systeme**: Agenten laufen auf verschiedenen Maschinen → netzwerkfähiger Broker
- **Skalierung**: Tausende Events pro Sekunde → Kafka, Redis Streams, NATS
