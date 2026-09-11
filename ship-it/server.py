#!/usr/bin/env python3
"""Ship It! Dashboard – Python-Backend (stdlib only).

Startet die Agenten als pi-Subprozesse, übersetzt ihre Ereignisse in
Terminal-Text, streamt ihn per SSE, verwaltet Projekte und liefert das
Dashboard aus.
"""

import json
import os
import signal
import subprocess
import sys
import threading
import re
import shutil
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import base64
import urllib.request
from urllib.parse import urlparse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJEKTE_DIR = os.path.join(BASE_DIR, "projekte")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
PI_EXTENSIONS_DIR = os.path.join(BASE_DIR, ".pi", "extensions")
PI_SKILLS_DIR = os.path.join(BASE_DIR, ".pi", "skills")


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
        "optional_outputs": ["website/logo.png", "website/instagram-bild.png"],
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
# Key: (slug, agent_name) → {"process": Popen, "output": list[str], "exit_code": int|None}
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
            f'Überarbeite deine bisherige Ausgabe.\nFeedback vom Nutzer: "{feedback}"'
        )
    else:
        aufgabe = "Führe deine Aufgabe aus."

    return f"""Projektordner: {p}

EINGABE (lies diese Dateien):
{eingaben_str}

AUSGABE (schreibe in diese Dateien, erstelle Verzeichnisse falls nötig):
{ausgaben_str}

{aufgabe}"""


# ---------------------------------------------------------------------------
# Agenten-Dateien: agents/<name>.md
# ---------------------------------------------------------------------------
# pi kennt keine Agenten. Ein Agent ist hier ein pi-Aufruf mit eigenem
# Systemprompt, eigenem Modell und eigenen Werkzeugen – alles drei steht in
# einer Markdown-Datei: oben das Frontmatter, darunter die Aufgabe.


def read_agent(agent: str) -> tuple[dict, str, str] | None:
    """Lies eine Agenten-Datei. Liefert (Frontmatter, Systemprompt, Rohtext)."""
    agent_file = os.path.join(AGENTS_DIR, f"{agent}.md")
    if not os.path.exists(agent_file):
        return None

    with open(agent_file, "r", encoding="utf-8") as f:
        content = f.read()

    body = content
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            frontmatter = content[3:end].strip()
            body = content[end + 3 :].strip()
            for line in frontmatter.split("\n"):
                if ":" in line and not line.startswith(" "):
                    key, _, value = line.partition(":")
                    meta[key.strip()] = value.strip()
    return meta, body, content


def agent_model(meta: dict) -> str:
    """Das Modell, mit dem ein Agent tatsächlich läuft: SHIP_IT_MODEL aus der
    .env schlägt den `model:`-Eintrag – für alle Agenten zugleich."""
    return os.environ.get("SHIP_IT_MODEL") or meta.get("model", "")


def _liste(wert: str) -> list[str]:
    """Kommagetrennte Frontmatter-Angabe als Liste: "read, write" → [read, write]"""
    return [teil.strip() for teil in wert.split(",") if teil.strip()]


def build_pi_command(meta: dict, system_prompt: str, prompt: str) -> list[str]:
    """Baue den pi-Aufruf für einen Agenten aus seinem Frontmatter.

    Die Flags im Einzelnen:
      --mode json   jedes Ereignis als JSON-Zeile – Denken, Werkzeugaufrufe,
                    Text. `-p` allein zeigt nur die Schlussantwort, das Terminal
                    im Dashboard bliebe minutenlang leer
      --no-session  kein Gesprächsverlauf, jeder Lauf beginnt bei null
      -nc           CLAUDE.md/AGENTS.md ignorieren – der Agent kennt nur
                    seinen Prompt
      -ns, -np      Skills und Prompt-Vorlagen nicht selbst einsammeln; ein
                    Skill kommt nur über `skills:` im Frontmatter dazu
      -ne, -e       nur die Werkzeuge aus .pi/extensions/ laden, nichts, was
                    global auf dem Rechner installiert ist
      --tools       genau die Werkzeuge aus dem Frontmatter, keine weiteren
    """
    cmd = ["pi", "--mode", "json", "--no-session", "-nc", "-ns", "-np", "-ne"]
    if os.path.isdir(PI_EXTENSIONS_DIR):
        for name in sorted(os.listdir(PI_EXTENSIONS_DIR)):
            if name.endswith(".ts"):
                cmd += ["-e", os.path.join(PI_EXTENSIONS_DIR, name)]

    model = agent_model(meta)
    if model:
        cmd += ["--model", model]
    if meta.get("thinking"):
        cmd += ["--thinking", meta["thinking"]]
    if meta.get("tools"):
        cmd += ["--tools", ",".join(_liste(meta["tools"]))]
    for skill in _liste(meta.get("skills", "")):
        cmd += ["--skill", os.path.join(PI_SKILLS_DIR, skill)]

    cmd += ["--system-prompt", system_prompt, "--", prompt]
    return cmd


# ---------------------------------------------------------------------------
# pi-Ereignisse → Terminal
# ---------------------------------------------------------------------------
# Farben für das xterm.js-Terminal im Dashboard (ANSI-Escape-Sequenzen)
ANSI_RESET = "\x1b[0m"
ANSI_FETT = "\x1b[1m"
ANSI_BLASS = "\x1b[2m"
ANSI_KURSIV = "\x1b[3m"
ANSI_ROT = "\x1b[31m"
ANSI_GELB = "\x1b[33m"
ANSI_CYAN = "\x1b[36m"
ZEILE_LEEREN = "\r\x1b[K"


def _zahl(n: int) -> str:
    """Tausenderpunkte wie im Deutschen: 12345 → 12.345"""
    return f"{n:,}".replace(",", ".")


def _groesse(zeichen: int) -> str:
    """Textlänge zum Vorlesen: 830 Zeichen, 5,2 KB"""
    if zeichen < 1024:
        return f"{zeichen} Zeichen"
    return f"{zeichen / 1024:.1f} KB".replace(".", ",")


def _gekuerzt(text: str, max_zeilen: int) -> str:
    """Die ersten Zeilen eines Werkzeugergebnisses, eingerückt."""
    zeilen = text.splitlines()
    gezeigt = [f"  {z[:200]}" for z in zeilen[:max_zeilen]]
    if len(zeilen) > max_zeilen:
        gezeigt.append(f"  … ({len(zeilen) - max_zeilen} weitere Zeilen)")
    return "\n".join(gezeigt)


def _werkzeug_kurz(name: str, args: dict) -> str:
    """Die Argumente eines Werkzeugaufrufs in einer Zeile – das, was man sehen will."""
    if name == "write":
        groesse = _groesse(len(args.get("content", "")))
        return f"{args.get('path', '')} {ANSI_BLASS}({groesse}){ANSI_RESET}"
    if name == "bash":
        befehl = args.get("command", "").strip().splitlines()
        if not befehl:
            return ""
        return befehl[0][:200] + (" …" if len(befehl) > 1 else "")
    for feld in ("path", "url"):
        if feld in args:
            return str(args[feld])
    return json.dumps(args, ensure_ascii=False)[:200]


class PiAusgabe:
    """Übersetzt den Ereignisstrom von `pi --mode json` in Terminal-Text.

    pi meldet jeden Zwischenschritt als JSON-Zeile: Denken, Text,
    Werkzeugaufrufe samt Ergebnis. Hier wird daraus das, was im
    Dashboard-Terminal zu sehen ist – der Agent soll beim Arbeiten sichtbar
    sein, nicht erst am Ende.
    """

    def __init__(self):
        self.zeilenanfang = True  # Steht der Cursor am Zeilenanfang?
        self.werkzeug = None  # Werkzeug, dessen Aufruf das Modell gerade schreibt
        self.werkzeug_zeichen = 0  # Bisher gestreamte Zeichen dieses Aufrufs
        self.fortschritt_bei = 0  # Stand der zuletzt gezeigten Fortschrittszeile

    def verarbeite(self, zeile: str) -> str:
        """Übersetze eine Ausgabezeile von pi in Text fürs Terminal."""
        zeile = zeile.strip()
        if not zeile:
            return ""
        try:
            ereignis = json.loads(zeile)
        except json.JSONDecodeError:
            ereignis = None
        if not isinstance(ereignis, dict):
            # Keine Ereigniszeile, sondern eine Meldung von pi selbst – meist
            # ein Fehler beim Start (unbekanntes Modell, fehlender Login)
            return self._ausgabe(f"{self._umbruch()}{ANSI_ROT}{zeile}{ANSI_RESET}\n")
        return self._ausgabe(self._uebersetze(ereignis))

    # Farbcodes am Textende – sie verschieben den Cursor nicht
    _ANSI_AM_ENDE = re.compile(r"(?:\x1b\[[0-9;]*[A-Za-z])+$")

    def _ausgabe(self, text: str) -> str:
        sichtbar = self._ANSI_AM_ENDE.sub("", text)
        if sichtbar:
            self.zeilenanfang = sichtbar.endswith("\n")
        return text

    def _umbruch(self) -> str:
        return "" if self.zeilenanfang else "\n"

    def _uebersetze(self, e: dict) -> str:
        typ = e.get("type")
        if typ == "message_update":
            return self._stream(e.get("assistantMessageEvent") or {})

        if typ == "tool_execution_start":
            name = e.get("toolName", "?")
            anfang = ZEILE_LEEREN if self.fortschritt_bei else self._umbruch()
            self.werkzeug, self.fortschritt_bei = None, 0
            kurz = _werkzeug_kurz(name, e.get("args") or {})
            return f"{anfang}{ANSI_CYAN}→ {ANSI_FETT}{name}{ANSI_RESET} {kurz}\n"

        if typ == "tool_execution_end":
            ergebnis = e.get("result") or {}
            text = "".join(
                teil.get("text", "")
                for teil in ergebnis.get("content") or []
                if teil.get("type") == "text"
            ).strip()
            if e.get("isError"):
                return f"{ANSI_ROT}{_gekuerzt(text or 'Fehler', 4)}{ANSI_RESET}\n"
            if e.get("toolName") == "bash" and text:
                return f"{ANSI_BLASS}{_gekuerzt(text, 6)}{ANSI_RESET}\n"
            return ""

        if typ == "message_end":
            nachricht = e.get("message") or {}
            if nachricht.get("role") == "assistant" and nachricht.get(
                "stopReason"
            ) in ("error", "aborted"):
                grund = nachricht.get("errorMessage") or "Anfrage abgebrochen"
                return f"{self._umbruch()}{ANSI_ROT}✗ {grund}{ANSI_RESET}\n"
            return ""

        if typ == "auto_retry_start":
            sekunden = e.get("delayMs", 0) / 1000
            return (
                f"{self._umbruch()}{ANSI_GELB}↻ {e.get('errorMessage', 'Fehler beim Anbieter')}"
                f" – neuer Versuch {e.get('attempt')}/{e.get('maxAttempts')}"
                f" in {sekunden:.0f}s{ANSI_RESET}\n"
            )

        if typ == "agent_end" and not e.get("willRetry"):
            return self._verbrauch(e.get("messages") or [])
        return ""

    def _stream(self, a: dict) -> str:
        """Was das Modell gerade Stück für Stück erzeugt."""
        art = a.get("type")
        if art == "thinking_start":
            return f"{self._umbruch()}{ANSI_BLASS}{ANSI_KURSIV}💭 "
        if art == "thinking_delta":
            # Die Denk-Zusammenfassungen kommen als Markdown – ** und
            # Leerzeilen stören im Terminal
            delta = a.get("delta", "").replace("**", "")
            delta = re.sub(r"\n{2,}", "\n", delta)
            return f"{ANSI_BLASS}{ANSI_KURSIV}{delta}{ANSI_RESET}"
        if art == "thinking_end":
            return f"{ANSI_RESET}{self._umbruch()}"
        if art == "text_start":
            return self._umbruch()
        if art == "text_delta":
            return a.get("delta", "")
        if art == "text_end":
            return self._umbruch()
        if art == "toolcall_start":
            # Im JSON-Modus lässt pi die halbfertige Antwort (partial) weg und
            # schreibt den Werkzeugnamen direkt ins Ereignis
            self.werkzeug = a.get("toolName") or "?"
            self.werkzeug_zeichen = self.fortschritt_bei = 0
            return ""
        if art == "toolcall_delta" and self.werkzeug:
            # Ein langer Aufruf – write mit einer ganzen Website – entsteht über
            # Minuten, bevor das Werkzeug überhaupt läuft. Eine mitlaufende Zeile
            # zeigt, dass der Agent gerade schreibt und nicht hängt.
            self.werkzeug_zeichen += len(a.get("delta", ""))
            if self.werkzeug_zeichen - self.fortschritt_bei >= 1000:
                anfang = ZEILE_LEEREN if self.fortschritt_bei else self._umbruch()
                self.fortschritt_bei = self.werkzeug_zeichen
                groesse = _groesse(self.werkzeug_zeichen)
                return f"{anfang}{ANSI_BLASS}✎ {self.werkzeug} … {groesse}{ANSI_RESET}"
        return ""

    def _verbrauch(self, nachrichten: list) -> str:
        """Schlusszeile: wie viel Text das Modell gelesen und geschrieben hat."""
        gelesen = geschrieben = 0
        kosten = 0.0
        for n in nachrichten:
            if n.get("role") != "assistant":
                continue
            usage = n.get("usage") or {}
            gelesen += usage.get("input", 0) + usage.get("cacheRead", 0)
            geschrieben += usage.get("output", 0)
            kosten += (usage.get("cost") or {}).get("total", 0)
        if not gelesen and not geschrieben:
            return ""
        zeile = f"Tokens: {_zahl(gelesen)} gelesen · {_zahl(geschrieben)} geschrieben"
        if kosten > 0:
            zeile += f" · Listenpreis: {kosten:.2f} $".replace(".", ",")
        return f"{self._umbruch()}\n{ANSI_BLASS}{zeile}{ANSI_RESET}\n"


def _kopfzeilen(meta: dict) -> str:
    """Was vor dem ersten Ereignis im Terminal steht: womit der Agent arbeitet."""
    zeilen = [f"Modell:    {agent_model(meta) or '(pi-Voreinstellung)'}"]
    if meta.get("thinking"):
        zeilen[0] += f" · Denken: {meta['thinking']}"
    zeilen.append(f"Werkzeuge: {', '.join(_liste(meta.get('tools', ''))) or '–'}")
    if meta.get("skills"):
        zeilen.append(f"Skills:    {', '.join(_liste(meta['skills']))}")
    return f"{ANSI_BLASS}" + "\n".join(zeilen) + f"{ANSI_RESET}\n\n"


def start_agent(slug: str, agent: str, feedback: str = None) -> dict:
    """Starte einen Agenten als pi-Subprozess."""
    key = (slug, agent)

    with process_lock:
        existing = running_processes.get(key)
        if existing and existing.get("exit_code") is None:
            proc = existing.get("process")
            if proc and proc.poll() is None:
                return {"error": "Agent läuft bereits"}

    definition = read_agent(agent)
    if not definition:
        return {"error": f"agents/{agent}.md nicht gefunden"}
    meta, system_prompt, _ = definition

    prompt = build_run_prompt(slug, agent, feedback)
    cmd = build_pi_command(meta, system_prompt, prompt)

    import sys

    print(
        f"[agent-start] {slug}/{agent} → pi --model {agent_model(meta)} "
        f"--tools {meta.get('tools', '')} '...'",
        file=sys.stderr,
    )

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # pi liest die Standardeingabe mit in den Auftrag ein. Bliebe sie
            # offen, wartete der Agent für immer auf ihr Ende.
            stdin=subprocess.DEVNULL,
            cwd=BASE_DIR,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return {
            "error": "pi CLI nicht gefunden – installieren mit "
            "'npm install -g @earendil-works/pi-coding-agent'"
        }
    except Exception as e:
        print(f"[agent-error] {slug}/{agent}: {e}", file=sys.stderr)
        return {"error": str(e)}

    proc_info = {
        "process": proc,
        "output": [_kopfzeilen(meta)],
        "exit_code": None,
    }

    with process_lock:
        running_processes[key] = proc_info

    # Background-Thread: Ereignisse lesen, übersetzen, für den SSE-Stream sammeln
    def reader():
        ausgabe = PiAusgabe()
        try:
            for zeile in proc.stdout:
                # Ein Ereignis in unerwarteter Form – etwa Werkzeugargumente,
                # die das Modell falsch gebaut hat – darf den Leser nicht
                # beenden: sonst bliebe der Rest des Laufs unsichtbar und pi
                # wartete womöglich auf eine volle Pipe
                try:
                    text = ausgabe.verarbeite(zeile)
                except Exception as e:
                    print(f"[agent-warn] {slug}/{agent}: {e!r}", file=sys.stderr)
                    continue
                if text:
                    proc_info["output"].append(text)
        except (OSError, ValueError):
            pass
        finally:
            proc_info["exit_code"] = proc.wait()

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    return {"status": "started", "agent": agent, "slug": slug}


# ---------------------------------------------------------------------------
# Bildgenerierung (OpenAI gpt-image-2)
# ---------------------------------------------------------------------------


def _extract_prompt(content: str, keyword: str) -> str | None:
    """Extrahiere einen Prompt – zuerst aus Code-Block nach Keyword, dann Inline."""
    idx = content.lower().find(keyword.lower())
    if idx >= 0:
        rest = content[idx:]
        match = re.search(r"```[^\n]*\n(.*?)```", rest, re.DOTALL)
        if match:
            return match.group(1).strip()
    # Fallback: **Keyword**: <text>
    match = re.search(
        rf"\*\*{re.escape(keyword)}\*\*\s*:\s*(.+)", content, re.IGNORECASE
    )
    if match:
        return match.group(1).strip()
    return None


def _call_image_api(
    api_key: str, prompt: str, quality: str = "low", size: str = "1024x1024"
) -> bytes:
    """Text-to-Image mit gpt-image-2."""
    url = "https://api.openai.com/v1/images/generations"
    payload = json.dumps(
        {
            "model": "gpt-image-2",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality,
            "output_format": "png",
        }
    ).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e

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
SAFE_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class QuietThreadingHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer, der harmlose Client-Disconnects stillschweigend verwirft.

    Browser schließen Keep-Alive-Verbindungen beim Projektwechsel, wodurch der
    blockierende readline() im Worker-Thread ConnectionResetError wirft. Diese
    Exceptions sind erwartet und sollen das Log nicht verrauschen.
    """

    def handle_error(self, request, client_address):
        import sys

        exc = sys.exc_info()[1]
        if isinstance(
            exc, (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)
        ):
            return
        super().handle_error(request, client_address)


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
            if not self._validate_slug(slug):
                return
            self._handle_get_agents(slug)
        elif (
            path.startswith("/api/projekte/")
            and "/agents/" in path
            and path.endswith("/stream")
        ):
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug):
                return
            agent = parts[5]
            self._handle_stream(slug, agent)
        elif path.startswith("/api/projekte/") and "/files/" in path:
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug):
                return
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
        elif path.startswith("/api/agents/") and path.endswith("/prompt"):
            parts = path.split("/")
            agent_name = parts[3]
            self._handle_get_agent_prompt(agent_name)
        else:
            # Statische Dateien aus dashboard/
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/projekte":
            self._handle_create_projekt()
        elif (
            path.startswith("/api/projekte/")
            and "/agents/" in path
            and path.endswith("/run")
        ):
            parts = path.split("/")
            slug = parts[3]
            if not self._validate_slug(slug):
                return
            agent = parts[5]
            self._handle_run_agent(slug, agent)
        elif path.startswith("/api/projekte/") and "/generate-image/" in path:
            parts = path.split("/")
            if len(parts) != 6:
                self._send_json({"error": "Not found"}, 404)
                return
            slug = parts[3]
            if not self._validate_slug(slug):
                return
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
            if not self._validate_slug(slug):
                return
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
        elif path.startswith("/api/projekte/"):
            parts = path.split("/")
            if len(parts) == 4 and parts[1] == "api" and parts[2] == "projekte":
                slug = parts[3]
                if not self._validate_slug(slug):
                    return
                self._handle_delete_projekt(slug)
            else:
                self._send_json({"error": "Not found"}, 404)
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # PUT /api/projekte/<slug>/produkt
        parts = path.split("/")
        if (
            len(parts) == 5
            and parts[1] == "api"
            and parts[2] == "projekte"
            and parts[4] == "produkt"
        ):
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

    def _stop_projekt_prozesse(self, slug):
        keys = []
        with process_lock:
            for key, info in list(running_processes.items()):
                if key[0] != slug:
                    continue
                keys.append(key)
                proc = info.get("process")
                if proc and proc.poll() is None:
                    proc.terminate()

        for key in keys:
            proc = None
            with process_lock:
                info = running_processes.get(key)
                if info:
                    proc = info.get("process")
            if not proc or proc.poll() is not None:
                continue
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass

        with process_lock:
            for key in keys:
                running_processes.pop(key, None)

    def _handle_delete_projekt(self, slug):
        projekt_dir = os.path.join(PROJEKTE_DIR, slug)
        if not os.path.isdir(projekt_dir):
            self._send_json({"error": "Projekt nicht gefunden"}, 404)
            return

        self._stop_projekt_prozesse(slug)

        try:
            shutil.rmtree(projekt_dir)
        except OSError:
            self._send_json({"error": "Projekt konnte nicht gelöscht werden"}, 500)
            return

        self._send_json({"deleted": slug})

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
        original_content = body["content"]
        if not original_content.strip():
            self._send_json({"error": "Content darf nicht leer sein"}, 400)
            return
        produkt_file = os.path.join(projekt_dir, "produkt.md")
        content_to_write = (
            original_content
            if original_content.endswith("\n")
            else original_content + "\n"
        )
        with open(produkt_file, "w", encoding="utf-8") as f:
            f.write(content_to_write)
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
            agents.append(
                {
                    "name": agent_name,
                    "label": AGENT_LABELS[agent_name],
                    "status": status,
                    "file_count": file_count,
                    "total_files": total_files,
                }
            )
        self._send_json(agents)

    def _handle_get_agent_prompt(self, agent_name):
        """Liefere den Systemprompt eines Agenten (ohne YAML-Frontmatter)."""
        if agent_name not in AGENT_PATHS:
            self._send_json({"error": "Unbekannter Agent"}, 400)
            return

        definition = read_agent(agent_name)
        if not definition:
            self._send_json({"error": "Agent-Datei nicht gefunden"}, 404)
            return
        meta, body, content = definition
        # Das Badge im Dashboard zeigt das Modell, das wirklich läuft
        meta = {**meta, "model": agent_model(meta)}

        self._send_json(
            {
                "body": body,
                "raw": content,
                "meta": meta,
                "agent": agent_name,
                "label": AGENT_LABELS.get(agent_name, agent_name),
            }
        )

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
                    self.wfile.write(
                        b"event: not_started\ndata: Agent nicht gestartet\n\n"
                    )
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
            files.append(
                {
                    "path": out_path,
                    "name": os.path.basename(out_path),
                    "exists": exists,
                    "size": os.path.getsize(full_path) if exists else 0,
                }
            )
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
        """Generiere ein Bild mit OpenAI gpt-image-2."""
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
                "style_suffix": (
                    "Render as a polished, professional brand logo with a "
                    "minimalist composition, soft directional lighting, subtle "
                    "depth and refined material finish (matte or satin). "
                    "Centered on a clean neutral background. Do NOT render as "
                    "flat vector art, SVG-style geometry, line icon or 2D clip "
                    "art."
                ),
            },
            "social-media": {
                "source": "social-media/instagram.md",
                "keyword": "Bildvorschlag",
                "output": "social-media/instagram-bild.png",
                "error_no_prompt": "Keine Bild-Beschreibung in instagram.md gefunden",
            },
        }

        if agent not in config:
            self._send_json(
                {"error": f"Bildgenerierung für '{agent}' nicht verfügbar"}, 400
            )
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
        if cfg.get("style_suffix"):
            prompt = f'{prompt} {cfg["style_suffix"]}'

        print(
            f"[image-gen] {slug}/{agent}: Prompt = {prompt[:150]}...", file=sys.stderr
        )

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

        print(
            f"[image-gen] {slug}/{agent}: Bild gespeichert ({len(image_data)} Bytes)",
            file=sys.stderr,
        )
        self._send_json(
            {"status": "ok", "path": cfg["output"], "size": len(image_data)}
        )

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

    server = QuietThreadingHTTPServer(("", PORT), ShipItHandler)
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
