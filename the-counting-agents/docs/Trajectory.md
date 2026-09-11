# What actually happens during an agent run

One line appears in the pane: `→ 42`. This page explains what lies in between — the **trajectory**, the sequence of requests, tool calls and results that produces that single line.

> Deutsche Fassung: [Trajectory_de.md](Trajectory_de.md)

## The basic shape

A language model cannot do anything. It receives text and produces text. To turn that into an agent you need three ingredients and a loop:

1. **The system prompt** says who the agent is and what it should do — here, the text below the frontmatter in `agents/<name>.md`.
2. **The tool list** travels along as a schema: name, description and expected parameters of every permitted tool. That is how the model sees what it can ask for.
3. **The task** is the message that starts the run: "Führe deinen nächsten Schritt aus." (Take your next step.)

Then the loop runs: the model answers either with **text** — the run is over — or with a **tool call**. In the second case pi executes the tool, appends the result to the conversation and sends the whole thing to the model again. The model decides afresh at every step.

The crucial part: **the model executes nothing.** It phrases a request ("call `bus_publish` with `value: 1`"), and pi decides whether and how that request is carried out. This is exactly where the tool allowlist takes effect — what is not in `--tools` cannot even be asked for.

## A real trajectory

Recorded with `pi --mode json` during one run of the counter agent, trimmed to the essentials:

```
Request 1  →  model: toolCall control_read {"agent": "counter"}       762 in / 33 out
           ←  pi:    {"status":"running","verbose":false,"reset_requested":false}

Request 2  →  model: toolCall state_read {"agent": "counter"}         820 in / 18 out
           ←  pi:    {"agent":"counter","last_value":0,"status":"running",...}

Request 3  →  model: toolCall bus_publish {"value": 1}                868 in / 18 out
           ←  pi:    {"published":{"seq":1,"value":1}}

Request 4  →  model: toolCall state_write {"agent":"counter",...}     908 in / 32 out
           ←  pi:    {"agent":"counter","last_value":1,...,"updated_at":"..."}

Request 5  →  model: "→ 1"                                            989 in /  7 out
              no more tools, run complete
```

Four tool calls, **five requests to the model**, one line of output. The sequence comes from the prompt — but not as a list of tool names; it is a sentence: check for instructions; see where you left off; put the next number on the bus; remember how far you got. Which tool belongs to which clause the model works out from the tool descriptions. It follows the order because it is written there, not because anything forces it to.

You can count this yourself at any time:

```bash
pi -p --mode json -nc -nbt -a --no-session \
   --model "$COUNTING_AGENTS_MODEL" \
   --tools bus_publish,control_read,state_read,state_write \
   --system-prompt "$(sed '1,/^---$/d;1,/^---$/d' agents/counter.md)" \
   "Führe deinen nächsten Schritt aus." < /dev/null \
   | grep -c '"type":"turn_start"'
```

The `< /dev/null` matters: in print mode pi also reads standard input to append it to the task. Without the redirect the command waits for someone to type something — and looks like it has hung.

## Why every request costs more than the last

The model has no memory. For it to still know in request 4 what happened in request 1, **the entire conversation so far is sent along every time**: system prompt, tool schemas, task, all previous tool calls and their results.

```
Request 1:  system + tools + task
Request 2:  ... + call 1 + result 1
Request 3:  ... + call 1 + result 1 + call 2 + result 2
Request 4:  ... and so on
```

That is exactly what the numbers above show: input grows from 762 to 989 tokens while output stays small. For the single line `→ 1`, **4347 tokens are read and 108 written** — forty times as much input as output.

Two observations follow that land well in a lecture:

- **Short tool results are money.** Our tools answer with one line of compact JSON, not with whole files. A `bus_read` returning every event instead of only the new ones would be paid for again in every subsequent request.
- **The system prompt is paid for on every request.** A prompt with two pages of error handling costs not once but five times per run. Moving that care into the tools saved not only clarity but tokens.

Providers counter this with **prompt caching**: the unchanged beginning of the conversation is reused and billed cheaper. pi shows it as `cacheRead`.

## Every run starts from zero

The start scripts call pi with `--no-session`. Between two runs **nothing** of the conversation survives — no history, no memory.

What the agent still knows, it knows from two files: `_state/<agent>.json` tells it where it left off, `_bus/numbers.log` what happened meanwhile. Its memory sits on disk, not in the model — readable with `cat`, visible to everyone in the room.

That has a practical side effect: a run that crashes or gets killed leaves no wreckage behind. The next one reads the state and carries on.

## What can go wrong

| What you see in the pane | What is behind it |
|---|---|
| The agent describes what it would do instead of doing it | The model produced text instead of a tool call. A blunter prompt usually helps ("call the tools") |
| The same value keeps reappearing | The closing `state_write` is missing, so `last_seq` never advances |
| The run aborts after 60 seconds | The watchdog in `run-agent.sh` — the model is not answering or is going in circles |
| HTTP 429 | Rate limit. Five requests per run add up quickly; see "Counting requests" in the [README](../README.md) |

## pi's events

For a closer look, `--mode json` gives one event per line:

| Event | Meaning |
|---|---|
| `agent_start` / `agent_end` | Brackets around the whole run |
| `turn_start` / `turn_end` | One request to the model — this is what you count |
| `message_start` / `message_update` / `message_end` | The answer, streaming and then complete |
| `tool_execution_start` / `tool_execution_end` | pi executes a tool |

Counting `turn_start` is the most honest measure of what an agent actually costs.

## Further reading

- [`pi-custom-tools.md`](pi-custom-tools.md) — how the tools called here are built
- [`experiment.md`](experiment.md) — why the architecture looks the way it does
