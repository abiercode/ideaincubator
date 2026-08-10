# Event: The Accountant

**Series:** The Model Games · **Season 1:** The Free League
**Discipline:** business-rule arithmetic under a precise specification.

## What this event measures

Whether a model builds what the *specification* says — not what its training habits expect. The domain is deliberately unglamorous: late-fee settlement math, full of boundary conditions (grace periods, payment timing, caps, rounding) where "close enough" is wrong and every rule has an exact answer.

Scored, per contestant:

- **Acceptance pass rate** — externally authored test suite, identical for every contestant, written before any heat runs.
- **Canary catch rate** — see the register below.
- **Cost-to-done** — total tokens/cost to a passing build, including retries.
- **Attempts-to-green** — retries per task; the thrash index.
- **Discipline** — scope creep beyond the spec, files touched outside the mandate, honest blocking vs. flailing.

## The canary register (public on purpose)

Canaries are rules that contradict what models do by default. They work even in the open: contestants receive the spec either way — the test is whether the model *reads* it or autocompletes from habit. Each canary maps to specific acceptance tests.

| # | Spec rule | The habit it contradicts |
|---|-----------|--------------------------|
| C1 | Fees round DOWN (floor) to the cent | Round-half-up / round-to-nearest |
| C2 | First accrual day is `due_date + grace_days + 1`; a payment dated day D applies BEFORE day D's accrual | Off-by-one on grace boundaries; payment-after-accrual ordering |
| C3 | Statement sorted by amount owed DESCENDING, ties by client name Z→A | Ascending sorts; A→Z tiebreaks |
| C4 | Money prints as `USD 1234.56` — no `$`, no thousands separators | `$1,234.56` |
| C5 | Malformed input → exit code 2, message on stderr | Exit code 1; errors on stdout |

## Provenance

The domain is resurrected from cal-001, where "late-fee calculator as a product" was researched by a free model and KILLED (no demonstrated market; commoditized free tools). The product died; the *specification* survived as a test fixture — which is exactly what the postmortem's "What Survived" section is for. No market claim is made or needed: this is a gym, not a store.

## Format

Events enter the pipeline at the planning stage: contestants receive `SPEC.md` (this folder) via stage contract P4, plan their build, then execute P5 build tasks in a fresh arena repo (one repo per event, one branch per contestant). The acceptance suite is authored by the operator side and is never shown to contestants during a heat; it is published with results after the heat completes.
