// test-tools.mjs — Prüft die Werkzeuge aus .pi/extensions/counting-tools.ts
//
// Aufruf: node scripts/test-tools.mjs
//
// Der Test kommt ohne Modell und ohne Netz aus: er lädt die Extension mit
// demselben TypeScript-Lader, den pi benutzt, fängt die registrierten
// Werkzeuge mit einer Attrappe ab und ruft sie direkt auf. Vor der Vorlesung
// einmal laufen lassen — dann weiß man, dass die Mechanik steht, bevor
// irgendein Agent startet.

import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const PROJECT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

// pi bringt seinen TypeScript-Lader (jiti) und die Schema-Bibliotheken selbst
// mit. Wir suchen sie dort, wo die installierte pi-CLI liegt.
const piBinary = fs.realpathSync(execSync("which pi", { encoding: "utf8" }).trim());
const piPackage = path.resolve(piBinary, "..", "..", "..");
const piModules = path.join(piPackage, "node_modules");

for (const required of ["jiti", "typebox", "@earendil-works/pi-ai"]) {
  if (!fs.existsSync(path.join(piModules, required))) {
    console.error(`Fehler: ${required} nicht gefunden unter ${piModules}`);
    console.error("Ist pi über npm installiert? (which pi)");
    process.exit(1);
  }
}

const { createJiti } = await import(pathToFileURL(path.join(piModules, "jiti/lib/jiti.mjs")));
const jiti = createJiti(import.meta.url, {
  alias: {
    typebox: path.join(piModules, "typebox/build/index.mjs"),
    "@earendil-works/pi-ai": path.join(piModules, "@earendil-works/pi-ai/dist/index.js"),
  },
});

const extension = await jiti.import(path.join(PROJECT, ".pi/extensions/counting-tools.ts"), {
  default: true,
});

const tools = {};
extension({ registerTool: (definition) => (tools[definition.name] = definition) });

const call = async (name, params) => {
  const result = await tools[name].execute("test", params, undefined, undefined, {});
  return { text: result.content[0].text, isError: result.isError ?? false };
};

// --- Testlauf auf leerem Stand -------------------------------------------

const AGENTS = ["counter", "odd", "even", "prime"];
const clean = () => {
  fs.rmSync(path.join(PROJECT, "_bus/numbers.log"), { force: true });
  fs.rmSync(path.join(PROJECT, "_bus/control.log"), { force: true });
  for (const a of AGENTS) fs.rmSync(path.join(PROJECT, `_state/${a}.json`), { force: true });
};

let failed = 0;
const check = (label, condition, detail = "") => {
  if (!condition) failed++;
  console.log(`${condition ? "✓" : "✗ FEHLER"}  ${label}${detail ? `  ${detail}` : ""}`);
};
const pause = () => new Promise((resolve) => setTimeout(resolve, 5));

clean();
console.log(`Werkzeuge: ${Object.keys(tools).join(", ")}\n`);

let r = await call("state_read", { agent: "counter" });
check("state_read ohne Datei liefert Startwerte", r.text.includes('"last_value":0') && !r.isError);
r = await call("bus_read", { since: 0 });
check("bus_read auf leerem Bus", r.text === '{"events":[],"latest_seq":0,"remaining":0}');
r = await call("control_read", { agent: "odd" });
check("control_read ohne Steuerungslog", JSON.parse(r.text).status === "running");

for (const value of [1, 2, 3]) await call("bus_publish", { value });
r = await call("bus_read", { since: 0 });
check("drei Ereignisse mit fortlaufender Sequenznummer", JSON.parse(r.text).latest_seq === 3);
r = await call("bus_read", { since: 2 });
check("bus_read liefert nur Neues", JSON.parse(r.text).events.length === 1);
r = await call("bus_read", { since: 0, limit: 2 });
check("limit begrenzt und meldet den Rest", JSON.parse(r.text).remaining === 1);
r = await call("bus_publish", { value: 1.5 });
check("Kommazahl wird abgelehnt", r.isError);

await call("state_write", { agent: "odd", last_seq: 3, numbers: [1, 3] });
r = await call("state_write", { agent: "odd", last_seq: 4 });
const odd = JSON.parse(r.text);
check("state_write behält numbers bei Teilaktualisierung", odd.numbers.length === 2 && odd.last_seq === 4);
check("count wird automatisch gesetzt", odd.count === 2);
check("updated_at wird automatisch gesetzt", typeof odd.updated_at === "string");

await call("control_send", { target: "odd", command: "pause" });
check("pause wirkt", JSON.parse((await call("control_read", { agent: "odd" })).text).status === "paused");
await call("control_send", { target: "all", command: "resume" });
check("resume an 'all' wirkt mit", JSON.parse((await call("control_read", { agent: "odd" })).text).status === "running");
await call("control_send", { target: "odd", command: "verbose" });
check("verbose wirkt", JSON.parse((await call("control_read", { agent: "odd" })).text).verbose === true);
check("Befehl an odd lässt even unberührt", JSON.parse((await call("control_read", { agent: "even" })).text).verbose === false);

await pause();
await call("control_send", { target: "all", command: "reset" });
check("Reset wird angefordert", JSON.parse((await call("control_read", { agent: "odd" })).text).reset_requested === true);
await pause();
await call("state_write", { agent: "odd", last_seq: 0, numbers: [] });
check("nach state_write ist der Reset erledigt", JSON.parse((await call("control_read", { agent: "odd" })).text).reset_requested === false);

r = await call("state_read", { agent: "all" });
check("state_read 'all' liefert alle vier", Object.keys(JSON.parse(r.text)).join(",") === AGENTS.join(","));

// Eine halb geschriebene Zeile entsteht, wenn zwei Agenten gleichzeitig lesen
// und schreiben. Sie darf den Bus nicht umwerfen.
fs.appendFileSync(path.join(PROJECT, "_bus/numbers.log"), '{"type":"number","seq":4,"val\n');
r = await call("bus_read", { since: 0 });
check("halb geschriebene Zeile wird übersprungen", JSON.parse(r.text).latest_seq === 3);
r = await call("bus_publish", { value: 4 });
check("Veröffentlichen läuft danach weiter", JSON.parse(r.text).published.seq === 4);

clean();

console.log("");
if (failed > 0) {
  console.error(`${failed} Prüfung(en) fehlgeschlagen.`);
  process.exit(1);
}
console.log("Alle Prüfungen bestanden.");
