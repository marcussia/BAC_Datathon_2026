---
description: Build baseline-vs-model comparison, drivers and gains chart
---
Target: $ARGUMENTS

1. Load data/clean.parquet. List the columns that could leak the answer and drop them; tell me which ones you dropped and why.
2. Run helpers.model() with the right id_cols/drop_cols, then drivers(). Run gains() if the target is yes/no.
3. Reply with:
   - the metrics table (best model vs baseline)
   - the top 5 drivers in plain English, with direction (e.g. "short tenure -> more churn")
   - the gains headline ("target the top 20%, catch X%")
   - one sentence a non-technical judge would understand
4. Append the result to FINDINGS.md.
