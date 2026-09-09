# The Counting Agents

A terminal-based demo of a multi-agent system. Autonomous LLM agents communicate via filesystem-based event logs and run inside a tmux session.

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
+--------------------+----------+
|     counter        | control  |
|      (2/3)         |  (1/3)   |
+----------+---------+----------+
|   odd    |  even   |  prime   |
|  (1/3)   |  (1/3)  |  (1/3)  |
+----------+---------+----------+
```

Each agent runs via `opencode run --agent <name>` inside a shell loop. Agent roles are defined as custom modes in `.opencode/modes/`.

## Prerequisites

- [tmux](https://github.com/tmux/tmux)
- [opencode](https://github.com/opencode-ai/opencode) CLI
- GitHub Copilot access (authenticated via `gh auth login`)

## Quickstart

```bash
# 1. Clone the repository
git clone <repo-url> && cd the-counting-agents

# 2. Start
./scripts/start.sh

# 3. Attach to the tmux session
tmux attach -t agents
```

## Control

The Control pane (top-right) shows an interactive menu navigable with the arrow keys. From there you can access the status dashboard, pause/resume, stop/reset, and send custom instructions.

```bash
# Stop the session from outside
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
│   ├── start.sh        # Start the tmux session
│   ├── stop.sh         # Stop the session
│   ├── reset.sh        # Reset state
│   ├── run-agent.sh    # Agent loop wrapper
│   └── run-control.sh  # Interactive control menu
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

The model can be changed in `opencode.json`:

```json
{
  "model": "github-copilot/gpt-4o"
}
```

## Variants

- **LLM variant** (default): Agents use `opencode` with LLM-based decisions
- **Shell variant** (planned): Pure Bash scripts without LLM — see `spec/Shell-Script-Variant-Spec.md`
