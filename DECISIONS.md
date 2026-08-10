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
| 2026-08-09 | Flagship public series | Generic experiment writeups · benchmark-style model comparison with real builds | **The Small Model Games: budget models compete in real software-build events, full receipts (repo + flight-recorder log) published; no single winner — per-model profiles and coaching cards** |
| 2026-08-09 | Series name | Cheap Model Olympics (blocked: "Olympic" is federally protected, Ted Stevens Act) · Artificial Arena (blocked: LMArena collision, reads as Artificial Analysis knockoff) · Coding Colosseum (spelling liability) · Pennyathlon · Cheapionship | **Small Model Games — zero search collisions at decision time** |
| 2026-08-09 | Launch events (v1) | 11-event taxonomy drafted | **The Dictation (spec fidelity w/ canaries), The Accountant (business-rule math), The Repair (fix failing tests); v1 scope = 3 events × ~5 models × 3 replicates, static results page** |
| 2026-08-09 | Event safety rule | — | **Every event is a pure input→output utility: no auth, no encryption, no payments, no personal data** |
| 2026-08-09 | Calibration run | Throwaway practice app · small slice of a real event | **First Games event run with a single model doubles as the calibration run** |
| 2026-08-09 | Season 1 roster | Paid budget models (OpenCode Go's 18) · free models only | **Free models only — "The Free League" (~20 free models across OpenCode and Kilo). Paid budget roster deferred to a later season. Free-tier quirks (rate limits, model churn) are logged as findings, not failures** |
| 2026-08-09 | Repo visibility, revisited | Stay private until first experiment writeup · go public now | **Public now — supersedes the earlier private-until-writeup row. Founder's call: build in the open from day one** |
| 2026-08-09 | Series name, revisited | Keep Small Model Games · Cost Comparison Model Games · Budget/Cheap Model Games · "The Model Games" as part of an abiercode "Model ___" family | **The Model Games — supersedes the Small Model Games row. Sibling naming with the Model Jobs project (separate repo); "cost comparison" is tagline/metric language, not an edition tag; no "CC" abbreviation; Season 1 remains the Free League. Sub-brands (Free League, event names) carry search uniqueness** |

## Open (decision needed, in rough order)

| Decision | Notes |
|----------|-------|
| Claim the name | **themodelgames** (decided 2026-08-09): domain (.com/.dev/.ai as available) + GitHub org name — founder only (needs registrar/GitHub accounts). Grab matching modeljobs handles in the same sitting to keep the family intact. Do before any public mention beyond this repo |
| Which event runs first (= calibration) | The Dictation or The Accountant; single model, small scope |
| Which cheap model to pin for experiments | Try candidates during calibration runs; record exact model ID |
| Which tool carries pre-registered runs | Depends on whether the observer can sit under Kilo; OpenCode is the likely fallback — test when observer exists |
| Observer tech stack | Chosen at P4 during EXP-000, from the allowed-stack constraint |
| Observer vs. startingsandbox ledger | The sibling project (delegation governance layer, `~/startingsandbox`) already has a frozen event schema and a recorder in progress. Decide before EXP-000 builds anything: is the incubator's observer a client of that ledger, or a separate system? |
| EXP-001 blanks | Task battery, per-run budget — must be committed before any EXP-001 run |
| Brand/profile polish | Org page, profile README, pinned repos — any time before going public |
