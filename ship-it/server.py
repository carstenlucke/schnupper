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
import termios
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import base64
import urllib.request
from urllib.parse import urlparse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJEKTE_DIR = os.path.join(BASE_DIR, "projekte")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")


def _load_dotenv():
    """Lade Variablen aus .env-Datei (falls vorhanden)."""
    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

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
        "optional_outputs": ["marketing/logo.png"],
    },
    "social-media": {
        "inputs": ["produkt.md", "zielgruppe/analyse.md", "marketing/konzept.md"],
        "outputs": [
            "social-media/instagram.md",
            "social-media/linkedin.md",
            "social-media/tiktok.md",
        ],
        "optional_outputs": [
            "social-media/instagram-bild.png",
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
        "optional_inputs": [
            "marketing/logo.png",
            "social-media/instagram-bild.png",
        ],
        "outputs": ["website/website-prompt.md", "website/index.html"],
    },
}

AGENT_ORDER = ["zielgruppe", "marketing", "social-media", "kalkulation", "website"]

AGENT_LABELS = {
    "zielgruppe": "Zielgruppen-Agent",
    "marketing": "Marketing-Agent",
    "social-media": "Social-Media-Agent",
    "kalkulation": "Kalkulations-Agent",
    "website": "Website-Agent",
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
    optional_inputs = set()
    for f in paths.get("optional_inputs", []):
        full = f"{p}/{f}"
        if os.path.exists(os.path.join(BASE_DIR, full)):
            eingaben.append(full)
            optional_inputs.add(full)
    feedback_outputs = set()
    if feedback:
        for f in paths["outputs"]:
            full = f"{p}/{f}"
            if full not in eingaben and os.path.exists(os.path.join(BASE_DIR, full)):
                eingaben.append(full)
                feedback_outputs.add(full)

    eingaben_lines = []
    for e in eingaben:
        if e in feedback_outputs:
            eingaben_lines.append(f"- {e}  (deine bisherige Ausgabe)")
        elif e in optional_inputs:
            eingaben_lines.append(f"- {e}  (optional, falls vorhanden)")
        else:
            eingaben_lines.append(f"- {e}")
    eingaben_str = "\n".join(eingaben_lines)
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

    # Flusssteuerung deaktivieren – verhindert, dass XON/XOFF-Zeichen
    # (0x11/0x13) in den Datenstrom gelangen und Dateien kontaminieren
    try:
        attrs = termios.tcgetattr(slave_fd)
        attrs[0] &= ~(termios.IXON | termios.IXOFF | termios.IXANY)
        termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)
    except termios.error:
        pass

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
# Bildgenerierung (OpenAI gpt-image-1.5)
# ---------------------------------------------------------------------------

def _extract_prompt(content: str, keyword: str) -> str | None:
    """Extrahiere einen Prompt – zuerst aus Code-Block nach Keyword, dann Inline."""
    idx = content.lower().find(keyword.lower())
    if idx >= 0:
        rest = content[idx:]
        match = re.search(r'```[^\n]*\n(.*?)```', rest, re.DOTALL)
        if match:
            return match.group(1).strip()
    # Fallback: **Keyword**: <text>
    match = re.search(rf'\*\*{re.escape(keyword)}\*\*\s*:\s*(.+)', content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _call_image_api(api_key: str, prompt: str, quality: str = "low",
                    size: str = "1024x1024") -> bytes:
    """Text-to-Image mit gpt-image-1.5."""
    url = "https://api.openai.com/v1/images/generations"
    payload = json.dumps({
        "model": "gpt-image-1.5",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "output_format": "b64_json",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    data = result.get("data")
    if not data or not data[0].get("b64_json"):
        raise RuntimeError("API-Antwort enthält keine Bilddaten")
    return base64.b64decode(data[0]["b64_json"])



def _get_all_outputs(agent: str) -> list[str]:
    """Gibt outputs + optional_outputs für einen Agenten zurück."""
    paths = AGENT_PATHS.get(agent, {})
    return paths.get("outputs", []) + paths.get("optional_outputs", [])


# ---------------------------------------------------------------------------
# HTTP-Handler
# ---------------------------------------------------------------------------
SAFE_SEGMENT_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')


class ShipItHandler(SimpleHTTPRequestHandler):
    """Request-Handler für das Ship It! Dashboard."""

    def _validate_slug(self, slug):
        """Validiere Slug gegen Path-Traversal."""
        if not SAFE_SEGMENT_RE.match(slug):
            self._send_json({"error": "Ungültiger Projektname"}, 400)
            return False
        projekt_dir = os.path.realpath(os.path.join(PROJEKTE_DIR, slug))
        if not projekt_dir.startswith(os.path.realpath(PROJEKTE_DIR)):
            self._send_json({"error": "Ungültiger Pfad"}, 400)
            return False
        return True

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
            if not self._validate_slug(slug): return
            self._handle_get_agents(slug)
        elif path.startswith("/api/projekte/") and "/agents/" in path and path.endswith("/stream"):
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug): return
            agent = parts[5]
            self._handle_stream(slug, agent)
        elif path.startswith("/api/projekte/") and "/files/" in path:
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug): return
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
            if not self._validate_slug(slug): return
            agent = parts[5]
            self._handle_run_agent(slug, agent)
        elif path.startswith("/api/projekte/") and "/generate-image/" in path:
            parts = path.split("/")
            if len(parts) != 6:
                self._send_json({"error": "Not found"}, 404)
                return
            slug = parts[3]
            if not self._validate_slug(slug): return
            if parts[4] != "generate-image":
                self._send_json({"error": "Not found"}, 404)
                return
            agent = parts[5]
            self._handle_generate_image(slug, agent)
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/projekte/") and "/files/" in path:
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug): return
            if len(parts) == 6:
                # DELETE /api/projekte/<slug>/files/<agent> → alle Dateien eines Agenten
                agent = parts[5]
                self._handle_delete_agent_files(slug, agent)
            elif len(parts) >= 7:
                # DELETE /api/projekte/<slug>/files/<agent>/<datei> → einzelne Datei
                agent = parts[5]
                datei = "/".join(parts[6:])
                self._handle_delete_file(slug, agent, datei)
            else:
                self._send_json({"error": "Not found"}, 404)
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # PUT /api/projekte/<slug>/produkt
        parts = path.split("/")
        if len(parts) == 5 and parts[1] == "api" and parts[2] == "projekte" and parts[4] == "produkt":
            slug = parts[3]
            if not self._validate_slug(slug):
                return
            self._handle_update_produkt(slug)
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
        try:
            body = self._read_body()
        except json.JSONDecodeError:
            self._send_json({"error": "Ungültiges JSON"}, 400)
            return
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

    def _handle_update_produkt(self, slug):
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        if not os.path.isdir(projekt_dir):
            self._send_json({"error": "Projekt nicht gefunden"}, 404)
            return
        try:
            body = self._read_body()
        except json.JSONDecodeError:
            self._send_json({"error": "Ungültiges JSON"}, 400)
            return
        if not body or "content" not in body:
            self._send_json({"error": "Content erforderlich"}, 400)
            return
        if not isinstance(body["content"], str):
            self._send_json({"error": "Content muss ein String sein"}, 400)
            return
        content = body["content"].strip()
        if not content:
            self._send_json({"error": "Content darf nicht leer sein"}, 400)
            return
        produkt_file = os.path.join(projekt_dir, "produkt.md")
        with open(produkt_file, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        self._send_json({"status": "ok"})

    # --- API: Agents ---

    def _handle_get_agents(self, slug):
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        if not os.path.isdir(projekt_dir):
            self._send_json({"error": "Projekt nicht gefunden"}, 404)
            return

        agents = []
        for agent_name in AGENT_ORDER:
            status = get_agent_status(slug, agent_name)
            # Dateien zählen (outputs + optional_outputs)
            file_count = 0
            for out_path in _get_all_outputs(agent_name):
                if os.path.exists(os.path.join(projekt_dir, out_path)):
                    file_count += 1
            total_files = len(_get_all_outputs(agent_name))
            agents.append({
                "name": agent_name,
                "label": AGENT_LABELS[agent_name],
                "status": status,
                "file_count": file_count,
                "total_files": total_files,
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

        try:
            body = self._read_body() or {}
        except json.JSONDecodeError:
            body = {}
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
                    self.wfile.write(b"event: not_started\ndata: Agent nicht gestartet\n\n")
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
        for out_path in _get_all_outputs(agent):
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
        if expected not in _get_all_outputs(agent):
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

        # Binärdateien (Bilder)
        if datei.endswith(".png"):
            with open(full_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", len(data))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
            return

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        content_type = "text/html" if datei.endswith(".html") else "text/markdown"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    # --- API: Bildgenerierung ---

    def _handle_generate_image(self, slug, agent):
        """Generiere ein Bild mit OpenAI gpt-image-1.5."""
        import sys
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            self._send_json({"error": "OPENAI_API_KEY nicht gesetzt"}, 500)
            return

        # Konfiguration pro Agent
        config = {
            "marketing": {
                "source": "marketing/konzept.md",
                "keyword": "Logo-Prompt",
                "output": "marketing/logo.png",
                "error_no_prompt": "Kein Logo-Prompt in konzept.md gefunden",
            },
            "social-media": {
                "source": "social-media/instagram.md",
                "keyword": "Bildvorschlag",
                "output": "social-media/instagram-bild.png",
                "error_no_prompt": "Keine Bild-Beschreibung in instagram.md gefunden",
            },
        }

        if agent not in config:
            self._send_json({"error": f"Bildgenerierung für '{agent}' nicht verfügbar"}, 400)
            return

        cfg = config[agent]
        source_path = os.path.join(PROJEKTE_DIR, slug, cfg["source"])
        if not os.path.exists(source_path):
            self._send_json({"error": f"{cfg['source']} nicht gefunden"}, 404)
            return

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = _extract_prompt(content, cfg["keyword"])
        if not prompt:
            self._send_json({"error": cfg["error_no_prompt"]}, 400)
            return

        # Produktname aus produkt.md lesen
        produkt_path = os.path.join(PROJEKTE_DIR, slug, "produkt.md")
        produktname = slug
        if os.path.exists(produkt_path):
            with open(produkt_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith("#"):
                    produktname = first_line.lstrip("#").strip()

        # Produktname immer mitgeben
        prompt = f'Product: "{produktname}". {prompt}'


        print(f"[image-gen] {slug}/{agent}: Prompt = {prompt[:150]}...", file=sys.stderr)

        try:
            image_data = _call_image_api(api_key, prompt)
        except Exception as e:
            print(f"[image-gen] Fehler: {e}", file=sys.stderr)
            self._send_json({"error": "Bildgenerierung fehlgeschlagen"}, 500)
            return

        image_path = os.path.join(PROJEKTE_DIR, slug, cfg["output"])
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(image_data)

        print(f"[image-gen] {slug}/{agent}: Bild gespeichert ({len(image_data)} Bytes)", file=sys.stderr)
        self._send_json({"status": "ok", "path": cfg["output"], "size": len(image_data)})

    # --- API: Dateien löschen ---

    def _handle_delete_file(self, slug, agent, datei):
        expected = f"{agent}/{datei}"
        if expected not in _get_all_outputs(agent):
            self._send_json({"error": "Nicht erlaubt"}, 403)
            return
        full_path = os.path.join(PROJEKTE_DIR, slug, expected)
        if not os.path.exists(full_path):
            self._send_json({"error": "Datei nicht gefunden"}, 404)
            return
        os.remove(full_path)
        self._send_json({"deleted": datei})

    def _handle_delete_agent_files(self, slug, agent):
        if agent not in AGENT_PATHS:
            self._send_json({"error": "Unbekannter Agent"}, 400)
            return
        deleted = []
        for f in _get_all_outputs(agent):
            full_path = os.path.join(PROJEKTE_DIR, slug, f)
            if os.path.exists(full_path):
                os.remove(full_path)
                deleted.append(f)
        # In-memory Status zurücksetzen
        key = (slug, agent)
        with process_lock:
            if key in running_processes:
                del running_processes[key]
        self._send_json({"deleted": deleted})

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
        return json.loads(raw)

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
