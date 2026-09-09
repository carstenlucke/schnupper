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
- A TensorX key for the model `qwen/qwen3.8-flash-next`

## Setup

```bash
cp .env.example .env
# fill in SCHNUPPER_TENSORX_API_KEY
```

The key belongs to this project alone. A TensorX account configured globally in
pi stays untouched: the demo registers the same endpoint under its own name
(`tensorx-schnupper`, see
[`.pi/extensions/tensorx-schnupper.ts`](.pi/extensions/tensorx-schnupper.ts)).
Lecture spending stays separate from everyday work, and the key can be revoked
on its own after the term.

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

## What an agent is

A text file. That's all.

```markdown
---
description: Erzeugt fortlaufende Zahlen und stellt sie in den Event-Bus
model: tensorx-schnupper/qwen/qwen3.8-flash-next
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

The `prime` agent is the only one with `thinking: low` — you should see it work
through a primality test while the others simply run.

## Further reading

- [`docs/pi-custom-tools.md`](docs/pi-custom-tools.md) — how the tools are built
  and how to add your own
- [`docs/experiment.md`](docs/experiment.md) — why the architecture looks the
  way it does
