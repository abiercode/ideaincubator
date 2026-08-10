## Problem
Freelancers and small businesses argue with clients over late-fee amounts because the math is genuinely ambiguous and different people calculate it differently. These disputes occur every time an invoice is overdue and no single, agreed-upon calculation exists to settle it. The arguing costs time, delays payment, and strains the relationship.

## Target User
Maya, a 37-year-old solo freelance web designer with roughly 40 active invoiced clients, who bills on 30-day net terms and currently has at least one overdue invoice every month.

## Hypothesis
Maya will run the tool monthly to generate a late-fee statement for an overdue client because she currently settles fee disputes through email back-and-forth with no agreed calculation.

## Kill Criteria
- Fewer than 5 of 10 interviewed freelancers report having had a late-fee disagreement with a client in the past 12 months.
- Fewer than 6 of 10 interviewed freelancers report computing late fees manually today (spreadsheet or by hand) rather than not charging them at all.
- If fewer than 4 of 5 test users, each with at least 10 overdue invoices, produce a client-ready statement within 5 minutes, the core job is not done.
- If fewer than 7 of 10 interviewed freelancers say they would use the tool monthly after a 10-minute demo.

## Monetization Guess
GUESS: a one-time paid CLI license for one user (approximately $29), with an optional cheap statement-template add-on pack.

## License
MIT — it is a local, client-side utility, not a hostable service, so there is no realistically commercial-hosted scenario to protect against.

## Constraint Check
| Constraint | Status | Reason |
| --- | --- | --- |
| Buildable in at most 3 build tasks by one developer | PASS | Late-fee calculation from tabular input is a small, well-scoped utility. |
| Pure input -> output utility; no accounts, auth, encryption, payments, personal data storage | PASS | It consumes input files and prints results; nothing is stored or authenticated. |
| Deterministic output that automated tests can verify | PASS | The same inputs will always produce the same printed math, which tests can assert exactly. |
| Runs entirely locally; no hosted services, no API keys | PASS | Command-line execution with no network or external services. |
| Releasable as open source | PASS | No proprietary dependencies or licensed assets are required. |

## Intake Verdict
INTAKE: ACCEPTED