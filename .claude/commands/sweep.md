---
description: Slice the outcome by every segment column and rank the biggest gaps
---
Load data/clean.parquet. For the outcome column ($ARGUMENTS, or the one identified in /start):
- if it's 0/1: run rate() against every categorical column with 2 to 25 categories and against quartiles of each numeric column
- if it's numeric: compare the mean and total by the same groups, using by()
Ignore groups with n < 30.

Return one table ranked by size of gap vs the overall average: column | group | value | overall | lift | n | share of rows.
Then name the top 3 gaps that look like real business insights (not artefacts or tiny groups) and say which deserve a chart. Save charts only for those 3.
