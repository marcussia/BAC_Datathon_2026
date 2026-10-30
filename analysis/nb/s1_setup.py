"""Section 1: imports, Colab detection, data load, helper functions pasted from helpers.py."""
import os, re
from nb import md, code

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

IMPORTS = '''# Colab has pandas, numpy, matplotlib, seaborn, scikit-learn preinstalled. Install only what's missing.
import sys, subprocess
for pkg, mod in [("pandas", "pandas"), ("numpy", "numpy"), ("matplotlib", "matplotlib"), ("scikit-learn", "sklearn")]:
    try:
        __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
IN_COLAB = "google.colab" in sys.modules
print("running in Colab" if IN_COLAB else "running locally")'''

LOAD = '''# Where the CSVs live. In Colab: a Drive folder (edit DATA_DIR). Locally: ../data next to this notebook.
DATA_DIR = "/content/drive/MyDrive/bac-datathon/data"   # <-- Colab: change to your Drive folder
FILE = "neiss_all_years.csv"
import os
if IN_COLAB:
    try:
        from google.colab import drive
        drive.mount("/content/drive")
        assert os.path.exists(os.path.join(DATA_DIR, FILE)), f"{FILE} not found in {DATA_DIR}"
    except Exception as e:                       # mount refused or file missing -> upload instead
        print("Drive not available:", e, "\\nUpload", FILE, "now:")
        from google.colab import files
        up = files.upload()
        DATA_DIR = "."
        assert FILE in up, f"expected {FILE}"
else:
    DATA_DIR = os.path.join("..", "data") if os.path.exists(os.path.join("..", "data", FILE)) else "data"
os.makedirs("charts", exist_ok=True)              # save_chart() writes here (deck pulls from it)
DATA_PATH = os.path.join(DATA_DIR, FILE)
print("data:", DATA_PATH)'''

CLEAN = '''raw = load(DATA_PATH)
df = clean(raw)
# Trap 2: decode age. 0 = unknown, 201-223 = months (1-23), else years.
a = df["age"]
df["age_unknown"] = a.eq(0)
df["is_infant_months"] = a.between(201, 223)
df["age_years"] = np.where(df.age_unknown, np.nan, np.where(df.is_infant_months, (a - 200) / 12, a))
df["age_group"] = pd.cut(df.age_years, [-0.01, 4, 14, 24, 44, 64, 74, 200],
                         labels=["0-4", "5-14", "15-24", "25-44", "45-64", "65-74", "75+"])
df["over65"] = df.age_years >= 65
df["over75"] = df.age_years >= 75
df["admitted"] = df.outcome.eq("Admitted to hospital").astype(int)
df["died"] = df.outcome.eq("Died").astype(int)
# a "fall" = the nurse's note says FELL / FALL / SLIP / TRIP (NEISS has no mechanism column)
df["fall"] = df.narrative.fillna("").str.contains(r"\\bF[AE]LL|\\bSLIP|\\bTRIP", regex=True)
# products that are the furniture/building/bathroom hazards behind most falls at home
FALL_GROUPS = ["Floors, stairs & building parts", "Furniture", "Bathroom"]
df["fall_product"] = df.product_group.isin(FALL_GROUPS)

EST = df.groupby("year").weight.sum()             # national estimate per year: the denominator everywhere
YEARS = sorted(df.year.unique())

def wrate(d, flag):
    """Weighted rate of a 0/1 column = share of the national estimate."""
    return float(np.average(d[flag], weights=d.weight)) if len(d) else float("nan")

SLIDES = []                                       # every number that goes on a slide is logged here
def SLIDE(n, label, value):
    SLIDES.append({"slide": n, "label": label, "value": value})
    print(f"SLIDE {n}: {label} = {value}")

pd.set_option("display.width", 200); pd.set_option("display.max_columns", 40)
print(f"rows {len(df):,} | national estimate {df.weight.sum():,.0f} | years {YEARS}")
print("est by year:", {int(k): f"{v / 1e6:.2f}M" for k, v in EST.items()})'''


def helpers_source():
    """helpers.py with the notebook-incompatible lines swapped. Asserts guard against silent drift."""
    src = open(os.path.join(ROOT, "helpers.py")).read()
    src = re.sub(r'^""".*?"""\n', "", src, count=1, flags=re.S)            # module docstring
    swaps = [('matplotlib.use("Agg")  # save charts to files without needing a display\n', ""),
             ('CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")', 'CHART_DIR = os.path.join(os.getcwd(), "charts")'),
             ("    plt.close(fig)\n", "    plt.show()\n")]                   # display inline after saving
    for old, new in swaps:
        assert old in src, f"helpers.py changed; update s1_setup.py swap: {old[:40]!r}"
        src = src.replace(old, new)
    return "# ---- helpers.py, pasted so the notebook is self-contained (source of truth: helpers.py in the repo) ----\n" + src


def cells():
    return [
        md("## 1. Setup and data load\nImports, Colab detection, data load and the helper functions. Run this section first; everything below depends on `df`, `EST` and the helpers."),
        md("Check that the libraries Colab ships with are present; install only what is missing."),
        code(IMPORTS),
        md("Load the data. In Colab we mount Google Drive and read `DATA_DIR/neiss_all_years.csv`; if the mount fails you get an upload prompt. Locally it reads `../data/`."),
        code(LOAD),
        md("Helper functions (`load`, `clean`, `by`, `rate`, `trend`, `top`, `crosstab`, `model`, `drivers`, `gains`, `segments`, `save_chart`). Pasted from `helpers.py` so the notebook runs on its own. Charts display inline and are saved to `charts/`."),
        code(helpers_source()),
        md("Load and clean. Decodes the age code (trap 2), adds `admitted`/`died` from `outcome`, a `fall` flag from the narrative, and `EST` = national estimate per year (SUM of weight), the denominator used everywhere. `SLIDE()` logs every number that goes on a slide."),
        code(CLEAN),
    ]
