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

### The "18% surge" is +18.3% by weight but only +6.9% by sampled ER visits; at 2023 weights it would be +11.6%
- **Number:** 2023 → 2024: rows 67,653 → 72,334 (+6.9%), est 12.74M → 15.07M (+18.3%), mean weight 188.3 → 208.3 (+10.6%). Reweighting 2024 rows at each hospital type's 2023 mean weight gives 14.22M (+11.6%). Within hospital types, rows and weights moved in opposite directions (Medium rows +39.5% / mean weight −32.4%; Very large rows −10.4% / weight +63.2%), which is a sample re-balancing signature. 2024 vs 2014: est +8.9% over 10 years, rows −1.6%. 2023 was itself a dip (−8.0% vs 2014)
- **Chart:** charts/a_surge_rows_vs_weight.png
- **So what:** the headline number is arithmetically right but ~7–12 pts of it is weighting change and rebound from a low 2023, not more injuries. Defensible underlying growth: +7% to +12%
- **Confidence:** med. Caveat: we can't separate a CPSC weighting update from real change without their methodology notes; the +6.9% row growth is itself affected by hospital turnover

### E-bike ER visits grew 1.2x in 2024, not 4x: the product category was renamed, and e-bikes are 0.7% of all visits
- **Number:** 2023 code "Mopeds or power-assisted cycles" (395 rows, 81k est) disappears in 2024 and is replaced by "Electric power-assisted pedal bicycles" (243 rows, 56k) + "Power-assisted cycles NEC" (203 rows, 44k) = 100k. Family growth 1.23x. Narrative-only definition (E-BIKE / ELECTRIC BIKE / MOTORIZED BICYCLE etc., false positives removed): 181 → 247 rows, 36k → 55k est, 1.56x. Union of both: 82k → 101k, 1.23x, = 0.7% of 2024 visits (455 rows). 175 of the 181 narrative e-bike rows in 2023 were coded as "Mopeds or power-assisted cycles", 230 of 247 in 2024 as the new e-bike code
- **Chart:** charts/a_ebike_like_for_like.png
- **So what:** "quadrupled" compares a new 2024 code (56k) with a 2023 code that didn't exist. Like-for-like growth is 1.2–1.6x from a base under 1% of visits. Growth is real but small
- **Confidence:** high on the recoding; med on the exact multiple (the 2023 moped code mixes petrol mopeds with e-bikes, and narratives undercount)

### E-bikes caused 0 of 184 deaths; 65+ falls caused 23 of 56 deaths in 2024 and 58x more hospital admissions
- **Number:** 2024 (weighted): e-bikes 101k visits, 15.1% admitted, 15k admissions, 0 deaths (n = 455 rows; 2 moped deaths across all 4 years, both struck by cars). 65+ falls (narrative FELL/FALL/SLIP/TRIP): 3.02M visits = 20.0% of all 2024 visits, 29.3% admitted, 883k admissions, 23 of 56 deaths (n = 11,893 rows). All 65+: 26.1% of visits, 26.0% admitted, 1.02M admissions, 30 of 56 deaths. 2024 deaths by product: floors 8, stairs 8, beds 7, bathtubs 6, fires 5, bicycles 3, e-bikes 0
- **Chart:** charts/a_admissions_ebike_vs_falls.png
- **So what:** e-bike visits are somewhat more severe than average (15.1% vs 10.7% admitted) but the volume is tiny. "Deadly new threat" is not supported; the deadly, growing hazard is older adults falling
- **Confidence:** high on direction; deaths are small n (56 in 2024, sample rows not estimates)

### 65+ falls went from 9% to 20% of all ER product injuries (2005 → 2024), and the rise shows inside every hospital type
- **Number:** 65+ falls est 1.13M (2005) → 1.59M (2014) → 2.48M (2023) → 3.02M (2024); share 9.0% → 20.0%; admissions 250k → 883k. 65+ share of all visits within each hospital type roughly doubled 2005 → 2024 (Large 11.3 → 24.8%, Medium 12.9 → 28.4%, Small 14.3 → 28.0%, Very large 12.1 → 26.7%), so it isn't a change in which hospitals are sampled
- **Chart:** (Germaine's b_ trend chart covers this)
- **So what:** the campaign target is 65+ falls at home: 1.59M visits with location = Home (10.5% of all 2024 visits, 32.5% admitted, 516k admissions); the true home figure is higher because 37% of locations are "Not recorded"
- **Confidence:** med. Caveat: 65+ share doubling outpaces US demographics (65+ population share ~12% → ~18%), so some of it may be weighting or ER-use behaviour rather than more falls


## B. Where the $10M goes (Germaine, branch germaine/recommendation, scripts analysis/2x_*.py, charts/b_*.png)

### Candidate 1 (75+ falls at home) beats micromobility 7x on admissions and kids' sports on every column
- **Number:** 2024 est injuries / admissions / admit % / deaths rows / 2005→2024 trend: (1) 75+ & floors/stairs/furniture/bathroom 1.80M / 588k / 32.7% / 15 / +139% (n = 7,085); (2) Bikes & micromobility group 866k / 88k / 10.2% / 4; (3) 5-14 team sports: see notebook s8 table. 5% / 10% reduction in (1) = 29,411 / 58,823 admissions avoided per year
- **Chart:** none (table in notebook s8)
- **So what:** $10M split proposed $5M hazard-removal kits, $3M GP/pharmacy reach, $1.5M measurement, $0.5M e-bike helmet/alcohol; no ban
- **Confidence:** high on ranking; low on impact size (no cost or campaign-effect data). Germaine to refine


## C. Limits and what would change our answer (both)

(append below this line)

