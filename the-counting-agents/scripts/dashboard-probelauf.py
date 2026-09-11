#!/usr/bin/env python3
"""dashboard-probelauf.py — Füttert den Bus, damit sich das Dashboard
ansehen lässt, ohne dass Agenten laufen.

Gedacht für die Generalprobe: Beamer anschließen, Schriftgrößen und Farben aus
der letzten Reihe prüfen, den Fokus-Klick einmal vorführen — alles ohne Modell,
ohne Netz, ohne Kosten. Ein Simulator zählt hoch, die drei Sammler hinken
unterschiedlich weit hinterher, prime wird zwischendurch pausiert und
vergreift sich gelegentlich an einer Zahl.

    ./scripts/dashboard-probelauf.py     in einem Pane
    ./scripts/dashboard.py               in einem zweiten

Läuft bis Strg-C und schreibt dabei in `_bus/` und `_state/` — dieselben
Dateien, die auch die echten Agenten benutzen. Deshalb NICHT parallel zu
einem laufenden `./scripts/start.sh` aufrufen.
"""

import json
import os
import random
import sys
import time
from datetime import datetime, timezone

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUS = os.path.join(PROJECT_DIR, "_bus")
STATE = os.path.join(PROJECT_DIR, "_state")

TAKT = 1.5  # Sekunden pro Zahl — etwa das Tempo der echten Agenten


def now():
    return datetime.now(timezone.utc).isoformat()


def is_prime(n):
    if n < 2:
        return False
    for f in range(2, int(n ** 0.5) + 1):
        if n % f == 0:
            return False
    return True


def append(name, event):
    with open(os.path.join(BUS, name), "a", encoding="utf8") as f:
        f.write(json.dumps(event) + "\n")


def write_state(agent, data):
    data["updated_at"] = now()
    with open(os.path.join(STATE, "%s.json" % agent), "w", encoding="utf8") as f:
        f.write(json.dumps(data) + "\n")


def main():
    os.makedirs(BUS, exist_ok=True)
    os.makedirs(STATE, exist_ok=True)
    log = os.path.join(BUS, "numbers.log")
    if os.path.exists(log) and os.path.getsize(log) > 0:
        antwort = input("Im Bus stehen schon Zahlen. Alles löschen? [j/N] ")
        if antwort.strip().lower() not in ("j", "ja"):
            print("Abgebrochen.")
            return

    open(os.path.join(BUS, "numbers.log"), "w").close()
    open(os.path.join(BUS, "control.log"), "w").close()
    for agent in ("counter", "odd", "even", "prime"):
        try:
            os.remove(os.path.join(STATE, "%s.json" % agent))
        except OSError:
            pass

    print("Probelauf läuft — Dashboard in einem anderen Pane starten.")
    print("Beenden mit Strg-C.\n")

    # Jeder Sammler zieht mit eigener Verzögerung nach. Genau das macht das
    # Dashboard sichtbar und die Terminalausgaben nicht.
    sammler = {
        "odd":   {"filter": lambda n: n % 2 == 1, "verzug": 1, "numbers": [], "last_seq": 0},
        "even":  {"filter": lambda n: n % 2 == 0, "verzug": 2, "numbers": [], "last_seq": 0},
        "prime": {"filter": is_prime,             "verzug": 4, "numbers": [], "last_seq": 0},
    }
    pausiert = set()

    seq = 0
    try:
        while True:
            seq += 1
            append("numbers.log", {"type": "number", "seq": seq,
                                   "value": seq, "timestamp": now()})
            write_state("counter", {"agent": "counter", "last_value": seq,
                                    "status": "running"})

            for name, s in sammler.items():
                if name in pausiert:
                    continue
                ziel = seq - s["verzug"]
                if ziel > s["last_seq"]:
                    for n in range(s["last_seq"] + 1, ziel + 1):
                        if s["filter"](n):
                            s["numbers"].append(n)
                    # Ab und zu vertut sich das Modell — auch das soll man sehen.
                    if name == "prime" and random.random() < 0.04 and ziel > 8:
                        s["numbers"].append(ziel if ziel % 2 else ziel + 1)
                    s["last_seq"] = ziel
                    write_state(name, {"agent": name, "last_seq": ziel,
                                       "numbers": sorted(set(s["numbers"])),
                                       "count": len(set(s["numbers"]))})

            if seq == 14:
                append("control.log", {"type": "control", "target": "prime",
                                       "command": "pause", "timestamp": now()})
                pausiert.add("prime")
                print("  → prime pausiert")
            if seq == 24:
                append("control.log", {"type": "control", "target": "prime",
                                       "command": "resume", "timestamp": now()})
                pausiert.discard("prime")
                print("  → prime läuft weiter")

            print("  Zahl %d im Bus" % seq)
            time.sleep(TAKT)
    except KeyboardInterrupt:
        print("\nProbelauf beendet. Aufräumen mit ./scripts/reset.sh")


if __name__ == "__main__":
    sys.exit(main())
