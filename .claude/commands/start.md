---
description: Kick off Round 2 - read the problem, load and profile the data, propose the plan
---
1. Read PROBLEM.md and list every file in data/ (for Excel files, list the sheet names and shapes).
2. Load the data with helpers.load(), run clean() and profile(). If there are several tables, figure out the join keys, merge them and check the row counts.
3. Save the cleaned data to data/clean.parquet.
4. Reply with:
   - the business question in one sentence and who the client is
   - a data summary: rows, columns, date range, the target/outcome column if there is one, data quality problems
   - 5 to 8 specific hypotheses worth testing, ranked by likely business impact, each naming the columns it uses
   - whether a model is worth building for this problem, and why
Keep it tight. Don't start the analysis until I pick the hypotheses.

$ARGUMENTS
