# BAC Datathon 2026, Round 2 (Team Nai Loong)

This folder is only for the NBS Business Analytics Club Datathon, Fri 30 Oct 2026. It has nothing to do with any other project.

## The task
Round 2: we get a real-world business problem statement and a dataset. We analyse it and pitch the findings to a panel of judges. The judges are business analytics people. They reward clear decisions backed by numbers, not clever code. Time is short (assume ~2.5 hours), so speed matters more than polish in the code.

The problem statement goes in `PROBLEM.md` and the dataset goes in `data/`. Read both before doing anything else.

## How to work
- **Use `helpers.py`**: `from helpers import *`. It already has load, clean, profile, by, rate, trend, top, crosstab, model, drivers, gains and segments. Don't rewrite these. Add new analysis as small scripts in `analysis/` (e.g. `analysis/03_churn_by_region.py`) so the work can be rerun.
- **Never modify files in `data/`.** Save cleaned data to `data/clean.parquet` (or .csv) and load from there afterwards.
- **Charts**: save to `charts/` with `save_chart()`. One message per chart, a title that states the finding (e.g. "Basic plan churns at 1.2x average", not "Churn by plan"), readable at slide size, and bar axes starting at 0.
- **Every number you report must come from code you ran.** Don't estimate or round in your head. Say n (sample size) next to rates.
- **Always compare against something**: overall average, baseline model, previous period. A number alone isn't an insight.
- Before trusting a headline number, break it down by the main segments (watch for Simpson's paradox) and check row counts after every merge.
- Check for leakage before modelling: drop columns that only exist because of the outcome (e.g. cancellation_date when predicting churn).
- Only model if it helps answer the business question. A descriptive question needs no model.
- When the problem is ambiguous, state the assumption you made in one line and keep going. Don't stop to ask unless the choice changes the whole direction.

## Keep `FINDINGS.md` updated
After each meaningful result, append to `FINDINGS.md`:
`### <finding as a headline>` / number + n / chart file / so-what for the business / confidence (high/med/low) and caveat.
The deck gets built from this file, so keep it accurate and short.

## Output style in chat
Short. Lead with the number and what it means. Tables over prose. No long code explanations unless asked.

## Pitch structure we're filling (7 slides)
1. Problem (one-sentence business question, who it's for, what it costs)
2. Data (size, time range, one line on cleaning)
3. Insight 1 (headline + chart + number)
4. Insight 2
5. Who to act on (model/segments: drivers, gains chart, vs baseline)
6. Recommendations (3 actions -> owner -> expected impact in $ or %)
7. Limits & next steps
