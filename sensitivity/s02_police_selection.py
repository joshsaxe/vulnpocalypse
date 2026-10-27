"""Chart 2 robustness: how many enterprises missing from the table would stop police being the majority?

Chart 2 can count only enterprises that were documented, and police actions come with press releases, indictments and
court filings, while an exit scam or a quiet retirement often does not. The chart's note says so ("shares flatter the
police"); this script puts a number on it.

Let R be how many times more likely an enterprise that police ended is to be in the table than one that closed some other
way (R = 1: no gap). If the table holds k police endings and m other closures, and every police ending is in it, the true
counts are about k and m R, so the true police share is k / (k + R m) and the table is missing about m (R - 1) of the other
closures (at least that many, if some police endings are missing too). The script gives that share, with the chart's own
beta-binomial interval (the observed share's Beta(1 + k, 1 + m) posterior, rescaled by R), for a range of R, and finds the R at
which police stop being the majority. Then smaller checks, none of which uses R: (1) the 20 enterprises still running;
(2) how many rows would have to be classed differently; (3) a stricter meaning of "ended by police"; (4) for each sector,
the chance that police ended a majority, how many rows would change that, and how many enterprises are still running;
(5) the 27 police endings that share nine end dates (coordinated takedowns), which the interval treats as independent.

Everything is exact (beta quantiles; no random numbers). The 'charted' share must reproduce results/c02_police.json; the
script stops if it does not. Runs in a second.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from scipy import stats
from common.paths import DATA, RESULTS, dump_json

d = pd.read_csv(DATA / "B_enterprise_lifespans.csv")
GROUP = {"botnet_maas": "Botnets and malware services", "forum": "Hacking and carding forums",     # as charts/c02_police.py
         "mixer_laundering": "Money-laundering services", "darknet_market": "Darknet markets",
         "ransomware": "Ransomware brands"}
d["group"] = d.sector.map(GROUP).fillna("Other criminal services*")
POLICE = {"le_takedown", "le_seizure", "le_arrests", "sanctions", "rebrand_after_le_pressure"}   # what the chart counts
STRICT = {"le_takedown", "le_seizure", "le_arrests"}        # arrests, takedowns and seizures only
closed = d[d.end_type != "still_active"]
n_active = int((d.end_type == "still_active").sum())
k = int(closed.end_type.isin(POLICE).sum())                 # ended by police
n = len(closed)                                             # closed
m = n - k                                                   # closed some other way
r3 = lambda x: round(float(x), 3)
r4 = lambda x: round(float(x), 4)          # the numbers stored in the results file
odds = lambda p: p / (1 - p)


def beta_q(k_, m_, ps=(0.1, 0.5, 0.9)):
    """10th, 50th and 90th percentiles of the police share under a uniform prior (what the chart reports)."""
    return [float(stats.beta.ppf(p, 1 + k_, 1 + m_)) for p in ps]


def share_given_gap(theta, R):
    """True police share when the observed share is theta and police endings are R times as likely to be documented."""
    return theta / (theta + (1 - theta) * R)


# ---- the chart's own numbers must come back
ref = json.load(open(RESULTS / "c02_police.json"))
charted = [round(x, 3) for x in beta_q(k, m)]
assert (k, n) == (ref["all"]["police_any"], ref["all"]["ended"]), "counts differ from Chart 2"
assert charted == ref["all"]["police_share_of_ended_q"], "charted share differs from Chart 2"
for g, sub in closed.groupby("group"):
    kg = int(sub.end_type.isin(POLICE).sum())
    assert [round(x, 3) for x in beta_q(kg, len(sub) - kg)] == ref["by_group"][g]["police_share_of_ended_q"], g
print("the charted shares reproduce results/c02_police.json")
print(f"closed {n}: ended by police {k}, otherwise {m}; still running {n_active}")

# ---- 1. the documentation gap
t10, t50, t90 = beta_q(k, m)
grid = []
for R in (1, 1.5, 2, 3, 4, 6, 10):
    lo, med, hi = (share_given_gap(t, R) for t in (t10, t50, t90))
    p_majority = 1 - stats.beta.cdf(R / (1 + R), 1 + k, 1 + m)       # P(police share > 1/2 | R)
    grid.append({"R": R, "other_closures_missing_at_least": round(m * (R - 1)), "police_share_q": [r4(lo), r4(med), r4(hi)],
                 "p_police_majority": r4(p_majority)})
tipping = {
    "R_majority_lost_at_observed_counts": r4(k / m),                  # k / (k + R m) = 1/2
    "other_closures_missing_at_least_then": k - m,                     # m (R - 1) at that R
    "missing_share_of_all_closures_then": r4((k - m) / (n + k - m)),
    "R_median_share_is_half": r4(odds(t50)),
    "R_90pct_sure_of_majority_below": r4(odds(t10)),
    "R_10pct_sure_of_majority_above": r4(odds(t90)),
    "R_median_share_is_two_thirds": r4(odds(t50) / 2),
    "R_median_share_is_three_quarters": r4(odds(t50) / 3),
}
print("\ndocumentation gap R (police endings R times as likely to be documented): police share, median (80% interval)")
for g_ in grid:
    lo, med, hi = g_["police_share_q"]
    print(f"  R = {g_['R']:>4}: missing at least {g_['other_closures_missing_at_least']:>3} other closures   {med:.1%} ({lo:.1%}-{hi:.1%})"
          f"   P(majority) {g_['p_police_majority']:.2f}")
print("  tipping points:", tipping)

# ---- 2. the 20 enterprises still running (right-censoring, not selection)
still = {}
for name, (kk, mm) in {"all_end_quietly": (k, m + n_active), "all_end_by_police": (k + n_active, m)}.items():
    still[name] = {"police_share_of_all_152": r4(kk / (kk + mm)), "police_share_q": [r4(x) for x in beta_q(kk, mm)]}
print("\nstill running:", still)

# ---- 3. classification
strict_k = int(closed.end_type.isin(STRICT).sum())
classification = {
    "police_endings_that_would_have_to_be_other_for_no_majority": k - n // 2,          # (k - x) / n <= 1/2
    "police_endings_that_would_have_to_be_other_for_under_two_thirds": k - int(np.ceil(2 * n / 3)) + 1,   # (k - x) / n < 2/3
    "strict_police_endings": strict_k,
    "strict_police_share_q": [r4(x) for x in beta_q(strict_k, n - strict_k)],
    "strict_police_share_point": r4(strict_k / n),
}
print("\nclassification:", classification)

# ---- 4. sectors
sectors = {}
for g, sub in d.groupby("group"):
    cl = sub[sub.end_type != "still_active"]
    kg, ng, tot = int(cl.end_type.isin(POLICE).sum()), len(cl), len(sub)
    running = tot - ng
    a_, b_ = 1 + kg, 1 + ng - kg
    # rows to reclassify to change the verdict: so that police ended half or fewer if they ended most, more than half if not
    change = (kg - ng // 2) if kg > ng / 2 else (ng // 2 + 1 - kg)
    need = max(0, tot // 2 + 1 - kg)          # of those still running, how many would have to end by police for police to end most of all
    sectors[g] = {"closed": ng, "police": kg, "still_running": running, "police_share_q": [r4(x) for x in beta_q(kg, ng - kg)],
                  "p_police_majority": r4(1 - stats.beta.cdf(0.5, a_, b_)),
                  "R_median_share_is_half": r4(odds(float(stats.beta.ppf(0.5, a_, b_)))),
                  "rows_to_reclassify_to_change_the_verdict": change,
                  "running_that_would_have_to_end_by_police_for_most_of_all": need if need <= running else None}
print("\nsectors (R below 1 means police endings would have to be LESS documented than the others for police to reach half):")
for g, s_ in sorted(sectors.items(), key=lambda kv: -kv[1]["police_share_q"][1]):
    print(f"  {g:32s} {s_['police']:>2}/{s_['closed']:<3} median {s_['police_share_q'][1]:.3f}  P(majority) {s_['p_police_majority']:.2f}"
          f"  R* {s_['R_median_share_is_half']:>7}  rows to change {s_['rows_to_reclassify_to_change_the_verdict']:>2}"
          f"  running {s_['still_running']:>2} (police must end {s_['running_that_would_have_to_end_by_police_for_most_of_all']})")

# ---- 5. coordinated takedowns: police endings that share an end date are not independent draws
full = closed[closed.end_type.isin(POLICE)].end_date.dropna()
full = full[full.str.len() == 10]                       # dated to the day (month and year dates cannot show a shared day)
shared = full[full.duplicated(keep=False)]
k_events = k - len(shared) + shared.nunique()           # each shared day counted once
clustering = {"police_endings_dated_to_the_day": len(full), "on_a_day_shared_with_another_police_ending": len(shared),
              "shared_days": int(shared.nunique()),
              "each_shared_day_counted_once": {"police": k_events, "other": m, "police_share_q": [r4(x) for x in beta_q(k_events, m)],
                                               "R_majority_lost": r4(k_events / m)}}
print("\ncoordinated takedowns:", clustering)

res = {"charted": {"closed": n, "police": k, "other": m, "still_running": n_active, "police_share_q": charted},
       "documentation_gap": {"grid": grid, "tipping_points": tipping},
       "still_running": still, "classification": classification, "sectors": sectors, "clustering": clustering}
dump_json(res, RESULTS / "sensitivity_c02.json")
