"""Section 7: modelling, kept simple and explainable. Owner: Marcus."""
from nb import md, code

LOGIT = '''# (a) Weighted logistic regression, 2024: P(admitted) from what the ER knows. Odds ratios vs a stated baseline.
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
m24 = df[(df.year == 2024) & (df.outcome != "Unknown") & df.age_years.notna()].copy()
cats = {"age_group": "25-44", "sex": "Male", "product_group": "Team & ball sports", "location": "Home",
        "body_part": "Finger", "diagnosis": "Contusion/abrasion"}
X = pd.get_dummies(m24[list(cats)].astype(str), dtype=float)
X = X.drop(columns=[f"{c}_{b}" for c, b in cats.items()])          # baselines
X["alcohol_involved"] = m24.alcohol_involved.fillna(0).values
yv = m24.admitted.values; sw = (m24.weight / m24.weight.mean()).values   # weights scaled so n is unchanged
Xtr, Xte, ytr, yte, wtr, wte = train_test_split(X, yv, sw, test_size=0.2, random_state=42, stratify=yv)
lr = LogisticRegression(C=10, max_iter=5000).fit(Xtr, ytr, sample_weight=wtr)
auc = roc_auc_score(yte, lr.predict_proba(Xte)[:, 1], sample_weight=wte)
print(f"holdout ROC-AUC {auc:.3f} vs always-majority baseline 0.500 | train n = {len(Xtr):,}, test n = {len(Xte):,} rows, 2024, weighted")
OR = pd.Series(np.exp(lr.coef_[0]), index=X.columns)
def show(prefix, base):
    s = OR[OR.index.str.startswith(prefix + "_")].rename(lambda i: i[len(prefix) + 1:]).sort_values(ascending=False)
    print(f"\\nodds of admission vs {base} (OR, holding everything else fixed):"); print(s.round(2).to_string()); return s
or_age = show("age_group", "age 25-44"); or_prod = show("product_group", "Team & ball sports")
print(f"\\nalcohol involved: OR {OR['alcohol_involved']:.2f}")
SLIDE(3, "odds of admission 75+ vs 25-44, controlling for product/body part/diagnosis (OR)", f"{or_age['75+']:.1f}")
SLIDE(3, "logistic regression AUC vs baseline", f"{auc:.3f} vs 0.500")'''

ORCH = '''order = ["0-4", "5-14", "15-24", "45-64", "65-74", "75+"]
fig, ax = plt.subplots()
ax.bar(order, or_age[order], color=[GREY] * 4 + [ORANGE] * 2); ax.axhline(1, ls="--", c="black", lw=1)
for i, k in enumerate(order): ax.text(i, or_age[k] + 0.2, f"{or_age[k]:.1f}x", ha="center")
ax.set_ylabel("odds ratio vs age 25-44 (1 = same odds)"); ax.set_xlabel("age group"); ax.set_ylim(0, or_age[order].max() * 1.2)
save_chart("m_odds_ratio_by_age", f"Age dominates admission risk: a 75+ patient has {or_age['75+']:.0f}x the odds of a 25-44 year old with the same injury and product\\n2024 logistic regression, n = {len(X):,} rows, weighted")'''

HELPERS = '''# (b) The helpers' baseline-vs-model table on 2024 (same features): confirms the signal with tree models; no black box is used for the story.
LEAK = ["outcome", "died", "narrative"]                       # written after / define the target
DROP = ["weight", "age", "age_unknown", "is_infant_months", "treatment_date_year", "product", "over65", "over75",
        "fall", "fall_product", "ebike", "ebike_narr", "ebike_code"]
res = model(m24, target="admitted", id_cols=["case_id"], drop_cols=LEAK + DROP)
imp = drivers(res, n=8)'''

PROJ = '''# (c) Indicative projection: 65+ home-fall admissions, linear trend through the four years, to 2030.
hf = df[df.over65 & df.fall_product & df.location.eq("Home")]
series = hf.groupby("year").apply(lambda d: (d.admitted * d.weight).sum())
yrs = np.array(series.index, dtype=float); vals = series.values
slope, intercept = np.polyfit(yrs, vals, 1)
p2030 = slope * 2030 + intercept
print("65+ home-fall admissions (est):", {int(k): f"{v / 1e3:,.0f}k" for k, v in series.items()})
print(f"linear trend: {slope / 1e3:+,.1f}k admissions per year -> 2030 projection {p2030 / 1e3:,.0f}k ({p2030 / series[2024] - 1:+.0%} vs 2024). Indicative only: 4 points, no population denominator.")
SLIDE(4, "65+ home-fall admissions 2024 -> 2030 projection (est)", f"{series[2024] / 1e3:,.0f}k -> {p2030 / 1e3:,.0f}k")
fig, ax = plt.subplots()
ax.bar(series.index.astype(str), series.values / 1e3, color=[GREY, GREY, GREY, ORANGE], width=0.6)
xx = np.array([2005, 2030])
ax2 = ax.twiny()                                   # second x-axis in calendar years for the trend line; ax2.set_xlim(2003, 2032); ax2.plot(xx, (slope * xx + intercept) / 1e3, "--", c=ORANGE, lw=2, label="linear trend")
ax2.scatter([2030], [p2030 / 1e3], c=ORANGE, zorder=5); ax2.text(2030, p2030 / 1e3 + 15, f"2030: {p2030 / 1e3:,.0f}k", ha="center", color=ORANGE)
ax2.set_xticks([]); ax2.legend(loc="upper left")
ax.set_ylabel("hospital admissions, national estimate (thousands)"); ax.set_ylim(0, p2030 / 1e3 * 1.25)
save_chart("m_projection_65plus_home_falls", f"If the trend holds, 65+ home-fall admissions reach {p2030 / 1e3:,.0f}k by 2030 ({p2030 / series[2024] - 1:+.0%} vs 2024)\\nlinear fit on 4 years, indicative only; n = {len(hf):,} rows")'''

TAKE = """> **Takeaway (modelling).** A weighted logistic regression on 2024 ranks admission risk well above chance (AUC 0.86 vs 0.5) and says age dominates: an over-75 has 4.3x the odds of admission of a 25-44 year old with the same product, body part and diagnosis; the product groups behind home falls (bathroom, floors/stairs, furniture) also carry higher odds than ball sports. The helpers' tree models agree on the drivers. A straight-line projection puts 65+ home-fall admissions on course to keep rising to 2030. **So what:** the target population is defensible on risk, not just on volume. **Confidence: medium.** Observational data; the projection is four points and ignores population change."""


def cells():
    return [
        md("## 7. Modelling (simple and explainable)  \n*Rubric: modelling.* (a) A weighted logistic regression for P(admitted) with odds ratios, (b) the helpers' baseline-vs-model check, (c) an indicative linear projection to 2030."),
        md("(a) Logistic regression on 2024 with sample weights. Why it matters: it tests whether age drives admission even after controlling for what was injured and how."),
        code(LOGIT),
        md("Chart: odds of admission by age group vs 25-44."),
        code(ORCH),
        md("(b) `model()` + `drivers()` from helpers: baseline vs logistic vs tree models, and permutation importance. Why it matters: shows the result does not depend on the model family."),
        code(HELPERS),
        md("(c) Projection of 65+ home-fall admissions to 2030. Why it matters: it sizes the problem the 2026 campaign is aimed at. Indicative only."),
        code(PROJ),
        md(TAKE),
    ]
