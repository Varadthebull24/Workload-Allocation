# Workload Allocation Model (WAM)

This repository contains the code and datasets for my MSc Data Science dissertation at the University of Manchester: *Optimisation and Heuristic Approaches to Academic Workload Allocation*.  

The project explores how **Integer Linear Programming (ILP)**, **Genetic Algorithms (GA)**, and **Large Neighbourhood Search (LNS)** can be used to allocate academic tasks fairly across staff.

---

## Repository Structure

- `data/` → Medium & Large synthetic datasets  
- `src/` → Source code for ILP and CLI runner  
- `New.ipynb` → Full end-to-end pipeline (ILP → GA → LNS → Polish + Visuals)  
- `configs_medium.json`, `configs_large.json` → Configuration files for experiments  
- `outputs/runs/` → Contains results for each labelled run

Each run folder inside `outputs/runs/` includes:
- `per_task.csv`, `per_staff.csv` → allocations and staff loads  
- `metrics.json` → fairness KPIs (spread, standard deviation, CV, Gini)  
- `info.json` → solver objective and metadata  
- `*.png` → per-run visuals (heatmaps, load plots, Lorenz curves, etc.)  
- `allocation_bundle.xlsx`, `staff_load_summary.csv`, `tasks_allocated.csv` (for polish runs)

---

## Results Summary

- **Medium instance (ILP baseline)**  
  Spread ≈ 20.5 | Std ≈ 6.1 | CV ≈ 0.278 | Gini ≈ 0.154  

- **Large instance**  
  - ILP baseline: Spread ≈ 30.0 | Std ≈ 7.4 | CV ≈ 0.533 | Gini ≈ 0.289  
  - GA: Spread ≈ 23.2 | Std ≈ 6.4 | CV ≈ 0.429 | Gini ≈ 0.232  
  - LNS: Similar to GA (minor variation)  

Full-resolution **Large dataset heatmaps** are included in each large run folder (e.g., `outputs/runs/large_ml/heatmap.png`, `outputs/runs/large_ml_ga/heatmap.png`).

---

## Visuals and Diagnostics

Each run folder contains:
- Heatmaps (task vs staff allocation)  
- Per-staff load distribution plots  
- Lorenz curves (fairness visualisation)  
- Logs and diagnostics (e.g., zero-candidate tasks, bottlenecks, GA/LNS traces)

---

## Notes

- The **notebook** (`New.ipynb`) is the main reproducibility path.  
- The **CLI** (`src/run.py`) is limited to ILP baseline and overwrites flat files unless renamed.  
- Final ILP polish can reduce fairness if objective weights favour efficiency.

---

## Citation

Oak, V. (2025). *Optimisation and Heuristic Approaches to Academic Workload Allocation*. MSc Data Science Dissertation, University of Manchester.
