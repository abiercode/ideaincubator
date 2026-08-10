# OPERATIONS — Manual Runner Protocol (v0)

Until EXP-000 delivers the automated runner, **the human operator is the runner, and this document is the runner's program.** Follow it identically on every run. Deviations are interventions; interventions get logged.

## Before any run (once)

1. Repo is committed and pushed — contract timestamps only mean something with git history.
2. Pick ONE cheap model and pin it: exact model ID, provider, and (if the tool exposes it) temperature. Write it in every RUNLOG. Do not switch models mid-run, ever.
3. Note the git SHA of this repo — that is `prompts_sha` for every run under it.

## Where a run's artifacts live — and where the model works

Three places, three jobs:

- **The filing cabinet (this repo).** Contracts, RUNLOGs, decisions, and every run's documents under `runs/<run_id>/`. **The model NEVER works inside this repo** — opening an agent session here would let it read contracts, experiment designs, and answer context, contaminating the run.
- **The workbench (an empty folder, e.g. `~/smg-workbench/<run_id>/`).** Where doc-stage sessions (P1–P4, P6) run. It is empty on purpose: the model sees nothing except the pasted contract. Copy whatever it produces back into the filing cabinet's `runs/<run_id>/`.
- **The arena (a separate test repo).** Where build sessions (P5) run — one repo per build, created empty when P5 begins, so its git history contains nothing but the build model's own commits. Record its URL in the RUNLOG. For events of The Model Games: one repo per event, one branch per contestant model.

## Per-run setup

1. Create `runs/<run_id>/` using the naming scheme `<exp>-<condition>-r<replicate>` (calibration runs use `cal-<n>`).
2. Copy the RUNLOG template (bottom of this file) into `runs/<run_id>/RUNLOG.md` and fill the header.
3. Have the tool's usage/cost display visible. You will read tokens and cost from it after every stage.

## Stage execution loop

For each stage, in order (P1 → P6; P5 repeats per task):

1. **Render the contract.** Open the stage file in `pipeline/`, replace every `{{PLACEHOLDER}}` with its content. What each stage needs:
   - P1: the raw idea paragraph; the current constraints (until `incubator.yml` exists, write them inline in the prompt).
   - P2: `IDEA.md`; your research protocol (until ported from your other repo, use a minimal numbered protocol and note that in the RUNLOG); whether the tool has web access.
   - P3: `IDEA.md`, `RESEARCH.md`, the build budget.
   - P4: `SPEC.md`, the granularity setting, task size limit, allowed stack.
   - P5 (per task): `ARCHITECTURE.md`, the one task file, ONLY the files that task lists as inputs, the test command.
   - P6: idea/verdict/spec, the RUNLOG totals (manual stand-in for `metrics.json`), `git log --oneline`, any BLOCKED files.
2. **Fresh session. Always.** Never continue a previous session into a new stage or task. Context hygiene is part of the method under test — a reused session invalidates the run.
3. **Paste the rendered contract.** Nothing else. No encouragement, no extra explanation. Extra words are an unlogged intervention.
4. **Save outputs verbatim** into `runs/<run_id>/` exactly as the model produced them. Do not fix typos, formatting, or names — if it needs fixing, that is an intervention.
5. **Check the Definition of Done** from the contract, literally: required headers present and in order, verdict strings exact, minimum item counts met, banned vague words absent (search for them), every AC mapped. For P5: test command exits 0, only permitted files touched, one commit with the required message.
6. **Record the stage row** in the RUNLOG: tokens in/out and cost from the tool's usage display, wall-clock, attempts, blocked or not.
7. **On DoD failure:**
   - Doc stages (P1–P4, P6): retry at most ONCE, in a fresh session, same rendered contract. Second failure = stage blocked; log it, then decide whether to intervene (and log the intervention level) or end the run as `blocked`.
   - Build tasks (P5): the 3-attempt bound is inside the contract. If the model doesn't stop itself and write its BLOCKED file, stopping it yourself is an L2 intervention.

## Intervention ladder (log every touch)

- **L1 — unblocked:** answered a question, supplied a missing input.
- **L2 — corrected:** redirected a wrong approach, stopped a thrash loop.
- **L3 — took over:** edited code or documents by hand.

Every entry needs level, minutes, and a one-line note. "I quickly fixed one import" is an L3 with a time cost. An empty interventions table on a run that needed no touches is the claim — make it true.

## Run rules

- **Pure runs (pre-registered experiment cells):** interventions are forbidden. A blocked run is a valid data point; an intervened run is voided (`failed`) and published anyway.
- **Calibration runs (`cal-*`):** interventions are allowed and expected — their purpose is to find contract bugs. No claims are ever made from calibration runs.
- Contract bugs found during calibration are fixed in `pipeline/`, committed, and noted; the new SHA applies to subsequent runs. Contracts are FROZEN during a pre-registered experiment.

## End of run

1. Fill RUNLOG totals (sum the stage rows) and the outcome line.
2. If stage P6 ran, its `RESULTS.md` lives in the run folder.
3. Commit the entire run folder. Nothing about a run is edited after its commit; corrections go in a dated addendum section.

## Before pushing anything public

Run this checklist every time, until the observer's `publish-check` automates it:

1. **No secrets.** Search the changes for API keys, tokens, and passwords before pushing (`git diff --cached` and skim). `.gitignore` catches config files, not text pasted into logs.
2. **Transcripts skimmed.** Any saved model output or pasted session content gets a human skim for keys, personal paths, and private data.
3. **Commit email is the noreply address.** `git config user.email` should show `...@users.noreply.github.com`, not a personal or business address.
4. **Ported content was cleared deliberately.** Anything copied from a private repo (research protocols, notes) was consciously reviewed for publication, not just pasted.
5. **Backlog stays home.** Ideas are published when they enter the pipeline (P1), never as a raw future-ideas list.

## RUNLOG template

```markdown
# RUNLOG — <run_id>

- Date:
- Experiment / purpose:
- Condition: authorship= granularity= context=
- Tool (and version):
- Model (exact ID, provider, temperature if known):
- prompts_sha:
- Web access available:

## Stages

| Stage | Task | Tokens in | Tokens out | Cost ($) | Wall clock | Attempts | Blocked? |
|-------|------|-----------|------------|----------|------------|----------|----------|

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
- ACs passed / total:
- Notes:

## Addenda

(dated corrections only — never edit the sections above after commit)
```
