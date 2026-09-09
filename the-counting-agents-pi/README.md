# The Counting Agents (pi)

Five agents count together. One produces numbers, three look at them, one runs
the show. They never talk to each other — they drop messages into a shared
file, and everyone reads what concerns them.

The demo runs in a Herdr tab with five panes and is built for an outreach
lecture: you watch agents work in real time, wait for each other, get paused
and start up again.

> German version: [readme_de.md](readme_de.md) — the demo itself is in German.

## What differs from `the-counting-agents`

The sister project does the same thing with the **OpenCode CLI** and a model
served locally through LM Studio. This one uses the **pi CLI** and a model in
the cloud — and above all: **its own tools**.

Under OpenCode the agents do their work through the generic `bash`, `read` and
`write` tools. They assemble JSON by hand, append it with `echo >>`, produce
timestamps, guard against empty files. What shows up in the pane is a shell
line.

Here every operation gets its own tool with a name that says what it does:

```
bus_publish {"value": 42}
```

Instead of:

```
bash echo '{"type":"number","seq":42,"value":42,"timestamp":"..."}' >> _bus/numbers.log
```

For an audience with no programming background, that is the whole difference.
And the agent prompts shrink from two pages of error handling to twelve lines
of task description.

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
```

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

## Running

From a Herdr pane, inside the project directory:

```bash
./scripts/start.sh
```

This creates the tab "Counting Agents (pi)" with five panes and starts an agent
in each. Focus lands on the steering pane.

| Command | Effect |
|---|---|
| `./scripts/start.sh` | Create tab, start agents |
| `./scripts/stop.sh` | Stop everything, close tab |
| `./scripts/reset.sh` | Clear bus and state |
| `./scripts/reset.sh --restart` | Clear and restart |

In the steering pane: arrow keys to select, Enter to run, `q` ends the demo.

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
- **Stretch the interval** — raise `interval` in the agents' frontmatter. At 20
  seconds the demo stays under 60 requests per minute, but it visibly drags.
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
