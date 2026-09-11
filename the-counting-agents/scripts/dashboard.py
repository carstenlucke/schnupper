#!/usr/bin/env python3
"""dashboard.py — Die Übersicht für den Beamer.

Läuft neben der Demo und zeigt, was in den fünf Panes untergeht: welche Zahl
schon bei wem angekommen ist, wie weit jeder Sammler zurückliegt, welche
Befehle die Steuerung geschickt hat. Große Schrift, ruhige Übergänge, ein
Fenster, das sich auf den Beamer legen lässt, ohne dass Herdr im Weg ist.
Farben nach dem THM-Corporate-Design.

    ./scripts/dashboard.py            startet auf Port 8777 und öffnet den Browser
    ./scripts/dashboard.py 9000       anderer Port
    ./scripts/dashboard.py --kein-browser

`./scripts/start.sh` startet das Dashboard von selbst mit; von Hand braucht man
es nur, wenn die Demo schon läuft oder man es auf einem anderen Port will.

Nur Standardbibliothek — dasselbe Muster wie der Server in `ship-it/`. Der
Server liefert die Seite und schiebt Änderungen über Server-Sent Events nach;
der Browser fragt nichts von sich aus ab. Gelesen wird nur, geschrieben nie.

Beenden mit Strg-C.
"""

import hashlib
import json
import os
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_data  # noqa: E402

DEFAULT_PORT = 8777
POLL_SECONDS = 0.4

PAGE = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Counting Agents</title>
<style>
  /* Farben nach dem THM-Corporate-Design (CD-Manual, 3. Auflage), in der
     dunklen Ableitung — der Beamer im Hörsaal ist dunkler als jeder Bildschirm. */
  :root {
    --bg: #1a252b;      /* THM Grau, maximal abgedunkelt */
    --panel: #2a3840;
    --line: #4a5c66;    /* THM Grau */
    --text: #e8ecf0;
    --muted: #93a4ae;
    --open: #3c4e58;    /* Kachel, die noch niemand hat */

    /* Die drei Zusatzfarben des CD sind laut Manual für Infografiken gedacht —
       genau das ist das Zahlenband. Jeder Sammler bekommt eine davon, und sie
       gilt überall gleich: auf der Kachel, im Chip vor dem Namen, im Balken,
       in der Legende. THM Rot bleibt allein den Fehlern vorbehalten. */
    --odd: #00b8e4;     /* THM Hellblau */
    --odd-bg: #10323c;
    --even: #80ba24;    /* THM Grün */
    --even-bg: #24331a;
    --prime: #f4aa00;   /* THM Gelb */
    --wrong: #b8243f;   /* THM Rot, für dunklen Grund aufgehellt */
    --wrong-bg: #3a1a22;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: clamp(16px, 2.5vw, 40px);
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-variant-numeric: tabular-nums;
  }
  header {
    display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap;
    /* Der grüne Strich ist das einzige Stück THM Grün ohne Datenbedeutung —
       er macht die Seite als THM-Seite erkennbar, ohne im Band mitzureden. */
    border-bottom: 3px solid #80ba24;
    padding-bottom: clamp(8px, 1vw, 14px);
  }
  h1 {
    margin: 0; font-size: clamp(20px, 2.2vw, 34px);
    letter-spacing: .14em; text-transform: uppercase; color: var(--text);
  }
  .sub { color: var(--muted); font-size: clamp(13px, 1.1vw, 17px); }
  .summary {
    margin: clamp(12px, 1.4vw, 20px) 0 clamp(18px, 2vw, 30px);
    font-size: clamp(16px, 1.6vw, 26px); color: var(--muted);
  }
  .summary b { color: var(--text); font-weight: 600; }

  /* --- Das Zahlenband ---------------------------------------------------
     Eine Kachel je Zahl im Bus. Die Füllung sagt, wer sie schon hat:
     hellblau = odd, grün = even. Der Punkt oben rechts gehört prime —
     hohl heißt „ist eine Primzahl", gefüllt heißt „prime hat sie". */
  .band {
    display: flex; flex-wrap: wrap; gap: clamp(5px, .6vw, 10px);
    margin-bottom: clamp(10px, 1.4vw, 18px);
  }
  .tile {
    position: relative;
    min-width: clamp(42px, 4.2vw, 72px);
    padding: clamp(6px, .8vw, 14px) clamp(4px, .5vw, 8px);
    border-radius: 8px; text-align: center;
    font-size: clamp(15px, 1.6vw, 27px); font-weight: 600;
    background: var(--panel); color: var(--muted);
    border: 2px solid var(--open);
    transition: background .5s ease, border-color .5s ease,
                color .5s ease, opacity .35s ease;
    animation: einblenden .45s ease both;
  }
  .tile.hat-odd  { border-color: var(--odd);  background: var(--odd-bg);  color: #d6f2fb; }
  .tile.hat-even { border-color: var(--even); background: var(--even-bg); color: #e7f4d2; }
  /* Zuletzt definiert, damit ein Rechenfehler jede andere Färbung übertönt. */
  .tile.wrong { border-color: var(--wrong); background: var(--wrong-bg); color: #ffc6cf; }

  .tile.soll-prime::after, .tile.hat-prime::after {
    content: ""; position: absolute; top: 5px; right: 6px;
    width: 9px; height: 9px; border-radius: 50%;
    border: 2px solid var(--prime); background: transparent;
    transition: background .5s ease;
  }
  .tile.hat-prime::after { background: var(--prime); }
  .tile.wrong::after { border-color: var(--wrong); background: var(--wrong); }

  @keyframes einblenden { from { opacity: 0; transform: translateY(-6px); } }

  /* Ein Agent ist angeklickt: nur seine Zahlen bleiben stehen. So lässt
     sich im Hörsaal einzeln zeigen, was jeder Sammler zu tun hat. */
  /* `:not(.hat-…)` sorgt dafür, dass eine falsch einsortierte Zahl im Fokus
     ihres Agenten stehen bleibt — sonst verschwände genau der Fehler. */
  .band[data-fokus="odd"]   .tile:not(.soll-odd):not(.hat-odd),
  .band[data-fokus="even"]  .tile:not(.soll-even):not(.hat-even),
  .band[data-fokus="prime"] .tile:not(.soll-prime):not(.hat-prime) { opacity: .1; }

  .legende { display: flex; gap: clamp(12px, 1.6vw, 26px); flex-wrap: wrap;
             align-items: center; color: var(--muted);
             font-size: clamp(12px, 1vw, 16px); }
  .legende span { display: flex; align-items: center; gap: 7px; }
  .dot { width: 14px; height: 14px; border-radius: 4px;
         border: 2px solid var(--open); background: var(--panel); }
  .dot.odd   { border-color: var(--odd);   background: var(--odd-bg); }
  .dot.even  { border-color: var(--even);  background: var(--even-bg); }
  .dot.wrong { border-color: var(--wrong); background: var(--wrong-bg); }
  .ring { width: 11px; height: 11px; border-radius: 50%;
          border: 2px solid var(--prime); background: transparent; }
  .ring.voll { background: var(--prime); }
  .hinweis { margin-left: auto; color: var(--muted); opacity: .8; }

  /* --- Die Agenten ------------------------------------------------------ */
  .agents { margin: clamp(20px, 2.4vw, 36px) 0 0; display: grid; gap: 10px; }
  .agent {
    display: grid; align-items: center; gap: clamp(10px, 1.4vw, 24px);
    grid-template-columns: minmax(170px, 1.2fr) auto minmax(90px, .6fr) minmax(90px, .6fr) minmax(120px, 1fr);
    background: var(--panel); border: 1px solid var(--line);
    border-left: 4px solid var(--open);
    border-radius: 10px; padding: clamp(9px, 1.1vw, 18px) clamp(12px, 1.4vw, 22px);
    font-size: clamp(14px, 1.3vw, 22px);
    transition: border-left-color .4s ease, background .2s ease;
  }
  .agent.klickbar { cursor: pointer; }
  .agent.klickbar:hover { background: #31414a; }
  .agent.fokus { background: #31414a; box-shadow: inset 0 0 0 1px var(--muted); }
  /* Der linke Balken trägt die Farbe des Agenten — dieselbe wie im Band.
     Der Betriebszustand kommt ohne eigene Farbe aus: durchgezogen läuft,
     gestrichelt pausiert, gepunktet gestoppt. Sonst müsste sich „pausiert"
     eine Farbe mit einem Sammler teilen, und das trifft im Vortrag immer
     ausgerechnet prime. */
  .agent.a-counter { border-left-color: var(--text); }
  .agent.a-odd     { border-left-color: var(--odd); }
  .agent.a-even    { border-left-color: var(--even); }
  .agent.a-prime   { border-left-color: var(--prime); }
  .agent.paused  { border-left-style: dashed; }
  .agent.stopped { border-left-style: dotted; }
  .agent .name { font-weight: 600; display: flex; align-items: center; gap: 10px; }
  .agent .name small { display: block; color: var(--muted); font-weight: 400;
                       font-size: .72em; letter-spacing: .04em; }
  .chip { width: 14px; height: 14px; border-radius: 4px; flex: none;
          border: 2px solid var(--open); background: var(--panel); }
  .chip.odd   { border-color: var(--odd);   background: var(--odd-bg); }
  .chip.even  { border-color: var(--even);  background: var(--even-bg); }
  .chip.prime { border-color: var(--prime); background: var(--prime); border-radius: 50%; }
  .chip.counter { border-color: var(--text); background: transparent; }
  .agent .status { color: var(--muted); white-space: nowrap; }
  .agent.paused  .status { color: var(--text); }
  .agent.stopped .status { color: var(--wrong); }
  .agent .zahl { color: var(--text); font-weight: 600; }
  /* Zurückliegen ist die Nachricht, Gleichstand der Normalfall. */
  .agent .lag.zurueck { color: var(--text); }
  .agent .lag.aktuell { color: var(--muted); }
  .balken { height: 10px; border-radius: 5px; background: var(--open); overflow: hidden; }
  .balken i { display: block; height: 100%; background: var(--muted);
              transition: width .5s ease; }
  .a-odd   .balken i { background: var(--odd); }
  .a-even  .balken i { background: var(--even); }
  .a-prime .balken i { background: var(--prime); }
  .still { color: var(--wrong); font-size: .8em; }

  .ticker { margin-top: clamp(18px, 2vw, 30px); color: var(--muted);
            font-size: clamp(12px, 1.1vw, 18px); }
  .ticker h2 { font-size: 1em; letter-spacing: .1em; text-transform: uppercase;
               color: var(--muted); margin: 0 0 8px; font-weight: 600; }
  .ticker li { list-style: none; padding: 3px 0; }
  .ticker time { color: var(--line); margin-right: 12px; }
  .ticker b { color: var(--text); font-weight: 600; }

  footer { margin-top: clamp(20px, 2vw, 34px); color: var(--muted); opacity: .7;
           font-size: clamp(11px, .9vw, 15px); }
  .offline { color: var(--wrong); }
</style>
</head>
<body>
  <header>
    <h1>Counting Agents</h1>
    <span class="sub">pi &middot; Herdr</span>
    <span class="sub" id="uhr" style="margin-left:auto"></span>
  </header>

  <p class="summary" id="summary">Warte auf den Bus&hellip;</p>

  <div class="band" id="band"></div>
  <div class="legende">
    <span><i class="dot"></i>noch niemand</span>
    <span><i class="dot odd"></i>odd hat sie</span>
    <span><i class="dot even"></i>even hat sie</span>
    <span><i class="ring"></i>Primzahl</span>
    <span><i class="ring voll"></i>prime hat sie</span>
    <span><i class="dot wrong"></i>falsch einsortiert</span>
    <span class="hinweis">Agent anklicken &rarr; nur dessen Zahlen</span>
  </div>

  <div class="agents" id="agents"></div>

  <div class="ticker">
    <h2>Steuerung</h2>
    <ul id="ticker"><li>keine Befehle</li></ul>
  </div>

  <footer id="fuss">Liest nur mit &mdash; Bus und Zustand bleiben unberührt.</footer>

<script>
const LABEL = {
  counter: ["counter", "Zähler"],
  odd:     ["odd", "Ungerade"],
  even:    ["even", "Gerade"],
  prime:   ["prime", "Primzahlen"],
};
// Das Zeichen vor dem Wort trägt den Zustand mit — auf dem Beamer erkennt man
// eine Form aus der letzten Reihe zuverlässiger als einen Farbton.
const STATUS = { running: "● läuft", paused: "‖ pausiert", stopped: "■ gestoppt" };
const SAMMLER = ["odd", "even", "prime"];

const band = document.getElementById("band");
const kacheln = new Map();   // Wert -> Element, damit nur Geändertes neu gesetzt wird
let fokus = null;            // angeklickter Sammler, oder null

function zeichneBand(numbers) {
  for (const n of numbers) {
    let el = kacheln.get(n.value);
    if (!el) {
      el = document.createElement("div");
      el.textContent = n.value;
      band.appendChild(el);
      kacheln.set(n.value, el);
    }
    const klassen = ["tile"];
    for (const a of SAMMLER) {
      if (n.expected[a])  klassen.push("soll-" + a);
      if (n.collected[a]) klassen.push("hat-" + a);
    }
    if (n.wrong.length) klassen.push("wrong");
    const neu = klassen.join(" ");
    if (el.className !== neu) el.className = neu;   // sonst startet die Animation neu
  }
  // Nach einem Reset verschwinden Zahlen aus dem Bus.
  const vorhanden = new Set(numbers.map(n => n.value));
  for (const [wert, el] of kacheln) {
    if (!vorhanden.has(wert)) { el.remove(); kacheln.delete(wert); }
  }
}

function setzeFokus(name) {
  fokus = (fokus === name) ? null : name;
  if (fokus) band.dataset.fokus = fokus; else delete band.dataset.fokus;
  for (const zeile of document.querySelectorAll(".agent")) {
    zeile.classList.toggle("fokus", zeile.dataset.agent === fokus);
  }
}

function zeichneAgenten(data) {
  const ziel = document.getElementById("agents");
  const latest = data.bus.latest_seq || 1;
  ziel.innerHTML = "";
  for (const name of ["counter", "odd", "even", "prime"]) {
    const a = data.agents[name];
    const [kurz, lang] = LABEL[name];
    const zeile = document.createElement("div");
    zeile.className = "agent a-" + name + " " + a.status
      + (SAMMLER.includes(name) ? " klickbar" : "")
      + (fokus === name ? " fokus" : "");
    zeile.dataset.agent = name;

    const mitte = name === "counter"
      ? `<span class="zahl">Wert ${a.last_value}</span><span></span><span></span>`
      : `<span class="zahl">${a.count} Zahlen</span>
         <span class="lag ${a.lag ? "zurueck" : "aktuell"}">${a.lag ? a.lag + " zurück" : "aktuell"}</span>
         <span class="balken"><i style="width:${Math.min(100, 100 * a.last_seq / latest)}%"></i></span>`;

    zeile.innerHTML = `
      <span class="name"><i class="chip ${name}"></i>${kurz}<small>${lang}</small></span>
      <span class="status">${STATUS[a.status] || a.status}${a.still ? ` <span class="still">· seit ${Math.round(a.idle_seconds)}s still</span>` : ""}</span>
      ${mitte}`;
    if (SAMMLER.includes(name)) {
      zeile.addEventListener("click", () => setzeFokus(name));
    }
    ziel.appendChild(zeile);
  }
}

function zeichneTicker(events) {
  const ziel = document.getElementById("ticker");
  if (!events.length) { ziel.innerHTML = "<li>keine Befehle</li>"; return; }
  ziel.innerHTML = events.slice().reverse().slice(0, 6).map(e =>
    `<li><time>${(e.timestamp || "").slice(11, 19)}</time>${e.target} &larr; <b>${e.command}</b></li>`
  ).join("");
}

function zeichne(data) {
  const takt = data.bus.seconds_per_number;
  document.getElementById("summary").innerHTML =
    `<b>${data.bus.count}</b> Zahlen im Bus &middot; zuletzt <b>${data.bus.last_value}</b>` +
    (takt ? ` &middot; ${takt.toFixed(1).replace(".", ",")} s pro Zahl` : "");
  document.getElementById("uhr").textContent = data.generated_at;
  zeichneBand(data.numbers);
  zeichneAgenten(data);
  zeichneTicker(data.control);
}

const quelle = new EventSource("/events");
quelle.onmessage = (e) => zeichne(JSON.parse(e.data));
quelle.onerror = () => {
  document.getElementById("fuss").innerHTML =
    '<span class="offline">Verbindung zum Dashboard verloren &mdash; läuft dashboard.py noch?</span>';
};
quelle.onopen = () => {
  document.getElementById("fuss").textContent =
    "Liest nur mit — Bus und Zustand bleiben unberührt.";
};
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_page()
        elif self.path == "/events":
            self._send_events()
        else:
            self.send_error(404)

    def _send_page(self):
        body = PAGE.encode("utf8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_events(self):
        """Server-Sent Events: geschickt wird nur, wenn sich etwas geändert hat.
        Die Verbindung bleibt offen, der Browser fragt nie von sich aus nach."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        letzter = None
        stille = 0.0
        try:
            while True:
                data = dashboard_data.snapshot()
                # generated_at ändert sich jede Sekunde und zählt nicht als Änderung.
                kern = dict(data)
                kern.pop("generated_at", None)
                fingerprint = hashlib.md5(
                    json.dumps(kern, sort_keys=True).encode("utf8")
                ).hexdigest()
                if fingerprint != letzter:
                    letzter = fingerprint
                    stille = 0.0
                    payload = json.dumps(data, ensure_ascii=False)
                    self.wfile.write(("data: %s\n\n" % payload).encode("utf8"))
                    self.wfile.flush()
                else:
                    stille += POLL_SECONDS
                    if stille >= 15:  # Kommentarzeile hält die Verbindung offen
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                        stille = 0.0
                time.sleep(POLL_SECONDS)
        except (BrokenPipeError, ConnectionResetError):
            pass  # Tab geschlossen — kein Fehler.

    def log_message(self, *args):
        pass  # Die Zugriffsprotokolle stören im Vorführ-Pane nur.


def main():
    port = DEFAULT_PORT
    browser_oeffnen = True
    for arg in sys.argv[1:]:
        if arg in ("--kein-browser", "--no-open"):
            browser_oeffnen = False
        elif arg.isdigit():
            port = int(arg)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    url = "http://127.0.0.1:%d/" % port
    print("Dashboard läuft auf %s" % url)
    print("Beenden mit Strg-C.")
    if browser_oeffnen:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard beendet.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
