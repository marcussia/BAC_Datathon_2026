"""Section 4: fact-check claim 2, 'e-bike injuries nearly quadrupled'. Owner: Marcus."""
from nb import md, code

PROD = '''# Definition (a): product codes. The e-bike code exists only in 2024; the 2023 code that held e-bikes has 0 rows in 2024.
P_EBIKE = "Electric power-assisted pedal bicycles"
P_NEC = "Power-assisted cycles, not elsewhere classified"
P_MOPED = "Mopeds or power-assisted cycles"
fam = df["product"].isin([P_EBIKE, P_NEC, P_MOPED])
t = df[fam].pivot_table(index="product", columns="year", values="weight", aggfunc=["size", "sum"]).fillna(0)
t.columns = [f"{'rows' if a == 'size' else 'est'}_{b}" for a, b in t.columns]
print(t.round(0).astype(int).to_string())
e24 = df[(df["product"] == P_EBIKE) & (df.year == 2024)]
print(f"\\n'{P_EBIKE}': 2024 only, {len(e24)} rows, {e24.weight.sum():,.0f} est. Compared with 0 in 2023 any growth multiple is possible: this is the '4x'.")
SLIDE(2, "e-bike product code 2024 (rows / est)", f"{len(e24)} / {e24.weight.sum():,.0f}; 0 rows in 2023")
SLIDE(2, "'Mopeds or power-assisted cycles' est 2023 -> 2024", f"{df[(df['product'] == P_MOPED) & (df.year == 2023)].weight.sum():,.0f} -> 0")'''

NARR = '''# Definition (b): the narrative. First the trap: "E BIKE" without a word boundary matches "THE BIKE" and "EXERCISE BIKE".
N = df.narrative.fillna("")
naive = N.str.contains(r"E-BIKE|EBIKE|E BIKE|ELECTRIC BIK", regex=True)
strict = N.str.contains(r"\\bE-?BIKE|\\bE BIKE|ELECTRIC BI(KE|CYCLE)|ELEC\\.? BI(KE|CYCLE)|ELECTRIC PEDAL|PEDAL ASSIST|POWER ASSIST|MOTORI[ZS]ED BI(KE|CYCLE)|\\bE-?BICYCLE", regex=True)
print("rows matched by year:\\n", pd.DataFrame({"naive regex": naive.groupby(df.year).sum(), "strict regex": strict.groupby(df.year).sum()}).T.to_string())
fp = df[naive & ~strict & (df.year == 2024)].narrative
print(f"\\nwhat the naive regex catches that the strict one doesn't (2024, {len(fp)} rows), e.g.:")
for s in fp.sample(5, random_state=1): print("  -", s[:100])
df["ebike_narr"] = strict
print("\\nstrict matches read as e-bikes, e.g.:")
for s in df[strict & (df.year == 2023)].narrative.sample(5, random_state=3): print("  -", s[:100])'''

CODED = '''# What were narrative e-bike rows coded as? 2023: the moped code. 2024: the new e-bike code. Same injuries, new label.
m = df.ebike_narr & (df.year >= 2023)
print(pd.crosstab(df.loc[m, "product"], df.loc[m, "year"]).sort_values(2024, ascending=False).head(6).to_string())'''

THREE = '''# Three like-for-like definitions, 2023 vs 2024.
df["ebike_code"] = df["product"].isin([P_EBIKE, P_NEC, P_MOPED])          # product family across the rename
df["ebike"] = df.ebike_narr | df["product"].isin([P_EBIKE, P_NEC, P_MOPED])  # union: used from here on
defs = {"(a) 2024 e-bike code only": df["product"] == P_EBIKE,
        "(b) narrative, strict regex": df.ebike_narr,
        "(c) product family (moped code -> e-bike + NEC codes)": df.ebike_code,
        "(d) narrative OR product family [used below]": df.ebike}
rows = []
for k, m in defs.items():
    d = df[m & (df.year >= 2023)].groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum")).reindex([2023, 2024]).fillna(0)
    rows.append({"definition": k, "rows_2023": int(d.rows[2023]), "rows_2024": int(d.rows[2024]), "est_2023": d.est[2023], "est_2024": d.est[2024],
                 "growth_x": d.est[2024] / d.est[2023] if d.est[2023] else float("inf"), "share_of_2024_%": d.est[2024] / EST[2024] * 100})
cmp = pd.DataFrame(rows).set_index("definition"); print(cmp.round(2).to_string())
gb, gd = cmp.loc["(b) narrative, strict regex", "growth_x"], cmp.loc["(d) narrative OR product family [used below]", "growth_x"]
SLIDE(1, "claim 2: e-bike growth 2023->2024, narrative definition (x)", f"{gb:.2f}")
SLIDE(1, "claim 2: e-bike growth 2023->2024, narrative OR product family (x)", f"{gd:.2f}")
SLIDE(2, "e-bikes share of all 2024 visits (%)", f"{cmp.loc['(d) narrative OR product family [used below]', 'share_of_2024_%']:.1f}")'''

CH = '''fig, ax = plt.subplots()
k = cmp.index[:3]; x = np.arange(3)
ax.bar(x - 0.2, cmp.loc[k, "est_2023"] / 1e3, 0.4, color=GREY, label="2023")
ax.bar(x + 0.2, cmp.loc[k, "est_2024"] / 1e3, 0.4, color=ACCENT, label="2024")
for i, d in enumerate(k):
    ax.text(i - 0.2, cmp.loc[d, "est_2023"] / 1e3 + 2, f"{cmp.loc[d, 'est_2023'] / 1e3:.0f}k", ha="center")
    ax.text(i + 0.2, cmp.loc[d, "est_2024"] / 1e3 + 2, f"{cmp.loc[d, 'est_2024'] / 1e3:.0f}k", ha="center")
ax.set_xticks(x, ["2024 code only\\n(the headline's method)", "narrative\\n(strict regex)", "product family\\n(across the rename)"])
ax.set_ylabel("national estimate (thousands of ER visits)"); ax.legend(); ax.set_ylim(0, cmp.est_2024.max() / 1e3 * 1.2)
save_chart("c2_ebike_three_definitions", f"E-bike visits grew {min(gb, gd):.1f}-{max(gb, gd):.1f}x, not 4x: the 2024 code is a rename of the 2023 moped code\\nn = {int(cmp.rows_2023.iloc[-1])} rows (2023), {int(cmp.rows_2024.iloc[-1])} rows (2024), definition (d)")'''

CAVEAT = '''# Caveat for any older-year narrative comparison: notes were capped at 142 characters before 2019 (400 after).
print(df.assign(L=df.narrative.str.len()).groupby("year").L.agg(["mean", "max"]).round(0).to_string())
print("-> 2023 vs 2024 is a fair narrative comparison (same cap). 2005/2014 vs 2024 is not.")'''

TAKE = """> **Takeaway (claim 2: "nearly quadrupled").** *Does not hold.* The "4x" compares a product code that only exists in 2024 (243 rows, 56k) with a 2023 in which the same injuries sat under "Mopeds or power-assisted cycles" (81k est, 0 rows in 2024). Like-for-like, e-bike ER visits grew 1.2x (product family) to 1.6x (strict narrative), to about 0.7% of all 2024 visits. A naive text search ("E BIKE" matching "THE BIKE") would have given a higher multiple on inflated counts. **So what:** real growth, small base, and the headline's multiple is a recoding artefact. **Confidence: high** on the recoding; medium on the exact multiple (the moped code mixes petrol mopeds and e-bikes)."""


def cells():
    return [
        md("## 4. Fact-check claim 2: \"E-bike injuries nearly quadrupled in a year\"  \n*Rubric: factuality.* Two ways to define an e-bike (product code, narrative), what the 2023 rows were coded as, and the like-for-like growth."),
        md("Definition (a), product codes by year. Why it matters: the e-bike code appears from nowhere in 2024 while the moped code vanishes, the trap-4 signature."),
        code(PROD),
        md("Definition (b), the narrative, with the regex trap shown. Why it matters: a careless text search inflates both years and the multiple."),
        code(NARR),
        md("What product code the narrative e-bike rows carry in each year. Why it matters: it proves the rename explains the jump."),
        code(CODED),
        md("Three definitions side by side. Why it matters: the verdict should not depend on which one we pick, and it doesn't."),
        code(THREE),
        md("Chart for slide 2."),
        code(CH),
        md("Narrative-length caveat. Why it matters: it bounds which years can be compared by text search."),
        code(CAVEAT),
        md(TAKE),
    ]
