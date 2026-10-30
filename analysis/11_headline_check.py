"""Fact-check the headline: 18% surge, e-bikes quadrupled, e-bikes deadly. Compare with 65+ falls."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
pd.set_option("display.max_rows", 100); pd.set_option("display.width", 220); pd.set_option("display.max_colwidth", 120)
df = load("data/clean.parquet")
w = df.weight
def H(t): print(f"\n{'='*8} {t} {'='*8}")
def est(m): return df.loc[m, "weight"].sum()

H("CLAIM 1: 18% surge. rows vs est, 2023 -> 2024")
y = df.groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"), mean_w=("weight", "mean"))
y["rows_chg_%"] = y.rows.pct_change() * 100; y["est_chg_%"] = y.est.pct_change() * 100; y["mean_w_chg_%"] = y.mean_w.pct_change() * 100
print(y.round(2))
H("by hospital_type 2023 vs 2024")
h = df[df.year >= 2023].groupby(["hospital_type", "year"]).agg(rows=("case_id", "size"), est=("weight", "sum"), mean_w=("weight", "mean")).unstack("year")
h["rows_chg_%"] = (h["rows"][2024] / h["rows"][2023] - 1) * 100
h["est_chg_%"] = (h["est"][2024] / h["est"][2023] - 1) * 100
h["mean_w_chg_%"] = (h["mean_w"][2024] / h["mean_w"][2023] - 1) * 100
print(h.round(1))
H("counterfactual: 2024 rows x 2023 mean weight per hospital type")
cf = (h["rows"][2024] * h["mean_w"][2023]).sum()
print(f"2023 est {y.est[2023]:,.0f} | 2024 actual {y.est[2024]:,.0f} (+{y['est_chg_%'][2024]:.1f}%) | 2024 at 2023 weights {cf:,.0f} (+{(cf / y.est[2023] - 1) * 100:.1f}%)")

H("CLAIM 2: e-bikes. Products with power-assist / electric / moped wording, by year (rows | est)")
pm = df["product"].str.contains(r"power-assist|electric|moped|e-bike|ebike", case=False, regex=True)
print(pd.crosstab(df.loc[pm, "product"], df.loc[pm, "year"]).to_string())
print(df[pm].pivot_table(index="product", columns="year", values="weight", aggfunc="sum").round(0).fillna(0).to_string())

N = df.narrative.fillna("")
ebike_re = r"\bE-?BIKE|\bE BIKE|ELECTRIC BI(KE|CYCLE)|ELEC\.? BI(KE|CYCLE)|ELECTRIC PEDAL|PEDAL ASSIST|POWER ASSIST|MOTORI[ZS]ED BI(KE|CYCLE)|\bE-?BICYCLE"
nb = N.str.contains(ebike_re, regex=True)
H("narrative-defined e-bike rows by year")
print(pd.DataFrame({"rows": nb.groupby(df.year).sum(), "est": w[nb].groupby(df.year).sum().round(0),
                    "share_of_year_est_%": (w[nb].groupby(df.year).sum() / y.est * 100).round(3)}))
H("what products are narrative e-bike rows coded as, 2023 vs 2024")
print(pd.crosstab(df.loc[nb & (df.year >= 2023), "product"], df.loc[nb & (df.year >= 2023), "year"]).sort_values(2024, ascending=False).head(12).to_string())
H("sample 2023 narrative e-bike matches (check for false positives)")
for s in df[nb & (df.year == 2023)].narrative.sample(12, random_state=1): print(" -", s[:110])
H("the 'quadrupled' candidates")
p24 = "Electric power-assisted pedal bicycles"; pm23 = "Mopeds or power-assisted cycles"
print("product 'Electric power-assisted pedal bicycles' rows/est by year:", df[df["product"] == p24].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum")).round(0).to_dict("index"))
print("product 'Mopeds or power-assisted cycles' by year:", df[df["product"] == pm23].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum")).round(0).to_dict("index"))
fam = df["product"].isin([p24, "Power-assisted cycles, not elsewhere classified", pm23])
f = df[fam & (df.year >= 2023)].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"))
print("PRODUCT FAMILY (2023 Mopeds/power-assisted -> 2024 Electric pedal + Power-assisted NEC):\n", f.round(0), f"\n  growth est {f.est[2024] / f.est[2023]:.2f}x")
H("sample narratives: 2023 'Mopeds or power-assisted cycles' / 2024 'Power-assisted cycles NEC'")
for s_ in df[(df["product"] == pm23) & (df.year == 2023)].narrative.sample(8, random_state=2): print(" 23-", s_[:110])
for s_ in df[(df["product"] == "Power-assisted cycles, not elsewhere classified")].narrative.sample(8, random_state=2): print(" 24-", s_[:110])
H("growth 2024 vs 2014 (10 yrs) and 2024 vs 2005")
print(f"est 2024/2014 {y.est[2024] / y.est[2014] - 1:+.1%} | rows {y.rows[2024] / y.rows[2014] - 1:+.1%} | est 2024/2005 {y.est[2024] / y.est[2005] - 1:+.1%}")
union = nb | fam
u = df[union & (df.year >= 2023)].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"))
print("UNION (narrative OR 2024 e-bike product codes):\n", u.round(0), f"\n  growth est {u.est[2024] / u.est[2023]:.2f}x | rows {u.rows[2024] / u.rows[2023]:.2f}x")
n23, n24 = nb[df.year == 2023].sum(), nb[df.year == 2024].sum()
print(f"narrative-only growth: rows {n24 / n23:.2f}x | est {w[nb & (df.year == 2024)].sum() / w[nb & (df.year == 2023)].sum():.2f}x")

H("CLAIM 3: deadly. deaths and admissions")
d24 = df[df.year == 2024]
eb24 = union & (df.year == 2024)
print(f"2024 deaths: total rows {int(d24.died.sum())} | e-bike (union def) rows {int(df.loc[eb24, 'died'].sum())}")
print("all-years deaths, e-bike union def:", int(df.loc[union, "died"].sum()), "| all-years e-bike rows:", int(union.sum()))
print("e-bike death narratives:"); [print(" -", s[:150]) for s in df[union & (df.died == 1)].narrative]

H("SEVERITY per visit, 2024 (weighted)")
fall_re = r"\bF[AE]LL|\bFALL|\bSLIP|\bTRIP"
falls = N.str.contains(fall_re, regex=True)
fall_prod = df.product_group.isin(["Floors, stairs & building parts", "Furniture", "Bathroom"])
old = df.age_years >= 65
segs = {"All 2024 visits": df.year == 2024,
        "E-bike (narrative or product)": eb24,
        "All bikes & micromobility": (df.product_group == "Bikes & micromobility") & (df.year == 2024),
        "65+ all injuries": old & (df.year == 2024),
        "65+ falls (narrative FELL/FALL/SLIP/TRIP)": old & falls & (df.year == 2024),
        "65+ floors/stairs/furniture/bathroom": old & fall_prod & (df.year == 2024),
        "65+ falls at home (known location)": old & falls & (df.year == 2024) & (df.location == "Home")}
rows = []
for k, m in segs.items():
    d = df[m]
    rows.append({"segment": k, "rows": len(d), "est_visits": d.weight.sum(), "share_of_2024_%": d.weight.sum() / y.est[2024] * 100,
                 "admit_%": np.average(d.admitted, weights=d.weight) * 100 if len(d) else np.nan,
                 "est_admissions": (d.admitted * d.weight).sum(), "deaths_rows": int(d.died.sum()), "deaths_est": (d.died * d.weight).sum()})
sev = pd.DataFrame(rows).set_index("segment"); print(sev.round(1).to_string())
sev.to_csv("analysis/11_severity_2024.csv")

H("65+ falls trend (narrative def), est by year + share of all visits")
t = df[old & falls].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"), adm=("admitted", lambda s: (s * df.loc[s.index, "weight"]).sum()))
t["share_%"] = t.est / y.est * 100; print(t.round(0))
print("65+ share of all est by year %:", (df[old].groupby("year").weight.sum() / y.est * 100).round(1).to_dict())
H("65+ share within each hospital type (est %), 2005 vs 2024 - is ageing just sample change?")
print(df[df.year.isin([2005, 2024])].assign(o=old).groupby(["hospital_type", "year"]).apply(lambda d: np.average(d.o, weights=d.weight) * 100).unstack().round(1))

H("2024 deaths by age group and by product (top)")
print(d24[d24.died == 1].groupby("age_group", observed=True).size().to_dict())
print(d24[d24.died == 1]["product"].value_counts().head(6).to_dict())

# ---- charts
fig, ax = plt.subplots()
lab = ["2023", "2024"]; x = np.arange(2)
ax.bar(x - 0.2, [y.rows[2023] / 1e3, y.rows[2024] / 1e3], 0.4, label="sample rows (k)", color=GREY)
ax.bar(x + 0.2, [y.est[2023] / 1e5, y.est[2024] / 1e5], 0.4, label="national estimate (100k)", color=ACCENT)
for i, (r, e) in enumerate(zip(y.rows[[2023, 2024]], y.est[[2023, 2024]])):
    ax.text(i - 0.2, r / 1e3 + 1, f"{r / 1e3:.1f}k", ha="center"); ax.text(i + 0.2, e / 1e5 + 1, f"{e / 1e6:.2f}M", ha="center")
ax.set_xticks(x, lab); ax.set_ylim(0, 175); ax.legend(loc="upper left"); ax.set_ylabel("")
save_chart("a_surge_rows_vs_weight", f"The '18% surge' is +{y['est_chg_%'][2024]:.0f}% by weight but only +{y['rows_chg_%'][2024]:.0f}% by actual ER visits sampled")

fig, ax = plt.subplots()
vals = [u.est[2023] / 1e3, u.est[2024] / 1e3]
ax.bar(lab, vals, color=[GREY, ACCENT]); [ax.text(i, v + 2, f"{v:,.0f}k", ha="center") for i, v in enumerate(vals)]
ax.set_ylim(0, max(vals) * 1.25); ax.set_ylabel("est. e-bike ER visits (thousands)")
save_chart("a_ebike_like_for_like", f"Like-for-like, e-bike ER visits grew {u.est[2024] / u.est[2023]:.1f}x, not 4x, and are {u.est[2024] / y.est[2024] * 100:.1f}% of all visits")

s = sev.loc[["E-bike (narrative or product)", "All bikes & micromobility", "65+ falls (narrative FELL/FALL/SLIP/TRIP)"]]
fig, ax = plt.subplots()
ax.bar(["E-bikes", "All bikes &\nmicromobility", "65+ falls"], s.est_admissions / 1e3, color=[GREY, GREY, ORANGE])
for i, (v, p) in enumerate(zip(s.est_admissions / 1e3, s["admit_%"])): ax.text(i, v + 5, f"{v:,.0f}k admitted\n({p:.0f}% of visits)", ha="center")
ax.set_ylim(0, s.est_admissions.max() / 1e3 * 1.3); ax.set_ylabel("est. hospital admissions, 2024 (thousands)")
save_chart("a_admissions_ebike_vs_falls", f"65+ falls caused {s.est_admissions.iloc[2] / s.est_admissions.iloc[0]:.0f}x more hospital admissions than e-bikes in 2024")
