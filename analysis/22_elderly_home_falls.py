"""B2. Deep-dive: 65+ injuries from floors, stairs, beds and bathroom fixtures (the home-fall products).
Chart: charts/b_65_homefall_trend.png (est visits and admissions 2005 -> 2024)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = load("data/clean.parquet")
FALL_PRODUCTS = {"Floors or flooring materials": "Floors", "Rugs or carpets, not specified": "Floors",
                 "Runners, throw rugs or doormats": "Floors", "Stairs or steps": "Stairs",
                 "Beds or bedframes, other or not specified": "Beds", "Bathtubs or showers": "Bathroom",
                 "Toilets": "Bathroom"}
df["fall_product"] = df["product"].map(FALL_PRODUCTS)
df["adm_w"] = df.weight * df.admitted
df["died_w"] = df.weight * df.died
old = df[df.fall_product.notna() & (df.age_years >= 65)].copy()
o24 = old[old.year == 2024]
all24 = df[df.year == 2024]


def agg(x):
    return pd.Series({"est_visits": x.weight.sum(), "est_admissions": x.adm_w.sum(), "est_deaths": x.died_w.sum(),
                      "n_rows": len(x), "adm_rate_%": x.adm_w.sum() / x.weight.sum() * 100})


print("=== 65+ home-fall products, 2024 ===")
s = agg(o24)
print(s.round(1).to_string())
print(f"share of ALL 2024 visits {s.est_visits/all24.weight.sum():.1%} | of ALL admissions "
      f"{s.est_admissions/all24.adm_w.sum():.1%} | of ALL deaths {s.est_deaths/all24.died_w.sum():.1%} "
      f"(deaths n = {int(o24.died.sum())} rows)")
print(f"narrative mentions FELL/FALL/SLIP/TRIP in {o24.narrative.str.contains('FELL|FALL|SLIP|TRIP').mean():.0%} of these rows")
print("\nby product (2024):\n", o24.groupby("fall_product").apply(agg, include_groups=False).round(1).sort_values("est_admissions", ascending=False).to_string())

tr = old.groupby("year").apply(agg, include_groups=False).round(1)
tr["all_injuries_est"] = df.groupby("year").weight.sum()
tr["share_of_all_%"] = (tr.est_visits / tr.all_injuries_est * 100).round(1)
print("\n=== trend ===\n", tr.to_string())
print(f"visits x{tr.est_visits[2024]/tr.est_visits[2005]:.1f}, admissions x{tr.est_admissions[2024]/tr.est_admissions[2005]:.1f} "
      f"(2005 -> 2024) vs all injuries x{tr.all_injuries_est[2024]/tr.all_injuries_est[2005]:.2f}")
tr75 = old[old.age_years >= 75].groupby("year").apply(agg, include_groups=False).round(1)
print("\n75+ only:\n", tr75.to_string())

# location: both denominators
loc = o24.groupby("location").weight.sum()
known = loc.drop("Not recorded")
print(f"\nlocation 2024: Home = {loc['Home']/loc.sum():.1%} of all (Not recorded = {loc['Not recorded']/loc.sum():.1%}) "
      f"| Home = {known['Home']/known.sum():.1%} of KNOWN location (n known = {int((o24.location!='Not recorded').sum()):,} of {len(o24):,}); "
      f"next: Other public property {known['Other public property']/known.sum():.1%} (nursing homes etc.)")
bp = (o24.groupby("body_part").weight.sum() / o24.weight.sum() * 100).nlargest(6).round(1)
dx = (o24.groupby("diagnosis").weight.sum() / o24.weight.sum() * 100).nlargest(6).round(1)
print("\ntop body parts (est %):", bp.to_dict())
print("top diagnoses (est %):", dx.to_dict())
adm_bp = o24.groupby("body_part").apply(lambda x: x.adm_w.sum() / x.weight.sum() * 100, include_groups=False)
print("admission rate by body part:", adm_bp.loc[["Upper leg", "Lower trunk", "Head", "Upper trunk", "Face", "Wrist"]].round(1).to_dict())
print(f"HIP in narrative: {o24.narrative.str.contains('HIP').mean():.1%} of rows; female share {o24[o24.sex=='Female'].weight.sum()/o24.weight.sum():.1%}; "
      f"median age {o24.age_years.median():.0f}")

# chart: trend
fig, ax = plt.subplots(figsize=(10, 5.6))
yrs = tr.index.astype(str)
ax.bar(yrs, tr.est_visits / 1e6, color=GREY, label="ER visits")
ax.bar(yrs, tr.est_admissions / 1e6, color=ORANGE, label="of which admitted")
for i, y in enumerate(tr.index):
    ax.text(i, tr.est_visits[y] / 1e6 + 0.03, f"{tr.est_visits[y]/1e6:.2f}M\n({tr['adm_rate_%'][y]:.0f}% admitted)", ha="center", fontsize=11)
ax.set_ylim(0, tr.est_visits.max() / 1e6 * 1.25); ax.set_ylabel("national estimate (millions)"); ax.legend(loc="upper left")
save_chart("b_65_homefall_trend", f"65+ falls on floors, stairs, beds and bathrooms: {tr.est_visits[2024]/1e6:.1f}M ER visits in 2024, "
                                    f"x{tr.est_visits[2024]/tr.est_visits[2005]:.1f} since 2005 (all injuries x{tr.all_injuries_est[2024]/tr.all_injuries_est[2005]:.1f})")
