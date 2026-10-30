"""B4. Predictive model that backs the recommendation: P(admitted | who, what, where).
Weighted (sample_weight = NEISS weight), trained on 2005-2023, tested on 2024 (temporal validation).
Features are known BEFORE diagnosis (no diagnosis/body_part/outcome -> no leakage into the policy question).
Outputs: analysis/24_*.csv, charts/b_severity_odds.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

df = load("data/clean.parquet")
n = df.narrative.fillna("")
EBIKE = r"E-BIKE|EBIKE|E BIKE|E-BICYCLE|ELECTRIC BIKE|ELEC BIKE|ELECTRIC BICYCLE|ELECTRIC PEDAL|PEDAL ASSIST|MOTORIZED BI"
df["ebike"] = (n.str.contains(EBIKE, regex=True) | df["product"].eq("Electric power-assisted pedal bicycles")).astype(int)
df["pedal_bike"] = (df["product"].str.contains("Bicycles and accessories|Mountain or all-terrain bicycles") & (df.ebike == 0)).astype(int)
df["powered_scooter"] = (df["product"].eq("Scooters, powered") | n.str.contains("ELECTRIC SCOOTER|E-SCOOTER")).astype(int)
df["fall"] = n.str.contains(r"FELL|FALL|SLIP|TRIP|STUMBL|LOST BALANCE", regex=True).astype(int)
df["alcohol"] = df.alcohol_involved.map({1: "Yes", 0: "No", 1.0: "Yes", 0.0: "No"}).fillna("Not collected").astype(str)
df["age_missing"] = df.age_years.isna().astype(int)
df["age_f"] = df.age_years.fillna(df.age_years.median())
df["month"] = df.treatment_date_month

cat = ["sex", "product_group", "location", "alcohol", "hospital_type"]
num = ["age_f", "age_missing", "ebike", "pedal_bike", "powered_scooter", "fall", "month", "year"]
X = df[cat + num].copy()
for c in cat:
    X[c] = X[c].astype("category")
y = df.admitted.values
w = df.weight.values
train = (df.year < 2024).values
test = (df.year == 2024).values

# ---- Model 1: gradient boosting, weighted, temporal validation ----
hgb = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.06, max_leaf_nodes=31, min_samples_leaf=100,
                                     l2_regularization=1.0, categorical_features="from_dtype", random_state=0)
hgb.fit(X[train], y[train], sample_weight=w[train])
p = hgb.predict_proba(X[test])[:, 1]
base = np.average(y[test], weights=w[test])
auc = roc_auc_score(y[test], p, sample_weight=w[test]); pr = average_precision_score(y[test], p, sample_weight=w[test])
print("=== Gradient boosting: train 2005-2023 (n = %s), test 2024 (n = %s), weighted ===" % (f"{train.sum():,}", f"{test.sum():,}"))
print(f"2024 weighted admitted rate {base:.3f} | ROC-AUC {auc:.3f} | PR-AUC {pr:.3f} (random = {base:.3f}) | Brier {brier_score_loss(y[test], p, sample_weight=w[test]):.4f}")
t = pd.DataFrame({"p": p, "y": y[test], "w": w[test]}); t["dec"] = pd.qcut(t.p, 10, labels=False, duplicates="drop")
cal = t.groupby("dec").apply(lambda g: pd.Series({"pred": np.average(g.p, weights=g.w), "obs": np.average(g.y, weights=g.w), "n_rows": len(g)}), include_groups=False)
print("calibration by predicted-risk decile (pred vs observed):"); print(cal.round(3).to_string())
cal.to_csv("analysis/24_calibration_2024.csv")
# top-decile capture
t = t.sort_values("p", ascending=False); t["cw"] = t.w.cumsum() / t.w.sum(); t["cy"] = (t.w * t.y).cumsum() / (t.w * t.y).sum()
cap20 = t.loc[t.cw <= 0.2, "cy"].max()
print(f"targeting the highest-risk 20% of 2024 visits captures {cap20:.0%} of admissions ({cap20/0.2:.1f}x random)")

# ---- baselines: how much of the AUC is age alone? does dropping hospital_type (admission practice) change the ranking? ----
def fit_auc(cols):
    Xb = X[cols]; mb = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06, min_samples_leaf=100,
                                                       categorical_features="from_dtype", random_state=0)
    mb.fit(Xb[train], y[train], sample_weight=w[train]); pb = mb.predict_proba(Xb[test])[:, 1]
    return roc_auc_score(y[test], pb, sample_weight=w[test]), average_precision_score(y[test], pb, sample_weight=w[test])
bl = pd.DataFrame({"features": ["age only", "age + fall flag", "all except hospital_type", "all except age", "all (main model)"],
                   "roc_auc": 0.0, "pr_auc": 0.0})
for i, cols in enumerate([["age_f"], ["age_f", "fall"], [c for c in cat + num if c != "hospital_type"], [c for c in cat + num if c not in ("age_f", "age_missing")], cat + num]):
    bl.loc[i, ["roc_auc", "pr_auc"]] = fit_auc(cols)
print("\nbaselines (2024, weighted):"); print(bl.round(3).to_string(index=False)); bl.to_csv("analysis/24_baselines.csv", index=False)

rng = np.random.default_rng(0); idx = rng.choice(np.where(test)[0], 20000, replace=False)
Xs, ys, ws = X.iloc[idx], y[idx], w[idx]; auc0 = roc_auc_score(ys, hgb.predict_proba(Xs)[:, 1], sample_weight=ws)
imp = {}
for c in Xs.columns:
    Xp = Xs.copy(); Xp[c] = Xp[c].sample(frac=1, random_state=1).values
    imp[c] = auc0 - roc_auc_score(ys, hgb.predict_proba(Xp)[:, 1], sample_weight=ws)
imp = pd.Series(imp).sort_values(ascending=False)
print("permutation importance (AUC drop when shuffled):"); print(imp.round(4).to_string()); imp.to_csv("analysis/24_importance.csv")

# ---- Model 2: logistic regression, 2023-24 (alcohol exists), interpretable odds ratios ----
df["age_band"] = pd.cut(df.age_f, [-0.1, 4, 14, 24, 44, 64, 74, 120], labels=["0-4", "5-14", "15-24", "25-44", "45-64", "65-74", "75+"]).astype(str)
df["vehicle"] = np.select([df.ebike == 1, df.powered_scooter == 1, df.pedal_bike == 1], ["e-bike", "powered scooter", "pedal bicycle"], "none")
df["fall_f"] = np.where(df.fall == 1, "fall", "no fall")
lcat = ["age_band", "sex", "product_group", "location", "alcohol", "vehicle", "fall_f", "hospital_type"]
L = df[lcat].astype(str)
ref = {"age_band": "25-44", "sex": "Female", "product_group": "Team & ball sports", "location": "Home", "alcohol": "No",
       "vehicle": "none", "fall_f": "no fall", "hospital_type": "Very large"}
pipe = Pipeline([("ohe", OneHotEncoder(handle_unknown="ignore")), ("lr", LogisticRegression(max_iter=3000, C=1.0))])
m = df.year.isin([2023, 2024]).values
pipe.fit(L[m], y[m], lr__sample_weight=w[m])
names = pipe.named_steps["ohe"].get_feature_names_out(lcat); ors = pd.Series(np.exp(pipe.named_steps["lr"].coef_[0]), index=names)
rows = []
for v in lcat:
    r = ors[f"{v}_{ref[v]}"]
    for k in [x for x in names if x.startswith(v + "_")]:
        rows.append((v, k[len(v) + 1:], ors[k] / r))
ortab = pd.DataFrame(rows, columns=["variable", "level", "odds_ratio_vs_ref"])
print(f"\n=== Logistic regression 2023-24 (n = {m.sum():,}, weighted), 2024 ROC-AUC {roc_auc_score(y[test], pipe.predict_proba(L[test])[:,1], sample_weight=w[test]):.3f} ===")
show = ortab[ortab.variable.isin(["age_band", "vehicle", "alcohol", "sex", "fall_f"])].sort_values(["variable", "odds_ratio_vs_ref"])
print(show.round(2).to_string(index=False)); ortab.to_csv("analysis/24_odds_ratios.csv", index=False)

# chart: odds ratios for age bands + vehicle + alcohol
pick = [("age_band", "0-4"), ("age_band", "5-14"), ("age_band", "15-24"), ("age_band", "25-44"), ("age_band", "45-64"), ("age_band", "65-74"), ("age_band", "75+"),
        ("alcohol", "Yes"), ("vehicle", "pedal bicycle"), ("vehicle", "powered scooter"), ("vehicle", "e-bike")]
lab = {"age_band": "age ", "alcohol": "alcohol ", "vehicle": ""}
vals = [ortab[(ortab.variable == a) & (ortab.level == b)].odds_ratio_vs_ref.iloc[0] for a, b in pick]
labels = [lab[a] + b + (" (ref)" if (a, b) == ("age_band", "25-44") else "") for a, b in pick]
colors = [ORANGE if a == "age_band" and b in ("65-74", "75+") else (ACCENT if a == "vehicle" else GREY) for a, b in pick]
fig, ax = plt.subplots(figsize=(10, 6))
yy = np.arange(len(pick))[::-1]
ax.barh(yy, vals, color=colors)
for yi, v in zip(yy, vals):
    ax.text(v + 0.1, yi, f"{v:.2f}x", va="center", fontsize=12)
ax.axvline(1, color="black", lw=1, ls="--"); ax.set_yticks(yy); ax.set_yticklabels(labels)
ax.set_xlim(0, max(vals) * 1.18); ax.set_xlabel("odds of hospital admission vs reference (age 25-44, no vehicle, no alcohol), 2023-24, weighted")
o75 = ortab[(ortab.variable == "age_band") & (ortab.level == "75+")].odds_ratio_vs_ref.iloc[0]
oeb = ortab[(ortab.variable == "vehicle") & (ortab.level == "e-bike")].odds_ratio_vs_ref.iloc[0]
save_chart("b_severity_odds", f"Age drives admission: 75+ have {o75:.1f}x the odds of a 25-44 year old; an e-bike adds {oeb:.2f}x once age is known")

# ---- use the model: expected 2024 admissions by hazard, and what-if ----
d = df[test].copy(); d["p"] = p; d["exp_adm"] = d.p * d.weight
d["hazard"] = np.where(d.ebike == 1, "E-bike", np.where((d.fall == 1) & (d.age_f >= 65), "Fall, 65+", np.where(d.fall == 1, "Fall, under 65", "Other")))
tab = d.groupby("hazard").agg(est_visits=("weight", "sum"), model_expected_adm=("exp_adm", "sum"),
                              observed_adm=("weight", lambda s: (s * d.loc[s.index, "admitted"]).sum()), n_rows=("weight", "size"))
tab["share_expected_%"] = tab.model_expected_adm / tab.model_expected_adm.sum() * 100
print("\n=== 2024: model-expected vs observed admissions by hazard (model trained without 2024) ==="); print(tab.round(0).to_string())
tab.to_csv("analysis/24_expected_adm_by_hazard.csv")
