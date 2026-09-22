# The Counting Agents (pi)

Five agents count together. One produces numbers, three look at them, one runs
the show. They never talk to each other — they drop messages into a shared
file, and everyone reads what concerns them.

The demo runs in a Herdr tab with five panes and is built for an outreach
lecture: you watch agents work in real time, wait for each other, get paused
and start up again.

> German version: [readme_de.md](readme_de.md) — the demo itself is in German.

## Custom tools instead of generic ones

The demo runs on the **pi CLI** with a model in the cloud — and above all with
**its own tools**.

pi ships generic tools: `bash`, `read` and `write`. The demo could be built on
them, too. The agents would then assemble JSON by hand, append it with
`echo >>`, produce timestamps, guard against empty files. What would show up in
the pane is a shell line.

Here every operation gets its own tool with a name that says what it does:

```
bus_publish {"value": 42}
```

Instead of:

```
bash echo '{"type":"number","seq":42,"value":42,"timestamp":"..."}' >> _bus/numbers.log
```

For an audience with no programming background, that is the whole difference.
And the agent prompts get by with twelve lines of task description instead of
two pages of error handling.

Second difference: the agents have **no** built-in tools. No `bash`, no `read`,
no `write`. Each can do exactly what its role requires — the counter may
publish, the collectors may only read. That is demonstrable on stage: take a
tool away from an agent and watch what happens.

## Layout

```
+--------------------+----------+
|  counter · numbers | control ·|
|                    |  steering|
+----------+---------+----------+
|   odd ·  | even ·  | prime ·  |
|   odds   |  evens  |  primes  |
+----------+---------+----------+
|      dashboard · overview     |
+-------------------------------+
```

The five upper panes are the agents. The strip at the bottom starts the
dashboard for the projector and prints nothing but its address — see
[The dashboard](#the-dashboard).

| Agent | Job | Tools |
|---|---|---|
| `counter` | Produces sequential numbers | `bus_publish`, `control_read`, `state_read`, `state_write` |
| `odd` | Collects the odd ones | `bus_read`, `control_read`, `state_read`, `state_write` |
| `even` | Collects the even ones | `bus_read`, `control_read`, `state_read`, `state_write` |
| `prime` | Tests for primes, one per run | `bus_read`, `control_read`, `state_read`, `state_write` |
| `control` | Shows state, sends commands | `state_read`, `bus_read`, `control_send` |

Communication happens through two append-only files:

- `_bus/numbers.log` — the numbers the counter publishes
- `_bus/control.log` — control commands (pause, resume, stop, reset, verbose, quiet)

What each agent remembers lives in `_state/<agent>.json`.

Both directories start with an underscore: they only come into existence at
runtime, do not belong in the repository, and sort themselves above the
directories you actually edit.

## Requirements

- [Herdr](https://herdr.dev) — the demo runs in a Herdr tab
- [pi](https://pi.dev) — the agent runtime (`pi --version`)
- A model pi can reach. The default is `openai-codex/gpt-5.6-luna` (ChatGPT
  subscription, set up once in pi via `/login`). `pi --list-models` shows what
  else is available.

## Setup

```bash
cp .env.example .env
```

One line in the `.env` matters:

```
COUNTING_AGENTS_MODEL=openai-codex/gpt-5.6-luna
```

It overrides the `model:` entry in the agent files and applies to all five at
once. When a provider slows down mid-lecture or a rate limit hits, change this
one line and restart the demo.

Not every model in `pi --list-models` is actually cleared for use —
`gpt-5.4-mini`, for one, is refused by Codex on a ChatGPT account. So start the
demo once before the lecture and watch for numbers appearing.

**TensorX as an alternative:** if `COUNTING_AGENTS_MODEL` names a
`tensorx-schnupper/...` model, the `.env` also needs
`SCHNUPPER_TENSORX_API_KEY`. That key belongs to this project alone; a TensorX
account configured globally in pi stays untouched, because the demo registers
the same endpoint under its own name (see
[`.pi/extensions/tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts)).
Lecture spending stays separate from everyday work.

Before the lecture, check that the tools do what they should — no model, no
network, no cost:

```bash
node scripts/test-tools.mjs
```

Editing the extensions in an editor shows red errors there: the project
deliberately ships no `node_modules`, so the editor cannot find the imported
packages. This does not bother pi — it resolves the imports with its own
TypeScript loader. One call links the packages the installed pi CLI already
carries; nothing is downloaded, nothing enters the repository:

```bash
./scripts/dev-typen.sh
```

## Running

From a Herdr pane, inside the project directory:

```bash
./scripts/start.sh
```

This creates the tab "Counting Agents (pi)", starts an agent in each of the five
upper panes and, in the strip below them, the dashboard, which opens in the
browser by itself. Focus lands on the steering pane.

| Command | Effect |
|---|---|
| `./scripts/start.sh` | Create tab, start agents and dashboard |
| `./scripts/start.sh --ohne-dashboard` | The five agent panes only |
| `./scripts/start.sh --speed 1.5` | One-and-a-half times the pace, `0.5` half |
| `./scripts/stop.sh` | Stop everything, close tab |
| `./scripts/reset.sh` | Clear bus and state |
| `./scripts/reset.sh --restart` | Clear and restart (passes `--speed` through) |

In the steering pane: arrow keys to select, Enter to run, `q` ends the demo.

**Pace.** `--speed` compresses or stretches the interval of all agents at once,
without touching a file: `--speed 2` halves the wait between two runs,
`--speed 0.5` doubles it. All agents share the same interval and are compressed
or stretched together; `prime` still falls behind, but because it thinks, not
because of its interval. The same works through `AGENT_SPEED` in the environment
or in the `.env`; a factor given on the command line wins. In the lecture hall this
is the lever against rate limits (see
[Counting requests](#counting-requests-why-rate-limits-bite-so-quickly)) and against
a bus that scrolls faster than you can talk.

## The dashboard

The agent panes show every single step — that is the point, but from the back
row it is a lot of text. The dashboard shows the overview alongside:

```bash
./scripts/dashboard.py            port 8777, opens the browser
./scripts/dashboard.py 9000       different port
./scripts/dashboard.py --kein-browser
```

It reads the bus and the state files and never writes, so it cannot disturb the
demo. The server pushes changes over Server-Sent Events; the browser never polls
on its own. Standard library only, no build.

**The number band.** Each tile is one number from the bus. Its colour says who
has already collected it:

| Colour | Meaning |
|---|---|
| grey | nobody yet |
| light blue | `odd` has it |
| green | `even` has it |
| gold ring | is a prime |
| gold dot, filled | `prime` has it |
| red | sorted wrongly |

Red is the interesting case: the dashboard recomputes which numbers are prime.
If the prime agent collects one that isn't, it shows. That does not happen on
every run, but when it does it is the best moment of the lecture — the model got
it wrong, and you can see it.

**Click an agent.** Clicking an agent row dims every tile that isn't its own;
only that agent's numbers stay. It lets you explain one collector at a time
without the others competing for attention. Click again to release.

**Lag.** Each agent row shows how far its collector trails the counter. The
panes don't show that, and it is the actual punchline: all four share the same
interval and still do not run in lockstep — `prime` slowest, because it thinks.

Colours and layout follow the [THM corporate design](https://go.thm.de/cd):
dark header bar with the logo mark, section titles with a green underline,
cards with a coloured edge on the left. The dark theme is the default because
a projector is darker than any screen; the button in the header switches to
the light theme, and the browser remembers the choice. The page loads the
Barlow typeface from Google Fonts — without a network the system font stack
takes over and everything stays usable.

**Dress rehearsal without a model.** Before the lecture you can check the
dashboard without running agents and spending tokens:

```bash
./scripts/dashboard-probelauf.py     in one pane
./scripts/dashboard.py               in another
```

The simulator counts up, lets the collectors trail by different amounts, pauses
`prime` in between and occasionally picks up the wrong number. It writes to the
same files as the real agents, so it must not run alongside
`./scripts/start.sh`.

## Counting requests: why rate limits bite so quickly

An agent run is **not one request to the model** but one per tool call plus one
for the closing answer. The counter calls `control_read`, `state_read`,
`bus_publish` and `state_write` — measured, that is five model requests for the
single line `→ 42` that shows up in the pane.

Extrapolated to the running demo: four agents in a loop, a run takes about ten
seconds, plus three seconds of interval — roughly **90 requests per minute**.

At [TensorX](https://docs.tensorx.ai/api-reference/rate-limits) the standard
allowance is 60 requests per minute per key. So the demo runs straight into a
limit, visible as HTTP 429 with `"reason": "rate_limit_requests"`.

There is a second trap that is easy to miss: TensorX reserves as many tokens per
request as `max_tokens` announces, no matter how short the answer turns out. At
the catalog value of 32768, the two-million-token minute budget would be spent
after 61 requests. That is why
[`tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts) deliberately
announces only 4096 — plenty for one line of output.

What helps when a limit hits:

- **Switch providers** — one `COUNTING_AGENTS_MODEL` line in the `.env`. That is
  why the default runs on a subscription model rather than TensorX.
- **Stretch the interval** — `./scripts/start.sh --speed 0.15` at startup, or
  raise `interval` in the agents' frontmatter for good. At 20 seconds the demo
  stays under 60 requests per minute, but it visibly drags.
- **Run fewer agents** — for some parts of the talk, counter and prime suffice.

For the lecture the arithmetic itself is a good moment: five agents, each
printing a single line, produce around a hundred requests per minute. You see
one number in the pane — behind it are five conversations with a model.

## What an agent is

A text file. That's all.

```markdown
---
description: Erzeugt fortlaufende Zahlen und stellt sie in den Event-Bus
model: openai-codex/gpt-5.6-luna
tools: bus_publish,control_read,state_read,state_write
thinking: off
interval: 3
---

# Counter-Agent

Du bist der **Counter**. Du erzeugst fortlaufende Zahlen — sonst nichts.
...
```

The header says which model does the thinking, which tools are allowed, how
often the agent runs and whether it may reason. Below it, in plain German, what
it should do. `scripts/run-agent.sh` reads the file and assembles the pi call.

When the `.env` sets `COUNTING_AGENTS_MODEL`, it applies to all five agents and
overrides their frontmatter entry.

The `prime` agent is the only one with `thinking: low` — you should see it work
through a primality test while the others simply run.

## Further reading

- [`docs/Trajectory.md`](docs/Trajectory.md) — what actually happens during a
  run: requests, tool calls, growing context
- [`docs/pi-custom-tools.md`](docs/pi-custom-tools.md) — how the tools are built
  and how to add your own
- [`docs/experiment.md`](docs/experiment.md) — why the architecture looks the
  way it does
