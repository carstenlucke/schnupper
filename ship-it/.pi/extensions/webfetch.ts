// webfetch.ts — Ein Werkzeug, mit dem die Agenten Webseiten lesen können
//
// pi bringt kein Werkzeug für das Internet mit, nur read, write, edit, bash,
// grep, find und ls. Recherchieren könnten die Agenten also nur über
// `bash curl ...` — das scheitert oft an Seiten, die Skripte abweisen, und
// liefert rohes HTML, in dem der eigentliche Text untergeht.
//
// Dieses Werkzeug holt eine Seite, wirft Skripte, Stile und Markup weg und gibt
// den lesbaren Text zurück, gekürzt auf ein verdauliches Maß. Im Terminal des
// Dashboards steht dann `webfetch https://…` statt einer Shell-Zeile.

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

// Obergrenze für den zurückgegebenen Text. Alles, was das Werkzeug liefert,
// liest das Modell mit — eine lange Seite kostet sonst Zeit und Tokens, ohne
// dass die Analyse besser wird.
const MAX_ZEICHEN = 20_000;
// Obergrenze für das, was überhaupt heruntergeladen wird. Die Kürzung auf
// MAX_ZEICHEN kommt erst nach dem Laden — ohne diese Grenze könnte eine
// riesige Seite den Speicher des Agenten volllaufen lassen.
const MAX_BYTES = 5_000_000;
const ZEITLIMIT_MS = 20_000;

const ok = (text: string, details: Record<string, unknown>) => ({
  content: [{ type: "text" as const, text }],
  details,
});

// Fehler meldet pi nur, wenn execute wirft – ein zurückgegebenes isError
// ignoriert es. Nur so zeigt das Dashboard den Fehlschlag rot an.
const fail = (message: string): never => {
  throw new Error(message);
};

/** Macht aus HTML lesbaren Text: Skripte, Stile und Tags raus, Absätze bleiben. */
function htmlZuText(html: string): string {
  return html
    .replace(/<(script|style|noscript|svg|template)\b[\s\S]*?<\/\1>/gi, " ")
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/<(br|\/p|\/div|\/li|\/h[1-6]|\/tr|\/section|\/article)\b[^>]*>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&amp;/g, "&")
    .replace(/[ \t]+/g, " ")
    .replace(/ *\n */g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** Liest den Text der Antwort, aber höchstens MAX_BYTES — der Rest wird gar nicht erst geladen. */
async function leseBegrenzt(antwort: Response): Promise<{ text: string; abgeschnitten: boolean }> {
  const leser = antwort.body?.getReader();
  if (!leser) return { text: "", abgeschnitten: false };
  const decoder = new TextDecoder();
  let text = "";
  let bytes = 0;
  while (true) {
    const { done, value } = await leser.read();
    if (done) return { text: text + decoder.decode(), abgeschnitten: false };
    if (bytes + value.byteLength > MAX_BYTES) {
      text += decoder.decode(value.subarray(0, MAX_BYTES - bytes));
      await leser.cancel().catch(() => {});
      return { text, abgeschnitten: true };
    }
    bytes += value.byteLength;
    text += decoder.decode(value, { stream: true });
  }
}

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "webfetch",
    label: "Web · Seite lesen",
    description:
      "Lädt eine Webseite und gibt ihren lesbaren Text zurück — ohne HTML, Skripte " +
      `und Stile, gekürzt auf ${MAX_ZEICHEN} Zeichen. Für Recherche im Internet; ` +
      "statt curl oder wget über bash.",
    parameters: Type.Object({
      url: Type.String({ description: "Vollständige Adresse der Seite, mit https://" }),
    }),
    async execute(_toolCallId, params, signal) {
      let ziel: URL;
      try {
        ziel = new URL(params.url);
      } catch {
        return fail(`Keine gültige Adresse: ${params.url}`);
      }
      if (ziel.protocol !== "https:" && ziel.protocol !== "http:") {
        return fail(`Nur http- und https-Adressen, nicht ${ziel.protocol}`);
      }

      // Bricht pi den Durchlauf ab, soll auch die Anfrage enden — und eine
      // Seite, die nicht antwortet, darf den Agenten nicht festhalten.
      const zeitlimit = AbortSignal.timeout(ZEITLIMIT_MS);
      let antwort: Response;
      try {
        antwort = await fetch(ziel, {
          signal: signal ? AbortSignal.any([signal, zeitlimit]) : zeitlimit,
          redirect: "follow",
          headers: {
            "User-Agent": "Mozilla/5.0 (Ship It! Schnuppervorlesung)",
            Accept: "text/html,text/plain,application/json;q=0.9,*/*;q=0.5",
          },
        });
      } catch (error) {
        const grund = zeitlimit.aborted ? `keine Antwort nach ${ZEITLIMIT_MS / 1000}s` : String(error);
        return fail(`${ziel.href} nicht erreichbar: ${grund}`);
      }
      if (!antwort.ok) {
        return fail(`${ziel.href} antwortet mit HTTP ${antwort.status}.`);
      }

      const typ = antwort.headers.get("content-type") ?? "";
      if (!/html|text|json|xml/i.test(typ)) {
        return fail(`${ziel.href} liefert keinen Text, sondern ${typ || "unbekannten Inhalt"}.`);
      }
      const { text: roh, abgeschnitten } = await leseBegrenzt(antwort);
      const text = /html/i.test(typ) ? htmlZuText(roh) : roh.trim();
      let gekuerzt = text.slice(0, MAX_ZEICHEN);
      if (abgeschnitten) {
        gekuerzt += `\n\n[… gekürzt, nur die ersten ${MAX_BYTES / 1_000_000} MB der Seite gelesen]`;
      } else if (text.length > MAX_ZEICHEN) {
        gekuerzt += `\n\n[… gekürzt, ${text.length} Zeichen insgesamt]`;
      }

      return ok(`Quelle: ${antwort.url}\n\n${gekuerzt}`, {
        url: antwort.url,
        zeichen: text.length,
        abgeschnitten,
      });
    },
  });
}
