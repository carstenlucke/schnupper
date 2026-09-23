"""dashboard_data.py — Liest Bus, Zustand und Agentendateien der Zähl-Agenten.

Die Auswertung hinter `dashboard.py`: Aus den beiden Logdateien und den
Zustandsdateien wird ein einziger Schnappschuss, den die Oberfläche nur noch
anzeigen muss. Dazu kommen die Agentendateien selbst, damit das Dashboard
zeigen kann, was jeder Agent als Auftrag bekommt. Getrennt gehalten, damit die
Darstellung sich ändern kann, ohne dass jemand an der Auswertung dreht.

Nur Standardbibliothek: keine Installation, kein Build, kein `pip`.

Gelesen wird ausschließlich. Das Dashboard läuft neben den Agenten und darf
weder Bus noch Zustand verändern.
"""

import json
import os
import time
from datetime import datetime, timezone

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUMBERS_LOG = os.path.join(PROJECT_DIR, "_bus", "numbers.log")
CONTROL_LOG = os.path.join(PROJECT_DIR, "_bus", "control.log")
STATE_DIR = os.path.join(PROJECT_DIR, "_state")

AGENTS_DIR = os.path.join(PROJECT_DIR, "agents")
ENV_FILE = os.path.join(PROJECT_DIR, ".env")

COLLECTORS = ("odd", "even", "prime")
AGENTS = ("counter",) + COLLECTORS
# Die Steuerung hat keinen Zustand und keine Zeile im Dashboard, aber eine
# Agentendatei wie die anderen — und die soll man zeigen können.
AGENT_FILES = AGENTS + ("control",)

# Sobald ein Agent so lange nichts mehr geschrieben hat, gilt er als stumm.
# Ein Durchlauf dauert wenige Sekunden; 25 s sind also ein echter Hänger und
# nicht bloß eine lange Modellantwort.
STILL_AFTER_SECONDS = 25


def _read_log(path):
    """Liest eine JSONL-Datei. Fehlende Datei, leere Datei und halb
    geschriebene Zeilen ergeben weniger Ereignisse, nie einen Fehler —
    wir lesen ja mitten im Schreibbetrieb."""
    events = []
    try:
        with open(path, "r", encoding="utf8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass  # Zeile war noch nicht fertig geschrieben.
    except OSError:
        return []
    return events


def _read_state(agent):
    path = os.path.join(STATE_DIR, "%s.json" % agent)
    try:
        with open(path, "r", encoding="utf8") as handle:
            raw = handle.read().strip()
    except OSError:
        return {}
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except ValueError:
        return {}


def _parse_ts(value):
    """ISO-Zeitstempel der Werkzeuge in Sekunden seit Epoche."""
    if not value:
        return None
    try:
        text = value.replace("Z", "+00:00")
        stamp = datetime.fromisoformat(text)
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        return stamp.timestamp()
    except ValueError:
        return None


def _is_prime(n):
    """Dient nur dem Abgleich: Was hätte der Prim-Agent einsammeln müssen?
    Entschieden wird im Betrieb weiterhin vom Modell — hier wird nachgerechnet,
    damit sichtbar wird, wenn es sich vertan hat."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def _last_reset(control_events, agent):
    """Zeitpunkt des letzten Resets, der für diesen Agenten gilt."""
    last = None
    for event in control_events:
        if event.get("command") != "reset":
            continue
        if event.get("target") in (agent, "all"):
            last = event.get("timestamp")
    return last


def _operating_status(control_events, agent):
    """Was für diesen Agenten gerade gilt — dieselbe Auswertung wie im
    Werkzeug `control_read` und in der Schleife von `run-agent.sh`:
    Befehle an den Agenten und an `all`, spätere überschreiben frühere."""
    status = "running"
    verbose = False
    for event in control_events:
        if event.get("target") not in (agent, "all"):
            continue
        command = event.get("command")
        if command in ("pause", "resume", "stop", "reset"):
            status = {"pause": "paused", "resume": "running",
                      "stop": "stopped", "reset": "running"}[command]
        elif command == "verbose":
            verbose = True
        elif command == "quiet":
            verbose = False
    return status, verbose


def _seconds_per_number(numbers):
    """Takt des Zählers aus den letzten Zahlen. None, solange es zu wenige gibt."""
    stamps = [t for t in (_parse_ts(n.get("timestamp")) for n in numbers[-10:]) if t]
    if len(stamps) < 2:
        return None
    span = stamps[-1] - stamps[0]
    return span / (len(stamps) - 1) if span > 0 else None


def agent_file(agent):
    """Die Agentendatei im Wortlaut: Frontmatter und Systemprompt.

    Nur für die bekannten Agenten — der Name kommt aus der URL, und ohne diese
    Prüfung ließe sich mit `../` jede Datei auf der Platte abrufen. Gibt None
    zurück, wenn der Name unbekannt ist oder die Datei fehlt."""
    if agent not in AGENT_FILES:
        return None
    try:
        with open(os.path.join(AGENTS_DIR, "%s.md" % agent), "r", encoding="utf8") as handle:
            return handle.read()
    except OSError:
        return None


def model_override():
    """Das Modell aus `COUNTING_AGENTS_MODEL`, oder None.

    Es schlägt den `model:`-Eintrag aller Agentendateien (siehe `agent_model`
    in agents-lib.sh). Maßgeblich ist wie dort die `.env`, die das Startskript
    per `source` einliest; ohne Eintrag dort gilt die Umgebung. Aus der `.env`
    wird nur diese eine Zeile gelesen — die Schlüssel darin bleiben unberührt."""
    try:
        with open(ENV_FILE, "r", encoding="utf8") as handle:
            for line in handle:
                line = line.strip()
                if line.startswith("export "):
                    line = line[len("export "):].lstrip()
                if line.startswith("COUNTING_AGENTS_MODEL="):
                    value = line.split("=", 1)[1].strip().strip("'\"")
                    return value or None
    except OSError:
        pass
    return os.environ.get("COUNTING_AGENTS_MODEL") or None


def snapshot():
    """Der vollständige Zustand der Demo als einfaches dict.

    Aufbau:
      bus      — Zahlen seit dem letzten Reset, höchste Sequenznummer, Takt
      numbers  — je Zahl: wer sie einsammeln müsste und wer sie schon hat
      agents   — je Agent: Betriebszustand, Sammlung, Rückstand zum Bus
      control  — die letzten Steuerbefehle
    """
    control_events = _read_log(CONTROL_LOG)
    all_numbers = _read_log(NUMBERS_LOG)

    # Nach einem Reset zählt nur, was danach in den Bus kam.
    reset_at = _last_reset(control_events, "counter")
    numbers = [n for n in all_numbers
               if reset_at is None or (n.get("timestamp") or "") > reset_at]

    latest_seq = max([n.get("seq", 0) for n in all_numbers] or [0])
    last_value = numbers[-1].get("value", 0) if numbers else 0

    states = {agent: _read_state(agent) for agent in AGENTS}
    collected = {
        agent: set(states[agent].get("numbers") or ())
        for agent in COLLECTORS
    }

    now = time.time()
    agents = {}
    for agent in AGENTS:
        state = states[agent]
        status, verbose = _operating_status(control_events, agent)
        updated_at = _parse_ts(state.get("updated_at"))
        entry = {
            "name": agent,
            "status": status,
            "verbose": verbose,
            "updated_at": state.get("updated_at"),
            "idle_seconds": round(now - updated_at, 1) if updated_at else None,
            "still": bool(updated_at and now - updated_at > STILL_AFTER_SECONDS),
        }
        if agent == "counter":
            entry["last_value"] = last_value
        else:
            last_seq = state.get("last_seq") or 0
            entry["last_seq"] = last_seq
            entry["numbers"] = sorted(collected[agent])
            entry["count"] = len(collected[agent])
            # Der Rückstand ist die eigentliche Pointe: jeder Sammler läuft in
            # seinem eigenen Takt und hinkt dem Zähler unterschiedlich weit
            # hinterher. In den Terminalausgaben ist das nicht zu sehen.
            entry["lag"] = max(0, latest_seq - last_seq)
        agents[agent] = entry

    # Je Zahl: welcher Sammler ist zuständig, und wer hat sie schon?
    band = []
    for event in numbers:
        value = event.get("value")
        if not isinstance(value, int):
            continue
        expected = {
            "odd": value % 2 == 1,
            "even": value % 2 == 0,
            "prime": _is_prime(value),
        }
        has = {agent: value in collected[agent] for agent in COLLECTORS}
        band.append({
            "seq": event.get("seq"),
            "value": value,
            "expected": expected,
            "collected": has,
            # Eingesammelt, obwohl nicht zuständig — das Modell hat sich vertan.
            "wrong": sorted(a for a in COLLECTORS if has[a] and not expected[a]),
            "pending": sorted(a for a in COLLECTORS if expected[a] and not has[a]),
        })

    return {
        "bus": {
            "count": len(numbers),
            "latest_seq": latest_seq,
            "last_value": last_value,
            "seconds_per_number": _seconds_per_number(numbers),
            "reset_at": reset_at,
        },
        "numbers": band,
        "agents": agents,
        "control": [
            {"target": e.get("target"), "command": e.get("command"),
             "timestamp": e.get("timestamp")}
            for e in control_events[-12:]
        ],
        "generated_at": datetime.now().strftime("%H:%M:%S"),
    }
