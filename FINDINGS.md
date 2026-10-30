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

### [Round-1 prep, SUPERSEDED for the pitch by the weighted severity model in section B, analysis/24] Flagging the riskiest 20% of ER visits catches 76% of hospital admissions (3.8x random)
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

**Definitions used in B (say which one is on the slide):**
- "65+ falls, any product" (Marcus, section A): narrative says FELL/FALL/SLIP/TRIP, age 65+. 2024: 3.02M visits, 883k admissions. Use for *how big the hazard is*.
- "65+ home-fall products" (B): product is floors/rugs, stairs, beds, bathtubs/showers or toilets, age 65+. 2024: 1.93M visits, 622k admissions. Use for *the campaign target*.
- "admitted" = outcome "Admitted to hospital" only. "e-bike" = new 2024 product code OR e-bike words in the narrative (12.4k admissions in 2024); Marcus's wider union adds "Power-assisted cycles NEC" (18.9k). State which when quoting a multiple.
- Every national number is SUM(weight); n = sample rows.

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

### Model: age, not the product, predicts who gets admitted. 75+ have 6.8x the odds of a 25-44 year old; an e-bike adds 1.1x once age is known (AUC 0.82 on held-out 2024)
- **Number:** Gradient boosting, sample_weight = NEISS weight, trained 2005-2023 (n = 213,225), tested on 2024 (n = 72,334), features known before diagnosis (age, sex, product group, location, alcohol, fall-in-narrative, vehicle flags, hospital type; no diagnosis/body part/outcome). 2024 ROC-AUC 0.817, PR-AUC 0.329 vs 0.107 random, calibrated within 1 pt in every risk decile (e.g. top decile predicted 37.5% vs observed 38.3%). Top 20% highest-risk visits hold 60% of admissions (3.0x). Baselines (same split): age alone AUC 0.777, age + fall flag 0.784, everything except age 0.743, everything except hospital_type 0.805, full 0.817, so age carries more signal than all other features combined. Permutation importance: age 0.255 AUC drop; hospital type 0.020; product group 0.016; fall 0.014; e-bike, scooter, bicycle flags 0.000. Logistic regression (2023-24, n = 139,987, AUC 0.815) odds of admission vs age 25-44: 0-4 0.36x, 45-64 2.2x, 65-74 4.3x, **75+ 6.8x**; alcohol 1.75x; fall 1.6x; male 1.35x; **e-bike 1.11x**, powered scooter 1.00x, pedal bicycle 0.90x. Out-of-sample 2024 check: model expects 863k admissions from 65+ falls vs 882k observed (54% of all expected admissions), 11.8k from e-bikes vs 12.4k observed (1%)
- **Chart:** charts/b_severity_odds.png (tables: analysis/24_odds_ratios.csv, 24_calibration_2024.csv, 24_importance.csv, 24_expected_adm_by_hazard.csv)
- **So what:** the model backs the recommendation two ways. (1) The thing that makes an ER visit turn into a hospital bed is being old and falling, not the product in the headline: swap an e-bike for a pedal bike or no vehicle and admission odds barely move. (2) Trained without seeing 2024, it still puts 54% of 2024's expected admissions on 65+ falls and 1% on e-bikes, so the $10M target is not a 2024 artefact
- **Confidence:** high on the ranking and direction; med on exact odds (hospital_type is the #2 driver, which is admission practice, not patient risk; alcohol is self-reported; vehicle flags rest on narrative regex)

### Slide-sentence check: under-65 injuries +0.8% since 2005, 65+ +151%; 75+ are 1 in 6 ER patients (weighted) and 43% of ALL admissions, 56x the admissions of every e-bike injury
- **Number:** 2005 -> 2024 est visits: under-65 11.04M -> 11.13M (+0.8%); 65+ 1.57M -> 3.93M (+151.1%); 75+ 1.05M -> 2.35M (+124%). 2024: 75+ = 15.6% of visits (1 in 6.4 weighted; by rows it is 1 in 7.9, so quote the weighted figure), 43.3% of all admissions (698k of 1.61M), 63.5% for 65+. 75+ = 54.6% of admissions from the home-fall products (floors, stairs, beds, bathroom), NOT 43% (that is their share of all admissions). 75+ all admissions / e-bike admissions = 56x with the B e-bike definition (12.4k, narrative or new code) or 37x with Marcus's wider union (18.9k incl. "Power-assisted cycles NEC"); 75+ home-fall admissions / e-bike = 36x or 23x
- **Chart:** none (script analysis/25_slide_claims_check.py)
- **So what:** safe wording: "Injuries to under-65s have been flat for 20 years (+1%); injuries to over-65s are up 151%. People 75+ are 1 in 6 ER patients but 43% of all hospital admissions, 56x the admissions caused by every e-bike injury combined." Do not say "43% of admissions from falls at home" (that figure is 55%), and do not say 47x (no definition gives it)
- **Confidence:** high; the e-bike multiple depends on the e-bike definition, so state which one

### 2026 outlook: 65+ home falls on trend to 641-672k admissions in the campaign year; e-bikes would need to quadruple EVERY year to reach 199k
- **Number:** 65+ home-fall-product admissions (est) 192k (2005) -> 320k (2014) -> 541k (2023) -> 622k (2024); log-linear trend 5.9%/yr fitted on 2005-2023 (avoids the 2024 re-weighting) gives 641k in 2026, 6.2%/yr on all four years gives 672k; visits 1.83-1.97M. E-bike admissions 2024 = 12.4k (n = 411): at the like-for-like 1.2x/yr they reach 18k in 2026 (65+ falls 36x larger); at 1.5x 28k (23x); at 2x 50k (13x); at the headline's 4x every year 199k (still 3x smaller)
- **Chart:** charts/b_projection_2026.png (table analysis/26_projection_2026.csv)
- **So what:** the $10M is spent in 2026, and under any growth story the elderly-fall problem is still an order of magnitude larger that year. The e-bike ban would not change the 2026 hospital bed count
- **Confidence:** med. Caveat: four data points, trend is indicative not a forecast; the 65+ range brackets the 2024 weighting uncertainty; e-bike scenarios are illustrative multipliers, not predictions

### Which message: bathroom and bed transfers (230k admissions a year) plus "check dizziness": 15% of 65+ home falls start with dizziness or weakness and 51% of those are admitted
- **Number:** 2023-24 narratives for 65+ home-fall products (n = 14,747; group admission rate 33.0%). Theme -> est admissions/yr, admitted %: dizzy/syncope/weakness 137k, 51% (n = 2,249); toilet/bathroom 122k, 36% (n = 2,832); getting out of/into bed 107k, 34% (n = 2,671); stairs 76k, 27%; found on floor / unwitnessed / could not get up 75k, 49% (n = 1,259); nursing home/assisted living 64k, 29%; rug/carpet/wet floor 36k, 27%; walker/cane 33k; at night 29k, 34%; dementia 21k, 42%; blood thinner 17k; footwear 3k
- **Chart:** charts/b_message_themes.png (table analysis/27_message_keywords.csv)
- **So what:** the campaign message is concrete: (1) make the two transfers safe, bed and toilet/shower (grab bars, raised seat, bed height, night light on the route); (2) "dizzy when you stand = see your doctor" (medication/blood-pressure review), because those falls are the ones that end in admission; (3) a fall alarm/check-in for people living alone, since unwitnessed falls admit at 49%. Rugs and footwear, the usual leaflet content, are a small share
- **Confidence:** med. Caveat: keyword themes overlap and depend on nurse wording; 2005/2014 narratives are too short to compare; nursing-home rows show the target also includes care facilities, not just private homes

### Combined model (Marcus's features + Germaine's, temporal split): AUC 0.88 on held-out 2024; 75+ still 5.0x the admission odds of a 25-44 year old, e-bike 0.97x, even controlling for body part and diagnosis
- **Number:** same weighted gradient boosting, trained 2005-2023 (n = 213,225), tested on 2024 (n = 72,334). Pre-diagnosis feature set (analysis/24): ROC-AUC 0.816, PR-AUC 0.329. Marcus's feature set (age, sex, product group, location, alcohol, body part, diagnosis): 0.871 / 0.475. Union of both: **0.876 / 0.505** (random = 0.107). Logistic odds from the union (2023-24, n = 139,987, AUC 0.867) vs age 25-44: 0-4 0.28x, 45-64 1.9x, 65-74 3.4x, **75+ 4.95x**; alcohol 1.47x; fall 1.23x; male 1.41x; e-bike **0.97x**, powered scooter 0.88x, pedal bicycle 0.81x. Out of sample the combined model assigns 55% of 2024 expected admissions to 65+ falls (865k expected vs 882k observed) and 1% to e-bikes (11.9k vs 12.4k)
- **Chart:** none (tables analysis/28_combined_auc.csv, 28_combined_odds.csv, 28_combined_expected.csv; script analysis/28_combined_model.py)
- **So what:** adding what the doctor finds (body part, diagnosis) lifts accuracy from 0.82 to 0.88 but does not move the conclusion: age is the driver and an e-bike adds nothing to admission odds once the injury itself is known. The three models (Colab 2024 logistic 4.3x, analysis/24 6.8x, combined 5.0x) bracket the 75+ effect at 4-7x; quote "4 to 7 times" if challenged
- **Confidence:** high on direction; med on the exact multiple (ranges 4.3-6.8x across specifications because diagnosis absorbs part of the age effect)

## C. Limits and what would change our answer (both)

(append below this line)

### What this data cannot tell us (and the extra data that would change the answer)
- **Sample, not a census, and the sample changed in 2024.** ~80-100 hospitals, then a 1-in-5 cut. 2024 has 9 distinct weight values vs 13 in 2023; the Very large stratum weight rose 78-105 -> 138 and Small 360-384 -> 522-540 while their row counts fell (-10%, -11%). Rows rose 6.9% but est rose 18.3%; re-weighting 2024 rows at 2023 mean weights per hospital type gives +11.6%. Any 2023->2024 growth figure (including ours for 65+ falls) carries this uncertainty. *Extra data:* CPSC's 2024 sample/weight documentation and the 2015-2022 years, to see a trend instead of two points.
- **No exposure or population denominators.** 65+ falls grew x2.6, but the 65+ population also grew; e-bike injuries grew while e-bike ridership grew faster. Injuries per 1,000 residents or per million trips may tell a different story. *Extra data:* Census population by age; e-bike/e-scooter sales and trip counts.
- **Coding changes masquerade as trends.** The e-bike product code exists only in 2024 (0 -> 243 rows, 56k est); "Mopeds or power-assisted cycles" (395 rows, 81k) disappears the same year. Under a consistent narrative definition e-bikes rose 1.3x by rows and 1.5x by est, not 4x. Diagnosis "Other/not stated" rose 7% -> 22% and location "Not recorded" 22% -> 37%, so fracture shares and home shares are floors and the denominator choice must be stated. *Extra data:* CPSC coding manual change log; ICD-coded discharge data.
- **ER visits only, first product only, one line of narrative.** Deaths here are ER deaths (184 rows in 4 years; 0 e-bike deaths), not all deaths; later deaths after admission are invisible. Only the first product is coded, so "bed" may hide a floor impact. *Extra data:* CDC WISQARS/NVSS mortality by product and age; HCUP admission costs to turn admissions into dollars (a hip fracture admission costs far more than the average, so our $ per admission avoided is conservative).
- **Severity is confounded by age, not product.** In a logistic model on 2023-24 (weighted, n = 139,987), 75+ has 8.1x the odds of a severe outcome vs 18-44, alcohol 1.8x, male 1.3x; e-bike vs no vehicle 1.05x and pedal bike 0.86x. A gradient-boosting model trained on 2005-2023 predicts 2024 severity with ROC-AUC 0.80, and age alone carries almost all of it (AUC drop 0.23 when shuffled vs 0.00 for the e-bike flag). The campaign effects (5%/10%) are assumptions, not measured. *Extra data:* evaluations of past fall-prevention campaigns (effect sizes) and helmet/alcohol enforcement for micromobility.
- **Small-n warnings.** E-bike rows 2024 = 243 in the category (95% Poisson CI 212-274 before the x5 scale-up); deaths per product per year are single digits. We never rank on deaths alone.
- **What would flip the recommendation:** exposure-adjusted e-bike injury rates still rising >2x a year with severity climbing; or evidence that fall campaigns have near-zero effect while helmet/speed rules have large effects. Neither is in this data.

