# Idea Incubator

A public software laboratory. Ideas go in, experiments come out, and every outcome — shipped or killed — is documented from hypothesis to result.

**New here? Read [START-HERE.md](START-HERE.md) first — it explains everything in plain English.**

## Operating thesis

**Judgment is expensive, labor is cheap.** A human (with frontier-model help) designs the stage contracts, acceptance criteria, and kill criteria. A cheap model executes against them. We never claim "no human involvement" — we claim **every human touch is logged.**

The incubator is also a methodology laboratory: each experiment tests not just a product idea, but a hypothesis about *how software should be built when AI does the labor*.

## Repository layout

```
pipeline/       Stage contracts — the versioned prompt templates the runner
                feeds to the build model. One contract per stage; each is
                self-contained because each agent sees only its own contract.
observer/       The agent observer — a passive local proxy that records every
                model call and run event to an append-only events.jsonl.
                metrics.json is derived from it by rollup, never hand-written.
                First build target of EXP-000 (see observer/SPEC.md).
metrics/        The metrics schema every run must emit (metrics.json per run).
experiments/    One folder per experiment. Pre-registration docs are committed
                BEFORE any results exist; git history is the timestamp.
```

## Pipeline stages

| Stage | Contract | Produces |
|-------|----------|----------|
| P1 | `pipeline/P1-intake.md` | `IDEA.md` |
| P2 | `pipeline/P2-research.md` | `RESEARCH.md`, `VERDICT.md` |
| P3 | `pipeline/P3-spec.md` | `SPEC.md` |
| P4 | `pipeline/P4-plan.md` | `ARCHITECTURE.md`, `TASKS/` |
| P5 | `pipeline/P5-build-task.md` | code, one commit per task |
| P6 | `pipeline/P6-postmortem.md` | `RESULTS.md` |

Contracts are prompts with `{{PLACEHOLDER}}` slots the runner fills. They are model-agnostic: anything model-specific lives in a per-model adapter, never in a contract. Every run records the git SHA of the contracts it ran under.

## Status

Design phase. Experiment 000 (the cheap model builds the runner itself) has not started. Nothing here has results yet — that's the point of pre-registration.
