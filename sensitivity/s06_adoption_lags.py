"""Chart 6 robustness: how much do the classification of past cases and the dating of one of them matter?

The methods appendix says: "Other defensible choices move these numbers: with the original classification the
business-model median is 7.4 years and the chance by the end of 2029 is 21%; dating encrypt-and-ransom from the first
criminal tool (2006) rather than the 1996 paper gives 5.3 years and 41%."  This script produces those numbers.

It repeats the business-model fit of charts/c06_attacker_lag.py (the same code and the same seed; only the input
changes) under three versions of the inputs:

    charted                   the classes and lags used in the chart
    original classification   before the classes were applied strictly: deepfake-voice fraud counted as a new business
                              model and double extortion (which needed leak sites) as a new tool
    encrypt-and-ransom 2006   its lag measured from the first criminal use of the idea (2006), 7 years, instead of from
                              the 1996 paper, 17 years

For each it reports the median lag of the business-model class (years, with its 80% credible interval) and the chance
that AI agents running whole intrusions are widespread by 1 January 2028 / 2030 / 2032, given that they were not by
October 2026 (the quantity Chart 10 plots as the solid red line). The 'charted' row must reproduce
results/c06_attacker_lag.json; the script stops if it does not.

A second block, not quoted in the methods appendix, does the same for the NEW TOOLS class (the left panel of Chart 6 and
the dashed 'if agents are a tool' line of Chart 10), because auditing the inputs found two dates that could be read
differently:

    Mirai from first sighting    the table's own lag for the Mirai botnet (0.1 year: first seen in August 2016, record attacks
                                 weeks later) instead of the 2.3 years the chart uses, which counts from the spread of cheap
                                 insecure gadgets in about 2014
    AI-written phishing, dated   the lag implied by the table's calendar years (1.6 years: ChatGPT in November 2022, 'scaled'
    by calendar year             in 2024) instead of the table's 2.5, which counts to the 2025 Verizon report's finding that
                                 about 10% of malicious email contained AI-written text

About 4 minutes in all.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from scipy import stats
from common.bayes import lognormal_interval_fit
from common.paths import DATA, RESULTS, dump_json

D = pd.read_csv(DATA / "I_adoption_lags.csv")
NOW = 2026.8
# the business-model ('eco') class, as in charts/c06_attacker_lag.py: technique -> lag override (None = use the table)
ECO_CHARTED = {
    "Ransomware-as-a-service (RaaS)": None,
    "Double extortion (steal + encrypt + leak)": None,
    "Commodity exploit kits": None,
    "Ransomware payments in Bitcoin": None,
    "Cobalt Strike as criminal C2 standard": None,
    "Darknet drug/data markets on Tor": None,
    "Cryptoviral extortion (public-key ransomware)": None,
}
AGENTIC_START = 2025 + 1.8 / 12            # AI agents running whole intrusions: not yet widespread (a business model)
ELAPSED = NOW - AGENTIC_START


def eco_fit(spec, seed=11):
    L = np.array([float(ov if ov is not None else D[D.technique == t].iloc[0].lag_scaled_years) for t, ov in spec.items()])
    lo = np.maximum(np.maximum(L - 0.5, L * 0.5), 1 / 365)
    hi = L + np.where(L < 1, L * 0.5, 0.5)
    lo, hi = np.r_[lo, ELAPSED], np.r_[hi, np.inf]              # agents running intrusions: right-censored
    return lognormal_interval_fit(lo, hi, prior_mu=0.0, prior_mu_sd=2.0, prior_sigma_scale=1.5, seed=seed)


def p_scaled_by(f):
    mu, sg = f["mu"], f["sigma"]
    S_el = stats.norm.sf((np.log(ELAPSED) - mu) / sg)
    return {str(t): round(float(np.mean((stats.norm.cdf((np.log(t - AGENTIC_START) - mu) / sg) - (1 - S_el)) / S_el)), 3)
            for t in (2028, 2030, 2032)}


VARIANTS = {"charted": dict(ECO_CHARTED)}
orig = dict(ECO_CHARTED)
del orig["Double extortion (steal + encrypt + leak)"]
orig["Deepfake voice / audio impersonation fraud"] = None
VARIANTS["original classification"] = orig
VARIANTS["encrypt-and-ransom dated from 2006"] = {**ECO_CHARTED, "Cryptoviral extortion (public-key ransomware)": 7.0}

res = {}
for name, spec in VARIANTS.items():
    f = eco_fit(spec)
    q = np.quantile(np.exp(f["mu"]), [0.1, 0.5, 0.9])
    res[name] = {"business_model_median_years": [round(float(v), 2) for v in q], "p_agentic_widespread_by": p_scaled_by(f)}
    print(f"{name:36s} median lag {q[1]:.1f} years ({q[0]:.1f}-{q[2]:.1f});  P(widespread by 2028/2030/2032) =",
          res[name]["p_agentic_widespread_by"], flush=True)


# ---- the 'new tools' class, as in charts/c06_attacker_lag.py -----------------------------------------------------
TOOL_CHARTED = {                       # technique -> lag override (None = use the table)
    "Deepfake voice / audio impersonation fraud": None,
    "IoT DDoS botnets (Mirai)": 2.3,                   # from cheap insecure gadgets (~2014); the table's own lag is 0.1
    "LLM-written phishing/BEC text": None,
}
TOOL_NOT_YET = [NOW - (2023 + 5 / 12),                 # criminal chatbots (WormGPT): right-censored
                NOW - (2022 + 10.97 / 12)]             # malware that calls AI models: right-censored


def tool_fit(spec, with_agents, seed=11):
    L = np.array([float(ov if ov is not None else D[D.technique == t].iloc[0].lag_scaled_years) for t, ov in spec.items()])
    lo = np.maximum(np.maximum(L - 0.5, L * 0.5), 1 / 365)
    hi = L + np.where(L < 1, L * 0.5, 0.5)
    cens = TOOL_NOT_YET + ([ELAPSED] if with_agents else [])
    lo, hi = np.r_[lo, cens], np.r_[hi, np.full(len(cens), np.inf)]
    return lognormal_interval_fit(lo, hi, prior_mu=0.0, prior_mu_sd=2.0, prior_sigma_scale=1.5, seed=seed)


TOOL_VARIANTS = {
    "charted": dict(TOOL_CHARTED),
    "Mirai from first sighting (0.1 year)": {**TOOL_CHARTED, "IoT DDoS botnets (Mirai)": 0.1},
    "AI-written phishing dated by calendar year (1.6 years)": {**TOOL_CHARTED, "LLM-written phishing/BEC text": 1.6},
}
tool_res = {}
for name, spec in TOOL_VARIANTS.items():
    q = np.quantile(np.exp(tool_fit(spec, with_agents=False)["mu"]), [0.1, 0.5, 0.9])
    p = p_scaled_by(tool_fit(spec, with_agents=True))
    tool_res[name] = {"tool_class_median_years": [round(float(v), 2) for v in q], "p_agentic_widespread_by_if_tool": p}
    print(f"[tool class] {name:56s} median lag {q[1]:.1f} years ({q[0]:.1f}-{q[2]:.1f});  P(widespread by 2028/2030/2032) =",
          p, flush=True)
res["tool_class"] = tool_res

ref = json.load(open(RESULTS / "c06_attacker_lag.json"))
assert res["charted"]["business_model_median_years"] == ref["class_median_years"]["eco"], "charted row differs from Chart 6"
assert res["charted"]["p_agentic_widespread_by"] == ref["p_agentic_scaled_by"], "charted row differs from Chart 6"
assert tool_res["charted"]["tool_class_median_years"] == ref["class_median_years"]["tool"], "charted tool row differs from Chart 6"
assert tool_res["charted"]["p_agentic_widespread_by_if_tool"] == ref["p_agentic_scaled_by_if_tool"], "charted tool row differs from Chart 6"
print("the charted rows reproduce results/c06_attacker_lag.json")
dump_json(res, RESULTS / "sensitivity_c06.json")
