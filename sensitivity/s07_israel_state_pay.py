"""Chart 7 robustness: Israel's state pay measured by Mossad and Shin Bet alone.

The methods appendix says: "Israel's state figures are averages for all army, Mossad and Shin Bet staff, not
engineers; against Mossad and Shin Bet alone the ratio is about 1.7."  Chart 7 uses four Israeli state rows
(data/F_pay.csv rows 32-35: IDF career personnel's starting and average pay, the Mossad and Shin Bet average, and IDF
civilian staff's average). This script repeats the Chart 7 measurement model (same code, same seed, the same random
stream in the same order) with only the Mossad and Shin Bet row (34) on the state side, and reports the private-to-state
ratio. The 'charted' rows must reproduce results/c07_pay.json; the script stops if they do. Runs in a second or two.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from common.paths import DATA, RESULTS, dump_json

F = pd.read_csv(DATA / "F_pay.csv")
GRADE_SD = {"A": 0.15, "B": 0.25, "C": 0.40, "D": 0.60}
ROLE_SD = 0.25
USE = {            # as in charts/c07_pay.py
    "United States": {"state": [0, 1, 7], "private": [11], "frontier": [14, 15]},
    "United Kingdom": {"state": [17, 18, 19, 20, 21, 22], "private": [24]},
    "Israel": {"state": [32, 33, 34, 35], "private": [39]},
    "China": {"state": [41], "private": [42]},
}


def posterior(rows, rng, n=60000, prior_sd=10.0):
    prec, num = 1 / prior_sd ** 2, np.log(80000) / prior_sd ** 2
    for i in rows:
        r = F.iloc[i]
        lo = r.usd_annual_low if pd.notna(r.usd_annual_low) else r.usd_annual_high
        hi = r.usd_annual_high if pd.notna(r.usd_annual_high) else r.usd_annual_low
        m = 0.5 * (np.log(lo) + np.log(hi))
        half = 0.5 * (np.log(hi) - np.log(lo))
        sd = np.sqrt(GRADE_SD[str(r.grade)[0]] ** 2 + (half / 1.28) ** 2 + ROLE_SD ** 2)
        prec += 1 / sd ** 2
        num += m / sd ** 2
    mu, s = num / prec, np.sqrt(1 / prec)
    return np.exp(rng.normal(mu, s, n))


def ratios(use):
    rng = np.random.default_rng(66)
    qr = lambda x: [round(float(t), 2) for t in np.quantile(x, [0.1, 0.5, 0.9])]
    out = {}
    for c, sides in use.items():
        d = {k: posterior(v, rng) for k, v in sides.items()}
        out[c] = qr(d["private"] / d["state"])
    return out


charted = ratios(USE)
variant_use = {**USE, "Israel": {"state": [34], "private": [39]}}
variant = ratios(variant_use)

ref = json.load(open(RESULTS / "c07_pay.json"))
for c in USE:
    assert charted[c] == ref[c]["ratio"], f"charted ratio for {c} differs from Chart 7"
print("the charted rows reproduce results/c07_pay.json")
res = {"israel_ratio_charted": charted["Israel"], "israel_ratio_mossad_shin_bet_only": variant["Israel"]}
print(f"Israel, private / state: charted {charted['Israel']}  Mossad and Shin Bet only {variant['Israel']}")
dump_json(res, RESULTS / "sensitivity_c07.json")
