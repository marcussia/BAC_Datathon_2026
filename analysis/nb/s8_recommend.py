"""Section 8: recommendation, where the $10M goes. Owner: Germaine (Marcus wrote the baseline)."""
from nb import md, code

TABLE = '''# Three candidate campaigns on the same numbers. Trend = 2005 -> 2024 change in national estimate.
d24 = df[df.year == 2024]
cands = {"(1) 75+ falls at home: floors/stairs/furniture/bathroom": lambda d: d.over75 & d.fall_product,
         "(2) E-bike / micromobility safety (Bikes & micromobility group)": lambda d: d.product_group == "Bikes & micromobility",
         "(3) Kids' team sports (5-14, Team & ball sports)": lambda d: (d.age_group == "5-14") & (d.product_group == "Team & ball sports")}
rows = []
for k, f in cands.items():
    c24, c05 = d24[f(d24)], df[(df.year == 2005) & f(df[df.year == 2005]).reindex(df[df.year == 2005].index)]
    rows.append({"candidate": k, "rows_2024": len(c24), "est_injuries_2024": c24.weight.sum(), "est_admissions_2024": (c24.admitted * c24.weight).sum(),
                 "admit_%": wrate(c24, "admitted") * 100, "deaths_2024_rows": int(c24.died.sum()), "trend_2005_2024_%": (c24.weight.sum() / c05.weight.sum() - 1) * 100})
ct = pd.DataFrame(rows).set_index("candidate")
ct["addressability"] = ["high: known hazards, known room, reachable via GPs/pharmacies/carers", "medium: behaviour (helmet, alcohol) + road design; exposure unknown", "low: sport injuries are mostly minor and accepted risk"]
print(ct.round(1).to_string())
c1 = ct.iloc[0]
SLIDE(4, "candidate 1 est injuries / admissions 2024", f"{c1.est_injuries_2024:,.0f} / {c1.est_admissions_2024:,.0f} (n = {int(c1.rows_2024):,})")
SLIDE(4, "candidate 1 vs 2 admissions (x)", f"{c1.est_admissions_2024 / ct.iloc[1].est_admissions_2024:.0f}")
SLIDE(4, "candidate 1 trend 2005->2024 (%)", f"{c1['trend_2005_2024_%']:+.0f}")'''

IMPACT = '''# What a 5% / 10% reduction in candidate-1 admissions would be worth, in admissions avoided (no cost data in NEISS).
for cut in (0.05, 0.10):
    print(f"{cut:.0%} fewer 75+ home-fall admissions = {c1.est_admissions_2024 * cut:,.0f} admissions avoided per year")
SLIDE(4, "admissions avoided per year at 5% / 10% reduction", f"{c1.est_admissions_2024 * 0.05:,.0f} / {c1.est_admissions_2024 * 0.10:,.0f}")'''

REC = """### Recommendation: put the $10M on over-75s falling at home
| | Action | Owner | Expected impact |
|---|---|---|---|
| 1 | **Home-hazard removal kit + check**: grab bars in bathrooms, bed height and night lighting, loose rugs and stair rails | Regulator with local councils and home-care providers | targets the 4 product families behind most 75+ admissions |
| 2 | **Reach via GPs and pharmacies, not TV**: medication review, balance/strength check, carer leaflet at the point of care | Regulator + health service | the population is reachable (1 in 6 ER patients, 43% of admissions) |
| 3 | **Measure it**: NEISS 2026 vs 2024 for 75+ home-fall admissions, with Census 75+ population as the denominator | Regulator analytics | a 5% reduction is tens of thousands of admissions a year (number printed above) |

**Rough split:** $5M hazard-removal grants and kits (via councils, means-tested), $3M clinical reach (GP/pharmacy materials, carer guidance), $1.5M measurement and evaluation, $0.5M a proportionate e-bike response.

**On e-bikes:** don't ban. The growth is real but small (about 0.7% of visits, 0 deaths), riders are adult men, and micromobility has the highest alcohol share of any product group. Helmet and sober-riding enforcement is the proportionate response; a ban answers a number that was an artefact."""

TAKE = """> **Takeaway (recommendation).** On every column (volume, admissions, deaths, trend, admission rate, addressability) candidate 1 wins: 7x the admissions of the whole micromobility group, and 23-41x those of e-bikes alone. **So what:** $10M on 75+ home-fall prevention via homes, GPs and pharmacies; a proportionate helmet/alcohol response on e-bikes; no ban. **Confidence: high** on the ranking, medium on the impact size (no cost or campaign-effect data)."""


def cells():
    return [
        md("## 8. Recommendation: where the $10M goes  \n*Rubric: insights + communication.* Three candidates on the same numbers, the pick, the message, the split, and the e-bike line."),
        md("Candidate comparison table. Why it matters: the pick should follow from the same four numbers for each option."),
        code(TABLE),
        md("Impact sizing in admissions avoided. Why it matters: it turns the pick into a number the regulator can be held to."),
        code(IMPACT),
        md(REC),
        md(TAKE),
    ]
