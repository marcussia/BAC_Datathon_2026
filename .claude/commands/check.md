---
description: Audit every number in DECK.md against the data before we present
---
Go through every number in DECK.md (and FINDINGS.md). For each one, recompute it from data/clean.parquet with code and report: number | slide | recomputed value | match? Flag anything that doesn't match, has no n, or claims causation from a correlation. Also check the referenced chart files exist. Fix FINDINGS.md and DECK.md where they are wrong and tell me what changed.
