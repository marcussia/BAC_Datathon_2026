"""B5. Verify the slide team's sentence numbers (2005 vs 2024, est = SUM weight)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import *
df = load("data/clean.parquet")
df["adm_w"] = df.weight * df.admitted
FALL = ["Floors or flooring materials", "Rugs or carpets, not specified", "Runners, throw rugs or doormats", "Stairs or steps",
        "Beds or bedframes, other or not specified", "Bathtubs or showers", "Toilets"]
EB = r"E-BIKE|EBIKE|E BIKE|E-BICYCLE|ELECTRIC BIKE|ELEC BIKE|ELECTRIC BICYCLE|ELECTRIC PEDAL|PEDAL ASSIST|MOTORIZED BI"
u65 = df.age_years < 65; o65 = df.age_years >= 65; o75 = df.age_years >= 75
e = lambda m, y: df[m & (df.year == y)].weight.sum()
a = lambda m, y: df[m & (df.year == y)].adm_w.sum()
print(f"under-65 visits 2005 {e(u65,2005):,.0f} -> 2024 {e(u65,2024):,.0f} = {e(u65,2024)/e(u65,2005)-1:+.1%}")
print(f"65+ visits 2005 {e(o65,2005):,.0f} -> 2024 {e(o65,2024):,.0f} = {e(o65,2024)/e(o65,2005)-1:+.1%}")
print(f"75+ visits 2005 {e(o75,2005):,.0f} -> 2024 {e(o75,2024):,.0f} = {e(o75,2024)/e(o75,2005)-1:+.1%}")
allm = df.age_years.notna() | df.age_years.isna()
print(f"75+ share of 2024 visits: {e(o75,2024)/e(allm,2024):.1%} (1 in {e(allm,2024)/e(o75,2024):.1f}); rows {int((o75&(df.year==2024)).sum()):,} of {int((df.year==2024).sum()):,} = 1 in {(df.year==2024).sum()/(o75&(df.year==2024)).sum():.1f}")
print(f"65+ share of 2024 visits: {e(o65,2024)/e(allm,2024):.1%}")
print(f"75+ share of ALL 2024 admissions: {a(o75,2024)/a(allm,2024):.1%} ({a(o75,2024):,.0f} of {a(allm,2024):,.0f})")
print(f"65+ share of ALL 2024 admissions: {a(o65,2024)/a(allm,2024):.1%}")
fp = df['product'].isin(FALL)
print(f"75+ share of admissions from home-fall PRODUCTS (all ages): {a(o75&fp,2024)/a(fp,2024):.1%} ({a(o75&fp,2024):,.0f} of {a(fp,2024):,.0f})")
home = df.location.eq('Home')
print(f"75+ share of admissions from home-fall products with location=Home: {a(o75&fp&home,2024)/a(fp&home,2024):.1%}")
print(f"75+ home-fall-product admissions {a(o75&fp,2024):,.0f} = {a(o75&fp,2024)/a(allm,2024):.1%} of ALL admissions")
eb = df.narrative.fillna('').str.contains(EB, regex=True) | df['product'].eq('Electric power-assisted pedal bicycles')
ebadm = a(eb, 2024); print(f"e-bike admissions 2024 (narrative or code): {ebadm:,.0f}")
print(f"75+ ALL admissions / e-bike admissions = {a(o75,2024)/ebadm:.0f}x")
print(f"75+ home-fall-product admissions / e-bike = {a(o75&fp,2024)/ebadm:.0f}x")
print(f"65+ home-fall-product admissions / e-bike = {a(o65&fp,2024)/ebadm:.0f}x")
print(f"65+ all admissions / e-bike = {a(o65,2024)/ebadm:.0f}x")
ebm = df['product'].isin(['Electric power-assisted pedal bicycles','Power-assisted cycles, not elsewhere classified']) | eb
print(f"(Marcus union def) e-bike admissions {a(ebm,2024):,.0f}; 75+ all adm / that = {a(o75,2024)/a(ebm,2024):.0f}x; 75+ home-fall / that = {a(o75&fp,2024)/a(ebm,2024):.0f}x")
