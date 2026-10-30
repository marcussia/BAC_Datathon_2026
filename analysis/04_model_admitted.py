"""Who gets admitted? Model P(admitted to hospital) from what's known at the ER visit."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
df = load("data/clean.parquet")
df = df[df.outcome != "Unknown"]  # 11 rows with no disposition
print("rows:", len(df), "| admitted rate:", round(df.admitted.mean(), 4))

LEAK = ["outcome",            # the target is derived from it
        "died",               # also derived from outcome
        "narrative"]          # nurse note written after the visit; can say 'ADMITTED'
DROP = ["weight",             # survey bookkeeping, not a patient attribute (proxy for hospital)
        "alcohol_involved",   # blank in 2005/2014; median-impute would turn 'not collected' into 'No'
        "age", "age_group", "age_unknown", "is_infant_months",  # duplicates of decoded age_years
        "treatment_date_year",  # duplicate of year
        "product"]            # 783 levels; product_group carries it
res = model(df, target="admitted", id_cols=["case_id"], drop_cols=LEAK + DROP)
res["table"].to_csv("analysis/04_model_table.csv")
imp = drivers(res, n=10)
print("\nDRIVERS:\n", imp.to_string())

# direction for the top categorical drivers: admitted rate per level vs overall (rows; weighted alongside)
overall = df.admitted.mean()
for c in [c for c in imp.head(6).index if c not in res["num"]]:
    g = df.groupby(c).agg(n=("admitted", "size"), rate=("admitted", "mean"),
                          w_rate=("admitted", lambda s: np.average(s, weights=df.loc[s.index, "weight"])))
    g = g[g.n >= 200]; g["lift"] = g.rate / overall
    print(f"\n{c} (overall {overall:.3f}): top/bottom levels\n", pd.concat([g.nlargest(4, "rate"), g.nsmallest(3, "rate")]).round(3).to_string())

lift = gains(res)
print("\nGAINS:\n", lift.to_string())
lift.to_csv("analysis/04_gains.csv")
# re-save charts with finding-style titles
pc = lift["cum_%_caught"]
x = np.arange(0, 11) * 10
plt.plot(x, np.r_[0, pc.values], marker="o", lw=2.2, color=ACCENT, label="model")
plt.plot([0, 100], [0, 100], "--", c="grey", label="random")
plt.xlabel("% of ER visits flagged (highest risk first)"); plt.ylabel("% of admissions caught"); plt.ylim(0, 100); plt.legend()
save_chart("gains_chart", f"Flagging the riskiest 20% of ER visits catches {pc.iloc[1]:.0f}% of admissions")
ax = imp.head(8).iloc[::-1].plot.barh(color=ACCENT); ax.set_xlabel("drop in ROC-AUC when shuffled")
save_chart("top_drivers", f"Diagnosis and age drive hospital admission most" if list(imp.index[:2]) in (["diagnosis","age_years"],["age_years","diagnosis"]) else f"Top driver of admission: {imp.index[0]}")
print("top 2 drivers:", list(imp.index[:2]))
