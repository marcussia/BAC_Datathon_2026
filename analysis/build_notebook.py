"""Build analysis/bac_round2.ipynb from the section modules in analysis/nb/.

Run:   python analysis/build_notebook.py            # writes the .ipynb
       python analysis/build_notebook.py --test     # also executes it top-to-bottom with nbclient (local mode)

Each section lives in its own file (analysis/nb/s<N>_*.py) and exposes cells() -> list of nbformat cells,
so two people can edit different sections on different branches without notebook JSON conflicts.
"""
import os, sys, importlib
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "bac_round2.ipynb")
sys.path.insert(0, HERE)

SECTIONS = [  # order = notebook order; one module per section, owner in comment
    "nb.s0_title",         # both (filled last)
    "nb.s1_setup",         # Marcus: setup, load, helpers paste
    "nb.s2_quality",       # Marcus: 6 traps
    "nb.s3_claim_surge",   # Marcus
    "nb.s4_claim_ebike",   # Marcus
    "nb.s5_claim_deadly",  # Marcus
    "nb.s6_ageing",        # Marcus numbers / Germaine campaign angle
    "nb.s7_modelling",     # Marcus
    "nb.s8_recommend",     # Germaine
    "nb.s9_limits",        # Germaine drafts, Marcus adds
    "nb.s10_appendix",     # both
]


def build():
    nb = new_notebook(metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                                "language_info": {"name": "python"}})
    for mod in SECTIONS:
        m = importlib.import_module(mod)
        cells = m.cells()
        assert cells and cells[0].cell_type == "markdown", f"{mod}: first cell must be a markdown header"
        nb.cells.extend(cells)
    nbformat.write(nb, OUT)
    print(f"wrote {OUT}: {len(nb.cells)} cells")
    return nb


def test(nb):
    from nbclient import NotebookClient
    client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": HERE}})
    client.execute()
    errs = [(i, o) for i, c in enumerate(nb.cells) if c.cell_type == "code"
            for o in c.get("outputs", []) if o.get("output_type") == "error"]
    assert not errs, f"cell {errs[0][0]} failed: {errs[0][1].get('ename')}: {errs[0][1].get('evalue')}"
    nbformat.write(nb, OUT)  # keep executed outputs so judges see charts without running
    print(f"executed OK: {sum(c.cell_type == 'code' for c in nb.cells)} code cells, outputs saved")


if __name__ == "__main__":
    nb = build()
    if "--test" in sys.argv:
        test(nb)
