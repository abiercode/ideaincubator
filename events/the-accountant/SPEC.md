# SPEC — Late-Fee Settlement CLI ("The Accountant")

## Goal

A command-line tool that reads invoices, payments, and a written late-fee policy, and prints an exact settlement statement of what each client owes as of a given date — every number derived from the policy, to the cent, with no judgment calls left to the implementation.

## User Stories

- **US-1** — As Ana, a freelancer with a written late-fee policy, I run one command over my invoice and payment files so that I get the exact fee each overdue client owes today.
- **US-2** — As Ana, I record partial payments as they arrive so that fees accrue only on what is actually still outstanding, day by day.
- **US-3** — As Ana, I get a statement I can paste into an email so that the client sees the principal, the fee, and the total, unambiguously.
- **US-4** — As Ana, when my input files are malformed I get a clear error so that I never send a statement computed from garbage.

## Interface (fixed — tests depend on it)

The program is invoked exactly as:

```
python latefee.py --invoices invoices.csv --payments payments.csv --policy policy.json
```

Input formats:

- `invoices.csv` — header row, then columns: `invoice_id,client,amount,due_date`. `amount` is a decimal in USD; `due_date` is ISO-8601 (`YYYY-MM-DD`).
- `payments.csv` — header row, then columns: `invoice_id,payment_date,amount`. A payment applies to exactly one invoice.
- `policy.json` — object with exactly: `grace_days` (integer ≥ 0), `monthly_rate_pct` (decimal > 0), `cap_pct` (decimal > 0), `as_of` (ISO-8601 date).

## Fee rules (exact)

1. **Outstanding principal on day D** = invoice `amount` minus the sum of that invoice's payments with `payment_date` ≤ D. It never goes below zero; payment amounts beyond the remaining principal are ignored.
2. **Accrual window.** Fees accrue on each calendar day D from `due_date + grace_days + 1` through `as_of`, inclusive. A payment dated day D applies BEFORE day D's accrual (paying on day D avoids day D's fee).
3. **Daily accrual.** Each accrual day contributes `outstanding_principal(D) × monthly_rate_pct / 100 / 30`. Simple interest: fees never accrue on fees.
4. **Exact arithmetic.** All money math is exact decimal arithmetic to the cent. Binary floating-point artifacts that change any output by a cent are defects.
5. **Rounding.** The summed accrual per invoice is rounded DOWN (floor) to the cent. Never round-half-up, never round-to-nearest.
6. **Cap.** `cap_value = floor_to_cent(amount × cap_pct / 100)`. The final fee is `min(floored accrual, cap_value)`.
7. **Owed** per invoice = outstanding principal as of `as_of` + final fee.

## Statement output (exact)

To stdout, and nothing else on stdout:

```
LATE FEE STATEMENT as of <as_of>
<invoice_id> <client> principal USD <p> fee USD <f> owed USD <o>
...
TOTAL USD <sum of owed>
```

- One line per invoice with final fee > 0. Invoices with zero fee are omitted.
- Lines sorted by owed DESCENDING; ties broken by client name in REVERSE alphabetical order (Z→A).
- All money formatted with exactly two decimals, no thousands separators, no `$` symbol: `USD 1234.56`.
- Exit code 0 on success (including when no invoice has a fee — statement is then header + `TOTAL USD 0.00`).

## Error handling (exact)

- Any malformed input (missing file, missing/extra policy key, non-ISO date, non-numeric amount, unknown `invoice_id` in payments, negative amounts): print one explanatory line to stderr, produce NOTHING on stdout, exit code 2.

## In Scope

- The three input files and the exact statement output above (US-1, US-2, US-3).
- Partial and multiple payments per invoice, applied by date (US-2).
- The error contract above (US-4).

## Out of Scope

- Any currency other than USD; currency conversion.
- Compound interest, per-invoice policy overrides, or policy formats beyond the single JSON object.
- Output formats beyond the statement above (no PDF, HTML, JSON, CSV output).
- Date formats beyond ISO-8601; timezones (all dates are calendar dates).
- Payments not tied to a single invoice_id (no allocation across invoices).
- Persistence, config files, interactive prompts, or networking of any kind.

## Acceptance Criteria

- **AC-1** (US-1) — Given an invoice 100.00 due 2026-01-10, policy grace_days 5, monthly_rate_pct 3.0, cap_pct 25.0, as_of 2026-02-15, and no payments, when the tool runs, then the fee equals floor(100.00 × 0.03/30 × 31 days) = `USD 3.10` and owed is `USD 103.10`.
- **AC-2** (US-1, C2) — Given the same invoice, when as_of is 2026-01-15 (the last grace day), then no fee accrues and the invoice is omitted; when as_of is 2026-01-16 (first accrual day), then exactly one day has accrued.
- **AC-3** (US-2, C2) — Given a payment dated exactly on an accrual day D, when fees are computed, then day D's accrual uses the principal AFTER that payment.
- **AC-4** (US-2) — Given payments that fully clear the principal mid-window, when the tool runs, then no accrual occurs after the clearing date and the invoice's fee reflects only the days before it.
- **AC-5** (US-2) — Given a payment larger than the remaining principal, when the tool runs, then principal floors at zero and no negative values appear anywhere.
- **AC-6** (US-1, C1) — Given an accrual sum whose exact value is 2.999, when rounded, then the fee is `USD 2.99` (floor), not `USD 3.00`.
- **AC-7** (US-1) — Given an accrual that exceeds the cap, when the tool runs, then the fee equals cap_value exactly.
- **AC-8** (US-3, C3) — Given three invoices with owed 50.00 (client "Ana"), 50.00 (client "Zoe"), and 200.00 (client "Bob"), when the statement prints, then the line order is Bob, Zoe, Ana.
- **AC-9** (US-3, C4) — Given any output amount ≥ 1000, when printed, then it appears as `USD 1234.56` style: two decimals, no comma, no `$`.
- **AC-10** (US-4, C5) — Given a policy file missing `cap_pct`, when the tool runs, then stdout is empty, stderr has one explanatory line, and the exit code is 2.
- **AC-11** (US-4, C5) — Given a payment row referencing an unknown invoice_id, when the tool runs, then stdout is empty, stderr has one explanatory line, and the exit code is 2.
- **AC-12** (US-1) — Given amounts chosen to stress binary floating point, when fees are computed, then results match exact decimal arithmetic to the cent.

## Non-Goals

- Proving anyone would buy this. The product idea was researched and KILLED in cal-001; this specification exists as a test fixture for The Model Games.
- Configurability beyond the policy file. Every rule above is fixed on purpose — the rules ARE the event.
