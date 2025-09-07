# Workload Allocation Model (WAM)

This repository implements optimisation and heuristic approaches for **academic workload allocation**, including **Integer Linear Programming (ILP)**, **Genetic Algorithms (GA)**, and **Large Neighbourhood Search (LNS)**. It was developed as part of my MSc Data Science dissertation at the University of Manchester.

---

## Repository Structure

- `data/` → Medium & Large synthetic datasets  
- `src/` → ILP + CLI runner (`run.py`, `ilp.py`)  
- `New.ipynb` → Full pipeline (ILP → GA → LNS → ILP polish + visualisations)  
- `configs_medium.json`, `configs_large.json` → Config files for experiments  
- `outputs/runs/` → Results folders for each labelled run (e.g., `medium_ml`, `large_ml_ga`, etc.)

Each run folder inside `outputs/runs/` contains:
- `per_task.csv`, `per_staff.csv` → allocations and staff loads  
- `metrics.json` → fairness KPIs (spread, standard deviation, coefficient of variation, Gini)  
- `info.json` → solver objective and metadata  
- `*.png` → per-run visuals (heatmaps, load plots, Lorenz curves, etc.)  
- `allocation_bundle.xlsx`, `staff_load_summary.csv`, `tasks_allocated.csv` (for polish runs)

---

## Environment Setup

```bash
git clone https://github.com/Varadthebull24/Workload-Allocation.git
cd Workload-Allocation

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install --upgrade pip
pip install -r requirements.txt || \
  pip install pandas numpy pulp ortools scikit-learn matplotlib

