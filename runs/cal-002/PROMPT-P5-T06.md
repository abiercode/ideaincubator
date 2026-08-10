# Stage contract P5 — BUILD-TASK

## Role

You are an implementer. You execute exactly one task. The judgment was done upstream; your job is precise, minimal execution. You are not asked to improve, extend, or rethink the plan.

## Inputs

Architecture:

```
# ARCHITECTURE — Late-Fee Settlement CLI

## Stack
- Python 3.11+, CPython, standard library only: argparse, csv, json, datetime.date, decimal, unittest; subprocess and tempfile for integration tests.
- No third-party packages, no pip installs.
- Entry point (fixed): `python latefee.py --invoices invoices.csv --payments payments.csv --policy policy.json`.
- All tests run with the standard library's unittest.

## File Map
- latefee.py — CLI entry point: argument parsing, orchestration, single stdout print, error contract, exit codes.
- errors.py — class LateFeeError(Exception); the only error type the CLI understands.
- policy.py — Policy dataclass and load_policy(path).
- records.py — Invoice and Payment dataclasses, load_invoices(path), load_payments(path), validate_payment_references(invoices, payments).
- fees.py — InvoiceResult dataclass and compute(invoice, payments, policy).
- statement.py — format_money(value) and build_statement(results, as_of).
- tests/__init__.py — marks tests/ a package so unittest loads it.
- tests/test_records.py — invoices/payments parsing and reference-check unit tests.
- tests/test_policy.py — policy parsing and validation unit tests.
- tests/test_fees.py — fee math unit tests (accrual, boundary, payments, floor, cap).
- tests/test_decimal_math.py — exact-decimal stress tests (AC-12).
- tests/test_statement.py — format_money and build_statement unit tests (AC-8, AC-9).
- tests/test_cli.py — subprocess tests of latefee.py: exact stdout bytes, stderr, exit codes (AC-10, AC-11).

## Data Model
- Policy: grace_days int >= 0; monthly_rate_pct Decimal > 0; cap_pct Decimal > 0; as_of date.
- Invoice: invoice_id str; client str; amount Decimal >= 0; due_date date.
- Payment: invoice_id str; payment_date date; amount Decimal >= 0.
- InvoiceResult (computed per invoice): invoice_id; client; principal Decimal >= 0 (outstanding as of policy.as_of); fee Decimal >= 0 (floored to cent, capped); owed Decimal = principal + fee.
- Relation: every Payment.invoice_id must appear among Invoice.invoice_id, else the input is malformed. Each payment attaches to exactly one invoice; fee computation consumes that invoice's own payments ordered by date.
- Invariants: no negative money value appears anywhere; all money quantities are exact Decimals, never floats.

## Module Interfaces
- errors.py: `class LateFeeError(Exception)`
- records.py:
  - `load_invoices(path: str) -> list[Invoice]`
  - `load_payments(path: str) -> list[Payment]`
  - `validate_payment_references(invoices: list[Invoice], payments: list[Payment]) -> None`
- policy.py: `load_policy(path: str) -> Policy`
- fees.py: `compute(invoice: Invoice, payments: list[Payment], policy: Policy) -> InvoiceResult`
- statement.py:
  - `format_money(value: Decimal) -> str`
  - `build_statement(results: list[InvoiceResult], as_of: date) -> str`
- latefee.py: `main(argv: list[str]) -> int`

## Key Decisions
1. All money is decimal.Decimal built from strings (raw CSV tokens, str() of parsed JSON numbers); floats never touch money paths. Rationale: AC-12.
2. Daily rate = Decimal(monthly_rate_pct)/100/30; each accrual day contributes outstanding principal x rate; contributions are summed over the whole window before any rounding. Rationale: AC-1 (100.00 at 3.0%, window 2026-01-16..2026-02-15 = 31 days, fee 3.10).
3. Accrual window is the inclusive calendar-day range [due_date + grace_days + 1, as_of]; an empty window means fee 0. Rationale: AC-2 (as_of on the last grace day accures nothing; the next day accrues exactly one day).
4. On each accrual day D, payments with payment_date <= D reduce the principal first, then D's accrual is computed on the reduced principal. Rationale: AC-3.
5. Outstanding principal = max(0, amount - sum of payments dated <= D); overpayments beyond the remaining principal are ignored. Rationale: AC-4, AC-5.
6. fee = min(floor_to_cent(sum of daily accruals), floor_to_cent(amount x cap_pct/100)); floor_to_cent uses quantize(Decimal("0.01"), ROUND_FLOOR). Rationale: AC-6 (2.999 -> 2.99), AC-7.
7. Display is f"{value:.2f}" on cent-exact Decimals prefixed with "USD "; no commas, no $, exactly two decimals. Rationale: AC-9 (USD 1234.56).
8. Every malformed input — missing file, bad CSV/JSON, wrong types, negative amounts, unknown invoice_id — raises LateFeeError carrying one human-readable line; main() catches it once, writes the message plus "\n" to stderr, returns exit code 2. Rationale: spec error contract.
9. The success path builds the entire statement string first, then prints it exactly once; nothing else ever touches stdout. Rationale: error handling leaves stdout empty.
10. Statement layout, byte-exact, trailing newline after the last line: "LATE FEE STATEMENT as of <as_of>", blank line, one row line per fee>0 invoice "<invoice_id> <client> principal USD <p> fee USD <f> owed USD <o>", blank line, "TOTAL USD <t>". Rationale: spec's exact blockquote.
11. Only invoices with fee > 0 appear; rows sorted by owed descending, ties broken by client name in reverse alphabetical order (Z->A); exact ties (equal owed and equal client) keep input order. Rationale: AC-8.
12. CSV parsing is strict: header must match the spec exactly (invoice_id,client,amount,due_date / invoice_id,payment_date,amount), every row exactly three fields, invoice_id and client non-empty, amounts parse as Decimal with negatives rejected, dates parsed with date.fromisoformat. Rationale: US-4.
13. policy.json must be a single JSON object with exactly the four keys (nothing missing, nothing extra); grace_days an int >= 0; monthly_rate_pct and cap_pct JSON numbers > 0 kept as Decimal(str(...)); as_of an ISO-8601 date string. Rationale: AC-10.
14. TOTAL = sum of owed over the printed rows only. Rationale: the statement's "sum of owed" covers what is displayed.

## Test Strategy
- All tests live in tests/; the single command running the whole suite, from the repository root, is: `python -m unittest discover -s tests -v`
- Each task's Done Check runs only its own test module, e.g. `python -m unittest tests.test_decimal_math -v`.
- Unit tests construct dataclasses directly and assert exact Decimal and str values; tests/test_cli.py spawns `sys.executable latefee.py ...` via subprocess with fixture files in a tempfile directory, asserting exact stdout bytes, exactly one stderr line when an error is expected, and the exit code.
```

Your task (T06):

```
## Objective
Add tests/test_decimal_math.py with stress tests proving that compute produces the same results as exact decimal arithmetic to the cent for inputs chosen to break binary floating point (amounts and rates like 19.99, 0.03, 0.07, repeated payments), verifying AC-12.

## Input Files
- ARCHITECTURE.md
- records.py
- policy.py
- fees.py

## Output Files
- tests/test_decimal_math.py

## Satisfies
- AC-12

## Depends On
- T03, T04

## Done Check
- python -m unittest tests.test_decimal_math -v
```

The working directory is the repository as of commit T05; the files your task lists as inputs are present on disk and you may read them. Test command: `python -m unittest tests.test_decimal_math -v`

Operational rule: do not end your turn until you have either made the commit or written the BLOCKED file.

## Task

Implement the objective in your task file so that its Done Check passes and the full test suite still passes.

## Rules

1. **Scope.** Create or modify ONLY the files listed under your task's Output Files, plus test files for your ACs. If you believe another file must change, that is a blocking condition (rule 6), not permission.
2. **No additions.** No features, endpoints, options, or refactors beyond the objective — even obvious improvements. Padding is a defect.
3. **Tests are law.** Never modify or delete an existing test to make it pass. If a test seems wrong, that is a blocking condition (rule 6).
4. **One commit.** When the Done Check passes, commit everything with the message `T06: <one-line summary>`.
5. **Retry bound.** You get at most 3 attempts at a passing Done Check. Attempt = implement (or fix), run `python -m unittest tests.test_decimal_math -v`, observe.
6. **Blocking.** On the 3rd failure, or if any rule above traps you, STOP and write `BLOCKED-T06.md` with exactly:
   - `## Task` — the task ID.
   - `## Attempts` — what you tried, one line each.
   - `## Failing Output` — the actual test/command output, pasted.
   - `## Suspected Cause` — your best one-paragraph diagnosis.
   - `## Needed` — the smallest thing that would unblock you.

   Then stop entirely. A well-written block is a successful outcome; a 4th attempt is a failure even if it works.

## Definition of done (machine-checked)

- `python -m unittest tests.test_decimal_math -v` exits 0.
- `git diff` touches only permitted files.
- Exactly one new commit exists with the required message format.
- OR: `BLOCKED-T06.md` exists in the required format and no partial changes are left uncommitted.

## Escalation

If a file your task names as an input was not provided, do not go looking for it or recreate it. That is a blocking condition — write the block file and stop.
