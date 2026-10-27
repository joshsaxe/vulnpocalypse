"""Chart 7 — security agencies (and their contractors) pay engineers a fraction of what private firms do.

Data: data/F_pay.csv. State side: advertised pay scales and job adverts (NSA, GCHQ and the
National Cyber Force, the NCSC), an official Israeli wage report (via Ynet) and a leaked salary sheet from i-Soon, a
contractor to China's security ministries. Private side: Levels.fyi median total pay of ML/AI software engineers in
each country, and of all OpenAI and Anthropic engineers. US dollars a year at market exchange rates.

Bayesian estimate: for each country and side, typical pay P is estimated on the log scale from the sources listed in
USE. Each source is a noisy measurement of log P: the midpoint of its range, with a standard deviation that adds
(a) source quality (grade A 0.15, B 0.25, C 0.40, D 0.60), (b) half the width of an advertised range and (c) 0.25 for
role mismatch. The prior is deliberately vague (log-normal centred on $80,000 with sd 10 in log units, i.e. essentially flat), so the data
decide. The private/state ratio is computed draw by draw, so its interval reflects both sides. Pensions and job
security, which narrow public-private gaps, are excluded. Russia and Iran publish nothing comparable.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from common.chart import *

F = pd.read_csv(DATA / "F_pay.csv")
GRADE_SD = {"A": 0.15, "B": 0.25, "C": 0.40, "D": 0.60}
ROLE_SD = 0.25
USE = {
    "United States": {"state": [0, 1, 7], "private": [11], "frontier": [14, 15]},
    "United Kingdom": {"state": [17, 18, 19, 20, 21, 22], "private": [24]},
    "Israel": {"state": [32, 33, 34, 35], "private": [39]},
    "China": {"state": [41], "private": [42]},
}
rng = np.random.default_rng(66)


def posterior(rows, n=60000, prior_sd=10.0):
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


q = lambda x: [round(float(t)) for t in np.quantile(x, [0.1, 0.5, 0.9])]
qr = lambda x: [round(float(t), 2) for t in np.quantile(x, [0.1, 0.5, 0.9])]
res = {}
for c, sides in USE.items():
    d = {k: posterior(v) for k, v in sides.items()}
    res[c] = {"state": q(d["state"]), "private": q(d["private"]), "ratio": qr(d["private"] / d["state"])}
    if "frontier" in d:
        res[c]["frontier"] = q(d["frontier"])
        res[c]["frontier_ratio"] = qr(d["frontier"] / d["state"])
dump_json(res, RESULTS / "c07_pay.json")
print(json.dumps(res, indent=1))

order = ["United States", "United Kingdom", "Israel", "China"]
sub = {"United States": "NSA and other agencies", "United Kingdom": "GCHQ, NCSC",
       "Israel": "Army, Mossad, Shin Bet*", "China": "i-Soon (a contractor), 2022"}
EN = "\u2013"
C = Chart(7, "Private firms pay AI engineers about two to three times what Western agencies do",
          "Typical annual pay, $ at market exchange rates, log scale",
          "Sources: USAJOBS (NSA adverts); Federal News Network; GCHQ, National Cyber Force and NCSC adverts (via "
          "Flexa and The Register); Israeli Finance Ministry via Ynet; AP (i-Soon leak); Levels.fyi; author's "
          "Bayesian measurement model (dots: medians; bars: 80% credible intervals)",
          note=("Private: median pay of ML/AI engineers, including stock. State pay excludes pensions and job "
                "security. *Averages for all staff, not just engineers. Russia and Iran publish nothing comparable."),
          plot_h_in=2.45)
TW = C.width_in - 0.24
CC, RL, PAD, RC = 1.02, 1.56, 0.08, 1.0       # country column, row-label column, gaps, ratio column (inches)
PW = TW - CC - RL - 2 * PAD - RC
ax = C.axes(((CC + RL + 2 * PAD) / TW, 0.13, PW / TW, 0.80))
hbar_axis(ax)
ax.set_xscale("log")
ax.set_xlim(5000, 6.0e5)
ax.set_xticks([10000, 100000])
ax.set_xticklabels(["$10k", "$100k"])
ax.minorticks_off()
ys = np.arange(len(order))[::-1] * 1.12
ticks, tlabels, tcols = [], [], []
for y, c in zip(ys, order):
    r = res[c]
    for side, col, dy, lab in (("state", GOV, 0.2, sub[c]), ("private", PRIV, -0.2, "Private firms")):
        lo, mid, hi = r[side]
        model_bar(ax, lo, hi, y + dy, col, lw=4.5, alpha=0.3)
        ax.plot(mid, y + dy, "o", color=col, ms=7.5, mec="white", mew=1.2, zorder=3)
        ticks.append(y + dy); tlabels.append(lab); tcols.append(INK if side == "state" else SECOND)
    ax.text(-(CC + RL + 2 * PAD) / PW, y + 0.2, c, transform=ax.get_yaxis_transform(), va="center_baseline", ha="left",
            fontsize=SMALL + 0.6, fontweight="bold", color=INK)
    lo, mid, hi = r["ratio"]
    t = ax.text(1 + 0.12 / PW, y, f"{mid:.1f}\u00d7", transform=ax.get_yaxis_transform(), va="center", ha="left",
                fontsize=LABEL, color=INK, fontweight="bold")
    ax.annotate(f" ({lo:.1f}{EN}{hi:.1f})", xycoords=t, xy=(1, 0.5), va="center", ha="left", fontsize=MIN,
                color=SECOND)
ax.text(1 + 0.12 / PW, max(ys) + 0.62, "Private \u00f7 state", transform=ax.get_yaxis_transform(), va="center",
        ha="left", fontsize=MIN, color=SECOND)
ax.set_yticks(ticks)
ax.set_yticklabels(tlabels, fontsize=SMALL + 0.4)
ax.tick_params(axis="y", pad=PAD * 72)
for lab, col in zip(ax.get_yticklabels(), tcols):
    lab.set_color(col)
ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)
C.save(str(FIGURES / "c07_pay"))
