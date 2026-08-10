# Contributing

Contributions are welcome once the incubator has real experiments running. Two rules apply from day one:

## 1. Sign your commits (DCO)

Every commit in a pull request must be signed off:

```bash
git commit -s -m "your message"
```

This adds a `Signed-off-by:` line certifying the [Developer Certificate of Origin](https://developercertificate.org/) — that you have the right to contribute the code and agree it ships under this repo's license. Plain English: it keeps the project's licensing clean and preserves the maintainer's ability to adjust licensing later without hunting down every past contributor. Unsigned commits can't be merged.

## 2. Contracts are frozen during experiments

Files in `pipeline/` are versioned measurement instruments. While a pre-registered experiment is running, changes to them are not merged — they'd invalidate in-flight runs. Propose the change; it lands when the experiment completes.
