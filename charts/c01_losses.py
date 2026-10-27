"""Chart 1 — estimated global losses to fraud and hacking, 2015-2025 (and a 2026 projection), and the part that
would not have happened without AI.

Model: models/c01_loss_trend.py (writes results/c01_loss_trend.json and results/c01_loss_trend_draws.npz).
Methods: docs/METHODS.md (the article's Appendix A).
Landscape, two panels. Left: one column per year, fraud stacked on hacking (medians), the AI-caused part marked in
amber at the top of each column from 2023, and a whisker for the 80% credible interval of the total. The 2026 column
is a one-year projection from the 2022-25 trend (the model's own forecast machinery), drawn faded with a dashed
outline. Right: 2025 as a grid in which each square is $1bn, so the AI part (amber, with its upper 80% range in pale
amber) is unmistakable. The pre-2022 trend test is described in docs/METHODS.md (Appendix A), not drawn.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import FIGURES, RESULTS
import json
import numpy as np
from matplotlib.patches import Rectangle
from common.chart import *

R = json.load(open(RESULTS / "c01_loss_trend.json"))
D = np.load(RESULTS / "c01_loss_trend_draws.npz")
yrs = np.array(R["years"])
i0 = list(yrs).index(2015)
YR = yrs[i0:]
F, H = D["fraud"][:, i0:], D["hack"][:, i0:]
A = D["aiF"][:, i0:] + D["aiH"][:, i0:]
f_med, h_med, a_med = np.median(F, 0), np.median(H, 0), np.median(A, 0)
t_q = np.quantile(F + H, [0.1, 0.5, 0.9], axis=0)
tot = R["total_2025"]
sh_all = R["ai_share_total_2025"]
ai_all = R["ai_total_2025"]
# 2026 projection
f26m, h26m = float(np.median(D["fraud26"])), float(np.median(D["hack26"]))
a26m = float(np.median(D["aiF26"] + D["aiH26"]))
t26 = np.quantile(D["fraud26"] + D["hack26"], [0.1, 0.9])
ai26 = R["ai_total_2026"]
XP = 2026.0
EN = "–"

C = Chart(1, f"AI probably caused less than 5% of the \\${round(tot[1], -2):.0f}bn lost to cybercrime in 2025",
          "Estimated global losses to fraud and hacking, $bn at 2025 prices",
          "Sources: FBI IC3; FTC; UK Finance; ACCC; Japan's National Police Agency; Canadian Anti-Fraud Centre; "
          "Singapore and Hong Kong police; EBA; ECB; Chainalysis; FinCEN; ITRC; IBM; Sophos; ransomware.live; "
          "Verizon; Heiding et al.; national price indices; author's Bayesian dynamic-factor model of "
          f"{R['n_series']} series and Monte Carlo estimate of AI's share",
          note=("Columns: median estimates; whiskers: 80% credible intervals for the total, mostly uncertainty about "
                "the overall level (growth is better determined). The 2026 column is a one-year projection from the "
                "2022-25 trend, with wider bands. *Losses that would not have happened without AI: the author's "
                f"estimate, not a measurement; 2025 central estimate \\${ai_all[1]:.0f}bn (2026 projection about "
                f"\\${ai26[1]:.0f}bn), 2025 80% range \\${ai_all[0]:.1f}bn{EN}{ai_all[2]:.0f}bn."),
          plot_h_in=2.7)
TW = C.width_in - 0.24
LW = 3.55                      # left panel width, inches
RX = LW + 0.42                 # right panel starts here
RW = TW - RX

# ---------------------------------------------------------------- left: losses by year
YL = 0.34                      # room for the y labels, inches
ax = C.axes((YL / TW, 0.10, (LW - YL) / TW, 0.80))
style_axis(ax, yright=False)
ax.tick_params(axis="y", labelsize=TICK, pad=3)
x = YR.astype(float)
w = 0.68
ax.bar(x, h_med, width=w, color=HACK, lw=0, zorder=2)
ax.bar(x, f_med, bottom=h_med, width=w, color=FRAUD, lw=0, zorder=2)
top = f_med + h_med
for xi, ti, ai in zip(x, top, a_med):
    if ai > 0.05:
        ax.bar(xi, ai, bottom=ti - ai, width=w, color=AI, lw=0, zorder=3)
for xi, lo, hi in zip(x, t_q[0], t_q[2]):
    ax.plot([xi, xi], [lo, hi], color=SECOND, lw=0.7, zorder=4, solid_capstyle="butt")
# 2026: a one-year projection, faded with a dashed outline
ax.bar(XP, h26m, width=w, color=HACK, lw=0, zorder=2, alpha=0.4)
ax.bar(XP, f26m, bottom=h26m, width=w, color=FRAUD, lw=0, zorder=2, alpha=0.4)
if a26m > 0.05:
    ax.bar(XP, a26m, bottom=h26m + f26m - a26m, width=w, color=AI, lw=0, zorder=3, alpha=0.7)
ax.bar(XP, h26m + f26m, width=w, facecolor="none", edgecolor=SECOND, lw=0.8, ls=(0, (2, 1.4)), zorder=3)
ax.plot([XP, XP], [t26[0], t26[1]], color=SECOND, lw=0.7, zorder=4, solid_capstyle="butt")
ax.set_xlim(2014.4, 2026.9)
ax.set_ylim(0, 590)
ax.set_yticks([0, 100, 200, 300, 400, 500])
ax.set_xticks([2015, 2017, 2019, 2021, 2023, 2025, 2026])
ax.set_xticklabels(["2015", "2017", "2019", "2021", "2023", "2025", "'26"])
ax.tick_params(axis="x", length=0, pad=4)
cg = 2022.5
ax.plot([cg, cg], [0, 470], color=SECOND, lw=0.8, ls=(0, (1, 2)), zorder=1)
halo_text(ax, cg - 0.12, 505, "ChatGPT launched", ha="right", va="top", fontsize=MIN, color=SECOND)
# legend, top left
key(ax, 0.02, 0.9, "Fraud and scams", FRAUD, kind="patch", size=SMALL + 0.2, gap=0.012)
key(ax, 0.02, 0.83, "Hacking", HACK, kind="patch", size=SMALL + 0.2, gap=0.012)
key(ax, 0.02, 0.735, "Caused by AI*", AI, kind="patch", size=SMALL + 0.2, gap=0.012)
ax.plot([0.037, 0.037], [0.645, 0.705], color=SECOND, lw=0.8, transform=ax.transAxes, clip_on=False)
ax.text(0.066, 0.675, "80% credible interval", transform=ax.transAxes, fontsize=SMALL + 0.2, color=INK,
        va="center", ha="left")
ax.add_patch(Rectangle((0.02, 0.57), 0.034, 0.045, transform=ax.transAxes, facecolor=GREY, alpha=0.4,
                       edgecolor=SECOND, lw=0.8, ls=(0, (2, 1.4)), clip_on=False))
ax.text(0.066, 0.59, "2026: projected", transform=ax.transAxes, fontsize=SMALL + 0.2, color=INK, va="center",
        ha="left")

# ---------------------------------------------------------------- right: 2025, each square $1bn
fq25, hq25 = f_med[-1], h_med[-1]
n_total = int(round(fq25) + round(hq25))            # squares: sum of the two medians, $bn
n_ai = int(round(ai_all[1]))                         # central estimate of the AI part
n_ai_hi = int(round(ai_all[2]))                      # upper end of its 80% range
NC, NR = 20, 15
GB, GH = 0.27, 0.636            # grid bottom and height, as shares of the plot height (square cells)
bx = C.axes((RX / TW, GB, RW / TW, GH))
bx.set_xlim(0, NC)
bx.set_ylim(0, NR)
bx.axis("off")
cell, sq = 1.0, 0.80
for k in range(n_total):
    r_, c_ = divmod(k, NC)
    col = AI if k < n_ai else (AI_LIGHT if k < n_ai_hi else LIGHT)
    bx.add_patch(Rectangle((c_ + (cell - sq) / 2, NR - 1 - r_ + (cell - sq) / 2), sq, sq, facecolor=col, lw=0))
C.text(RX / TW, GB + GH + 0.03, "2025: each square is \\$1bn", fontsize=LABEL, fontweight="bold", color=INK,
       ha="left", va="bottom")
# legend under the grid
for i, (col, txt) in enumerate([(AI, f"Caused by AI*: about \\${ai_all[1]:.0f}bn ({sh_all[1]*100:.1f}%)"),
                                 (AI_LIGHT, f"AI*'s upper range: up to \\${ai_all[2]:.0f}bn"),
                                 (LIGHT, f"Everything else: about \\${round(n_total - n_ai, -1):.0f}bn")]):
    yy = GB - 0.075 - i * 0.075
    x_in = RX + 0.012
    C.fig.add_artist(Rectangle((C.region[0] + (x_in / TW) * C.region[2], C.region[1] + yy * C.region[3] - 0.045 / C.H),
                               0.09 / C.width_in, 0.09 / C.H, transform=C.fig.transFigure, facecolor=col, lw=0))
    C.text((RX + 0.17) / TW, yy, txt, fontsize=SMALL + 0.2, color=INK, ha="left", va="center")
C.save(str(FIGURES / "c01_losses"))
print("ok 2026:", round(h26m), round(f26m), round(h26m + f26m), "AI", round(a26m, 2), "whisker", t26.round().tolist())
