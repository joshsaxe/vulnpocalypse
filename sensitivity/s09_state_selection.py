"""Chart 9 robustness: what the hidden campaigns and the famous ones can and cannot change.

Chart 9 is not a model: it draws the time from first intrusion to discovery for nine well-documented state-linked
campaigns, and says state hackers "can stay hidden for years and use only a sliver of their access". The note says the
campaigns are "not a sample: ones still hidden are missing and famous ones over-represented". Two different biases, and
they matter for different claims:

  * Hidden campaigns (never discovered, or discovered late) have no dwell time yet, or a longer one. They can only add
    long cases, so they cannot weaken "can stay hidden for years". That claim is an existence claim: it fails only if the
    long cases themselves are wrong. The script says how wrong they would have to be (the dwell time overstated by what
    factor, and what is left if the two Kaspersky cases, which are the longest, are dropped), and shows that the nine are
    not a selection of the longest cases in the table: two more campaigns have a dwell figure, and four more have dates
    but no figure.
  * Famous campaigns are over-represented, which would overstate how TYPICAL a long dwell is. The script compares the
    charted campaigns with the table's other campaigns and with Mandiant's median for espionage.
  * "Only a sliver" rests on two campaigns that report both how many systems were infected and how many were worked
    (SolarWinds and Equation Group). The script gives the ratio under the loosest reading of each count, and by what factor
    the number worked would have to be undercounted for it to reach 10%.
  * The charted years are what the sources say, which is not always what the table's own start and discovery dates give
    (Volt Typhoon's five years is CISA's figure for some victims; BRICKSTORM's 1.08 is Mandiant's average per victim). The
    script repeats the nine on the table's own dates, so that the comparison with Mandiant's median does not hang on those two.

No random numbers. The 'charted' years must reproduce results/c09_state_patience.json; the script stops if they do not.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))                    # the repository root
import numpy as np
import pandas as pd
from common.paths import DATA, RESULTS, dump_json

E = pd.read_csv(DATA / "H_espionage_cases.csv")
r2 = lambda x: round(float(x), 2)
get = lambda name: float(E[E.campaign.str.startswith(name)].years_undetected.astype(float).iloc[0])   # as charts/c09_state_patience.py

# ---- the nine charted campaigns, as drawn (Volt Typhoon's five years is a lower bound)
CHARTED = {"Equation Group": get("Equation Group"), "Regin": get("Regin"), "Volt Typhoon†": 5.0,
           "SolarWinds": get("SolarWinds SUNBURST ("), "BRICKSTORM": get("UNC5221 BRICKSTORM"), "OPM breach": get("OPM"),
           "Midnight Blizzard": get("Midnight Blizzard"), "Ivanti zero-days": get("UNC5221 Ivanti"), "Storm-0558": get("Storm-0558")}
MANDIANT_ESPIONAGE = 122 / 365            # median days to discovery, espionage and North Korean IT-worker cases (M-Trends 2026)
ref = json.load(open(RESULTS / "c09_state_patience.json"))["years_to_discovery"]
for k_, v in CHARTED.items():
    assert round(v, 3) == ref[k_], f"{k_} differs from Chart 9"
assert round(MANDIANT_ESPIONAGE, 3) == ref["Typical spying case*"]
print("the charted years reproduce results/c09_state_patience.json")

# ---- the table's campaigns (not its benchmark, contrast and duplicate rows)
camp = E[~E.campaign.str.startswith(("Mandiant", "Contrast")) & ~E.campaign.str.contains("tradecraft source")].copy()


def years(x):
    if pd.isna(x):
        return np.nan
    s = str(x)
    return float(np.mean([float(t) for t in s.split("-")])) if "-" in s else float(s)     # "1-2" (Salt Typhoon) is read as 1.5


camp["yrs"] = camp.years_undetected.map(years)
with_figure = camp[camp.yrs.notna()]
no_figure = camp[camp.yrs.isna()]
allv = sorted(with_figure.yrs, reverse=True)
chv = sorted(CHARTED.values(), reverse=True)
count = lambda v, t: int(sum(x >= t for x in v))

# ---- 1. "can stay hidden for years": how wrong would the long cases have to be?
LONG = {"Equation Group": CHARTED["Equation Group"], "Regin": CHARTED["Regin"], "Volt Typhoon†": CHARTED["Volt Typhoon†"]}
years_claim = {
    "charted_nine": {"n": len(chv), "at_least_2y": count(chv, 2), "at_least_5y": count(chv, 5), "at_least_10y": count(chv, 10)},
    "campaigns_with_a_figure": {"n": len(allv), "at_least_2y": count(allv, 2), "at_least_5y": count(allv, 5),
                                "at_least_10y": count(allv, 10)},
    "overstatement_factor_to_fall_below_2y": {k_: r2(v / 2) for k_, v in LONG.items()},
    "years_to_remove_to_fall_below_2y": {k_: r2(v - 2) for k_, v in LONG.items()},
    "campaigns_left_out_with_a_figure": [c for c in with_figure.campaign if not any(c.startswith(s) for s in
                                         ("Equation Group", "Regin", "Volt Typhoon", "SolarWinds SUNBURST (", "UNC5221 BRICKSTORM",
                                          "OPM", "Midnight Blizzard", "UNC5221 Ivanti", "Storm-0558"))],
    "campaigns_with_dates_but_no_figure": list(no_figure.campaign),
}
kaspersky = with_figure.publisher.astype(str).str.startswith("Kaspersky")      # the two longest cases come from one vendor
rest = sorted(with_figure[~kaspersky].yrs, reverse=True)
years_claim["without_kaspersky_reports"] = {"campaigns_dropped": list(with_figure[kaspersky].campaign), "at_least_2y": count(rest, 2),
                                            "longest_years": r2(rest[0]), "longest": with_figure[~kaspersky].sort_values("yrs").campaign.iloc[-1]}
print("\n'years': campaigns with a dwell figure, longest first:", [r2(x) for x in allv])
print(" ", years_claim)

# ---- 2. typical? the famous nine against the rest, and against Mandiant's median
typical = {"median_charted_nine_years": r2(np.median(chv)), "median_campaigns_with_a_figure_years": r2(np.median(allv)),
           "mandiant_espionage_median_years": r2(MANDIANT_ESPIONAGE),
           "charted_median_over_mandiant": r2(np.median(chv) / MANDIANT_ESPIONAGE),
           "all_median_over_mandiant": r2(np.median(allv) / MANDIANT_ESPIONAGE),
           "charted_nine_at_least_1y": count(chv, 1), "campaigns_with_a_figure_at_least_1y": count(allv, 1)}
print("\ntypical:", typical)

# ---- 3. "only a sliver": the number worked would have to be undercounted by what factor to reach 10%?
sw, eq = E[E.campaign.str.startswith("SolarWinds SUNBURST (")].iloc[0], E[E.campaign.str.startswith("Equation Group")].iloc[0]
assert "18,000" in sw.victims_broad and "17,000" in sw.victims_broad and "9 federal agencies" in sw.victims_targeted
assert "tens of thousands" in eq.victims_broad and "more than 500 victims" in eq.victims_targeted
SLIVER = {   # (infected, loosest reading first), (worked)
    "SolarWinds": ((18000, 17000), 109),                   # about 100 companies and 9 federal agencies of some 18,000 (17,000 per SolarWinds)
    "Equation Group": ((20000, 10000), 500),               # more than 500 victims seen of 'tens of thousands' (20,000 literally, 10,000 loosely)
}
sliver = {}
for name, (infected, worked) in SLIVER.items():
    hi_ratio = max(worked / x for x in infected)           # the loosest reading: the fewest infected
    sliver[name] = {"worked": worked, "infected_readings": list(infected),
                    "worked_share_by_reading": [round(worked / x, 4) for x in infected],
                    "undercount_factor_to_reach_10pct": [r2(0.10 * x / worked) for x in infected],
                    "undercount_factor_to_reach_50pct": [r2(0.50 * x / worked) for x in infected],
                    "largest_worked_share": round(hi_ratio, 4)}
sw_microsoft = 40 / 18000       # Microsoft's own count of customers "targeted more precisely" by 17 December 2020
sliver["SolarWinds"]["worked_share_if_only_microsofts_40_customers"] = round(sw_microsoft, 4)
print("\nsliver:", sliver)

# ---- 4. the nine on the table's own start and discovery dates
PREFIX = {"Equation Group": "Equation Group", "Regin": "Regin", "Volt Typhoon†": "Volt Typhoon", "SolarWinds": "SolarWinds SUNBURST (",
          "BRICKSTORM": "UNC5221 BRICKSTORM", "OPM breach": "OPM", "Midnight Blizzard": "Midnight Blizzard",
          "Ivanti zero-days": "UNC5221 Ivanti", "Storm-0558": "Storm-0558"}


def mid(x):
    """A date given to the month or the year is placed at the middle of that month or year."""
    x = str(x)
    return pd.Timestamp(x + "-15") if len(x) == 7 else pd.Timestamp(x + "-07-01") if len(x) == 4 else pd.Timestamp(x)


def own_years(row):
    return (mid(row.discovered) - mid(row.start)).days / 365.25


row_of = lambda prefix: E[E.campaign.str.startswith(prefix)].iloc[0]
own = {k_: own_years(row_of(PREFIX[k_])) for k_ in CHARTED}
own_v = sorted(own.values(), reverse=True)
differ = [k_ for k_ in CHARTED if max(CHARTED[k_], own[k_]) / min(CHARTED[k_], own[k_]) > 1.5]
regin = row_of("Regin")
assert "spring 2012" in regin.notes                                           # 'Kaspersky aware of Regin from spring 2012'
own_dates = {"years_on_the_tables_own_dates": {k_: r2(v) for k_, v in own.items()},
             "differ_from_the_chart_by_more_than_1.5x": differ,
             "median_of_the_nine_years": r2(np.median(own_v)), "median_over_mandiant": r2(np.median(own_v) / MANDIANT_ESPIONAGE),
             "at_least_2y": count(own_v, 2), "at_least_5y": count(own_v, 5), "at_least_10y": count(own_v, 10),
             "regin_years_until_kaspersky_knew_of_it_in_spring_2012": r2((pd.Timestamp("2012-04-15") - mid(regin.start)).days / 365.25),
             "left_out_with_dates_but_no_figure": {c.campaign: r2(own_years(c)) for c in no_figure.itertuples()}}
print("\non the table's own dates:", own_dates)

res = {"charted_years": {k_: r2(v) for k_, v in CHARTED.items()}, "years_claim": years_claim, "typical": typical, "sliver": sliver,
       "own_dates": own_dates}
dump_json(res, RESULTS / "sensitivity_c09.json")
