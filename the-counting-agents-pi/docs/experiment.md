# The experiment: what this version does differently

This project exists twice. `the-counting-agents` runs on the OpenCode CLI with
a model on your own machine; this version runs on the pi CLI with a model in
the cloud and tools of its own. Both show the same thing: five agents
collaborating through files.

The comparison is the actual yield. What changes when agents get fitting tools
instead of generic ones?

> Deutsche Fassung: [experiment_de.md](experiment_de.md)

## The starting observation

In the OpenCode version, more than half of every agent prompt consists of
instructions that have nothing to do with the task:

- produce timestamps with `date -u +%Y-%m-%dT%H:%M:%SZ`, because BSD `date`
  does not know the millisecond format
- do not open empty files with the read tool, because that triggers an offset
  error
- write log files with `bash` and `echo >>`, never with `write`, because
  `write` replaces the file
- no absolute paths, no leading slashes
- always read `bus/numbers.log` in full, because the read tool's offset counts
  lines, not sequence numbers

Every one of those lines is there because a run once failed on it. They are not
wrong — they are merely in the wrong place. This is knowledge about tools,
stored in a prompt, repeated across five files, and every model has to read and
obey it on every single run.

## The counter-test

In this version that knowledge sits in the tools' code, once. The odd agent's
prompt is thirty lines afterwards and contains only what it should do — with a
single rule about mechanics: the run ends with `state_write`.

What becomes visible:

### Errors move from runtime into design

An agent can no longer open an empty file incorrectly, because it does not open
files at all. What remains are errors of a different kind: a tool called at the
wrong time, or not at all. That is the more interesting sort — it is about the
task, not about the toolbox.

And it can be fixed without changing models. When the local model skipped the
closing `state_write` during a test run, no better model was needed — one
sentence in the prompt explaining why that call is not optional was.

### Taking something away beats forbidding it

The collector agents must not write to the bus. In the OpenCode version that is
a rule in the prompt — and a model that goes off the rails can break it,
because `bash` is right there. Here they simply lack the tool.
`--no-builtin-tools` removes `bash`, `read` and `write`; `--tools` grants
exactly four names.

For the lecture this is the most tangible point: an agent is not the same as a
model. An agent is a model, a task and a toolbox — and the toolbox decides what
can happen at all.

### Bookkeeping does not belong in the model

Assigning sequence numbers, setting timestamps, counting lists, determining the
control command currently in force: these have exactly one right answer. A
language model usually finds it — and usually is not enough when a run starts
every three seconds and a lecture hall is watching.

The line runs where things get interesting: whether 91 is prime remains the
model's call. An `is_prime` tool would be more reliable and would rob the demo
of its subject.

## What stayed the same

The architecture. Both versions share the decisions argued in
`the-counting-agents/docs/experiment.md`:

- **Two files as the bus**, append-only. No broker, no queue, no network. You
  can read them with `cat` — invaluable on stage.
- **No locking, no acknowledgements.** Each agent remembers how far it has
  read and picks up the rest next time. Miss a run, catch up later.
- **No cleanup, no rotation.** A demo lasts 90 minutes; the files stay small.
- **The prime agent is deliberately slow.** One number per run, so the pane
  shows it falling behind while the others carry on.

## What this version costs

Honesty is part of it: the model now runs in the cloud. That is fast — a run
takes seconds instead of a minute and a half — and it costs money, if not much.
Five agents across one lecture stay within cents; pi displays the cost per run
in the pane.

In exchange, the lecture-hall setup disappears: no LM Studio, no model to load,
no wait on the first run. To show the demo without a network, put a local model
in the agents' frontmatter lines — the tools stay the same.

## When to do it differently

Everything here is built for demonstrability, not for operation. The moment
agents do work someone depends on, other rules apply: a queue with delivery
guarantees, retries with backoff, schema versions for events, observability
worth the name. None of that is here — and that is not an omission but the
point.
