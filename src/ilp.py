
import pandas as pd
import pulp as pl
from collections import defaultdict

def load_inputs(data_dir:str):
    staff = pd.read_csv(f"{data_dir}/staff.csv")
    tasks = pd.read_csv(f"{data_dir}/tasks.csv")
    eligibility = pd.read_csv(f"{data_dir}/eligibility.csv")
    quals = pd.read_csv(f"{data_dir}/qualifications.csv")
    availability = pd.read_csv(f"{data_dir}/availability.csv")
    contracts = pd.read_csv(f"{data_dir}/contracts.csv")
    preferences = pd.read_csv(f"{data_dir}/preferences.csv") if (pd.io.common.file_exists(f"{data_dir}/preferences.csv")) else pd.DataFrame(columns=["staff_id","task_id","pref_score"])
    incompat = pd.read_csv(f"{data_dir}/incompatibilities.csv") if (pd.io.common.file_exists(f"{data_dir}/incompatibilities.csv")) else pd.DataFrame(columns=["task_id","task_id2","reason"])
    slot_prefs = pd.read_csv(f"{data_dir}/slot_prefs.csv") if (pd.io.common.file_exists(f"{data_dir}/slot_prefs.csv")) else pd.DataFrame(columns=["staff_id","slot_type","cost"])
    return staff, tasks, eligibility, quals, availability, preferences, contracts, incompat, slot_prefs

def solve_ilp(data_dir:str, cfg:dict):
    staff, tasks, eligibility, quals, availability, preferences, contracts, incompat, slot_prefs = load_inputs(data_dir)
    S = staff["staff_id"].tolist()
    T = tasks["task_id"].tolist()
    M = tasks["module"].unique().tolist()
    P = tasks["period"].unique().tolist()
    slot_types = tasks["slot_type"].unique().tolist()

    hours = dict(tasks[["task_id","hours"]].values)
    period_of = dict(tasks[["task_id","period"]].values)
    module_of = dict(tasks[["task_id","module"]].values)
    slot_of = dict(tasks[["task_id","slot_type"]].values)
    type_of = dict(tasks[["task_id","type"]].values)
    must_assign = dict(tasks[["task_id","must_assign"]].values)

    max_hours = dict(staff[["staff_id","max_hours"]].values)
    target_hours = dict(staff[["staff_id","target_hours"]].values)
    grade = dict(staff[["staff_id","grade"]].values)
    prep_cap = dict(staff[["staff_id","prep_cap"]].values)
    soft_prep_target = dict(staff[["staff_id","soft_prep_target"]].values)
    thr_excess = dict(staff[["staff_id","thr_excess"]].values)
    home_campus = dict(staff[["staff_id","home_campus"]].values)

    eligible_pairs = set((r.task_id, r.staff_id) for r in eligibility.itertuples() if getattr(r,"eligible",1)==1)
    skill_penalty = {(r.task_id, r.staff_id): getattr(r,"penalty",0.0) for r in eligibility.itertuples()}
    qualified = set((r.staff_id, r.module) for r in quals.itertuples() if r.qualified==1)
    available = {(r.staff_id, r.period): r.available for r in availability.itertuples()}
    contract_limit = {(r.staff_id, r.slot_type): r.limit for r in contracts.itertuples()}

    from collections import defaultdict
    pref_penalty = defaultdict(float)
    for r in preferences.itertuples():
        pref_penalty[(r.task_id, r.staff_id)] = float(1.0 - r.pref_score)

    slot_cost = defaultdict(float)
    for r in slot_prefs.itertuples():
        slot_cost[(r.staff_id, r.slot_type)] = float(r.cost)

    cand = set()
    for t in T:
        mmod = module_of[t]
        for s in S:
            if (t,s) in eligible_pairs and (s,mmod) in qualified:
                cand.add((t,s))

    if cfg.get("use_topk", False):
        k = int(cfg.get("topk_per_task", 5))
        pruned = set()
        for t in T:
            lst = []
            for s in S:
                if (t,s) in cand:
                    sc = 0.5*pref_penalty.get((t,s),0.5) + 0.5*skill_penalty.get((t,s),0.0)
                    lst.append((sc, s))
            lst.sort(key=lambda x:x[0])
            keep = set(s for _,s in lst[:max(1,k)])
            for s in S:
                if (t,s) in cand and s in keep:
                    pruned.add((t,s))
        cand = pruned

    m = pl.LpProblem("WAM", pl.LpMinimize)
    x = pl.LpVariable.dicts("x", (T,S), 0, 1, pl.LpBinary)
    y = pl.LpVariable.dicts("y", (S,M), 0, 1, pl.LpBinary)
    assign_slot = pl.LpVariable.dicts("assign_slot", (S, slot_types), 0, None, pl.LpInteger)
    devp = pl.LpVariable.dicts("devp", S, lowBound=0)
    devm = pl.LpVariable.dicts("devm", S, lowBound=0)
    excess = pl.LpVariable.dicts("excess", S, lowBound=0)
    frag_excess = pl.LpVariable.dicts("frag_excess", S, lowBound=0)

    # Hard constraints
    for t in T:
        m += pl.lpSum(x[t][s] for s in S if (t,s) in cand) == must_assign[t], f"cover_{t}"

    for s in S:
        m += pl.lpSum(hours[t]*x[t][s] for t in T if (t,s) in cand) <= max_hours[s], f"cap_{s}"

    for t in T:
        for s in S:
            if (t,s) not in cand:
                m += x[t][s] == 0, f"ineligible_{t}_{s}"

    for s in S:
        for p in P:
            if available.get((s,p),1)==0:
                m += pl.lpSum(x[t][s] for t in T if period_of[t]==p) == 0, f"avail_{s}_{p}"

    for s in S:
        for p in P:
            m += pl.lpSum(x[t][s] for t in T if period_of[t]==p) <= 1, f"one_per_period_{s}_{p}"

    for s in S:
        for mmod in M:
            for t in T:
                if module_of[t]==mmod:
                    m += y[s][mmod] >= x[t][s], f"y_link_{s}_{mmod}_{t}"
        m += pl.lpSum(y[s][mmod] for mmod in M) <= prep_cap[s], f"prep_cap_{s}"

    if not preferences.empty:
        pass

    # Incompatibility pairs
    # (re-load within function to avoid dependency)
    import pandas as pd
    inc_path = f"{data_dir}/incompatibilities.csv"
    if pd.io.common.file_exists(inc_path):
        incompat = pd.read_csv(inc_path)
        for r in incompat.itertuples():
            t1, t2 = r.task_id, r.task_id2
            for s in S:
                if (t1,s) in cand or (t2,s) in cand:
                    m += x[t1][s] + x[t2][s] <= 1, f"incomp_{t1}_{t2}_{s}"

    # Soft linkages
    for s in S:
        load_s = pl.lpSum(hours[t]*x[t][s] for t in T if (t,s) in cand)
        m += load_s - target_hours[s] == devp[s] - devm[s], f"fair_balance_{s}"

    for s in S:
        if grade[s] == "junior":
            load_s = pl.lpSum(hours[t]*x[t][s] for t in T if (t,s) in cand)
            m += excess[s] >= load_s - thr_excess[s], f"junior_excess_{s}"
        else:
            m += excess[s] == 0, f"junior_excess_zero_{s}"

    for s in S:
        m += frag_excess[s] >= pl.lpSum(y[s][mmod] for mmod in M) - soft_prep_target[s], f"frag_excess_{s}"

    for s in S:
        for sl in slot_types:
            m += assign_slot[s][sl] == pl.lpSum(x[t][s] for t in T if slot_of[t]==sl), f"link_slot_{s}_{sl}"
            lim = contract_limit.get((s,sl), 999)
            if lim < 999:
                m += assign_slot[s][sl] <= lim, f"slot_limit_{s}_{sl}"

    # Objective
    w_fair = float(cfg.get("fairness_weight",1.0))
    w_pref = float(cfg.get("pref_weight",0.3))
    w_skill = float(cfg.get("skill_weight",0.4))
    w_cont = float(cfg.get("continuity_weight",0.1))
    w_jun = float(cfg.get("junior_weight",0.2))
    w_admin = float(cfg.get("admin_weight",0.2))
    w_slot = float(cfg.get("slot_weight",0.05))
    w_frag = float(cfg.get("frag_weight",0.1))

    pref_term = pl.lpSum( (pref_penalty.get((t,s),0.0)) * x[t][s] for (t,s) in cand )
    skill_term = pl.lpSum( (skill_penalty.get((t,s),0.0)) * x[t][s] for (t,s) in cand )
    cont_term = pl.lpSum( pl.lpSum(y[s][mmod] for s in S) - 1 for mmod in M )
    # admin_term approximated as number of admin task-assignments (can be refined to a target deviation)
    admin_term = pl.lpSum( (1 if type_of[t]=="admin" else 0) * x[t][s] for (t,s) in cand )
    slot_term = pl.lpSum( slot_cost.get((s, slot_of[t]),0.0) * x[t][s] for (t,s) in cand )

    obj = (
        w_fair * pl.lpSum(devp[s] + devm[s] for s in S)
        + w_pref * pref_term
        + w_skill * skill_term
        + w_cont * cont_term
        + w_jun * pl.lpSum(excess[s] for s in S)
        + w_admin * admin_term
        + w_slot * slot_term
        + w_frag * pl.lpSum(frag_excess[s] for s in S)
    )
    m += obj

    solver = pl.PULP_CBC_CMD(msg=0, timeLimit=int(cfg.get("time_limit_s",300)), gapRel=float(cfg.get("mip_gap",0.02)))
    status = m.solve(solver)

    per_task = []
    load = {s:0.0 for s in S}
    for t in T:
        for s in S:
            val = pl.value(x[t][s])
            if val is not None and val > 0.5:
                per_task.append({"task_id": t, "staff_id": s, "hours": float(hours[t]), "module": module_of[t], "period": period_of[t]})
                load[s] += hours[t]

    per_staff = [{"staff_id": s, "load": float(load[s])} for s in S]
    info = {"status": pl.LpStatus[status], "objective": float(pl.value(obj)) if pl.value(obj) is not None else None}
    return per_task, per_staff, info
