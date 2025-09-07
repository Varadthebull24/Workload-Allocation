
import json, sys, pandas as pd, os
from ilp import solve_ilp

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run.py <data_dir> <config.json>")
        raise SystemExit(1)
    data_dir = sys.argv[1]
    cfg_path = sys.argv[2]
    cfg = json.loads(open(cfg_path).read())
    per_task, per_staff, info = solve_ilp(data_dir, cfg)
    print(json.dumps(info, indent=2))
    outdir = os.path.join(os.path.dirname(cfg_path), "..", "outputs", "runs")
    os.makedirs(outdir, exist_ok=True)
    pd.DataFrame(per_task).to_csv(os.path.join(outdir,"per_task.csv"), index=False)
    pd.DataFrame(per_staff).to_csv(os.path.join(outdir,"per_staff.csv"), index=False)
    with open(os.path.join(outdir,"info.json"), "w") as f:
        f.write(json.dumps(info, indent=2))
