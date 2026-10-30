"""Section 9: limitations and extra data. Owner: Germaine drafts, Marcus adds."""
from nb import md, code

NUMS = '''# The limitation numbers, recomputed.
print(f"deaths are small-n sample rows: {int(df.died.sum())} across 4 years, {int(df[df.year == 2024].died.sum())} in 2024 (1-in-5 sample)")
print(f"mean weight 2023 -> 2024: {df[df.year == 2023].weight.mean():.1f} -> {df[df.year == 2024].weight.mean():.1f}")
print(f"location Not recorded, 2024: {df[df.year == 2024].location.eq('Not recorded').mean():.1%} of rows")
print(f"narrative cap: {df[df.year <= 2014].narrative.str.len().max()} chars before 2019, {df[df.year >= 2023].narrative.str.len().max()} after")
print(f"products present in only some years: {(df.groupby('product').year.nunique() < 4).sum()} of {df['product'].nunique()}")
print(f"e-bike rows 2024 (full definition): {int(df[(df.year == 2024) & df.ebike].shape[0])} -> wide uncertainty on any e-bike rate")'''

LIM = """### What this data cannot tell us
| Limit | Why it matters here | Data that would change the answer |
|---|---|---|
| **No exposure denominators** | E-bike sales grew fast, so injuries per ride may have fallen; the 151% rise in 65+ injuries is partly just more over-65s | E-bike sales/registrations and ride counts; Census population by age and year |
| **Sampling frame / weight change 2023→2024** | Mean weight +10.6% in one year; we cannot fully separate it from real growth | CPSC's weighting notes; the full (5x) NEISS file |
| **First product only** | "Fell out of bed, hit the floor" is coded once; bed vs floor is a coder's choice | A secondary-product field |
| **Narrative length changed** (142 → 400 chars in 2019) | Text searches find more in recent years by construction; we only compared 2023 vs 2024 | Consistent coding of mechanism (fall, collision) |
| **"Not recorded" location is 37% of 2024 rows** | Home share is a range (36% to 57%), not a point | Better location coding |
| **Product renames** | The e-bike "4x" is one; others may lurk in any multi-year comparison | A stable product crosswalk from CPSC |
| **Deaths are small-n** (56 rows in 2024) and **ER-only** | NEISS misses deaths before arrival and after admission; "deadly" is undercounted for every hazard | NVSS mortality data; hospital discharge data |
| **Admission is our only severity proxy** | No cost, length of stay or disability | Injury cost data; discharge records |
| **No campaign-effect data** | The 5-10% reduction is an assumption, not an estimate | Evaluations of past fall-prevention campaigns |"""

TAKE = """> **Takeaway (limits).** The verdicts on the three claims are robust to these limits (they rest on recoding and weighting facts visible in the data). The size of the recommendation's impact is not: population denominators, cost data and campaign evaluations would sharpen it, and exposure data could change the e-bike picture, though not the ranking. **Confidence: high** that the ranking survives; **low** on exact impact."""


def cells():
    return [
        md("## 9. Limitations and extra data  \n*Rubric: limitations.* What we cannot conclude, why it matters for this question, and what data would change the answer."),
        md("The limitation numbers, recomputed from the data so the slide can quote them."),
        code(NUMS),
        md(LIM),
        md(TAKE),
    ]
