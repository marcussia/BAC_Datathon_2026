---
description: Turn one hypothesis into a verified, slide-ready insight
---
Hypothesis to test: $ARGUMENTS

1. Write a short script in analysis/ that tests it on data/clean.parquet, and run it.
2. Check that it holds up: break it down by the 1 or 2 main segments, check n, and say whether the gap is big enough to matter (use a quick significance test if it's borderline).
3. If it holds, make ONE slide-ready chart with a title that states the finding and save it with save_chart().
4. Append it to FINDINGS.md in the standard format.
5. Reply with: verdict (holds / partly / doesn't), the headline number with n, the chart path, and a one-line so-what.
