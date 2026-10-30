"""BAC Datathon helpers. Import with:  from helpers import *

Loading/cleaning:  df = clean(load("data/file.csv"))
Profiling:         profile(df)
Slicing:           by(df, "region", "revenue"), rate(df, "plan", "churn"),
                   trend(df, "order_date", "revenue", "M"), top(df, "product", "revenue")
Modelling:         res = model(df, target="churn", id_cols=["customer_id"])
                   drivers(res), gains(res)
Every chart saves to charts/<name>.png at 200 dpi, sized for slides.
Works on pandas 2.x and 3.x.
"""
import os
import re
import warnings

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # save charts to files without needing a display
import matplotlib.pyplot as plt
from pandas.api.types import (is_bool_dtype, is_datetime64_any_dtype,
                              is_numeric_dtype, is_object_dtype, is_string_dtype)

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 60)
pd.set_option("display.width", 200)

CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHART_DIR, exist_ok=True)
ACCENT, GREY, ORANGE = "#2563eb", "#cbd5e1", "#f97316"
plt.rcParams.update({
    "figure.figsize": (10, 5.6), "figure.dpi": 110, "savefig.dpi": 200,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 16, "axes.titleweight": "bold", "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.frameon": False,
    "axes.prop_cycle": matplotlib.cycler(color=[ACCENT, ORANGE, "#10b981", "#8b5cf6", "#ef4444", "#64748b"]),
})


# ---------- utilities ----------
def snake(c):
    c = re.sub(r"[^0-9a-zA-Z]+", "_", str(c).strip()).strip("_").lower()
    return c or "col"


def is_text(s):
    return (is_object_dtype(s) or is_string_dtype(s)) and not is_numeric_dtype(s)


def text_cols(d):
    return [c for c in d.columns if is_text(d[c]) or isinstance(d[c].dtype, pd.CategoricalDtype) or is_bool_dtype(d[c])]


def save_chart(name, title=None):
    """Save the current figure to charts/<name>.png and close it. Returns the path."""
    fig = plt.gcf()
    if title:
        fig.axes[0].set_title(title)
    fig.tight_layout()
    path = os.path.join(CHART_DIR, re.sub(r"[^a-z0-9_]+", "_", name.lower()) + ".png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("chart saved ->", path)
    return path


# ---------- load + clean ----------
def load(path, sheet=0):
    """Read csv/xlsx/json/parquet with snake_case columns. sheet=None returns a dict of all sheets."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls", ".xlsm"):
        out = pd.read_excel(path, sheet_name=sheet)
    elif ext == ".json":
        out = pd.read_json(path)
    elif ext == ".parquet":
        out = pd.read_parquet(path)
    else:
        try:
            out = pd.read_csv(path)
        except UnicodeDecodeError:
            out = pd.read_csv(path, encoding="latin-1")
    fix = lambda d: d.rename(columns=snake)
    return {k: fix(v) for k, v in out.items()} if isinstance(out, dict) else fix(out)


def profile(d):
    """One row per column: dtype, % missing, # unique, example value."""
    print(f"{len(d):,} rows x {d.shape[1]} cols | duplicate rows: {d.duplicated().sum():,}")
    return pd.DataFrame({
        "dtype": d.dtypes.astype(str),
        "missing_%": (d.isna().mean() * 100).round(1),
        "n_unique": d.nunique(),
        "example": [d[c].dropna().iloc[0] if d[c].notna().any() else None for c in d.columns],
    }).sort_values("missing_%", ascending=False)


def clean(d, verbose=True):
    """Drop duplicates, '$1,200'->1200, parse dates, Yes/No->1/0, add year/month/dow for dates. Prints a log."""
    d = d.copy()
    log, n0 = [], len(d)
    d = d.drop_duplicates()
    if len(d) < n0:
        log.append(f"dropped {n0 - len(d):,} duplicate rows")
    money = r"[$,%\s]|SGD|S\$"
    for c in d.columns:
        s = d[c]
        if not is_text(s):
            continue
        s = s.astype(object)
        d[c] = s.where(s.isna(), s.astype(str).str.strip()).replace(
            {"": np.nan, "nan": np.nan, "NaN": np.nan, "None": np.nan, "NA": np.nan, "N/A": np.nan, "-": np.nan})
        s = d[c]
        stripped = s.dropna().astype(str).str.replace(money, "", regex=True)
        if len(stripped) and pd.to_numeric(stripped, errors="coerce").notna().mean() > 0.95:
            d[c] = pd.to_numeric(s.astype(str).str.replace(money, "", regex=True), errors="coerce")
            log.append(f"{c}: text -> number")
            continue
        looks_date = s.dropna().astype(str).str.match(r"^\d{4}-\d{2}-\d{2}|^\d{1,2}/\d{1,2}/\d{2,4}").mean() > 0.9
        if re.search(r"date|time|_at$|_on$|month|period", c) or looks_date:
            dt = pd.to_datetime(s, errors="coerce")
            if dt.notna().mean() > 0.9 * s.notna().mean():
                d[c] = dt
                log.append(f"{c}: text -> datetime")
                continue
        low = s.dropna().astype(str).str.lower()
        yn = {"yes": 1, "y": 1, "true": 1, "t": 1, "1": 1, "no": 0, "n": 0, "false": 0, "f": 0, "0": 0}
        if low.nunique() == 2 and set(low.unique()) <= set(yn):
            d[c] = s.astype(str).str.lower().map(yn)
            log.append(f"{c}: yes/no -> 1/0")
    for c in [c for c in d.columns if is_datetime64_any_dtype(d[c])]:
        d[f"{c}_year"], d[f"{c}_month"], d[f"{c}_dow"] = d[c].dt.year, d[c].dt.month, d[c].dt.dayofweek
        log.append(f"{c}: added _year/_month/_dow")
    if verbose:
        print("\n".join(log) if log else "nothing needed fixing")
    return d


# ---------- slicing (the numbers that go on slides) ----------
def by(d, group, metric=None):
    """Per-group total/mean/median/count and share of total. metric=None gives counts and shares."""
    if metric is None:
        out = d[group].value_counts(dropna=False).to_frame("count")
        out["share_%"] = (out["count"] / out["count"].sum() * 100).round(1)
        return out
    g = d.groupby(group, dropna=False)[metric]
    out = pd.DataFrame({"total": g.sum(), "mean": g.mean(), "median": g.median(), "count": g.size()})
    out["share_of_total_%"] = (out["total"] / out["total"].sum() * 100).round(1)
    return out.sort_values("total", ascending=False)


def rate(d, group, flag, min_n=20, chart=True, name=None):
    """Rate of a 0/1 outcome per group vs overall, with lift. Saves a bar chart (above-average bars highlighted)."""
    overall = d[flag].mean()
    g = d.groupby(group, dropna=False)[flag].agg(rate="mean", n="size")
    g = g[g["n"] >= min_n].sort_values("rate", ascending=False)
    g["lift_vs_avg"] = (g["rate"] / overall).round(2)
    if chart and len(g):
        h = g.head(15).iloc[::-1]
        ax = (h["rate"] * 100).plot.barh(color=[ACCENT if r > overall else GREY for r in h["rate"]])
        ax.axvline(overall * 100, ls="--", c="black", lw=1)
        ax.text(overall * 100, ax.get_ylim()[1], f" avg {overall:.1%}", fontsize=11, va="bottom")
        ax.set_xlabel(f"{flag} rate (%)"); ax.set_ylabel("")
        ax.set_title(f"{flag} rate by {group}")
        save_chart(name or f"rate_{flag}_by_{group}")
    print(f"overall {flag} rate: {overall:.1%}")
    return g


def trend(d, date_col, metric=None, freq="M", agg="sum", name=None):
    """Resample over time (D/W/M/Q/Y), save a line chart, print first->last change and peak."""
    s = d.set_index(date_col).sort_index()
    src = s[metric] if metric else s
    try:
        r = src.resample(freq)
    except ValueError:
        r = src.resample(freq + "E")  # pandas 3 wants ME/QE/YE
    s = r.agg(agg) if metric else r.size()
    ax = s.plot(marker="o", lw=2.2, color=ACCENT)
    ax.set_title(f"{metric or 'count'} ({agg}) per {freq}"); ax.set_xlabel("")
    save_chart(name or f"trend_{metric or 'count'}_{freq}")
    if len(s) > 1 and s.iloc[0]:
        print(f"first {s.iloc[0]:,.2f} -> last {s.iloc[-1]:,.2f} ({(s.iloc[-1] / s.iloc[0] - 1) * 100:+.1f}%) | "
              f"peak {s.idxmax():%Y-%m-%d} at {s.max():,.2f}")
    return s


def top(d, group, metric=None, n=10, agg="sum", name=None):
    """Top-N groups as a horizontal bar chart; prints how concentrated the total is."""
    s = (d.groupby(group)[metric].agg(agg) if metric else d[group].value_counts()).sort_values(ascending=False)
    head = s.head(n)
    ax = head.iloc[::-1].plot.barh(color=ACCENT)
    ax.set_title(f"Top {min(n, len(s))} {group} by {metric or 'count'}"); ax.set_ylabel("")
    save_chart(name or f"top_{group}_{metric or 'count'}")
    if agg == "sum" or metric is None:
        print(f"top {len(head)} of {len(s)} {group} = {head.sum() / s.sum():.1%} of total")
    return head


def crosstab(d, row, col, flag=None):
    """Two-way table: counts (flag=None) or the mean of a 0/1/numeric column per cell."""
    if flag is None:
        return pd.crosstab(d[row], d[col], margins=True)
    return d.pivot_table(index=row, columns=col, values=flag, aggfunc="mean", margins=True).round(3)


# ---------- modelling ----------
def model(d, target, id_cols=(), drop_cols=(), test_size=0.2, seed=42):
    """Baseline vs logistic/ridge, random forest, gradient boosting. Returns a dict for drivers()/gains()."""
    from sklearn.compose import ColumnTransformer
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.ensemble import (HistGradientBoostingClassifier, HistGradientBoostingRegressor,
                                  RandomForestClassifier, RandomForestRegressor)
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn import metrics as M

    data = d.dropna(subset=[target]).copy()
    y = data[target]
    is_clf = is_text(y) or y.nunique() <= 10
    if is_clf and not is_numeric_dtype(y):
        y = y.astype("category").cat.codes
    excl = set(id_cols) | set(drop_cols) | {target} | {c for c in data.columns if is_datetime64_any_dtype(data[c])}
    num = [c for c in data.select_dtypes(include="number").columns if c not in excl]
    cat = [c for c in text_cols(data) if c not in excl and data[c].nunique() <= 50]
    X = data[num + cat]
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False, min_frequency=10)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("ohe", ohe)]), cat),
    ])
    strat = y if is_clf and y.value_counts().min() >= 2 else None
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, random_state=seed, stratify=strat)
    binary = is_clf and y.nunique() == 2
    if is_clf:
        models = {"Baseline (always majority)": DummyClassifier(strategy="most_frequent"),
                  "Logistic regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
                  "Random forest": RandomForestClassifier(300, min_samples_leaf=3, class_weight="balanced", n_jobs=-1, random_state=seed),
                  "Gradient boosting": HistGradientBoostingClassifier(random_state=seed)}
    else:
        models = {"Baseline (always mean)": DummyRegressor(), "Ridge regression": Ridge(),
                  "Random forest": RandomForestRegressor(300, min_samples_leaf=3, n_jobs=-1, random_state=seed),
                  "Gradient boosting": HistGradientBoostingRegressor(random_state=seed)}
    rows, fitted = [], {}
    avg = "binary" if binary else "macro"
    for name, m in models.items():
        p_ = Pipeline([("pre", pre), ("model", m)]).fit(X_tr, y_tr)
        fitted[name] = p_
        p = p_.predict(X_te)
        if is_clf:
            r = {"model": name, "accuracy": M.accuracy_score(y_te, p),
                 "precision": M.precision_score(y_te, p, average=avg, zero_division=0),
                 "recall": M.recall_score(y_te, p, average=avg, zero_division=0),
                 "f1": M.f1_score(y_te, p, average=avg, zero_division=0)}
            if binary:
                r["roc_auc"] = M.roc_auc_score(y_te, p_.predict_proba(X_te)[:, 1])
        else:
            r = {"model": name, "MAE": M.mean_absolute_error(y_te, p),
                 "RMSE": float(np.sqrt(M.mean_squared_error(y_te, p))), "R2": M.r2_score(y_te, p)}
        rows.append(r)
    key = ("roc_auc" if binary else "f1") if is_clf else "R2"
    table = pd.DataFrame(rows).set_index("model").sort_values(key, ascending=False).round(3)
    best = next(n for n in table.index if not n.startswith("Baseline"))
    base = next(n for n in table.index if n.startswith("Baseline"))
    print(table.to_string())
    print(f"\nbest: {best} | {key} {table.loc[best, key]:.3f} vs baseline {table.loc[base, key]:.3f} | "
          f"{len(num)} numeric + {len(cat)} categorical features | test rows {len(X_te):,}")
    return {"table": table, "best": best, "pipe": fitted[best], "fitted": fitted, "X_te": X_te, "y_te": y_te,
            "is_clf": is_clf, "binary": binary, "key": key, "data": data, "target": target, "num": num}


def drivers(res, n=10, seed=42):
    """Permutation importance on original column names + quartile direction check. Saves top_drivers.png."""
    from sklearn.inspection import permutation_importance
    scoring = ("roc_auc" if res["binary"] else "f1_macro") if res["is_clf"] else "r2"
    pi = permutation_importance(res["pipe"], res["X_te"], res["y_te"], n_repeats=5, random_state=seed,
                                scoring=scoring, n_jobs=-1)
    imp = pd.Series(pi.importances_mean, index=res["X_te"].columns).sort_values(ascending=False)
    ax = imp.head(n).iloc[::-1].plot.barh(color=ACCENT)
    ax.set_title(f"Top drivers of {res['target']}"); ax.set_xlabel(f"drop in {scoring} when shuffled")
    save_chart("top_drivers")
    data, t = res["data"], res["target"]
    if is_numeric_dtype(data[t]):
        for c in [c for c in imp.head(5).index if c in res["num"]]:
            q = pd.qcut(data[c].rank(method="first"), 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])
            print(f"{c}: mean {t} by quartile -> {data.groupby(q, observed=True)[t].mean().round(3).to_dict()}")
    return imp.head(15).round(4)


def gains(res):
    """Decile lift table + gains chart for binary targets. Prints a slide-ready headline."""
    if not res["binary"]:
        print("gains() only applies to yes/no targets")
        return None
    proba = res["pipe"].predict_proba(res["X_te"])[:, 1]
    t = pd.DataFrame({"y": np.asarray(res["y_te"]), "p": proba}).sort_values("p", ascending=False).reset_index(drop=True)
    t["decile"] = (np.arange(len(t)) * 10 // len(t)) + 1
    lift = t.groupby("decile").agg(n=("y", "size"), positives=("y", "sum"), rate=("y", "mean"))
    lift["cum_%_caught"] = (lift["positives"].cumsum() / lift["positives"].sum() * 100).round(1)
    lift["lift"] = (lift["rate"] / t["y"].mean()).round(2)
    x = np.arange(0, 11) * 10
    plt.plot(x, np.r_[0, lift["cum_%_caught"].values], marker="o", lw=2.2, color=ACCENT, label="model")
    plt.plot([0, 100], [0, 100], "--", c="grey", label="random")
    plt.xlabel("% of population targeted (highest risk first)"); plt.ylabel("% of positives caught")
    plt.legend(); plt.title("Gains chart")
    save_chart("gains_chart")
    print(f"HEADLINE: targeting the top 20% catches {lift['cum_%_caught'].iloc[1]:.0f}% of positives "
          f"({lift['cum_%_caught'].iloc[1] / 20:.1f}x random)")
    return lift


def segments(d, cols, k=None, seed=42):
    """K-means on scaled cols (k picked by silhouette if None). Adds d['segment'] and returns a profile table."""
    from sklearn.cluster import KMeans
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler
    Z = StandardScaler().fit_transform(SimpleImputer(strategy="median").fit_transform(d[cols]))
    if k is None:
        idx = np.random.RandomState(seed).choice(len(Z), min(len(Z), 5000), replace=False)
        scores = {kk: silhouette_score(Z[idx], KMeans(kk, n_init=10, random_state=seed).fit_predict(Z[idx])) for kk in range(2, 7)}
        k = max(scores, key=scores.get)
        print("silhouette:", {a: round(b, 3) for a, b in scores.items()}, "-> k =", k)
    d["segment"] = KMeans(k, n_init=10, random_state=seed).fit_predict(Z)
    prof = d.groupby("segment")[cols].mean().round(2)
    prof.insert(0, "size_%", (d["segment"].value_counts(normalize=True).sort_index() * 100).round(1))
    return prof
