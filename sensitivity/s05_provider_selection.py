"""Chart 5 robustness: what the chart cannot see, and how many missing cases it would take to change the picture.

Chart 5 shows how long nine hacking, fraud and spying operations ran before an AI provider cut them off (41% within
30 days, 44% for 180 days or more). It can show only operations that a provider cut off AND whose report gives a duration.
Two kinds of missing operation matter, and they push in opposite directions:

  1. hidden QUICK catches: bans within 30 days that no report mentions (a short ban is easy to leave out of a threat
     report). They are what could overturn the chart. Q of them are added to the nine.
  2. hidden LONG cases: operations that ran 180 days or more before a cut-off that no report describes, or that have not
     been cut off yet. They can only add to the long end. H of them are added to the nine.

Every case added is counted with the chart's own method: the shares within 30 days and at 180 days or more are
beta-binomial (uniform prior) over the log-uniform durations. The chart gets them by Monte Carlo. Here the Monte Carlo is
replaced by the distribution it samples from (the number of cases within 30 days, or at 180 days or more, is a sum of
independent yes-or-no outcomes with known odds), so the tipping points are exact, with no sampling noise. A threshold is where
the posterior MEDIAN of a share crosses a line; the script also says where the LOW END of the 80% interval does. Then it gives
3. what the chart cannot say about how often providers catch abuse at all, 4. how many of the table's provider cut-offs give
a duration, and how the nine split by provider, 5. which cases carry the shares (each case left out in turn, and two groups of
cases whose 'duration' is not a time to cut-off), and 6. the shares if every cut-off in the table with a stated duration is
used. The 'charted' shares must reproduce results/c05_inference.json; the script stops if they do not. Runs in a few seconds.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import brentq
from common.paths import DATA, RESULTS, dump_json

# ---- the chart's cases and model, exactly as charts/c05_inference.py (case, lower bound, upper bound in days)
CAUGHT = [("ANT-2026-09-GTG50020", 4, 26), ("ANT-2025-08-GTG2002", 7, 30), ("ANT-2025-11-GTG1002", 10, 60),
          ("ANT-2026-09-GTG50014", 21, 21), ("ANT-2026-09-GTG50029", 30, 148), ("OAI-2025-04-AKIRABOT", 180, 225),
          ("MS-2026-09-EVILTOKENS", 213, 213), ("ANT-2025-08-GTG5004", 180, 225), ("SVC-XANTHOROX", 290, 315)]
D = pd.read_csv(DATA / "D_platform_cases.csv").set_index("case_id")
lo = np.array([c[1] for c in CAUGHT], float)
hi = np.array([c[2] for c in CAUGHT], float)
ex = np.isclose(lo, hi)
lo_i, hi_i = np.where(ex, lo * 0.8, lo), np.where(ex, hi * 1.2, hi)       # an exact duration is widened 20% each way
n, N = len(CAUGHT), 20000
rng = np.random.default_rng(44)
u = rng.uniform(size=(N, n))
dur = np.exp(np.log(lo_i) + u * (np.log(hi_i) - np.log(lo_i)))
k30, k180 = (dur <= 30).sum(1), (dur >= 180).sum(1)
s30 = rng.beta(1 + k30, 1 + n - k30)
s180 = rng.beta(1 + k180, 1 + n - k180)
q3 = lambda a: [round(float(v), 3) for v in np.quantile(a, [0.1, 0.5, 0.9])]
ref = json.load(open(RESULTS / "c05_inference.json"))
assert q3(s30) == ref["share_within_30d"] and q3(s180) == ref["share_180d_plus"], "charted shares differ from Chart 5"
print("the charted shares reproduce results/c05_inference.json:", q3(s30), q3(s180))
for c in CAUGHT:
    assert c[0] in D.index, c[0]

# ---- exact version of the same calculation: the shares are mixtures of betas over the counts k30 and k180
L_LO, L_HI = np.log(lo_i), np.log(hi_i)
P30 = np.clip((np.log(30) - L_LO) / (L_HI - L_LO), 0, 1)           # chance that each case was cut off within 30 days
P180 = np.clip((L_HI - np.log(180)) / (L_HI - L_LO), 0, 1)         # chance that each case ran 180 days or more
r4 = lambda x: round(float(x), 4)


def count_pmf(p):
    """Distribution of the number of 'yes' among independent yes-or-no outcomes with chances p."""
    pmf = np.array([1.0])
    for x in p:
        pmf = np.convolve(pmf, [1 - x, x])
    return pmf


# the chart's Monte Carlo draws from exactly these distributions
for p, k_ in ((P30, k30), (P180, k180)):
    assert np.abs(count_pmf(p) - np.bincount(k_, minlength=n + 1) / N).max() < 0.02, "Monte Carlo counts differ from the exact ones"


def mixture_q(pmf, a, b, ps=(0.1, 0.5, 0.9)):
    """Quantiles of a mixture of Beta(a(j), b(j)) with weights pmf[j]."""
    js = [j for j in range(len(pmf)) if pmf[j] > 1e-12]

    def cdf(x):
        return sum(pmf[j] * stats.beta.cdf(x, a(j), b(j)) for j in js)
    return [float(brentq(lambda x: cdf(x) - p, 1e-9, 1 - 1e-9)) for p in ps]


ALL = np.ones(n, bool)


def shares(keep=ALL, add_quick=0, add_long=0, add_other=0):
    """Shares within 30 days and at 180+ days (10th, 50th and 90th percentiles) for the cases in `keep` plus operations of
    known kind: add_quick quick catches (within 30 days), add_long long ones (180 days or more), add_other in between."""
    nn = int(keep.sum()) + add_quick + add_long + add_other
    return {"within_30d": mixture_q(count_pmf(P30[keep]), lambda j: 1 + j + add_quick, lambda j: 1 + nn - j - add_quick),
            "d180_plus": mixture_q(count_pmf(P180[keep]), lambda j: 1 + j + add_long, lambda j: 1 + nn - j - add_long), "n": nn}


rounded = lambda s: {"n": s["n"], "within_30d": [r4(x) for x in s["within_30d"]], "d180_plus": [r4(x) for x in s["d180_plus"]]}
pct = lambda s, key: f"{s[key][1]:.0%} ({s[key][0]:.0%}-{s[key][2]:.0%})"
base = shares()
assert all(abs(a - b) < 0.01 for a, b in zip(base["within_30d"] + base["d180_plus"], q3(s30) + q3(s180))), \
    "the exact shares should agree with the chart's Monte Carlo to within 0.01"
print("exact, as charted: within 30 days", pct(base, "within_30d"), " 180 days or more", pct(base, "d180_plus"))


def first(cond, kind, upto=200):
    """Smallest number of added operations of one kind for which cond(shares) holds."""
    for x in range(upto + 1):
        if cond(shares(**{kind: x})):
            return x
    return None


# ---- 1. hidden quick catches Q
quick_grid = []
for Q in (0, 2, 4, 6, 9, 12, 18):
    quick_grid.append({"Q": Q, **rounded(shares(add_quick=Q))})
quick_tipping = {    # medians; the last two use the low end of the 80% interval of the 180-days-or-more share
    "most_cut_offs_within_a_month": first(lambda s: s["within_30d"][1] >= 0.5, "add_quick"),
    "quick_catches_twice_as_common_as_180d_plus": first(lambda s: s["within_30d"][1] >= 2 * s["d180_plus"][1], "add_quick"),
    "fewer_than_a_quarter_ran_180d_plus": first(lambda s: s["d180_plus"][1] < 0.25, "add_quick"),
    "fewer_than_a_fifth_ran_180d_plus": first(lambda s: s["d180_plus"][1] < 0.2, "add_quick"),
    "low_end_below_a_quarter_180d_plus": first(lambda s: s["d180_plus"][0] < 0.25, "add_quick"),
    "low_end_below_a_fifth_180d_plus": first(lambda s: s["d180_plus"][0] < 0.2, "add_quick"),
}
print("\nhidden QUICK catches Q added to the nine (median and 80% interval of the shares)")
for g in quick_grid:
    print(f"  Q = {g['Q']:>2} (n = {g['n']:>2}): within 30 d {g['within_30d'][1]:.1%} ({g['within_30d'][0]:.1%}-{g['within_30d'][2]:.1%})"
          f"   180 d or more {g['d180_plus'][1]:.1%} ({g['d180_plus'][0]:.1%}-{g['d180_plus'][2]:.1%})")
print("  tipping points (smallest Q):", quick_tipping)

# ---- 2. hidden long cases H
long_grid = []
for H in (0, 3, 6, 9, 18, 36):
    long_grid.append({"H": H, **rounded(shares(add_long=H))})
long_tipping = {"long_ones_twice_as_common_as_quick_catches": first(lambda s: s["d180_plus"][1] >= 2 * s["within_30d"][1], "add_long")}
print("\nhidden LONG cases H added to the nine")
for g in long_grid:
    print(f"  H = {g['H']:>2} (n = {g['n']:>2}): within 30 d {g['within_30d'][1]:.1%} ({g['within_30d'][0]:.1%}-{g['within_30d'][2]:.1%})"
          f"   180 d or more {g['d180_plus'][1]:.1%} ({g['d180_plus'][0]:.1%}-{g['d180_plus'][2]:.1%})")
print("  tipping points (smallest H):", long_tipping)

# ---- 3. what the chart cannot say: how often providers catch abuse at all
f30, f180_before = base["within_30d"][1], 1 - base["d180_plus"][1]
frontier = [{"d": d_, "cut_off_within_30d": r4(d_ * f30), "cut_off_before_180d": r4(d_ * f180_before)}
            for d_ in (1.0, 0.75, 0.5, 0.25, 0.1)]
detect = {"frontier": frontier, "d_needed_for_half_cut_off_before_180d": r4(0.5 / f180_before),
          "d_needed_for_half_cut_off_within_30d": r4(0.5 / f30)}
print("\nif providers eventually cut off a share d of all abusive operations, the share cut off by day 30 / 180 is d x")
print(f"  {f30:.0%} / {f180_before:.0%} (the chart's medians); d needed for half to be cut off before day 180: "
      f"{detect['d_needed_for_half_cut_off_before_180d']}; within 30 days: {detect['d_needed_for_half_cut_off_within_30d']} (above 1: impossible)")

# ---- 4. how many cut-offs in the table state a duration, and where the nine come from
CUT = {   # hacking, fraud and spying operations an AI provider cut off, by the provider that did (explicit lists, a judgement)
    "Anthropic": {"duration": ["ANT-2025-08-GTG2002", "ANT-2025-08-GTG5004", "ANT-2025-11-GTG1002", "ANT-2026-09-GTG50014",
                               "ANT-2026-09-GTG50020", "ANT-2026-09-GTG50029"],
                  "left_out": ["ANT-2025-08-CONTAGIOUS"],       # a stated duration (0 days: banned before any prompt) that the chart leaves out
                  "none": ["ANT-2026-09-GTG20006", "ANT-2026-09-GTG10007", "ANT-2026-09-GTG50021", "ANT-2026-09-GTG15001"]},
    "OpenAI": {"duration": ["OAI-2025-04-AKIRABOT"], "left_out": [],
               "none": ["OAI-2024-02-STATE", "OAI-2024-10-CYBER3", "OAI-2025-02-PEERREVIEW", "OAI-2025-02-DPRKEMPLOY",
                        "OAI-2025-02-DPRKCYBER", "OAI-2025-02-CAMBODIA", "OAI-2025-06-SCOPECREEP", "OAI-2025-06-APT5-APT15",
                        "OAI-2025-06-DPRKIT", "OAI-2025-06-WRONGNUMBER", "OAI-2025-10-RUMALWARE", "OAI-2025-10-UTA0388",
                        "OAI-2025-10-SCAMS", "OAI-2026-02-DATEBAIT", "OAI-2026-02-CYBERSPECOPS", "OAI-2026-07-POIPET",
                        "MS-2025-11-SESAMEOP"]},
    # MS-2024-02-STATE is the same five actors in the same joint report as OAI-2024-02-STATE (its row says so): counted once, above
    "Microsoft": {"duration": ["MS-2026-09-EVILTOKENS"], "left_out": [], "none": ["MS-2025-02-STORM2139"]},
    "Google": {"duration": ["SVC-XANTHOROX"], "left_out": [], "none": ["GTIG-2025-01-GEMINI", "GTIG-2025-11-OTHERS", "GTIG-2026-06-OUTSIDER"]},
}
EXCLUDED_QUICK = ["OAI-2024-05-ZEROZENO", "ANT-2025-08-CONTAGIOUS", "OAI-2026-09-DISTILL"]    # influence; a ban at sign-up; model copying
EXCLUDED_LONG = ["ANT-2026-09-GTG54006"]                                                     # influence, 29 accounts for about 16 months
ids = [c for v in CUT.values() for kind in v.values() for c in kind]
none_ids = [c for v in CUT.values() for c in v["none"]]
left_out = [c for v in CUT.values() for c in v["left_out"]]
assert len(ids) == len(set(ids)) and all(c in D.index for c in ids), "case lists must be distinct and in the table"
assert "MS-2024-02-STATE" in D.index and "Same five actors as OAI-2024-02-STATE" in D.loc["MS-2024-02-STATE", "notes"]
assert sorted(c for v in CUT.values() for c in v["duration"]) == sorted(c[0] for c in CAUGHT), "the nine must match Chart 5"
assert set(left_out) <= set(EXCLUDED_QUICK) and not set(none_ids) & set(EXCLUDED_QUICK + EXCLUDED_LONG), \
    "a cut-off with a stated duration must not also be listed as one without"
total = len(ids)
by_provider = {p: {"cut_off": len(v["duration"]) + len(v["left_out"]) + len(v["none"]), "with_duration_used_by_chart": len(v["duration"]),
                   "stated_duration_left_out_of_chart": len(v["left_out"])} for p, v in CUT.items()}
stated_within_30d = int((hi <= 30).sum()) + len(left_out)       # known quick: three charted cases and the ban at sign-up
silent = int(D.loc[none_ids, ["start_date", "duration_basis"]].isna().all(axis=1).sum())    # no start date and nothing on duration
disclosure = {"cut_offs_in_table": total, "with_usable_duration": n, "share_with_duration": r4(n / total),
              "stated_duration_left_out_of_chart": len(left_out), "without_duration": len(none_ids),
              "without_duration_and_without_start_date_or_basis": silent, "by_provider": by_provider,
              "share_within_30d_if_every_missing_duration_were": {"over_30d": r4(stated_within_30d / total),
                                                                  "within_30d": r4((stated_within_30d + len(none_ids)) / total)}}
print("\ncut-offs of hacking, fraud or spying in the table (the joint OpenAI and Microsoft report counted once):", total,
      "of which with a usable duration:", n, "| stated but left out:", len(left_out), "| none:", len(none_ids), by_provider)
print("  share within 30 days if the missing durations were all long / all short:", disclosure["share_within_30d_if_every_missing_duration_were"])
prov = np.array([c[0].startswith("ANT-") for c in CAUGHT])
split = {}
for name, mask in (("Anthropic's six", prov), ("the other three (OpenAI, Microsoft, Google)", ~prov)):
    split[name] = {"n": int(mask.sum()), "within_30d_for_sure": int((hi[mask] <= 30).sum()),
                   "180d_or_more_for_sure": int((lo[mask] >= 180).sum()),
                   "upper_bounds_days": sorted(int(x) for x in hi[mask])}
print("  the nine by source of the cut-off:", split)

# ---- 5. which cases carry the shares
# The nine do not all measure the same thing. The three that are certainly within a month: GTG-2002's 30 days is the window in
# which its victims were hit ('in just the last month'), GTG-50020's 26 days is how long its network addresses were active, and
# GTG-50014's 21 days is how long one stolen key was used (its addresses were active for 75 days). The three long cases that
# are not Anthropic's: AkiraBot was found by SentinelOne before OpenAI disabled its key, EvilTokens ended in a court seizure and
# arrests, and Xanthorox's 10 months is a product's lifetime (Google disabled its accounts at the end).
WINDOWS = ["ANT-2025-08-GTG2002", "ANT-2026-09-GTG50020", "ANT-2026-09-GTG50014"]
NOT_ANTHROPIC = ["OAI-2025-04-AKIRABOT", "MS-2026-09-EVILTOKENS", "SVC-XANTHOROX"]
for c in WINDOWS + NOT_ANTHROPIC:
    assert c in [x[0] for x in CAUGHT]
keep_without = lambda drop: np.array([c[0] not in drop for c in CAUGHT])
leave_one_out = [{"left_out": c[0], **rounded(shares(keep=keep_without([c[0]])))} for c in CAUGHT]
groups = {"without_the_three_windows": WINDOWS, "without_the_three_long_cases_that_are_not_anthropics": NOT_ANTHROPIC,
          "without_both_groups": WINDOWS + NOT_ANTHROPIC}
dropped = {k_: {"left_out": v, **rounded(shares(keep=keep_without(v)))} for k_, v in groups.items()}
rng_lo = lambda key: [r4(min(x[key][1] for x in leave_one_out)), r4(max(x[key][1] for x in leave_one_out))]
which_cases = {"leave_one_out": leave_one_out, "range_of_medians_leave_one_out": {"within_30d": rng_lo("within_30d"), "d180_plus": rng_lo("d180_plus")},
               "groups": dropped}
print("\nwhich cases carry the shares: leave one out ->", {c[0].split('-', 2)[-1]: (f"{x['within_30d'][1]:.0%}", f"{x['d180_plus'][1]:.0%}")
                                                      for c, x in zip(CAUGHT, leave_one_out)})
for k_, g in dropped.items():
    print(f"  {k_:55s} n = {g['n']}: within 30 d {g['within_30d'][1]:.1%} ({g['within_30d'][0]:.1%}-{g['within_30d'][2]:.1%})"
          f"   180 d or more {g['d180_plus'][1]:.1%} ({g['d180_plus'][0]:.1%}-{g['d180_plus'][2]:.1%})")

# ---- 6. every cut-off in the table with a stated duration, whatever the kind of operation
for c in EXCLUDED_QUICK + EXCLUDED_LONG:
    r = D.loc[c]
    assert (r.duration_days_high <= 30) if c in EXCLUDED_QUICK else (r.duration_days_low >= 180), c
inclusive = shares(add_quick=len(EXCLUDED_QUICK), add_long=len(EXCLUDED_LONG))
print("\nwith the four cut-offs the chart leaves out that have a stated duration added:", rounded(inclusive))

res = {"charted": {"share_within_30d": q3(s30), "share_180d_plus": q3(s180)},
       "hidden_quick_catches": {"grid": quick_grid, "tipping_points": quick_tipping},
       "hidden_long_cases": {"grid": long_grid, "tipping_points": long_tipping},
       "detection_rate": detect, "disclosure": disclosure, "nine_by_source": split, "which_cases_carry_the_shares": which_cases,
       "all_stated_durations": {"added_quick": EXCLUDED_QUICK, "added_long": EXCLUDED_LONG, **rounded(inclusive)}}
dump_json(res, RESULTS / "sensitivity_c05.json")
