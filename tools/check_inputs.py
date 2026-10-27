#!/usr/bin/env python3
"""Check the numbers typed into the chart scripts against the data tables they came from.

Almost every number behind the figures is read from data/ or computed from it. A few are typed into a script, because
they sit in a table's notes column rather than in a column of their own, or because they are judgements. This script
finds each of them and says which kind it is:

    MATCH        the typed number equals the number in the data table
    DERIVED      it follows from the table by arithmetic that this script redoes
    APPROX       it is a rounding of a table figure, within a stated tolerance
    ASSUMED      the table gives one bound (or none) and the author supplied the rest; the data bound is shown
    OVERRIDE     deliberately different from the table, for the reason given
    NOTE         a quirk in the data worth knowing about; the chart script is not wrong
    NOT IN DATA  typed from an outside source that is not in the tables: docs/PARAMETERS.md says where it comes from
    FAIL         the typed number contradicts the table (the script then exits with status 1)

Usage:
    python tools/check_inputs.py                                  # print the report
    python tools/check_inputs.py --update-docs docs/PARAMETERS.md # rewrite the table between the two marker comments

Row numbers are pandas row numbers (0 is the first data row, as the chart scripts count them); a spreadsheet shows that
row as number + 2 because of the header.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd

from common.lifespans import load as load_lifespans
from common.paths import DATA, RESULTS

CHECKS = []          # (chart, what, typed, status, evidence)


def add(chart, what, typed, status, evidence):
    CHECKS.append((chart, what, typed, status, evidence))


def verdict(ok, status):
    return status if ok else "FAIL"


def near(a, b, tol):
    """Relative closeness."""
    return abs(a - b) <= tol * max(abs(b), 1e-12)


def csv(name, **kw):
    return pd.read_csv(DATA / name, **kw)


A1 = csv("A1_fraud_series.csv", dtype={"year": str})
A2 = csv("A2_hacking_series.csv", dtype={"year": str})
A1E = csv("A1_fraud_ai_evidence.csv")
A2E = csv("A2_hacking_ai_evidence.csv")
C_PAY, C2, F_PAY = csv("C_pay.csv"), csv("C2_dev_pay_by_country.csv"), csv("F_pay.csv")
D_CASES = csv("D_platform_cases.csv").set_index("case_id")
E_JUDGE, E_TIMES = csv("E_stage_judgements.csv"), csv("E_stage_times.csv")
G_ADOPT, G_VENDOR = csv("G_adoption.csv"), csv("G_vendor_ai.csv")
H_CASES, I_LAGS, J_VULNS = csv("H_espionage_cases.csv"), csv("I_adoption_lags.csv"), csv("J_ai_vulns.csv")


def series_value(df, sid, year):
    d = df[(df.series_id == sid) & (df.year == str(year))]
    assert len(d) == 1, (sid, year, len(d))
    return float(d.value.iloc[0])


def money(v):
    return f"${v:,.0f}"


def span_days(a, b):
    """Days between two dates given as 'YYYY', 'YYYY-MM' or 'YYYY-MM-DD' (start of the period for a, end for b)."""
    def parse(s, end):
        p = [int(x) for x in str(s).split("-")]
        if len(p) == 1:
            return dt.date(p[0], 12, 31) if end else dt.date(p[0], 1, 1)
        if len(p) == 2:
            nxt = dt.date(p[0] + (p[1] == 12), p[1] % 12 + 1, 1)
            return nxt - dt.timedelta(days=1) if end else dt.date(p[0], p[1], 1)
        return dt.date(*p)
    return (parse(b, True) - parse(a, False)).days, (parse(b, False) - parse(a, True)).days


# ======================================================================================================== lede figure
ok = round(4.38 / 20, 2) == 0.22 and round(132.65 / 17, 1) == 7.8
add("0", "Cost to find a flaw, per bug: $0.22 (cheap model) to $7.80 (frontier agent)", "0.22, 7.8",
    verdict(ok, "NOT IN DATA"),
    f"CyberGym (Lu et al., 2026): $4.38 for 20 bugs, $132.65 for 17; arithmetic checked ({4.38/20:.3f}, {132.65/17:.2f})")
add("0", "Cost to break into an AI lab's code repository", "3,000", "NOT IN DATA", "Hacktron write-up: 'less than $3,000 in tokens'")
add("0", "Cost of a browser exploit chain", "40,000", "NOT IN DATA", "XBOW: about $40,000 in API fees for six days")

# ======================================================================================================== chart 1
chain = {("WORLD_CHAINALYSIS_SCAM_REVENUE_V2023", 2021): 10.9, ("WORLD_CHAINALYSIS_SCAM_REVENUE_V2023", 2022): 5.9,
         ("WORLD_CHAINALYSIS_SCAM_REVENUE_V2026", 2024): 12.0, ("WORLD_CHAINALYSIS_SCAM_REVENUE_V2026_PROJ", 2025): 17.0}
for (sid, yr), typed in chain.items():
    got = series_value(A1, sid, yr)
    add("1", f"Chainalysis crypto-scam revenue {yr}, $bn", f"{typed}", verdict(got == typed, "MATCH"),
        f"A1_fraud_series {sid.replace('WORLD_CHAINALYSIS_SCAM_REVENUE_', '')} {yr} = {got}")
got = series_value(A2, "CHAINALYSIS_RANSOMWARE_LATEST", 2025) / 1e9
note = str(A2[(A2.series_id == "CHAINALYSIS_RANSOMWARE_LATEST") & (A2.year == "2025")].notes.iloc[0])
add("1", "Chainalysis ransomware payments 2025, $bn", "0.90",
    verdict(near(got, 0.82, 0.01) and "$900 million" in note, "OVERRIDE"),
    f"table: ${got:.2f}bn (published floor); override to $0.90bn because Chainalysis says it expects 2025 'to approach or "
    "exceed $900 million' once attribution catches up (same row's notes)")
for yr, typed in ((2023, 1.10), (2024, 0.734)):
    got = series_value(A2, "FINCEN_RANSOMWARE_PAYMENTS", yr) / 1e9
    add("1", f"FinCEN ransomware payments {yr}, $bn", f"{typed}", verdict(near(got, typed, 1e-3), "MATCH"),
        f"A2_hacking_series FINCEN_RANSOMWARE_PAYMENTS {yr} = {got}")
note = str(A2[(A2.series_id == "FINCEN_RANSOMWARE_PAYMENTS") & (A2.year == "2023")].notes.iloc[0])
add("1", "FinCEN ransomware payments 2022, $bn", "0.62",
    verdict(round(1.1 / 1.77, 2) == 0.62 and "620m" in note, "DERIVED"),
    "FinCEN gives 2023 = $1.1bn, up 77% on 2022, which implies 1.1/1.77 = $0.62bn; the row's notes say this figure is "
    "'derived, not published'")
ic3_share = float(A1E[A1E.metric == "Share of IC3 2025 total reported losses"].value.iloc[0])
add("1", "Share of fraud dollars in IC3 complaints that mention AI (the 'noticed' share), central value", "0.042",
    verdict(near(ic3_share, 0.042, 0.03), "APPROX"),
    f"A1_fraud_ai_evidence: $893.3m of $20.877bn = {ic3_share:.4f} of all IC3 losses (the 2025 report); range 2.5-7% is a judgement")
ai_hack = float(A1E[A1E.claim.str.contains("hacking types", na=False)].value.iloc[0]) * 1e9
cat = {k: series_value(A1, k, 2025) * 1e9 for k in ("US_IC3_CAT_DATA_BREACH", "US_IC3_CAT_MALWARE_SCAREWARE_VIRUS",
                                                    "US_IC3_CAT_BOTNET", "US_IC3_CAT_SIM_SWAP")}
lo_share = ai_hack / sum(cat.values())
hi_share = ai_hack / (cat["US_IC3_CAT_DATA_BREACH"] + cat["US_IC3_CAT_MALWARE_SCAREWARE_VIRUS"])
add("1", "Share of hacking-type dollars in IC3 complaints that mention AI, central value", "0.014",
    verdict(lo_share - 0.002 <= 0.014 <= hi_share + 0.002, "APPROX"),
    f"A1_fraud_ai_evidence: {money(ai_hack)} of AI-referencing losses over the hacking-type categories' dollars "
    f"= {lo_share:.1%} (data breach, malware, botnet, SIM swap) to {hi_share:.1%} (data breach and malware only); range 0.7-2.8% is a judgement")
v10 = float(A2E[A2E.claim.str.contains("doubled from ~5% to ~10%", na=False)].value.iloc[0])
add("1", "Share of malicious e-mail with AI-written text, used for 'unnoticed' AI in fraud (mean)", "0.10",
    verdict(v10 == 0.10, "MATCH"), f"A2_hacking_ai_evidence (Verizon DBIR 2025): {v10}")
ibm_rows = A2E[A2E.claim.str.startswith("IBM/Ponemon", na=False)]
ibm = [float(ibm_rows[ibm_rows.claim.str.contains(k, na=False)].value.iloc[0]) for k in ("2025 edition", "2026 edition")]
add("1", "Share of breaches in which attackers used AI, used for 'unnoticed' AI in hacking (mean)", "0.20",
    verdict(near(float(np.mean(ibm)), 0.20, 0.05), "APPROX"),
    f"A2_hacking_ai_evidence (IBM): {ibm[0]:.0%} (2025 edition) and {ibm[1]:.0%} (2026 edition); their midpoint is {np.mean(ibm):.3f}")
for what, typed in (("Total level of 2025 fraud losses: lognormal(median $220bn, 90% interval 105-461)", "220, 105, 461"),
                    ("Total level of 2025 hacking losses: lognormal(median $76bn, 90% interval 31-188)", "76, 31, 188"),
                    ("America's share of 2025 fraud losses: mean 0.42, 10th percentile 0.32", "0.42, 0.32")):
    add("1", what, typed, "NOT IN DATA", "the author's earlier triangulation (docs/PARAMETERS.md); no table in data/")
add("1", "Common reporting drift subtracted: America 0.02+/-0.02, elsewhere 0.01+/-0.015, hacking 0.01+/-0.02 a year",
    "see models/c01_loss_trend.py", "ASSUMED", "judgement; sensitivity/s01_loss_trend.py halves and doubles it")
add("1", "AI adoption vs 2025: 2023 about 0.25, 2024 about 0.5; 2026 lognormal(1.4, 90% interval 1.0-2.0)", "0.25, 0.5, 1.4",
    "ASSUMED", "judgement")
add("1", "But-for fractions (central 25%, sceptical 10%, generous 50% of noticed AI losses) and unnoticed shares", "see model",
    "ASSUMED", "judgements; the model averages the three sets with equal weight")
n_series = json.load(open(RESULTS / "c01_loss_trend.json"))["n_series"] if (RESULTS / "c01_loss_trend.json").exists() else None
add("1", "Number of loss series pooled", "23 (in the chart's source line)",
    "MATCH" if n_series in (None, 23) else "FAIL",
    f"results/c01_loss_trend.json n_series = {n_series}" if n_series else "run charts/c01_losses.py to check")

# ======================================================================================================== chart 2
life = load_lifespans()
raw = csv("B_enterprise_lifespans.csv")
add("2", "'All 152' (row label)", "152", verdict(len(raw) == 152, "MATCH"),
    f"B_enterprise_lifespans.csv has {len(raw)} rows; {len(life)} have dates and enter the competing-risks estimate")

# ======================================================================================================== chart 3
crime = [(0, 12000, 24000), (2, 24000, 24000), (4, 48000, 48000), (8, 120000, 120000)]
for i, lo, hi in crime:
    r = C_PAY.iloc[i]
    add("3", f"{r.role[:60]}", f"${lo:,}" + (f"-{hi:,}" if hi != lo else ""),
        verdict(r.usd_annual_low == lo and r.usd_annual_high == hi, "MATCH"), f"C_pay.csv row {i}: {money(r.usd_annual_low)}-{money(r.usd_annual_high)}")
for i, typed, what in ((22, 195000, "Median total pay, US software engineers, 2025"), (23, 250000, "AI engineers' total pay, 2026")):
    r = C_PAY.iloc[i]
    add("3", what, f"{typed:,}", verdict(r.usd_annual_low == typed, "MATCH"), f"C_pay.csv row {i}: {money(r.usd_annual_low)}")
a, b = F_PAY.iloc[14].usd_annual_low, F_PAY.iloc[15].usd_annual_low
add("3", "OpenAI or Anthropic, 2026", "878,750", verdict((a + b) / 2 == 878750, "DERIVED"),
    f"mean of the two medians in F_pay.csv rows 14 and 15: ({money(a)} + {money(b)}) / 2")
mins, maxs = C_PAY.iloc[[2, 3, 4, 5]].usd_annual_low.min(), C_PAY.iloc[[2, 3, 4, 5]].usd_annual_low.max()
add("3", "Band: median pay in dark-web job ads by role, $1,300-4,000 a month", "15,600-48,000 a year",
    verdict(mins == 1300 * 12 and maxs == 4000 * 12, "MATCH"),
    f"C_pay.csv rows 2-5: lowest role median {money(mins)} (designer), highest {money(maxs)} (reverse engineer)")
add("3", "Russian developers' take-home pay by level, H1 2021 (roubles a month: 52,000 / 120,000 / 195,000 / 230,000)",
    "52,000 ... 230,000", "NOT IN DATA", "Habr Career, first half of 2021 (bibliography)")
add("3", "Roubles per dollar, 2021 average", "73.65", "NOT IN DATA", "World Bank (bibliography)")

# ======================================================================================================== chart 4
stages = E_JUDGE[E_JUDGE.stage.str.match(r"^\d")]
add("4", "Eight stages; the central hour shares sum to 100%", "8 stages, 1.00",
    verdict(len(stages) == 8 and abs(stages.labour_share_mid.sum() - 1) < 1e-9, "MATCH"),
    f"E_stage_judgements.csv: {len(stages)} stages, shares sum to {stages.labour_share_mid.sum():.2f}")
tot = float((stages.labour_share_mid * stages.ai_automatable_mid).sum())
add("4", "'Together, AI can do about 36% of the hours' (note under the bars)", "36%", verdict(round(tot * 100) == 36, "DERIVED"),
    f"sum of share x AI-doable share over the eight stages = {tot:.3f}")
add("4", "Hand-over share 10-80%, AI speed-up 3-20x, checking time 10-40% of doing it by hand", "10-80%, 3-20x, 10-40%",
    "ASSUMED", "judgements: no public dataset measures them; stated in the chart's note")

# ======================================================================================================== chart 5
CAUGHT = {"ANT-2026-09-GTG50020": (4, 26), "ANT-2025-08-GTG2002": (7, 30), "ANT-2025-11-GTG1002": (10, 60),
          "ANT-2026-09-GTG50014": (21, 21), "ANT-2026-09-GTG50029": (30, 148), "OAI-2025-04-AKIRABOT": (180, 225),
          "MS-2026-09-EVILTOKENS": (213, 213), "ANT-2025-08-GTG5004": (180, 225), "SVC-XANTHOROX": (290, 315)}
NOTCUT = {"CS-2026-10-ARTEX": (7, 21), "AWS-2026-02-FORTIGATE": (38, 38), "SVC-WORMGPT": (62, 188),
          "ANT-2025-08-VIETNAM": (270, 270), "ANT-2026-09-GTG50027": (263, 263), "SVC-GHOSTGPT": (610, 610)}
for cid, (lo, hi) in {**CAUGHT, **NOTCUT}.items():
    r = D_CASES.loc[cid]
    dl, dh = r.duration_days_low, r.duration_days_high
    typed = f"{lo}" + (f"-{hi}" if hi != lo else "")
    if cid == "ANT-2026-09-GTG50027":
        # the row dates the build 'Jan-Jul 2026' and the report 10 Sep 2026; 263 days is January to about 21 September
        d_rep = (dt.date(2026, 9, 10) - dt.date(2026, 1, 1)).days
        status = verdict(near(d_rep, hi, 0.06), "APPROX")
        ev = (f"row: system built Jan-Jul 2026, account banned in July, still running on local models at the report "
              f"(10 Sep 2026 = {d_rep} days after 1 Jan); {hi} days is within 5% of that, invisible on a log axis")
    elif cid == "SVC-GHOSTGPT":
        d0 = dt.date(2025, 1, 23)                                       # Abnormal's post, the row's pub_date
        lo_d, hi_d = (dt.date(2026, 9, 1) - d0).days, (dt.date(2026, 9, 30) - d0).days
        status = verdict(lo_d - 5 <= hi <= hi_d + 5, "DERIVED")
        ev = f"first documented 23 Jan 2025 (Abnormal; the row's pub_date), still sold in Sep 2026: {lo_d}-{hi_d} days"
    elif pd.notna(dl) and pd.notna(dh):                                 # both bounds are in the table
        if (dl, dh) == (lo, hi):
            status, ev = "MATCH", f"D_platform_cases: {dl:.0f}-{dh:.0f} days"
        elif dl == dh == lo and hi > lo:                                # the table has one figure; the author added an upper bound
            status, ev = "ASSUMED", f"D_platform_cases gives {dl:.0f} days (ban after detection); the upper bound {hi} is assumed"
        else:
            status, ev = "FAIL", f"D_platform_cases: {dl:.0f}-{dh:.0f} days"
    elif pd.isna(dl) and pd.notna(dh) and dh == hi:                     # one bound in the table, the other assumed
        status, ev = "ASSUMED", f"D_platform_cases gives only the upper bound ({dh:.0f} days); the lower bound {lo} is assumed"
    elif pd.notna(r.start_date) and pd.notna(r.end_date):               # dates in the table; days derived from them
        d_max, d_min = span_days(r.start_date, r.end_date)
        d_min, d_max = min(d_min, d_max), max(d_min, d_max)
        status = verdict(lo <= d_min + 5 and hi >= d_max - 5 and lo >= 0.75 * d_min and hi <= 1.1 * d_max, "DERIVED")
        ev = f"dates in the table: {r.start_date} to {r.end_date} is {d_min}-{d_max} days; the typed range rounds that outward"
    else:
        status, ev = "FAIL", "no basis found in the table"
    add("5", f"{cid}: duration, days ({'cut off' if cid in CAUGHT else 'not cut off'})", typed, status, ev)
add("5", "Of the nine cut off: 'three or four within a month' and 'four lasted six months or more' (note)", "3-4, 4",
    verdict(sum(h <= 30 for _, h in CAUGHT.values()) == 3 and sum(l >= 180 for l, _ in CAUGHT.values()) == 4, "DERIVED"),
    f"counts from the nine ranges: {sum(h <= 30 for _, h in CAUGHT.values())} end by day 30 (a fourth, 30-148, starts at day 30), "
    f"{sum(l >= 180 for l, _ in CAUGHT.values())} start at day 180 or later")

# ======================================================================================================== chart 6
by = I_LAGS.set_index("technique")
mir = by.loc["IoT DDoS botnets (Mirai)"]
span = float(mir.scaled_use_date.split("-")[0]) + (int(mir.scaled_use_date.split("-")[1]) - 0.5) / 12 - 2014.5
add("6", "Mirai botnets: lag from cheap insecure gadgets (about 2014) to widespread use", "2.3",
    verdict(near(span, 2.3, 0.03) and float(mir.lag_scaled_years) == 0.1, "OVERRIDE"),
    f"table lag is {mir.lag_scaled_years} years (from the Mirai code's first sighting, Aug 2016); the chart counts from mid-2014 "
    f"to Oct 2016 = {span:.1f}; sensitivity/s06_adoption_lags.py shows the alternative")
for tech, typed, what in (("Dedicated criminal LLMs (WormGPT, FraudGPT)", 2023 + 5 / 12, "WormGPT start: June 2023"),
                          ("LLM-in-the-loop / AI-generated malware", 2022 + 10.97 / 12, "AI-malware start: 30 Nov 2022"),
                          ("Agentic intrusion / extortion", 2025 + 1.8 / 12, "Agentic intrusion start: 24 Feb 2025")):
    d = str(by.loc[tech].availability_date).split("-")
    y = int(d[0]) + ((int(d[1]) - 1) + ((int(d[2]) - 1) / 30 if len(d) > 2 else 0)) / 12
    add("6", what, f"{typed:.3f}", verdict(abs(y - typed) < 0.03, "MATCH"), f"I_adoption_lags availability_date {by.loc[tech].availability_date} = {y:.3f}")
for tech in by.index:
    r = by.loc[tech]
    if pd.notna(r.lag_scaled_years) and pd.notna(r.scaled_use_date) and tech != "IoT DDoS botnets (Mirai)":
        def yr(s):
            p = str(s).split("-")
            return int(p[0]) + ((int(p[1]) - 0.5) / 12 if len(p) > 1 else 0.5)
        calc = yr(r.scaled_use_date) - yr(r.availability_date)
        if abs(calc - float(r.lag_scaled_years)) > 0.75:
            add("6", f"{tech}: lag in the table vs lag implied by its dates", f"{r.lag_scaled_years}", "NOTE",
                f"table says {r.lag_scaled_years} years; its availability and 'scaled' years imply {calc:.1f}. The table counts to the "
                "2025 Verizon report that found about 10% of malicious e-mail had AI text. Used as given; sensitivity/s06_adoption_lags.py "
                "shows the effect of the other reading")

# ======================================================================================================== chart 7
USE = {"United States": ({"state": [0, 1, 7], "private": [11], "frontier": [14, 15]}),
       "United Kingdom": ({"state": [17, 18, 19, 20, 21, 22], "private": [24]}),
       "Israel": ({"state": [32, 33, 34, 35], "private": [39]}),
       "China": ({"state": [41], "private": [42]})}
for country, sides in USE.items():
    good = True
    for side, rows in sides.items():
        for i in rows:
            r = F_PAY.iloc[i]
            good &= r.country == country
            if side == "state":
                good &= r.sector == "national_security"
            elif side == "private":
                good &= r.sector == "private_tech" and "ML/AI" in r.role
            else:
                good &= r.sector == "private_frontier_ai" and ("OpenAI" in r.role or "Anthropic" in r.role)
    add("7", f"{country}: rows used on each side", json.dumps(sides).replace('"', ""), verdict(bool(good), "MATCH"),
        "F_pay.csv: state rows are national_security, private rows are the country's Levels.fyi ML/AI engineer median, frontier rows OpenAI and Anthropic")
add("7", "Measurement-model settings: grade sd A .15 / B .25 / C .40 / D .60, role-mismatch sd .25, prior N(log 80,000, 10)", "see chart",
    "ASSUMED", "judgements; Chart 7's docstring explains them")

# ======================================================================================================== chart 8
labels = ["Open-source software", "Agile / DevSecOps", "Smartphones / mobile devices", "Commercial cloud",
          "Machine learning (production ML)", "SaaS / video conferencing", "Generative AI (LLM chatbots)"]
add("8", "The seven technologies fitted or shown", "7 names", verdict(set(labels) <= set(G_ADOPT.technology), "MATCH"),
    "all seven appear in G_adoption.csv; the two grade-D rows (PCs, corporate e-mail and web) are left out")
add("8", "Priors a ~ N(log 5, 1), b ~ N(0, 0.1), s ~ HalfNormal(0.7); NOW = 2026.8", "see chart", "ASSUMED", "judgements")

# ======================================================================================================== chart 9
H = H_CASES.set_index("campaign")
get = lambda prefix: H[H.index.str.startswith(prefix)].iloc[0]
months = lambda y: y * 12
sw, br, opm = get("SolarWinds SUNBURST ("), get("UNC5221 BRICKSTORM"), get("OPM")
mb, iv, st = get("Midnight Blizzard"), get("UNC5221 Ivanti"), get("Storm-0558")
for name, row, label, calc in (("SolarWinds", sw, "15 months", months(float(sw.years_undetected))),
                               ("BRICKSTORM", br, "13 months", months(float(br.years_undetected))),
                               ("OPM breach", opm, "11 months", months(float(opm.years_undetected))),
                               ("Midnight Blizzard", mb, "7 weeks", float(mb.years_undetected) * 52.18),
                               ("Ivanti zero-days", iv, "5 weeks", float(iv.years_undetected) * 52.18),
                               ("Storm-0558", st, "1 month", months(float(st.years_undetected)))):
    typed = float(label.split()[0])
    add("9", f"{name}: bar label", label, verdict(abs(calc - typed) < 0.8, "MATCH"),
        f"H_espionage_cases years_undetected {float(row.years_undetected)} = {calc:.1f} {label.split()[1]}")
for key, label in (("Equation Group", "14 years"), ("Regin", "11 years")):
    r = get(key)
    add("9", f"{key}: bar label", label, verdict(float(r.years_undetected) == float(label.split()[0]), "MATCH"),
        f"H_espionage_cases years_undetected = {r.years_undetected}")
add("9", "Volt Typhoon: 5+ years (a lower bound, hollow marker)", "5.0",
    verdict(float(get("Volt Typhoon").years_undetected) == 5 and "at least five years" in str(get("Volt Typhoon").notes), "MATCH"),
    "H_espionage_cases: 5; notes: 'at least five years' (CISA)")
spy = float(get("Mandiant M-Trends 2026: espionage").years_undetected)
add("9", "Typical spying case: 122 days", "122/365", verdict(abs(spy - 122 / 365) < 0.005, "MATCH"),
    f"H_espionage_cases (Mandiant M-Trends 2026 row): {spy} years; notes: 'the median dwell time for both categories was 122 days'")
allm = E_TIMES[E_TIMES.metric == "Global median dwell time"].iloc[0]
add("9", "Typical intruder: 14 days", "14/365", verdict(allm.value == 14 and allm.unit == "days", "MATCH"),
    f"E_stage_times.csv: {allm.metric} = {allm.value} {allm.unit} ({allm.year})")
eqg = get("Equation Group")
add("9", "Equation Group annotation '500+ victims among tens of thousands infected'", "500, tens of thousands",
    verdict("more than 500" in str(eqg.victims_targeted) and "tens of thousands" in str(eqg.victims_broad), "MATCH"),
    "H_espionage_cases victims columns")
add("9", "Regin annotation '27 victims in 14 countries'", "27, 14", verdict("27 victims in 14 countries" in str(get("Regin").victims_targeted), "MATCH"),
    "H_espionage_cases victims_targeted")
sw_t = str(sw.victims_targeted)
add("9", "SolarWinds annotation 'about 110 of 18,000 infected were exploited'", "110 of 18,000",
    verdict("~100 private-sector companies and 9 federal agencies" in sw_t and "18,000" in str(sw.victims_broad), "DERIVED"),
    "about 100 companies + 9 agencies = about 109 (Neuberger, 2021) of about 18,000 that downloaded the update")

# ======================================================================================================== chart 10
for f in ("c06_attacker_lag.py", "c08_govlag.py", "c10_odds.py"):
    src = (ROOT / "charts" / f).read_text()
    found = re.search(r"^NOW = 2026\.8\b", src, re.M) or re.search(r">= 2026\.8\b", src)    # Chart 8 writes the date inline
    add("10", f"'Now' is 2026.8 in charts/{f}", "2026.8", verdict(found is not None, "MATCH"),
        "late October 2026, when the data were compiled")

# ======================================================================================================== chart 11
add("11", "34 vendors tracked", "34 (in the chart's text)", verdict(len(G_VENDOR) == 34, "MATCH"), f"G_vendor_ai.csv has {len(G_VENDOR)} rows")
P_SUB = {"a", "b", "c", "none", "ml-only"}
grades_ok = set(G_VENDOR.substance.str.strip().str.lower()) <= P_SUB and set(G_VENDOR.date_conf.str.strip().str.upper()) <= {"A", "B", "C"}
add("11", "Probability a feature counts: A 1.0, B 0.95, C 0.60, none 0; date confidence A/B/C offsets", "see chart",
    verdict(grades_ok, "ASSUMED"), "judgements; every grade in G_vendor_ai.csv is covered by the script's lookup")
add("11", "Defensive spend medians $bn 2022-26: 8.0, 10.5, 13.5, 16.4, 20.3 (log-sd 0.42)", "8.0 ... 20.3", "ASSUMED",
    "judgement anchored on two market-research houses' figures for 2025-26 (about $16bn and $20bn); not in data/")
add("11", "Offensive spend medians $m 2022-26: 0.3, 2.0, 6.0, 12.0, 22.0 (log-sd 0.85)", "0.3 ... 22.0", "ASSUMED",
    "a deliberately generous guess at what attackers spend; not in data/")
add("11", "Market-research anchors: Mordor Intelligence $16.44bn (2025) and $20.58bn (2026); Precedence Research $19.45bn (2026)",
    "see docstring", "NOT IN DATA", "G_vendor_ai_sources.md and the bibliography list the pages")

# ======================================================================================================== chart 12
def jrow(metric):
    d = J_VULNS[J_VULNS.metric.str.contains(metric, regex=False, na=False)]
    assert len(d) == 1, (metric, len(d))
    return d.iloc[0]


reported, patched = jrow("findings reported to maintainers"), jrow("patched upstream")
tracked, exploited = jrow("vulnerabilities attributed to AI-assisted discovery"), jrow("confirmed exploited in the wild")
add("12", "Funnel: 6,157 reported; 516 patched", "6157, 516", verdict((reported.value, patched.value) == (6157, 516), "MATCH"),
    "J_ai_vulns.csv value column")
rn = str(reported.notes)
add("12", "Funnel: 29,439 flagged; 5,103 acknowledged", "29439, 5103", verdict("29439" in rn and "5103" in rn, "MATCH"),
    "J_ai_vulns.csv notes of the 6,157 row ('29439 candidates; ... 5103 acknowledged')")
add("12", "14 exploited of 1,061 AI-found flaws tracked", "14, 1061", verdict((exploited.value, tracked.value) == (14, 1061), "MATCH"),
    "J_ai_vulns.csv value column")
add("12", "All-flaws benchmark: about 1.4%", "1.4%", verdict("~1.4%" in str(exploited.notes), "MATCH"), "J_ai_vulns.csv notes of the 14 row")
add("12", "'Nine in ten reports checked by outsiders proved real' (note)", "90%",
    verdict("5674 of 6123 externally reviewed confirmed valid" in rn and 5674 / 6123 > 0.9, "DERIVED"),
    f"notes of the 6,157 row: 5,674 of 6,123 externally reviewed confirmed valid = {5674 / 6123:.1%}")
add("12", "'Only one in 12 ... has been patched' (title)", "1 in 12", verdict(round(6157 / 516) == 12, "DERIVED"), f"6,157 / 516 = {6157 / 516:.1f}")

# ================================================================================================================ report
ORDER = {"FAIL": 0, "OVERRIDE": 1, "NOTE": 2, "ASSUMED": 3, "NOT IN DATA": 4, "APPROX": 5, "DERIVED": 6, "MATCH": 7}


def table():
    lines = ["| Chart | What is typed | Typed value | Status | Where it comes from, and what was checked |", "|---|---|---|---|---|"]
    for chart, what, typed, status, ev in CHECKS:
        cells = [chart, what, "`" + typed.replace("|", "/") + "`", f"**{status}**" if status != "MATCH" else status, ev]
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--update-docs", metavar="FILE", help="rewrite the table between <!-- BEGIN CHECKS --> and <!-- END CHECKS -->")
    args = ap.parse_args()
    counts = {}
    for chart, what, typed, status, ev in CHECKS:
        counts[status] = counts.get(status, 0) + 1
        if not args.update_docs:
            print(f"[{status:11s}] chart {chart:>2s}  {what}\n{'':16s}typed {typed}  |  {ev}")
    print("\n" + "  ".join(f"{k} {counts[k]}" for k in sorted(counts, key=ORDER.get)) + f"   (total {len(CHECKS)})")
    if args.update_docs:
        p = Path(args.update_docs)
        text = p.read_text()
        pat = re.compile(r"(<!-- BEGIN CHECKS -->).*?(<!-- END CHECKS -->)", re.S)
        assert pat.search(text), "markers not found"
        p.write_text(pat.sub(lambda m: m.group(1) + "\n" + table() + "\n" + m.group(2), text))
        print("updated", p)
    if counts.get("FAIL"):
        print("\nSome typed numbers contradict the data: see the FAIL lines above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
