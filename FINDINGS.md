# Findings

Running log. Newest at the bottom. Format per finding:

### <Finding written as a slide headline>
- **Number:** ... (n = ...)
- **Chart:** charts/....png
- **So what:** ...
- **Confidence:** high / med / low, caveat: ...

---

### Data: 285,559 ER visits (1-in-5 NEISS sample) = 54.3M estimated US product-injury ER visits across 2005/2014/2023/2024
- **Number:** rows 72,074 / 73,498 / 67,653 / 72,334; est 12.6M / 13.8M / 12.7M / 15.1M (sum of weight). All-years file reconciles with the yearly files; case_id unique
- **Chart:** none
- **So what:** every share uses SUM(weight). Row counts overweight Children's hospitals (18.5% of rows, 3.2% of est)
- **Confidence:** high. Caveat: product names change between years; location "Not recorded" grows 20.6% → 37.2% (est share)

### Over-65s are 20% of injuries but are admitted at 24.7%, vs 1.8–9.2% for every other age group
- **Number:** admitted share (est) 65+ 24.7% vs 0–4 2.2%, 5–14 1.8%, 15–24 2.2%, 25–44 3.9%, 45–64 9.2%; 65+ = 20.1% of est visits (n = 46,504 rows) and 45% of deaths (79 of 184 rows)
- **Chart:** none yet
- **So what:** falls (floors, beds, stairs) among the elderly are the costliest injuries; the overall admitted share rose 4.3% → 10.7% (2005 → 2024) as mean patient age rose 30.8 → 40.6
- **Confidence:** med. Caveat: part of the admission rise may be a change in hospital practice, not just age mix; not yet broken down by age within each year

### Home injuries from building parts and furniture are growing while ball sports shrink
- **Number:** 2005 → 2024 est: Beds 421k → 943k (2.2x), Toilets 3.4x, Exercise 3.0x; Basketball 0.7x, Football 0.7x; Furniture share 12.9% → 16.6%, Team & ball sports share 13.7% → 10.7%
- **Chart:** none yet
- **So what:** prevention spend should move toward home and elderly fall safety; powered scooters and e-bikes are new categories (powered scooters 115k est in 2024)
- **Confidence:** med. Caveat: product categories changed between years (e.g. Toys rename, powered scooters split), so check the narrative before claiming a new category is real growth

### Flagging the riskiest 20% of ER visits catches 76% of hospital admissions (3.8x random)
- **Number:** gradient boosting ROC-AUC 0.894 vs baseline 0.500 (random forest also 0.894; logistic 0.878). Test n = 57,110 visits; admitted rate 8.2% (n = 285,548). Top 10% flagged: 44.5% admitted (5.4x avg), 54.4% of admissions caught
- **Chart:** charts/gains_chart.png, charts/top_drivers.png
- **So what:** diagnosis + age + body part alone (all known at triage) sort out who will need a bed. Drivers: fractures 20.3% admitted (n = 44,904) vs sprains 0.6%; oldest age quartile 21.6% vs 2.7–5.0%; upper leg (hip) 29.3% (n = 3,470) vs finger 1.1%; Bathroom products 16.5% vs team sports 2.2%
- **Confidence:** med. Caveat: hospital_type is driver #4 (Small/Children's admit ~4.5% vs ~10% elsewhere), which reflects hospital practice, not patient risk. Model is unweighted (rows, not national estimate). Leakage dropped: outcome, died, narrative. Accuracy is misleading here (baseline 91.8% by always saying "no")

---
# Round 2: headline fact-check and the $10M campaign

## A. Headline fact-check (Marcus, branch marcus/headline-check, scripts analysis/1x_*.py, charts/a_*.png)

(append findings below this line)


## B. Where the $10M goes (Germaine, branch germaine/recommendation, scripts analysis/2x_*.py, charts/b_*.png)

(append findings below this line)

### Over-65s are 26% of 2024 ER visits but 64% of admissions and 59% of deaths; admitted at 4.9x the under-65 rate in every product group
- **Number:** 2024 est: 65+ = 3.93M visits (26.1%), 1.02M admissions (63.5%), 6.8k deaths (59.3%); n = 15,302 rows. Admission rate 65+ 26.0% vs under-65 5.3% (ratio 1.6x to 10.9x across the 14 product groups). Biggest cells by admissions: Floors/stairs/building parts 65+ 419k, Furniture 65+ 319k, Bathroom 65+ 95k. Bikes & micromobility, all ages, all sexes: 88k admissions; e-bikes alone 12k
- **Chart:** charts/b_adm_rate_by_group.png (table: analysis/21_hazard_map_2024.csv)
- **So what:** whatever the product, the population that fills hospital beds is the elderly. A campaign aimed at 15-44 riders targets a 9% admission-rate group; one aimed at 65+ targets a 26% group
- **Confidence:** high. Caveat: "admitted" = Admitted to hospital only (held/transferred excluded); all shares are SUM(weight); deaths are 56 rows in 2024 so death shares are indicative

### 65+ falls on floors, stairs, beds and bathrooms: 1.9M ER visits and 622k admissions in 2024 (13% of visits, 39% of all admissions), x2.6 since 2005 while all injuries grew x1.2
- **Number:** 2024 est 1,926,712 visits (n = 7,648), 622,473 admissions (32.3% admitted), 4,820 deaths (20 rows, 41.8% of all 2024 deaths). By product: Floors 802k visits / 35.6% admitted; Beds 484k / 31.6%; Stairs 379k / 24.8%; Bathroom (tub, shower, toilet) 262k / 34.2%. Trend est visits 741k (2005) -> 1.11M (2014) -> 1.60M (2023) -> 1.93M (2024), admissions x3.2; share of all injuries 5.9% -> 12.8%. 75+ alone: 1.28M visits, 442k admissions (34.5%). 91% of these narratives say FELL/FALL/SLIP/TRIP. Location: Home = 55.4% of all rows (22.9% Not recorded) = **71.8% of known location** (n known 5,779); next is Other public property 27.7% (nursing homes). Body: Head 27.4%, Lower trunk 15.9%; Dx: Fracture 22.2%, Internal organ injury (head) 19.6%, Other/not stated 27.3%. Hip/upper-leg injuries admitted 51%, lower trunk 47%. 62% female, median age 79
- **Chart:** charts/b_65_homefall_trend.png
- **So what:** this is the single largest and fastest-growing severe-injury hazard in the data, it happens at home, and it is the ageing population, not a new product. The message is fall-proofing the home (floor/rugs, bed transfers, bathroom grab bars, stairs lighting/handrails), aimed at 75+ and their carers
- **Confidence:** high on size and direction. Caveats: growth is partly population ageing (no census denominator in the data); 2024 weights are higher than 2023 (Marcus, section A) so 2023->2024 growth is overstated; "Other/not stated" diagnosis is 27% so fracture share is a floor; location unknown for 23%

### $10M on 65+ home falls: a 10% cut avoids 62k admissions a year ($161 each); the same cut in micromobility for men 15-44 avoids 3k ($3,250 each); e-bikes alone 1.2k
- **Number:** 2024 est admissions and 10% reduction: 65+ home-fall products 622k -> 62.2k avoided (n = 7,648); 65+ any fall (narrative, any product) 883k -> 88.3k; Micromobility men 15-44 30.8k -> 3.1k (n = 1,476; 9.3% admitted, 1 death row); Micromobility all ages 88k -> 8.8k; E-bikes only 12.4k -> 1.2k (n = 411, 0 deaths); Infant falls 0-4 12.2k -> 1.2k (n = 5,969; 1.5% admitted). 65+ home falls have 20x the admissions and 3.5x the admission rate of the micromobility group; a 5% cut in 65+ falls beats a 10% cut in micromobility by 10x
- **Chart:** charts/b_impact_compare.png (table: analysis/23_impact_10m.csv)
- **So what:** 3 actions -> owner -> impact: (1) Home fall-proofing kit + campaign for 75+ and carers (grab bars, bed height, night lights, rug removal) -> regulator with retailers/pharmacies -> floors+beds+bathroom = 85% of the 622k (528k/yr); 10% = 53k admissions avoided. (2) Bathroom transfer safety via discharge planning and home care -> hospitals/Medicare -> bathroom admitted 34%, toilets x3.4 since 2005. (3) Stairs handrail + lighting checks in 65+ housing, and do NOT spend on an e-bike ban -> councils/housing -> stairs = 38% of deaths in these four products; e-bikes 0 deaths in 2024. Honesty check: micromobility does not beat 65+ falls on volume, severity or deaths under any definition tried
- **Confidence:** med-high. Caveats: 5%/10% are assumed campaign effects, not measured; no cost per admission in the data (a hip-fracture admission is far costlier than average, so $ saved is understated); no exposure data (e-bike injuries per rider may still be rising fast, which matters for the council's question but not for where the $10M buys most)

## C. Limits and what would change our answer (both)

(append below this line)

