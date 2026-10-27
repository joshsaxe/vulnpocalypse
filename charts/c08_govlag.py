"""Chart 8 — how far America's defence and intelligence agencies lag business in adopting new technology.

Data: data/G_adoption.csv: for each technology invented outside government, a range of years in
which it became mainstream in American business and a range in which it became mainstream in US defence and
intelligence agencies (milestones differ by row: a policy memo, a big contract, a new organisation, user counts).
Two grade-D rows (PCs, corporate e-mail and web) are excluded; the Covid-era switch to video calls is shown but not
fitted (an emergency, not routine adoption).

Model (Bayesian, interval-censored): lag L_i is known only to lie in [NS_low - business_high, NS_high - business_low];
log L_i ~ Normal(a + b (year_i - 2015), s); priors a ~ N(log 5, 1), b ~ N(0, 0.1), s ~ HalfNormal(0.7); adaptive
Metropolis. Fitted twice: with all rows, and without the generative-AI row, the only recent point, which carries
much of the trend. Projection: AI agents for offensive cyber operations, with business adoption in 2025-26 and a lag
drawn from each fit's posterior predictive. The two fits' draws are pooled with equal weight and then conditioned on
'not yet' (a date after October 2026); that keeps about 70% of the draws of the first fit and 90% of the second, so the
mixture is about 44% the all-rows fit and 56% the fit without generative AI.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from scipy import stats
from common.bayes import metropolis
from common.chart import *

D = pd.read_csv(DATA / "G_adoption.csv")
LABELS = {
    "Open-source software": "Open-source software",
    "Agile / DevSecOps": "Agile development",
    "Smartphones / mobile devices": "Smartphones",
    "Commercial cloud": "Cloud computing",
    "Machine learning (production ML)": "Machine learning",
    "SaaS / video conferencing": "Video calls (Covid)",
    "Generative AI (LLM chatbots)": "Generative-AI chatbots",
}
rows = D[D.technology.isin(LABELS)].copy()
rows["pl"], rows["ph"] = rows.private_mainstream_year_low, rows.private_mainstream_year_high
rows["nl"], rows["nh"] = rows.ns_mainstream_year_low, rows.ns_mainstream_year_high
rows["pm"] = (rows.pl + rows.ph) / 2
rows["lag_lo"] = np.maximum(0.25, rows.nl - rows.ph)
rows["lag_hi"] = np.maximum(rows.lag_lo + 0.25, rows.nh - rows.pl)


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


base = rows[~rows.technology.str.startswith("SaaS")]
nogen = base[~base.technology.str.startswith("Generative")]
res = {}
fits = {}
proj = {}
for name, f, seed in (("all", base, 7), ("without_genai", nogen, 8)):
    a, b, s, rh = fit_rows(f, seed)
    rng = np.random.default_rng(71 + seed)
    pyear = rng.uniform(2025.0, 2026.0, a.size)
    lag_pred = np.exp(a + b * (pyear - 2015) + s * rng.standard_normal(a.size))
    fits[name] = (a, b, s)
    proj[name] = pyear + lag_pred
    res[name] = {"rhat": rh.round(3).tolist(), "p_shrinking": round(float(np.mean(b < 0)), 3),
                 "lag_2005": round(float(np.median(np.exp(a + b * (2005 - 2015)))), 2),
                 "lag_2024": round(float(np.median(np.exp(a + b * (2024 - 2015)))), 2),
                 "lag_2024_q": np.quantile(np.exp(a + b * 9), [0.1, 0.5, 0.9]).round(2).tolist(),
                 "ns_year_q": np.quantile(pyear + lag_pred, [0.1, 0.5, 0.9]).round(1).tolist()}
mix = np.concatenate([proj["all"], proj["without_genai"]])
mix = mix[mix >= 2026.8]          # routine use has not begun as of October 2026
res["mixture"] = {"ns_year_q": np.quantile(mix, [0.1, 0.5, 0.9]).round(1).tolist(),
                  "p_by_end_2029": round(float(np.mean(mix < 2030.0)), 3),
                  "p_by_end_2027": round(float(np.mean(mix < 2028.0)), 3)}
dump_json(res, RESULTS / "c08_govlag.json")
print(json.dumps(res, indent=1))
# the posterior draws that Chart 10 turns into odds-by-year curves (agency adoption not yet happened by Oct 2026)
allf = proj["all"][proj["all"] >= 2026.8]
ngf = proj["without_genai"][proj["without_genai"] >= 2026.8]
np.savez(RESULTS / "c10_draws_agencies.npz", mix=mix, all=allf, nogen=ngf)

EN = "\u2013"
C = Chart(8, "US security agencies adopted chatbots within two years, against four to nine before",
          "When each technology became mainstream in American business and in US defence and intelligence agencies",
          "Sources: Linux Journal; Defense One; DISA; DoD CIO; Washington Technology; CIA and DoD contract "
          "announcements; Wikipedia; DoD CDAO; CDO Magazine; Fortune; Air Force Times; DefenseScoop; McKinsey; "
          "author's Bayesian interval-censored regression of lag on year",
          note=("Dots: midpoints of the range of years (lines) in which each technology became mainstream; milestones "
                "vary by row (a policy memo, a big contract, a new unit or user numbers). Business-side years, except "
                "for generative AI's, and the agencies' years for open source are the author's estimates. Gap: years "
                "from business to the agencies (range in brackets). Projection: hollow dot, median; bar, 80% credible interval."),
          plot_h_in=2.75)
TW = C.width_in - 0.24
LC = 1.95                      # label column, inches
ax = C.axes((LC / TW, 0.10, (TW - LC) / TW, 0.78))
for sname in ("top", "right", "left"):
    ax.spines[sname].set_visible(False)
ax.spines["bottom"].set_color(AXIS)
ax.xaxis.grid(True, color=GRID, lw=0.7, zorder=0)
ax.set_axisbelow(True)
NAMES = {"Open-source software": "Open-source software", "Smartphones / mobile devices": "iPhones",
         "Agile / DevSecOps": "Agile software development", "Commercial cloud": "Cloud computing",
         "Machine learning (production ML)": "Machine learning", "SaaS / video conferencing": "Video calls (Covid emergency)",
         "Generative AI (LLM chatbots)": "Generative-AI chatbots"}
rr = rows.copy()
rr["pmid"] = (rr.pl + rr.ph) / 2
rr["nmid"] = (rr.nl + rr.nh) / 2
rr = rr.sort_values("pmid")
mq = res["mixture"]["ns_year_q"]
items = [(NAMES[r.technology], r.pl, r.ph, r.nl, r.nh, r.lag_lo, r.lag_hi, r.technology.startswith("SaaS"))
         for _, r in rr.iterrows()]
n = len(items) + 1
ys = np.arange(n)[::-1].astype(float)
for (lab, pl, ph, nl, nh, llo, lhi, covid), y in zip(items, ys[:-1]):
    pm, nm = (pl + ph) / 2, (nl + nh) / 2
    cp, cn = (GREY, GREY) if covid else (PRIV, GOV)
    ax.plot([pm, nm], [y, y], color=LIGHT, lw=3.0, zorder=1, solid_capstyle="butt")
    if ph > pl:
        data_range(ax, pl, ph, y, cp, tick=0.13, lw=1.1, zorder=2)
    if nh > nl:
        data_range(ax, nl, nh, y, cn, tick=0.13, lw=1.1, zorder=2)
    ax.plot(pm, y, "o", color=cp, ms=7, mec="white", mew=1.0, zorder=3)
    ax.plot(nm, y, "o", color=cn, ms=7, mec="white", mew=1.0, zorder=3)
    mid = nm - pm
    if covid:
        txt, sub = "0" + EN + "2 years", "in an emergency"
    elif lhi - llo <= 1.01 or mid < 3:
        txt, sub = f"{llo:.0f}{EN}{lhi:.0f} years", None
    else:
        txt, sub = f"{mid:.0f} years", f"({llo:.0f}{EN}{lhi:.0f})"
    t = halo_text(ax, max(nh, nm) + 0.6, y, txt, va="center", ha="left", fontsize=SMALL + 0.4, color=INK,
                  fontweight="normal" if covid else "bold")
    if sub:
        ax.annotate(" " + sub, xycoords=t, xy=(1, 0.5), va="center", ha="left", fontsize=MIN, color=SECOND,
                    path_effects=HALO)
# projection row: AI agents in US offensive cyber operations
y = ys[-1]
ax.plot([2025.5, mq[1]], [y, y], color=LIGHT, lw=3.0, zorder=1, solid_capstyle="butt")
data_range(ax, 2025.0, 2026.0, y, PRIV, tick=0.13, lw=1.1, zorder=2)
ax.plot(2025.5, y, "o", color=PRIV, ms=7, mec="white", mew=1.0, zorder=3)
model_bar(ax, mq[0], mq[2], y, GOV, lw=6, alpha=0.3)
ax.plot(mq[1], y, "o", mfc="white", mec=GOV, mew=1.6, ms=7, zorder=4)
halo_text(ax, mq[2] + 0.5, y, "probably\nby end-2029", va="center", ha="left", fontsize=SMALL + 0.4, color=INK,
          fontweight="bold", linespacing=1.0)
# today
ax.plot([2026.8, 2026.8], [-1.1, 0.45], color=SECOND, lw=0.7, ls=(0, (1, 2)), zorder=1)
ax.text(2026.95, -0.72, "Today", fontsize=MIN, color=SECOND, ha="left", va="center")
# row labels
labels = [it[0] for it in items] + ["AI agents in US offensive\ncyber operations (projected)"]
ax.set_yticks(ys)
ax.set_yticklabels(labels, fontsize=SMALL + 0.4, color=INK, linespacing=1.0)
for lab in ax.get_yticklabels():
    if "Covid" in lab.get_text():
        lab.set_color(SECOND)
    if "projected" in lab.get_text():
        lab.set_fontweight("bold")
ax.tick_params(axis="y", length=0, pad=6)
ax.set_xlim(2003, 2041.5)
ax.set_xticks([2005, 2010, 2015, 2020, 2025, 2030])
ax.tick_params(axis="x", labelsize=TICK)
ax.set_ylim(-1.1, n - 0.2)
# legend above the plot
AW = TW - LC
key(ax, -LC / AW, 1.075, "Mainstream in business", PRIV, kind="dot", size=SMALL + 0.4, ms=7, gap=0.006)
key(ax, -LC / AW + 1.9 / AW, 1.075, "Mainstream in US defence and intelligence agencies", GOV, kind="dot", size=SMALL + 0.4, ms=7,
    gap=0.006)
C.save(str(FIGURES / "c08_govlag"))
