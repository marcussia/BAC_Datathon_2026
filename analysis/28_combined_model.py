"""B8. Combined model: Marcus's features (age, sex, product group, location, body part, diagnosis, alcohol)
+ Germaine's (fall flag, vehicle flags, hospital type), on the temporal split (train 2005-2023, test 2024), weighted.
Three rows: pre-diagnosis (24), Marcus-style feature set, combined. Outputs analysis/28_*.csv"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score

df = load("data/clean.parquet")
n = df.narrative.fillna("")
EB = r"E-BIKE|EBIKE|E BIKE|E-BICYCLE|ELECTRIC BIKE|ELEC BIKE|ELECTRIC BICYCLE|ELECTRIC PEDAL|PEDAL ASSIST|MOTORIZED BI"
df["ebike"] = (n.str.contains(EB, regex=True) | df["product"].eq("Electric power-assisted pedal bicycles")).astype(int)
df["pedal_bike"] = (df["product"].str.contains("Bicycles and accessories|Mountain or all-terrain bicycles") & (df.ebike == 0)).astype(int)
df["powered_scooter"] = (df["product"].eq("Scooters, powered") | n.str.contains("ELECTRIC SCOOTER|E-SCOOTER")).astype(int)
df["fall"] = n.str.contains(r"FELL|FALL|SLIP|TRIP|STUMBL|LOST BALANCE", regex=True).astype(int)
df["alcohol"] = df.alcohol_involved.map({1: "Yes", 0: "No", 1.0: "Yes", 0.0: "No"}).fillna("Not collected").astype(str)
df["age_missing"] = df.age_years.isna().astype(int)
df["age_f"] = df.age_years.fillna(df.age_years.median())
y = df.admitted.values; w = df.weight.values
train = (df.year < 2024).values; test = (df.year == 2024).values
CAT_PRE = ["sex", "product_group", "location", "alcohol", "hospital_type"]
NUM_PRE = ["age_f", "age_missing", "ebike", "pedal_bike", "powered_scooter", "fall", "year"]
SETS = {"Germaine pre-diagnosis (analysis/24)": (CAT_PRE, NUM_PRE),
        "Marcus feature set (incl. body part + diagnosis)": (["sex", "product_group", "location", "alcohol", "body_part", "diagnosis"], ["age_f", "age_missing"]),
        "COMBINED (union of both)": (CAT_PRE + ["body_part", "diagnosis"], NUM_PRE)}
rows = []; preds = {}
for name, (cat, num) in SETS.items():
    X = df[cat + num].copy()
    for c in cat: X[c] = X[c].astype("category")
    m = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.06, max_leaf_nodes=31, min_samples_leaf=100,
                                       l2_regularization=1.0, categorical_features="from_dtype", random_state=0)
    m.fit(X[train], y[train], sample_weight=w[train]); p = m.predict_proba(X[test])[:, 1]; preds[name] = p
    rows.append({"model": name, "roc_auc_2024": roc_auc_score(y[test], p, sample_weight=w[test]),
                 "pr_auc_2024": average_precision_score(y[test], p, sample_weight=w[test])})
t = pd.DataFrame(rows); print("=== trained 2005-2023, tested on 2024, weighted ==="); print(t.round(3).to_string(index=False)); t.to_csv("analysis/28_combined_auc.csv", index=False)

# odds ratios from the combined feature set, logistic, 2023-24
df["age_band"] = pd.cut(df.age_f, [-0.1, 4, 14, 24, 44, 64, 74, 120], labels=["0-4", "5-14", "15-24", "25-44", "45-64", "65-74", "75+"]).astype(str)
df["vehicle"] = np.select([df.ebike == 1, df.powered_scooter == 1, df.pedal_bike == 1], ["e-bike", "powered scooter", "pedal bicycle"], "none")
df["fall_f"] = np.where(df.fall == 1, "fall", "no fall")
lcat = ["age_band", "sex", "product_group", "location", "alcohol", "vehicle", "fall_f", "hospital_type", "body_part", "diagnosis"]
L = df[lcat].astype(str); mm = df.year.isin([2023, 2024]).values
pipe = Pipeline([("ohe", OneHotEncoder(handle_unknown="ignore")), ("lr", LogisticRegression(max_iter=3000, C=1.0))]).fit(L[mm], y[mm], lr__sample_weight=w[mm])
names = pipe.named_steps["ohe"].get_feature_names_out(lcat); ors = pd.Series(np.exp(pipe.named_steps["lr"].coef_[0]), index=names)
ref = {"age_band": "25-44", "vehicle": "none", "alcohol": "No", "fall_f": "no fall", "sex": "Female"}
out = []
for v, b in ref.items():
    r = ors[f"{v}_{b}"]
    for k in [x for x in names if x.startswith(v + "_")]: out.append((v, k[len(v) + 1:], ors[k] / r))
ot = pd.DataFrame(out, columns=["variable", "level", "odds_ratio_vs_ref"]).sort_values(["variable", "odds_ratio_vs_ref"])
print(f"\n=== combined logistic 2023-24 (n = {mm.sum():,}), 2024 AUC {roc_auc_score(y[test], pipe.predict_proba(L[test])[:,1], sample_weight=w[test]):.3f}; odds vs reference, controlling for body part AND diagnosis ===")
print(ot.round(2).to_string(index=False)); ot.to_csv("analysis/28_combined_odds.csv", index=False)
# expected admissions by hazard from the combined model
d = df[test].copy(); d["p"] = preds["COMBINED (union of both)"]; d["exp"] = d.p * d.weight
d["hazard"] = np.where(d.ebike == 1, "E-bike", np.where((d.fall == 1) & (d.age_f >= 65), "Fall, 65+", np.where(d.fall == 1, "Fall, under 65", "Other")))
tab = d.groupby("hazard").agg(expected_adm=("exp", "sum"), observed_adm=("weight", lambda s: (s * d.loc[s.index, "admitted"]).sum()))
tab["share_expected_%"] = tab.expected_adm / tab.expected_adm.sum() * 100
print("\n=== combined model: expected vs observed 2024 admissions by hazard ==="); print(tab.round(0).to_string()); tab.to_csv("analysis/28_combined_expected.csv")
