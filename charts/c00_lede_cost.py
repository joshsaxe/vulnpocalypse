"""Lede figure (unnumbered) — how little the automated part of a cyberattack now costs, in AI tokens.

Best available public evidence, each a single documented case:
- Find a software flaw: the per-bug cost of autonomous coding agents on real open-source C/C++ bugs in the CyberGym
  academic test (Lu et al., arXiv:2610.11602, Oct 2026): a cheap open model solved all 20 bugs for $4.38 (about
  $0.22 each); a frontier agent (Codex/GPT-5.5) solved 17 of 20 for $132.65 (about $7.80 each). Range about $0.20-8.
- Break into a top AI lab: the AI tokens Hacktron spent on its two-month project, which reached OpenAI's internal
  code repository; the write-up puts the whole project at "less than $3,000 in tokens".
- Build a browser exploit chain: XBOW reported about $40,000 in API fees for the six-day effort that produced a
  full-chain Chrome exploit (which Google later rewarded with its maximum bounty).
Nominal US dollars, log scale. Only the automated part is priced here; much of a real attack is still done by hand.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import FIGURES, RESULTS, dump_json
import matplotlib
matplotlib.rcParams["text.parse_math"] = False      # render every "$" literally
from common.chart import *

COST = [  # label, low, high (None -> a point), value label
    ("Find a software flaw", 0.22, 7.8, "20¢–$8 each"),
    ("Break into a top AI lab", 3000, None, "under $3,000"),
    ("Build a browser exploit chain", 40000, None, "about $40,000"),
]

C = Chart(0, "If breaking in and finding flaws are this cheap, where are the attacks?",
          "What AI now charges to do each job, in tokens, $, log scale",
          "Sources: Lu et al., CyberGym (2026); Hacktron; XBOW; author's compilation",
          note=("Each figure is one documented public case, not a market average. Finding a flaw: the per-bug cost "
                "of autonomous agents on real open-source bugs in an academic test (CyberGym), from cents with a "
                "cheap model to about $8 with a frontier one. Breaking in: the tokens Hacktron spent reaching "
                "OpenAI's internal code over two months. The exploit chain: XBOW's API bill for a full-chain Chrome "
                "attack, which Google later rewarded with its top bounty. These are only the automated parts of an "
                "attack; much of the rest is still done by hand (see later charts)."),
          plot_h_in=1.72, tag="THE PRICE OF A HACK")
TW = C.width_in - 0.24
LC, PAD = 2.35, 0.10            # label column, gap (inches)
PW = TW - LC - PAD - 0.10
ax = C.axes(((LC + PAD) / TW, 0.17, PW / TW, 0.76))
hbar_axis(ax, xgrid=True)
ax.set_xscale("log")
ax.set_xlim(0.1, 1.3e5)
ax.set_xticks([1, 100, 1e4])
ax.set_xticklabels(["$1", "$100", "$10k"])
ax.minorticks_off()

ys = [0.0, -1.0, -2.0]
for y, (lab, lo, hi, vt) in zip(ys, COST):
    if hi is not None:
        data_range(ax, lo, hi, y, AI, tick=0.17, lw=1.6, zorder=3)
        halo_text(ax, hi * 1.6, y, vt, va="center", ha="left", fontsize=SMALL + 0.8, color=INK, fontweight="bold",
                  zorder=5)
    else:
        ax.plot(lo, y, "o", color=AI, ms=9, mec="white", mew=1.2, zorder=4)
        if lo >= 2e4:                 # near the right edge: label to the left of the dot
            halo_text(ax, lo / 1.7, y, vt, va="center", ha="right", fontsize=SMALL + 0.8, color=INK,
                      fontweight="bold", zorder=5)
        else:
            halo_text(ax, lo * 1.7, y, vt, va="center", ha="left", fontsize=SMALL + 0.8, color=INK,
                      fontweight="bold", zorder=5)
ax.set_ylim(-2.7, 0.7)
ax.set_yticks(ys)
ax.set_yticklabels([c[0] for c in COST], fontsize=SMALL + 1.4, color=INK)
ax.tick_params(axis="y", length=0, pad=PAD * 72)
C.save(str(FIGURES / "c00_lede_cost"))
dump_json({"costs_usd": {lab: {"low": lo, "high": hi if hi is not None else lo} for lab, lo, hi, _ in COST}},
          RESULTS / "c00_lede_cost.json")
print("ok")
