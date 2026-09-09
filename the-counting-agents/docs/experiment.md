# The Experiment: Why So Scrappy?

## What is this about?

This project is an **experiment**, not a production system. The central question is:

> How far can you get with a multi-agent system that requires **virtually no programming effort** to build?

The entire project consists of Markdown definitions for the agents, a handful of shell scripts, and JSON files. No framework, no library, no custom code implementing business logic — the LLM agents **are** the logic. The setup demonstrates that coordinated autonomous agents can be realized today with minimal effort.

At the same time, this is a **hands-on evaluation of specific tools**: [opencode](https://github.com/opencode-ai/opencode) as the CLI for agent execution and [tmux](https://github.com/tmux/tmux) as a runtime environment that makes multiple agents visible in parallel. Both tools are deliberately tested here for their suitability in multi-agent scenarios.

This leads to a second question:

> Can these agents coordinate meaningfully through a filesystem — without a message broker, without infrastructure?

The answer to both questions is: Yes, for certain scenarios. And showing exactly that is the purpose of this project.

## Deliberate Decisions, Not Oversights

Every piece of "technical debt" in this project is a deliberate decision. Here are the key ones:

### Reading Log Files in Full

The consumer agents (odd, even, prime) read the **entire `bus/numbers.log` on every cycle** and filter in memory for `seq > last_seq`.

**What a real message queue would do differently:**
- Consumers read only new messages from a server-managed offset
- Backpressure and flow control are built in
- Delivery guarantees (at-least-once, exactly-once) are part of the protocol
- Scaling is O(1) per message, not O(n) per read cycle

**Why we do it this way regardless:**
- Maximum transparency — `cat bus/numbers.log` shows the complete system state
- No additional process (broker) needed that must run and be monitored
- Debugging is trivial: read the files, done
- The data volume is irrelevant in this demo context (hundreds of lines, not millions)

### No Acknowledgements, No Locking

There is no mechanism guaranteeing that a message is processed exactly once. An agent could crash between reading and updating its state — and on restart process messages twice or skip them entirely.

**Why this is OK here:** The agents count numbers. A missed or duplicated value is not data loss — it is an observation.

### Append-Only Without Rotation

The log files grow without limit. There is no log rotation, no compaction, no cleanup.

**Why this is OK here:** A `./scripts/reset.sh` resets everything. The system runs for minutes to hours, not weeks.

### No Schema Registry, No Versioning

The event formats are defined implicitly in the agent definitions, not in a central schema.

**Why this is OK here:** Five agents, two event types, one developer. The complexity of schema management would overshadow the actual purpose of the experiment.

## What the Experiment Shows

### 1. LLM Agents Need Less Infrastructure Than You Think

An `echo '...' >> file.log` is sufficient as a communication channel. The agents are robust enough to work reliably with this primitive mechanism.

### 2. Event Sourcing Works With Files Too

The pattern — immutable events, consumers derive their state from them — is architecturally sound. Whether the storage is a filesystem or Kafka does not change the principle.

### 3. The Limits Become Visible

The prime agent intentionally lags behind. This is precisely what makes differences in processing speed observable — something that would disappear behind abstractions in a real queue.

## What This Project Is Not

- **Not an architecture template** for production systems
- **Not proof** that you don't need message queues
- **Not a best practice** for agent communication

It is an experiment that shows how little infrastructure autonomous agents need at minimum — and where the limits of that minimalism lie.

## When You Should Do It Differently

As soon as any of these criteria apply, file-based communication is no longer sufficient:

- **Long-running systems**: The system should run for days or weeks → log rotation, compaction
- **Many consumers**: More than a handful of agents reading the same bus → broker with fan-out
- **Reliability**: Message loss is not tolerable → acknowledgements, idempotency
- **Distributed systems**: Agents run on different machines → network-capable broker
- **Scale**: Thousands of events per second → Kafka, Redis Streams, NATS
