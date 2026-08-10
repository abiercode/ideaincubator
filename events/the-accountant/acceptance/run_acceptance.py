#!/usr/bin/env python3
"""Acceptance suite for The Accountant (The Model Games, Season 1).

Usage:  python3 run_acceptance.py /path/to/latefee.py

The referee. Runs the contestant's latefee.py as a subprocess against fixture
files and compares stdout / stderr / exit codes exactly. Pre-registered before
any heat runs; contestants never receive this file in-session.

Every expected value was hand-computed from the spec's fee rules:
  daily accrual = principal(D) * monthly_rate_pct / 100 / 30
  window: due_date + grace_days + 1 .. as_of, inclusive
  payment dated D applies BEFORE day D's accrual
  fee = min(floor_to_cent(sum), floor_to_cent(amount * cap_pct / 100))
Policy in all fee cases: grace 5, monthly 3.0% (=> $0.001/day per $1), cap 25%.
"""

import json
import os
import subprocess
import sys
import tempfile

POLICY = {"grace_days": 5, "monthly_rate_pct": 3.0, "cap_pct": 25.0}

def policy(as_of, **overrides):
    p = dict(POLICY)
    p["as_of"] = as_of
    p.update(overrides)
    return p

HEADER_I = "invoice_id,client,amount,due_date"
HEADER_P = "invoice_id,payment_date,amount"

# Each case: id, invoices rows, payments rows, policy (dict, or raw str for
# malformed), expect dict: exit / stdout (exact, or None = must be empty) /
# stderr_nonempty.
CASES = [
    dict(
        id="AC-1 baseline accrual",
        # 31 accrual days (Jan16..Feb15) x $0.10 = 3.10 exactly; floor 3.10.
        invoices=["INV1,Ana,100.00,2026-01-10"], payments=[],
        policy=policy("2026-02-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-15\n"
            "INV1 Ana principal USD 100.00 fee USD 3.10 owed USD 103.10\n"
            "TOTAL USD 103.10")),
    ),
    dict(
        id="AC-2a last grace day, zero-fee statement (canary C2)",
        # as_of = due+5: window start Jan16 > as_of -> no accrual, omitted.
        invoices=["INV1,Ana,100.00,2026-01-10"], payments=[],
        policy=policy("2026-01-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-01-15\n"
            "TOTAL USD 0.00")),
    ),
    dict(
        id="AC-2b first accrual day (canary C2)",
        # Exactly 1 day: floor(0.10) = 0.10.
        invoices=["INV1,Ana,100.00,2026-01-10"], payments=[],
        policy=policy("2026-01-16"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-01-16\n"
            "INV1 Ana principal USD 100.00 fee USD 0.10 owed USD 100.10\n"
            "TOTAL USD 100.10")),
    ),
    dict(
        id="AC-3 payment applies before same-day accrual (canary C2)",
        # Jan16 principal after the Jan16 payment = 50.00 -> 0.05 accrues.
        invoices=["INV1,Ana,100.00,2026-01-10"],
        payments=["INV1,2026-01-16,50.00"],
        policy=policy("2026-01-16"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-01-16\n"
            "INV1 Ana principal USD 50.00 fee USD 0.05 owed USD 50.05\n"
            "TOTAL USD 50.05")),
    ),
    dict(
        id="AC-4 principal cleared mid-window stops accrual",
        # Days Jan16..19 at $100 = 4 x 0.10 = 0.40; payment Jan20 zeroes
        # principal before Jan20's accrual; nothing accrues after.
        invoices=["INV1,Ana,100.00,2026-01-10"],
        payments=["INV1,2026-01-20,100.00"],
        policy=policy("2026-02-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-15\n"
            "INV1 Ana principal USD 0.00 fee USD 0.40 owed USD 0.40\n"
            "TOTAL USD 0.40")),
    ),
    dict(
        id="AC-5 overpayment floors at zero, no negatives",
        # Paid 150 on 100 during grace: principal 0 for the whole window.
        invoices=["INV1,Ana,100.00,2026-01-10"],
        payments=["INV1,2026-01-12,150.00"],
        policy=policy("2026-02-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-15\n"
            "TOTAL USD 0.00")),
    ),
    dict(
        id="AC-6 floor rounding (canary C1)",
        # 149.95 x 0.001 = 0.14995/day; 20 days (Jan16..Feb4) = 2.999 exactly.
        # Floor => 2.99. Round-half-up implementations print 3.00 and fail.
        invoices=["INV1,Ana,149.95,2026-01-10"], payments=[],
        policy=policy("2026-02-04"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-04\n"
            "INV1 Ana principal USD 149.95 fee USD 2.99 owed USD 152.94\n"
            "TOTAL USD 152.94")),
    ),
    dict(
        id="AC-7 cap applies",
        # 304 accrual days (Jan16..Nov15) x 0.10 = 30.40 > cap 25.00.
        invoices=["INV1,Ana,100.00,2026-01-10"], payments=[],
        policy=policy("2026-11-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-11-15\n"
            "INV1 Ana principal USD 100.00 fee USD 25.00 owed USD 125.00\n"
            "TOTAL USD 125.00")),
    ),
    dict(
        id="AC-8 sort owed desc, ties Z->A (canary C3)",
        # 31 days. Ana/Zoe: 48.75 -> 1.51125 floor 1.51, owed 50.26 (tie).
        # Bob: 195.00 -> 6.045 floor 6.04, owed 201.04.
        # Order: Bob, then tie broken Z->A: Zoe before Ana.
        invoices=[
            "INV1,Ana,48.75,2026-01-10",
            "INV2,Zoe,48.75,2026-01-10",
            "INV3,Bob,195.00,2026-01-10",
        ],
        payments=[],
        policy=policy("2026-02-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-15\n"
            "INV3 Bob principal USD 195.00 fee USD 6.04 owed USD 201.04\n"
            "INV2 Zoe principal USD 48.75 fee USD 1.51 owed USD 50.26\n"
            "INV1 Ana principal USD 48.75 fee USD 1.51 owed USD 50.26\n"
            "TOTAL USD 301.56")),
    ),
    dict(
        id="AC-9 formatting >= 1000: no commas, no $ (canary C4)",
        # 32000 x 0.001 = 32.00/day x 31 = 992.00; cap 8000 not hit.
        invoices=["INV1,Ana,32000.00,2026-01-10"], payments=[],
        policy=policy("2026-02-15"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-02-15\n"
            "INV1 Ana principal USD 32000.00 fee USD 992.00 owed USD 32992.00\n"
            "TOTAL USD 32992.00")),
    ),
    dict(
        id="AC-10 malformed policy: exit 2, stderr, empty stdout (canary C5)",
        invoices=["INV1,Ana,100.00,2026-01-10"], payments=[],
        policy_raw=json.dumps({"grace_days": 5, "monthly_rate_pct": 3.0,
                               "as_of": "2026-02-15"}),  # cap_pct missing
        expect=dict(exit=2, stdout=None, stderr_nonempty=True),
    ),
    dict(
        id="AC-11 unknown invoice_id in payments: exit 2 (canary C5)",
        invoices=["INV1,Ana,100.00,2026-01-10"],
        payments=["INV9,2026-01-12,10.00"],
        policy=policy("2026-02-15"),
        expect=dict(exit=2, stdout=None, stderr_nonempty=True),
    ),
    dict(
        id="AC-12 exact decimal arithmetic (float trap)",
        # 40.00 for 50 days (Jan16..Mar6): exact accrual = 2.000 -> 2.00.
        # In binary floats, 3.0/100/30 lands just BELOW 0.001, so
        # 40*rate*50 = 1.9999999999999998 and a float floor prints 1.99.
        # Exact decimal arithmetic is the spec; 1.99 fails.
        invoices=["INV1,Ana,40.00,2026-01-10"], payments=[],
        policy=policy("2026-03-06"),
        expect=dict(exit=0, stdout=(
            "LATE FEE STATEMENT as of 2026-03-06\n"
            "INV1 Ana principal USD 40.00 fee USD 2.00 owed USD 42.00\n"
            "TOTAL USD 42.00")),
    ),
]


def run_case(latefee_path, case):
    with tempfile.TemporaryDirectory() as td:
        inv = os.path.join(td, "invoices.csv")
        pay = os.path.join(td, "payments.csv")
        pol = os.path.join(td, "policy.json")
        with open(inv, "w") as f:
            f.write(HEADER_I + "\n" + "".join(r + "\n" for r in case["invoices"]))
        with open(pay, "w") as f:
            f.write(HEADER_P + "\n" + "".join(r + "\n" for r in case["payments"]))
        with open(pol, "w") as f:
            f.write(case.get("policy_raw") or json.dumps(case["policy"]))
        try:
            proc = subprocess.run(
                [sys.executable, latefee_path,
                 "--invoices", inv, "--payments", pay, "--policy", pol],
                capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return False, "timed out after 30s"

    exp = case["expect"]
    problems = []
    if proc.returncode != exp["exit"]:
        problems.append(f"exit code: expected {exp['exit']}, got {proc.returncode}")
    got_out = proc.stdout.rstrip("\n")
    if exp["stdout"] is None:
        if got_out:
            problems.append(f"stdout should be empty, got: {got_out!r}")
    elif got_out != exp["stdout"]:
        problems.append(f"stdout mismatch:\n--- expected ---\n{exp['stdout']}\n--- got ---\n{got_out}")
    if exp.get("stderr_nonempty") and not proc.stderr.strip():
        problems.append("stderr should contain an explanatory line, got nothing")
    return (not problems), "; ".join(problems) if problems else "ok"


def main():
    if len(sys.argv) != 2:
        print("usage: python3 run_acceptance.py /path/to/latefee.py", file=sys.stderr)
        sys.exit(2)
    latefee = sys.argv[1]
    if not os.path.exists(latefee):
        print(f"not found: {latefee}", file=sys.stderr)
        sys.exit(2)
    passed = 0
    for case in CASES:
        ok, detail = run_case(latefee, case)
        print(f"{'PASS' if ok else 'FAIL'}  {case['id']}")
        if not ok:
            print(f"      {detail}")
        passed += ok
    print(f"\n{passed}/{len(CASES)} acceptance checks passed")
    sys.exit(0 if passed == len(CASES) else 1)


if __name__ == "__main__":
    main()
