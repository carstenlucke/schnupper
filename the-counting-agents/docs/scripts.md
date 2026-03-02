# Scripts Documentation

All scripts are located in `scripts/` and implemented as executable Bash scripts with `set -euo pipefail`.

## start.sh

Creates and starts the tmux session `agents` with 5 panes (see layout in the README).

**What happens on startup:**
1. Checks that `tmux` and `opencode` are installed
2. Terminates any existing session with the same name
3. Creates `bus/` and `state/` directories and clears the log files
4. Initializes state files (`state/*.json`) with default values
5. Builds the tmux layout (Counter + Control in the top row, Odd/Even/Prime in the bottom row)
6. Starts the agents:
   - Pane 0: Counter (top-left, 2/3 wide)
   - Pane 1: Control (top-right, 1/3 wide) via `run-control.sh`
   - Panes 2–4: `run-agent.sh <name> <interval>` for odd, even, prime (bottom row, each 1/3 wide)

**Usage:**
```bash
./scripts/start.sh
tmux attach -t agents
```

## stop.sh

Stops all agents and terminates the tmux session.

1. Writes a `{"command":"stop","target":"all"}` event to `bus/control.log`
2. Waits 2 seconds to allow agents to pick up the stop event
3. Kills the tmux session `agents`

**Usage:**
```bash
./scripts/stop.sh
```

## reset.sh

Clears logs and state files.

1. Empties `bus/numbers.log` and `bus/control.log`
2. Deletes all state files (`state/*.json`)

With `--restart` the session is also stopped and restarted.

**Usage:**
```bash
./scripts/reset.sh            # Reset only
./scripts/reset.sh --restart  # Reset + restart
```

## run-agent.sh

Generic loop wrapper for the filter agents (counter, odd, even, prime).

**Parameters:**
- `$1` — Agent name (e.g. `counter`, `odd`)
- `$2` — Interval in seconds (default: 3)

**Behavior:**
1. Before each cycle, checks whether a stop command for `all` or the agent's own name is present in `bus/control.log`
2. Calls `opencode run --agent <name> "Execute your next step."`
3. Waits the configured interval, then starts the next cycle

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
