"""Chart 12 — AI finds software flaws far faster than they are fixed; AI-found flaws are exploited at the usual rate.

Data: every count below is in data/J_ai_vulns.csv: 6,157, 516, 1,061 and 14 in its value column; 29,439 candidate findings
and 5,103 acknowledged in the notes of the 6,157 row; the 1.4% benchmark in the notes of the 14 row. They are typed in
this script, and tools/check_inputs.py confirms each one against the file.
Funnel: Anthropic's coordinated-disclosure dashboard (2 October 2026): 29,439 candidate findings, 6,157 reported to the
maintainers of 591 projects (5,674 of 6,123 externally reviewed confirmed valid), 5,103 acknowledged, 516 patched
upstream. Exploitation: VulnCheck's tracker of AI-attributed vulnerabilities (28 July 2026): 14 of 1,061 confirmed
exploited in the wild; all-CVE ratio of known-exploited to published vulnerabilities in 1H 2026, about 1.4%.

Bayesian estimate: probability that an AI-found flaw is exploited, Beta(1,1) prior + 14 of 1,061 -> Beta(15, 1048);
median and 80% interval. Caveat: AI-found flaws are mostly recent and exploitation accrues over years, so the rate
may rise.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import FIGURES, RESULTS, dump_json
import json
import numpy as np
from scipy import stats
from common.chart import *

FUN = [("Flagged by AI as possible flaws", 29439), ("Reported to software maintainers", 6157),
       ("Acknowledged by maintainers", 5103), ("Patched", 516)]
a, b = 1 + 14, 1 + 1061 - 14
qq = stats.beta.ppf([0.1, 0.5, 0.9], a, b) * 100
res = {"p_exploit_pct_q": [round(float(v), 2) for v in qq], "patched_share_of_reported": round(516 / 6157, 3)}
dump_json(res, RESULTS / "c12_funnel.json")
print(res)

EN = "\u2013"
C = Chart(12, "Only one in 12 flaws that AI found and reported has been patched so far",
          "Flaws found with AI in Anthropic's disclosure programme, by stage, to October 2nd 2026",
          "Sources: Anthropic (vulnerability-disclosure dashboard); VulnCheck; author's beta-binomial estimate (dot: "
          "observed share; bar: 80% credible interval)",
          note=("Counts are Anthropic's own; nine in ten reports checked by outsiders proved real. Many reports are "
                "recent, so the patched share, and the AI-found exploitation rate, may rise. The all-flaws figure is "
                "a rough benchmark, not a like-for-like rate."),
          plot_h_in=2.25)
TW = C.width_in - 0.24
LW = 3.45                 # funnel panel width, inches
RX = 3.95                 # exploitation panel starts here, inches
RW = TW - RX - 0.05
ax = C.axes((0.0, 0.03, LW / TW, 0.94))
hbar_axis(ax, xgrid=False)
ax.spines["bottom"].set_visible(False)
ys = np.arange(len(FUN))[::-1] * 1.55
for y, (lab, v) in zip(ys, FUN):
    if lab.startswith("Flagged"):
        ax.barh(y, v, height=0.62, color="white", edgecolor=DEF, lw=0.9, zorder=2)
        lab = "Flagged by AI as possible flaws (unchecked)"
    else:
        ax.barh(y, v, height=0.62, color=DEF, alpha=0.85, lw=0, zorder=2)
    ax.text(0, y + 0.40, lab, fontsize=SMALL + 0.4, color=INK, va="bottom", ha="left")
    halo_text(ax, v + 500, y, f"{v:,}", fontsize=LABEL, color=INK, va="center", ha="left", fontweight="bold")
ax.set_yticks([])
ax.set_xticks([])
ax.set_xlim(0, 35500)
ax.set_ylim(-0.5, ys[0] + 1.0)
halo_text(ax, 516 + 4600, ys[-1], "about one in 12 reported", fontsize=MIN, color=SECOND, va="center", ha="left")

bx = C.axes((RX / TW, 0.13, RW / TW, 0.66))
hbar_axis(bx, xgrid=False)
C.text(RX / TW, 0.885, "Share exploited in real attacks, %", fontsize=LABEL, fontweight="bold", color=INK,
       ha="left", va="bottom")
rows = [("AI-found flaws tracked by VulnCheck (14 of 1,061)", qq, HACK, 1.25),
        (f"All flaws, Jan{EN}Jun 2026: newly exploited \u00f7 newly published", None, GREY, 0.0)]
for lab, q_, col, y in rows:
    if q_ is not None:
        model_bar(bx, q_[0], q_[2], y, col, lw=4.5, alpha=0.35)
        bx.plot(14 / 1061 * 100, y, "o", color=col, ms=7, mec="white", mew=1.1, zorder=3)
        halo_text(bx, q_[2] + 0.1, y, f"{14/1061*100:.1f}% ({q_[0]:.1f}{EN}{q_[2]:.1f})", fontsize=LABEL,
                  color=INK, va="center", ha="left", fontweight="bold")
    else:
        bx.plot(1.4, y, "o", color=col, ms=7, mec="white", mew=1.0, zorder=3)
        halo_text(bx, 1.4 + 0.12, y, "about 1.4%", fontsize=LABEL, color=INK, va="center", ha="left",
                  fontweight="bold")
    lines = wrap_balanced(lab, RW, SMALL + 0.2)
    for i, ln in enumerate(lines[::-1]):
        bx.text(0, y + 0.28 + i * 0.27, ln, fontsize=SMALL + 0.2, color=INK, ha="left", va="bottom")
bx.set_yticks([])
bx.set_xlim(0, 3)
bx.set_xticks([0, 1, 2, 3])
bx.set_xticklabels(["0", "1", "2", "3%"])
bx.set_ylim(-0.45, 2.05)
C.save(str(FIGURES / "c12_funnel"))
