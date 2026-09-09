# Specification: Terminal-Based Multi-Agent Demo (LLM-Driven, No Custom Code)

## 1. Purpose and Motivation

This project specifies a **terminal-based demonstration of multi-agent systems** designed primarily for **teaching and conceptual understanding**, not for production use.

The core motivation is to:
- make agent-based systems tangible and observable,
- demonstrate coordination, communication, state, and control,
- avoid traditional programming by using LLM-driven agents (e.g. OpenCode with Codex),
- rely on standard Unix tools and the filesystem as the communication substrate.

---

## 2. Conceptual Model

An agent is defined as:
- an independent terminal process,
- started with a system prompt defining its role and goals,
- capable of reading shared artifacts and appending new ones,
- isolated from direct calls to other agents.

All interaction happens via shared communication artifacts.

---

## 3. High-Level Architecture

- Each agent runs in its own tmux pane.
- Communication uses append-only event logs (JSON Lines).
- State is stored explicitly in per-agent state files.

---

## 4. Repository Structure

```
agentsim/
├── bus/
│   ├── numbers.log
│   ├── control.log
├── agents/
│   ├── counter/
│   ├── odd/
│   ├── even/
│   ├── prime/
│   └── control/
├── state/
└── scripts/
```

---

## 5. Communication Model

All communication follows an event sourcing model.

### Number Event
```json
{"type":"number","seq":1,"value":1}
```

### Control Event
```json
{"type":"control","target":"counter","command":"pause"}
```

---

## 6. Agents and Responsibilities

### Counter Agent
- Produces increasing numbers
- Writes to numbers.log
- Reads control.log

### Odd / Even Agents
- Read numbers.log
- Filter values
- Persist state

### Prime Agent
- Detects prime numbers
- Operates slower intentionally

### Control Agent
- Reads user input
- Writes control events

---

## 7. Execution Flow

1. Initialize logs
2. Start tmux
3. Launch agents
4. Observe interaction

---

## 8. Constraints

- No custom programming
- Append-only logs
- Human-readable artifacts

---

## 9. Acceptance Criteria

- Agents run concurrently
- Behavior is observable
- State persists across restarts
