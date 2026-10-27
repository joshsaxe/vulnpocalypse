"""Chart 1 model: global losses to cyber-enabled fraud and to hacking, 2005-2025, and the part caused by AI.

Three steps, each simple on its own.

1. SHAPE. Loss series published by police, regulators, banks and blockchain analysts are each a noisy, partial view
   of the same underlying trend. A one-factor dynamic model (dfm.gibbs_dfm_drift) pools them: on the log scale,
   series s in year t = its own level + its own slow reporting drift + the shared trend + noise. The shared trend
   is smooth (its growth rate can change a little each year). Definition breaks (IC3 in 2010, the FTC in 2015 and
   2017) start a new series; Japan's narrower pre-2010 series is dropped (its 2009 collapse reflects a change of
   definition and new bank controls, not a fall in fraud elsewhere). Fraud is modelled separately for America, where the data are
   richest, and for the rest of the world; hacking is one global trend.

2. LEVEL. The model above says how losses changed, not how big they are, because every published series is a
   floor (most victims never report). The 2025 level comes from a separate triangulation (the author's earlier
   study): fraud $220bn (90% interval 105-461), hacking $76bn (31-188), built from national statistics grossed up
   for under-reporting, bottom-up costings and two global surveys. America is taken to be about 42% (32-52%) of
   2025 fraud losses.

3. DRIFT THAT HITS EVERY SERIES. If more victims report each year everywhere, every series rises faster than true
   losses and step 1 cannot tell. We therefore assume reporting rates rose by a common amount each year -
   America's complaint portals 2% a year (sd 2 points), other countries' series 1% (sd 1.5), hacking series 1%
   (sd 2) - and subtract it. This makes earlier years larger and their uncertainty wider.

AI. The share of each year's losses that would not have happened without AI cannot be read off the loss data (an
effect of a few per cent is far inside the noise), so it is a structural Monte Carlo built from direct evidence
(data/A1_fraud_ai_evidence.csv, data/A2_hacking_ai_evidence.csv);
see AI_PARAMS below:
    share(2025) = noticed x but-for(noticed) + unnoticed x but-for(unnoticed)
- noticed: share of dollars in FBI IC3 complaints that mention AI (2025: about 4.2% of fraud-type dollars, 1.4% of
  hacking-type dollars), 80% range 2.5-7% and 0.7-2.8%;
- but-for(noticed): how much of that would not have happened without AI, mean 25% (80% range 8-55%), because most
  is investment fraud in which an 'AI trading bot' is only the lure;
- unnoticed: losses where AI was used but victims could not tell (Verizon: about 10% of malicious e-mail had
  AI-written text; IBM: attackers used AI in 16-25% of studied breaches), mean 10% for fraud and 20% for hacking;
- but-for(unnoticed): small (fraud mean 8%, hacking 3%), because phishing's success did not rise as AI text spread.
Earlier years scale the 2025 share by an adoption index (2024 about half of 2025, 2023 about a quarter). Result:
about 1.6% of 2025 fraud losses (80% range 0.4-5.3%) and 0.8% of hacking losses (0.2-3.8%). As a check, both trend models
are refitted on data to 2022 only and projected forward: if AI had driven a surge, 2023-25 losses would sit above
that projection (they sit below it, with probability 0.84 for fraud and 0.74 for hacking).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from scipy import stats, optimize
from common.dfm import gibbs_dfm_drift, forecast_from
from common.deflators import to_2025_prices

YEARS = np.arange(2005, 2026)
T = len(YEARS)
RNG = np.random.default_rng(2025)
N_DRAWS = 6000

A1 = pd.read_csv(DATA / "A1_fraud_series.csv")


def a1(sid):
    d = A1[A1.series_id == sid][["year", "value"]].copy()
    d["year"] = d.year.astype(int)
    return d.groupby("year").value.first()


def row(values: pd.Series, country, y0=None, y1=None):
    """Return a length-T array of log real values (np.nan where missing)."""
    out = np.full(T, np.nan)
    v = values.dropna()
    v = v[(v.index >= (y0 or 0)) & (v.index <= (y1 or 9999)) & (v.index >= 2005)]
    real = to_2025_prices(v.values, v.index.values, country)
    for yr, r in zip(v.index.values, real):
        out[yr - 2005] = np.log(r)
    return out


# ------------------------------------------------------------------------------------------------ fraud series
def fraud_series():
    tot = a1("US_IC3_TOTAL_LOSS")
    F, H, O = a1("US_IC3_FRAUD_TYPE_LOSS"), a1("US_IC3_HACKING_TYPE_LOSS"), a1("US_IC3_OTHER_TYPE_LOSS")
    share = (F / (F + H + O)).dropna()            # category rows are multi-coded before 2023: use shares
    ic3_fraud = tot.copy()
    for y in ic3_fraud.index:
        ic3_fraud[y] = tot[y] * (share[y] if y in share.index else share[2015])
    ftc = a1("US_FTC_SENTINEL_FRAUD_LOSS")
    us = {
        "IC3 complaints referred to police, 2005-09": row(tot, "US", 2005, 2009),
        "IC3 fraud-type losses, 2011-25": row(ic3_fraud, "US", 2011, 2025),
        "FTC Consumer Sentinel, 2005-14": row(ftc, "US", 2005, 2014),
        "FTC Consumer Sentinel, 2015-16": row(ftc, "US", 2015, 2016),
        "FTC Consumer Sentinel, 2017-25": row(ftc, "US", 2017, 2025),
    }
    chain = pd.Series({2021: 10.9, 2022: 5.9, 2024: 12.0, 2025: 17.0})  # latest vintages; 2025 = Chainalysis' projection
    sepa = a1("SEPA_CARD_FRAUD_VALUE")
    row_ = {
        "UK Finance unauthorised fraud, 2013-25": row(a1("UK_FIN_UNAUTH_LOSS"), "GB"),
        "UK Finance push-payment scams, 2020-25": row(a1("UK_FIN_APP_LOSS"), "GB"),
        "Australia Scamwatch, 2009-25": row(a1("AU_SCAMWATCH_LOSS"), "AU"),
        "Japan special fraud, 2010-25": row(a1("JP_SPECIAL_FRAUD_LOSS"), "JP", 2010, 2025),
        "Canada Anti-Fraud Centre, 2020-25": row(a1("CA_CAFC_REPORTED_LOSS"), "CA"),
        "Singapore Police Force, 2018-25": row(a1("SG_SCAM_LOSS"), "SG"),
        "Hong Kong Police deception, 2024-25": row(a1("HK_DECEPTION_LOSS"), "HK"),
        "EBA/ECB payment fraud, EEA, 2022-24": row(a1("EEA_PAYMENT_FRAUD_VALUE"), "EA"),
        "ECB card fraud, SEPA, 2013-19": row(sepa, "EA"),
        "Chainalysis crypto-scam revenue, 2021-25": row(chain, "US"),
    }
    return us, row_


def fit(series: dict, seed, upto=None, n_iter=9000, n_burn=3000):
    names = list(series)
    Y = np.vstack([series[k] for k in names])
    if upto is not None:
        Y = Y.copy()
        Y[:, YEARS > upto] = np.nan
        keep = ~np.all(np.isnan(Y), axis=1) & (np.sum(~np.isnan(Y), axis=1) >= 1)
        Y = Y[keep]
        names = [n for n, k in zip(names, keep) if k]
    ref = int(np.argmax(np.sum(~np.isnan(Y), axis=1)))
    out = gibbs_dfm_drift(Y, YEARS, ref=ref, drift_sd=0.03, n_iter=n_iter, n_burn=n_burn, seed=seed,
                          sigma_prior=[(3.0, 3.0 * 0.2 ** 2)] * Y.shape[0], tau_prior=(2.0, 0.02))
    out["names"] = names
    out["Y"] = Y
    return out


def thin(a, n=N_DRAWS):
    idx = np.linspace(0, len(a) - 1, n).astype(int)
    return a[idx]


def lognormal(median, lo90, hi90, n):
    sd = (np.log(hi90) - np.log(lo90)) / (2 * 1.645)
    return np.exp(RNG.normal(np.log(median), sd, n))


def beta_q(lo, mid, hi, p=0.90):
    """Beta(a,b) matching 5th/50th/95th percentiles (p=0.9) on the log scale (good for small shares)."""
    qs = np.array([0.5 - p / 2, 0.5, 0.5 + p / 2])
    tgt = np.log([lo, mid, hi])

    def loss(v):
        a, b = np.exp(v)
        return np.sum((np.log(stats.beta.ppf(qs, a, b) + 1e-12) - tgt) ** 2)
    best = min((optimize.minimize(loss, np.log([mid * s, (1 - mid) * s]), method="Nelder-Mead",
                                  options={"xatol": 1e-8, "fatol": 1e-12, "maxiter": 5000})
                for s in (5, 20, 80)), key=lambda r: r.fun)
    return tuple(np.exp(best.x))


def rel(x):
    """Trend relative to 2025 (log)."""
    return x - x[:, [-1]]


def common_drift(mean, sd, n):
    return RNG.normal(mean, sd, n)


def run_fraud():
    us, row_ = fraud_series()
    fu = fit(us, seed=11)
    fr = fit(row_, seed=12)
    n = N_DRAWS
    rUS, rRW = thin(rel(fu["x"])), thin(rel(fr["x"]))
    dUS, dRW = common_drift(0.02, 0.02, n), common_drift(0.01, 0.015, n)
    yrs = YEARS - 2025
    corrUS = rUS - dUS[:, None] * yrs[None, :]
    corrRW = rRW - dRW[:, None] * yrs[None, :]
    F25 = lognormal(220, 105, 461, n)
    a, b = optimize.brentq(lambda k: stats.beta.ppf(0.1, 0.42 * k, 0.58 * k) - 0.32, 2, 2000), None
    k = a
    sUS = RNG.beta(0.42 * k, 0.58 * k, n)
    fraud = F25[:, None] * (sUS[:, None] * np.exp(corrUS) + (1 - sUS[:, None]) * np.exp(corrRW))
    # ---- pre-ChatGPT check: refit on data to 2022 and project 2023-25
    fu22, fr22 = fit(us, seed=21, upto=2022), fit(row_, seed=22, upto=2022)
    i22 = 2022 - 2005
    gUS = forecast_from(thin(fu22["x"]), i22, 3, thin(fu22["tau"]), rng=np.random.default_rng(5)) - \
        thin(fu22["x"])[:, [i22]]
    gRW = forecast_from(thin(fr22["x"]), i22, 3, thin(fr22["tau"]), rng=np.random.default_rng(6)) - \
        thin(fr22["x"])[:, [i22]]
    # dollars: start from the full-model 2022 values of each component
    us22 = F25 * sUS * np.exp(corrUS[:, i22])
    rw22 = F25 * (1 - sUS) * np.exp(corrRW[:, i22])
    proj = us22[:, None] * np.exp(gUS - dUS[:, None] * np.arange(1, 4)) + \
        rw22[:, None] * np.exp(gRW - dRW[:, None] * np.arange(1, 4))
    # ---- one-year projection to 2026 (a projected column; the pre-2022 check's machinery, one step from 2025)
    xUS, xRW = thin(fu["x"]), thin(fr["x"])
    g26US = forecast_from(xUS, 20, 1, thin(fu["tau"]), rng=np.random.default_rng(15))[:, 0] - xUS[:, 20]
    g26RW = forecast_from(xRW, 20, 1, thin(fr["tau"]), rng=np.random.default_rng(16))[:, 0] - xRW[:, 20]
    fraud26 = (F25 * sUS * np.exp(corrUS[:, -1])) * np.exp(g26US - dUS) + \
        (F25 * (1 - sUS) * np.exp(corrRW[:, -1])) * np.exp(g26RW - dRW)
    return {"fraud": fraud, "proj": proj, "fraud26": fraud26, "fit_us": fu, "fit_row": fr, "sUS": sUS, "F25": F25,
            "us_names": fu["names"], "row_names": fr["names"]}


A2 = pd.read_csv(DATA / "A2_hacking_series.csv")


def a2(sid):
    d = A2[A2.series_id == sid][["year", "value"]].copy()
    d = d[d.year.astype(str).str.fullmatch(r"\d{4}")]
    d["year"] = d.year.astype(int)
    return d.groupby("year").value.first() / 1e9          # USD bn (counts are left as counts / 1e9; level-free)


def hack_series():
    """Global hacking-loss indicators (all in US$, deflated with US CPI). Counts enter as volume indices."""
    chain = a2("CHAINALYSIS_RANSOMWARE_LATEST").copy()
    chain[2025] = 0.90          # Chainalysis expects 2025 to 'approach or exceed $900m' once attribution catches up
    itrc, ibm = a2("ITRC_DATA_COMPROMISES"), a2("IBM_CODB_GLOBAL_AVG")
    breach = (itrc * ibm).dropna()
    hit, rec = a2("SOPHOS_SHARE_HIT"), a2("SOPHOS_MEAN_RECOVERY_COST")
    soph = (hit * rec).dropna()
    fincen = pd.Series({2022: 0.62, 2023: 1.10, 2024: 0.734})
    theft = a2("CHAINALYSIS_STOLEN_FUNDS")
    theft = theft[theft.index >= 2020]                      # 2018 is a lower bound only
    return {
        "IC3 ransomware, data-breach and malware losses, 2015-25": row(a2("IC3_HACKING_CORE_DERIVED"), "US"),
        "Chainalysis ransomware payments (latest estimates), 2020-25": row(chain, "US"),
        "Chainalysis ransomware payments (Jan 2021 estimates), 2019-20": row(a2("CHAINALYSIS_RANSOMWARE_VINTAGE_2021"),
                                                                              "US"),
        "FinCEN ransomware payments, 2022-24": row(fincen, "US"),
        "Chainalysis crypto stolen in hacks, 2020-25": row(theft, "US"),
        "ITRC breach notices x IBM cost per breach, 2018-25": row(breach, "US"),
        "Sophos share of firms hit x recovery cost, 2019-23": row(soph, "US"),
        "Ransomware leak-site victims (count), 2023-25": row(a2("RANSOMWARE_LIVE_LEAKSITE_VICTIMS"), "US", 2023, 2025),
    }


def run_hack():
    hs = hack_series()
    fh = fit(hs, seed=31)
    n = N_DRAWS
    yrs = YEARS - 2025
    dH = common_drift(0.01, 0.02, n)
    corr = thin(rel(fh["x"])) - dH[:, None] * yrs[None, :]
    H25 = lognormal(76, 31, 188, n)
    hack = H25[:, None] * np.exp(corr)
    fh22 = fit(hs, seed=32, upto=2022)
    i22 = 2022 - 2005
    g = forecast_from(thin(fh22["x"]), i22, 3, thin(fh22["tau"]), rng=np.random.default_rng(8)) - \
        thin(fh22["x"])[:, [i22]]
    proj = hack[:, [i22]] * np.exp(g - dH[:, None] * np.arange(1, 4))
    xH = thin(fh["x"])
    g26 = forecast_from(xH, 20, 1, thin(fh["tau"]), rng=np.random.default_rng(18))[:, 0] - xH[:, 20]
    hack26 = (H25 * np.exp(corr[:, -1])) * np.exp(g26 - dH)
    first = int(min(np.where(~np.isnan(v))[0].min() for v in hs.values()))
    return {"hack": hack, "proj": proj, "hack26": hack26, "fit": fh, "names": fh["names"],
            "first_year": int(YEARS[first]), "H25": H25}


# ---------------------------------------------------------------- AI's share: a structural Monte Carlo
# share(2025) = noticed x but-for(noticed) + unnoticed x but-for(unnoticed)
#   noticed   = share of losses in complaints that mention AI (IC3 2025: 4.2% of fraud-type dollars, 1.4% of
#               hacking-type dollars), allowed to differ abroad
#   but-for(noticed)   = how much of that would not have happened without AI (most is investment fraud in which
#               'AI trading bots' are only the lure; deepfaked bosses and cloned voices are the genuine novelty)
#   unnoticed = losses where AI was used but victims could not tell (Verizon: ~10% of malicious e-mail had
#               AI-written text; IBM: attackers used AI in 16-25% of studied breaches)
#   but-for(unnoticed) = small, because phishing success did not rise (Verizon) and AI-written lures only match
#               human experts in experiments (Heiding et al.)
# Earlier years scale 2025 by an adoption index (2024 about half of 2025, 2023 about a quarter).
AI_PARAMS = {
    "fraud": {"noticed": (0.042, 0.025, 0.07), "bf_noticed": (0.25, 0.08, 0.55),
              "unnoticed": (0.10, 0.04, 0.25), "bf_unnoticed": (0.08, 0.02, 0.25)},
    "hack": {"noticed": (0.014, 0.007, 0.028), "bf_noticed": (0.25, 0.08, 0.55),
             "unnoticed": (0.20, 0.10, 0.35), "bf_unnoticed": (0.03, 0.01, 0.10)},
}
ADOPTION = {2023: (0.25, 0.10, 0.45), 2024: (0.50, 0.30, 0.70), 2025: (1.0, 1.0, 1.0)}


def beta_mq(mean, lo, hi, p=0.8):
    """Beta with the given mean whose central p-interval best matches (lo, hi)."""
    def loss(logk):
        k = np.exp(logk)
        a, b = mean * k, (1 - mean) * k
        ql, qh = stats.beta.ppf([(1 - p) / 2, (1 + p) / 2], a, b)
        return (np.log(ql) - np.log(lo)) ** 2 + (np.log(qh) - np.log(hi)) ** 2
    r = optimize.minimize_scalar(loss, bounds=(np.log(1.0), np.log(5000)), method="bounded")
    k = np.exp(r.x)
    return mean * k, (1 - mean) * k


# The but-for fractions and the unnoticed shares are judgements, so the estimate averages three sets of them with
# equal weight: the central set above, a sceptical set (AI rarely decisive) and a generous set (AI often decisive).
AI_SPECS = {
    "central": AI_PARAMS,
    "sceptical": {
        "fraud": {**AI_PARAMS["fraud"], "bf_noticed": (0.10, 0.03, 0.25), "bf_unnoticed": (0.03, 0.01, 0.10)},
        "hack": {**AI_PARAMS["hack"], "bf_noticed": (0.10, 0.03, 0.25), "bf_unnoticed": (0.01, 0.003, 0.04)}},
    "generous": {
        "fraud": {**AI_PARAMS["fraud"], "bf_noticed": (0.50, 0.25, 0.75), "unnoticed": (0.15, 0.06, 0.35),
                  "bf_unnoticed": (0.15, 0.05, 0.35)},
        "hack": {**AI_PARAMS["hack"], "bf_noticed": (0.50, 0.25, 0.75), "unnoticed": (0.30, 0.15, 0.50),
                 "bf_unnoticed": (0.08, 0.02, 0.20)}},
}


def _ai_share_one(P, n):
    m, lo, hi = P["noticed"]
    noticed = np.exp(RNG.normal(np.log(m), (np.log(hi) - np.log(lo)) / (2 * 1.2816), n))
    draws = {}
    for k_ in ("bf_noticed", "unnoticed", "bf_unnoticed"):
        a, b = beta_mq(*P[k_])
        draws[k_] = RNG.beta(a, b, n)
    s25 = noticed * draws["bf_noticed"] + draws["unnoticed"] * draws["bf_unnoticed"]
    return s25, {"noticed": noticed, **draws}


def ai_share(kind, n):
    """Equal mixture over AI_SPECS; returns n x T shares (0 before 2023) and the 2025 component draws."""
    k = len(AI_SPECS)
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    parts, s25 = [], []
    for (name, spec), m in zip(AI_SPECS.items(), sizes):
        s, d = _ai_share_one(spec[kind], m)
        s25.append(s)
        parts.append(d)
    s25 = np.concatenate(s25)
    comp = {key: np.concatenate([d[key] for d in parts]) for key in parts[0]}
    perm = RNG.permutation(n)
    s25 = s25[perm]
    comp = {key: v[perm] for key, v in comp.items()}
    out = np.zeros((n, T))
    for yr, (mean, lo, hi) in ADOPTION.items():
        if yr == 2025:
            adopt = np.ones(n)
        else:
            a, b = beta_mq(mean, lo, hi)
            adopt = RNG.beta(a, b, n)
        out[:, yr - 2005] = s25 * adopt
    return out, comp


def qs(a, p=(0.1, 0.5, 0.9)):
    return np.quantile(a, p, axis=0)


def run_all():
    rf, rh = run_fraud(), run_hack()
    n = N_DRAWS
    sF, partsF = ai_share("fraud", n)
    sH, partsH = ai_share("hack", n)
    F, H = rf["fraud"], rh["hack"]
    aiF, aiH = F * sF, H * sH
    i15 = 2015 - 2005
    tot = F[:, i15:] + H[:, i15:]
    aitot = aiF[:, i15:] + aiH[:, i15:]
    # ---- 2026 projected column: one-year forecast of each component, with AI adoption extended past 2025
    f26, h26 = rf["fraud26"], rh["hack26"]
    adopt26 = lognormal(1.4, 1.0, 2.0, n)                 # 2026 AI adoption vs 2025 (median 1.4x, 90% range 1.0-2.0)
    sF26 = np.clip(sF[:, -1] * adopt26, 0.0, 0.9)
    sH26 = np.clip(sH[:, -1] * adopt26, 0.0, 0.9)
    aiF26, aiH26 = f26 * sF26, h26 * sH26
    tot26, aitot26 = f26 + h26, aiF26 + aiH26
    q3 = lambda a: [round(float(v), 4) for v in np.quantile(a, [0.1, 0.5, 0.9])]
    res = {
        "years": YEARS.tolist(),
        "fraud_q": np.quantile(F, [0.1, 0.5, 0.9], axis=0).round(2).tolist(),
        "hack_q": np.quantile(H, [0.1, 0.5, 0.9], axis=0).round(2).tolist(),
        "hack_first_year": rh["first_year"],
        "ai_fraud_q": np.quantile(aiF, [0.1, 0.5, 0.9], axis=0).round(3).tolist(),
        "ai_hack_q": np.quantile(aiH, [0.1, 0.5, 0.9], axis=0).round(3).tolist(),
        "share_fraud_2025": q3(sF[:, -1]), "share_hack_2025": q3(sH[:, -1]),
        "share_fraud_2024": q3(sF[:, -2]), "share_hack_2024": q3(sH[:, -2]),
        "share_fraud_2023": q3(sF[:, -3]), "share_hack_2023": q3(sH[:, -3]),
        "total_2025": q3(tot[:, -1]), "ai_total_2025": q3(aitot[:, -1]),
        "ai_share_total_2025": q3(aitot[:, -1] / tot[:, -1]),
        "fraud_2026": q3(f26), "hack_2026": q3(h26), "total_2026": q3(tot26),
        "ai_fraud_2026": q3(aiF26), "ai_hack_2026": q3(aiH26), "ai_total_2026": q3(aitot26),
        "ai_share_total_2026": q3(aitot26 / tot26),
        "share_fraud_2026": q3(sF26), "share_hack_2026": q3(sH26),
        "fraud_growth_05_25": q3(F[:, -1] / F[:, 0]), "fraud_growth_15_25": q3(F[:, -1] / F[:, 10]),
        "fraud_growth_17_22_pa": q3((F[:, 17] / F[:, 12]) ** (1 / 5) - 1),
        "fraud_growth_22_25_pa": q3((F[:, -1] / F[:, 17]) ** (1 / 3) - 1),
        "hack_growth_15_25": q3(H[:, -1] / H[:, 10]),
        "hack_growth_17_22_pa": q3((H[:, 17] / H[:, 12]) ** (1 / 5) - 1),
        "hack_growth_22_25_pa": q3((H[:, -1] / H[:, 17]) ** (1 / 3) - 1),
        "fraud_growth_15_19_pa": q3((F[:, 14] / F[:, 10]) ** (1 / 4) - 1),
        "fraud_growth_19_22_pa": q3((F[:, 17] / F[:, 14]) ** (1 / 3) - 1),
        "hack_growth_15_19_pa": q3((H[:, 14] / H[:, 10]) ** (1 / 4) - 1),
        "hack_growth_19_22_pa": q3((H[:, 17] / H[:, 14]) ** (1 / 3) - 1),
        "p_hack_slower_22_25_vs_17_22": round(float(np.mean((H[:, -1] / H[:, 17]) ** (1 / 3) < (H[:, 17] / H[:, 12]) ** (1 / 5))), 3),
        "p_hack_under_half_22_25_vs_17_22": round(float(np.mean(((H[:, -1] / H[:, 17]) ** (1 / 3) - 1) < 0.5 * ((H[:, 17] / H[:, 12]) ** (1 / 5) - 1))), 3),
        "p_fraud_slower_22_25_vs_19_22": round(float(np.mean((F[:, -1] / F[:, 17]) ** (1 / 3) < (F[:, 17] / F[:, 14]) ** (1 / 3))), 3),
        "p_fraud_faster_22_25_vs_15_19": round(float(np.mean((F[:, -1] / F[:, 17]) ** (1 / 3) > (F[:, 14] / F[:, 10]) ** (1 / 4))), 3),
        "p_ai_share_total_2025_below_5pc": round(float(np.mean(aitot[:, -1] / tot[:, -1] < 0.05)), 3),
        "p_ai_share_total_2025_below_1pc": round(float(np.mean(aitot[:, -1] / tot[:, -1] < 0.01)), 3),
        "ai_hack_2023_25_sum": q3(aiH[:, -3:].sum(1)),
        "ai_specs": list(AI_SPECS),
        "fraud_proj_q": np.quantile(rf["proj"], [0.1, 0.5, 0.9], axis=0).round(2).tolist(),
        "hack_proj_q": np.quantile(rh["proj"], [0.1, 0.5, 0.9], axis=0).round(2).tolist(),
        "fraud_actual_over_pretrend_2025": q3(F[:, -1] / rf["proj"][:, -1]),
        "p_fraud_below_pretrend": round(float(np.mean(F[:, -1] < rf["proj"][:, -1])), 3),
        "hack_actual_over_pretrend_2025": q3(H[:, -1] / rh["proj"][:, -1]),
        "p_hack_below_pretrend": round(float(np.mean(H[:, -1] < rh["proj"][:, -1])), 3),
        "fraud_pretrend_2025": q3(rf["proj"][:, -1]), "hack_pretrend_2025": q3(rh["proj"][:, -1]),
        "us_share_2025": q3(rf["sUS"]),
        "series": {"fraud_us": rf["us_names"], "fraud_row": rf["row_names"], "hack": rh["names"]},
        "n_series": len(rf["us_names"]) + len(rf["row_names"]) + len(rh["names"]),
        "sigma": {"fraud_us": dict(zip(rf["us_names"], np.median(rf["fit_us"]["sigma"], 0).round(3).tolist())),
                  "fraud_row": dict(zip(rf["row_names"], np.median(rf["fit_row"]["sigma"], 0).round(3).tolist())),
                  "hack": dict(zip(rh["names"], np.median(rh["fit"]["sigma"], 0).round(3).tolist()))},
        "ai_parts_fraud": {k: q3(v) for k, v in partsF.items()},
        "ai_parts_hack": {k: q3(v) for k, v in partsH.items()},
    }
    np.savez_compressed(RESULTS / "c01_loss_trend_draws.npz", fraud=F, hack=H, aiF=aiF, aiH=aiH,
                        projF=rf["proj"], projH=rh["proj"], fraud26=f26, hack26=h26, aiF26=aiF26, aiH26=aiH26)
    dump_json(res, RESULTS / "c01_loss_trend.json")
    return res


if __name__ == "__main__":
    res = run_all()
    skip = {"fraud_q", "hack_q", "ai_fraud_q", "ai_hack_q", "series", "sigma"}
    for k, v in res.items():
        if k not in skip:
            print(k, v)
    print("series", res["series"])
    print("sigma", res["sigma"])
