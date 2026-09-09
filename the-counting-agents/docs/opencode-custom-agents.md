# Opencode as a Custom Agent Platform

This document describes how [opencode](https://github.com/opencode-ai/opencode) can be used as a runtime for custom, specialized AI agents — and why it's worth doing.

## What is opencode?

Opencode is an open-source AI coding agent for the terminal. It provides an interactive TUI (Text User Interface) but can also be used non-interactively via the CLI. It is precisely this non-interactive usage that makes opencode an ideal platform for autonomous agents.

Official documentation: [opencode.ai/docs](https://opencode.ai/docs/)

## Why opencode for Custom Agents?

### No application code required

The key advantage: you don't need to write **any application code**. Agents are defined purely declaratively in Markdown — system prompt, allowed tools, model selection. Opencode handles the entire execution: model calls, tool usage, file access, shell commands.

### Built-in LLM integration

Opencode supports various LLM providers (Anthropic, OpenAI, GitHub Copilot, and others) and fully abstracts the integration. Switching models is a single line in the configuration.

### Built-in tool access

Every agent has access to powerful, built-in tools:
- **Bash** — Execute shell commands
- **Read** — Read files
- **Write** — Write files
- **Edit** — Edit files
- **Glob/Grep** — Search files

These tools can be enabled or disabled per agent to precisely control the agent's scope of action.

## Defining Custom Agents

There are two ways to define custom agents:

### 1. Markdown files (recommended)

Agents are stored as Markdown files with YAML frontmatter:

- **Per-project:** `.opencode/agents/` in the project directory
- **Global:** `~/.config/opencode/agents/`

Official documentation: [opencode.ai/docs/agents](https://opencode.ai/docs/agents/)

#### Example from this project

Here is how the Counter agent is defined in `.opencode/agents/counter.md`:

```markdown
---
description: Counter agent that generates sequential numbers into the event bus
model: github-copilot/gpt-4o
tools:
  bash: true
  read: true
  write: true
---

# Counter Agent

Du bist der **Counter-Agent** in einem Multi-Agent-System.
Deine einzige Aufgabe ist es, fortlaufende Zahlen zu erzeugen
und als Events in den Event-Bus zu schreiben.

## Dein Verhalten
1. State lesen: Lies `state/counter.json` ...
2. Control-Events prüfen: Lies `bus/control.log` ...
3. Wenn Status "running": Erhöhe `last_value` um 1 ...
...
```

The frontmatter defines the metadata, while the Markdown body serves as the system prompt.

### 2. JSON configuration in opencode.json

Alternatively, agents can be defined directly in `opencode.json`:

```json
{
  "agent": {
    "counter": {
      "description": "Counter agent that generates sequential numbers",
      "model": "github-copilot/gpt-4o",
      "prompt": "You are the Counter agent ...",
      "tools": {
        "bash": true,
        "read": true,
        "write": true
      }
    }
  }
}
```

Official documentation: [opencode.ai/docs/config](https://opencode.ai/docs/config/)

## Configuration Options

Each agent supports these options in the frontmatter or JSON configuration:

| Option | Description |
|--------|-------------|
| `description` | Short description of the agent (required) |
| `model` | Model override (e.g. `anthropic/claude-sonnet-4-5`) |
| `mode` | `primary`, `subagent`, or `all` |
| `prompt` | System prompt (Markdown body or text reference) |
| `temperature` | Response creativity (0.0–1.0) |
| `tools` | Enable/disable tool access |
| `permission` | Granular permissions (`ask`, `allow`, `deny`) |
| `steps` | Maximum iterations per invocation |

Official documentation: [opencode.ai/docs/agents](https://opencode.ai/docs/agents/)

## Running Agents

### Non-interactive (for automation)

The `opencode run` command executes an agent non-interactively — ideal for loops and scripts:

```bash
opencode run --agent counter "Execute your next step."
```

Official documentation: [opencode.ai/docs/cli](https://opencode.ai/docs/cli/)

### Key Flags

| Flag | Description |
|------|-------------|
| `--agent <name>` | Selects the agent to run |
| `--model <provider/model>` | Overrides the model |
| `--file <path>` | Attaches a file to the message |
| `--session <id>` | Continues an existing session |
| `--format <json\|text>` | Output format |

### Persistent Server (reduced latency)

For frequent invocations, a persistent server can be started that only initializes once:

```bash
# Start the server
opencode serve

# Run agents through the server
opencode run --attach http://localhost:4096 --agent counter "Execute your next step."
```

This avoids the cold start on every invocation — especially useful for fast agent cycles.

Official documentation: [opencode.ai/docs/cli](https://opencode.ai/docs/cli/)

## Permissions and Security

Opencode provides granular control over which tools an agent may use:

```json
{
  "agent": {
    "reviewer": {
      "permission": {
        "edit": "deny",
        "write": "deny",
        "bash": {
          "git *": "allow",
          "rm *": "deny"
        }
      }
    }
  }
}
```

This way, a review agent can read code but not modify it — a security principle that is especially important for autonomous agents.

## Practical Example: This Project

*The Counting Agents* uses opencode purely as an agent runtime. Five agents are defined as Markdown files in `.opencode/agents/` and are executed in loops via shell scripts:

```bash
# From scripts/run-agent.sh (simplified)
while true; do
    opencode run --agent "$AGENT_NAME" "Execute your next step."
    sleep "$INTERVAL"
done
```

The agents:
- **Read and write files** (event bus, state)
- **Execute shell commands** (appending to log files)
- **Make autonomous decisions** (based on their system prompt)
- **Coordinate with each other** (via the filesystem)

The result: a complete multi-agent system without a single line of application code.

## Ideas for Your Own Custom Agents

The mechanics are suitable for many scenarios beyond counting agents:

- **Code Reviewer** — Monitors a directory and provides feedback on changed files
- **Test Runner** — Executes tests and documents results
- **Documentation Generator** — Reads source code and updates documentation
- **Log Analyst** — Monitors log files and creates summaries
- **Deployment Agent** — Performs deployments according to defined rules

The key is to give the agent a clear role, defined file paths, and a consistent behavioral pattern through the system prompt.

## Further Reading

- [Opencode — Official Documentation](https://opencode.ai/docs/)
- [Opencode — Agents](https://opencode.ai/docs/agents/)
- [Opencode — CLI Reference](https://opencode.ai/docs/cli/)
- [Opencode — Configuration](https://opencode.ai/docs/config/)
- [Opencode — Rules (Custom Instructions)](https://opencode.ai/docs/rules/)
- [Opencode — GitHub Repository](https://github.com/opencode-ai/opencode)
