// counting-tools.ts — Die Werkzeuge der Zähl-Agenten
//
// Ohne diese Datei müssten die Agenten ihre Arbeit über die allgemeinen
// Werkzeuge (bash, read, write) erledigen: JSON von Hand zusammenbauen, an
// Logdateien anhängen, Zeitstempel erzeugen, leere Dateien abfangen. Genau
// das stand früher als seitenlange Fehlerbehandlung in jedem Agent-Prompt.
//
// Hier bekommt stattdessen jeder Handgriff ein eigenes Werkzeug mit einem
// sprechenden Namen. Im Pane steht dann `bus_publish {value: 42}` statt einer
// Shell-Zeile — für ein Publikum ohne Programmiererfahrung der entscheidende
// Unterschied. Die Agent-Prompts schrumpfen von zwei Seiten auf zwölf Zeilen.
//
// Die Werkzeuge sind bewusst schmal: sie erledigen die Buchhaltung
// (Sequenznummern, Zeitstempel, Zählerstände), treffen aber keine
// Entscheidungen. Ob eine Zahl gerade oder prim ist, entscheidet weiterhin
// das Modell — das ist ja das, was in der Vorlesung zu sehen sein soll.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { StringEnum } from "@earendil-works/pi-ai";
import { Type } from "typebox";

// Pfade hängen an der Lage dieser Datei (.pi/extensions/), nicht am
// Arbeitsverzeichnis. So schreibt ein aus einem Unterordner gestarteter Agent
// nicht versehentlich einen zweiten Event-Bus.
const PROJECT_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const NUMBERS_LOG = path.join(PROJECT_DIR, "_bus", "numbers.log");
const CONTROL_LOG = path.join(PROJECT_DIR, "_bus", "control.log");

const AGENTS = ["counter", "odd", "even", "prime"] as const;
const COMMANDS = ["pause", "resume", "stop", "reset", "verbose", "quiet"] as const;

type AgentName = (typeof AGENTS)[number];

interface NumberEvent {
  type: "number";
  seq: number;
  value: number;
  timestamp: string;
}

interface ControlEvent {
  type: "control";
  target: AgentName | "all";
  command: (typeof COMMANDS)[number];
  timestamp: string;
}

interface AgentState {
  agent: AgentName;
  last_seq?: number;
  last_value?: number;
  numbers?: number[];
  count?: number;
  status?: string;
  updated_at?: string | null;
}

// --- Dateizugriff ---------------------------------------------------------

const stateFile = (agent: AgentName) => path.join(PROJECT_DIR, "_state", `${agent}.json`);

// Zeitstempel mit Millisekunden. Die Reihenfolge zweier Ereignisse innerhalb
// derselben Sekunde muss erkennbar bleiben — control_read vergleicht sie.
const now = () => new Date().toISOString();

/** Liest eine Logdatei zeilenweise als JSON. Fehlende Datei, leere Datei und
 *  kaputte Zeilen führen nie zu einem Fehler, sondern zu weniger Ereignissen. */
function readLog<T>(file: string): T[] {
  if (!fs.existsSync(file)) return [];
  const events: T[] = [];
  for (const line of fs.readFileSync(file, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      events.push(JSON.parse(trimmed) as T);
    } catch {
      // Halb geschriebene Zeile — beim nächsten Durchlauf ist sie vollständig.
    }
  }
  return events;
}

/** Hängt ein Ereignis an eine Logdatei an. Anhängen ist die einzige erlaubte
 *  Schreibart am Bus: Vergangenes wird nie überschrieben. */
function appendLog(file: string, event: unknown): void {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.appendFileSync(file, `${JSON.stringify(event)}\n`, "utf8");
}

function defaultState(agent: AgentName): AgentState {
  return agent === "counter"
    ? { agent, last_value: 0, status: "running", updated_at: null }
    : { agent, last_seq: 0, numbers: [], count: 0, updated_at: null };
}

function readState(agent: AgentName): AgentState {
  const file = stateFile(agent);
  if (!fs.existsSync(file)) return defaultState(agent);
  const raw = fs.readFileSync(file, "utf8").trim();
  if (!raw) return defaultState(agent);
  try {
    return { ...defaultState(agent), ...(JSON.parse(raw) as AgentState), agent };
  } catch {
    return defaultState(agent);
  }
}

const ok = (payload: unknown) => ({
  content: [{ type: "text" as const, text: JSON.stringify(payload) }],
  details: payload as Record<string, unknown>,
});

const fail = (message: string) => ({
  content: [{ type: "text" as const, text: message }],
  details: { error: message },
  isError: true,
});

// --- Werkzeuge ------------------------------------------------------------

export default function (pi: ExtensionAPI) {
  // bus_publish — eine Zahl in den Event-Bus stellen.
  // Die Sequenznummer vergibt das Werkzeug: der Agent liefert nur den Wert.
  pi.registerTool({
    name: "bus_publish",
    label: "Bus · veröffentlichen",
    description:
      "Stellt eine Zahl als Ereignis in den Event-Bus (_bus/numbers.log). " +
      "Die fortlaufende Sequenznummer und der Zeitstempel werden automatisch vergeben. " +
      "Gibt das geschriebene Ereignis zurück.",
    parameters: Type.Object({
      value: Type.Number({ description: "Die zu veröffentlichende Zahl" }),
    }),
    async execute(_toolCallId, params) {
      if (!Number.isInteger(params.value)) {
        return fail(`Nur ganze Zahlen können veröffentlicht werden, nicht ${params.value}.`);
      }
      const events = readLog<NumberEvent>(NUMBERS_LOG);
      const lastSeq = events.reduce((max, e) => Math.max(max, e.seq ?? 0), 0);
      const event: NumberEvent = {
        type: "number",
        seq: lastSeq + 1,
        value: params.value,
        timestamp: now(),
      };
      appendLog(NUMBERS_LOG, event);
      return ok({ published: { seq: event.seq, value: event.value } });
    },
  });

  // bus_read — die noch nicht gesehenen Ereignisse holen.
  // `since` ist die zuletzt verarbeitete Sequenznummer aus dem eigenen State.
  pi.registerTool({
    name: "bus_read",
    label: "Bus · lesen",
    description:
      "Liest neue Ereignisse aus dem Event-Bus (_bus/numbers.log): alle mit einer " +
      "Sequenznummer größer als `since`. Gibt die Ereignisse, die höchste " +
      "Sequenznummer im Bus und die Zahl der noch nicht gelieferten Ereignisse zurück.",
    parameters: Type.Object({
      since: Type.Number({
        description: "Zuletzt verarbeitete Sequenznummer; 0 liest von Anfang an",
      }),
      limit: Type.Optional(
        Type.Number({ description: "Höchstens so viele Ereignisse liefern (Standard: 50)" }),
      ),
    }),
    async execute(_toolCallId, params) {
      const limit = Math.max(1, Math.min(params.limit ?? 50, 500));
      const events = readLog<NumberEvent>(NUMBERS_LOG);
      const latestSeq = events.reduce((max, e) => Math.max(max, e.seq ?? 0), 0);
      const pending = events.filter((e) => (e.seq ?? 0) > params.since);
      const delivered = pending.slice(0, limit);
      return ok({
        events: delivered.map((e) => ({ seq: e.seq, value: e.value })),
        latest_seq: latestSeq,
        remaining: pending.length - delivered.length,
      });
    },
  });

  // control_read — den für mich geltenden Zustand erfragen.
  // Das Werkzeug wertet den Steuerungs-Bus aus Sicht eines Agenten aus, statt
  // ihm rohe Ereignisse hinzulegen: Befehle an "all" gelten mit, spätere
  // Befehle überschreiben frühere.
  pi.registerTool({
    name: "control_read",
    label: "Steuerung · lesen",
    description:
      "Fragt ab, was für einen Agenten gerade gilt. Wertet _bus/control.log aus: " +
      "Befehle an den Agenten selbst und an 'all', spätere überschreiben frühere. " +
      "Gibt status (running/paused/stopped), verbose (an/aus) und reset_requested zurück. " +
      "reset_requested ist true, wenn seit dem letzten state_write ein Reset angefordert wurde.",
    parameters: Type.Object({
      agent: StringEnum(AGENTS, { description: "Für welchen Agenten gefragt wird" }),
    }),
    async execute(_toolCallId, params) {
      const relevant = readLog<ControlEvent>(CONTROL_LOG).filter(
        (e) => e.target === params.agent || e.target === "all",
      );

      let status = "running";
      let verbose = false;
      let lastReset: string | null = null;

      for (const event of relevant) {
        switch (event.command) {
          case "pause":
            status = "paused";
            break;
          case "resume":
            status = "running";
            break;
          case "stop":
            status = "stopped";
            break;
          case "verbose":
            verbose = true;
            break;
          case "quiet":
            verbose = false;
            break;
          case "reset":
            lastReset = event.timestamp ?? now();
            status = "running";
            break;
        }
      }

      // Ein Reset gilt als erledigt, sobald der Agent danach seinen State
      // geschrieben hat. Ohne diesen Vergleich würde er sich bei jedem
      // Durchlauf erneut zurücksetzen und nie wieder vorankommen.
      const updatedAt = readState(params.agent).updated_at ?? null;
      const resetRequested = lastReset !== null && (updatedAt === null || lastReset > updatedAt);

      return ok({ status, verbose, reset_requested: resetRequested });
    },
  });

  // control_send — ein Kommando an die Agenten schicken.
  // Nur der Control-Agent bekommt dieses Werkzeug (siehe agents/control.md).
  pi.registerTool({
    name: "control_send",
    label: "Steuerung · senden",
    description:
      "Schickt einen Steuerbefehl an einen Agenten oder an alle (_bus/control.log). " +
      "Erlaubte Befehle: pause, resume, stop, reset, verbose, quiet.",
    parameters: Type.Object({
      target: StringEnum([...AGENTS, "all"] as const, {
        description: "Empfänger: ein Agent oder 'all'",
      }),
      command: StringEnum(COMMANDS, { description: "Der Befehl" }),
    }),
    async execute(_toolCallId, params) {
      const event: ControlEvent = {
        type: "control",
        target: params.target,
        command: params.command,
        timestamp: now(),
      };
      appendLog(CONTROL_LOG, event);
      return ok({ sent: { target: event.target, command: event.command } });
    },
  });

  // state_read — den eigenen (oder, für die Steuerung, jeden) Zustand lesen.
  pi.registerTool({
    name: "state_read",
    label: "Zustand · lesen",
    description:
      "Liest den gespeicherten Zustand eines Agenten aus _state/<agent>.json. " +
      "Mit 'all' kommen alle vier Zustände auf einmal. Fehlt eine Datei, kommen " +
      "die Startwerte zurück — ein Fehler ist das nie.",
    parameters: Type.Object({
      agent: StringEnum([...AGENTS, "all"] as const, {
        description: "Welcher Zustand gelesen wird",
      }),
    }),
    async execute(_toolCallId, params) {
      if (params.agent === "all") {
        return ok(Object.fromEntries(AGENTS.map((a) => [a, readState(a)])));
      }
      return ok(readState(params.agent as AgentName));
    },
  });

  // state_write — den eigenen Zustand fortschreiben.
  // Nur die übergebenen Felder ändern sich; count und updated_at setzt das
  // Werkzeug. Ein Agent kann seine Sammlung also nicht aus Versehen leeren,
  // indem er sie beim Schreiben vergisst.
  pi.registerTool({
    name: "state_write",
    label: "Zustand · schreiben",
    description:
      "Schreibt den Zustand eines Agenten nach _state/<agent>.json. Nur die " +
      "angegebenen Felder werden geändert, alles andere bleibt stehen. " +
      "Anzahl (count) und Zeitstempel werden automatisch gesetzt.",
    parameters: Type.Object({
      agent: StringEnum(AGENTS, { description: "Wessen Zustand geschrieben wird" }),
      last_seq: Type.Optional(
        Type.Number({ description: "Zuletzt verarbeitete Sequenznummer aus dem Bus" }),
      ),
      last_value: Type.Optional(
        Type.Number({ description: "Zuletzt erzeugter Wert (nur Counter)" }),
      ),
      numbers: Type.Optional(
        Type.Array(Type.Number(), {
          description: "Die vollständige gesammelte Zahlenliste (ersetzt die bisherige)",
        }),
      ),
      status: Type.Optional(
        StringEnum(["running", "paused", "stopped"] as const, {
          description: "Eigener Betriebszustand",
        }),
      ),
    }),
    async execute(_toolCallId, params) {
      const { agent, ...changes } = params;
      const state: AgentState = { ...readState(agent) };

      if (changes.last_seq !== undefined) state.last_seq = changes.last_seq;
      if (changes.last_value !== undefined) state.last_value = changes.last_value;
      if (changes.status !== undefined) state.status = changes.status;
      if (changes.numbers !== undefined) state.numbers = changes.numbers;
      if (state.numbers !== undefined) state.count = state.numbers.length;
      state.updated_at = now();

      const file = stateFile(agent);
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, `${JSON.stringify(state)}\n`, "utf8");
      return ok(state);
    },
  });
}
