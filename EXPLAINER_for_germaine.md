# What is going on (paste this into another Claude chat if you want it explained further)

## The event
I am Germaine, in Team Nai Loong (with Marcus) at the NBS Business Analytics Club Datathon 2026, Round 2, on Fri 30 Oct 2026. Stop-work is 19:55, submission by 20:00 by email to abc-bac-training@e.ntu.edu.sg. Deliverables: a slide deck of max 5 slides with recommendations, plus the code. Then a 5-minute pitch and 2-3 minutes of Q&A. Judging: Factuality 25, Insights 25, Modelling 20, Limitations 15, Communication 15.

## The data
NEISS, the US Consumer Product Safety Commission's emergency-room injury surveillance system. Each row is one ER visit for an injury involving a consumer product (stairs, beds, bikes, footballs, knives...). It is a sample of about 80-100 hospitals, and the datathon version is a further random 1-in-5 cut. Four years: 2005, 2014, 2023, 2024; 285,559 rows; 15 columns (age, sex, body part, diagnosis, outcome, location, product, product group, alcohol, hospital type, weight, narrative). The key rule: each row has a `weight` saying how many US visits it represents, so national numbers are SUM(weight), never row counts. Other traps: ages 201-223 mean babies in months, alcohol is blank before 2019, product names get renamed between years, and "Not recorded" location grew from 22% to 37%.

## The problem statement
A newspaper headline said: "Product injuries surged 18% in 2024, and e-bikes are the deadly new threat. E-bike injuries nearly quadrupled in a year." A regulator has $10M for one national prevention campaign in 2026, and a city council wants to ban e-bikes. We are the regulator's analysts. Three asks: (1) fact-check the headline, (2) say where the $10M should go (hazard, population, message), (3) say what the data cannot tell us and what extra data would change the answer.

## How the team split it
- Marcus: workstream A, the headline fact-check (branch marcus/headline-check, scripts analysis/1x_*, charts/a_*).
- Me: workstream B, where the $10M goes (branch germaine/recommendation, scripts analysis/2x_*, charts/b_*). I also wrote section C (limits).
- Everything is in the GitHub repo marcussia/bac-datathon-r2. Findings go in FINDINGS.md, which the slide team builds the deck from. My work is in Pull Request #1.

## What Marcus found (section A)
- The "18% surge" is +18.3% by weighted estimate but only +6.9% by actual sampled visits. The 2024 weights were higher than 2023's (the hospital sample was rebalanced). Reweighting 2024 at 2023 weights gives +11.6%. So the underlying growth is 7-12%, and 2023 was itself a low year.
- E-bikes did not quadruple. In 2024 the agency created a new product code for e-bikes (0 rows in 2023, 243 in 2024) and retired the old "mopeds or power-assisted cycles" code. Like for like, e-bike visits grew 1.2x to 1.6x, from a base under 1% of all visits.
- E-bikes caused 0 of 184 deaths across the four years. 65+ falls caused 23 of the 56 deaths in 2024.

## What I found (section B)
1. Over-65s are 26% of 2024 ER visits but 64% of hospital admissions and 59% of deaths. They are admitted at 26.0% vs 5.3% for under-65s, 4.9x, and that holds in every one of the 14 product groups.
2. The lead hazard: 65+ falling on floors, stairs, beds and in bathrooms. 2024: 1.93M visits (n = 7,648 rows), 622k admissions (32% admitted), 42% of all deaths. It grew 2.6x since 2005 while all injuries grew 1.2x. 72% happen at home (using known locations), the rest mostly in nursing homes. Head and hip injuries dominate; hip injuries are admitted 51% of the time. Median age 79, 62% women.
3. Impact maths: a 10% cut in those falls avoids 62k admissions a year ($161 per admission avoided from the $10M). The same 10% cut in micromobility injuries among men 15-44 avoids 3.1k ($3,250 each). E-bikes alone: 1.2k. Infant falls: 1.2k. Micromobility loses on volume, severity and deaths under every definition.
4. Model: a weighted gradient-boosting model trained on 2005-2023 and tested on 2024 predicts who gets admitted with ROC-AUC 0.82, well calibrated. Age alone gets 0.78; every other feature combined without age gets 0.74. In odds terms, 75+ have 6.8x the admission odds of a 25-44 year old; being on an e-bike adds 1.11x once age is known. Out of sample, the model assigns 54% of 2024's expected admissions to 65+ falls and 1% to e-bikes.
5. 2026 outlook (the campaign year): 65+ home falls on trend to 641-672k admissions. E-bikes at a realistic 1.2x a year reach 18k (36x smaller). Even if they quadrupled every single year they would reach 199k, still 3x smaller.
6. The message, from 14,747 nurse narratives: bathroom/toilet transfers (122k admissions a year) and getting in/out of bed (107k) are the two moments; 15% of these falls start with dizziness or weakness and those are admitted 51% of the time; people found alone on the floor are admitted 49% of the time. Rugs and footwear, the usual leaflet content, are tiny.
7. Recommendation: spend the $10M on fall-proofing for people 75+ and their carers, focused on bed and bathroom transfers, a "dizzy when you stand, see your doctor" line, and check-ins for those living alone. Do not fund an e-bike ban.

## Section C: what the data cannot tell us
No population or exposure denominators (65+ population also grew; e-bike riding grew faster than injuries). The 2024 sample and weights changed, so any 2023-2024 growth is uncertain. Product recodes masquerade as trends. Deaths are ER deaths only. Severity is driven by age, not product. The 5%/10% campaign effects are assumptions. Extra data that would help: CPSC weight documentation, Census population by age, e-bike trip counts, CDC mortality, hospital cost data.

## Slide-team wording check
Their sentence "under-65s flat (+1%), over-65s +151%, 75+ are 43% of admissions from falls at home, 47x e-bikes, 1 in 6 patients is over 75" has two errors: 43% is the 75+ share of ALL admissions (their share of home-fall admissions is 55%), and no definition gives 47x (it is 56x with our e-bike definition, 37x with Marcus's wider one). Safe wording is in SUBMISSION.md.

## What is left to do (team, not analysis)
Marcus opens his PR; both branches merge into main (checked: no conflicts); deck of 5 slides from FINDINGS.md; zip the repo as the code; email by 20:00.
