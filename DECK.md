# Deck: 5 slides (MAX). Numbers come from `analysis/slide_numbers.csv` (SLIDE n: labels in the notebook). Run /check before presenting.

## Slide 1: Two of the three headline claims don't survive the data
Scorecard, one row per claim: claim | verdict | the number.
| Claim | Verdict | Number |
|---|---|---|
| "Injuries surged 18% in 2024" | Partly holds | +18.3% by weight, +6.9% by sampled visits; +11.6% at 2023 weights |
| "E-bike injuries nearly quadrupled" | Does not hold | 1.2-1.6x like-for-like; the 4x is a product-code rename |
| "E-bikes are the deadly new threat" | Does not hold | 0 of 56 deaths in 2024; 0.7% of visits |
- Subtitle: NEISS 2005/2014/2023/2024, 285,559 sampled visits = 54.3M national estimate; every number weighted.
- Chart: none (table). Owner: Marcus.

## Slide 2: Why the 18% and the 4x are artefacts: survey weights and a renamed product code
- Left: `c1_surge_rows_vs_weight.png` (rows +7%, weight +18%, mean weight 188 → 208).
- Right: `c2_ebike_three_definitions.png` (2024 e-bike code 56k vs 0; moped code 81k → 0; like-for-like 82k → 101k).
- One line: 2023 was a low base (2024 vs 2014 = +8.9%); a naive "E BIKE" text search matches "THE BIKE".
- Owner: Marcus.

## Slide 3: The real story: injuries to under-65s are flat (+1%), to over-65s up 151%; over-75s are 1 in 6 patients and 43% of admissions
- Chart: `c4_admissions_75plus_vs_ebike.png` (23x, 41x on the code-only definition; 347k admissions = 21% of all 2024 admissions) with `c4_under65_vs_over65.png` as inset if space.
- Bullets: 75+ admitted 15x as often as children (30% vs 2%); floors, beds, stairs, bathrooms; fastest risers since 2005 are toilets 3.4x, beds 2.2x, bathtubs 1.8x; 65+ = 43% of deaths (79 of 184).
- Model line: 75+ has 4.3x the odds of admission of a 25-44 year old with the same injury and product (AUC 0.86).
- Owner: Marcus numbers, Germaine framing.

## Slide 4: Recommendation: $10M on over-75s falling at home, through homes, GPs and pharmacies. Don't ban e-bikes
- Candidate table (3 rows: 75+ home falls / micromobility / kids' sports) on est injuries, admissions, deaths, trend, admit rate, addressability.
- 3 actions → owner → impact: hazard-removal kits; GP/pharmacy reach; measure with Census denominator. Split: $5M / $3M / $1.5M / $0.5M e-bike helmet+alcohol.
- Impact: 5% reduction = 29,411 admissions avoided per year; 10% = 58,823 (SLIDE 4). Candidate 1: 1.80M injuries, 588k admissions, +139% since 2005.
- Chart: `m_projection_65plus_home_falls.png` (indicative 2030).
- Owner: Germaine.

## Slide 5: What this data can't tell us, and what would change our mind
- No exposure denominators (e-bikes on the road; 75+ population), weight change 2023→2024, first-product-only coding, narrative cap 142 → 400 chars, "Not recorded" location 37%, deaths small-n (56 rows) and ER-only.
- Would change the answer: Census population by age, e-bike sales/registrations, full-weight NEISS, hospital discharge/cost data.
- Verdict line: the ranking survives all of these; the impact size doesn't.
- Owner: Germaine drafts, Marcus adds.

## Judge Q&A (5)
1. Is the 18% real? Weighted yes, sampled no: +6.9% rows, +11.6% at fixed weights; 2023 was a low base.
2. Why not e-bikes if they're growing fastest? 0.7% of visits, 0 deaths; 75+ home falls cause 23x the admissions.
3. Should the council ban e-bikes? No: the 4x is a recoding, no exposure data, riders are adult men with the highest alcohol share; enforce helmets and sober riding.
4. Did you use the weights? Every national number is SUM(weight); Children's hospitals are 18.5% of rows but 3.2% of visits.
5. Isn't the ageing trend just the hospital sample changing? The 65+ share doubled within every hospital type, and age dominates admission odds after controlling for product and injury.
