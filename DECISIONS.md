# Decision Log

Every decision that shapes this project, in one place. The decider is always the founder; AI (frontier-model) input is advisory. A decision isn't real until it has a row here.

## Decided

| Date | Decision | Options considered | Outcome |
|------|----------|--------------------|---------|
| 2026-08-09 | What this project is | Content site about ideas · portfolio of small apps · public incubator with a documented kill process | **Public software laboratory: ideas → experiments → shipped or killed, everything published** |
| 2026-08-09 | Division of labor | Fully autonomous cheap AI · human builds everything · split by cost of judgment | **Judgment (contracts, criteria, kills) = human + frontier AI; labor (building) = cheap AI; every human touch logged** |
| 2026-08-09 | Who builds the incubator's own tools | Human builds them · frontier AI builds them · cheap AI builds them as the first case study | **Cheap AI builds them — that is EXP-000, dogfooded and documented** |
| 2026-08-09 | How the cheap AI is instructed | One big plan doc · freeform prompting · versioned stage contracts with machine-checkable "done" rules | **Six stage contracts (P1–P6), frozen during experiments, versioned by git SHA** |
| 2026-08-09 | How experiment claims stay honest | Publish results as they come · pre-register predictions and metrics before running | **Pre-registration, committed to git before any run** |
| 2026-08-09 | First real experiment | Cheap vs expensive model · autonomy levels · documentation granularity | **EXP-001: the granularity sweep (goal-only vs one plan vs phased vs fully sliced); authorship test deferred to EXP-002, context-freshness control to EXP-003** |
| 2026-08-09 | How runs are measured | Trust the tool's dashboard · hand-kept logs forever · passive local proxy recording every call | **The observer: flight-recorder proxy, file-based, stats derived from raw events — never hand-written. Manual RUNLOG until it exists** |
| 2026-08-09 | Repo architecture | Everything in one repo · lab repo + separate test-area repo per build | **Two-repo split: this lab repo holds methodology; each build gets its own clean test repo; observer gets its own repo when built** |
| 2026-08-09 | GitHub identity | phxwebsites · osograjales-ai · drmarlabizpro accounts | **abiercode org, committing as osograjales-ai with GitHub noreply email; personal emails never in commits** |
| 2026-08-09 | License | MIT · Apache-2.0 · AGPL · source-available | **MIT on this repo; Apache-2.0 planned for the observer; per-product choice at intake (MIT default, AGPL-3.0 for hostable services) — see P1 contract; DCO required from contributors** |
| 2026-08-09 | Repo visibility | Public now · private until there's something to show | **Private until the first experiment writeup exists; keep pushing to the private remote so GitHub independently records commit arrival times** |
| 2026-08-09 | Idea backlog | Publish all ideas · publish only ideas that enter the pipeline | **Backlog stays private (gitignored); ideas become public at intake (P1)** |
| 2026-08-09 | How decisions get made | AI acts and reports · founder decides everything, AI advises | **Founder is in the loop on every decision; AI presents options + recommendation and waits. No AI co-author lines in commits** |

## Open (decision needed, in rough order)

| Decision | Notes |
|----------|-------|
| Which cheap model to pin for experiments | Try candidates during calibration runs; record exact model ID |
| Throwaway idea for the first calibration run | Deliberately disposable; 2–3 build tasks max |
| Which tool carries pre-registered runs | Depends on whether the observer can sit under Kilo; OpenCode is the likely fallback — test when observer exists |
| Observer tech stack | Chosen at P4 during EXP-000, from the allowed-stack constraint |
| EXP-001 blanks | Task battery, per-run budget — must be committed before any EXP-001 run |
| Brand/profile polish | Org page, profile README, pinned repos — any time before going public |
