#!/usr/bin/env python
"""Run the whole pipeline (or part of it) in dependency order and print a timing table.

    python tools/run_all.py                 # refit the loss-trend model, then draw all 13 figures (about 3 minutes, one script at a time)
    python tools/run_all.py --figures       # draw the figures only (reuses results/c01_loss_trend*)
    python tools/run_all.py --only c04 c07  # just those charts (a prefix of the script name is enough)
    python tools/run_all.py -j 2            # run two independent scripts at a time (about 2 minutes on two cores)
    python tools/run_all.py --sensitivity   # also run the seven robustness checks in sensitivity/ (about 6 more minutes at -j 2)
    python tools/run_all.py --only s06      # one robustness check (it first reruns the chart it checks)

Every script is self-contained: it reads data/*.csv, writes its numbers to results/ and its picture to figures/.
Two charts depend on others: Chart 1 reads the loss-trend model's output, and Chart 10 reads the posterior draws
that Charts 6 and 8 save. This runner respects that order; the Makefile calls it.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (name, script, names it must wait for); the last seven are robustness checks, run only with --sensitivity or --only
STEPS = [
    ("model_c01", "models/c01_loss_trend.py", []),
    ("c00_lede_cost", "charts/c00_lede_cost.py", []),
    ("c01_losses", "charts/c01_losses.py", ["model_c01"]),
    ("c02_police", "charts/c02_police.py", []),
    ("c03_talent", "charts/c03_talent.py", []),
    ("c04_amdahl", "charts/c04_amdahl.py", []),
    ("c05_inference", "charts/c05_inference.py", []),
    ("c06_attacker_lag", "charts/c06_attacker_lag.py", []),
    ("c07_pay", "charts/c07_pay.py", []),
    ("c08_govlag", "charts/c08_govlag.py", []),
    ("c09_state_patience", "charts/c09_state_patience.py", []),
    ("c10_odds", "charts/c10_odds.py", ["c06_attacker_lag", "c08_govlag"]),
    ("c11_defenders", "charts/c11_defenders.py", []),
    ("c12_funnel", "charts/c12_funnel.py", []),
    ("s01_loss_trend", "sensitivity/s01_loss_trend.py", []),
    ("s02_police_selection", "sensitivity/s02_police_selection.py", ["c02_police"]),
    ("s05_provider_selection", "sensitivity/s05_provider_selection.py", ["c05_inference"]),
    ("s06_adoption_lags", "sensitivity/s06_adoption_lags.py", ["c06_attacker_lag"]),
    ("s07_israel_state_pay", "sensitivity/s07_israel_state_pay.py", ["c07_pay"]),
    ("s08_open_source_dating", "sensitivity/s08_open_source_dating.py", ["c08_govlag"]),
    ("s09_state_selection", "sensitivity/s09_state_selection.py", ["c09_state_patience"]),
]
OPTIONAL = {s[0] for s in STEPS if s[1].startswith("sensitivity/")}


def run_one(name: str, script: str) -> tuple[str, bool, float, str]:
    t0 = time.time()
    p = subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, capture_output=True, text=True)
    return name, p.returncode == 0, time.time() - t0, (p.stdout + p.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--figures", action="store_true", help="skip refitting the loss-trend model")
    ap.add_argument("--only", nargs="+", metavar="CHART", help="run only these charts (e.g. c04 c07)")
    ap.add_argument("-j", "--jobs", type=int, default=1, help="scripts to run at once (default 1)")
    ap.add_argument("--sensitivity", action="store_true", help="also run the robustness checks in sensitivity/")
    args = ap.parse_args()

    steps = [s for s in STEPS if args.sensitivity or args.only or s[0] not in OPTIONAL]
    if args.figures:
        steps = [s for s in steps if s[0] != "model_c01"]
    if args.only:
        want = [w.lower() for w in args.only]
        keep = {s[0] for s in steps if any(s[0].startswith(w) for w in want)}
        if not keep:
            print(f"nothing matches {args.only}; choose from: {', '.join(s[0] for s in STEPS)}")
            return 2
        # a chart that needs another step's output pulls that step in
        changed = True
        while changed:
            changed = False
            for name, _, deps in steps:
                if name in keep:
                    for d in deps:
                        if d not in keep and any(s[0] == d for s in steps):
                            keep.add(d)
                            changed = True
        steps = [s for s in steps if s[0] in keep]

    in_run = {s[0] for s in steps}
    done: dict[str, bool] = {}
    pending = list(steps)
    running: dict = {}
    failed = False
    t_start = time.time()
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        while pending or running:
            # a step is ready when every step it waits for (that is part of this run) has finished successfully
            ready = [s for s in pending if all(done.get(d) for d in s[2] if d in in_run)]
            while ready and len(running) < max(1, args.jobs) and not failed:
                s = ready.pop(0)
                pending.remove(s)
                running[pool.submit(run_one, s[0], s[1])] = s
            if not running:
                break
            finished = [f for f in running if f.done()]
            if not finished:
                time.sleep(0.05)
                continue
            for f in finished:
                running.pop(f)
                name, ok, secs, out = f.result()
                done[name] = ok
                print(f"{'ok  ' if ok else 'FAIL'} {name:22s} {secs:6.1f} s", flush=True)
                if not ok:
                    failed = True
                    print(out[-2000:])
    if failed:
        print("stopped: a script failed")
        return 1
    print(f"{'-' * 40}\nall done in {time.time() - t_start:.0f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
