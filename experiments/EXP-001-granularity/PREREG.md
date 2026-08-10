# EXP-001 — The Granularity Sweep

**Status: PRE-REGISTERED. No results exist. The git timestamp of this file predates every run.**

## Question

What is the optimal unit of documentation and context for a cheap coding model — a bare goal, one master plan, a phased document set, or a fully decomposed one-doc-per-task structure?

## Background

The popular assumption is "more/better-structured instructions help." Existing evidence (skills benchmarks, long-context studies) says this is not reliably true, and nobody has published a controlled granularity curve for cheap models. Cheap models make replication affordable, so we can run each condition multiple times — which frontier-model experiments cannot economically do.

## Conditions

All conditions in this experiment use **human+frontier-authored documents** (`authorship: human_frontier`). The authorship axis (cheap model writes its own docs) is deferred to EXP-002; the context-hygiene control is deferred to EXP-003.

| ID | Granularity | Builder receives |
|----|-------------|------------------|
| C0 | `goal_only` | One paragraph stating the goal. Nothing else. The "vibe coding" floor. |
| C1 | `monolith` | One `PLAN.md` containing the full spec, architecture, and task list as prose. |
| C2 | `phased` | ~6 documents: idea, research, spec, architecture, task list, test strategy. |
| C3 | `blown_out` | `ARCHITECTURE.md` + one narrow task file per task; each build session sees only its own task (contract P5). |

**Information-parity rule:** C1, C2, and C3 are all derived from the same master specification — C1 by concatenation, C2 by splitting into phases, C3 by task-slicing. They must contain the same information, differently structured. Otherwise this experiment measures information quantity, not structure. C0 intentionally has less information; it is the floor baseline, not a parity condition.

## Design

Two tiers, same conditions:

- **Tier 1 — task battery (the statistics).** {{N_TASKS}} small independent coding tasks (target 12–15), each run under all 4 conditions, n ≥ 3 replicates per cell. This is where directional evidence comes from.
- **Tier 2 — flagship build (the story).** One real project built once per condition, all artifacts public. Weak as statistics, strong as a public case study.

**Task selection criteria** (tasks to be chosen and committed here BEFORE any run):

1. Not tutorial-famous. No todo apps, no weather apps — nothing a model completes from training memory, which would artificially favor C0.
2. Deterministically testable: pass/fail decidable by a script.
3. Contains at least one piece of specific business logic that must come from the documents, not from priors.
4. Buildable within the per-run budget below.

Chosen tasks: _TBD — this section must be filled and committed before the first run._

## Constants (held fixed across all cells)

- Model: _TBD_ (one cheap model, same version, same temperature, pinned in every `metrics.json`).
- Stage contracts at git SHA: _pinned at first run; prompts frozen for the experiment's duration._
- Acceptance test suite: written by human+frontier BEFORE any run, identical across all conditions. This is the measurement instrument, not part of any condition.
- Budget: _TBD_ max model spend per run; runs exceeding it are recorded as `failed`, not extended.

## Rules

1. **Pure runs.** No human interventions. A blocked run is a completed data point with outcome `blocked`. Any intervention voids the run (`failed`), and the void is published like any other result.
2. **Frozen prompts.** No contract edits mid-experiment. A discovered harness bug aborts and restarts the experiment with a new pre-reg amendment noting what changed and why.
3. **No post-hoc conditions.** New cells require a dated amendment section below, added before those cells run.
4. **Everything publishes.** Every run's `metrics.json`, artifacts, and git history are public regardless of outcome.

## Hypotheses (directional predictions, registered before data)

- **H1 — Floor is task-dependent.** C0 (goal-only) approaches the other conditions on generic task shapes and collapses on tasks whose business logic lives in the documents.
- **H2 — Inverted U.** C2 (phased) outperforms C1 on acceptance-rate per dollar; C3 wins on the most complex tasks but pays overhead (more tokens, more orchestration) on simple ones. Maximal decomposition is not predicted to dominate.
- **H3 — Decomposition buys stability, not just success.** C3 shows lower variance across replicates and fewer thrash loops (retries) than C1, even where mean success is similar.
- **H4 — Context freshness confound.** A substantial share of C3's advantage (if any) is attributable to fresh context per task rather than document structure. Not testable inside EXP-001 — registered here, tested in EXP-003 (monolith doc + fresh session per task).

## Metrics

- **Primary:** acceptance-criteria pass rate (from the fixed external test suite).
- **Secondary:** cost (USD), tokens, retries, blocked rate, wall-clock, variance across replicates.
- **Quality:** rubric score (0–10) from a frontier-model judge, blinded — condition-identifying content stripped from code before judging.
- All metrics conform to `metrics/metrics.schema.json`, one `metrics.json` per run.

## Analysis plan

Report per-cell means and full ranges. With n=3–5 per cell we make **no statistical-significance claims** — only directional consistency ("C2 beat C1 in 14 of 15 tasks") with all raw data published for reanalysis. Aggregation scripts are committed before results exist.

## Kill criteria for this experiment

- If the harness cannot produce 5 consecutive clean runs (no harness errors) during setup, the experiment halts and EXP-000 reopens.
- If C0 and C3 are statistically indistinguishable on every task including the document-dependent ones, the task battery is declared invalid (tasks too generic) and is redesigned under an amendment.

## Amendments

_None yet. Amendments must be dated, appended here, and committed before any affected run._
