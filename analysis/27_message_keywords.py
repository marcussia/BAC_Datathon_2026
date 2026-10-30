"""B7. Which message? What the narratives say 65+ home-fall patients were doing (2023-24, 400-char narratives).
Keyword rows + est share + admission rate per theme. Chart: charts/b_message_themes.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = load("data/clean.parquet")
df["adm_w"] = df.weight * df.admitted
FALL = ["Floors or flooring materials", "Rugs or carpets, not specified", "Runners, throw rugs or doormats", "Stairs or steps",
        "Beds or bedframes, other or not specified", "Bathtubs or showers", "Toilets"]
o = df[df["product"].isin(FALL) & (df.age_years >= 65) & df.year.isin([2023, 2024])].copy()
n = o.narrative.fillna("")
themes = {
    "getting out of / into bed": r"OUT OF BED|OUT OF THE BED|INTO BED|GETTING UP FROM BED|OFF THE BED|OFF BED|ROLLED OUT OF BED|FELL FROM BED|FELL OFF BED",
    "toilet / bathroom": r"TOILET|BATHROOM|COMMODE|SHOWER|BATHTUB|TUB",
    "at night / dark": r"NIGHT|DARK|2AM|3AM|4AM|MIDNIGHT|NOCTURIA|TO URINATE",
    "rug / carpet / wet floor": r"RUG|CARPET|WET FLOOR|SLIPPERY|SLIPPED ON",
    "stairs": r"STAIR|STEPS",
    "walker / cane / wheelchair": r"WALKER|CANE|WHEELCHAIR|ROLLATOR",
    "dizzy / syncope / weakness": r"DIZZ|SYNCOP|PASSED OUT|LIGHTHEADED|WEAK|LOST BALANCE|UNSTEADY|VERTIGO",
    "dementia / confusion": r"DEMENTIA|ALZHEIMER|CONFUS|MEMORY",
    "blood thinner": r"BLOOD THINNER|ELIQUIS|XARELTO|WARFARIN|COUMADIN|ANTICOAG|THINNERS|PLAVIX",
    "nursing home / assisted living": r"NURSING HOME|ASSISTED LIVING|FACILITY|NURSING FACILITY|SNF|REHAB",
    "found on floor / alone": r"FOUND ON|FOUND DOWN|LYING ON THE FLOOR|UNWITNESSED|LIVES ALONE|UNABLE TO GET UP|COULD NOT GET UP|COULDN'T GET UP",
    "footwear / socks": r"SLIPPER|SOCKS|BAREFOOT|SHOES",
}
rows = []
for k, pat in themes.items():
    m = n.str.contains(pat, regex=True)
    x = o[m]
    rows.append({"theme": k, "rows": int(m.sum()), "share_rows_%": m.mean() * 100, "share_est_%": x.weight.sum() / o.weight.sum() * 100,
                 "adm_rate_%": x.adm_w.sum() / x.weight.sum() * 100 if len(x) else np.nan, "est_adm_per_yr": x.adm_w.sum() / 2})
t = pd.DataFrame(rows).sort_values("est_adm_per_yr", ascending=False)
base = o.adm_w.sum() / o.weight.sum() * 100
print(f"65+ home-fall product visits 2023-24: n = {len(o):,}, base admission rate {base:.1f}%")
print(t.round(1).to_string(index=False)); t.to_csv("analysis/27_message_keywords.csv", index=False)
print("\nsamples, 'found on floor / alone':"); print(o[n.str.contains(themes["found on floor / alone"], regex=True)].narrative.sample(5, random_state=1).to_string(index=False))
print("\nsamples, 'getting out of / into bed':"); print(o[n.str.contains(themes["getting out of / into bed"], regex=True)].narrative.sample(5, random_state=1).to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 6))
h = t.iloc[::-1]
ax.barh(h.theme, h.est_adm_per_yr / 1e3, color=[ORANGE if v > base else GREY for v in h["adm_rate_%"]])
for i, (v, r, nn) in enumerate(zip(h.est_adm_per_yr / 1e3, h["adm_rate_%"], h.rows)):
    ax.text(v + 1, i, f"{v:,.0f}k/yr, {r:.0f}% admitted (n={nn:,})", va="center", fontsize=11)
ax.set_xlim(0, h.est_adm_per_yr.max() / 1e3 * 1.55); ax.set_xlabel("est hospital admissions per year, 65+ home-fall products, 2023-24 (orange = above the group's %.0f%% admission rate)" % base)
top = t.iloc[0]; bath = t.set_index("theme").loc["toilet / bathroom"]; bed = t.set_index("theme").loc["getting out of / into bed"]
save_chart("b_message_themes", f"Message = bathroom + bed transfers ({(bath.est_adm_per_yr+bed.est_adm_per_yr)/1e3:,.0f}k admissions/yr) and 'check dizziness': "
                               f"{top['share_rows_%']:.0f}% of falls start with dizziness/weakness and {top['adm_rate_%']:.0f}% of those are admitted")
