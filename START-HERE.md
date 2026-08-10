# Start Here — the whole project in plain English

Read this before anything else. Every other document in this repo is the detailed version of something on this page.

## What is this project?

You have ideas for apps. Instead of just building them and hoping, you run each idea through a fixed process that:

1. decides whether the idea is worth building,
2. builds a small cheap version using AI,
3. publishes the whole story — costs, mistakes, failures included.

Most ideas will die in the process. That's fine. **The public record of the process is the real product.** The apps are the evidence.

## The one rule everything follows

**Smart planning is expensive. Building is cheap.**

A human (you) plus a smart AI do the thinking: the plans, the checklists, the rules. A cheap AI does the building. And whenever you step in to help the cheap AI, you write it down. You never claim "no humans involved" — you claim "**every time a human helped, it's on the record.**"

## The assembly line

Every idea goes through six steps. Each step has its own instruction sheet (the files in `pipeline/`):

1. **Intake** — turn a rough idea into a one-page card: the problem, who has it, and the "kill criteria" — tripwires agreed in advance that stop the idea before it wastes money.
2. **Research** — actively try to kill the idea with evidence. Ideas must *survive* research, not be flattered by it.
3. **Spec** — write down exactly what the first small version must do, as a checklist so precise a test can verify each line.
4. **Plan** — pick the tech and slice the work into small numbered tasks.
5. **Build** — the cheap AI does one task at a time, starting fresh each task. It gets 3 tries. If it's still failing, it must stop and write down why it's stuck instead of flailing.
6. **Postmortem** — an honest writeup with real numbers. Shipped or killed, it gets published.

Those instruction sheets are called **stage contracts** in the other docs. A contract is just a strict work order: *here's your input, here's the job, here's exactly what "done" looks like, here's what to do if you get stuck.* The "done" checklist is deliberately robotic — things a script can check (does the file exist? do the tests pass?) — never matters of taste.

## The experiment hiding inside

Big question this project tries to answer: **how much written instruction does a cheap AI actually need to build well?**

Four ways to brief the same project:

- **Just the goal.** One paragraph. Figure it out.
- **One big plan.** Everything in a single document.
- **A handful of docs.** Idea, research, spec, plan — maybe six files.
- **Fully sliced.** One tiny document per task; the AI sees only its own task.

Run the same project all four ways. Same final test for all of them. Compare cost, success rate, and how often the AI got stuck. Then repeat each way a few times, because one try proves nothing — and repeats are affordable precisely because the AI is cheap.

"**Granularity**" in the other docs just means: *how finely the instructions are sliced.*

## Calling your shot

Before running the experiment, you publish what you predict will happen and exactly how you'll measure it — and commit that to git *first*, so the timestamp proves you didn't move the goalposts after seeing results. That's all "**pre-registration**" means: calling the shot before you swing.

## The flight recorder

The "**observer**" is a small program that sits between your AI tool and the AI company's servers. Every call passes through it, and it writes down everything: what was sent, what came back, how many tokens, what it cost, how long it took. It never changes anything — it only records. The run's stats file is generated from this recording automatically, so **no number in this project is ever typed by hand.** (Until the observer exists, you keep the stats sheet manually — that's the RUNLOG.)

## Mini dictionary

| Word in the docs | What it actually means |
|---|---|
| Stage contract | The instruction sheet for one step of the assembly line |
| Definition of Done (DoD) | The robotic checklist that decides if a step's output counts |
| Kill criteria | Pre-agreed tripwires that kill an idea |
| Run | One trip through the assembly line (or part of it) |
| Calibration run | Practice run. Helping allowed. Used to fix the instruction sheets. Results never count. |
| Pure run | Real run. No helping allowed. If the AI gets stuck, "stuck" IS the result. |
| Intervention | Any time a human steps in. L1 = answered a question. L2 = pointed it the right way. L3 = did it yourself. |
| Blocked | The AI stopped and explained why, instead of thrashing. That's obedience, not failure. |
| Condition | One of the setups being compared (e.g. "just the goal") |
| Replicate | Doing the identical run again to see if the result holds |
| Granularity | How finely the instructions are sliced |
| Pre-registration | Publishing predictions and measurements before running |
| Observer | The flight recorder between your AI tool and the provider |
| Rollup | Turning the recorder's raw log into the stats file (`metrics.json`) |
| RUNLOG | The hand-kept stats sheet used until the observer exists |
| EXP-000 | The first project: the cheap AI builds the incubator's own tools |
| EXP-001 | The "how much documentation does it need" experiment |

## What you actually do next

1. **Make it official.** `git init`, commit everything, push to GitHub. Timestamps mean nothing until this happens.
2. **Practice.** Take a throwaway idea through the assembly line by hand, following `OPERATIONS.md`. The cheap AI *will* misread some instruction sheets — that's the point. Fix the sheets, commit the fixes.
3. **EXP-000.** Have the cheap AI build the flight recorder, then the tool that runs the assembly line automatically.
4. **EXP-001.** Fill in the blanks in the experiment plan (which tasks, which model, what budget), commit, then run it for real — no helping allowed.

## Map of this repo

| File / folder | What it is |
|---|---|
| `README.md` | The front door — short version for visitors |
| `START-HERE.md` | This file — the plain-English version |
| `OPERATIONS.md` | How to drive a run by hand, step by step |
| `pipeline/` | The six instruction sheets |
| `observer/` | The flight recorder's blueprint |
| `metrics/` | The exact format of the stats file |
| `experiments/` | The called shots — one folder per experiment |
