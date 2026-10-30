"""Quiz prep part 2: product-name changes, narrative keywords, who-gets-hurt-by-what, biggest changes 2005->2024."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
pd.set_option("display.max_rows", 200); pd.set_option("display.float_format", lambda x: f"{x:,.1f}"); pd.set_option("display.max_colwidth", 60)
df = load("data/clean.parquet")
def H(t): print(f"\n{'='*8} {t} {'='*8}")

H("QUIRK 4: toys names by year (rows)")
t = df[df["product"].str.startswith("Toys", na=False)]
print(pd.crosstab(t["product"], t.year))
H("Products present in only some years: count by first year seen")
py = df.groupby("product").year.agg(lambda s: tuple(sorted(s.unique())))
print(py.value_counts().head(10))
new24 = py[py.apply(lambda y: 2005 not in y and 2014 not in y)]
print("new since 2023 (top by 2024 est):")
print(df[df["product"].isin(new24.index)].groupby("product").weight.sum().sort_values(ascending=False).head(10))
gone = py[py.apply(lambda y: 2023 not in y and 2024 not in y)]
print("gone after 2014 (top by est):"); print(df[df["product"].isin(gone.index)].groupby("product").weight.sum().sort_values(ascending=False).head(8))

H("BIGGEST product changes 2005 -> 2024 (est, products present both years)")
pv = df.pivot_table(index="product", columns="year", values="weight", aggfunc="sum")
both = pv.dropna(subset=[2005, 2024]); both = both[(both[2005] > 20000) | (both[2024] > 20000)]
both["chg"] = both[2024] - both[2005]; both["x"] = both[2024] / both[2005]
print("UP:"); print(both.sort_values("chg", ascending=False).head(8)[[2005, 2014, 2023, 2024, "x"]])
print("DOWN:"); print(both.sort_values("chg").head(8)[[2005, 2014, 2023, 2024, "x"]])

H("Micromobility products by year (est)")
m = df[df.product_group == "Bikes & micromobility"]
print(m.pivot_table(index="product", columns="year", values="weight", aggfunc="sum").fillna(0).sort_values(2024, ascending=False).head(10))

H("TOP product by age group (est)")
for g, d in df.groupby("age_group", observed=True):
    s = d.groupby("product").weight.sum().sort_values(ascending=False)
    print(f"{g}: " + " | ".join(f"{p[:35]} {v/1e3:,.0f}k" for p, v in s.head(3).items()))
H("Infants (<2y, months code): top products"); print(df[df.is_infant_months].groupby("product").weight.sum().sort_values(ascending=False).head(5))
H("TOP product by sex (est)")
for g, d in df[df.sex != "Unknown"].groupby("sex"):
    print(g, d.groupby("product").weight.sum().sort_values(ascending=False).head(4).round(0).to_dict())
H("Top diagnosis per body part head/finger")
for bp in ["Head", "Finger", "Face"]:
    print(bp, df[df.body_part == bp].groupby("diagnosis").weight.sum().sort_values(ascending=False).head(3).round(0).to_dict())

H("NARRATIVE keywords: rows (naive vs careful) by year")
N = df.narrative.fillna("")
kw = {
  "TRAMPOLINE": N.str.contains(r"\bTRAMPOLINE", regex=True),
  "HELMET (naive)": N.str.contains("HELMET"),
  "NO/WITHOUT HELMET": N.str.contains(r"\b(?:NO|WITHOUT|W/O|NOT WEARING(?: A)?) HELMET", regex=True),
  "CAR (naive)": N.str.contains("CAR"),
  "CAR (word)": N.str.contains(r"\bCARS?\b", regex=True),
  "ETOH": N.str.contains(r"\bETOH\b", regex=True),
  "LOC": N.str.contains(r"\bLOC\b", regex=True),
  "DOG": N.str.contains(r"\bDOGS?\b", regex=True),
  "PICKLEBALL": N.str.contains("PICKLEBALL"),
  "E-SCOOTER/ELECTRIC SCOOTER": N.str.contains(r"E-?SCOOTER|ELECTRIC SCOOTER|ELEC SCOOTER", regex=True),
  "NURSING HOME": N.str.contains("NURSING HOME"),
}
print(pd.DataFrame({k: v.groupby(df.year).sum() for k, v in kw.items()}).T)
print("\nETOH in narrative vs alcohol_involved=1 (2023-24):")
r = df[df.year >= 2023]; e = r.narrative.str.contains(r"\bETOH\b", regex=True, na=False)
print(pd.crosstab(e, r.alcohol_involved, margins=True))
print("\nSample 'CAR' naive matches that aren't the word CAR:")
print(df[kw["CAR (naive)"] & ~kw["CAR (word)"]].narrative.str.extract(r"(\w*CAR\w*)")[0].value_counts().head(8))
