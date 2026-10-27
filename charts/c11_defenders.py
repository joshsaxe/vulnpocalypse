"""The defenders' build-up: an unnumbered lede-style exhibit with two landscape panels.

Left: Bayesian adoption curve, the cumulative number of 34 major security and platform vendors that had shipped a
substantive generative-AI security feature, 2022-2026 (median and 80% credible interval).
Right: estimated annual AI spend on cyber-defence and on cyber-offence, $, log scale, 2022-2026 (median and 80% range,
a judgement Monte Carlo).

MODEL A, vendor adoption. Reads data/G_vendor_ai.csv: vendor, tier, first_year, substance (A/B/C/none), date_conf (A/B/C).
Monte Carlo over two uncertainties:
  - whether a vendor's feature really counts as "substantive": P(count) by grade A 1.0, B 0.95, C 0.60, none 0.0;
  - when it shipped: date_conf A = that year for sure; B = that year w.p. 0.8, else +/-1; C = that year w.p. 0.5,
    +/-1 w.p. 0.2 each, +/-2 w.p. 0.05 each (clipped to 2022-2026).
For each draw we get, for every year, how many of the tracked vendors had shipped by then; we report the median and an
80% credible interval. The denominator is every vendor tracked, including those with no substantive feature.

MODEL B, spend. An order-of-magnitude estimate, not a measurement; intervals are "80% ranges", the article's convention
for a judgement Monte Carlo (as opposed to a data posterior).
Defensive anchors ($bn): the generative-AI cyber-defence market, from two market-research houses that put 2025 at about
$16bn and 2026 at about $20bn, growing ~25% a year (Mordor Intelligence $16.44bn in 2025 and $20.58bn in 2026; Precedence
Research $19.45bn in 2026). Earlier years are the implied back-cast of that trend. These houses' figures are soft and
probably broad, so each year is drawn log-normally around the anchor with a wide spread.
Offensive anchors ($m): a deliberately generous best guess at what attackers spend on AI. Bespoke criminal tools (WormGPT,
FraudGPT and successors) proved thin wrappers or scams with no real revenue; crooks mostly jailbreak the same mainstream
models defenders use, and the API spend behind documented agentic campaigns is small. Spread is wider still.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import matplotlib
matplotlib.rcParams["text.parse_math"] = False
import numpy as np
import pandas as pd
from common.chart import *

YEARS = [2022, 2023, 2024, 2025, 2026]

# ---------------------------------------------------------------------------------------- model A: vendor adoption
P_SUB = {"a": 1.0, "b": 0.95, "c": 0.60, "none": 0.0, "ml-only": 0.0}      # chance a vendor's feature counts, by grade


def vendor_adoption(n=60000, seed=77):
    G = pd.read_csv(DATA / "G_vendor_ai.csv")
    rng = np.random.default_rng(seed)

    def year_draw(y0, conf):
        y0 = int(y0)
        if conf == "A":
            return np.full(n, y0)
        if conf == "B":
            probs = {0: 0.8, -1: 0.1, 1: 0.1}
        else:
            probs = {0: 0.5, -1: 0.2, 1: 0.2, -2: 0.05, 2: 0.05}
        offs = np.array(list(probs))
        pr = np.array(list(probs.values()))
        pr = pr / pr.sum()
        return np.clip(y0 + rng.choice(offs, size=n, p=pr), 2022, 2026)

    M = len(G)
    counted_year = np.full((n, M), 9999)      # the year each vendor counts from, per draw (9999 = never)
    for j, r in G.iterrows():
        grade = str(r.substance).strip().lower()
        p = P_SUB.get(grade, 0.0)
        counts = rng.random(n) < p
        yrs = year_draw(r.first_year if pd.notna(r.first_year) else 2026, str(r.date_conf).strip().upper())
        counted_year[counts, j] = yrs[counts]
    cum = {y: (counted_year <= y).sum(axis=1) for y in YEARS}          # per-draw cumulative count by year

    def band(x):
        return [int(round(float(v))) for v in np.quantile(x, [0.1, 0.5, 0.9])]

    return {
        "n_vendors": int(M),
        "years": YEARS,
        "cum_count": {str(y): band(cum[y]) for y in YEARS},
        "cum_share": {str(y): [round(v / M, 3) for v in band(cum[y])] for y in YEARS},
        "by_tier": {t: int((G.tier == t).sum()) for t in sorted(G.tier.unique())},
        "grades": {g: int((G.substance.str.lower() == g).sum()) for g in ["a", "b", "c", "none", "ml-only"]
                   if (G.substance.str.lower() == g).any()},
    }


# ---------------------------------------------------------------------------------------- model B: spend
# Judgement inputs (medians; defensive in $bn, offensive in $m). Nothing here is read from a data file: see
# docs/PARAMETERS.md for where each anchor comes from.
DEF_BN = {2022: 8.0, 2023: 10.5, 2024: 13.5, 2025: 16.4, 2026: 20.3}
OFF_M = {2022: 0.3, 2023: 2.0, 2024: 6.0, 2025: 12.0, 2026: 22.0}
SIG_DEF = 0.42     # log-sd: 80% range about a factor of 1.9 either side
SIG_OFF = 0.85     # log-sd: 80% range about a factor of 2.9 either side (far more uncertain)


def ai_spend(n=80000, seed=2026):
    rng = np.random.default_rng(seed)

    def draws(median, sig):
        return np.exp(rng.normal(np.log(median), sig, n))

    def band(x):
        return [round(float(v), 4) for v in np.quantile(x, [0.1, 0.5, 0.9])]

    defense = {y: draws(DEF_BN[y], SIG_DEF) for y in YEARS}            # $bn
    offense = {y: draws(OFF_M[y], SIG_OFF) / 1000.0 for y in YEARS}    # -> $bn
    return {
        "years": YEARS,
        "defense_bn": {str(y): band(defense[y]) for y in YEARS},
        "offense_bn": {str(y): band(offense[y]) for y in YEARS},
        "ratio_2026": band(defense[2026] / offense[2026]),
    }


AD = vendor_adoption()
SP = ai_spend()
dump_json({"adoption": AD, "spend": SP}, RESULTS / "c11_defenders.json")
print("vendors", AD["n_vendors"])
for y in YEARS:
    print(y, "cum", AD["cum_count"][str(y)], "share", AD["cum_share"][str(y)])
print("defence 2026 ($bn)", SP["defense_bn"]["2026"])
print("offence 2026 ($bn)", SP["offense_bn"]["2026"])
print("ratio 2026 (def/off)", [round(v) for v in SP["ratio_2026"]])

# ---------------------------------------------------------------------------------------- the chart
YRS = np.array(AD["years"])
M = AD["n_vendors"]
cum = np.array([AD["cum_count"][str(y)] for y in AD["years"]])          # rows: year; cols q10,q50,q90
dfn = np.array([SP["defense_bn"][str(y)] for y in SP["years"]])
off = np.array([SP["offense_bn"][str(y)] for y in SP["years"]])

C = Chart(11, "Defenders embraced AI fast; attackers have barely begun",
          "Left: major vendors shipping generative-AI security features, of 34 tracked. Right: estimated annual AI "
          "spend, $, log scale",
          "Sources: author's vendor census (34 firms, dated to each vendor's first feature); Mordor Intelligence and "
          "Precedence Research (defensive market); Abnormal Security and this article's evidence (attacker side); "
          "author's Bayesian models",
          note=("Left: cumulative count of the 34 security and platform vendors tracked, by the year each first "
                "shipped a substantive generative-AI feature (a copilot or an autonomous agent, not legacy machine "
                "learning); median and 80% credible interval, allowing for uncertainty about dates and about what "
                "counts as substantive. Right: a judgement Monte Carlo, median and 80% range. Defensive spend is the "
                "generative-AI cyber-defence market (two research houses, ~$20bn in 2026); attacker spend is a "
                "generous guess, since bespoke criminal tools proved thin wrappers or scams and crooks mostly "
                "jailbreak mainstream models. Order-of-magnitude, not a measurement."),
          plot_h_in=2.62)
TW = C.width_in - 0.24
LW = 3.02                        # left panel width, inches
RX = LW + 0.52                   # right panel starts here
RW = TW - RX
x = YRS.astype(float)

# ---------------------------------------------------------------- left: vendor adoption
YL = 0.30
axL = C.axes((YL / TW, 0.115, (LW - YL) / TW, 0.76))
style_axis(axL, yright=False)
axL.tick_params(axis="y", labelsize=TICK, pad=3)
axL.fill_between(x, cum[:, 0], cum[:, 2], color=DEF, alpha=0.18, lw=0, zorder=2)
axL.plot(x, cum[:, 1], color=DEF, lw=2.4, zorder=4)
axL.plot(x, cum[:, 1], "o", color=DEF, ms=6, mec="white", mew=1.1, zorder=5)
axL.axhline(M, color=SECOND, lw=0.8, ls=(0, (1, 2)), zorder=1)
halo_text(axL, 2022.05, M - 0.4, f"all {M} tracked", va="top", ha="left", fontsize=MIN, color=SECOND)
axL.set_xlim(2021.8, 2026.3)
axL.set_ylim(0, M + 2)
axL.set_yticks([0, 10, 20, 30])
axL.set_xticks([2022, 2023, 2024, 2025, 2026])
axL.set_xticklabels(["2022", "'23", "'24", "'25", "'26"])
axL.tick_params(axis="x", length=0, pad=4)
# callout on the 2026 median
m26 = cum[-1, 1]
halo_text(axL, 2025.95, m26 - 2.4, f"{m26} of {M}\nby 2026", va="top", ha="right", fontsize=SMALL, color=INK,
          fontweight="bold", linespacing=1.0)
C.text(YL / TW, 0.115 + 0.76 + 0.025, "Vendors with a generative-AI feature", fontsize=LABEL, fontweight="bold",
       color=INK, ha="left", va="bottom")

# ---------------------------------------------------------------- right: spend, defence vs offence
axR = C.axes((RX / TW, 0.115, RW / TW, 0.76))
style_axis(axR, yright=False)
axR.set_yscale("log")
for arr, col in ((dfn, DEF), (off, HACK)):
    axR.fill_between(x, arr[:, 0], arr[:, 2], color=col, alpha=0.15, lw=0, zorder=2)
    axR.plot(x, arr[:, 1], color=col, lw=2.4, zorder=4)
    axR.plot(x, arr[:, 1], "o", color=col, ms=5.5, mec="white", mew=1.0, zorder=5)
axR.set_xlim(2021.8, 2026.3)
axR.set_ylim(1e-4, 7e1)
axR.set_yticks([1e-3, 1e-1, 1e1])
axR.set_yticklabels(["$1m", "$100m", "$10bn"])
axR.minorticks_off()
axR.set_xticks([2022, 2023, 2024, 2025, 2026])
axR.set_xticklabels(["2022", "'23", "'24", "'25", "'26"])
axR.tick_params(axis="x", length=0, pad=4)
axR.tick_params(axis="y", labelsize=TICK, pad=2)
# direct labels on the two lines, at 2026
halo_text(axR, 2025.9, dfn[-1, 1] * 2.6, "On defence", va="bottom", ha="right", fontsize=SMALL + 0.4, color=DEF,
          fontweight="bold")
halo_text(axR, 2025.9, off[-1, 1] * 2.8, "On offence", va="bottom", ha="right", fontsize=SMALL + 0.4, color=HACK,
          fontweight="bold")
# the gap
ratio = SP["ratio_2026"][1]
halo_text(axR, 2024.0, 2.3, f"~{int(round(ratio/100)*100):,}x more\nspent on defence", va="center", ha="center",
          fontsize=SMALL, color=INK, style="italic", linespacing=1.0, zorder=6)
C.text(RX / TW, 0.115 + 0.76 + 0.025, "Estimated annual AI spend", fontsize=LABEL, fontweight="bold", color=INK,
       ha="left", va="bottom")
C.save(str(FIGURES / "c11_defenders"))
print("adoption 2026 median", m26, "of", M, "| defence 2026 $bn", dfn[-1, 1], "| offence 2026 $bn", off[-1, 1],
      "| ratio", ratio)
