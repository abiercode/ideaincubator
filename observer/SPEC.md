# SPEC — Agent Observer

<!-- Written in the P3 contract format on purpose: this spec is the build input for
     EXP-000. The observer is built BEFORE the runner — nothing can be measured
     without it. Bootstrap note: the observer's own build cannot be fully observed;
     it is documented with manual notes, and every run after it is observed. -->

## Goal

A passive, tool-agnostic recorder that captures every model call and run event into an append-only local log, and derives each run's `metrics.json` from that log — so that no metric in the incubator is ever hand-written.

## User Stories

- **US-1** — As the incubator operator, I point any agent tool (the runner, OpenCode, any CLI that accepts a base-URL override) at the observer so that every model call in a run is recorded without depending on the tool's cooperation.
- **US-2** — As the operator, I record my own interventions with one command so that every human touch becomes data on the L1/L2/L3 ladder.
- **US-3** — As the operator, I run one rollup command to produce `metrics.json` so that published metrics are derived from raw events, never typed by hand.
- **US-4** — As a reader of the public repo, I can inspect the full event log and transcripts of any run so that every published number is auditable back to raw events.
- **US-5** — As the operator, I run a redaction pass before publishing so that transcripts can go public without leaking secrets.

## In Scope

- A local HTTP proxy that forwards provider API traffic unmodified and logs each call (US-1).
- Run context: a start/end command that tags subsequent events with `run_id`, `stage`, and `task_id` (US-1, US-3).
- Append-only `events.jsonl` per run, with large request/response payloads stored as content-addressed blobs beside it (US-4).
- Cost computation at log time from a versioned local pricing table (US-3, US-4).
- An intervention-logging command (US-2).
- A rollup command producing `metrics.json` that validates against `metrics/metrics.schema.json` (US-3).
- A redaction command that scans blobs for secret patterns and rewrites matches (US-5).

## Out of Scope

- Any dashboard, web UI, or chart rendering. The artifact is files.
- Any hosted or multi-user service. This runs on one machine, writing to one repo.
- Modifying, retrying, caching, rate-limiting, or rerouting traffic. The observer never changes an outcome.
- Enforcing stage contracts, Done Checks, or retry bounds. Enforcement is the runner's job.
- Automatic intervention detection. Humans log their own touches.
- Provider API key management or authentication features beyond passing credentials through.
- Analysis, statistics, or judgment of run quality. The observer records; it does not conclude.

## Acceptance Criteria

- **AC-1** (US-1) — Given a tool configured with the observer's base URL, when the tool makes a model API call, then the request is forwarded to the provider byte-identical, the response is returned to the tool byte-identical, and exactly one `model_call` event is appended containing token counts taken from the provider's usage field.
- **AC-2** (US-1) — Given a streaming request, when the provider streams a response, then chunks are forwarded to the tool as they arrive, and after the stream ends one `model_call` event is appended with the assembled response and final usage counts.
- **AC-3** (US-1) — Given the provider returns an error status, when the observer relays it, then the tool receives the error unmodified and the event records the status code and error body.
- **AC-4** (US-1) — Given `observe start --run <id> --stage <stage> [--task <task>]` has been run, when any event is logged, then the event carries that run_id, stage, and task_id until `observe end` or a new context is set.
- **AC-5** (US-3) — Given a logged `model_call`, when its cost is computed, then `cost_usd` equals the event's token counts priced by the pricing table entry for that model, and the event records the pricing table version used.
- **AC-6** (US-2) — Given `observe log-intervention <L1|L2|L3> --minutes <n> "<note>"`, when the command completes, then one `intervention` event is appended with that level, minutes, and note, and a subsequent rollup includes the minutes in `totals.human_minutes`.
- **AC-7** (US-3) — Given a run directory containing `events.jsonl`, when `observe rollup` runs, then a `metrics.json` is written that validates against `metrics/metrics.schema.json` with zero validation errors.
- **AC-8** (US-3) — Given a process crash mid-run, when the observer restarts and rollup runs on the partial log, then all events appended before the crash are intact and rollup completes without error.
- **AC-9** (US-4) — Given any `model_call` event, when a reader follows its request and response references, then the full payloads are present in the run's blob store and their hashes match the references.
- **AC-10** (US-5) — Given a blob containing a string matching a configured secret pattern, when `observe redact` runs, then the blob is rewritten with the match replaced by a placeholder, and a `redaction` event is appended recording which blob was altered.
- **AC-11** (US-5) — Given `observe redact` has not been run on a run directory, when `observe publish-check` runs, then it exits nonzero and names the unscanned blobs.

## Non-Goals

- Proving the observer as a standalone product. If it earns an experiment page of its own later, that is a separate decision with its own pre-registration.
- Measuring output quality. The blinded judge does that, outside the observer.
- Supporting every provider on day one. v0 targets the providers the incubator actually uses; the pricing table and forwarding rules are data, not code branches.
