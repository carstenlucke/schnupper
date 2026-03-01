# Release v0.1.0 — The Counting Agents

**Date:** 2026-03-01

The first release of *The Counting Agents* — a terminal-based demo of a multi-agent system in which autonomous LLM agents communicate via filesystem-based append-only event logs.

---

## Highlights

- **Five cooperating agents** run in parallel inside a tmux session: Counter, Odd, Even, Prime, and Control.
- **No infrastructure required** — all communication is performed through append-only JSONL files on the filesystem.
- **Fully observable** — each agent runs in its own tmux pane so decisions and processing are visible in real time.

---

## Agents

- **Counter** generates an ongoing sequence of numbers and writes them as events to the bus. It supports pause, resume, stop, and reset commands.
- **Odd** and **Even** filter odd and even numbers respectively from the event stream and accumulate them in their own state files.
- **Prime** detects prime numbers — intentionally slower (one event per cycle) to demonstrate visible speed differences between agents.
- **Control** displays a compact status dashboard and issues control commands to the other agents.

## Interactive Control

- The Control pane provides an interactive menu navigable with the arrow keys.
- Available actions: status dashboard, pause/resume, stop, reset, per-agent verbose/quiet modes, and free custom commands.

## Output Modes

- **Quiet mode** (default): concise, cycle-by-cycle summaries.
- **Verbose mode**: detailed output including processing metadata — toggled per agent via the Control menu.
- When many numbers are collected, the display is automatically shortened (first 3 + last 2 values).

## Scripts

- `start.sh` — creates the tmux session with all agents and initializes the bus and state directories.
- `stop.sh` — sends a stop event and cleanly terminates the session.
- `reset.sh` — clears logs and state. With `--restart` the session is restarted immediately.

## Documentation

- **README** with architecture diagram, quickstart guide, and event format reference.
- **Experiment documentation** (`docs/experiment.md`) describes the deliberate architectural choices and the questions the project explores.
- **Script documentation** (`docs/scripts.md`) contains details on all operation scripts.
- **Specification** for a planned shell-script variant without LLM dependencies.
