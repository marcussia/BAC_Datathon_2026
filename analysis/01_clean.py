"""Load NEISS all-years file, sanity-check vs per-year files, decode age, save data/clean.parquet."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *

df = clean(load("data/neiss_all_years.csv"))

# all_years should be exactly the 4 yearly files stacked
yearly = pd.concat([load(f"data/neiss_{y}.csv") for y in (2005, 2014, 2023, 2024)])
print("rows all_years:", len(df), "| sum of yearly files:", len(yearly), "| case_id unique:", df.case_id.is_unique)
print("weight sums match:", np.isclose(df.weight.sum(), yearly.weight.sum()))

# Quirk 2: age code. 0 = unknown, 201-223 = months (1-23), else years
a = df["age"]
df["age_unknown"] = a.eq(0)
df["is_infant_months"] = a.between(201, 223)
df["age_years"] = np.where(df.age_unknown, np.nan, np.where(df.is_infant_months, (a - 200) / 12, a))
df["age_group"] = pd.cut(df.age_years, [-0.01, 4, 14, 24, 44, 64, 200],
                         labels=["0-4", "5-14", "15-24", "25-44", "45-64", "65+"])
# Quirk 3: alcohol only collected 2019+, so mark 2005/2014 as not collected (NaN), not 0
print("alcohol non-null by year:\n", df.groupby("year").alcohol_involved.apply(lambda s: s.notna().mean()).round(3))
df["died"] = df.outcome.str.contains("Died|death|Fatal|DOA", case=False, na=False).astype(int)
df["admitted"] = df.outcome.str.contains("Admitted|Hospitalized", case=False, na=False).astype(int)
df.to_parquet("data/clean.parquet", index=False)
print("saved data/clean.parquet", df.shape)
print(df.outcome.value_counts())
