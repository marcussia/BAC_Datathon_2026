"""Section 6: the real story, ageing and falls at home. Owner: Marcus (numbers) / Germaine (campaign angle)."""
from nb import md, code

AGE_YR = '''# National estimate by age band and year. Under-65 flat, 65+ up 151%.
ag = df.assign(band=np.where(df.over65, "65+", "under 65")).groupby(["year", "band"]).weight.sum().unstack()
ag["65+_share_%"] = ag["65+"] / ag.sum(axis=1) * 100
print((ag / [1e6, 1e6, 1]).round(2).rename(columns={"65+": "65+ (M)", "under 65": "under 65 (M)"}).to_string())
g_old, g_young = ag["65+"][2024] / ag["65+"][2005] - 1, ag["under 65"][2024] / ag["under 65"][2005] - 1
print(f"\\n2005 -> 2024: under-65 {g_young:+.1%} | 65+ {g_old:+.1%}")
d24 = df[df.year == 2024]
s75 = d24.loc[d24.over75, "weight"].sum() / EST[2024]
adm75 = (d24.admitted * d24.weight)[d24.over75].sum() / (d24.admitted * d24.weight).sum()
print(f"2024: 75+ = {s75:.1%} of visits (1 in {1 / s75:.1f}) and {adm75:.1%} of all hospital admissions")
SLIDE(3, "under-65 injuries growth 2005->2024 (%)", f"{g_young * 100:+.1f}")
SLIDE(3, "65+ injuries growth 2005->2024 (%)", f"{g_old * 100:+.1f}")
SLIDE(3, "65+ share of est 2005 -> 2024 (%)", f"{ag['65+_share_%'][2005]:.1f} -> {ag['65+_share_%'][2024]:.1f}")
SLIDE(3, "75+ share of 2024 visits / of 2024 admissions (%)", f"{s75 * 100:.1f} / {adm75 * 100:.1f}")'''

CH1 = '''fig, ax = plt.subplots()
x = np.arange(len(YEARS))
ax.bar(x - 0.2, ag["under 65"] / 1e6, 0.4, color=GREY, label="under 65")
ax.bar(x + 0.2, ag["65+"] / 1e6, 0.4, color=ORANGE, label="65 and over")
for i, yr in enumerate(YEARS):
    ax.text(i - 0.2, ag["under 65"][yr] / 1e6 + 0.15, f"{ag['under 65'][yr] / 1e6:.1f}M", ha="center")
    ax.text(i + 0.2, ag["65+"][yr] / 1e6 + 0.15, f"{ag['65+'][yr] / 1e6:.1f}M", ha="center")
ax.set_xticks(x, YEARS); ax.set_ylabel("national estimate (millions of ER visits)"); ax.legend(); ax.set_ylim(0, 13)
save_chart("c4_under65_vs_over65", f"Injuries to under-65s are flat since 2005 ({g_young:+.0%}); injuries to over-65s are up {g_old:+.0%}\\nn = {len(df):,} rows, weighted")'''

ADMIT = '''# Admission rate by age group, 2024. Why older adults dominate admissions even though kids have more visits.
ar = d24.groupby("age_group", observed=True).apply(lambda d: pd.Series({"rows": len(d), "est": d.weight.sum(), "admit_%": wrate(d, "admitted") * 100}))
print(ar.round(1).to_string())
SLIDE(3, "admission rate 75+ vs 5-14 (%)", f"{ar.loc['75+', 'admit_%']:.1f} vs {ar.loc['5-14', 'admit_%']:.1f}")
ax = ar["admit_%"].plot.bar(color=[GREY] * 5 + [ORANGE] * 2, rot=0)
for i, v in enumerate(ar["admit_%"]): ax.text(i, v + 0.5, f"{v:.0f}%", ha="center")
ax.set_ylabel("admitted to hospital, % of national estimate"); ax.set_xlabel("age group"); ax.set_ylim(0, ar["admit_%"].max() * 1.2)
save_chart("c4_admission_rate_by_age", f"1 in {100 / ar.loc['75+', 'admit_%']:.0f} injured over-75s is admitted, vs 1 in {100 / ar.loc['5-14', 'admit_%']:.0f} children\\n2024, n = {len(d24):,} rows")'''

PROD = '''# What injures older adults: top products and where it happens, 2024.
for lab, m in [("65+", d24.over65), ("75+", d24.over75)]:
    t = d24[m].groupby("product").weight.sum().sort_values(ascending=False).head(5)
    print(f"{lab} top products (est, 2024): " + " | ".join(f"{p[:28]} {v / 1e3:,.0f}k" for p, v in t.items()))
o = d24[d24.over75]
home_all = o.loc[o.location.eq("Home"), "weight"].sum() / o.weight.sum() * 100
home_known = o.loc[o.location.eq("Home"), "weight"].sum() / o.loc[~o.location.eq("Not recorded"), "weight"].sum() * 100
print(f"\\n75+ injuries at Home: {home_all:.1f}% of all | {home_known:.1f}% of known-location (Not recorded = {o.loc[o.location.eq('Not recorded'), 'weight'].sum() / o.weight.sum() * 100:.0f}%)")
print(f"75+ visits that are falls (narrative): {wrate(o.assign(f=o.fall.astype(int)), 'f') * 100:.0f}%")
dx = o[o.fall].groupby("diagnosis").weight.sum().sort_values(ascending=False).head(4)
bp = o[o.fall].groupby("body_part").weight.sum().sort_values(ascending=False).head(4)
print("75+ falls, top diagnoses: " + ", ".join(f"{k} {v / o[o.fall].weight.sum() * 100:.0f}%" for k, v in dx.items()))
print("75+ falls, top body parts: " + ", ".join(f"{k} {v / o[o.fall].weight.sum() * 100:.0f}%" for k, v in bp.items()))
SLIDE(3, "75+ share at Home (all / known location, %)", f"{home_all:.1f} / {home_known:.1f}")'''

RISE = '''# The products rising fastest since 2005 are bathroom and bedroom: the older-adult fall story, product by product.
pv = df.pivot_table(index="product", columns="year", values="weight", aggfunc="sum")
big = pv[(pv[2005] > 50000) & (pv[2024] > 50000)].copy()
big["x_2005_2024"] = big[2024] / big[2005]
big["65+_share_2024_%"] = d24[d24.over65].groupby("product").weight.sum().reindex(big.index).fillna(0) / big[2024] * 100
print("fastest risers (products > 50k est in both years):")
print((big.sort_values("x_2005_2024", ascending=False).head(8) / [1e3, 1e3, 1e3, 1e3, 1, 1]).round(1).rename(columns={2005: "2005 (k)", 2014: "2014 (k)", 2023: "2023 (k)", 2024: "2024 (k)"}).to_string())
print("\\nfastest fallers:")
print((big.sort_values("x_2005_2024").head(5) / [1e3, 1e3, 1e3, 1e3, 1, 1]).round(1).rename(columns={2005: "2005 (k)", 2014: "2014 (k)", 2023: "2023 (k)", 2024: "2024 (k)"}).to_string())'''

CH14 = '''# The decisive comparison: 75+ home-fall admissions vs e-bike admissions, 2024, two e-bike definitions.
hf = d24[d24.over75 & d24.fall_product & d24.location.eq("Home")]
hf_adm = (hf.admitted * hf.weight).sum()
eb_code = d24[d24["product"] == "Electric power-assisted pedal bicycles"]; eb_all = d24[d24.ebike]
adm = {"E-bikes\\n(2024 product code only)": (eb_code.admitted * eb_code.weight).sum(),
       "E-bikes\\n(narrative OR product family)": (eb_all.admitted * eb_all.weight).sum(),
       "75+ falls at home\\n(floors/stairs/furniture/bathroom)": hf_adm}
ns = {"E-bikes\\n(2024 product code only)": len(eb_code), "E-bikes\\n(narrative OR product family)": len(eb_all), "75+ falls at home\\n(floors/stairs/furniture/bathroom)": len(hf)}
ratio_code, ratio_all = hf_adm / adm["E-bikes\\n(2024 product code only)"], hf_adm / adm["E-bikes\\n(narrative OR product family)"]
print(f"75+ home-fall admissions {hf_adm:,.0f} (n = {len(hf):,} rows) | e-bike admissions: code-only {adm['E-bikes\\n(2024 product code only)']:,.0f} (n = {len(eb_code)}), full definition {adm['E-bikes\\n(narrative OR product family)']:,.0f} (n = {len(eb_all)})")
print(f"ratio: {ratio_code:.0f}x (code-only e-bike definition) | {ratio_all:.0f}x (full definition)  <- we quote the smaller one")
print(f"share of ALL 2024 admissions that are 75+ home falls on these products: {hf_adm / (d24.admitted * d24.weight).sum() * 100:.1f}%")
fs = d24[d24.over75 & (d24.product_group == "Floors, stairs & building parts") & d24.location.eq("Home")]
fs_adm = (fs.admitted * fs.weight).sum()
print(f"narrower definition, floors/stairs only at Home: {fs_adm:,.0f} admissions (n = {len(fs):,}) = {fs_adm / adm['E-bikes\\n(narrative OR product family)']:.0f}x e-bikes (full def)")
SLIDE(3, "75+ home-fall admissions 2024 (est)", f"{hf_adm:,.0f} (n = {len(hf):,})")
SLIDE(3, "75+ home-fall admissions / e-bike admissions (x), full e-bike def", f"{ratio_all:.0f} (code-only def: {ratio_code:.0f})")
fig, ax = plt.subplots()
ax.bar(list(adm), [v / 1e3 for v in adm.values()], color=[GREY, GREY, ORANGE])
for i, (k, v) in enumerate(adm.items()): ax.text(i, v / 1e3 + 3, f"{v / 1e3:,.0f}k admitted\\n(n = {ns[k]:,} rows)", ha="center")
ax.set_ylabel("hospital admissions, national estimate (thousands)"); ax.set_ylim(0, hf_adm / 1e3 * 1.3)
save_chart("c4_admissions_75plus_vs_ebike", f"Over-75s falling at home caused {ratio_all:.0f}x more hospital admissions than e-bikes in 2024\\nweighted; e-bike shown on both definitions")'''

DEATH = '''# Deaths, all 4 years: who and what.
dd = df[df.died == 1]
print(f"deaths: {len(dd)} rows | aged 65+: {int(dd.over65.sum())} ({dd.over65.mean():.0%}) | aged 75+: {int(dd.over75.sum())} ({dd.over75.mean():.0%})")
print("top products in deaths (rows):", dd["product"].value_counts().head(5).to_dict())
SLIDE(3, "share of all deaths aged 65+ (rows, 4 years)", f"{dd.over65.mean() * 100:.0f}% ({int(dd.over65.sum())} of {len(dd)})")'''

TAKE = """> **Takeaway (the real story).** Injuries to under-65s are flat since 2005 (+1%) while injuries to over-65s are up 151%; 65+ went from 12% to 26% of all ER product injuries. In 2024 one in six patients is over 75 and they are 43% of all hospital admissions, admitted 15 times as often as children (30% vs 2%). What hurts them is the home: floors, beds, stairs, bathrooms, and the products rising fastest since 2005 are toilets, beds and bathtubs. Over-75s falling at home on those products caused 23x more admissions than e-bikes (41x on the headline's own e-bike definition), 21% of all 2024 admissions, and 65+ are 43% of all deaths. **So what:** the hazard, the population and the place for the $10M are clear. **Confidence: medium-high.** Part of the 151% is simply more older people (no population denominator here); the within-hospital-type check in FINDINGS says it is not a sampling artefact."""


def cells():
    return [
        md("## 6. The real story: ageing and falls at home  \n*Rubric: insights.* Growth by age band, severity by age, what and where, the fastest-rising products, and the decisive admissions chart."),
        md("National estimate by age band and year. Why it matters: it splits the 20-year growth into 'more people' and 'older people'."),
        code(AGE_YR),
        md("Chart for slide 3: under-65 vs 65+ over four years."),
        code(CH1),
        md("Admission rate by age group, 2024. Why it matters: severity, not visit count, is what costs hospitals and lives."),
        code(ADMIT),
        md("Top products, home share and injury type for 65+/75+. Why it matters: it names the hazard and the room, which is what a campaign needs."),
        code(PROD),
        md("Fastest rising and falling products since 2005. Why it matters: bathroom and bedroom rising while ball sports fall is the ageing story told by products."),
        code(RISE),
        md("The decisive chart: admissions from over-75s falling at home vs e-bikes, on both e-bike definitions."),
        code(CH14),
        md("Deaths across all four years. Why it matters: it closes the 'deadly' argument."),
        code(DEATH),
        md(TAKE),
    ]
