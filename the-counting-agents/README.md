# The Counting Agents

A terminal-based demo of a multi-agent system. Autonomous LLM agents communicate via filesystem-based event logs and run side by side in a [Herdr](https://herdr.dev) tab — one named pane per agent.

## Concept

Five agents work together:

- **Counter** — Generates a sequential stream of numbers and writes them to the event bus
- **Odd** — Filters and collects odd numbers
- **Even** — Filters and collects even numbers
- **Prime** — Detects prime numbers (intentionally slower)
- **Control** — Displays a status dashboard and sends control commands

Agents communicate exclusively through append-only JSONL files in the `bus/` directory. Each agent persists its state in `state/`.

## Architecture

```
+-------------------------------------------+---------------------+
|             counter · Zähler              | control · Steuerung |
|                   (2/3)                   |        (1/3)        |
+---------------------+---------------------+---------------------+
|   odd · Ungerade    |    even · Gerade    | prime · Primzahlen  |
|        (1/3)        |        (1/3)        |        (1/3)        |
+---------------------+---------------------+---------------------+
```

Each agent runs via `opencode run --agent <name>` inside a shell loop. Agent roles are defined as custom modes in `.opencode/modes/`.

`start.sh` builds this layout in the current Herdr workspace as a tab named **Counting Agents** and labels every pane after the agent it hosts.

## Prerequisites

- [Herdr](https://herdr.dev) — the demo must be started from inside a Herdr pane
- [opencode](https://github.com/opencode-ai/opencode) CLI
- [LM Studio](https://lmstudio.ai) with its `lms` CLI on the `PATH` — the agents run against a local model, no cloud account needed

## Quickstart

```bash
# 1. Clone the repository
git clone <repo-url> && cd the-counting-agents

# 2. Start Herdr and open a pane in this directory
herdr

# 3. Start the demo — it opens the "Counting Agents" tab and focuses it
./scripts/start.sh
```

`start.sh` calls `scripts/start-lmstudio.sh` first: it starts the LM Studio
server, downloads the model on first run, and loads it into memory. Run that
script once before a lecture so the first agent cycle does not wait on a cold
model.

## Control

The Control pane (top-right) shows an interactive menu navigable with the arrow keys. From there you can access the status dashboard, pause/resume, stop/reset, and send custom instructions.

```bash
# Stop from another pane (also closes the demo tab)
./scripts/stop.sh

# Clear state and logs
./scripts/reset.sh

# Reset + restart
./scripts/reset.sh --restart
```

Detailed script documentation: [docs/scripts.md](docs/scripts.md)

Background on the experiment and deliberate architectural decisions: [docs/experiment.md](docs/experiment.md)

Using opencode as a custom agent platform: [docs/opencode-custom-agents.md](docs/opencode-custom-agents.md)

## Directory Structure

```
the-counting-agents/
├── .opencode/modes/    # Agent definitions (custom modes)
│   ├── counter.md
│   ├── odd.md
│   ├── even.md
│   ├── prime.md
│   └── control.md
├── opencode.json       # opencode configuration
├── bus/                # Event bus (JSONL files)
│   ├── numbers.log     # Number events
│   └── control.log     # Control events
├── state/              # Agent state (JSON)
├── scripts/            # Shell scripts (details: docs/scripts.md)
│   ├── start.sh          # Open the Herdr tab and start all agents
│   ├── start-lmstudio.sh # Start the LM Studio server and load the model
│   ├── stop.sh           # Stop the agents and close the tab
│   ├── herdr-lib.sh      # Shared Herdr CLI helpers
│   ├── reset.sh          # Reset state
│   ├── run-agent.sh      # Agent loop wrapper
│   └── run-control.sh    # Interactive control menu
└── spec/               # Specifications
```

## Event Formats

### Number Event (bus/numbers.log)
```json
{"type":"number","seq":1,"value":1,"timestamp":"2025-01-01T00:00:00Z"}
```

### Control Event (bus/control.log)
```json
{"type":"control","target":"all","command":"stop","timestamp":"2025-01-01T00:00:00Z"}
```

## Configuration

The agents run against [Qwen3.6 35B-A3B](https://lmstudio.ai/models/qwen/qwen3.6-35b-a3b),
served locally by LM Studio over its OpenAI-compatible API. It is a mixture-of-experts
model: 35B parameters in total, only 3B active per token, so it stays fast while
handling the multi-step tool chains these agents need. The provider and the
model are configured in `opencode.json`:

```json
{
  "model": "lmstudio/qwen/qwen3.6-35b-a3b",
  "provider": {
    "lmstudio": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://127.0.0.1:1234/v1" },
      "models": { "qwen/qwen3.6-35b-a3b": { "name": "Qwen3.6 35B-A3B (local)" } }
    }
  }
}
```

Every agent repeats the same model in its front matter (`.opencode/agents/*.md`)
and can therefore be pointed at a different one individually.

`scripts/start-lmstudio.sh` reads four environment variables, which is the
quickest way to try another local model:

| Variable | Default | Meaning |
|---|---|---|
| `COUNTING_AGENTS_MODEL` | `qwen/qwen3.6-35b-a3b` | LM Studio model key |
| `COUNTING_AGENTS_PARALLEL` | `5` | Concurrent predictions — one per agent |
| `COUNTING_AGENTS_CONTEXT_PER_AGENT` | `16384` | Context one agent cycle may use |
| `COUNTING_AGENTS_CONTEXT` | *per-agent × parallel* (`81920`) | Total context of the model |

`--context-length` sizes the **whole** model, and LM Studio divides it among the
parallel slots. A single cycle measures a good 10,000 tokens, so 16k spread
across five agents leaves roughly 3k each and every cycle dies with "Context
size has been exceeded". That is why the total is calculated rather than fixed.

Changing the model here also means changing it in `opencode.json` and in the
agent front matter.

## Variants

- **LLM variant** (default): Agents use `opencode` with LLM-based decisions
- **Shell variant** (planned): Pure Bash scripts without LLM — see `spec/Shell-Script-Variant-Spec.md`
