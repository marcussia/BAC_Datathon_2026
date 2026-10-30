"""B6. Forward look to 2026 (the campaign year): 65+ home-fall admissions vs an e-bike worst case.
Log-linear trend on est admissions. Two fits: 2005-2023 (avoids the 2024 re-weighting) and 2005-2024.
E-bike: 2024 base x growth scenarios (1.2x like-for-like, 1.5x, 2x per year). Chart: charts/b_projection_2026.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = load("data/clean.parquet")
df["adm_w"] = df.weight * df.admitted
FALL = ["Floors or flooring materials", "Rugs or carpets, not specified", "Runners, throw rugs or doormats", "Stairs or steps",
        "Beds or bedframes, other or not specified", "Bathtubs or showers", "Toilets"]
EB = r"E-BIKE|EBIKE|E BIKE|E-BICYCLE|ELECTRIC BIKE|ELEC BIKE|ELECTRIC BICYCLE|ELECTRIC PEDAL|PEDAL ASSIST|MOTORIZED BI"
old = df[df["product"].isin(FALL) & (df.age_years >= 65)]
adm = old.groupby("year").adm_w.sum(); vis = old.groupby("year").weight.sum(); n = old.groupby("year").size()
print("65+ home-fall products, est admissions:", adm.round(0).to_dict(), "| n rows:", n.to_dict())


def proj(series, years_fit, target=2026):
    x = np.array(years_fit, float); yv = np.log(series.loc[years_fit].values)
    b, a = np.polyfit(x, yv, 1)
    return np.exp(a + b * target), np.exp(b) - 1


rows = []
for label, yrs in [("fit 2005-2023 (excludes 2024 re-weight)", [2005, 2014, 2023]), ("fit 2005-2024", [2005, 2014, 2023, 2024])]:
    p26, g = proj(adm, yrs); pv, gv = proj(vis, yrs)
    rows.append({"basis": label, "annual_growth_adm": g, "adm_2026": p26, "visits_2026": pv})
    print(f"{label}: admissions grow {g:.1%}/yr -> 2026 = {p26:,.0f}; visits grow {gv:.1%}/yr -> 2026 = {pv:,.0f}")
pt = pd.DataFrame(rows)
lo, hi = pt.adm_2026.min(), pt.adm_2026.max()

eb = df[(df.narrative.fillna("").str.contains(EB, regex=True) | df["product"].eq("Electric power-assisted pedal bicycles")) & (df.year == 2024)]
eb_adm = eb.adm_w.sum(); eb_vis = eb.weight.sum()
print(f"\ne-bike 2024: {eb_vis:,.0f} visits, {eb_adm:,.0f} admissions (n = {len(eb)})")
sc = pd.DataFrame({"scenario": ["1.2x/yr (like-for-like 2023->24)", "1.5x/yr (narrative growth 2023->24)", "2x/yr", "4x/yr (the headline, every year)"],
                   "growth": [1.2, 1.5, 2.0, 4.0]})
sc["ebike_adm_2026"] = eb_adm * sc.growth ** 2
sc["65plus_fall_adm_2026_low"] = lo; sc["ratio_low"] = lo / sc.ebike_adm_2026
print(sc.round({"growth": 1, "ebike_adm_2026": 0, "65plus_fall_adm_2026_low": 0, "ratio_low": 0}).to_string(index=False))
pd.concat([pt, sc], axis=1).to_csv("analysis/26_projection_2026.csv", index=False)
print(f"\nEven at 4x a year, e-bikes reach {sc.ebike_adm_2026.iloc[-1]:,.0f} admissions in 2026 vs {lo:,.0f}-{hi:,.0f} for 65+ home falls "
      f"({lo/sc.ebike_adm_2026.iloc[-1]:.0f}x). At the like-for-like 1.2x, the gap is {lo/sc.ebike_adm_2026.iloc[0]:.0f}x.")

# chart
fig, ax = plt.subplots(figsize=(10, 5.8))
yrs = [2005, 2014, 2023, 2024]
ax.plot(yrs, adm.loc[yrs] / 1e3, marker="o", lw=2.5, color=ORANGE, label="65+ home-fall admissions (observed)")
x = np.array([2005, 2014, 2023, 2024, 2026]); b, a = np.polyfit([2005, 2014, 2023], np.log(adm.loc[[2005, 2014, 2023]].values), 1)
ax.plot(x, np.exp(a + b * x) / 1e3, ls="--", color=ORANGE, lw=1.5, label="trend fitted on 2005-2023")
ax.fill_between([2026], [lo / 1e3], [hi / 1e3], color=ORANGE, alpha=0.3)
ax.scatter([2026], [(lo + hi) / 2e3], color=ORANGE, s=80); ax.text(2026.1, hi / 1e3, f"2026: {lo/1e3:,.0f}-{hi/1e3:,.0f}k", fontsize=12, va="bottom", ha="right")
ax.plot([2024, 2026], [eb_adm / 1e3, sc.ebike_adm_2026.iloc[-1] / 1e3], marker="o", color=ACCENT, lw=2.5, label="e-bike admissions if they 4x EVERY year")
ax.text(2026.1, sc.ebike_adm_2026.iloc[-1] / 1e3 + 15, f"e-bikes at 4x/yr: {sc.ebike_adm_2026.iloc[-1]/1e3:,.0f}k", color=ACCENT, fontsize=12, ha="right")
ax.set_ylim(0, hi / 1e3 * 1.18); ax.set_xlim(2003, 2027.5); ax.set_ylabel("hospital admissions per year (thousands, est)"); ax.legend(loc="upper left")
save_chart("b_projection_2026", f"In 2026, 65+ home falls will send ~{lo/1e3:,.0f}-{hi/1e3:,.0f}k people to a hospital bed; e-bikes at 4x a year would reach {sc.ebike_adm_2026.iloc[-1]/1e3:,.0f}k")
