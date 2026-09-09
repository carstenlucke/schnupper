# Custom tools for pi

This demo brings its own tools. What that means, how they are built, and what
to keep in mind when extending them.

> Deutsche Fassung: [pi-custom-tools_de.md](pi-custom-tools_de.md)

## Why custom tools at all?

A language model cannot do anything by itself. It can produce text — and it can
ask to use a tool. Which tools exist is up to whoever runs it.

pi ships generic ones: `bash`, `read`, `write`, `edit`, `grep`, `find`, `ls`.
They can do everything and demonstrate nothing. When the counter agent
publishes a number, the audience sees:

```
bash echo '{"type":"number","seq":42,"value":42,"timestamp":"2026-09-09T21:15:03.412Z"}' >> _bus/numbers.log
```

With a custom tool it looks like this:

```
bus_publish {"value": 42}
```

The second difference matters more: **whatever a tool handles, the prompt no
longer has to explain.** In the OpenCode version of this project every agent
prompt carried half a page of error handling — don't open empty files with the
read tool, produce timestamps without milliseconds, never write absolute paths,
don't use `write` for log files. That was not a task description but an
operating manual for tools built for something else.

Now that care lives in code once, and the prompt describes the task.

## Where the tools live

pi loads extensions from several places:

| Location | Scope |
|---|---|
| `~/.pi/agent/extensions/*.ts` | everywhere |
| `.pi/extensions/*.ts` | this project only |

This demo uses the project-local one:

```
.pi/extensions/
├── counting-tools.ts       the six tools
└── tensorx-schnupper.ts    a model access of its own (optional)
```

TypeScript is loaded directly — no build step, no `node_modules` in the
project; pi brings the loader.

**Project-local extensions only run once the project is trusted.** That is a
security boundary: an extension can execute arbitrary code, so pi asks on the
first interactive start. In the non-interactive mode (`-p`) the agents run in,
nothing is asked — which is why the scripts pass `-a` to trust the project for
that single call.

## What a tool looks like

The heart of [`counting-tools.ts`](../.pi/extensions/counting-tools.ts),
abridged:

```typescript
import { Type } from "typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "bus_publish",
    label: "Bus · veröffentlichen",
    description:
      "Stellt eine Zahl als Ereignis in den Event-Bus (_bus/numbers.log). " +
      "Die fortlaufende Sequenznummer und der Zeitstempel werden automatisch vergeben.",
    parameters: Type.Object({
      value: Type.Number({ description: "Die zu veröffentlichende Zahl" }),
    }),
    async execute(_toolCallId, params) {
      // ... determine sequence number, append the line ...
      return { content: [{ type: "text", text: JSON.stringify(result) }], details: result };
    },
  });
}
```

Four things matter:

- **`name`** is what the model calls and what appears in the pane. Short and
  telling.
- **`description`** is not a comment for humans but the instruction manual for
  the model. It decides whether the tool gets used correctly. Whatever the tool
  does automatically belongs here — otherwise the model tries to do it itself.
- **`parameters`** describes the inputs as a schema. pi validates them before
  `execute` runs; wrong types never reach the code.
- **`execute`** returns text the model gets to see. Here: compact JSON — few
  tokens, unambiguous.

Descriptions and parameters are written in German because everything the model
reads in this demo is German, including the prompts.

## The six tools

| Tool | What it does |
|---|---|
| `bus_publish` | Appends a number to `_bus/numbers.log`; assigns sequence number and timestamp |
| `bus_read` | Returns events with `seq > since`, plus `latest_seq` and how many remain |
| `control_read` | Tells an agent what currently applies: `status`, `verbose`, `reset_requested` |
| `control_send` | Writes a control command to `_bus/control.log` |
| `state_read` | Reads `_state/<agent>.json`; `all` returns all four at once |
| `state_write` | Advances the state; sets `count` and `updated_at` itself |

Three design decisions are worth a look:

**The tools do no arithmetic.** Whether a number is even or prime is the
model's call. An `is_prime` tool would be more reliable — and would remove
exactly what the lecture is about. The tools do the bookkeeping, the model does
the work.

**`control_read` returns an answer, not raw material.** It could hand back the
lines from `control.log` and let the agent work it out: what applies when
"pause all" came first and "resume odd" later? That evaluation is always the
same and always error-prone, so it lives in code. The agent asks "what applies
to me?" and gets `{"status":"running",...}`.

**`state_write` only changes what it is given.** An agent that forgets its
collected numbers while writing does not lose them. That is deliberately
forgiving: a model that drops a field on the third run should not topple the
demo.

## Who gets which tool

Registered does not mean available. Which tools an agent gets is declared in
its frontmatter and becomes `--tools` in the pi call:

```yaml
tools: bus_read,control_read,state_read,state_write
```

Plus `-nbt` (`--no-builtin-tools`): no `bash`, no `read`, no `write`. The
collector agents cannot write to the bus — not because the prompt forbids it,
but because they lack the tool.

That is the point worth pausing on during the lecture: an agent is not the
model. An agent is a model **plus** a task **plus** a set of tools — and the
last ingredient decides what can happen at all.

## Adding a tool

1. Add another `pi.registerTool({...})` in `counting-tools.ts`.
2. Add a check for it in `scripts/test-tools.mjs` and run
   `node scripts/test-tools.mjs` — no model, no network, no cost.
3. List the tool name in the frontmatter of the agents allowed to use it.
4. Describe in the agent's prompt **when** to use it. The *how* belongs in the
   tool's `description`.

When an agent loops or calls the same tool over and over, the cause is almost
always the `description` — and almost never the prompt.

## Further reading

[`Trajectory.md`](Trajectory.md) shows how these tools actually get called
during a run, with a recorded trajectory.

pi's documentation ships with the installed package and is thorough:

```bash
open "$(dirname "$(dirname "$(readlink -f "$(which pi)")")")/../docs"
```

Relevant here: `extensions.md` (tools, events, commands), `custom-provider.md`
(custom model access) and `usage.md` (the flags the start scripts use).
