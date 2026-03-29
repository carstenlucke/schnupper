#!/usr/bin/env python3
"""Ship It! Dashboard – Python-Backend (stdlib only).

Startet OpenCode-Agenten als PTY-Subprozesse, streamt Output per SSE,
verwaltet Projekte und liefert das Dashboard aus.
"""

import json
import os
import pty
import select
import signal
import subprocess
import threading
import re
import shlex
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJEKTE_DIR = os.path.join(BASE_DIR, "projekte")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

# ---------------------------------------------------------------------------
# Agent-Pfad-Templates
# ---------------------------------------------------------------------------
AGENT_PATHS = {
    "zielgruppe": {
        "inputs": ["produkt.md"],
        "outputs": ["zielgruppe/analyse.md"],
    },
    "marketing": {
        "inputs": ["produkt.md", "zielgruppe/analyse.md"],
        "outputs": ["marketing/konzept.md"],
    },
    "social-media": {
        "inputs": ["produkt.md", "zielgruppe/analyse.md", "marketing/konzept.md"],
        "outputs": [
            "social-media/instagram.md",
            "social-media/linkedin.md",
            "social-media/tiktok.md",
        ],
    },
    "kalkulation": {
        "inputs": ["produkt.md"],
        "outputs": ["kalkulation/preiskalkulation.md"],
    },
    "website": {
        "inputs": [
            "produkt.md",
            "zielgruppe/analyse.md",
            "marketing/konzept.md",
            "kalkulation/preiskalkulation.md",
        ],
        "outputs": ["website/website-prompt.md", "website/index.html"],
    },
    "app-prototyp": {
        "inputs": [
            "produkt.md",
            "zielgruppe/analyse.md",
            "marketing/konzept.md",
            "kalkulation/preiskalkulation.md",
        ],
        "outputs": ["app-prototyp/spec.md", "app-prototyp/index.html"],
    },
}

AGENT_ORDER = ["zielgruppe", "marketing", "social-media", "kalkulation", "website", "app-prototyp"]

AGENT_LABELS = {
    "zielgruppe": "Zielgruppen-Agent",
    "marketing": "Marketing-Agent",
    "social-media": "Social-Media-Agent",
    "kalkulation": "Kalkulations-Agent",
    "website": "Website-Agent",
    "app-prototyp": "App-Prototyp-Agent",
}

# ---------------------------------------------------------------------------
# Prozess-Verwaltung (in-memory)
# ---------------------------------------------------------------------------
# Key: (slug, agent_name) → {"process": Popen, "master_fd": int, "output": list[str], "exit_code": int|None}
running_processes: dict[tuple[str, str], dict] = {}
process_lock = threading.Lock()


def slugify(name: str) -> str:
    """Erzeuge einen URL-freundlichen Slug aus einem Namen."""
    s = name.lower().strip()
    s = re.sub(r"[äÄ]", "ae", s)
    s = re.sub(r"[öÖ]", "oe", s)
    s = re.sub(r"[üÜ]", "ue", s)
    s = re.sub(r"ß", "ss", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def get_agent_status(slug: str, agent: str) -> str:
    """Leite den Agent-Status aus Dateisystem + Prozessliste ab."""
    key = (slug, agent)
    with process_lock:
        proc_info = running_processes.get(key)
        if proc_info and proc_info.get("exit_code") is None:
            # Prozess könnte fertig sein – prüfen
            proc = proc_info.get("process")
            if proc and proc.poll() is not None:
                proc_info["exit_code"] = proc.returncode
            else:
                return "running"

        if proc_info and proc_info.get("exit_code") is not None:
            # Prozess beendet – prüfe Outputs
            if verify_outputs(slug, agent):
                return "done"
            return "error"

    # Kein Prozess bekannt – prüfe Dateisystem
    if verify_outputs(slug, agent):
        return "done"
    return "idle"


def verify_outputs(slug: str, agent: str) -> bool:
    """Prüfe ob alle erwarteten Output-Dateien existieren."""
    for f in AGENT_PATHS[agent]["outputs"]:
        if not os.path.exists(os.path.join(PROJEKTE_DIR, slug, f)):
            return False
    return True


def build_run_prompt(slug: str, agent: str, feedback: str = None) -> str:
    """Baue den vollständigen Run-Prompt mit expliziten Pfaden."""
    p = f"projekte/{slug}"
    paths = AGENT_PATHS[agent]

    eingaben = [f"{p}/{f}" for f in paths["inputs"]]
    if feedback:
        for f in paths["outputs"]:
            full = f"{p}/{f}"
            if full not in eingaben and os.path.exists(os.path.join(BASE_DIR, full)):
                eingaben.append(f"{full}  ← deine bisherige Ausgabe")

    eingaben_str = "\n".join(f"- {e}" for e in eingaben)
    ausgaben_str = "\n".join(f"- {p}/{f}" for f in paths["outputs"])

    if feedback:
        aufgabe = (
            "Überarbeite deine bisherige Ausgabe.\n"
            f'Feedback vom Nutzer: "{feedback}"'
        )
    else:
        aufgabe = "Führe deine Aufgabe aus."

    return f"""Projektordner: {p}

EINGABE (lies diese Dateien):
{eingaben_str}

AUSGABE (schreibe in diese Dateien, erstelle Verzeichnisse falls nötig):
{ausgaben_str}

{aufgabe}"""


def start_agent(slug: str, agent: str, feedback: str = None) -> dict:
    """Starte einen OpenCode-Agent als PTY-Subprocess."""
    key = (slug, agent)

    with process_lock:
        existing = running_processes.get(key)
        if existing and existing.get("exit_code") is None:
            proc = existing.get("process")
            if proc and proc.poll() is None:
                return {"error": "Agent läuft bereits"}

    prompt = build_run_prompt(slug, agent, feedback)
    cmd = ["opencode", "run", "--agent", agent, prompt]

    import sys
    print(f"[agent-start] {slug}/{agent} → {' '.join(cmd[:4])} '...'", file=sys.stderr)

    # PTY erstellen für ANSI-Farben
    master_fd, slave_fd = pty.openpty()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=slave_fd,
            stderr=slave_fd,
            stdin=subprocess.DEVNULL,
            cwd=BASE_DIR,
            env={**os.environ, "TERM": "xterm-256color"},
        )
    except Exception as e:
        os.close(master_fd)
        os.close(slave_fd)
        print(f"[agent-error] {slug}/{agent}: {e}", file=sys.stderr)
        return {"error": str(e)}
    os.close(slave_fd)

    proc_info = {
        "process": proc,
        "master_fd": master_fd,
        "output": [],
        "exit_code": None,
    }

    with process_lock:
        running_processes[key] = proc_info

    # Background-Thread zum Lesen des Outputs
    def reader():
        try:
            while True:
                r, _, _ = select.select([master_fd], [], [], 0.5)
                if r:
                    try:
                        data = os.read(master_fd, 4096)
                        if not data:
                            break
                        proc_info["output"].append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        break
                if proc.poll() is not None:
                    # Restliche Daten lesen
                    try:
                        while True:
                            r, _, _ = select.select([master_fd], [], [], 0.1)
                            if r:
                                data = os.read(master_fd, 4096)
                                if not data:
                                    break
                                proc_info["output"].append(data.decode("utf-8", errors="replace"))
                            else:
                                break
                    except OSError:
                        pass
                    break
        finally:
            try:
                os.close(master_fd)
            except OSError:
                pass
            proc_info["exit_code"] = proc.returncode if proc.returncode is not None else proc.wait()

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    return {"status": "started", "agent": agent, "slug": slug}


# ---------------------------------------------------------------------------
# HTTP-Handler
# ---------------------------------------------------------------------------
class ShipItHandler(SimpleHTTPRequestHandler):
    """Request-Handler für das Ship It! Dashboard."""

    def log_message(self, format, *args):
        """Kompaktes Logging auf stderr."""
        import sys
        print(f"[{self.log_date_time_string()}] {format % args}", file=sys.stderr)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API-Routen
        if path == "/api/projekte":
            self._handle_get_projekte()
        elif path.startswith("/api/projekte/") and path.endswith("/agents"):
            slug = path.split("/")[3]
            self._handle_get_agents(slug)
        elif path.startswith("/api/projekte/") and "/agents/" in path and path.endswith("/stream"):
            parts = path.split("/")
            slug = parts[3]
            agent = parts[5]
            self._handle_stream(slug, agent)
        elif path.startswith("/api/projekte/") and "/files/" in path:
            parts = path.split("/")
            slug = parts[3]
            # /api/projekte/<slug>/files/<agent> oder /api/projekte/<slug>/files/<agent>/<datei>
            if len(parts) == 6:
                agent = parts[5]
                self._handle_get_files(slug, agent)
            elif len(parts) >= 7:
                agent = parts[5]
                datei = "/".join(parts[6:])
                self._handle_get_file_content(slug, agent, datei)
            else:
                self._send_json({"error": "Not found"}, 404)
        else:
            # Statische Dateien aus dashboard/
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/projekte":
            self._handle_create_projekt()
        elif path.startswith("/api/projekte/") and "/agents/" in path and path.endswith("/run"):
            parts = path.split("/")
            slug = parts[3]
            agent = parts[5]
            self._handle_run_agent(slug, agent)
        else:
            self._send_json({"error": "Not found"}, 404)

    # --- API: Projekte ---

    def _handle_get_projekte(self):
        projekte = []
        if os.path.isdir(PROJEKTE_DIR):
            for slug in sorted(os.listdir(PROJEKTE_DIR)):
                projekt_dir = os.path.join(PROJEKTE_DIR, slug)
                if not os.path.isdir(projekt_dir):
                    continue
                produkt_file = os.path.join(projekt_dir, "produkt.md")
                name = slug
                if os.path.exists(produkt_file):
                    with open(produkt_file, "r", encoding="utf-8") as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("#"):
                            name = first_line.lstrip("#").strip()
                # Gesamtstatus berechnen
                statuses = [get_agent_status(slug, a) for a in AGENT_ORDER]
                if all(s == "done" for s in statuses):
                    overall = "done"
                elif any(s in ("running", "done", "error") for s in statuses):
                    overall = "in_progress"
                else:
                    overall = "new"
                projekte.append({"slug": slug, "name": name, "status": overall})
        self._send_json(projekte)

    def _handle_create_projekt(self):
        body = self._read_body()
        if not body:
            self._send_json({"error": "Kein Body"}, 400)
            return
        name = body.get("name", "").strip()
        beschreibung = body.get("beschreibung", "").strip()
        if not name:
            self._send_json({"error": "Name erforderlich"}, 400)
            return

        slug = slugify(name)
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        os.makedirs(projekt_dir, exist_ok=True)

        produkt_file = os.path.join(projekt_dir, "produkt.md")
        with open(produkt_file, "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\n{beschreibung}\n")

        self._send_json({"slug": slug, "name": name}, 201)

    # --- API: Agents ---

    def _handle_get_agents(self, slug):
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        if not os.path.isdir(projekt_dir):
            self._send_json({"error": "Projekt nicht gefunden"}, 404)
            return

        agents = []
        for agent_name in AGENT_ORDER:
            status = get_agent_status(slug, agent_name)
            # Dateien zählen
            file_count = 0
            for out_path in AGENT_PATHS[agent_name]["outputs"]:
                if os.path.exists(os.path.join(projekt_dir, out_path)):
                    file_count += 1
            agents.append({
                "name": agent_name,
                "label": AGENT_LABELS[agent_name],
                "status": status,
                "file_count": file_count,
                "total_files": len(AGENT_PATHS[agent_name]["outputs"]),
            })
        self._send_json(agents)

    def _handle_run_agent(self, slug, agent):
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        if not os.path.isdir(projekt_dir):
            self._send_json({"error": "Projekt nicht gefunden"}, 404)
            return
        if agent not in AGENT_PATHS:
            self._send_json({"error": "Unbekannter Agent"}, 400)
            return

        body = self._read_body() or {}
        feedback = body.get("feedback")

        result = start_agent(slug, agent, feedback)
        if "error" in result:
            self._send_json(result, 409)
        else:
            self._send_json(result)

    # --- API: SSE-Stream ---

    def _handle_stream(self, slug, agent):
        key = (slug, agent)

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        sent_index = 0
        try:
            while True:
                with process_lock:
                    proc_info = running_processes.get(key)

                if not proc_info:
                    self.wfile.write(b"event: error\ndata: Agent nicht gestartet\n\n")
                    self.wfile.flush()
                    break

                # Neue Output-Chunks senden
                output = proc_info["output"]
                while sent_index < len(output):
                    chunk = output[sent_index]
                    for line in chunk.splitlines(True):
                        escaped = json.dumps(line)
                        self.wfile.write(f"data: {escaped}\n\n".encode())
                    self.wfile.flush()
                    sent_index += 1

                # Prüfe ob Prozess beendet
                if proc_info["exit_code"] is not None:
                    # Restliche Daten senden
                    while sent_index < len(output):
                        chunk = output[sent_index]
                        for line in chunk.splitlines(True):
                            escaped = json.dumps(line)
                            self.wfile.write(f"data: {escaped}\n\n".encode())
                        self.wfile.flush()
                        sent_index += 1

                    exit_code = proc_info["exit_code"]
                    self.wfile.write(f"event: done\ndata: {exit_code}\n\n".encode())
                    self.wfile.flush()
                    break

                import time
                time.sleep(0.2)

        except (BrokenPipeError, ConnectionResetError):
            pass

    # --- API: Dateien ---

    def _handle_get_files(self, slug, agent):
        if agent not in AGENT_PATHS:
            self._send_json({"error": "Unbekannter Agent"}, 400)
            return

        files = []
        for out_path in AGENT_PATHS[agent]["outputs"]:
            full_path = os.path.join(PROJEKTE_DIR, slug, out_path)
            exists = os.path.exists(full_path)
            files.append({
                "path": out_path,
                "name": os.path.basename(out_path),
                "exists": exists,
                "size": os.path.getsize(full_path) if exists else 0,
            })
        self._send_json(files)

    def _handle_get_file_content(self, slug, agent, datei):
        # Sicherheit: Pfad muss in AGENT_PATHS definiert sein
        expected = f"{agent}/{datei}"
        if expected not in AGENT_PATHS.get(agent, {}).get("outputs", []):
            # Auch produkt.md erlauben
            if datei != "produkt.md":
                self._send_json({"error": "Nicht erlaubt"}, 403)
                return
            full_path = os.path.join(PROJEKTE_DIR, slug, "produkt.md")
        else:
            full_path = os.path.join(PROJEKTE_DIR, slug, expected)

        if not os.path.exists(full_path):
            self._send_json({"error": "Datei nicht gefunden"}, 404)
            return

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        content_type = "text/html" if datei.endswith(".html") else "text/markdown"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    # --- Statische Dateien ---

    def _serve_static(self, path):
        if path == "/" or path == "":
            path = "/index.html"

        file_path = os.path.join(DASHBOARD_DIR, path.lstrip("/"))
        if not os.path.isfile(file_path):
            self.send_error(404)
            return

        ext = os.path.splitext(file_path)[1]
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        ct = content_types.get(ext, "application/octet-stream")

        with open(file_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    # --- Hilfsmethoden ---

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


# ---------------------------------------------------------------------------
# Server starten
# ---------------------------------------------------------------------------
def main():
    os.makedirs(PROJEKTE_DIR, exist_ok=True)

    server = ThreadingHTTPServer(("", PORT), ShipItHandler)
    print(f"Ship It! Dashboard → http://localhost:{PORT}")

    def shutdown(sig, frame):
        print("\nServer wird beendet...")
        # Laufende Prozesse beenden
        with process_lock:
            for key, info in running_processes.items():
                proc = info.get("process")
                if proc and proc.poll() is None:
                    proc.terminate()
        server.shutdown()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
