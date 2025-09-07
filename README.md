# Workload Allocation Model (WAM)

Optimisation and heuristic approaches for **academic workload allocation**.  
This repository implements **Integer Linear Programming (ILP)**, **Genetic Algorithms (GA)**, and **Large Neighbourhood Search (LNS)** for fair task distribution across academic staff, with reproducibility aligned to my MSc Data Science dissertation at the University of Manchester.

---

## Repository Structure

Workload-Allocation/
├─ data/ # Medium & Large synthetic instances
├─ src/ # ILP + CLI runner (run.py, ilp.py)
├─ New.ipynb # Full pipeline (ILP → GA → LNS → ILP Polish + Visuals)
├─ configs_medium.json
├─ configs_large.json
└─ outputs/
└─ runs/
├─ medium_ml/ # Artefacts for Medium ILP run
├─ large_ml/ # Artefacts for Large ILP run
├─ large_ml_ga/ # GA refinements (Large)
├─ large_ml_lns/ # LNS refinements (Large)
└─ ... # Other labelled experiments



Each **run folder** under `outputs/runs/` contains:
- `per_task.csv`, `per_staff.csv` → allocations & staff loads
- `metrics.json` → fairness KPIs (spread, std, CV, Gini)
- `info.json` → solver objective & metadata
- `*.png` → per-run visuals (heatmaps, Lorenz curves, load plots, etc.)
- `allocation_bundle.xlsx`, `staff_load_summary.csv` (polish runs only)

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
Tested on Python 3.10+ (works on 3.11).

🚀 How to Run
Notebook (recommended)
Open New.ipynb

Run all cells sequentially

Produces labelled outputs under outputs/runs/ and all visuals (heatmaps, load plots, Lorenz curves)

CLI (ILP baseline only)
From inside src/:

bash
Copy code
python run.py ../data/medium ../configs_medium.json
python run.py ../data/large  ../configs_large.json
 Key Results
Medium (ILP baseline)
Spread ≈ 20.5 | Std ≈ 6.1 | CV ≈ 0.278 | Gini ≈ 0.154

Large

ILP baseline: Spread ≈ 30.0 | Std ≈ 7.4 | CV ≈ 0.533 | Gini ≈ 0.289

GA: Spread ≈ 23.2 | Std ≈ 6.4 | CV ≈ 0.429 | Gini ≈ 0.232

LNS: Similar to GA (minor variation)

Full-resolution Large dataset heatmaps and extended diagnostics are inside the run folders (e.g., outputs/runs/large_ml/heatmap.png).

 Diagnostics & Visuals
Heatmaps (task vs staff allocations)

Per-staff load distribution plots

Lorenz curves (fairness visualisation)

Extended logs (zero-candidate tasks, bottlenecks, GA/LNS traces)

All stored inside their respective run folders.

 Citation
Oak, V. (2025). Optimisation and Heuristic Approaches to Academic Workload Allocation. MSc Data Science Dissertation, University of Manchester.

 Notes
Notebook path is the authoritative run pipeline.

CLI runs may overwrite flat files unless moved/renamed.

Final ILP polish can reduce fairness if weights favour efficiency.

yaml


