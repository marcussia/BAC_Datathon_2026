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
