"""Section 3: fact-check claim 1, 'product injuries surged 18% in 2024'. Owner: Marcus."""
from nb import md, code

C1 = '''y = df.groupby("year").agg(rows=("case_id", "size"), est=("weight", "sum"), mean_weight=("weight", "mean"))
y["rows_chg_%"] = y.rows.pct_change() * 100
y["est_chg_%"] = y.est.pct_change() * 100
y["mean_weight_chg_%"] = y.mean_weight.pct_change() * 100
print(y.round(1).to_string())
g_rows, g_w, g_est = y.rows[2024] / y.rows[2023], y.mean_weight[2024] / y.mean_weight[2023], y.est[2024] / y.est[2023]
print(f"\\n2023 -> 2024 decomposition: est growth {g_est:.3f} = rows growth {g_rows:.3f} x mean-weight growth {g_w:.3f}  (check: {g_rows * g_w:.3f})")
print(f"2014 -> 2024 (10 years): est {y.est[2024] / y.est[2014] - 1:+.1%}, rows {y.rows[2024] / y.rows[2014] - 1:+.1%}")
print(f"2005 -> 2024 (19 years): est {y.est[2024] / y.est[2005] - 1:+.1%}, rows {y.rows[2024] / y.rows[2005] - 1:+.1%}")
SLIDE(1, "claim 1: est growth 2023->2024 (%)", f"{(g_est - 1) * 100:+.1f}")
SLIDE(1, "claim 1: rows growth 2023->2024 (%)", f"{(g_rows - 1) * 100:+.1f}")
SLIDE(2, "mean weight 2023 -> 2024", f"{y.mean_weight[2023]:.1f} -> {y.mean_weight[2024]:.1f} ({(g_w - 1) * 100:+.1f}%)")
SLIDE(2, "est growth 2014->2024 (%)", f"{(y.est[2024] / y.est[2014] - 1) * 100:+.1f}")'''

C1B = '''# Where did the weight change come from? Rows and weights moved in opposite directions inside hospital types.
h = df[df.year >= 2023].groupby(["hospital_type", "year"]).agg(rows=("case_id", "size"), est=("weight", "sum"), mean_w=("weight", "mean")).unstack("year")
out = pd.DataFrame({"rows_chg_%": (h["rows"][2024] / h["rows"][2023] - 1) * 100,
                    "mean_w_chg_%": (h["mean_w"][2024] / h["mean_w"][2023] - 1) * 100,
                    "est_chg_%": (h["est"][2024] / h["est"][2023] - 1) * 100})
print(out.round(1).to_string())
cf = (h["rows"][2024] * h["mean_w"][2023]).sum()        # 2024 rows at each hospital type's 2023 mean weight
cf_g = (cf / y.est[2023] - 1) * 100
print(f"\\n2024 estimate if each hospital type kept its 2023 mean weight: {cf / 1e6:.2f}M = {cf_g:+.1f}% (actual {(g_est - 1) * 100:+.1f}%)")
SLIDE(2, "est growth 2023->2024 holding 2023 weights (%)", f"{cf_g:+.1f}")'''

CH = '''fig, ax = plt.subplots()
x = np.arange(2); lab = ["2023", "2024"]
ax.bar(x - 0.2, y.rows[[2023, 2024]] / 1e3, 0.4, color=GREY, label="rows sampled (thousands)")
ax.bar(x + 0.2, y.est[[2023, 2024]] / 1e5, 0.4, color=ACCENT, label="national estimate (100k)")
for i, yr in enumerate([2023, 2024]):
    ax.text(i - 0.2, y.rows[yr] / 1e3 + 1.5, f"{y.rows[yr] / 1e3:.1f}k", ha="center")
    ax.text(i + 0.2, y.est[yr] / 1e5 + 1.5, f"{y.est[yr] / 1e6:.2f}M", ha="center")
ax.set_xticks(x, lab); ax.set_ylim(0, 180); ax.legend(loc="upper left")
save_chart("c1_surge_rows_vs_weight", f"The '18% surge' is {(g_est - 1) * 100:+.0f}% by weight but {(g_rows - 1) * 100:+.0f}% by ER visits sampled\\nn = {y.rows[2023]:,} rows (2023), {y.rows[2024]:,} rows (2024)")'''

CH2 = '''ax = (y.est / 1e6).plot.bar(color=[GREY, GREY, GREY, ACCENT], rot=0)
for i, v in enumerate(y.est / 1e6): ax.text(i, v + 0.2, f"{v:.2f}M", ha="center")
ax.set_ylabel("national estimate (millions of ER visits)"); ax.set_xlabel(""); ax.set_ylim(0, 17)
save_chart("c1_est_by_year", f"2024 is {(y.est[2024] / y.est[2014] - 1) * 100:+.0f}% vs 2014: the 'surge' is mostly a rebound from a low 2023\\nn = {len(df):,} rows, 4 years")'''

TAKE = """> **Takeaway (claim 1: "surged 18%").** *Partly holds.* The weighted estimate did rise 18.3% (12.74M → 15.07M), but only 6.9% more ER visits were sampled; the rest is the mean weight rising 10.6% (188 → 208), i.e. the sampling frame. Holding 2023 weights, 2024 is +11.6%. 2023 was itself a low year (−8% vs 2014); 2024 vs 2014 is +8.9% over ten years. **So what:** the right description is "single-digit underlying growth, inflated by reweighting and a low base". **Confidence: medium.** We can't fully separate a CPSC weight update from real change without their methodology notes."""


def cells():
    return [
        md("## 3. Fact-check claim 1: \"Product injuries surged 18% in 2024\"  \n*Rubric: factuality.* Rows vs weighted growth, the weight change, and 2024 in 20-year context."),
        md("Growth by year, by rows and by national estimate. Why it matters: the 18% is a weighted number; if rows grew far less, part of the surge is the survey, not the injuries."),
        code(C1),
        md("Weight change by hospital type, and the counterfactual: what would 2024 look like at 2023 weights? Why it matters: it bounds how much of the 18% is real."),
        code(C1B),
        md("Chart for slide 2: rows vs weight, 2023 vs 2024."),
        code(CH),
        md("Chart: 2024 in context of all four years."),
        code(CH2),
        md(TAKE),
    ]
