# RESEARCH

Restatement of the problem: Solo freelancers (target persona: Maya, a web designer with ~40 clients on Net-30 terms) end up in back-and-forth email arguments with clients over how much an overdue invoice's late fee should be. The idea claims the calculation "is genuinely ambiguous," that these disputes recur whenever an invoice is overdue, and that the freelancer would run a tool monthly to produce a late-fee statement that settles the amount.

## Existing Solutions

- **Most freelancers do not charge late fees at all.** In a Ruul survey of 30,000+ freelancers, 40% said they do not request a late fee to protect the client relationship, and 25% said they do not know how to charge one (Ruul, 2026). IPSE's 2024 survey found only 16% of freelancers include penalty/interest clauses in their contracts. The dominant behavior is not "calculator disagreement" — it is "they don't bother."
- **Those who do charge compute it by hand, by spreadsheet, or in simple arithmetic they already have.** The calculation is a single formula — invoice amount × monthly rate × months overdue, or a daily proration — repeated across blogs, invoicing vendors, and legal guides. It is not a hard computation, and multiple sources state flatly that disputes over the amount "resolve when the calculation is visible and simple" (Ruul, 2026).
- **The decisive step is conversational and legal, not arithmetic.** A fee is only enforceable if it was disclosed in a signed contract or proposal before the work began; a fee that appears first on the invoice is routinely refused and struck down in most jurisdictions (LancerWise, LegalClarity, 1099Freelance, all 2026). The binding constraint is the contractual clause and the willingness to risk the relationship — not the multiplication.
- **A leading fraction of freelancers does pay late**, so some of the pain is real: 29% of freelance invoices are paid at least one day late (Bonsai, 100k+ freelancers, 3 years of data); 85% of freelancers are paid late at least some of the time (Remote, 2025); 35% of UK freelancers experienced a delay in the last 12 months (IPSE, 2024).

## Competitors

Direct competitors — the specific job is "compute a late fee and produce a statement line":

- **InvoiceCat, ChaseAI, Plutio, Protawk, ClearReceivables, KipBill — free, no-signup, browser-based late-fee calculators** that take amount, due date, rate, and grace period, output the fee and a copy-ready statement line ("Late payment fee (1.5% per month, 24 days overdue): $12.00"), and are maintained for free by invoicing vendors as lead generation. They are $0 and take under a minute. Why Maya won't use a paid CLI over these: free, no install, no terminal, no learning curve.
- **Free spreadsheets** — the fee formula is one line; any freelancer already tracking invoices in a spreadsheet can add it in seconds. Zero cost, zero new tool.

Adjacent competitors — the job embedded in tools the target user already owns:

- **FreshBooks** — built-in late-fee charging (flat or percentage) with automatic application and reminders, from $19/mo. Used by the exact persona.
- **QuickBooks Online** — automatic late fees applied to overdue invoices up to six months, per-customer rates and grace periods.
- **Bonsai** — default late-fee percentage auto-applied the day after due date, recurring monthly; the suite marketed specifically to freelancers.
- **Agiled, HoneyBook, Invoice Ninja, Xero** — automatic late-fee application per vendor (Agiled 2026 roundup; QuickBooks/FreshBooks/Bonsai help centers, 2026).
- **Wave** — free forever invoicing; no automatic fees, but a manual line item exists for anyone who wants it ($0).
- **Ledger / Beancount (CLI accounting)** — plain-text command-line accounting that can generate any custom report including fee statements; free. Notably, CLI accounting tools are documented as appealing to developers, with a "steeper learning curve" — evidence the terminal is a developer channel, not a designer channel.

Why Maya does not use these "instead": she doesn't have a fee problem she's willing to act on. The people who do charge already get the calculation from tools she could already own, and the freelancers who don't charge are choosing not to, not failing to calculate.

## Demand Evidence

- [verified] 29% of freelance invoices are paid at least one day late (Bonsai analysis of 100,000+ freelancers over 3 years).
- [verified] 85% of freelancers report invoices paid late at least some of the time; 21% are paid late or not at all more than half the time (Remote, State of Freelance Work 2025).
- [verified] 35% of UK freelancers experienced late payment in the last 12 months; average amount currently owed is £5,230 (IPSE, 2024).
- [verified] 53% of surveyed freelancers were paid late 4+ times in the last year; 58% struggled to cover living expenses due to late payments (Ruul, ~30,000 respondents, 2026).
- [verified] 65% of freelancers had an invoice dispute in the past year (Skynova, 510 freelancers) — but the top driver was invoice errors, with payment delays listed by 33%; there is no data in any source found measuring "late-fee amount disagreements" as a distinct category.
- [verified] 40% of freelancers do not request late fees to protect the client relationship; 25% do not know how to charge one (Ruul, 2026) — this is demand evidence for the general pain of late payments, and simultaneously adverse evidence for this specific product.
- [assumed] A meaningful share of freelancers would rather waive a fee than argue, and one-time clients whose debt exceeds the fee threshold are rare for solo service businesses.

## Counterevidence

1. **The premise is false: the math is not genuinely ambiguous.** The industry-standard formula (amount × rate × months/days-overdue, or a flat fee) is published everywhere; every dispute-resolution guide states that the dispute ends when the calculation is written out simply (Ruul, 2026; LancerWise, 2026; LegalClarity, 2026). What actually creates "different people calculating differently" — rate choice, simple vs. compound, proration method — is settled by the signed contract clause, not by a calculator. A tool that computes a number does not resolve a dispute with a client who never agreed to the clause in the first place.
2. **The target user's binding constraint is not arithmetic — it is willingness and contract.** The single most common reason late fees go uncollected is that there was no prior written agreement (LegalClarity, 2026; LancerWise, 2026; 1099Freelance, 2026); courts strike down undisclosed or punitive fees. Meanwhile 40% of freelancers skip fees to protect relationships and 25% don't know how to charge at all (Ruul, 2026). A statement generator addresses none of these failure modes; it produces the document the freelancer was already unwilling to send.
3. **The only segment that computes late fees by hand is already served, for free, by tools they own.** FreshBooks, QuickBooks Online, Bonsai, Agiled, HoneyBook, Invoice Ninja, and Xero apply late fees automatically inside the invoicing workflow; six-plus free no-signup calculators (InvoiceCat, ChaseAI, Plutio, Protawk, ClearReceivables, KipBill) generate the exact statement copy. The residual market is freelancers who (a) don't use invoicing software, (b) do charge fees, and (c) will pay $29 for a terminal tool — a population with no demonstrated existence.
4. **The social evidence cuts against the monetized habit.** One-time licensing ($29, MIT) of a CLI tool aimed at a non-technical persona: CLI-first finance tools are explicitly catalogued as developer tools with high learning curves (WelikeRemoteStack, 2026), and the fatigue/donation economics of freelancer invoicing skew to free tiers and $16–33/mo subscription suites (Wave free, Zoho free, FreshBooks $19). No survey in any of the sources reviewed shows freelancers paying one-time fees for statement utilities.
5. **Fee-amount disputes may not be a recurring event at all.** Most late payments are short: over 75% of late invoices are paid within 14 days of the due date and 90% within a month (Bonsai). For sub-$1,000 invoices a 1.5% fee is $7–15, and guides explicitly recommend waiving fees when the amount is trivial (Ruul, 2026). The population that (a) charges, (b) has a client who argues over the amount, and (c) argues at least once a quarter — Maya's implied usage rate — is a thin sliver of an already thin segment, and no source documents it.

## Risks

- **Technical:** trivial arithmetic with no defensible complexity; any spreadsheet or calculator replicates it end-to-end, so the tool's only differentiation would be statement formatting (with which the free calculators already ship).
- **Market:** the core job is already free or embedded in tools the persona already pays for; fee-amount disputes specifically are not a documented pain category in any survey reviewed, so willingness-to-pay is unproven at any price and most pessimistic at $29.
- **Distribution:** a CLI licensed one-time and MIT-licensed has no channel: terminal adoption is concentrated among developers, not designers; a senior solo web designer (Maya) is unlikely to install, run, or pay for command-line tooling; incumbents own the search/queries category with free calculators.