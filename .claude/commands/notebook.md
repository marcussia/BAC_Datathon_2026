---
description: Regenerate analysis/bac_round2.ipynb from analysis/build_notebook.py, execute it with nbclient, report errors
---
Run `python analysis/build_notebook.py --test` from the repo root (use the Anaconda python). It rebuilds `analysis/bac_round2.ipynb` from the section modules in `analysis/nb/` and executes every cell top to bottom with nbclient, saving outputs and charts to `analysis/charts/`.

If it fails: report the section module, the first line of the failing cell and the error, fix the section module (never the .ipynb by hand), and rerun until clean.

When it passes: print the `SLIDE n:` lines from the executed notebook (they're also in `analysis/slide_numbers.csv`) and list the chart files written. Remind me to `git add analysis/` so the script, notebook and charts are committed together.
$ARGUMENTS
