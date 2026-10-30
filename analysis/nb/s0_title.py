"""Section 0: title and executive summary. Owner: both. Numbers below are copied from the executed notebook outputs."""
from nb import md

TITLE = """# Product injuries, e-bikes and the $10M: a fact-check of the headline
**BAC Datathon 2026, Round 2. Team Nai Loong: Marcus, Germaine, Pin Wei, Jay.**

**The headline:** *"Product injuries surged 18% in 2024, and e-bikes are the deadly new threat. E-bike injuries nearly quadrupled in a year."*

**Executive summary.** __SUMMARY__

**How to read this notebook.** Sections follow the marking rubric: data quality and weights (2), factuality of each claim (3-5), insight (6), modelling (7), recommendation (8), limitations (9). Every number used on a slide is printed with a `SLIDE n:` label and collected in the appendix (10). National estimates are SUM(weight); row counts are labelled *rows*.

**Data:** NEISS 2005, 2014, 2023, 2024; 1-in-5 random sample with weights scaled to national totals; 285,559 rows = 54.3M estimated US ER visits for consumer-product injuries."""

SUMMARY = ("Of the three claims, one partly holds and two do not. The 18% rise is +18.3% by weight but +6.9% by sampled ER visits; most of the gap is a 10.6% jump in survey weights and a low 2023 base, so underlying growth is single-digit. "
           "E-bike injuries did not quadruple: the 2024 e-bike product code is a rename of the 2023 moped code; like-for-like growth is 1.2-1.6x, to 0.7% of all visits. E-bikes caused 0 of 56 deaths in 2024. "
           "The real story is ageing: injuries to under-65s are flat since 2005 (+1%) while injuries to over-65s are up 151%; one in six 2024 patients is over 75 and they are 43% of all hospital admissions. "
           "Over-75s falling at home on floors, stairs, furniture and bathroom fixtures caused 23x more admissions than e-bikes (41x on the headline's own e-bike definition) and 21% of all admissions."
           "**Recommendation:** spend the $10M on home-fall prevention for over-75s, delivered through homes, GPs and pharmacies; respond to e-bikes with helmet and sober-riding enforcement, not a ban.")


def cells():
    return [md(TITLE.replace("__SUMMARY__", SUMMARY))]
