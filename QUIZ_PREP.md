# Quiz prep: NEISS ER product injuries (2005 / 2014 / 2023 / 2024)

Source: `analysis/02_quiz_facts.py`, `analysis/03_quiz_quirks.py` (outputs saved next to them as `.out.txt`).
"Rows" = COUNT of sample rows. "Est" = SUM(weight) = national estimate. **Read the question for which one it wants.**

## The 6 traps (likely quiz questions)
| # | Trap | Proof from the data |
|---|---|---|
| 1 | Rows ≠ national total; use `weight` | Children's hospitals: **18.5% of rows but 3.2% of est**. Small hospitals: 14.1% of rows → **30.1% of est** (rank 4 → 1). Very large: rank 1 by rows, 4 by est |
| 2 | Age 201–223 = months; 0 = unknown | Raw `age` mean = **44.4 (wrong)**. Decoded: 31.9 (rows), **36.5 (weighted)**. 16,824 infant rows; only 11 rows with age 0; no ages 121–200. Oldest = 108 |
| 3 | Blank alcohol ≠ "No" | `alcohol_involved` 0% filled in 2005 and 2014, 100% in 2023 and 2024 |
| 4 | Product names change | "Toys, not elsewhere classified": 553 rows (2005) → 39 (2014), and "Toys, not specified" appears with 270 rows in 2014. 783 distinct products overall; only 552 appear in all 4 years |
| 5 | "Not recorded" in the denominator | Home share 2024: **36.0% of all** vs **57.3% of known location**. Location "Not recorded" grew 20.6% → 37.2% (est, 2005 → 2024) |
| 6 | Product ≠ something bought | Top products are **stairs and floors** (building parts); "Exercise" and "Soccer" are activities |

Keyword traps (rows): "CAR" naive = 4,367 in 2024 vs 1,278 as a whole word (CARRYING, CART, CARPET, DAYCARE, METACARPAL...). "HELMET" = 1,562 in 2024, but 319 of those are "NO/WITHOUT HELMET". Narratives max out at 142 chars (2005, 2014) vs 400 (2023, 2024), so keyword counts rise for recent years partly because the notes are longer.

## Size
| Year | Rows | National est | Weight min–max | Mean weight |
|---|---|---|---|---|
| 2005 | 72,074 | 12,611,769 | 29.1–415.8 | 175.0 |
| 2014 | 73,498 | 13,842,140 | 28.6–560.8 | 188.3 |
| 2023 | 67,653 | 12,739,755 | 38.0–448.7 | 188.3 |
| 2024 | 72,334 | 15,068,366 | 32.9–540.3 | 208.3 |
| **All** | **285,559** | **54,262,029** | 28.6–560.8 | |

The all-years file equals the 4 yearly files stacked (rows and weights reconcile), and `case_id` is unique. Every year runs Jan 1–Dec 31. 14 product groups.
Note: 2023 has the **fewest rows** but more est than 2005, so rows and est disagree on which year was "smallest".

## Rankings (all years, est; rows rank in brackets where it differs)
**Product groups:** 1 Floors, stairs & building parts 24.5% · 2 Furniture 15.2% · 3 Team & ball sports 11.9% · 4 Fitness & rec 10.8% · 5 Kitchen 7.3% · 6 Tools/yard/DIY 6.6% (rows #8) · 7 Household items 5.8% (rows #6) · 8 Bikes & micromobility 5.5% (rows #7) ... last: Other 0.6%. Toys, babies & kids' products rank #11 by rows but #12 by est.

**Products:** 1 Stairs or steps 4.38M (8.1%) · 2 Floors 4.25M · 3 Beds 2.77M · 4 Bicycles 1.82M (rows #5) · 5 Basketball 1.69M (rows #4) · 6 Football 1.39M · 7 Chairs · 8 Knives (rows #9) · 9 Bathtubs/showers (rows #11) · 10 Ceilings & walls (rows #8)
- **#1 by year (est):** 2005 Stairs · 2014 Stairs · 2023 **Floors** · 2024 **Floors**. But 2024 *by rows* it's still Stairs (5,532 vs 5,337), so the answer flips with the method.

**Body part:** Head 15.3% · Lower trunk (rows #4) · Finger · Face (rows #2) · Upper trunk
**Diagnosis:** Laceration 17.7% · Other/not stated 16.4% (est #2, rows #3) · Fracture 15.2% (rows #2) · Contusion/abrasion · Strain/sprain
**Location:** Home 42.5% of all (est) · Not recorded 30.7% · Sports/rec 12.2% · Other public 7.5% · School/daycare 4.2% · Street 2.8%
**Outcome:** Treated & released 88.2% · Admitted 8.2% · Left w/o being seen 1.6% · Transferred 1.3% · Observation 0.7% · **Died 0.1% (184 rows, est 35,730)**
**Sex:** Male 54.0% est (55.2% rows). Female share 44.6% (2005) → 46.3% (2024)
**Age group (est):** 65+ 20.1% (#1; rows #3) · 25–44 20.0% · 5–14 17.4% (**#1 by rows**) · 45–64 · 15–24 · 0–4 10.3%

## Who gets hurt by what (est)
| Group | Top 3 products |
|---|---|
| 0–4 | Beds 597k · Floors 376k · Tables 290k |
| Infants <2 (months code) | Beds · Floors · Stairs · Sofas · Tables |
| 5–14 | **Football** 690k · Bicycles 597k · Basketball 593k |
| 15–24 | **Basketball** 771k · Football 578k · Stairs 519k |
| 25–44 | Stairs 1,157k · **Knives** 473k · Floors 450k |
| 45–64 | Stairs 1,092k · Floors 759k · Beds 389k |
| 65+ | **Floors** 2,211k · Beds 1,223k · Stairs 1,022k |
| Female | Stairs · Floors · Beds · Chairs |
| Male | Stairs · Floors · Basketball · Bicycles |

Head → most common dx "Internal organ injury" (NEISS's code for internal head injury, e.g. closed head injury), then Laceration, Concussion. Finger and Face → Laceration.

## Severity
- **Admitted share rose:** 4.3% (2005) → 6.3% (2014) → 11.1% (2023) → 10.7% (2024), est.
- **Admitted by age (est):** 65+ **24.7%** vs 0–4 2.2%, 5–14 1.8%, 25–44 3.9%, 45–64 9.2%.
- **Admitted by group (est):** Bathroom **16.7%** (highest) · Floors/stairs 12.7% · Furniture 11.5% · Off-road vehicles 11.3% ... Team & ball sports **1.9%** (lowest).
- **Deaths:** 184 rows in total (45 / 30 / 53 / 56 by year). Top by est: Beds 4,215 · Floors 4,212 (rows #1, with 27 rows) · Stairs 3,824. Age 65+ = 45% of deaths. *Small n, so treat with care.*

## Alcohol (2023 and 2024 only)
- Yes: 2023 **1,330 rows, 2.2% est** · 2024 **1,270 rows, 2.1% est**.
- Male 2.7% vs Female 1.5% (est).
- Top products with alcohol: Stairs 18.1% · Floors 14.0% · Bicycles · Beds · Chairs.
- "ETOH" in the narrative (880 rows) mostly agrees with the flag (843 of them are flagged 1), but 1,757 flagged rows don't mention ETOH, so narrative search undercounts.

## Trends 2005 → 2024 (est)
- **Up:** Beds 421k → 943k (**2.2x**) · Exercise 3.0x · Toilets **3.4x** · Bathtubs/showers 1.8x · Footwear 2.3x · Floors 1.5x. Furniture's share 12.9% → 16.6%, Bathroom's 2.2% → 4.0%. Mean age (weighted) 30.8 → 40.6, i.e. an ageing population.
- **Down:** Basketball 0.7x · Football 0.7x · Baseball 0.6x · ATVs 0.5x · Team & ball sports share 13.7% → 10.7%.
- **New categories (first seen 2023 or 2024):** Scooters, powered (115k in 2024) · Scooters, unspecified · E-bikes (2024 only, 56k) · Power-assisted cycles · Hoverboards. Narrative "E-SCOOTER" rows: 11 (2005) → 370 (2024). Pickleball: 0 → 93 rows.
- **Gone after 2014:** Wheelchairs · Crutches/canes/walkers · First aid equipment, plus the old "Scooters / skateboards, powered", which was split into the new categories.
- "Toys, NEC" fell 0.2x only because of the rename (trap 4). It is not a real drop.

## Timing (all years, est)
- Peak month **July** (4.97M), then May; low month **February** (3.77M).
- Busiest day of week **Sunday**, then Saturday; quietest **Thursday**.
- Busiest single date by est: 2014-04-12; by rows: 2014-05-04.

## Unknowns grow over time (row %)
| | 2005 | 2014 | 2023 | 2024 |
|---|---|---|---|---|
| location Not recorded | 22.0 | 28.7 | 34.6 | 36.9 |
| diagnosis Other/not stated | 7.4 | 13.1 | 20.7 | 21.5 |
| body part unknown | 0.6 | 0.5 | 2.6 | 2.6 |
