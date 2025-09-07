# Workload Allocation Model

This repo contains my MSc Data Science project on **academic workload allocation**.  
It looks at different optimisation and heuristic approaches — **ILP (Integer Linear Programming)** as a baseline, and **Genetic Algorithms (GA)** plus **Large Neighbourhood Search (LNS)** as alternative methods — to see how fairly tasks can be distributed across staff.

---

## What’s Inside

- `data/` → synthetic Medium and Large workload datasets  
- `src/` → Python source code, including the ILP runner (`run.py`, `ilp.py`)  
- `New.ipynb` → main notebook with the full pipeline and plots  
- `configs_*.json` → config files for running experiments  
- `outputs/runs/` → results saved by each run (labelled folders)

Each folder in `outputs/runs/` has:
- CSVs with allocations (`per_task.csv`, `per_staff.csv`)  
- Solver info (`info.json`, `metrics.json`)  
- Plots (`.png` files: heatmaps, Lorenz curves, load distributions, etc.)  
- Extra exports for polish runs (`allocation_bundle.xlsx`, summaries)

---

## Highlights

- **Medium dataset (ILP baseline):**  
  Spread ≈ 20.5 | Std ≈ 6.1 | CV ≈ 0.278 | Gini ≈ 0.154  

- **Large dataset:**  
  - ILP baseline: Spread ≈ 30.0 | Std ≈ 7.4 | CV ≈ 0.533 | Gini ≈ 0.289  
  - GA refinement: Spread ≈ 23.2 | Std ≈ 6.4 | CV ≈ 0.429 | Gini ≈ 0.232  
  - LNS: close to GA results  

The full-size **Large dataset heatmaps** are in their respective run folders, e.g. `outputs/runs/large_ml/heatmap.png`.

---

## Visuals & Logs

For each run you’ll find:
- Heatmaps of task vs staff allocation  
- Distribution of staff loads  
- Lorenz curves for fairness  
- Logs/diagnostics (e.g. bottlenecks, GA/LNS traces)

---

## Notes

- The notebook (`New.ipynb`) is the main way to reproduce results end-to-end.  
- The CLI (`src/run.py`) runs the ILP baseline only, and will overwrite files unless you move/rename them.  
- The polish step sometimes improves the global objective but can slightly reduce fairness.  
- ⚠️ **Dataset guidelines are strict.** Results depend on the provided schema, column names, and constraints.  
  If the dataset structure is changed or not followed exactly, the outputs may be invalid or inconsistent with the dissertation results.

---

## Reference

Oak, V. (2025). *Optimisation and Heuristic Approaches to Academic Workload Allocation*. MSc Data Science Dissertation, University of Manchester.
