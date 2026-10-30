"""B1. 2024 hazard map: est visits, admissions, deaths by product_group x age_group (weighted).
Chart: charts/b_adm_rate_by_group.png (admission rate per product group, 65+ vs under-65)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = load("data/clean.parquet")
d = df[df.year == 2024].copy()
d["adm_w"] = d.weight * d.admitted
d["died_w"] = d.weight * d.died


def agg(x):
    return pd.Series({"est_visits": x.weight.sum(), "est_admissions": x.adm_w.sum(), "est_deaths": x.died_w.sum(),
                      "n_rows": len(x), "adm_rate_%": x.adm_w.sum() / x.weight.sum() * 100})


hm = d.groupby(["product_group", "age_group"], observed=True).apply(agg, include_groups=False).round(1)
hm.to_csv("analysis/21_hazard_map_2024.csv")
print("=== 2024 hazard map (est), top 15 cells by admissions ===")
print(hm.sort_values("est_admissions", ascending=False).head(15).to_string())

tot = d.groupby("product_group").apply(agg, include_groups=False).sort_values("est_admissions", ascending=False).round(1)
print("\n=== by product group (2024, est) ===\n", tot.to_string())
age = d.groupby("age_group", observed=True).apply(agg, include_groups=False).round(1)
print("\n=== by age group (2024, est) ===\n", age.to_string())
print(f"\n65+ = {age.loc['65+','est_visits']/age.est_visits.sum():.1%} of visits, "
      f"{age.loc['65+','est_admissions']/age.est_admissions.sum():.1%} of admissions, "
      f"{age.loc['65+','est_deaths']/age.est_deaths.sum():.1%} of deaths (n = {int(age.loc['65+','n_rows']):,} rows)")

# chart: admission rate by product group, 65+ vs under-65
d["is65"] = np.where(d.age_group.astype(str) == "65+", "65+", "under 65")
r = d.groupby(["product_group", "is65"]).apply(lambda x: x.adm_w.sum() / x.weight.sum() * 100, include_groups=False).unstack()
n65 = d[d.is65 == "65+"].groupby("product_group").size()
r = r.loc[tot.index]  # order by total admissions
overall65 = d[d.is65 == "65+"].adm_w.sum() / d[d.is65 == "65+"].weight.sum() * 100
overallu = d[d.is65 != "65+"].adm_w.sum() / d[d.is65 != "65+"].weight.sum() * 100
fig, ax = plt.subplots(figsize=(11, 6.2))
y = np.arange(len(r))[::-1]
ax.barh(y + 0.2, r["under 65"], 0.4, color=GREY, label=f"under 65 (avg {overallu:.1f}%)")
ax.barh(y - 0.2, r["65+"], 0.4, color=ORANGE, label=f"65+ (avg {overall65:.1f}%)")
ax.set_yticks(y); ax.set_yticklabels([f"{g}  (65+ n={n65.get(g,0):,})" for g in r.index])
ax.set_xlim(0, max(r.max()) * 1.12); ax.set_xlabel("share of ER visits admitted to hospital, 2024 (%)")
ax.legend(loc="lower right")
ratio = overall65 / overallu
save_chart("b_adm_rate_by_group", f"Over-65s are admitted at {ratio:.1f}x the rate of under-65s, in every product group")
print(f"\n65+ admission rate {overall65:.1f}% vs under-65 {overallu:.1f}% ({ratio:.1f}x); ratio range by group: "
      f"{(r['65+']/r['under 65']).min():.1f}x to {(r['65+']/r['under 65']).max():.1f}x")
print(r.round(1).to_string())
