#!/usr/bin/env python3
"""dashboard.py — Die Übersicht für den Beamer.

Läuft neben der Demo und zeigt, was in den fünf Panes untergeht: welche Zahl
schon bei wem angekommen ist, wie weit jeder Sammler zurückliegt, welche
Befehle die Steuerung geschickt hat. Große Schrift, ruhige Übergänge, ein
Fenster, das sich auf den Beamer legen lässt, ohne dass Herdr im Weg ist.
Farben und Gestaltung nach dem THM-Corporate-Design, in derselben Ausprägung
wie die anderen Dashboards des Repos: dunkle Kopfleiste mit Bildmarke,
Abschnittstitel mit grüner Unterkante, Karten mit farbiger Kante links. Dunkel
ist voreingestellt; ein Umschalter im Kopf wechselt auf die helle
Standardanwendung, die Wahl merkt sich der Browser. Die Schrift Barlow kommt
von Google Fonts — ohne Netz greift der Systemschrift-Stack, die Seite
funktioniert unverändert.

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
import urllib.parse
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
<!-- Bildmarke StudiumPlus als Favicon, inline: Kreuz aus fünf Quadraten, die
     Mitte in THM Grün. So kommt die Seite ohne Bilddatei aus. -->
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%231A252B'/%3E%3Crect x='13' y='4'  width='6' height='6' fill='%237C8D96'/%3E%3Crect x='4'  y='13' width='6' height='6' fill='%237C8D96'/%3E%3Crect x='13' y='13' width='6' height='6' fill='%2380BA24'/%3E%3Crect x='22' y='13' width='6' height='6' fill='%237C8D96'/%3E%3Crect x='13' y='22' width='6' height='6' fill='%237C8D96'/%3E%3C/svg%3E">
<!-- Barlow und Barlow Condensed: der im THM-CD dokumentierte Ersatz für die
     lizenzpflichtige Hausschrift DIN Pro. Ohne Netz greift der
     Systemschrift-Stack in font-family — die Seite bleibt vollständig
     benutzbar, sie sieht nur anders aus. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<!-- Farbthema vor dem ersten Rendern setzen, damit nichts aufblitzt. Dunkel ist
     die Voreinstellung (Beamer); eine Wahl über den Umschalter bleibt gespeichert. -->
<script>
  (function () {
    var wahl = null;
    try { wahl = localStorage.getItem("counting-agents-theme"); } catch (e) {}
    document.documentElement.classList.toggle("dark", wahl !== "light");
  })();
</script>
<style>
  /* ============================================================
     Farben nach dem THM-Corporate-Design (CD-Manual, 3. Auflage), in
     derselben Ausprägung wie im Dashboard von agent-party: Flächen- und
     Schriftfarben stehen als leerzeichengetrennte RGB-Kanäle in Variablen,
     damit sich daraus mit rgb(var(--name) / alpha) auch Tönungen bilden
     lassen. Welches Thema gilt, entscheidet die Klasse "dark" am
     <html>-Element.

     Fläche und Schrift bleiben getrennt: THM Grün und THM Gelb sind in
     Reinform zu hell für kleinen Text auf hellem Grund. Sie bleiben
     Füllfarbe; für Text gibt es die abgedunkelten "-text"-Varianten.
     ============================================================ */
  :root {
    --base: 245 245 245;             /* #F5F5F5 – Seitengrund */
    --surface: 255 255 255;          /* #FFFFFF – Karten, Kacheln */
    --surface-mid: 235 235 235;      /* #EBEBEB – gedämpfte Fläche */
    --header: 26 37 43;              /* #1A252B – Kopfleiste und Kennzahlenblock */
    --on-header: 255 255 255;
    --on-header-variant: 168 180 188; /* #A8B4BC – gedämpfte Schrift auf dem Dunkel */
    --on-surface: 42 56 64;          /* THM Grau dunkel #2A3840 – Überschriften */
    --on-surface-variant: 74 92 102; /* THM Grau #4A5C66 – Fließtext */
    --accent: 128 186 36;            /* THM Grün #80BA24 – Ränder, Marke */
    --accent-text: 69 107 13;        /* #456B0D – Grün für Text */
    --error-color: 156 19 46;        /* THM Rot #9C132E – Text */

    /* Die Zusatzfarben des CD sind laut Manual für Infografiken gedacht —
       genau das ist das Zahlenband. Jeder Sammler bekommt eine davon, und sie
       gilt überall gleich: auf der Kachel, im Chip vor dem Namen, im Balken,
       in der Legende. THM Rot bleibt allein den Fehlern vorbehalten.
       Ohne Zusatz ist es die Füllfarbe, "-text" die Schrift darauf. */
    --counter: 74 92 102;   --counter-text: 74 92 102;  /* THM Grau */
    --odd: 0 184 228;       --odd-text: 0 112 140;      /* THM Hellblau */
    --even: 128 186 36;     --even-text: 69 107 13;     /* THM Grün */
    --prime: 244 170 0;     --prime-text: 132 90 0;     /* THM Gelb */
    --wrong: 156 19 46;     --wrong-text: 156 19 46;    /* THM Rot */

    --hover-schatten: 0 2px 6px rgba(34, 44, 49, .12);
    color-scheme: light;
  }

  /* Dunkel – aus den Negativ-Regeln des CD-Manuals abgeleitet. Grund #1A252B,
     Kartenfläche #212E35, Kopfleiste eine Stufe dunkler. */
  .dark {
    --base: 26 37 43;                /* #1A252B */
    --surface: 33 46 53;             /* #212E35 */
    --surface-mid: 46 62 70;         /* #2E3E46 */
    --header: 16 24 29;              /* #10181D */
    --on-surface: 232 236 240;       /* Offwhite #E8ECF0 */
    --on-surface-variant: 178 190 198; /* #B2BEC6 */
    --accent-text: 168 216 110;      /* #A8D86E */
    --error-color: 244 168 179;      /* #F4A8B3 */

    --counter: 124 141 150;  --counter-text: 178 190 198; /* #7C8D96 */
    --odd-text: 95 212 242;                               /* #5FD4F2 */
    --even-text: 168 216 110;                             /* #A8D86E */
    --prime-text: 255 192 61;                             /* #FFC03D */
    /* THM Rot, für dunklen Grund aufgehellt: in Reinform hebt es sich weder
       von der Kachelfüllung noch vom Grund ab, und der Fehlgriff des
       Prim-Agenten ist genau der Moment, der auf dem Beamer auffallen soll. */
    --wrong: 224 90 112;     --wrong-text: 244 168 179;   /* #E05A70 */

    --hover-schatten: 0 0 0 1px rgb(var(--on-surface) / .3);
    color-scheme: dark;
  }

  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; display: flex; flex-direction: column;
    background: rgb(var(--base)); color: rgb(var(--on-surface));
    font-family: 'Barlow', -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-variant-numeric: tabular-nums;
  }

  /* --- Kopfleiste: Marke links, Uhr und Umschalter rechts ----------------
     Sie ist in beiden Themen dunkel und führt in den Kennzahlenblock über —
     auf dem Beamer soll dort ein Titelbalken stehen, keine Werkzeugleiste. */
  .kopfleiste {
    display: flex; align-items: center; justify-content: space-between;
    gap: 16px; flex-wrap: wrap; flex-shrink: 0;
    padding: 10px clamp(16px, 2.5vw, 40px);
    background: rgb(var(--header)); color: rgb(var(--on-header));
  }
  .kopf-marke { display: flex; align-items: center; gap: 12px; }
  .kopf-logo { width: 30px; height: 30px; flex: none; }
  /* Die Kopfleiste ist immer dunkel: THM Grün bleibt unverändert, THM Grau
     wäre dort zu dunkel und ist auf #7C8D96 aufgehellt. */
  .logo-gruen { fill: #80BA24; }
  .logo-grau  { fill: #7C8D96; }
  .kopf-titel {
    margin: 0; font-family: 'Barlow Condensed', 'Barlow', sans-serif;
    font-size: clamp(20px, 2vw, 26px); font-weight: 700;
    letter-spacing: .06em; text-transform: uppercase; line-height: 1.1;
  }
  .kopf-unterzeile {
    margin: 0; font-size: 11px; letter-spacing: .14em; text-transform: uppercase;
    color: rgb(var(--on-header-variant));
  }
  .kopf-rechts { display: flex; align-items: center; gap: 12px; }
  #uhr { font-size: 13px; letter-spacing: .08em; color: rgb(var(--on-header-variant)); }
  /* Der Umschalter zeigt, wohin er schaltet: auf der dunklen Seite die Sonne,
     auf der hellen den Mond. Inline-SVG, damit die Seite ohne Icon-Font
     auskommt. */
  #thema {
    width: 32px; height: 32px; flex: none; border-radius: 9999px;
    display: flex; align-items: center; justify-content: center;
    color: rgb(var(--on-header)); background: rgb(var(--on-header) / .1);
    border: none; padding: 0; cursor: pointer;
    transition: background-color 140ms ease;
  }
  #thema:hover { background: rgb(var(--on-header) / .2); }
  #thema:focus-visible { outline: 2px solid rgb(var(--accent)); outline-offset: 2px; }
  #thema svg { width: 18px; height: 18px; display: block; }
  #thema .sonne { display: none; }
  .dark #thema .sonne { display: block; }
  .dark #thema .mond { display: none; }

  main { flex: 1; }
  .inhalt {
    max-width: 1320px; margin: 0 auto;
    padding: clamp(16px, 2vw, 28px) clamp(16px, 2.5vw, 40px) clamp(20px, 2.4vw, 34px);
  }

  /* --- Kennzahlenblock ---------------------------------------------------
     Dieselbe dunkle Fläche wie die Kopfleiste, mit dem Rasterbild rechts:
     reine Fläche, ein Verweis auf das Logo, kein Datenbild. */
  .kennzahlen {
    position: relative; overflow: hidden; border-radius: 6px;
    background: rgb(var(--header)); color: rgb(var(--on-header));
    margin-bottom: clamp(18px, 2.2vw, 30px);
  }
  .kennzahlen-raster {
    position: absolute; top: 0; right: 0; width: 280px; height: 100%;
    background-image:
      linear-gradient(rgb(var(--accent) / .55) 1px, transparent 1px),
      linear-gradient(90deg, rgb(var(--accent) / .55) 1px, transparent 1px);
    background-size: 14px 14px; opacity: .3;
    -webkit-mask-image: linear-gradient(90deg, transparent, #000 70%);
    mask-image: linear-gradient(90deg, transparent, #000 70%);
  }
  .kennzahlen-inhalt { position: relative; padding: clamp(16px, 2vw, 26px); }
  .kennzahlen-marke {
    margin: 0 0 8px; font-size: 11px; letter-spacing: .12em;
    text-transform: uppercase; color: rgb(var(--on-header-variant));
  }
  #summary {
    margin: 0; font-family: 'Barlow Condensed', 'Barlow', sans-serif;
    font-size: clamp(26px, 3.2vw, 46px); font-weight: 600; line-height: 1.15;
  }
  #takt {
    margin: 8px 0 0; font-size: clamp(13px, 1.2vw, 18px);
    color: rgb(var(--on-header-variant));
  }

  /* --- Abschnitte -------------------------------------------------------- */
  .abschnitt { margin-bottom: clamp(20px, 2.4vw, 34px); }
  /* Überschrift mit grüner Unterkante — dieselbe Marke wie in agent-party. */
  .abschnitt-titel {
    display: inline-block; margin: 0 0 14px;
    font-family: 'Barlow Condensed', 'Barlow', sans-serif;
    font-size: clamp(16px, 1.5vw, 20px); font-weight: 600;
    letter-spacing: .1em; text-transform: uppercase;
    padding-bottom: 4px; border-bottom: 2px solid rgb(var(--accent));
  }

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
    border-radius: 6px; text-align: center;
    font-size: clamp(15px, 1.6vw, 27px); font-weight: 600;
    background: rgb(var(--surface)); color: rgb(var(--on-surface-variant));
    border: 2px solid rgb(var(--on-surface) / .15);
    transition: background .5s ease, border-color .5s ease,
                color .5s ease, opacity .35s ease;
    animation: einblenden .45s ease both;
  }
  .tile.hat-odd  { border-color: rgb(var(--odd));  background: rgb(var(--odd) / .14);  color: rgb(var(--odd-text)); }
  .tile.hat-even { border-color: rgb(var(--even)); background: rgb(var(--even) / .14); color: rgb(var(--even-text)); }
  /* Zuletzt definiert, damit ein Rechenfehler jede andere Färbung übertönt. */
  .tile.wrong { border-color: rgb(var(--wrong)); background: rgb(var(--wrong) / .16); color: rgb(var(--wrong-text)); }

  .tile.soll-prime::after, .tile.hat-prime::after {
    content: ""; position: absolute; top: 5px; right: 6px;
    width: 9px; height: 9px; border-radius: 50%;
    border: 2px solid rgb(var(--prime)); background: transparent;
    transition: background .5s ease;
  }
  .tile.hat-prime::after { background: rgb(var(--prime)); }
  .tile.wrong::after { border-color: rgb(var(--wrong)); background: rgb(var(--wrong)); }

  @keyframes einblenden { from { opacity: 0; transform: translateY(-6px); } }

  /* Ein Agent ist angeklickt: nur seine Zahlen bleiben stehen. So lässt
     sich im Hörsaal einzeln zeigen, was jeder Sammler zu tun hat. */
  /* `:not(.hat-…)` sorgt dafür, dass eine falsch einsortierte Zahl im Fokus
     ihres Agenten stehen bleibt — sonst verschwände genau der Fehler. */
  .band[data-fokus="odd"]   .tile:not(.soll-odd):not(.hat-odd),
  .band[data-fokus="even"]  .tile:not(.soll-even):not(.hat-even),
  .band[data-fokus="prime"] .tile:not(.soll-prime):not(.hat-prime) { opacity: .1; }

  .legende { display: flex; gap: clamp(12px, 1.6vw, 26px); flex-wrap: wrap;
             align-items: center; color: rgb(var(--on-surface-variant));
             font-size: clamp(12px, 1vw, 16px); }
  .legende span { display: flex; align-items: center; gap: 7px; }
  .dot { width: 14px; height: 14px; border-radius: 4px;
         border: 2px solid rgb(var(--on-surface) / .15); background: rgb(var(--surface)); }
  .dot.odd   { border-color: rgb(var(--odd));   background: rgb(var(--odd) / .14); }
  .dot.even  { border-color: rgb(var(--even));  background: rgb(var(--even) / .14); }
  .dot.wrong { border-color: rgb(var(--wrong)); background: rgb(var(--wrong) / .16); }
  .ring { width: 11px; height: 11px; border-radius: 50%;
          border: 2px solid rgb(var(--prime)); background: transparent; }
  .ring.voll { background: rgb(var(--prime)); }
  .hinweis { margin-left: auto; opacity: .8; }

  /* --- Die Agenten ------------------------------------------------------
     Eine Zeile je Agent, gebaut wie die Profilkachel in agent-party: 4px
     Balken links in der Farbe des Agenten, Karte rechts daneben. */
  .agents { display: grid; gap: 10px; }
  .agent {
    display: grid; align-items: center; gap: clamp(10px, 1.4vw, 24px);
    grid-template-columns: minmax(170px, 1.2fr) auto minmax(90px, .6fr) minmax(90px, .6fr) minmax(120px, 1fr) auto;
    background: rgb(var(--surface));
    border: 1px solid rgb(var(--on-surface) / .1);
    border-left: 4px solid rgb(var(--on-surface) / .25);
    border-radius: 0 6px 6px 0;
    padding: clamp(9px, 1.1vw, 18px) clamp(12px, 1.4vw, 22px);
    font-size: clamp(14px, 1.3vw, 22px);
    transition: border-left-color .4s ease, box-shadow 140ms ease;
  }
  .agent.klickbar { cursor: pointer; }
  /* Der Hover-Schatten ist themenabhängig: ein dunkler Schlagschatten wäre auf
     dem dunklen Grund unsichtbar, dort tritt eine helle Kante an seine Stelle. */
  .agent.klickbar:hover { box-shadow: var(--hover-schatten); }
  /* Der Fokusring muss den Hover-Schatten übertönen — sonst verschwindet er,
     sobald die Maus auf der angeklickten Zeile stehen bleibt. */
  .agent.fokus,
  .agent.klickbar.fokus:hover { box-shadow: 0 0 0 2px rgb(var(--accent) / .55); }
  /* Der linke Balken trägt die Farbe des Agenten — dieselbe wie im Band.
     Der Betriebszustand kommt ohne eigene Farbe aus: durchgezogen läuft,
     gestrichelt pausiert, gepunktet gestoppt. Sonst müsste sich „pausiert"
     eine Farbe mit einem Sammler teilen, und das trifft im Vortrag immer
     ausgerechnet prime. */
  .agent.a-counter { border-left-color: rgb(var(--counter)); }
  .agent.a-odd     { border-left-color: rgb(var(--odd)); }
  .agent.a-even    { border-left-color: rgb(var(--even)); }
  .agent.a-prime   { border-left-color: rgb(var(--prime)); }
  .agent.paused  { border-left-style: dashed; }
  .agent.stopped { border-left-style: dotted; }
  .agent .name {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Barlow Condensed', 'Barlow', sans-serif;
    font-weight: 600; letter-spacing: .06em; text-transform: uppercase;
  }
  .agent .name small {
    display: block; font-family: 'Barlow', sans-serif; font-weight: 400;
    text-transform: none; letter-spacing: .02em; font-size: .62em;
    color: rgb(var(--on-surface-variant));
  }
  .chip { width: 14px; height: 14px; border-radius: 4px; flex: none;
          border: 2px solid rgb(var(--on-surface) / .15); background: rgb(var(--surface)); }
  .chip.odd   { border-color: rgb(var(--odd));   background: rgb(var(--odd) / .14); }
  .chip.even  { border-color: rgb(var(--even));  background: rgb(var(--even) / .14); }
  .chip.prime { border-color: rgb(var(--prime)); background: rgb(var(--prime)); border-radius: 50%; }
  .chip.counter { border-color: rgb(var(--counter)); background: transparent; }
  /* Hülle um alles außer dem Prompt-Knopf; ihre Kinder sitzen direkt im Raster. */
  .agent .teile { display: contents; }
  .agent .status { color: rgb(var(--on-surface-variant)); white-space: nowrap; }
  .agent.paused  .status { color: rgb(var(--on-surface)); }
  .agent.stopped .status { color: rgb(var(--error-color)); }
  .agent .zahl { color: rgb(var(--on-surface)); font-weight: 600; }
  /* Zurückliegen ist die Nachricht, Gleichstand der Normalfall. */
  .agent .lag.zurueck { color: rgb(var(--on-surface)); }
  .agent .lag.aktuell { color: rgb(var(--on-surface-variant)); }
  .balken { height: 10px; border-radius: 5px; background: rgb(var(--on-surface) / .12); overflow: hidden; }
  .balken i { display: block; height: 100%; background: rgb(var(--on-surface-variant));
              transition: width .5s ease; }
  .a-odd   .balken i { background: rgb(var(--odd)); }
  .a-even  .balken i { background: rgb(var(--even)); }
  .a-prime .balken i { background: rgb(var(--prime)); }
  .still { color: rgb(var(--error-color)); font-size: .8em; }

  /* --- Steuerung --------------------------------------------------------- */
  .karte {
    background: rgb(var(--surface));
    border: 1px solid rgb(var(--on-surface) / .1);
    border-radius: 6px; padding: clamp(12px, 1.4vw, 18px);
  }
  .karte .abschnitt-titel { margin-bottom: 10px; }
  .karte-kopf { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
  #ticker { list-style: none; margin: 0; padding: 0; }
  #ticker li { padding: 3px 0; font-size: clamp(12px, 1.1vw, 18px);
               color: rgb(var(--on-surface-variant)); }
  #ticker time { color: rgb(var(--on-surface-variant) / .9); margin-right: 12px; }
  #ticker b { color: rgb(var(--on-surface)); font-weight: 600; }

  /* --- Prompt-Knopf und Prompt-Fenster -----------------------------------
     Ein Agent ist eine Markdown-Datei. Das Fenster zeigt sie im Wortlaut, in
     zwei Teilen: oben das Frontmatter, aus dem run-agent.sh die Flags für pi
     baut, darunter der Text, den das Modell als Systemprompt bekommt. */
  .knopf-prompt {
    font: inherit; font-size: clamp(11px, .8vw, 14px); font-weight: 600;
    letter-spacing: .08em; text-transform: uppercase; white-space: nowrap;
    color: rgb(var(--on-surface-variant)); background: transparent;
    border: 1px solid rgb(var(--on-surface) / .25); border-radius: 4px;
    padding: 5px 10px; cursor: pointer;
    transition: border-color 140ms ease, color 140ms ease;
  }
  .knopf-prompt:hover { border-color: rgb(var(--accent)); color: rgb(var(--on-surface)); }
  .knopf-prompt:focus-visible { outline: 2px solid rgb(var(--accent)); outline-offset: 2px; }

  #prompt-fenster {
    width: min(1040px, calc(100vw - 32px)); max-height: calc(100vh - 48px);
    padding: 0; border: none; border-radius: 6px;
    background: rgb(var(--surface)); color: rgb(var(--on-surface));
    box-shadow: 0 12px 40px rgba(0, 0, 0, .35);
  }
  #prompt-fenster[open] { display: flex; flex-direction: column; }
  #prompt-fenster::backdrop { background: rgb(16 24 29 / .6); }
  .fenster-kopf {
    display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
    padding: 10px clamp(12px, 1.6vw, 22px);
    background: rgb(var(--header)); color: rgb(var(--on-header));
  }
  .reiter { display: flex; gap: 4px; flex-wrap: wrap; flex: 1; }
  .reiter button {
    display: flex; align-items: center; gap: 8px;
    font-family: 'Barlow Condensed', 'Barlow', sans-serif;
    font-size: clamp(14px, 1.2vw, 19px); font-weight: 600;
    letter-spacing: .06em; text-transform: uppercase;
    color: rgb(var(--on-header-variant)); background: transparent;
    border: none; border-bottom: 2px solid transparent; padding: 6px 10px; cursor: pointer;
  }
  .reiter button:hover { color: rgb(var(--on-header)); }
  .reiter button[aria-selected="true"] { color: rgb(var(--on-header)); border-bottom-color: rgb(var(--accent)); }
  .reiter button:focus-visible { outline: 2px solid rgb(var(--accent)); outline-offset: 2px; }
  /* Die Sammler und der Zähler behalten ihre Chip-Farben; nur die Steuerung hat
     keine eigene und braucht auf der dunklen Kopfleiste eine helle Kante. */
  .reiter .chip.control { border-color: rgb(var(--on-header) / .3); background: transparent; }
  #prompt-zu {
    width: 32px; height: 32px; flex: none; border-radius: 9999px; border: none;
    font-size: 20px; line-height: 1; cursor: pointer;
    color: rgb(var(--on-header)); background: rgb(var(--on-header) / .1);
  }
  #prompt-zu:hover { background: rgb(var(--on-header) / .2); }
  #prompt-zu:focus-visible { outline: 2px solid rgb(var(--accent)); outline-offset: 2px; }

  .fenster-inhalt { overflow: auto; padding: clamp(14px, 1.8vw, 26px); }
  .datei-name {
    margin: 0 0 14px; font-size: clamp(12px, .95vw, 15px); letter-spacing: .04em;
    color: rgb(var(--on-surface-variant));
  }
  .datei-name code { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; color: rgb(var(--on-surface)); }
  .teil + .teil { margin-top: clamp(14px, 1.6vw, 22px); }
  .teil-titel {
    margin: 0 0 6px; font-size: clamp(11px, .85vw, 14px); font-weight: 600;
    letter-spacing: .12em; text-transform: uppercase; color: rgb(var(--on-surface-variant));
  }
  .teil-titel span { font-weight: 400; letter-spacing: .04em; text-transform: none; }

  /* Markdown im Quelltext, nur eingefärbt, nicht umgesetzt: Die Zuschauer
     sollen sehen, was wirklich in der Datei steht — Rauten und Sternchen
     inklusive. Die Satzzeichen des Markdowns sind grün und treten zurück,
     der Text selbst bleibt vorn. Die Farben der Sammler kommen hier bewusst
     nicht vor; sie bedeuten im Dashboard überall „dieser Agent". */
  .md {
    margin: 0; white-space: pre-wrap; overflow-wrap: anywhere;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    font-size: clamp(13px, 1.15vw, 19px); line-height: 1.55;
    color: rgb(var(--on-surface-variant));
    background: rgb(var(--base)); border: 1px solid rgb(var(--on-surface) / .1);
    border-left: 4px solid rgb(var(--accent)); border-radius: 0 6px 6px 0;
    padding: clamp(10px, 1.2vw, 18px) clamp(12px, 1.4vw, 22px);
  }
  .md.frontmatter { border-left-color: rgb(var(--on-surface) / .3); }
  .md .zeichen  { color: rgb(var(--accent-text)); opacity: .85; }
  .md .schluessel { color: rgb(var(--accent-text)); font-weight: 600; }
  .md .wert     { color: rgb(var(--on-surface)); }
  .md .werkzeug { color: rgb(var(--on-surface)); font-weight: 600;
                  background: rgb(var(--on-surface) / .08); border-radius: 3px; padding: 0 3px; }
  .md .titel    { color: rgb(var(--on-surface)); font-weight: 700; }
  .md strong    { color: rgb(var(--on-surface)); font-weight: 700; }
  .md .inline-code { color: rgb(var(--on-surface)); background: rgb(var(--on-surface) / .08);
                     border-radius: 3px; padding: 0 3px; }
  .md .block-code { color: rgb(var(--on-surface)); }
  .md .fehlt    { color: rgb(var(--error-color)); }
  .md .hinweis  { color: rgb(var(--on-surface-variant)); font-style: italic; }

  footer { margin-top: clamp(18px, 2vw, 30px); color: rgb(var(--on-surface-variant));
           font-size: clamp(11px, .9vw, 15px); }
  .offline { color: rgb(var(--error-color)); }
</style>
</head>
<body>
  <header class="kopfleiste">
    <div class="kopf-marke">
      <!-- Bildmarke StudiumPlus: Kreuz aus fünf Quadraten, die Mitte in THM
           Grün. Das Raster ist am Logo abgemessen — Quadrat zu Lücke verhält
           sich 2:1, hier 8 zu 4 auf 32 Einheiten. -->
      <svg class="kopf-logo" viewBox="0 0 32 32" role="img" aria-label="StudiumPlus">
        <rect x="12" y="0"  width="8" height="8" class="logo-grau"/>
        <rect x="0"  y="12" width="8" height="8" class="logo-grau"/>
        <rect x="12" y="12" width="8" height="8" class="logo-gruen"/>
        <rect x="24" y="12" width="8" height="8" class="logo-grau"/>
        <rect x="12" y="24" width="8" height="8" class="logo-grau"/>
      </svg>
      <div>
        <h1 class="kopf-titel">Counting Agents</h1>
        <p class="kopf-unterzeile">pi &middot; Herdr &middot; Event-Bus</p>
      </div>
    </div>

    <div class="kopf-rechts">
      <span id="uhr"></span>
      <button id="thema" type="button" aria-label="Farbthema wechseln">
        <svg class="sonne" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <circle cx="12" cy="12" r="4"/>
          <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>
        </svg>
        <svg class="mond" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>
        </svg>
      </button>
    </div>
  </header>

  <main>
    <div class="inhalt">
      <section class="kennzahlen">
        <div class="kennzahlen-raster" aria-hidden="true"></div>
        <div class="kennzahlen-inhalt">
          <p class="kennzahlen-marke">Zahlen-Bus</p>
          <p id="summary">Warte auf den Bus&hellip;</p>
          <p id="takt"></p>
        </div>
      </section>

      <section class="abschnitt">
        <h2 class="abschnitt-titel">Zahlenband</h2>
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
      </section>

      <section class="abschnitt">
        <h2 class="abschnitt-titel">Agenten</h2>
        <div class="agents" id="agents"></div>
      </section>

      <section class="karte">
        <div class="karte-kopf">
          <h2 class="abschnitt-titel">Steuerung</h2>
          <button type="button" class="knopf-prompt" data-prompt="control">Prompt</button>
        </div>
        <ul id="ticker"><li>keine Befehle</li></ul>
      </section>

      <footer id="fuss">Liest nur mit &mdash; Bus und Zustand bleiben unberührt.</footer>
    </div>
  </main>

  <!-- Das Prompt-Fenster: ein Reiter je Agent, darunter seine Datei. -->
  <dialog id="prompt-fenster" aria-label="Agentendatei">
    <div class="fenster-kopf">
      <div class="reiter" id="prompt-reiter" role="tablist" aria-label="Agentendateien"></div>
      <button type="button" id="prompt-zu" aria-label="Schließen" title="Schließen (Esc)">&times;</button>
    </div>
    <div class="fenster-inhalt" id="prompt-inhalt" role="tabpanel"></div>
  </dialog>

<script>
const LABEL = {
  counter: ["counter", "Zähler"],
  odd:     ["odd", "Ungerade"],
  even:    ["even", "Gerade"],
  prime:   ["prime", "Primzahlen"],
  control: ["control", "Steuerung"],   // nur für das Prompt-Fenster, keine Zeile
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

// Die Zeilen entstehen einmal und bleiben stehen; neu gesetzt wird nur ihr
// Inhalt. Der Prompt-Knopf überlebt so jede Aktualisierung — sonst würde er
// mehrmals pro Sekunde ausgetauscht, und ein Klick, der gerade in einen
// Austausch fällt, käme nie an.
const agentZeilen = new Map();   // Name -> {zeile, teile}

function agentZeile(name) {
  let z = agentZeilen.get(name);
  if (z) return z;
  const zeile = document.createElement("div");
  zeile.dataset.agent = name;
  zeile.innerHTML = `<span class="teile"></span>
    <button type="button" class="knopf-prompt" data-prompt="${name}">Prompt</button>`;
  if (SAMMLER.includes(name)) {
    // Der Prompt-Knopf liegt in der Zeile, soll aber nicht zugleich den Fokus umschalten.
    zeile.addEventListener("click", (e) => {
      if (!e.target.closest("[data-prompt]")) setzeFokus(name);
    });
  }
  document.getElementById("agents").appendChild(zeile);
  z = { zeile, teile: zeile.firstElementChild };
  agentZeilen.set(name, z);
  return z;
}

function zeichneAgenten(data) {
  const latest = data.bus.latest_seq || 1;
  for (const name of ["counter", "odd", "even", "prime"]) {
    const a = data.agents[name];
    const [kurz, lang] = LABEL[name];
    const { zeile, teile } = agentZeile(name);
    zeile.className = "agent a-" + name + " " + a.status
      + (SAMMLER.includes(name) ? " klickbar" : "")
      + (fokus === name ? " fokus" : "");

    const mitte = name === "counter"
      ? `<span class="zahl">Wert ${a.last_value}</span><span></span><span></span>`
      : `<span class="zahl">${a.count} Zahlen</span>
         <span class="lag ${a.lag ? "zurueck" : "aktuell"}">${a.lag ? a.lag + " zurück" : "aktuell"}</span>
         <span class="balken"><i style="width:${Math.min(100, 100 * a.last_seq / latest)}%"></i></span>`;

    teile.innerHTML = `
      <span class="name"><i class="chip ${name}"></i>${kurz}<small>${lang}</small></span>
      <span class="status">${STATUS[a.status] || a.status}${a.still ? ` <span class="still">· seit ${Math.round(a.idle_seconds)}s still</span>` : ""}</span>
      ${mitte}`;
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
  document.getElementById("summary").textContent =
    `${data.bus.count} Zahlen im Bus`;
  document.getElementById("takt").innerHTML =
    `zuletzt <b>${data.bus.last_value}</b>` +
    (takt ? ` &middot; ${takt.toFixed(1).replace(".", ",")} s pro Zahl` : "");
  document.getElementById("uhr").textContent = data.generated_at;
  zeichneBand(data.numbers);
  zeichneAgenten(data);
  zeichneTicker(data.control);
}

// --- Prompt-Fenster --------------------------------------------------------
// Ein Agent ist eine Markdown-Datei: oben das Frontmatter mit den Einstellungen,
// darunter die Aufgabe in normalem Deutsch. Das Fenster zeigt die Datei im
// Wortlaut und färbt das Markdown ein, ohne es umzusetzen — eine
// Hervorhebungs-Bibliothek wäre eine Abhängigkeit mehr, und für die Handvoll
// Auszeichnungen in den Agentendateien reicht ein Zeilen-Durchgang.
const PROMPT_AGENTEN = Object.keys(LABEL);
const fenster = document.getElementById("prompt-fenster");
const reiter = document.getElementById("prompt-reiter");
const inhalt = document.getElementById("prompt-inhalt");
let offenerPrompt = null;
let promptAnfrage = 0;   // nur die jüngste Antwort zählt, falls schnell umgeschaltet wird

function esc(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
const zeichen = (text) => `<span class="zeichen">${esc(text)}</span>`;

// Innerhalb einer Zeile: `Code` und **fett**. Zuerst an den Backticks trennen,
// damit Sternchen in einem Code-Stück Code bleiben.
function mdInline(text) {
  return text.split(/(`[^`]+`)/).map((teil, i) => i % 2
    ? `<span class="inline-code">${zeichen("`")}${esc(teil.slice(1, -1))}${zeichen("`")}</span>`
    : esc(teil).replace(/\*\*(.+?)\*\*/g, `${zeichen("**")}<strong>$1</strong>${zeichen("**")}`)
  ).join("");
}

function mdZeile(zeile) {
  let m;
  if ((m = zeile.match(/^(#{1,6} )(.*)$/))) {
    return zeichen(m[1]) + `<span class="titel">${mdInline(m[2])}</span>`;
  }
  if ((m = zeile.match(/^(\s*)([-*]|\d+\.)( .*)$/))) {
    return m[1] + zeichen(m[2]) + mdInline(m[3]);
  }
  return mdInline(zeile);
}

function mdRumpf(zeilen) {
  let imCode = false;
  return zeilen.map(zeile => {
    if (/^\s*```/.test(zeile)) { imCode = !imCode; return zeichen(zeile); }
    if (imCode) return `<span class="block-code">${esc(zeile)}</span>`;
    return mdZeile(zeile);
  }).join("\n");
}

// Frontmatter: Schlüssel, Doppelpunkt, Wert. Bei `tools` wird jedes Werkzeug
// einzeln hervorgehoben — das ist die Zeile, an der man im Vortrag dreht.
// `modell` ist COUNTING_AGENTS_MODEL aus der .env: Es schlägt die Zeile
// `model:`, und das Fenster sagt dazu, womit der Agent wirklich läuft.
function mdFrontmatter(zeilen, modell) {
  return zeilen.map(zeile => {
    if (zeile === "---") return zeichen(zeile);
    const m = zeile.match(/^([\w-]+)(:\s*)(.*)$/);
    if (!m) return esc(zeile);
    const wert = m[1] === "tools"
      ? m[3].split(/(,\s*)/).map((w, i) => i % 2 ? zeichen(w) : `<span class="werkzeug">${esc(w)}</span>`).join("")
      : `<span class="wert">${esc(m[3])}</span>`;
    const hinweis = m[1] === "model" && modell && modell !== m[3].trim()
      ? `<span class="hinweis">  ← läuft mit ${esc(modell)} (COUNTING_AGENTS_MODEL in .env)</span>`
      : "";
    return `<span class="schluessel">${esc(m[1])}</span>${zeichen(m[2])}${wert}${hinweis}`;
  }).join("\n");
}

// Aufgeteilt wie in agents-lib.sh: bis zum zweiten `---` das Frontmatter,
// danach der Systemprompt. Eine Abweichung ist gewollt: agent_prompt lässt
// jede Zeile `---` weg, auch eine im Rumpf — hier bleibt die Datei im Wortlaut.
function zeigeDatei(name, text, modell) {
  const zeilen = text.replace(/\r\n/g, "\n").split("\n");
  let kopf = [], rumpf = zeilen;
  if (zeilen[0] === "---") {
    const ende = zeilen.indexOf("---", 1);
    if (ende > 0) { kopf = zeilen.slice(0, ende + 1); rumpf = zeilen.slice(ende + 1); }
  }
  while (rumpf.length && !rumpf[0].trim()) rumpf.shift();
  while (rumpf.length && !rumpf[rumpf.length - 1].trim()) rumpf.pop();

  inhalt.innerHTML =
    `<p class="datei-name">Datei <code>agents/${name}.md</code></p>` +
    (kopf.length ? `<div class="teil">
      <p class="teil-titel">Frontmatter <span>— daraus werden die Einstellungen für pi: Modell, Werkzeuge, Nachdenken</span></p>
      <pre class="md frontmatter">${mdFrontmatter(kopf, modell)}</pre></div>` : "") +
    `<div class="teil">
      <p class="teil-titel">Systemprompt <span>— dieser Text geht als Auftrag an das Modell</span></p>
      <pre class="md">${mdRumpf(rumpf)}</pre></div>`;
  inhalt.scrollTop = 0;
}

async function zeigePrompt(name) {
  offenerPrompt = name;
  for (const knopf of reiter.children) {
    knopf.setAttribute("aria-selected", knopf.dataset.reiter === name ? "true" : "false");
  }
  if (!fenster.open) fenster.showModal();
  const nummer = ++promptAnfrage;
  let text = null, modell = null;
  let fehler = "Keine Verbindung — läuft dashboard.py noch?";
  try {
    const antwort = await fetch("/agent/" + name, { cache: "no-store" });
    if (antwort.ok) {
      text = await antwort.text();
      const kopf = antwort.headers.get("X-Modell-Env");
      if (kopf) modell = decodeURIComponent(kopf);
    } else {
      fehler = "Datei nicht gefunden.";
    }
  } catch (e) {}
  if (nummer !== promptAnfrage) return;
  if (text === null) {
    inhalt.innerHTML = `<p class="datei-name">Datei <code>agents/${name}.md</code></p>
      <pre class="md"><span class="fehlt">${fehler}</span></pre>`;
    return;
  }
  zeigeDatei(name, text, modell);
}

reiter.innerHTML = PROMPT_AGENTEN.map(name =>
  `<button type="button" role="tab" data-reiter="${name}" aria-selected="false" title="${LABEL[name][1]}"><i class="chip ${name}"></i>${name}</button>`
).join("");
reiter.addEventListener("click", (e) => {
  const knopf = e.target.closest("[data-reiter]");
  if (knopf) zeigePrompt(knopf.dataset.reiter);
});
// Ein Zuhörer für alle Prompt-Knöpfe: die in den Agentenzeilen und den in
// der Steuerungs-Karte.
document.addEventListener("click", (e) => {
  const knopf = e.target.closest("[data-prompt]");
  if (knopf) zeigePrompt(knopf.dataset.prompt);
});
document.getElementById("prompt-zu").addEventListener("click", () => fenster.close());
// Klick neben das Fenster schließt es; Esc erledigt der Browser selbst.
fenster.addEventListener("click", (e) => { if (e.target === fenster) fenster.close(); });
// Mit den Pfeiltasten von Agent zu Agent — praktisch mit dem Presenter.
fenster.addEventListener("keydown", (e) => {
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const namen = PROMPT_AGENTEN;
  const schritt = e.key === "ArrowRight" ? 1 : -1;
  const i = (namen.indexOf(offenerPrompt) + schritt + namen.length) % namen.length;
  e.preventDefault();
  zeigePrompt(namen[i]);
  reiter.children[i].focus();
});

// Farbthema: Dunkel ist die Voreinstellung, die Wahl überlebt das Neuladen.
// Welches Symbol der Knopf zeigt, regelt das CSS über die Klasse "dark"; hier
// wird nur die Beschriftung für Screenreader nachgezogen.
const thema = document.getElementById("thema");
function zeigeThema() {
  const dunkel = document.documentElement.classList.contains("dark");
  const label = dunkel ? "Zum hellen Farbthema wechseln" : "Zum dunklen Farbthema wechseln";
  thema.setAttribute("aria-label", label);
  thema.title = label;
}
thema.addEventListener("click", () => {
  const dunkel = !document.documentElement.classList.contains("dark");
  document.documentElement.classList.toggle("dark", dunkel);
  try { localStorage.setItem("counting-agents-theme", dunkel ? "dark" : "light"); } catch (e) {}
  zeigeThema();
});
zeigeThema();

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
        elif self.path.startswith("/agent/"):
            self._send_agent_file(self.path[len("/agent/"):])
        else:
            self.send_error(404)

    def _send_agent_file(self, agent):
        """Die Agentendatei als Klartext. Jedes Mal frisch von der Platte —
        nimmt man einem Agenten im Vortrag ein Werkzeug weg, zeigt das
        Dashboard beim nächsten Öffnen schon die geänderte Datei."""
        text = dashboard_data.agent_file(agent)
        if text is None:
            self.send_error(404)
            return
        body = text.encode("utf8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        # Das Modell aus der .env schlägt die Zeile `model:` der Datei; das
        # Fenster soll zeigen, womit der Agent tatsächlich läuft.
        modell = dashboard_data.model_override()
        if modell:
            self.send_header("X-Modell-Env", urllib.parse.quote(modell, safe="/:@"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

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
