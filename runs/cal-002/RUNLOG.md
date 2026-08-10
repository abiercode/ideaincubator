# RUNLOG — cal-002

- Date: 2026-08-09 (opened)
- Experiment / purpose: Calibration of stages P4–P5 + first heat of The Accountant (The Model Games, Free League Season 1). Enters pipeline at planning stage — event spec is human+frontier authored (events/the-accountant/SPEC.md). Interventions allowed and logged; no medal claims from a calibration heat.
- Condition: authorship=human_frontier granularity=phased context=fresh_per_task
- Tool (and version): OpenCode (fill in version)
- Model (exact ID, provider, temperature if known): DeepSeek V4 Flash Free via OpenCode free tier (confirm exact ID shown in OpenCode)
- prompts_sha: (fill in at first sitting: `git rev-parse --short HEAD`)
- Web access available: (note per session)
- **Wall clock: RECORD THIS RUN** (cal-001 gap): note start and end time of every sitting.

## Stages

| Stage | Task | Tokens in | Tokens out | Cost ($) | Wall clock | Attempts | Blocked? |
|-------|------|-----------|------------|----------|------------|----------|----------|
| P4 | — | (pending founder's report) | — | $0 (free tier) | (pending) | 1 | No |
| P5 | T01 | (pending founder's report) | — | $0 (free tier) | (pending) | 1 | No |

Stage notes:
- P4 (2026-08-09): DoD PASSED mechanically — 12/12 ACs each claimed exactly once, dependency graph acyclic and topologically numbered, 6 required sections per task, no "and also", no implementation code smuggled. Plan quality is genuinely strong: all 5 canaries correctly planned (Decimal-from-strings + ROUND_FLOOR for C1/AC-12 float trap caught AT PLANNING TIME, payment-before-accrual C2, Z→A C3, USD format C4, exit-2/stderr C5); AC-1's 31-day arithmetic hand-verified correct in Key Decision 2.
- **FOUNDER DECISION (2026-08-09): OBSERVE, do not intervene.** The blank-line defect rides into the build untouched; the prediction below was committed before any build sitting. Zero interventions logged for this observation — spotting is not touching.
- **DEFECT OBSERVED AT REVIEW:** Key Decision 10 and task T08 INVENT blank lines in the statement layout ("header, blank line, rows, blank line, TOTAL"). The spec's exact output block has no blank lines. Violates "do not invent requirements"; propagates deterministically to the builder via T08, whose objective cites "the exact layout from the architecture" — not the spec. If unintervened, prediction: builder's own tests will pass while all 11 stdout-comparing acceptance checks fail on the blank lines.
- P5/T01 (2026-08-10): Mechanical DoD PASSED, operator-verified — exactly one commit (`ea21420`, correct message format, noreply author), working tree clean, exactly the 4 permitted files, Done Check re-run by operator: 19/19. **Discipline finding — SCOPE CREEP: T01 also implemented T02's entire objective** (`load_payments`, `validate_payment_references` — the commit message even admits "invoices/payments input layer"). Rule 2 ("no additions") violated in spirit; mechanical DoD couldn't catch it because the extra work landed inside permitted Output Files. Likely cause: ARCHITECTURE's Module Interfaces section lists records.py's full interface, and the model implemented the interface, not the task. Observe posture holds — no intervention; T02 proceeds as planned to see how the model handles finding its work already done (block honestly / pad / add tests and commit).
- Minor deviations logged: ARCHITECTURE.md has a 6th section ("Module Interfaces") beyond the five listed — contract says "with sections", not "exactly these sections"; wording-hardening candidate post-run. 10 tasks for a ~6-file program (4 tasks satisfy no ACs) — task-count inflation under "phased" granularity, a data point for EXP-001. Key Decision 11 completes an undefined tiebreak (equal owed AND equal client → input order) — benign, arguably necessary.

## Interventions

| Stage | Task | Level | Minutes | Note |
|-------|------|-------|---------|------|

## Totals

- Cost ($):
- Tokens in / out:
- Wall clock:
- Human minutes (interventions + setup + review):

## Outcome

- Status: shipped | killed | blocked | failed
- ACs passed / total: (from events/the-accountant/acceptance/run_acceptance.py — 13 checks)
- Canaries caught / 5:
- Arena repo:
- Notes:

## Addenda

(dated corrections only — never edit the sections above after commit)
