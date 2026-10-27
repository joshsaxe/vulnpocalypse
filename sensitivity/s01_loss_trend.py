"""Chart 1 robustness: does the finding that growth slowed after 2022 survive other defensible assumptions?

The methods appendix says: "the main finding, that growth slowed after 2022, survives changes to the assumptions: no
common reporting drift, double the drift, and tighter or looser limits on how far a single series may drift. Across
them, fraud losses grew by 12-17% a year in 2017-22 and by 8-11% a year in 2022-25; hacking losses by 22-25% a year,
then by 9-11%. Two hacking indicators count incidents rather than dollars. Dropping them makes hacking losses roughly
flat since 2022 (3% a year)."  This script produces those numbers (on medians the first range is 11.1-16.9%; the 12 is
the mean-based figure from one variant, see docs/METHODS.md). It re-runs the Chart 1 model (models/c01_loss_trend.py)
with one assumption changed at a time:

    baseline              the model as charted
    no common drift       the reporting-rate drift that hits every series is set to zero (charted: +2% a year for
                          American portals, +1% elsewhere, +1% for hacking)
    double common drift   that drift doubled
    idiosyncratic 0.01    each series may drift only 1 point a year relative to the others (charted: sd 3 points)
    idiosyncratic 0.06    each series may drift up to 6 points a year relative to the others
    hacking, dollars only the two hacking indicators that count incidents (breach notices x average breach cost, and
                          victims named on ransomware leak sites) are dropped

Output: results/sensitivity_c01.json and a table on screen. About 40 seconds. The script re-uses the model module, so
it cannot drift away from it; the baseline row reproduces results/c01_loss_trend.json.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
sys.path.insert(0, str(ROOT / "models"))         # models/c01_loss_trend.py
import numpy as np
import c01_loss_trend as M
from common.paths import RESULTS, dump_json

LEAK_AND_BREACH = ["Ransomware leak-site victims (count), 2023-25", "ITRC breach notices x IBM cost per breach, 2018-25"]
i = {y: y - 2005 for y in (2005, 2012, 2015, 2017, 2022, 2025)}


def growth(X, y0, y1):
    """Median compound annual growth between two years, across draws (per cent)."""
    return round(float(np.median((X[:, i[y1]] / X[:, i[y0]]) ** (1 / (y1 - y0)) - 1)) * 100, 1)


def summarise(F=None, H=None):
    out = {}
    if F is not None:
        out["fraud_median_bn"] = {str(y): round(float(np.median(F[:, i[y]])), 1) for y in (2005, 2015, 2022, 2025)}
        out["fraud_growth_pct_pa"] = {"2017-22": growth(F, 2017, 2022), "2022-25": growth(F, 2022, 2025)}
        # the appendix's lower end for fraud in 2017-22 (12%) is the mean across draws, not the median; kept for the record
        out["fraud_growth_2017-22_mean_pct_pa"] = round(float(np.mean((F[:, i[2022]] / F[:, i[2017]]) ** 0.2 - 1)) * 100, 1)
    if H is not None:
        out["hack_median_bn"] = {str(y): round(float(np.median(H[:, i[y]])), 1) for y in (2015, 2022, 2025)}
        out["hack_growth_pct_pa"] = {"2017-22": growth(H, 2017, 2022), "2022-25": growth(H, 2022, 2025)}
    return out


results = {}


def run(name, fraud=True, hack=True):
    F = M.run_fraud()["fraud"] if fraud else None
    H = M.run_hack()["hack"] if hack else None
    results[name] = summarise(F, H)
    print(f"{name:24s}", results[name], flush=True)


# the order of the runs matters a little: the model draws from one seeded random stream
run("baseline")

orig_drift = M.common_drift
M.common_drift = lambda mean, sd, n: np.zeros(n)
run("no common drift")
M.common_drift = lambda mean, sd, n: M.RNG.normal(2 * mean, sd, n)
run("double common drift")
M.common_drift = orig_drift

orig_hack_series = M.hack_series


def dollars_only():
    d = orig_hack_series()
    for k in LEAK_AND_BREACH:
        d.pop(k)
    return d


M.hack_series = dollars_only
run("hacking, dollars only", fraud=False)
M.hack_series = orig_hack_series

orig_gibbs = M.gibbs_dfm_drift
for sd in (0.01, 0.06):
    def patched(*args, _sd=sd, **kwargs):
        kwargs["drift_sd"] = _sd
        return orig_gibbs(*args, **kwargs)
    M.gibbs_dfm_drift = patched
    run(f"idiosyncratic drift {sd}")
M.gibbs_dfm_drift = orig_gibbs

# the ranges quoted in the appendix: every variant except 'hacking, dollars only' (which is its own sentence)
core = [v for k, v in results.items() if k != "hacking, dollars only"]
rng = lambda key, per: [min(v[key][per] for v in core), max(v[key][per] for v in core)]
results["ranges_across_variants_pct_pa"] = {
    "fraud_2017-22": rng("fraud_growth_pct_pa", "2017-22"), "fraud_2022-25": rng("fraud_growth_pct_pa", "2022-25"),
    "hack_2017-22": rng("hack_growth_pct_pa", "2017-22"), "hack_2022-25": rng("hack_growth_pct_pa", "2022-25")}
print("ranges across variants:", results["ranges_across_variants_pct_pa"])
dump_json(results, RESULTS / "sensitivity_c01.json")
