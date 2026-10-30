# US Emergency Room Product Injuries: 2005, 2014, 2023, 2024

## What is this?
Every row is **one visit to a US hospital emergency room (ER)** by someone injured in an incident involving a consumer product: a bed, stairs, a bicycle, a knife, a football…

The data comes from a US government safety agency (the Consumer Product Safety Commission). They don't record every ER in the country. They use a **sample of about 80–100 hospitals** chosen to represent the whole US, the same way an opinion poll represents a whole population.

To keep the files small, this datathon version is a **random 1-in-5 sample** of the agency's records. The weights have been scaled up to match, so adding up `weight` still gives national estimates.

## Files
| File | Rows | Use it for |
|---|---|---|
| `neiss_2005.csv`, `neiss_2014.csv`, `neiss_2023.csv`, `neiss_2024.csv` | ~68k–74k each | one year at a time |
| `neiss_all_years.csv` | ~286k | all four years together |

Every file opens in Excel.

All files have the same 15 columns.

## Columns
| Column | Example | Meaning |
|---|---|---|
| `case_id` | 240138835 | unique ID of the ER visit |
| `year` | 2024 | year of the visit |
| `treatment_date` | 2024-01-05 | date of the ER visit |
| `age` | 12 | age of the patient (**see rule 2**) |
| `sex` | Male | Male / Female / Unknown |
| `body_part` | Foot | main injured body part |
| `diagnosis` | Contusion/abrasion | what the doctor diagnosed |
| `outcome` | Treated and released | what happened next: released, admitted to hospital, transferred, died… |
| `location` | Sports/recreation place | where the injury happened |
| `product` | Soccer | the product or activity involved |
| `product_group` | Team & ball sports | a broad group of products |
| `alcohol_involved` | No | whether alcohol was involved (**see rule 3**) |
| `hospital_type` | Small | type of sample hospital: Small / Medium / Large / Very large / Children's |
| `weight` | 522.29 | how many US ER visits this row represents (**see rule 1**) |
| `narrative` | "12 YOM WAS HIT IN FOOT WHILE PLAYING SOCCER DX: CONTUSION" | the nurse's short note about what happened |

## The 5 rules you must know
1. **Rows are not national totals. Use `weight`.** Each row is one patient at a *sample* hospital. `weight` says how many real ER visits across the US that row stands for. To estimate a national number, **add up `weight`** instead of counting rows. The two can give very different answers.
2. **Ages above 200 are babies, measured in months.** `201` = 1 month old, `212` = 12 months, `223` = 23 months. Everyone aged 2 and over is in normal years. `0` means the age is unknown.
3. **Blank does not mean "No".** `alcohol_involved` only started being recorded in 2019. In the 2005 and 2014 files it is blank because nobody collected it.
4. **Product names can change between years.** The agency sometimes splits, merges or renames product categories. The same thing can appear under different names in different years, and new categories can appear.
5. **"Not recorded" is a real answer.** Some columns (e.g. `location`) have a "Not recorded" value. Decide whether to include it before calculating percentages.

## Reading the narrative
The nurse's notes use medical shorthand:

| Shorthand | Meaning | Shorthand | Meaning |
|---|---|---|---|
| YOM / YOF | year-old male / female | DX | diagnosis |
| MOM / MOF | month-old male / female | FX | fracture |
| PT | patient | LAC | laceration (cut) |
| C/O | complains of | CHI | closed head injury |
| S/P | "status post" = after | LOC | loss of consciousness |
| ETOH | alcohol | `***` | text removed for privacy |

**Tip:** the narrative is searchable. Excel: filter "Text contains…". Python: `df[df.narrative.str.contains("TRAMPOLINE")]`. Before trusting a keyword count, read 10–20 of the matching rows: "HELMET" also matches "NO HELMET", and "CAR" also matches "CARPET".
