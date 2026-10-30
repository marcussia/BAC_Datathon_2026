# Submission checklist (stop-work 19:55, email by 20:00)

1. Merge PR #1 (germaine/recommendation) and Marcus's headline-check branch into `main`. Both were dry-run merged against each other and main: no conflicts.
2. Deck: max 5 slides. Suggested one-number-per-slide: 4.9x admission (charts/b_adm_rate_by_group.png), 18% vs 7% vs 1.2x fact-check (charts/a_*.png), 62k vs 3k admissions avoided (charts/b_impact_compare.png), 2026 outlook (charts/b_projection_2026.png), message themes (charts/b_message_themes.png) + limits.
3. Code: zip of `main` (analysis/, helpers.py, charts/, FINDINGS.md; data/ is gitignored) or the repo link.
4. Email to abc-bac-training@e.ntu.edu.sg: deck + code. Confirm who sends.
5. Safe wording for the headline slide (every number from analysis/25_slide_claims_check.py):
   "Injuries to under-65s have been flat for 20 years (+1%); injuries to over-65s are up 151%. People 75+ are 1 in 6 ER patients
   but 43% of all hospital admissions, 56 times the admissions caused by every e-bike injury combined."
   Do not say "43% of admissions from falls at home" (that is 55%). Do not say 47x (no definition gives it; 56x with the B e-bike definition, 37x with the wider one).
6. Quote one model only: the weighted severity model (analysis/24, AUC 0.82 on held-out 2024, age-only 0.78, all-but-age 0.74). The Round-1 triage model at the top of FINDINGS.md is marked superseded.
7. Label which "65+ falls" definition each slide uses (see the Definitions block at the top of FINDINGS section B).
