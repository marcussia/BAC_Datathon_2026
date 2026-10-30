"""B3. Impact maths for the $10M: 2024 est admissions per candidate hazard x 5% / 10% reduction = admissions avoided.
Candidates: 65+ home-fall products vs micromobility (men 15-44) vs infant falls (0-4) vs e-bikes alone.
Chart: charts/b_impact_compare.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = load("data/clean.parquet")
d = df[df.year == 2024].copy()
d["adm_w"] = d.weight * d.admitted
d["died_w"] = d.weight * d.died
FALL_PRODUCTS = ["Floors or flooring materials", "Rugs or carpets, not specified", "Runners, throw rugs or doormats",
                 "Stairs or steps", "Beds or bedframes, other or not specified", "Bathtubs or showers", "Toilets"]
EBIKE = r"E-BIKE|EBIKE|E BIKE|E-BICYCLE|ELECTRIC BIKE|ELEC BIKE|ELECTRIC BICYCLE|ELECTRIC PEDAL|PEDAL ASSIST|MOTORIZED BI"
fall_narr = d.narrative.str.contains("FELL|FALL|SLIP|TRIP", regex=True)
cands = {
    "65+ home-fall products (floors, stairs, beds, bathroom)": d["product"].isin(FALL_PRODUCTS) & (d.age_years >= 65),
    "65+ any fall (narrative), any product": fall_narr & (d.age_years >= 65),
    "Micromobility, men 15-44": (d.product_group == "Bikes & micromobility") & (d.sex == "Male") & d.age_years.between(15, 44),
    "Micromobility, all ages": d.product_group == "Bikes & micromobility",
    "E-bikes only (new code or narrative)": d["product"].eq("Electric power-assisted pedal bicycles") | d.narrative.str.contains(EBIKE, regex=True),
    "Infant falls 0-4 (narrative), any product": fall_narr & (d.age_years < 5),
}
rows = []
for k, m in cands.items():
    x = d[m]
    rows.append({"candidate": k, "n_rows": len(x), "est_visits": x.weight.sum(), "est_admissions": x.adm_w.sum(),
                 "adm_rate_%": x.adm_w.sum() / x.weight.sum() * 100, "est_deaths": x.died_w.sum(), "deaths_rows": int(x.died.sum()),
                 "avoided_at_5%": x.adm_w.sum() * 0.05, "avoided_at_10%": x.adm_w.sum() * 0.10})
t = pd.DataFrame(rows).set_index("candidate")
t["$ per admission avoided @10% ($10M)"] = 1e7 / t["avoided_at_10%"]
pd.set_option("display.float_format", lambda v: f"{v:,.1f}")
print("=== 2024, national estimates ===")
print(t.to_string())
lead, alt = t.index[0], "Micromobility, men 15-44"
print(f"\n65+ home-fall products vs micromobility men 15-44: {t.loc[lead,'est_admissions']/t.loc[alt,'est_admissions']:.0f}x the admissions, "
      f"{t.loc[lead,'adm_rate_%']/t.loc[alt,'adm_rate_%']:.1f}x the admission rate; a 5% cut in the former avoids "
      f"{t.loc[lead,'avoided_at_5%']/t.loc[alt,'avoided_at_10%']:.1f}x more admissions than a 10% cut in the latter.")
t.to_csv("analysis/23_impact_10m.csv")

# chart
show = t.loc[[lead, "Micromobility, men 15-44", "Infant falls 0-4 (narrative), any product", "E-bikes only (new code or narrative)"]]
labels = ["65+ falls: floors, stairs,\nbeds, bathroom", "Micromobility,\nmen 15-44", "Infant falls 0-4", "E-bikes only"]
fig, ax = plt.subplots(figsize=(10, 5.6))
vals = show["avoided_at_10%"] / 1000
bars = ax.bar(labels, vals, color=[ORANGE, GREY, GREY, GREY])
for b, v, n in zip(bars, vals, show.n_rows):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:,.1f}k\n(n={n:,})", ha="center", fontsize=12)
ax.set_ylim(0, vals.max() * 1.2); ax.set_ylabel("hospital admissions avoided per year (thousands)")
save_chart("b_impact_compare", f"A 10% cut in 65+ home falls avoids {vals.iloc[0]:,.0f}k admissions a year, "
                               f"{vals.iloc[0]/vals.iloc[1]:.0f}x the micromobility alternative")

# actions (evidence computed, not typed)
x = d[cands[lead]].copy()
x["fp"] = x["product"].map({"Floors or flooring materials": "Floors", "Rugs or carpets, not specified": "Floors",
                            "Runners, throw rugs or doormats": "Floors", "Stairs or steps": "Stairs",
                            "Beds or bedframes, other or not specified": "Beds", "Bathtubs or showers": "Bathroom", "Toilets": "Bathroom"})
adm_by = x.groupby("fp").adm_w.sum(); rate_by = x.groupby("fp").apply(lambda g: g.adm_w.sum() / g.weight.sum() * 100, include_groups=False)
death_by = x.groupby("fp").died_w.sum()
fbb = adm_by[["Floors", "Beds", "Bathroom"]].sum() / adm_by.sum()
acts = pd.DataFrame([
    ["Home fall-proofing kit + message to 75+ (grab bars, bed height, night lighting, rug removal)", "Regulator + retailers/pharmacies",
     f"floors+beds+bathroom = {fbb:.0%} of 65+ home-fall admissions ({adm_by[['Floors','Beds','Bathroom']].sum()/1e3:,.0f}k/yr)"],
    ["Bathroom transfer safety (toilet, tub/shower) via home-care and discharge nurses", "Hospitals / Medicare discharge planning",
     f"Bathroom admission rate {rate_by['Bathroom']:.0f}% (highest with floors {rate_by['Floors']:.0f}%)"],
    ["Stairs: handrails + lighting checks for 65+ homes; do NOT fund an e-bike ban", "Councils / housing agencies",
     f"Stairs = {death_by['Stairs']/death_by.sum():.0%} of deaths in these four; e-bikes {int(t.loc['E-bikes only (new code or narrative)','deaths_rows'])} deaths in 2024"],
], columns=["action", "owner", "evidence"])
print("\n=== 3 actions ===\n", acts.to_string(index=False))
