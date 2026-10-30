---
description: Audit every number in DECK.md against the executed notebook and the data before we present
---
1. Read `analysis/slide_numbers.csv` (written by the notebook's appendix cell; every `SLIDE n:` print lands there). If it is older than `analysis/build_notebook.py` or any file in `analysis/nb/`, run `/notebook` first.
2. Go through every number in DECK.md slide by slide. For each one report: number | slide | source (`SLIDE` label, or FINDINGS.md entry, or none) | recomputed value | match?
   - If the number has a `SLIDE` label, compare to `slide_numbers.csv`.
   - If not, recompute it from `data/clean.parquet` with code, and add a `SLIDE(n, ...)` call to the right section module so the notebook covers it next build.
3. Flag anything that doesn't match, has no n, uses rows where a national estimate was meant (or vice versa), or claims causation from a correlation.
4. Check every chart file referenced in DECK.md exists in `analysis/charts/` or `charts/`.
5. Fix DECK.md and FINDINGS.md where they are wrong and tell me exactly what changed.
$ARGUMENTS
