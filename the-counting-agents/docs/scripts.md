# Scripts Documentation

All scripts are located in `scripts/` and implemented as executable Bash scripts with `set -euo pipefail`.

## start.sh

Creates the Herdr tab **Counting Agents** with 5 panes in the current workspace (see layout in the README). Must be run from inside a Herdr pane — the script picks up the workspace from `$HERDR_WORKSPACE_ID`.

**What happens on startup:**
1. Checks that the script runs inside Herdr (`$HERDR_ENV`) and that `herdr` and `opencode` are installed
2. Runs `start-lmstudio.sh` (skip with `SKIP_LMSTUDIO=1`)
3. Closes an existing **Counting Agents** tab if one is present
4. Creates `bus/` and `state/` directories and clears the log files
5. Initializes state files (`state/*.json`) with default values
6. Builds the layout with `herdr pane split` (Counter + Control in the top row, Odd/Even/Prime in the bottom row)
7. Names every pane after the agent it hosts via `herdr pane rename`:
   - `counter · Zähler` (top-left, 2/3 wide)
   - `control · Steuerung` (top-right, 1/3 wide)
   - `odd · Ungerade`, `even · Gerade`, `prime · Primzahlen` (bottom row, each 1/3 wide)
8. Starts the agents with `herdr pane run`: `run-control.sh` in the Control pane, `run-agent.sh <name> <interval>` in the other four
9. Brings the tab to the front with `herdr tab focus`, with the Control pane focused

Run it from a pane **outside** the demo tab — the script refuses to close the tab it is running in itself.

**Usage:**
```bash
./scripts/start.sh
```

## stop.sh

Stops all agents and closes the Herdr tab.

1. Writes a `{"command":"stop","target":"all"}` event to `bus/control.log`
2. Waits 2 seconds to allow agents to pick up the stop event
3. Closes the **Counting Agents** tab (outside Herdr it stops after step 2 and says so)

**Usage:**
```bash
./scripts/stop.sh
```

## reset.sh

Clears logs and state files.

1. Empties `bus/numbers.log` and `bus/control.log`
2. Deletes all state files (`state/*.json`)

With `--restart` the demo tab is also closed and started again.

**Usage:**
```bash
./scripts/reset.sh            # Reset only
./scripts/reset.sh --restart  # Reset + restart
```

## start-lmstudio.sh

Brings the local model online. Called by `start.sh`, but worth running on its own
before a lecture — loading a cold model takes long enough to be awkward on stage.

1. Starts the LM Studio server unless it is already running (`lms server start`)
2. Downloads the model on first use (`lms get`)
3. Loads it into memory unless it is already loaded **with the required context and parallelism** (`lms load`) — a model left over from an earlier run with a smaller context is unloaded and reloaded

Each step is idempotent, so repeated calls are cheap.

**Environment variables:**
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

**Usage:**
```bash
./scripts/start-lmstudio.sh
```

## herdr-lib.sh

Shared helpers for `start.sh` and `stop.sh`, included via `source` — not meant to be run directly.

- `herdr_require` — verifies that `herdr` is installed and that the caller sits in a Herdr pane
- `herdr_demo_tab_id` — looks up the tab ID of the **Counting Agents** tab in the current workspace
- `herdr_split` — splits a pane and returns the new pane ID

The Herdr CLI answers in single-line JSON, which is parsed here with `tr`/`grep`/`sed`. No `jq` required.

## run-agent.sh

Generic loop wrapper for the filter agents (counter, odd, even, prime).

**Parameters:**
- `$1` — Agent name (e.g. `counter`, `odd`)
- `$2` — Interval in seconds (default: 3)

**Behavior:**
1. Before each cycle, checks whether a stop command for `all` or the agent's own name is present in `bus/control.log`
2. Points `XDG_DATA_HOME` at `.opencode-data/<agent>`, giving every agent its own opencode database. Sharing the default one in `~/.local/share/opencode` makes four of the five processes abort immediately with `database is locked`, because they all write to the same SQLite file. `start.sh` clears the directory on each start.
3. Calls `opencode run --agent <name> "Execute your next step."`
4. Aborts the cycle after `COUNTING_AGENTS_TIMEOUT` seconds (default 240) — a local model occasionally leaves `opencode` hanging, and without the watchdog the pane would sit dead for the rest of the demo. With all five agents asking at once a cycle measures 85–115 seconds, so the limit has to sit well above that or it would cut off normal operation
5. Waits the configured interval, then starts the next cycle

**Usage:**
```bash
./scripts/run-agent.sh counter 3
./scripts/run-agent.sh prime 5
```

## run-control.sh

Interactive control menu for the Control pane. Replaces the generic `run-agent.sh` wrapper for the control agent.

**Menu items:**
| # | Action | Implementation |
|---|--------|----------------|
| 1 | Show status dashboard | `opencode run --agent control` |
| 2 | Pause counter | Writes directly to `bus/control.log` |
| 3 | Resume counter | Writes directly to `bus/control.log` |
| 4 | Stop all agents | Writes directly to `bus/control.log` |
| 5 | Reset all agents | Writes directly to `bus/control.log` |
| 6 | Toggle verbose/quiet | Submenu: choose agent + mode, then writes to `bus/control.log` |
| 7 | Enter custom instruction | Free text input, forwarded to `opencode run --agent control` |

**Navigation:**
- Arrow keys up/down: move selection
- Enter: execute action
- `q`: exit menu

**Design decision:** Simple commands (pause, resume, stop, reset, verbose, quiet) are written directly via `echo` to `bus/control.log` without an LLM call. Only the status dashboard and custom instructions use `opencode run`.
