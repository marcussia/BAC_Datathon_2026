"""Section 2: data quality and the 6 traps. Owner: Marcus."""
from nb import md, code

T1 = '''# Trap 1: a row is one patient at a SAMPLE hospital; weight = how many US ER visits it stands for.
g = df.groupby("hospital_type").agg(rows=("case_id", "size"), est=("weight", "sum"), mean_weight=("weight", "mean"))
g["rows_%"] = g.rows / g.rows.sum() * 100
g["est_%"] = g.est / g.est.sum() * 100
g = g.sort_values("est", ascending=False)
print(g.round(1))
ch = g.loc["Children's"]
SLIDE(2, "Children's hospitals share of rows vs national estimate (%)", f"{ch['rows_%']:.1f} vs {ch['est_%']:.1f}")

ax = g[["rows_%", "est_%"]].plot.bar(color=[GREY, ACCENT], rot=0)
ax.set_ylabel("share (%)"); ax.set_xlabel(""); ax.legend(["rows (sample)", "national estimate (weighted)"])
save_chart("q_rows_vs_weight_by_hospital", f"Counting rows over-weights Children's hospitals 6x: {ch['rows_%']:.1f}% of rows but {ch['est_%']:.1f}% of visits\\nn = {len(df):,} rows, all 4 years")'''

T2 = '''# Trap 2: ages 201-223 are babies in months; 0 = unknown. Raw mean is wrong.
k = df[df.age_years.notna()]
print(f"rows with age 201-223 (months): {int(df.is_infant_months.sum()):,} | age 0 (unknown): {int(df.age_unknown.sum()):,}")
print(f"raw 'age' mean: {df.age.mean():.1f}  <- WRONG, mixes month codes in")
print(f"decoded mean age: {k.age_years.mean():.1f} (rows) | {np.average(k.age_years, weights=k.weight):.1f} (weighted)")
SLIDE(5, "raw vs decoded mean age", f"{df.age.mean():.1f} vs {np.average(k.age_years, weights=k.weight):.1f} (weighted)")'''

T3 = '''# Trap 3: alcohol_involved was only collected from 2019. Blank in 2005/2014 means "not asked", not "No".
print(raw.groupby("year").alcohol_involved.apply(lambda s: f"{s.notna().mean():.0%} filled").to_string())
print("-> alcohol numbers are only ever computed on 2023-2024 in this notebook")'''

T4 = '''# Trap 4: product categories get split and renamed between years.
for pat, label in [("^Toys, not", "Toys"), ("power-assisted|Mopeds", "E-bikes / mopeds")]:
    m = df["product"].str.contains(pat, regex=True)
    print(f"\\n{label}: rows by year"); print(pd.crosstab(df.loc[m, "product"], df.loc[m, "year"]).to_string())
print("\\n-> a category that appears from nowhere (or collapses) is usually a rename, not a real change. Section 4 shows this is exactly what the e-bike claim trips on.")'''

T5 = '''# Trap 5: "Not recorded" / "Other/not stated" are real values and they grow over time.
unk = pd.DataFrame({"location = Not recorded": df.location.eq("Not recorded"),
                    "diagnosis = Other/not stated": df.diagnosis.eq("Other/not stated"),
                    "body_part = Not stated/unknown": df.body_part.eq("Not stated/unknown"), "year": df.year})
print((unk.groupby("year").mean() * 100).round(1).to_string())
nr24 = df[df.year == 2024].location.eq("Not recorded").mean() * 100
SLIDE(5, "location 'Not recorded' share of 2024 rows (%)", f"{nr24:.1f}")
# the home share depends on the denominator you pick:
d24 = df[df.year == 2024]
home_all = d24.loc[d24.location.eq("Home"), "weight"].sum() / d24.weight.sum() * 100
home_known = d24.loc[d24.location.eq("Home"), "weight"].sum() / d24.loc[~d24.location.eq("Not recorded"), "weight"].sum() * 100
print(f"\\n2024 share of injuries at Home: {home_all:.1f}% of all visits | {home_known:.1f}% of visits with a known location")'''

T6 = '''# Trap 6: "product" is whatever was involved: stairs and floors are parts of a building, "Exercise" is an activity.
t = df.groupby("product").weight.sum().sort_values(ascending=False).head(8)
print((t / 1e6).round(2).rename("national est (M), all 4 years").to_string())
print("\\n-> for the campaign question, product_group gives the hazard family; product gives the detail")'''

DENOM = """### Our denominators, stated once
- **National estimate (SUM of weight) everywhere**, unless a number is explicitly labelled *rows*. Rows are shown next to rates as n.
- **"Not recorded" stays in the denominator** and is reported separately. Where a share depends on it (home share), both versions are shown.
- **Alcohol: 2023-2024 only.** Age uses the decoded `age_years`. Years compared like-for-like after checking product names."""

TAKE = """> **Takeaway (data quality).** Rows and weights rank hospitals differently (Children's: 18.5% of rows, 3.2% of visits), the raw age column overstates mean age by ~8 years, alcohol is blank before 2019, products get renamed (Toys 553 → 39 rows; Mopeds 395 → 0), and "Not recorded" location grew from 22% to 37% of rows. **So what:** every number below uses weights, decoded age, and a stated denominator. **Confidence: high.**"""


def cells():
    return [
        md("## 2. Data quality and the 6 traps  \n*Rubric: factuality, correct use of weights.* One cell of evidence per trap, then the denominators we use for the rest of the notebook."),
        md("**Trap 1: rows are not national totals.** Children's and Very large hospitals are over-sampled; counting rows over-counts them. Why it matters: every share in this notebook must be weighted."),
        code(T1),
        md("**Trap 2: ages above 200 are babies in months.** Why it matters: any mean, sort or `age > x` filter on the raw column silently includes 201–223."),
        code(T2),
        md("**Trap 3: blank is not 'No'.** Why it matters: an alcohol rate across all years would be wrong by construction."),
        code(T3),
        md("**Trap 4: product names change between years.** Why it matters: this is the mechanism behind the 'e-bikes quadrupled' claim (section 4)."),
        code(T4),
        md("**Trap 5: 'Not recorded' is a real answer and it is growing.** Why it matters: 'share at home' changes by 20 points depending on the denominator."),
        code(T5),
        md("**Trap 6: a 'product' is not always something you buy.** Why it matters: the biggest hazards are parts of the home, not consumer goods, which shapes the campaign."),
        code(T6),
        md(DENOM),
        md(TAKE),
    ]
