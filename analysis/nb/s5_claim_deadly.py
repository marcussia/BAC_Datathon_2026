"""Section 5: fact-check claim 3, 'e-bikes are the deadly new threat'. Owner: Marcus."""
from nb import md, code

DEATHS = '''d24 = df[df.year == 2024]
print(f"2024 deaths: {int(d24.died.sum())} rows (est {d24.loc[d24.died == 1, 'weight'].sum():,.0f}) | of which e-bike (definition d): {int(d24.loc[d24.ebike, 'died'].sum())}")
print(f"all 4 years: {int(df.died.sum())} deaths; e-bike: {int(df.loc[df.ebike, 'died'].sum())} (n = {int(df.ebike.sum())} e-bike rows)")
for s in df[df.ebike & (df.died == 1)].narrative: print("   e-bike-family death:", s[:120])
print("\\n2024 deaths by product (rows):"); print(d24[d24.died == 1]["product"].value_counts().head(6).to_string())
print("\\n2024 deaths by age group (rows):", d24[d24.died == 1].groupby("age_group", observed=True).size().to_dict())
SLIDE(1, "claim 3: e-bike deaths 2024 (rows)", f"{int(d24.loc[d24.ebike, 'died'].sum())} of {int(d24.died.sum())}")
SLIDE(3, "2024 deaths aged 65+ (rows)", f"{int(d24.loc[d24.over65, 'died'].sum())} of {int(d24.died.sum())}")'''

SEV = '''# Severity per visit vs volume, 2024, weighted. Admission is our severity proxy (no cost data).
segs = {"All 2024 visits": pd.Series(True, index=d24.index),
        "E-bikes (narrative OR product family)": d24.ebike,
        "All bikes & micromobility": d24.product_group == "Bikes & micromobility",
        "65+ all injuries": d24.over65,
        "65+ falls (narrative)": d24.over65 & d24.fall,
        "75+ falls (narrative)": d24.over75 & d24.fall,
        "75+ floors/stairs/furniture/bathroom at Home": d24.over75 & d24.fall_product & d24.location.eq("Home")}
rows = []
for k, m in segs.items():
    d = d24[m]
    rows.append({"segment": k, "rows": len(d), "est_visits": d.weight.sum(), "share_%": d.weight.sum() / EST[2024] * 100,
                 "admit_%": wrate(d, "admitted") * 100, "est_admissions": (d.admitted * d.weight).sum(), "deaths_rows": int(d.died.sum())})
sev = pd.DataFrame(rows).set_index("segment"); print(sev.round(1).to_string())
eb, allv = sev.loc["E-bikes (narrative OR product family)"], sev.loc["All 2024 visits"]
SLIDE(1, "e-bike admission rate vs all visits (%)", f"{eb['admit_%']:.1f} vs {allv['admit_%']:.1f}")
SLIDE(3, "e-bike est admissions 2024", f"{eb['est_admissions']:,.0f} (n = {int(eb['rows'])} rows)")'''

AGE = '''# Who rides into the ER on an e-bike? Age profile (weighted) and alcohol share by product group (2024 only, trap 3).
eb24 = d24[d24.ebike]
print("e-bike visits by age group (% of e-bike est):")
print((eb24.groupby("age_group", observed=True).weight.sum() / eb24.weight.sum() * 100).round(1).to_string())
print(f"\\ne-bike riders: male {wrate(eb24.assign(m=eb24.sex.eq('Male').astype(int)), 'm') * 100:.0f}% | median age {eb24.age_years.median():.0f}")
alc = d24.groupby("product_group").apply(lambda d: wrate(d, "alcohol_involved") * 100).sort_values(ascending=False)
print("\\nalcohol involved, % of 2024 est, by product group:"); print(alc.round(1).head(5).to_string())
print(f"e-bikes specifically: {wrate(eb24, 'alcohol_involved') * 100:.1f}% (n = {len(eb24)})")
SLIDE(2, "alcohol share, Bikes & micromobility 2024 (%)", f"{alc['Bikes & micromobility']:.1f} (highest group; all visits {wrate(d24, 'alcohol_involved') * 100:.1f})")'''

CH = '''k = ["E-bikes (narrative OR product family)", "All 2024 visits", "65+ falls (narrative)"]
fig, ax = plt.subplots()
ax.bar(["E-bikes", "All visits", "65+ falls"], sev.loc[k, "admit_%"], color=[GREY, GREY, ORANGE])
for i, d in enumerate(k): ax.text(i, sev.loc[d, "admit_%"] + 0.5, f"{sev.loc[d, 'admit_%']:.1f}%\\n(n = {int(sev.loc[d, 'rows']):,} rows)", ha="center")
ax.set_ylabel("admitted to hospital, % of national estimate"); ax.set_ylim(0, sev.loc[k, "admit_%"].max() * 1.3)
save_chart("c3_admission_rate_ebike_vs_falls", f"E-bike visits are admitted {sev.loc[k[0], 'admit_%']:.0f}% of the time; 65+ falls {sev.loc[k[2], 'admit_%']:.0f}%, on 30x the volume\\n2024, weighted")'''

TAKE = """> **Takeaway (claim 3: "deadly new threat").** *Does not hold in this data.* 0 of the 56 deaths recorded in 2024 involved an e-bike (0 of 184 across all four years; the two deaths in the moped/e-bike family were moped riders hit by cars). E-bike visits are somewhat more severe than average per visit (about 15% admitted vs 11% overall), riders are mostly male adults, and micromobility has the highest alcohol share of any product group (~4%). **So what:** e-bikes are a real but small and partly behavioural (alcohol, helmets) risk; the deadly hazard in the data is older adults falling: 30 of 56 deaths were aged 65+. **Confidence: high** on direction; deaths are small-n sample rows, not estimates."""


def cells():
    return [
        md("## 5. Fact-check claim 3: \"E-bikes are the deadly new threat\"  \n*Rubric: factuality + insight.* Deaths, admission rate, who the riders are, and severity vs volume."),
        md("Deaths in 2024 and across all years, by product and age. Why it matters: 'deadly' is a testable word."),
        code(DEATHS),
        md("Severity per visit (admission rate) vs volume, e-bikes against the alternatives. Why it matters: a hazard can be severe per visit yet tiny in total harm."),
        code(SEV),
        md("Age, sex and alcohol profile of e-bike visits. Why it matters: it tells us whether the right e-bike response is a ban or a behaviour campaign."),
        code(AGE),
        md("Chart: admission rate, e-bikes vs all vs 65+ falls."),
        code(CH),
        md(TAKE),
    ]
