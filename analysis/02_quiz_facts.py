"""Quiz prep: headline facts, each as rows (COUNT) and national estimate (SUM weight)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
pd.set_option("display.max_rows", 200); pd.set_option("display.float_format", lambda x: f"{x:,.1f}")
df = load("data/clean.parquet")

def rw(d, col, n=10):
    """Rows and weighted estimate per group, with ranks and shares."""
    g = d.groupby(col, observed=True).agg(rows=("case_id", "size"), est=("weight", "sum"))
    g["row_%"] = g.rows / g.rows.sum() * 100
    g["est_%"] = g.est / g.est.sum() * 100
    g["rank_rows"] = g.rows.rank(ascending=False).astype(int)
    g["rank_est"] = g.est.rank(ascending=False).astype(int)
    return g.sort_values("est", ascending=False).head(n)

def H(t): print(f"\n{'='*8} {t} {'='*8}")

H("SIZE BY YEAR")
y = df.groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"),
                           w_min=("weight", "min"), w_max=("weight", "max"), w_mean=("weight", "mean"),
                           d_min=("treatment_date", "min"), d_max=("treatment_date", "max"))
print(y); print("TOTAL rows", len(df), "| est", f"{df.weight.sum():,.0f}")
print("distinct products:", df["product"].nunique(), "| groups:", df.product_group.nunique())
print("products per year:", df.groupby("year")["product"].nunique().to_dict())

for col, n in [("product_group", 14), ("product", 15), ("body_part", 10), ("diagnosis", 10),
               ("location", 12), ("outcome", 8), ("sex", 4), ("hospital_type", 6), ("age_group", 7)]:
    H(f"{col.upper()} (all years)"); print(rw(df, col, n))

H("TOP 5 PRODUCTS BY YEAR (est)")
for yr, d in df.groupby("year"):
    print(yr, rw(d, "product", 5)[["rows", "est", "est_%", "rank_rows"]].round(1).to_string(), sep="\n")

H("PRODUCT GROUP SHARE BY YEAR (est %)")
print(pd.crosstab(df.product_group, df.year, values=df.weight, aggfunc="sum", normalize="columns").mul(100).round(1))

H("AGE")
k = df[df.age_years.notna()]
print("unknown age rows:", int(df.age_unknown.sum()), "| infant(201-223) rows:", int(df.is_infant_months.sum()))
print("raw age mean (WRONG, mixes codes):", round(df.age.mean(), 2))
print("decoded mean age rows:", round(k.age_years.mean(), 2), "| weighted:", round(np.average(k.age_years, weights=k.weight), 2),
      "| median rows:", k.age_years.median())
print("by year decoded mean (weighted):", k.groupby("year").apply(lambda d: np.average(d.age_years, weights=d.weight)).round(2).to_dict())
print("oldest age:", k.age_years.max(), "| raw age values >120 & <201:", int(df.age.between(121, 200).sum()))
print("infants est by year:", df[df.is_infant_months].groupby("year").weight.sum().round(0).to_dict())

H("SEX share by year (est %, excl Unknown)")
s = df[df.sex != "Unknown"]
print(pd.crosstab(s.year, s.sex, values=s.weight, aggfunc="sum", normalize="index").mul(100).round(1))

H("OUTCOMES: admitted & died by year")
o = df.groupby("year").apply(lambda d: pd.Series({
    "died_rows": d.died.sum(), "died_est": (d.died * d.weight).sum(),
    "admit_row_%": d.admitted.mean() * 100, "admit_est_%": np.average(d.admitted, weights=d.weight) * 100}))
print(o)
H("DEATHS by product (rows/est, top 10)"); print(rw(df[df.died == 1], "product", 10))
H("DEATHS by age_group"); print(rw(df[df.died == 1], "age_group", 7))
H("ADMISSION rate by age_group (est %)")
print(df.groupby("age_group", observed=True).apply(lambda d: np.average(d.admitted, weights=d.weight) * 100).round(1))
H("ADMISSION rate by product_group (est %)")
print(df.groupby("product_group").apply(lambda d: np.average(d.admitted, weights=d.weight) * 100).sort_values(ascending=False).round(1))

H("LOCATION: share at Home, two denominators, by year")
home = df.location.str.contains("Home", na=False)
nr = df.location.eq("Not recorded")
for yr in sorted(df.year.unique()):
    m = df.year == yr; w = df.weight
    print(yr, f"home/all={w[m & home].sum() / w[m].sum():.1%}",
          f"home/known={w[m & home].sum() / w[m & ~nr].sum():.1%}", f"not_recorded={w[m & nr].sum() / w[m].sum():.1%}")
print("location values:", df.location.unique().tolist())

H("ALCOHOL (2023-24 only)")
a = df[df.year >= 2023]
print(a.groupby("year").apply(lambda d: pd.Series({"yes_rows": d.alcohol_involved.sum(),
      "yes_row_%": d.alcohol_involved.mean() * 100, "yes_est_%": np.average(d.alcohol_involved, weights=d.weight) * 100})))
print("top products where alcohol=1:"); print(rw(a[a.alcohol_involved == 1], "product", 8))
print("alcohol by sex (est %):", a.groupby("sex").apply(lambda d: np.average(d.alcohol_involved, weights=d.weight) * 100).round(1).to_dict())

H("HOSPITAL TYPE: rows vs est (oversampling)")
print(rw(df, "hospital_type", 6))
print(df.groupby("hospital_type").weight.agg(["min", "mean", "max"]))

H("UNKNOWN shares by year (row %)")
unk = pd.DataFrame({"location_NR": df.location.eq("Not recorded"), "diag_other": df.diagnosis.eq("Other/not stated"),
                    "body_unknown": df.body_part.eq("Not stated/unknown"), "sex_unknown": df.sex.eq("Unknown"),
                    "outcome_unknown": df.outcome.eq("Unknown"), "age_0": df.age_unknown, "year": df.year})
print(unk.groupby("year").mean().mul(100).round(2))

H("SEASONALITY: est by month & day of week (all years)")
print(df.groupby("treatment_date_month").weight.sum().div(1e3).round(0).to_dict())
print(df.groupby("treatment_date_dow").weight.sum().div(1e3).round(0).to_dict(), "(0=Mon)")
print("busiest single date:", df.groupby("treatment_date").weight.sum().idxmax(), "| by rows:", df.treatment_date.value_counts().idxmax())

H("NARRATIVE length by year")
print(df.assign(L=df.narrative.str.len()).groupby("year").L.agg(["mean", "max"]).round(1))
