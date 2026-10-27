"""Chart 8 robustness: dating open source's arrival in US agencies from the Pentagon's 2009 policy memo.

The methods appendix says: "That rests partly on the estimated years: dating open source's agency adoption from the
Pentagon's October 2009 policy memo (2009-11) instead of 2012-14 removes the downward trend from the fit without
generative AI and lowers the chance to 55% (median mid-2029)."  This script produces those numbers.

It repeats the Chart 8 model (charts/c08_govlag.py: the same code and seeds) with one input changed: the open-source row's
agency years (ns_mainstream_year_low / _high) are 2009 and 2011 instead of 2012 and 2014. It reports, for the fit
without the generative-AI row, the chance that the lag is shrinking, and for the mix of the two fits the median year
and the chance that US agencies are routinely using AI agents by the end of 2029 (given that they were not by October
2026). The 'charted' row must reproduce results/c08_govlag.json; the script stops if it does not. About 2.5 minutes.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from scipy import stats
from common.bayes import metropolis
from common.paths import DATA, RESULTS, dump_json

LABELS = ["Open-source software", "Agile / DevSecOps", "Smartphones / mobile devices", "Commercial cloud",
          "Machine learning (production ML)", "SaaS / video conferencing", "Generative AI (LLM chatbots)"]


def prepare(os_years=None):
    rows = pd.read_csv(DATA / "G_adoption.csv")
    rows = rows[rows.technology.isin(LABELS)].copy()
    if os_years is not None:
        m = rows.technology == "Open-source software"
        rows.loc[m, "ns_mainstream_year_low"], rows.loc[m, "ns_mainstream_year_high"] = os_years
    rows["pl"], rows["ph"] = rows.private_mainstream_year_low, rows.private_mainstream_year_high
    rows["nl"], rows["nh"] = rows.ns_mainstream_year_low, rows.ns_mainstream_year_high
    rows["pm"] = (rows.pl + rows.ph) / 2
    rows["lag_lo"] = np.maximum(0.25, rows.nl - rows.ph)
    rows["lag_hi"] = np.maximum(rows.lag_lo + 0.25, rows.nh - rows.pl)
    return rows


def fit_rows(f, seed):
    lo, hi, x = f.lag_lo.values, f.lag_hi.values, f.pm.values - 2015

    def logp(th):
        a, b, ls = th
        s = np.exp(ls)
        if not 0.05 < s < 3:
            return -np.inf
        mu = a + b * x
        p = stats.norm.cdf((np.log(hi) - mu) / s) - stats.norm.cdf((np.log(lo) - mu) / s)
        return (np.sum(np.log(np.clip(p, 1e-300, None))) + stats.norm.logpdf(a, np.log(5), 1)
                + stats.norm.logpdf(b, 0, 0.1) + stats.halfnorm.logpdf(s, scale=0.7) + ls)

    dr, rh, acc = metropolis(logp, np.array([np.log(5), 0.0, np.log(0.4)]), n_iter=30000, n_burn=8000,
                             init_scale=0.1, seed=seed)
    return dr[:, 0], dr[:, 1], np.exp(dr[:, 2]), rh


def run(os_years=None):
    rows = prepare(os_years)
    base = rows[~rows.technology.str.startswith("SaaS")]
    nogen = base[~base.technology.str.startswith("Generative")]
    out, proj = {}, {}
    for name, f, seed in (("all", base, 7), ("without_genai", nogen, 8)):
        a, b, s, rh = fit_rows(f, seed)
        rng = np.random.default_rng(71 + seed)
        pyear = rng.uniform(2025.0, 2026.0, a.size)
        lag_pred = np.exp(a + b * (pyear - 2015) + s * rng.standard_normal(a.size))
        proj[name] = pyear + lag_pred
        out[name] = {"p_shrinking": round(float(np.mean(b < 0)), 3)}
    mix = np.concatenate([proj["all"], proj["without_genai"]])
    mix = mix[mix >= 2026.8]          # routine use had not begun by October 2026
    out["mixture"] = {"ns_year_q": np.quantile(mix, [0.1, 0.5, 0.9]).round(1).tolist(),
                      "p_by_end_2029": round(float(np.mean(mix < 2030.0)), 3)}
    return out


charted = run()
ref = json.load(open(RESULTS / "c08_govlag.json"))
assert charted["mixture"]["ns_year_q"] == ref["mixture"]["ns_year_q"], "charted row differs from Chart 8"
assert charted["mixture"]["p_by_end_2029"] == ref["mixture"]["p_by_end_2029"], "charted row differs from Chart 8"
assert charted["without_genai"]["p_shrinking"] == ref["without_genai"]["p_shrinking"], "charted row differs from Chart 8"
print("the charted row reproduces results/c08_govlag.json")
variant = run((2009, 2011))
res = {"charted": charted, "open_source_agency_years_2009_2011": variant}
print("charted                      :", charted)
print("open source in agencies 2009-11:", variant)
dump_json(res, RESULTS / "sensitivity_c08.json")
