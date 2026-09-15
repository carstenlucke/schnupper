#!/usr/bin/env python3
"""Agent Party — Server für die Schnuppervorlesung.

Die Teilnehmenden legen Rollenprofile an, wählen daraus eine Besetzung und
geben ihr ein Thema. Danach diskutieren die gewählten Profile reihum. Jeder
Beitrag ist ein eigener Aufruf der pi CLI.

Nur Python-Standardbibliothek, keine externen Abhängigkeiten.
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

PORT = 8100
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFIL_DIR = os.path.join(BASE_DIR, "profile")
PARTYS_DIR = os.path.join(BASE_DIR, "partys")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

# Die sechs Farben des THM-Corporate-Designs. Mehr gibt es nicht — eine
# unbekannte Farbe wird auf "grau" zurückgesetzt, statt den Eintrag abzulehnen.
FARBEN = ["gruen", "grau", "rot", "gelb", "hellblau", "blau"]

# Denkstufen von pi. "off" bedeutet: Flag gar nicht erst mitgeben.
THINKING_STUFEN = ["off", "minimal", "low", "medium", "high", "xhigh"]

# Diese drei Anbieter sind die drei Wege, die in der Vorlesung gezeigt werden:
# ChatGPT-Abo, Cloud-Anbieter, lokales Modell. Was pi sonst noch kennt
# (github-copilot etwa), bleibt bewusst aus der Auswahl.
ANBIETER = ["openai-codex", "tensorx", "lmstudio"]

MAX_RUNDEN = 5
MAX_TEILNEHMER = 8
MIN_TEILNEHMER = 2

# Deckel für den Gesprächsverlauf im Prompt. Greift im Normalfall nie —
# siehe kuerze_verlauf().
VERLAUF_ZEICHEN = 6000
BEITRAG_ZEICHEN = 800

# Ein Zwischenruf ist ein Satz, kein Vortrag. Länger abgeschnitten, statt
# abgelehnt — im Hörsaal soll nichts an einer Kleinigkeit scheitern.
ZWISCHENRUF_ZEICHEN = 500

SAFE_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _load_dotenv():
    """Lies .env, ohne bestehende Umgebungsvariablen zu überschreiben."""
    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

STANDARD_MODELL = (
    os.environ.get("AGENT_PARTY_STANDARD_MODELL") or "openai-codex/gpt-5.6-luna"
)


# ============================================================================
# Kleinkram
# ============================================================================

UMLAUTE = {
    "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
    "Ä": "ae", "Ö": "oe", "Ü": "ue",
}


def slugify(name: str) -> str:
    """Aus einem Anzeigenamen einen dateisystemtauglichen Slug machen."""
    text = name.strip().lower()
    for zeichen, ersatz in UMLAUTE.items():
        text = text.replace(zeichen.lower(), ersatz)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "profil"


def sicherer_pfad(slug: str, basis: str) -> str | None:
    """Pfad unterhalb von `basis` — oder None, wenn der Slug nicht taugt.

    Zwei Ebenen, weil hier im Gegensatz zu den Schwesterprojekten *alle*
    Slugs aus Nutzereingaben stammen: erst die Zeichen-Whitelist, dann eine
    realpath-Prüfung, die auch Symlinks abfängt.
    """
    if not slug or not SAFE_SEGMENT_RE.match(slug):
        return None
    ziel = os.path.realpath(os.path.join(basis, slug))
    if not ziel.startswith(os.path.realpath(basis) + os.sep):
        return None
    return ziel


def jetzt_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _einzeilig(wert) -> str:
    """Eine Zeile draus machen — so, wie das flache Frontmatter es braucht.

    Zeilenumbrüche würden es zerreißen, drei Bindestriche ebenso: sie sähen
    beim nächsten Lesen aus wie das Ende des Kopfteils.
    """
    return re.sub(r"-{3,}", "–", " ".join(str(wert).split()))


def _kurz(text: str, zeichen: int) -> str:
    text = text.strip()
    if len(text) <= zeichen:
        return text
    return text[:zeichen].rstrip() + " …"


# ============================================================================
# Profile — die Markdown-Datei ist der Zustand, es gibt keine Liste im Speicher
# ============================================================================

def frontmatter_lesen(inhalt: str) -> tuple[dict, str]:
    """Flaches Frontmatter lesen: eine Zeile je Feld, `schluessel: wert`.

    Kein YAML-Parser. Eingerückte Zeilen werden übersprungen, beim Wert
    gewinnt der erste Doppelpunkt — eine Beschreibung darf also selbst einen
    enthalten.
    """
    meta: dict[str, str] = {}
    rumpf = inhalt
    if inhalt.startswith("---"):
        ende = inhalt.find("---", 3)
        if ende != -1:
            kopf = inhalt[3:ende].strip()
            rumpf = inhalt[ende + 3:].strip()
            for zeile in kopf.split("\n"):
                if ":" in zeile and not zeile.startswith(" "):
                    schluessel, _, wert = zeile.partition(":")
                    meta[schluessel.strip()] = wert.strip()
    return meta, rumpf


def frontmatter_schreiben(daten: dict) -> str:
    """Profil-Dict in Dateiform bringen. Feldreihenfolge ist fest."""
    zeilen = ["---"]
    for feld in ("name", "beschreibung", "model", "thinking", "farbe"):
        zeilen.append(f"{feld}: {daten.get(feld, '')}")
    zeilen.append("---")
    zeilen.append("")
    zeilen.append(daten.get("text", "").strip())
    zeilen.append("")
    return "\n".join(zeilen)


def profil_pfad(slug: str) -> str | None:
    """Dateipfad eines Profils. Die Endung kommt erst nach der Slug-Prüfung
    dazu — ein Punkt ist im Slug selbst nicht erlaubt."""
    ordner = sicherer_pfad(slug, PROFIL_DIR)
    return ordner + ".md" if ordner else None


def profil_lesen(slug: str) -> dict | None:
    pfad = profil_pfad(slug)
    if not pfad or not os.path.isfile(pfad):
        return None
    with open(pfad, "r", encoding="utf-8") as f:
        inhalt = f.read()
    meta, rumpf = frontmatter_lesen(inhalt)
    return {
        "slug": slug,
        "name": meta.get("name") or slug,
        "beschreibung": meta.get("beschreibung", ""),
        "model": meta.get("model", ""),
        "thinking": meta.get("thinking", "medium"),
        "farbe": meta.get("farbe") if meta.get("farbe") in FARBEN else "grau",
        "text": rumpf,
    }


def profil_liste() -> list[dict]:
    if not os.path.isdir(PROFIL_DIR):
        return []
    profile = []
    for datei in sorted(os.listdir(PROFIL_DIR)):
        if not datei.endswith(".md"):
            continue
        profil = profil_lesen(datei[:-3])
        if profil:
            profile.append(profil)
    profile.sort(key=lambda p: p["name"].lower())
    return profile


def profil_pruefen(daten: dict) -> tuple[dict, str | None]:
    """Eingabe säubern statt abzulehnen.

    Nur Name und Rollentext sind Pflicht; alles andere wird auf einen
    sinnvollen Wert gezogen. Im Hörsaal soll nichts an einer Kleinigkeit
    scheitern.
    """
    name = str(daten.get("name", "")).strip()
    text = str(daten.get("text", "")).strip()
    if not name:
        return {}, "Das Profil braucht einen Namen."
    if not text:
        return {}, "Das Profil braucht einen Rollentext."

    thinking = str(daten.get("thinking", "")).strip()
    if thinking not in THINKING_STUFEN:
        thinking = "medium"

    farbe = str(daten.get("farbe", "")).strip()
    if farbe not in FARBEN:
        farbe = "grau"

    return {
        "name": _einzeilig(name),
        "beschreibung": _einzeilig(daten.get("beschreibung", "")),
        "model": _einzeilig(daten.get("model", "")),
        "thinking": thinking,
        "farbe": farbe,
        "text": text,
    }, None


def profil_schreiben(slug: str, daten: dict) -> bool:
    """Über eine Temp-Datei schreiben und dann umbenennen.

    Eine halb geschriebene Datei wäre beim nächsten Party-Start ein kaputter
    Systemprompt — os.replace ist auf einem Dateisystem atomar.
    """
    pfad = profil_pfad(slug)
    if not pfad:
        return False
    os.makedirs(PROFIL_DIR, exist_ok=True)
    temp = pfad + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        f.write(frontmatter_schreiben(daten))
    os.replace(temp, pfad)
    return True


def profil_loeschen(slug: str) -> bool:
    pfad = profil_pfad(slug)
    if not pfad or not os.path.isfile(pfad):
        return False
    os.remove(pfad)
    return True


def profil_in_offener_party(slug: str) -> list[str]:
    """Namen der Partys, die dieses Profil brauchen und noch nicht durch sind."""
    betroffen = []
    for eintrag in party_liste():
        if eintrag["status"] == "fertig":
            continue
        if slug in eintrag["sitzung"].get("teilnehmer", []):
            betroffen.append(eintrag["sitzung"].get("titel", eintrag["slug"]))
    return betroffen


# ============================================================================
# Modelle — einmal pro Serverlauf von pi erfragt
# ============================================================================

_modelle_cache: list[dict] | None = None


def modelle_lesen() -> list[dict]:
    """`pi --list-models` auswerten, gefiltert auf die drei Anbieter.

    Die Ausgabe hat eine Kopfzeile und danach feste Spalten
    `provider model context max-out thinking images` — zerlegbar per split().
    """
    global _modelle_cache
    if _modelle_cache is not None:
        return _modelle_cache

    modelle: list[dict] = []
    try:
        ergebnis = subprocess.run(
            ["pi", "--list-models"],
            capture_output=True, text=True, timeout=15,
            encoding="utf-8", errors="replace",
        )
        for zeile in ergebnis.stdout.splitlines()[1:]:
            spalten = zeile.split()
            if len(spalten) < 5:
                continue
            anbieter, modell = spalten[0], spalten[1]
            if anbieter not in ANBIETER:
                continue
            modelle.append({
                "id": f"{anbieter}/{modell}",
                "anbieter": anbieter,
                "modell": modell,
                "denken": spalten[4] == "yes",
            })
    except (OSError, subprocess.SubprocessError):
        # pi fehlt oder antwortet nicht. Das Dashboard zeigt dann ein freies
        # Textfeld statt eines Dropdowns — die Demo bleibt bedienbar.
        modelle = []

    _modelle_cache = modelle
    return modelle


# ============================================================================
# Prompts
# ============================================================================

SYSTEMPROMPT_ENTWURF = """Du schreibst Rollenprofile für eine Gesprächsrunde, in der mehrere KI-Agenten
reihum miteinander diskutieren. Aus einer kurzen Stichwortidee machst du eine
vollständige Profildatei.

Gib ausschließlich die Datei aus. Kein Vorwort, kein Nachwort, keine Rückfrage,
keine Code-Zäune, keine Emoji. Die erste Zeile deiner Antwort ist genau drei
Bindestriche.

So ist die Datei aufgebaut:

---
name: <Anzeigename der Rolle, ein bis drei Wörter>
beschreibung: <ein Halbsatz, höchstens 60 Zeichen>
model: <einer der erlaubten Modellnamen>
thinking: <off, minimal, low, medium, high oder xhigh>
farbe: <gruen, grau, rot, gelb, hellblau oder blau>
---
<Rollentext>

Regeln für den oberen Teil zwischen den Bindestrichzeilen:
- Genau diese fünf Zeilen, genau in dieser Reihenfolge, je Zeile ein Feld.
- Schreibweise "schluessel: wert". Keine Anführungszeichen, kein Zeilenumbruch
  innerhalb eines Wertes, keine Leerzeile.
- Erlaubte Modellnamen: {modelle}
- Im Zweifel nimm model: {standardmodell} und thinking: medium.
- Die Farbe wählst du passend zur Rolle; sie ist nur eine Anzeigefarbe.

Regeln für den Rollentext unter der zweiten Bindestrichzeile:
- Er ist die Anweisung an die Rolle selbst, also Anrede in der zweiten Person:
  "Du bist ...".
- 80 bis 150 Wörter. Normales Deutsch, ganze Sätze, ein Absatz oder zwei.
- Keine Aufzählungszeichen, keine Überschriften, keine Sternchen, kein Markdown.
- Beschreibe vier Dinge: wer die Rolle ist, worauf sie in einer Diskussion
  achtet, wie sie spricht, und woran sie sich reibt.
- Schreibe nichts über Länge, Format, Reihenfolge oder Rundenzahl der Beiträge.
  Das regelt die Gesprächsleitung und würde sich hier nur widersprechen.
- Keine Namen realer Personen, keine Emoji, keine Anführungszeichen um den
  gesamten Text.
"""

# So heißt der Mensch am Rechner im Prompt: die Person, die die Runde leitet,
# dazwischenruft und am Ende ein Fazit zieht.
LEITUNG = "Gesprächsleitung"

ZWISCHENRUF_VORLAGE = """
ZWISCHENRUF DER GESPRÄCHSLEITUNG
{texte}
Nimm diesen Einwurf ernst: Er ist keine Wortmeldung, auf die du antwortest,
sondern die Vorgabe, an der du dich ausrichtest. Geh gleich zu Beginn darauf
ein und bleibe dabei in deiner Rolle.
"""

BEITRAG_VORLAGE = """Du nimmst an einer Gesprächsrunde teil. Du sprichst als {name}.

THEMA
{titel}

{starter}

WER MITDISKUTIERT
{teilnehmer}

BISHERIGER VERLAUF
{verlauf}
{zwischenruf}
DU BIST JETZT AN DER REIHE — Runde {runde} von {runden}.
Antworte als {name}, auf Deutsch, in der Ich-Form.
Gehe auf mindestens einen Beitrag vor dir ein und nenne die Person beim Namen,
sofern schon jemand gesprochen hat.
Schreibe 3 bis 6 Sätze und höchstens 120 Wörter.
Gib nur deinen Redebeitrag aus: kein Namensschild davor, keine Anführungszeichen,
keine Regieanweisungen, keine Aufzählungspunkte, keine Überschriften, keine Emoji.
Wiederhole nicht, was schon gesagt wurde — bring etwas Neues ein.
"""


# Das Fazit ist der einzige Beitrag, dessen Rolle nicht aus profile/ kommt:
# Die Gesprächsleitung ist keine Stimme am Tisch, sondern der Blick von außen.
# Ihr Systemprompt steht deshalb hier im Code — wie der für „Profil
# ausarbeiten" auch.
SYSTEMPROMPT_FAZIT = """Du bist die Gesprächsleitung einer Diskussionsrunde und ziehst am Ende Bilanz.
Du hast selbst keine Meinung zum Thema und ergreifst für niemanden Partei. Du
hörst zu und ordnest ein.

Schreibe auf Deutsch, sachlich und ohne Floskeln. Kein Vorwort, keine Anrede,
keine Rückfrage, keine Emoji.

Gib genau drei Abschnitte aus, jeder mit dieser Überschrift und darunter zwei
bis vier Sätzen:

**Worin sie sich einig sind**
**Wo sie sich widersprechen**
**Was offen bleibt**

Nenne die Beteiligten beim Namen, wenn du ihre Position wiedergibst. Erfinde
nichts dazu: Was im Verlauf nicht vorkommt, steht auch nicht im Fazit. Bleib
insgesamt unter 220 Wörtern."""

FAZIT_VORLAGE = """Fasse diese Gesprächsrunde zusammen.

THEMA
{titel}

{starter}

WER MITDISKUTIERT HAT
{teilnehmer}

DER VERLAUF
{verlauf}
"""


def systemprompt_entwurf() -> str:
    ids = [m["id"] for m in modelle_lesen()][:10]
    return SYSTEMPROMPT_ENTWURF.format(
        modelle=", ".join(ids) if ids else STANDARD_MODELL,
        standardmodell=STANDARD_MODELL,
    )


def teilnehmer_block(profile: list[dict], ich_platz: int) -> str:
    zeilen = []
    for platz, profil in enumerate(profile):
        zeile = f"- {profil['name']}"
        if profil["beschreibung"]:
            zeile += f" – {profil['beschreibung']}"
        # Über den Platz, nicht über den Slug: eine von Hand bearbeitete oder
        # ältere sitzung.json kann dasselbe Profil zweimal enthalten, und dann
        # trügen beide Zeilen "(das bist du)".
        if platz == ich_platz:
            zeile += " (das bist du)"
        zeilen.append(zeile)
    return "\n".join(zeilen)


def _sprecher(eintrag: dict, namen: dict[str, str]) -> str:
    """Wer hat das gesagt — für den Verlauf im Prompt.

    Die Gesprächsleitung ist der Mensch am Rechner. Sie tritt unter eigenem
    Namen auf, damit die Profile ihren Einwurf nicht für den Beitrag einer
    anderen Rolle halten und ihn beantworten statt aufzugreifen.
    """
    art = eintrag.get("art", "beitrag")
    if art == "zwischenruf":
        return f"{LEITUNG} (Zwischenruf)"
    if art == "fazit":
        return f"{LEITUNG} (Zwischenfazit)"
    slug = eintrag.get("profil", "")
    return namen.get(slug, slug)


def offene_zwischenrufe(eintraege: list[dict]) -> list[str]:
    """Die Zwischenrufe, auf die noch niemand geantwortet hat.

    Alles ab dem letzten Beitrag: was davor liegt, ist im Verlauf schon
    aufgegriffen worden und braucht keine eigene Aufforderung mehr.
    """
    offen = []
    for eintrag in reversed(eintraege):
        if ist_beitrag(eintrag):
            break
        if eintrag.get("art") == "zwischenruf":
            offen.append(eintrag.get("text", ""))
    return list(reversed(offen))


def kuerze_verlauf(eintraege: list[dict], namen: dict[str, str]) -> str:
    """Den Gesprächsverlauf für den Prompt aufbereiten.

    Zwei Stufen: erst ein Deckel je Beitrag, dann ein Fenster über die
    Gesamtlänge. Beides greift im Normalfall nicht — es sind Sicherungen
    gegen ein Modell, das die Längenvorgabe ignoriert, bzw. gegen sehr lange
    Partys. Die ausgelassene Mitte wird sichtbar markiert, nicht heimlich
    entfernt.
    """
    if not eintraege:
        return "(Noch hat niemand gesprochen. Du eröffnest die Runde.)"

    stuecke = [
        f"{_sprecher(e, namen)}: {_kurz(e['text'], BEITRAG_ZEICHEN)}"
        for e in eintraege
    ]

    if sum(len(s) for s in stuecke) <= VERLAUF_ZEICHEN or len(stuecke) <= 8:
        return "\n\n".join(stuecke)

    ausgelassen = len(stuecke) - 7
    return "\n\n".join(
        [stuecke[0], f"[… {ausgelassen} frühere Beiträge ausgelassen …]"]
        + stuecke[-6:]
    )


def baue_beitrag_prompt(sitzung: dict, profile: list[dict], ich_platz: int,
                        runde: int, eintraege: list[dict]) -> str:
    """Der Prompt für einen Beitrag — wer dran ist, sagt der Platz.

    Der Platz und nicht das Profil, damit es auch dann eindeutig bleibt, wenn
    in einer alten sitzung.json dasselbe Profil zweimal am Tisch sitzt.
    """
    ich = profile[ich_platz]
    namen = {p["slug"]: p["name"] for p in profile}
    offen = offene_zwischenrufe(eintraege)
    return BEITRAG_VORLAGE.format(
        name=ich["name"],
        titel=sitzung.get("titel", ""),
        starter=sitzung.get("starter", ""),
        teilnehmer=teilnehmer_block(profile, ich_platz),
        verlauf=kuerze_verlauf(eintraege, namen),
        zwischenruf=ZWISCHENRUF_VORLAGE.format(
            texte="\n".join(f"„{text}“" for text in offen)) if offen else "",
        runde=runde,
        runden=sitzung.get("runden", 1),
    )


def baue_fazit_prompt(sitzung: dict, profile: list[dict],
                      eintraege: list[dict]) -> str:
    namen = {p["slug"]: p["name"] for p in profile}
    return FAZIT_VORLAGE.format(
        titel=sitzung.get("titel", ""),
        starter=sitzung.get("starter", ""),
        teilnehmer="\n".join(
            f"- {p['name']}" + (f" – {p['beschreibung']}" if p["beschreibung"] else "")
            for p in profile),
        verlauf=kuerze_verlauf(eintraege, namen),
    )


# ============================================================================
# pi-Anbindung
# ============================================================================

def baue_pi_befehl(system_prompt: str, prompt: str,
                   modell: str = "", thinking: str = "") -> list[str]:
    """Den pi-Aufruf zusammensetzen.

    -nt  – kein einziges Werkzeug. Ein Party-Agent kann antworten, sonst
           nichts: nicht lesen, nicht schreiben, nicht ins Netz.
    --no-session – jeder Beitrag ist ein eigener Prozess. Das Modell erinnert
           sich nicht; den Verlauf geben wir jedes Mal neu im Prompt mit.
    -nc -ns -np -ne – keine globalen Kontextdateien, Skills, Prompt-Vorlagen
           oder Extensions. Die Demo läuft auf jedem Rechner gleich.
    --mode json – statt -p, damit die Denkschritte live sichtbar werden.
    """
    cmd = ["pi", "--mode", "json", "--no-session",
           "-nt", "-nc", "-ns", "-np", "-ne"]

    # AGENT_PARTY_MODEL schlägt alles andere — der Hebel für den Hörsaal.
    modell = os.environ.get("AGENT_PARTY_MODEL") or modell or STANDARD_MODELL
    cmd += ["--model", modell]

    # Nicht jedes Modell kann denken (siehe die thinking-Spalte von
    # `pi --list-models`); bei "off" oder leer bleibt das Flag weg.
    if thinking and thinking != "off":
        cmd += ["--thinking", thinking]

    cmd += ["--system-prompt", system_prompt, "--", prompt]
    return cmd


def starte_pi(cmd: list[str]) -> subprocess.Popen:
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # pi liest die Standardeingabe mit in den Auftrag ein. Bliebe sie
        # offen, wartete der Prozess für immer auf ihr Ende.
        stdin=subprocess.DEVNULL,
        cwd=BASE_DIR,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class PiStrom:
    """Übersetzt den JSON-Strom von pi in Ereignisse fürs Dashboard.

    Das Gegenstück zur Terminalausgabe der Schwesterprojekte — hier ohne ein
    einziges ANSI-Zeichen, weil das Frontend Sprechblasen zeigt und kein
    Terminal.
    """

    def __init__(self) -> None:
        self.text: list[str] = []
        self.denken: list[str] = []
        self.fehler: str | None = None
        self.kosten: float = 0.0

    @property
    def voller_text(self) -> str:
        return "".join(self.text).strip()

    @property
    def volles_denken(self) -> str:
        return "".join(self.denken).strip()

    def verarbeite(self, zeile: str) -> dict | None:
        """Eine Ausgabezeile von pi → genau ein Ereignis oder None."""
        zeile = zeile.strip()
        if not zeile:
            return None

        try:
            ereignis = json.loads(zeile)
        except json.JSONDecodeError:
            # Meldung von pi selbst – fehlender Login, unbekanntes Modell.
            # Muss sichtbar bleiben, sonst rätselt man im Hörsaal.
            return {"art": "meldung", "text": zeile}

        if not isinstance(ereignis, dict):
            return {"art": "meldung", "text": zeile}

        art = ereignis.get("type")

        if art == "message_update":
            return self._strom(ereignis.get("assistantMessageEvent") or {})

        if art == "message_end":
            # stopReason und errorMessage stecken in der Nachricht, nicht im
            # Ereignis selbst. Eine Ebene zu hoch gelesen, und jeder
            # Anbieterfehler bliebe unsichtbar — pi endet dabei mit Code 0.
            nachricht = ereignis.get("message") or {}
            grund = nachricht.get("stopReason")
            if nachricht.get("role") == "assistant" and grund in ("error", "aborted"):
                self.fehler = nachricht.get("errorMessage") or f"pi meldet: {grund}"
                return {"art": "fehler", "text": self.fehler}
            return None

        if art == "auto_retry_start":
            sekunden = round((ereignis.get("delayMs") or 0) / 1000)
            versuch = ereignis.get("attempt", "?")
            maximal = ereignis.get("maxAttempts", "?")
            # pi verwirft den angefangenen Beitrag und streamt ihn neu. Was
            # bisher kam, muss deshalb auch hier weg — sonst steht der Anfang
            # zweimal in verlauf.jsonl und vergiftet alle Folgeprompts.
            self.text.clear()
            self.denken.clear()
            self.fehler = None
            return {"art": "meldung", "neustart": True,
                    "text": f"Neuer Versuch {versuch}/{maximal} in {sekunden} s"}

        if art == "agent_end" and not ereignis.get("willRetry"):
            self.kosten = self._kosten(ereignis.get("messages") or [])
            return {"art": "ende", "kosten": self.kosten}

        return None

    def _strom(self, teil: dict) -> dict | None:
        art = teil.get("type")
        if art == "text_delta":
            delta = teil.get("delta", "")
            self.text.append(delta)
            return {"art": "text", "delta": delta}
        if art == "thinking_delta":
            delta = teil.get("delta", "")
            self.denken.append(delta)
            return {"art": "denken", "delta": delta}
        return None

    @staticmethod
    def _kosten(nachrichten: list) -> float:
        gesamt = 0.0
        for nachricht in nachrichten:
            if not isinstance(nachricht, dict):
                continue
            verbrauch = nachricht.get("usage") or {}
            kosten = verbrauch.get("cost") or {}
            try:
                gesamt += float(kosten.get("total") or 0)
            except (TypeError, ValueError):
                pass
        return round(gesamt, 4)


# ============================================================================
# Sitzungen und Verlauf
# ============================================================================

def sitzung_lesen(slug: str) -> dict | None:
    ordner = sicherer_pfad(slug, PARTYS_DIR)
    if not ordner:
        return None
    pfad = os.path.join(ordner, "sitzung.json")
    if not os.path.isfile(pfad):
        return None
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def sitzung_schreiben(slug: str, sitzung: dict) -> bool:
    ordner = sicherer_pfad(slug, PARTYS_DIR)
    if not ordner:
        return False
    os.makedirs(ordner, exist_ok=True)
    with open(os.path.join(ordner, "sitzung.json"), "w", encoding="utf-8") as f:
        json.dump(sitzung, f, ensure_ascii=False, indent=2)
    return True


def verlauf_pfad(slug: str) -> str | None:
    ordner = sicherer_pfad(slug, PARTYS_DIR)
    return os.path.join(ordner, "verlauf.jsonl") if ordner else None


def verlauf_lesen(slug: str) -> list[dict]:
    """Beiträge aus der jsonl lesen.

    Eine kaputte letzte Zeile wird verworfen: ein Beitrag ist größer als das,
    was das Dateisystem am Stück schreibt, ein Absturz mittendrin also
    möglich.
    """
    pfad = verlauf_pfad(slug)
    if not pfad or not os.path.isfile(pfad):
        return []
    eintraege = []
    with open(pfad, "r", encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if not zeile:
                continue
            try:
                eintraege.append(json.loads(zeile))
            except json.JSONDecodeError:
                continue
    return eintraege


# Zwei Threads hängen an dieselbe Datei an: die Party-Schleife einen Beitrag,
# ein Request-Thread einen Zwischenruf. Eine Zeile je Schreibvorgang, unter
# einem Lock — sonst schieben sich zwei halbe JSON-Zeilen ineinander.
verlauf_lock = threading.Lock()


def verlauf_anhaengen(slug: str, eintrag: dict) -> None:
    pfad = verlauf_pfad(slug)
    if not pfad:
        return
    with verlauf_lock, open(pfad, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag, ensure_ascii=False) + "\n")
        f.flush()


def ist_beitrag(eintrag: dict) -> bool:
    """Zählt dieser Eintrag als Redebeitrag?

    In der jsonl steht dreierlei: Beiträge der Profile, Zwischenrufe der
    Gesprächsleitung und das Fazit. Nur das erste zählt gegen
    `runden × teilnehmer` — ein Zwischenruf darf keine Runde verschlucken.
    Einträge ohne `art` stammen aus einer Sitzung von vor dieser
    Unterscheidung und sind Beiträge.
    """
    return eintrag.get("art", "beitrag") == "beitrag"


def nur_beitraege(eintraege: list[dict]) -> list[dict]:
    return [e for e in eintraege if ist_beitrag(e)]


def party_erwartet(sitzung: dict) -> int:
    return int(sitzung.get("runden", 0)) * len(sitzung.get("teilnehmer", []))


def party_status(slug: str, sitzung: dict | None = None) -> str:
    """Status aus Registry und Dateien ableiten — es gibt kein State-File.

    "pausiert" ist auch der Zustand nach einem Serverneustart mitten in der
    Party; ein erneutes Start setzt dort fort, wo die jsonl aufhört.
    """
    sitzung = sitzung or sitzung_lesen(slug)
    if not sitzung:
        return "neu"

    with laeufe_lock:
        lauf = laeufe.get(slug)
    if lauf and not lauf.beendet:
        return "laeuft"

    anzahl = len(nur_beitraege(verlauf_lesen(slug)))
    if anzahl >= party_erwartet(sitzung):
        return "fertig"
    if lauf and lauf.fehler:
        return "fehler"
    if anzahl == 0:
        return "neu"
    return "pausiert"


def party_liste() -> list[dict]:
    if not os.path.isdir(PARTYS_DIR):
        return []
    partys = []
    for slug in sorted(os.listdir(PARTYS_DIR)):
        if not SAFE_SEGMENT_RE.match(slug):
            continue
        sitzung = sitzung_lesen(slug)
        if not sitzung:
            continue
        partys.append({
            "slug": slug,
            "sitzung": sitzung,
            "status": party_status(slug, sitzung),
            "beitraege": len(nur_beitraege(verlauf_lesen(slug))),
            "erwartet": party_erwartet(sitzung),
        })
    partys.sort(key=lambda p: p["sitzung"].get("erstellt", ""), reverse=True)
    return partys


def party_loeschen(slug: str) -> bool:
    ordner = sicherer_pfad(slug, PARTYS_DIR)
    if not ordner or not os.path.isdir(ordner):
        return False
    with laeufe_lock:
        lauf = laeufe.get(slug)
    stoppe_party(slug)
    # Erst wenn die Schleife durch ist, darf das Verzeichnis weg: sonst
    # schreibt der Thread gleich noch einen fertigen Beitrag in eine Datei,
    # deren Ordner es nicht mehr gibt, und stirbt mit Traceback.
    frist = time.monotonic() + 5
    while lauf and not lauf.beendet and time.monotonic() < frist:
        time.sleep(0.05)
    with laeufe_lock:
        laeufe.pop(slug, None)
    shutil.rmtree(ordner, ignore_errors=True)
    return True


# ============================================================================
# Die Party-Schleife
# ============================================================================

class Lauf:
    """Der Zustand einer laufenden Party.

    `ereignisse` hat genau einen Schreiber (den Schleifen-Thread) und viele
    Leser (die SSE-Verbindungen). Anhängen und Indexzugriff sind unter dem
    GIL atomar — deshalb braucht die Liste kein Lock. Nicht „aufräumen".
    """

    def __init__(self, slug: str, sitzung: dict) -> None:
        self.slug = slug
        self.sitzung = sitzung
        self.ereignisse: list[dict] = []
        self.beendet = False
        self.fehler: str | None = None
        self.abbruch = threading.Event()
        self.prozess: subprocess.Popen | None = None
        # Schützt abbruch und prozess *gemeinsam*. Ohne diese Klammer
        # entsteht bei einem Stop während des Prozessstarts ein Waisen-pi,
        # der im Hintergrund weiterredet.
        self.prozess_lock = threading.Lock()
        # Zwischenrufe, die noch in die Datei müssen. Sie kommen aus einem
        # Request-Thread, geschrieben werden sie vom Schleifen-Thread —
        # siehe schreibe_einwuerfe().
        self.einwuerfe: list[dict] = []
        self.einwurf_lock = threading.Lock()


laeufe: dict[str, Lauf] = {}
laeufe_lock = threading.Lock()


def sende(lauf: Lauf, ereignis: dict, eintrag_nr: int) -> None:
    """Ein Ereignis in den Puffer — mit der Marke, die es einordnet.

    `eintrag_nr` ist die Zahl der Zeilen, die zum Zeitpunkt des Ereignisses
    in verlauf.jsonl standen. Der Stream filtert daran ab, was eine neu
    verbundene Verbindung schon aus der Datei bekommen hat (siehe
    _party_stream). Beiträge, Zwischenrufe und Fazit zählen dafür gemeinsam.
    """
    lauf.ereignisse.append({"eintrag_nr": eintrag_nr, **ereignis})


def starte_party(slug: str) -> tuple[dict, int]:
    sitzung = sitzung_lesen(slug)
    if not sitzung:
        return {"fehler": "Party nicht gefunden"}, 404

    profile = []
    for teilnehmer in sitzung.get("teilnehmer", []):
        profil = profil_lesen(teilnehmer)
        if not profil:
            return {"fehler": f"Das Profil „{teilnehmer}“ gibt es nicht mehr."}, 409
        profile.append(profil)

    if len(nur_beitraege(verlauf_lesen(slug))) >= party_erwartet(sitzung):
        return {"fehler": "Diese Party ist schon durch. „Weitere Runde“ "
                          "hängt eine an."}, 409

    # Prüfen und Eintragen in einem Zug: ein Doppelklick auf „Start" darf
    # nicht zwei Threads erzeugen, die in dieselbe jsonl schreiben.
    with laeufe_lock:
        vorhanden = laeufe.get(slug)
        if vorhanden and not vorhanden.beendet:
            return {"fehler": "Diese Party läuft bereits."}, 409
        lauf = Lauf(slug, sitzung)
        laeufe[slug] = lauf

    threading.Thread(target=_party_schleife, args=(lauf, profile),
                     daemon=True).start()
    return {"status": "gestartet",
            "ab_beitrag": len(nur_beitraege(verlauf_lesen(slug)))}, 200


def schreibe_einwuerfe(lauf: Lauf) -> None:
    """Wartende Zwischenrufe an die Datei anhängen.

    Das tut nur der Schleifen-Thread, und nur zwischen zwei Beiträgen. Täte
    es der Request-Thread sofort, stünde der Zwischenruf in der Datei vor
    einer Blase, deren Ereignisse schon die Marke davor tragen — eine
    Verbindung, die genau dann neu aufmacht, bekäme den laufenden Beitrag
    weggefiltert. Sichtbar ist der Einwurf trotzdem sofort: wirf_ein() legt
    ihn zusätzlich in den Ereignispuffer.
    """
    with lauf.einwurf_lock:
        offen, lauf.einwuerfe = lauf.einwuerfe, []
    for eintrag in offen:
        verlauf_anhaengen(lauf.slug, eintrag)


def _pi_durchlauf(lauf: Lauf, marke: int, system_prompt: str, prompt: str,
                  modell: str, thinking: str) -> tuple[str, str, float] | None:
    """Ein pi-Prozess von vorn bis hinten: Ereignisse raus, Ergebnis zurück.

    Liefert (Text, Denken, Dauer) — oder None, wenn abgebrochen wurde oder
    etwas schiefging; die Meldung dafür ist dann schon im Puffer. Beitrag und
    Fazit teilen sich diesen Weg, damit es die Abbruchbehandlung nur einmal
    gibt.
    """
    begonnen = time.monotonic()

    with lauf.prozess_lock:
        if lauf.abbruch.is_set():
            return None
        try:
            lauf.prozess = starte_pi(baue_pi_befehl(
                system_prompt, prompt, modell, thinking))
        except FileNotFoundError:
            lauf.fehler = ("pi wurde nicht gefunden. Installieren mit: "
                           "npm install -g @earendil-works/pi-coding-agent")
            sende(lauf, {"art": "fehler", "text": lauf.fehler}, marke)
            return None

    prozess = lauf.prozess
    strom = PiStrom()
    try:
        for zeile in prozess.stdout:
            if lauf.abbruch.is_set():
                break
            try:
                ereignis = strom.verarbeite(zeile)
            except Exception as fehler:
                # Nie den Leser sterben lassen — sonst läuft pi auf eine
                # volle Pipe und hängt.
                print(f"[party-warn] {lauf.slug}: {fehler!r}", file=sys.stderr)
                continue
            if ereignis:
                sende(lauf, ereignis, marke)
    except (OSError, ValueError):
        pass

    rc = prozess.wait()
    with lauf.prozess_lock:
        lauf.prozess = None

    if lauf.abbruch.is_set():
        # Ein halber Satz im Verlauf würde alle Folgeprompts vergiften — der
        # Teilbeitrag wird verworfen. Das muss auch ankommen: der
        # Ereignispuffer wird nie gekürzt (sonst verlieren die mitlesenden
        # SSE-Verbindungen ihren Index), die angefangene Blase bleibt also
        # stehen. Ohne diese Kennzeichnung sähe sie beim Neuladen aus wie ein
        # fertiger Beitrag, den es im Verlauf gar nicht gibt.
        sende(lauf, {"art": "verworfen",
                     "text": "Abgebrochen — dieser Beitrag zählt "
                             "nicht und steht nicht im Verlauf."}, marke)
        return None

    if rc != 0 or strom.fehler or not strom.voller_text:
        lauf.fehler = strom.fehler or f"pi endete mit Code {rc}"
        sende(lauf, {"art": "fehler", "text": lauf.fehler}, marke)
        return None

    return (strom.voller_text, strom.volles_denken,
            round(time.monotonic() - begonnen, 1))


def _party_schleife(lauf: Lauf, profile: list[dict]) -> None:
    """Reihum, ein pi-Prozess je Beitrag.

    Sequenziell und nicht parallel: die Profile sollen aufeinander antworten
    können, und im Hörsaal ist das Nacheinander der Punkt.
    """
    slug = lauf.slug
    sitzung = lauf.sitzung
    teilnehmer = sitzung.get("teilnehmer", [])
    nach_slug = {p["slug"]: p for p in profile}
    gesamt = party_erwartet(sitzung)

    try:
        while not lauf.abbruch.is_set():
            # Vor jedem Beitrag frisch von der Platte: seit dem letzten kann
            # ein Zwischenruf dazugekommen sein, und der gehört in den Prompt.
            schreibe_einwuerfe(lauf)
            eintraege = verlauf_lesen(slug)
            nr = len(nur_beitraege(eintraege))
            if nr >= gesamt:
                break

            # Die Marke ist die Dateilänge, nicht die Beitragszahl: sonst
            # zählten Stream und Datei verschieden, sobald ein Zwischenruf
            # dazwischenliegt.
            marke = len(eintraege)
            runde, platz = divmod(nr, len(teilnehmer))
            profil = nach_slug[teilnehmer[platz]]

            sende(lauf, {
                "art": "beitrag_start",
                "sorte": "beitrag",
                "runde": runde + 1,
                "profil": profil["slug"],
                "name": profil["name"],
                "farbe": profil["farbe"],
            }, marke)

            ergebnis = _pi_durchlauf(
                lauf, marke, profil["text"],
                baue_beitrag_prompt(sitzung, profile, platz, runde + 1, eintraege),
                sitzung.get("modell") or profil.get("model", ""),
                profil["thinking"])
            if ergebnis is None:
                break

            text, denken, dauer = ergebnis
            eintrag = {
                "art": "beitrag",
                "runde": runde + 1,
                "profil": profil["slug"],
                "text": text,
                "denken": denken,
                "zeit": jetzt_iso(),
                "dauer_s": dauer,
            }
            # Erst schreiben, dann melden: ein Browser, der genau dazwischen
            # neu verbindet, bekommt den Beitrag aus der Datei statt gar nicht.
            verlauf_anhaengen(slug, eintrag)
            sende(lauf, {
                "art": "beitrag_ende",
                "sorte": "beitrag",
                "runde": eintrag["runde"],
                "profil": eintrag["profil"],
                "dauer_s": eintrag["dauer_s"],
            }, marke)
    finally:
        # Was noch in der Warteschlange liegt, gehört trotzdem in die Datei —
        # sonst wäre der Zwischenruf weg, den jemand Sekunden vor dem Stopp
        # eingeworfen hat.
        schreibe_einwuerfe(lauf)
        lauf.beendet = True


def _fazit_schleife(lauf: Lauf, profile: list[dict]) -> None:
    """Ein einziger Durchlauf: die Gesprächsleitung zieht Bilanz.

    Läuft über dieselbe Registry wie eine Party — solange das Fazit
    entsteht, ist die Sitzung belegt und niemand startet ihr eine Runde
    dazwischen.
    """
    slug = lauf.slug
    sitzung = lauf.sitzung
    try:
        eintraege = verlauf_lesen(slug)
        marke = len(eintraege)
        runde = int(sitzung.get("runden", 1))

        sende(lauf, {
            "art": "beitrag_start",
            "sorte": "fazit",
            "runde": runde,
            "profil": "fazit",
            "name": LEITUNG,
            "farbe": "grau",
        }, marke)

        ergebnis = _pi_durchlauf(
            lauf, marke, SYSTEMPROMPT_FAZIT,
            baue_fazit_prompt(sitzung, profile, eintraege),
            sitzung.get("modell", ""), "low")
        if ergebnis is None:
            return

        text, denken, dauer = ergebnis
        eintrag = {
            "art": "fazit",
            "runde": runde,
            "profil": "fazit",
            "text": text,
            "denken": denken,
            "zeit": jetzt_iso(),
            "dauer_s": dauer,
        }
        verlauf_anhaengen(slug, eintrag)
        sende(lauf, {
            "art": "beitrag_ende",
            "sorte": "fazit",
            "runde": runde,
            "profil": "fazit",
            "dauer_s": dauer,
        }, marke)
    finally:
        schreibe_einwuerfe(lauf)
        lauf.beendet = True


def starte_fazit(slug: str) -> tuple[dict, int]:
    sitzung = sitzung_lesen(slug)
    if not sitzung:
        return {"fehler": "Party nicht gefunden"}, 404

    eintraege = verlauf_lesen(slug)
    if not nur_beitraege(eintraege):
        return {"fehler": "Noch hat niemand gesprochen."}, 409

    # Die Profile nur für die Namen im Prompt — ein gelöschtes Profil darf
    # das Fazit nicht verhindern, der Verlauf steht ja schon.
    profile = [profil_lesen(t) or {"slug": t, "name": t, "beschreibung": ""}
               for t in sitzung.get("teilnehmer", [])]

    with laeufe_lock:
        vorhanden = laeufe.get(slug)
        if vorhanden and not vorhanden.beendet:
            return {"fehler": "Erst muss die Runde durch sein."}, 409
        lauf = Lauf(slug, sitzung)
        laeufe[slug] = lauf

    threading.Thread(target=_fazit_schleife, args=(lauf, profile),
                     daemon=True).start()
    return {"status": "gestartet"}, 200


def wirf_ein(slug: str, text: str) -> tuple[dict, int]:
    """Einen Zwischenruf der Gesprächsleitung in die Sitzung geben.

    Er wirkt auf den nächsten Beitrag: die Schleife liest den Verlauf vor
    jedem Durchlauf neu, und baue_beitrag_prompt() hebt hervor, worauf noch
    niemand geantwortet hat.
    """
    sitzung = sitzung_lesen(slug)
    if not sitzung:
        return {"fehler": "Party nicht gefunden"}, 404

    text = " ".join(str(text).split())
    if not text:
        return {"fehler": "Der Zwischenruf ist leer."}, 400
    text = text[:ZWISCHENRUF_ZEICHEN]

    eintraege = verlauf_lesen(slug)
    plaetze = len(sitzung.get("teilnehmer", [])) or 1
    eintrag = {
        "art": "zwischenruf",
        "runde": len(nur_beitraege(eintraege)) // plaetze + 1,
        "text": text,
        "zeit": jetzt_iso(),
    }

    with laeufe_lock:
        lauf = laeufe.get(slug)

    if lauf and not lauf.beendet:
        with lauf.einwurf_lock:
            lauf.einwuerfe.append(eintrag)
        sende(lauf, {"art": "zwischenruf", "runde": eintrag["runde"],
                     "text": text}, len(eintraege))
        return {"status": "eingeworfen", "live": True, "eintrag": eintrag}, 200

    # Läuft gerade nichts, schreibt der Request-Thread selbst — es gibt
    # keinen Beitrag, dessen Marke dabei kaputtgehen könnte.
    verlauf_anhaengen(slug, eintrag)
    return {"status": "eingeworfen", "live": False, "eintrag": eintrag}, 200


def naechste_runde(slug: str) -> tuple[dict, int]:
    """Eine Runde anhängen und gleich loslaufen.

    MAX_RUNDEN deckelt das Einrichten, nicht das Nachlegen: wie oft die
    Gesprächsleitung im Hörsaal verlängert, entscheidet der Verlauf des
    Gesprächs und nicht das Formular.
    """
    sitzung = sitzung_lesen(slug)
    if not sitzung:
        return {"fehler": "Party nicht gefunden"}, 404

    with laeufe_lock:
        lauf = laeufe.get(slug)
    if lauf and not lauf.beendet:
        return {"fehler": "Diese Party läuft bereits."}, 409

    vorher = int(sitzung.get("runden", 1))
    sitzung["runden"] = vorher + 1
    sitzung_schreiben(slug, sitzung)

    antwort, status = starte_party(slug)
    if status != 200:
        # Der Start ist gescheitert — etwa weil ein Profil fehlt. Dann darf
        # die Runde auch nicht in der Datei stehen bleiben, sonst gilt die
        # Sitzung als unfertig und lässt sich nur noch fortsetzen.
        sitzung["runden"] = vorher
        sitzung_schreiben(slug, sitzung)
        return antwort, status

    antwort["runden"] = sitzung["runden"]
    return antwort, status


def stoppe_party(slug: str) -> bool:
    with laeufe_lock:
        lauf = laeufe.get(slug)
    if not lauf or lauf.beendet:
        return False

    with lauf.prozess_lock:
        lauf.abbruch.set()
        prozess = lauf.prozess

    # Drei Phasen, keine davon unter einem Lock: terminate, warten, kill.
    if prozess and prozess.poll() is None:
        prozess.terminate()
        try:
            prozess.wait(timeout=3)
        except subprocess.TimeoutExpired:
            prozess.kill()
            try:
                prozess.wait(timeout=1)
            except subprocess.TimeoutExpired:
                pass
    return True


def beende_alle() -> None:
    with laeufe_lock:
        slugs = list(laeufe.keys())
    for slug in slugs:
        stoppe_party(slug)


# ============================================================================
# HTTP
# ============================================================================

class QuietThreadingHTTPServer(ThreadingHTTPServer):
    """Abgebrochene SSE-Verbindungen sind normal — keine Tracebacks dafür."""

    def handle_error(self, request, client_address):
        fehler = sys.exc_info()[1]
        if isinstance(fehler, (ConnectionResetError, BrokenPipeError,
                               ConnectionAbortedError)):
            return
        super().handle_error(request, client_address)


MIME_TYPEN = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


class PartyHandler(SimpleHTTPRequestHandler):

    # ---------------------------------------------------------------- Routing

    def do_HEAD(self):
        # Nicht erben: die Variante von SimpleHTTPRequestHandler bedient sich
        # am Arbeitsverzeichnis und ginge damit an _serve_static() vorbei —
        # HEAD /server.py hätte Größe und Datum des Quelltexts verraten.
        self._serve_static(urlparse(self.path).path, nur_kopf=True)

    def do_GET(self):
        pfad = urlparse(self.path).path
        teile = pfad.split("/")

        if pfad == "/api/profile":
            self._send_json(profil_liste())
        elif pfad == "/api/modelle":
            self._send_json(modelle_lesen())
        elif pfad == "/api/partys":
            self._send_json(party_liste())
        elif pfad.startswith("/api/partys/") and pfad.endswith("/stream"):
            self._party_stream(teile[3])
        elif len(teile) == 4 and pfad.startswith("/api/partys/"):
            self._party_lesen(teile[3])
        else:
            self._serve_static(pfad)

    def do_POST(self):
        pfad = urlparse(self.path).path
        teile = pfad.split("/")

        if pfad == "/api/profile":
            self._profil_anlegen()
        elif pfad == "/api/profile/entwurf":
            self._profil_entwurf()
        elif pfad == "/api/partys":
            self._party_anlegen()
        elif pfad.startswith("/api/partys/") and pfad.endswith("/start"):
            self._party_start(teile[3])
        elif pfad.startswith("/api/partys/") and pfad.endswith("/stop"):
            self._party_stop(teile[3])
        elif pfad.startswith("/api/partys/") and pfad.endswith("/zwischenruf"):
            self._party_zwischenruf(teile[3])
        elif pfad.startswith("/api/partys/") and pfad.endswith("/runde"):
            self._party_runde(teile[3])
        elif pfad.startswith("/api/partys/") and pfad.endswith("/fazit"):
            self._party_fazit(teile[3])
        else:
            self.send_error(404)

    def do_PUT(self):
        pfad = urlparse(self.path).path
        teile = pfad.split("/")
        if len(teile) == 4 and pfad.startswith("/api/profile/"):
            self._profil_aendern(teile[3])
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        teile = parsed.path.split("/")
        if len(teile) == 4 and parsed.path.startswith("/api/profile/"):
            self._profil_loeschen(teile[3], "force=1" in (parsed.query or ""))
        elif len(teile) == 4 and parsed.path.startswith("/api/partys/"):
            self._party_loeschen(teile[3])
        else:
            self.send_error(404)

    # ---------------------------------------------------------------- Profile

    def _profil_anlegen(self):
        daten = self._read_body()
        if daten is None:
            return
        gepruft, fehler = profil_pruefen(daten)
        if fehler:
            self._send_json({"fehler": fehler}, 400)
            return
        slug = slugify(gepruft["name"])
        vorhanden = profil_pfad(slug)
        if vorhanden and os.path.isfile(vorhanden):
            self._send_json({"fehler": "Ein Profil mit diesem Namen gibt es schon."}, 409)
            return
        if not profil_schreiben(slug, gepruft):
            self._send_json({"fehler": "Ungültiger Name"}, 400)
            return
        self._send_json(profil_lesen(slug), 201)

    def _profil_aendern(self, slug):
        if not profil_lesen(slug):
            self._send_json({"fehler": "Profil nicht gefunden"}, 404)
            return
        daten = self._read_body()
        if daten is None:
            return
        gepruft, fehler = profil_pruefen(daten)
        if fehler:
            self._send_json({"fehler": fehler}, 400)
            return
        profil_schreiben(slug, gepruft)
        self._send_json(profil_lesen(slug))

    def _profil_loeschen(self, slug, erzwingen):
        if not profil_lesen(slug):
            self._send_json({"fehler": "Profil nicht gefunden"}, 404)
            return
        betroffen = profil_in_offener_party(slug)
        if betroffen and not erzwingen:
            self._send_json({
                "fehler": "Dieses Profil wird noch gebraucht.",
                "partys": betroffen,
            }, 409)
            return
        profil_loeschen(slug)
        self._send_json({"status": "geloescht"})

    def _profil_entwurf(self):
        """Profil vom Sprachmodell ausarbeiten lassen — als SSE.

        Kein Slug, kein Langzeitzustand: die Lebensdauer des pi-Prozesses ist
        exakt die des Requests. Bricht der Browser ab, fliegt das nächste
        Schreiben auf die Nase und der finally-Block räumt pi weg. Deshalb
        braucht dieser Endpunkt keinen eigenen Stop.
        """
        daten = self._read_body()
        if daten is None:
            return
        idee = str(daten.get("idee", "")).strip()
        if not idee:
            self._send_json({"fehler": "Bitte beschreibe die Rolle in einem Satz."}, 400)
            return

        try:
            prozess = starte_pi(baue_pi_befehl(
                systemprompt_entwurf(), f"Stichwortidee: {idee}",
                STANDARD_MODELL, "low"))
        except FileNotFoundError:
            self._send_json({"fehler": "pi wurde nicht gefunden."}, 500)
            return

        self._sse_kopf()
        try:
            strom = PiStrom()
            for zeile in prozess.stdout:
                try:
                    ereignis = strom.verarbeite(zeile)
                except Exception:
                    continue
                if ereignis:
                    self._sse_ereignis(ereignis)
            self._sse_ende("fertig")
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            if prozess.poll() is None:
                prozess.terminate()
                try:
                    prozess.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    prozess.kill()

    # ---------------------------------------------------------------- Partys

    def _party_anlegen(self):
        daten = self._read_body()
        if daten is None:
            return

        titel = " ".join(str(daten.get("titel", "")).split())
        starter = str(daten.get("starter", "")).strip()
        teilnehmer = [str(t) for t in daten.get("teilnehmer", [])]
        try:
            runden = int(daten.get("runden", 2))
        except (TypeError, ValueError):
            runden = 2

        if not titel:
            self._send_json({"fehler": "Die Party braucht ein Thema."}, 400)
            return
        if not starter:
            self._send_json({"fehler": "Die Party braucht eine Einstiegsfrage."}, 400)
            return
        if not MIN_TEILNEHMER <= len(teilnehmer) <= MAX_TEILNEHMER:
            self._send_json({
                "fehler": f"Es müssen {MIN_TEILNEHMER} bis {MAX_TEILNEHMER} "
                          "Profile am Tisch sitzen."}, 400)
            return
        for slug in teilnehmer:
            if not profil_lesen(slug):
                self._send_json({"fehler": f"Das Profil „{slug}“ gibt es nicht."}, 400)
                return
        # Der Name ist die Identität des Agenten — im Teilnehmerblock, im
        # Verlauf und in der Anweisung, die Person beim Namen zu nennen.
        # Zweimal dasselbe Profil hieße zweimal derselbe Name.
        if len(set(teilnehmer)) != len(teilnehmer):
            self._send_json({
                "fehler": "Jedes Profil sitzt nur einmal am Tisch. Für zwei "
                          "ähnliche Stimmen im Profil-Editor „Duplizieren“ "
                          "und der Kopie einen eigenen Namen geben."}, 400)
            return
        runden = max(1, min(MAX_RUNDEN, runden))

        slug = slugify(titel)
        basis, zaehler = slug, 2
        while os.path.isdir(os.path.join(PARTYS_DIR, slug)):
            slug = f"{basis}-{zaehler}"
            zaehler += 1

        sitzung = {
            "titel": titel,
            "starter": starter,
            "teilnehmer": teilnehmer,
            "runden": runden,
            # Leer heißt: das Modell aus dem jeweiligen Profil, sonst der
            # Serverstandard. Hier STANDARD_MODELL einzusetzen würde das Feld
            # in der Profildatei stillschweigend entwerten.
            "modell": str(daten.get("modell", "")).strip(),
            "erstellt": jetzt_iso(),
        }
        if not sitzung_schreiben(slug, sitzung):
            self._send_json({"fehler": "Ungültiges Thema"}, 400)
            return
        self._send_json({"slug": slug, "sitzung": sitzung}, 201)

    def _party_lesen(self, slug):
        sitzung = sitzung_lesen(slug)
        if not sitzung:
            self._send_json({"fehler": "Party nicht gefunden"}, 404)
            return
        # Bewusst ohne Verlauf: der kommt ausschließlich über den Stream,
        # damit das Frontend die Sprechblasen nur an einer Stelle baut.
        self._send_json({
            "slug": slug,
            "sitzung": sitzung,
            "status": party_status(slug, sitzung),
            "beitraege": len(nur_beitraege(verlauf_lesen(slug))),
            "erwartet": party_erwartet(sitzung),
        })

    def _party_start(self, slug):
        antwort, status = starte_party(slug)
        self._send_json(antwort, status)

    def _party_stop(self, slug):
        if not sitzung_lesen(slug):
            self._send_json({"fehler": "Party nicht gefunden"}, 404)
            return
        gestoppt = stoppe_party(slug)
        self._send_json({"status": "gestoppt" if gestoppt else "lief nicht"})

    def _party_zwischenruf(self, slug):
        daten = self._read_body()
        if daten is None:
            return
        antwort, status = wirf_ein(slug, daten.get("text", ""))
        self._send_json(antwort, status)

    def _party_runde(self, slug):
        antwort, status = naechste_runde(slug)
        self._send_json(antwort, status)

    def _party_fazit(self, slug):
        antwort, status = starte_fazit(slug)
        self._send_json(antwort, status)

    def _party_loeschen(self, slug):
        if not party_loeschen(slug):
            self._send_json({"fehler": "Party nicht gefunden"}, 404)
            return
        self._send_json({"status": "geloescht"})

    def _party_stream(self, slug):
        """Beiträge live — und den bisherigen Verlauf gleich mit.

        Reihenfolge ist Teil des Vertrags: erst die Datei lesen (ergibt n),
        dann nachliefern, dann erst die Registry. Der laufende Beitrag hat
        eintrag_nr == n und liegt vollständig im Ereignispuffer; alles
        darunter steht in der Datei. So gibt es weder Lücke noch Dopplung —
        ganz ohne Lock, weil die Ereignisliste nur wächst.

        `n` zählt Zeilen, nicht Beiträge: Zwischenrufe und Fazit stehen in
        derselben Datei und verschieben die Marke mit.
        """
        if not sitzung_lesen(slug):
            self._send_json({"fehler": "Party nicht gefunden"}, 404)
            return

        self._sse_kopf()
        try:
            eintraege = verlauf_lesen(slug)
            n = len(eintraege)
            profile = {p["slug"]: p for p in profil_liste()}

            for eintrag in eintraege:
                art = eintrag.get("art", "beitrag")
                if art == "zwischenruf":
                    self._sse_ereignis({
                        "art": "zwischenruf",
                        "runde": eintrag.get("runde", 1),
                        "text": eintrag.get("text", ""),
                        "nachgeliefert": True,
                    })
                    continue

                slug_profil = eintrag.get("profil", "")
                profil = profile.get(slug_profil, {})
                self._sse_ereignis({
                    "art": "beitrag_start",
                    "sorte": art,
                    "runde": eintrag.get("runde", 1),
                    "profil": slug_profil,
                    "name": LEITUNG if art == "fazit"
                            else profil.get("name", slug_profil),
                    "farbe": profil.get("farbe", "grau"),
                    "nachgeliefert": True,
                })
                if eintrag.get("denken"):
                    self._sse_ereignis({"art": "denken", "delta": eintrag["denken"]})
                self._sse_ereignis({"art": "text", "delta": eintrag.get("text", "")})
                self._sse_ereignis({
                    "art": "beitrag_ende",
                    "sorte": art,
                    "runde": eintrag.get("runde", 1),
                    "profil": slug_profil,
                    "dauer_s": eintrag.get("dauer_s", 0),
                })

            with laeufe_lock:
                lauf = laeufe.get(slug)

            if not lauf or (lauf.beendet and len(lauf.ereignisse) == 0):
                self._sse_ende(party_status(slug))
                return

            index = 0
            letzter_ping = time.monotonic()
            while True:
                ereignisse = lauf.ereignisse
                while index < len(ereignisse):
                    ereignis = ereignisse[index]
                    index += 1
                    if ereignis.get("eintrag_nr", 0) < n:
                        continue
                    self._sse_ereignis(
                        {k: v for k, v in ereignis.items() if k != "eintrag_nr"})
                    letzter_ping = time.monotonic()

                if lauf.beendet and index >= len(lauf.ereignisse):
                    self._sse_ende(party_status(slug))
                    return

                # Zwischen zwei Beiträgen kann es lange still sein — ein Ping
                # hält die Verbindung wach.
                if time.monotonic() - letzter_ping > 15:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    letzter_ping = time.monotonic()

                time.sleep(0.15)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    # ---------------------------------------------------------------- Helfer

    def _sse_kopf(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

    def _sse_ereignis(self, ereignis: dict):
        nutzlast = json.dumps(ereignis, ensure_ascii=False)
        self.wfile.write(f"data: {nutzlast}\n\n".encode("utf-8"))
        self.wfile.flush()

    def _sse_ende(self, status: str):
        self.wfile.write(f"event: done\ndata: {status}\n\n".encode("utf-8"))
        self.wfile.flush()

    def _read_body(self):
        try:
            laenge = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            laenge = 0
        if laenge == 0:
            self._send_json({"fehler": "Leere Anfrage"}, 400)
            return None
        try:
            return json.loads(self.rfile.read(laenge))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json({"fehler": "Ungültiges JSON"}, 400)
            return None

    def _send_json(self, daten, status=200):
        rumpf = json.dumps(daten, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(rumpf)))
        self.end_headers()
        self.wfile.write(rumpf)

    def _serve_static(self, pfad, nur_kopf=False):
        if pfad in ("/", ""):
            pfad = "/index.html"
        datei = os.path.realpath(os.path.join(DASHBOARD_DIR, pfad.lstrip("/")))
        # Auch statische Dateien bekommen die realpath-Prüfung: sonst holt
        # `/../server.py` den Quelltext aus dem Projektverzeichnis.
        if not datei.startswith(os.path.realpath(DASHBOARD_DIR) + os.sep):
            self.send_error(404)
            return
        if not os.path.isfile(datei):
            self.send_error(404)
            return
        endung = os.path.splitext(datei)[1]
        with open(datei, "rb") as f:
            inhalt = f.read()
        self.send_response(200)
        self.send_header("Content-Type",
                         MIME_TYPEN.get(endung, "application/octet-stream"))
        self.send_header("Content-Length", str(len(inhalt)))
        self.end_headers()
        if not nur_kopf:
            self.wfile.write(inhalt)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}", file=sys.stderr)


def main():
    os.makedirs(PROFIL_DIR, exist_ok=True)
    os.makedirs(PARTYS_DIR, exist_ok=True)

    server = QuietThreadingHTTPServer(("", PORT), PartyHandler)
    print(f"Agent Party → http://localhost:{PORT}")
    if not shutil.which("pi"):
        print("  Achtung: pi wurde nicht gefunden — das Dashboard startet, "
              "aber keine Party läuft.", file=sys.stderr)

    def herunterfahren(sig, frame):
        print("\nServer wird beendet...")
        beende_alle()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGINT, herunterfahren)
    signal.signal(signal.SIGTERM, herunterfahren)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
