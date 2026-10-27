"""Chart 10 -- the chance, year by year, that AI agents running whole intrusions become routine.

Combines the two adoption-lag models behind Chart 6 (criminals) and Chart 8 (US defence and intelligence agencies);
charts/c06_attacker_lag.py and charts/c08_govlag.py save their posterior draws, which this script reads (run them first).

Criminals (Chart 6). Lag from a technology's arrival to widespread criminal use ~ log-normal, fitted by class with
interval-censored scaled cases and right-censored not-yet-scaled cases. Agents running whole intrusions have been around
since early 2025 (1.65 years at October 2026) without becoming widespread. For each posterior draw (mu, sigma) the chance
that they are widespread by date t, given that they are not yet, is
    [F(t - start) - F(elapsed)] / [1 - F(elapsed)],   F = log-normal CDF,
averaged over draws. Solid line: agents as a new business model (class fitted to the 'eco' cases). Dashed line: agents as
a new tool (class fitted to the 'tool' cases, refitted with agentic intrusion as a not-yet-scaled tool).

US agencies (Chart 8). Interval-censored regression of the lag between business and agency adoption on year, fitted with
all rows and without the generative-AI row; business adoption of AI agents in 2025-26; lag from each fit's posterior
predictive; conditioned on agency adoption not having happened by October 2026 (2026.8). Centre line: the two fits mixed
with equal weight before that conditioning (afterwards the all-rows fit supplies about 44% of the draws and the fit without the
generative-AI row about 56%, because the latter puts more of its probability on later dates). The band's edges are the two fits.

'By 2030' means by 1 January 2030, i.e. by the end of 2029.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import FIGURES, RESULTS, dump_json
import json
import numpy as np
from scipy import stats
from common.chart import *

NOW = 2026.8
CR = np.load(RESULTS / "c10_draws_criminals.npz")      # written by charts/c06_attacker_lag.py
GV = np.load(RESULTS / "c10_draws_agencies.npz")       # written by charts/c08_govlag.py
ELAPSED, START = float(CR["elapsed"]), float(CR["start"])


def crim_curve(mu, sg, tg):
    S_el = stats.norm.sf((np.log(ELAPSED) - mu) / sg)
    out = []
    for t in tg:
        F = stats.norm.cdf((np.log(t - START) - mu) / sg)
        out.append(np.mean((F - (1 - S_el)) / S_el))
    return np.array(out)


def gov_curve(x, tg):
    return np.array([np.mean(x < t) for t in tg])


XEND = 2034.0
tg = np.unique(np.r_[np.linspace(NOW, XEND, 90), 2028.0, 2030.0, 2032.0])   # exact points for the quoted values
c_biz = crim_curve(CR["eco_mu"], CR["eco_sigma"], tg)
c_tool = crim_curve(CR["tw_mu"], CR["tw_sigma"], tg)
g_mix = gov_curve(GV["mix"], tg)
g_all = gov_curve(GV["all"], tg)
g_ng = gov_curve(GV["nogen"], tg)
at = lambda arr, t: float(np.interp(t, tg, arr))
res = {}
for t in (2028.0, 2030.0, 2032.0, 2034.0):
    res[str(int(t))] = {"criminals_business_model": round(at(c_biz, t), 3), "criminals_new_tool": round(at(c_tool, t), 3),
                        "agencies_mixture": round(at(g_mix, t), 3), "agencies_all_rows": round(at(g_all, t), 3),
                        "agencies_without_genai": round(at(g_ng, t), 3)}
# years from October 2026 until each curve reaches 50% (read off a fine grid; the curves only rise)
fine = np.linspace(NOW, 2060.0, 20001)
curves = {"criminals_business_model": crim_curve(CR["eco_mu"], CR["eco_sigma"], fine),
          "criminals_new_tool": crim_curve(CR["tw_mu"], CR["tw_sigma"], fine),
          "agencies_mixture": gov_curve(GV["mix"], fine),
          "agencies_all_rows": gov_curve(GV["all"], fine),
          "agencies_without_genai": gov_curve(GV["nogen"], fine)}
res["years_from_now_to_even_odds"] = {k: round(float(np.interp(0.5, v, fine)) - NOW, 1) for k, v in curves.items()}
dump_json(res, RESULTS / "c10_odds.json")
print(json.dumps(res, indent=1))
# cross-check against the Chart 6 / Chart 8 outputs
ref6 = json.load(open(RESULTS / "c06_attacker_lag.json"))
ref8 = json.load(open(RESULTS / "c08_govlag.json"))
print("Chart 6 reference:", ref6["p_agentic_scaled_by"], ref6["p_agentic_scaled_by_if_tool"])
print("Chart 8 reference:", ref8["mixture"])

EN = "–"
pc = lambda v: f"{round(v * 100):.0f}%"
C = Chart(10, "By the end of 2029, AI agents are probably routine in American cyber operations, and may be in crime too",
          "Chance that AI agents running whole intrusions are in widespread use by each date, given that they are not yet",
          "Sources: models of the adoption lags in Charts 6 and 8 (see their sources); author's Bayesian models",
          note=("Criminals: widespread use in crime; solid line, if agents are a new business model; dashed, if a new tool "
                "(Chart 6). Agencies: mainstream in US defence and intelligence agencies; band, models fitted with and "
                "without the generative-AI case, line, their mix (Chart 8). Dates are the start of the year, so 2030 is the "
                "end of 2029. The cases behind both models are few and hand-picked: read the numbers as rough."),
          plot_h_in=2.7)
TW = C.width_in - 0.24
RCOL = 1.60
PW = TW - RCOL
ax = C.axes((0.0, 0.085, PW / TW, 0.835))
for sname in ("top", "right", "left"):
    ax.spines[sname].set_visible(False)
ax.spines["bottom"].set_color(AXIS)
ax.yaxis.grid(True, color=GRID, lw=0.7, zorder=0)
ax.set_axisbelow(True)
X0 = 2026.0
ax.set_xlim(X0, XEND)
ax.set_ylim(0, 1.0)
ax.set_xticks([2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034])
ax.tick_params(axis="x", labelsize=TICK)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels([])
ax.tick_params(axis="y", length=0)
for v, lab in ((0.25, "25"), (0.5, "50"), (0.75, "75"), (1.0, "100%")):
    ax.text(X0 + 0.04, v + 0.012, lab, fontsize=TICK, color=SECOND, ha="left", va="bottom", zorder=1)

# end-of-2029 guide
ax.axvline(2030.0, color=SECOND, lw=0.7, ls=(0, (1, 2)), zorder=1)
ax.text(2030.06, 1.03, "End of 2029", fontsize=SMALL, color=SECOND, ha="left", va="bottom", clip_on=False)
# criminals
ax.fill_between(tg, c_biz, c_tool, color=HACK, alpha=0.15, lw=0, zorder=2)
ax.plot(tg, c_biz, color=HACK, lw=2.2, zorder=4)
ax.plot(tg, c_tool, color=HACK, lw=1.7, ls=(0, (4, 2.2)), zorder=4)
# US agencies
ax.fill_between(tg, g_ng, g_all, color=GOV, alpha=0.13, lw=0, zorder=2)
ax.plot(tg, g_mix, color=GOV, lw=2.2, zorder=5)
ax.text(NOW - 0.06, 0.045, "Today", fontsize=SMALL, color=SECOND, ha="right", va="bottom")

# values at the end of 2029
T = 2030.0
ax.plot(T, at(g_mix, T), "o", ms=6.5, mfc="white", mec=GOV, mew=1.7, zorder=6)
ax.plot(T, at(c_biz, T), "o", ms=6.5, mfc="white", mec=HACK, mew=1.7, zorder=6)
ax.plot(T, at(c_tool, T), "o", ms=6.0, mfc="white", mec=HACK, mew=1.5, zorder=6)
halo_text(ax, T - 0.09, at(g_mix, T) + 0.045, pc(at(g_mix, T)), fontsize=LABEL + 1, fontweight="bold", color=INK,
          ha="right", va="bottom", zorder=7)
halo_text(ax, T - 0.09, at(c_tool, T) - 0.05, pc(at(c_tool, T)), fontsize=LABEL + 1, fontweight="bold", color=INK,
          ha="right", va="top", zorder=7)
halo_text(ax, T + 0.09, at(c_biz, T) - 0.055, pc(at(c_biz, T)), fontsize=LABEL + 1, fontweight="bold", color=INK,
          ha="left", va="top", zorder=7)

# direct labels in the right margin, at the ends of the lines
LX_ = XEND + 0.1
LS = 0.062
def end_label(y, bold, light=None):
    lines = [(bold, "bold")] + ([(light, "normal")] if light else [])
    n_ = len(lines)
    for i, (t_, w_) in enumerate(lines):
        yy = y + (n_ - 1) * LS / 2 - i * LS
        ax.text(LX_, yy, t_, fontsize=SMALL + 0.4, fontweight=w_, color=INK, ha="left", va="center", clip_on=False)
end_label(0.915, "US defence and", "intelligence agencies")
end_label(0.775, "Criminals", "if a new tool")
end_label(0.625, "Criminals", "if a new business model")
C.save(str(FIGURES / "c10_odds"))
