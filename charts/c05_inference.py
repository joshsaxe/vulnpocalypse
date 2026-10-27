"""Chart 5 — how long hacking and fraud operations kept using rented AI before the provider cut them off, and
the operations no provider cut off.

Data: data/D_platform_cases.csv: disruption reports by OpenAI, Anthropic and Microsoft, 2024-26.
CAUGHT: the nine hacking and fraud cases whose reports bound how long the abuse ran before the provider cut it off.
Influence operations, a model-copying campaign and a ban at sign-up are left out. Where a report gives only one
bound we assume the other (ASSUME, shown in the note). NOT CUT OFF: cases in the same table where no AI provider ended
the operation (self-hosted or reseller models, or a ban that came after the system had moved to local models).

Bayesian estimate: for each case the duration is taken as log-uniform between its bounds; for each Monte Carlo draw
we count cases cut off within 30 days and cases lasting 180 days or more, and combine the counts with a uniform
Beta(1,1) prior to get the population shares (median and 80% interval). These are shares of operations that were
caught and disclosed; disclosures cover only about 2.7 years, so long-running recent operations are missing and the
true durations are probably longer.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from common.chart import *

CAUGHT = [  # case_id, label, lo, hi, sub-label   (every hacking, fraud or spying case whose provider cut it off
    # and whose report bounds how long it ran; OpenAI's scam-ring bans are left out because "in the last three
    # months" is a reporting window, not a duration)
    ("ANT-2026-09-GTG50020", "Russian-speaking gang", 4, 26, None),
    ("ANT-2025-08-GTG2002", "'Vibe-hacking' extortionist", 7, 30, None),
    ("ANT-2025-11-GTG1002", "Chinese state spies", 10, 60, None),
    ("ANT-2026-09-GTG50014", "ShinyHunters affiliates", 21, 21, None),
    ("ANT-2026-09-GTG50029", "French hacktivist", 30, 148, None),
    ("OAI-2025-04-AKIRABOT", "AkiraBot spam tool", 180, 225, "found by SentinelOne"),
    ("MS-2026-09-EVILTOKENS", "EvilTokens phishing service", 213, 213, "also seized by court order"),
    ("ANT-2025-08-GTG5004", "AI-built ransomware seller", 180, 225, "sold kits on dark-web forums"),
    ("SVC-XANTHOROX", "Xanthorox 'dark AI'", 290, 315, "ran on Google's Gemini"),
]
NOTCUT = [  # case_id, label, lo, hi, still running, note
    ("CS-2026-10-ARTEX", "ARTEX vs Korean lenders", 7, 21, False, "DeepSeek via a reseller"),
    ("AWS-2026-02-FORTIGATE", "FortiGate break-ins", 38, 38, False, "found by Amazon; no ban reported"),
    ("SVC-WORMGPT", "WormGPT (2023)", 62, 188, False, "self-hosted; quit"),
    ("ANT-2025-08-VIETNAM", "Chinese spies vs Vietnam", 270, 270, False, "caught; no ban reported"),
    ("ANT-2026-09-GTG50027", "Malian surveillance system", 263, 263, True, "banned; ran on local models"),
    ("SVC-GHOSTGPT", "GhostGPT chatbot", 610, 610, True, "still sold in September 2026"),
]
D = pd.read_csv(DATA / "D_platform_cases.csv").set_index("case_id")
for c in CAUGHT + NOTCUT:
    assert c[0] in D.index, c[0]
rng = np.random.default_rng(44)
lo = np.array([c[2] for c in CAUGHT], float)
hi = np.array([c[3] for c in CAUGHT], float)
ex = np.isclose(lo, hi)
lo_i, hi_i = np.where(ex, lo * 0.8, lo), np.where(ex, hi * 1.2, hi)
N = 20000
u = rng.uniform(size=(N, len(CAUGHT)))
dur = np.exp(np.log(lo_i) + u * (np.log(hi_i) - np.log(lo_i)))
k30 = (dur <= 30).sum(1)
k180 = (dur >= 180).sum(1)
n = len(CAUGHT)
s30 = rng.beta(1 + k30, 1 + n - k30)
s180 = rng.beta(1 + k180, 1 + n - k180)
q = lambda a: [round(float(v), 3) for v in np.quantile(a, [0.1, 0.5, 0.9])]
raw30 = int(np.sum(hi <= 30))
raw180 = int(np.sum(lo >= 180))
res = {"n_caught": n, "share_within_30d": q(s30), "share_180d_plus": q(s180), "raw_within_30d": raw30,
       "raw_180d_plus": raw180, "sample_median_days": float(np.median(np.sqrt(lo * hi)))}
dump_json(res, RESULTS / "c05_inference.json")
print(json.dumps(res, indent=1))
EN = "\u2013"
s30q = res["share_within_30d"]
C = Chart(5, "AI firms cut some abusers off within weeks, but as many run for half a year",
          "Malicious operations using AI models, by how long each ran, log scale",
          "Sources: Anthropic, OpenAI, Microsoft and Google threat reports; SentinelOne; CrowdStrike; Amazon; Krebs "
          "on Security; Cato Networks; Abnormal Security; KELA; author's beta-binomial estimate (in note; 80% "
          "credible interval)",
          note=(f"Lines: published ranges; one bound assumed where a report gives only one. Arrows: still running. "
                f"Of the nine cut off, three or four went within a month (estimated share {s30q[1]*100:.0f}%, "
                f"{s30q[0]*100:.0f}{EN}{s30q[2]*100:.0f}%) and four lasted six months or more. Only cases caught "
                "and disclosed appear."),
          plot_h_in=3.0)
TW = C.width_in - 0.24                      # text width, inches
PAD = 0.08                                  # label-to-plot gap, inches
LW_L, LW_R, GAP_P = 1.56, 1.50, 0.25        # label columns and gap between panels, inches
PW = (TW - LW_L - LW_R - 2 * PAD - GAP_P) / 2
BOT, HGT = 0.10, 0.81
YMIN, YMAX = -12.45, 0.35


def panel(x0_in, lw_in, rows, color, head, cut):
    ax = C.axes(((x0_in + lw_in + PAD) / TW, BOT, PW / TW, HGT))
    hbar_axis(ax)
    ax.set_xscale("log")
    ax.set_xlim(0.8, 1600)
    ax.set_xticks([1, 30, 365])
    ax.set_xticklabels(["1 day", "1 month", "1 year"], fontsize=SMALL)
    ax.minorticks_off()
    ax.axvline(30, color=AXIS, lw=0.8, ls=(0, (2, 2)), zorder=1)
    ys, labels = [], []
    y = 0.0
    for r in rows:
        lab, l_, h_, sub = r[1], r[2], r[3], r[-1]
        ongoing = (not cut) and r[4]
        y -= 1.0 if sub is None else 1.72
        yl = y + (0.36 if sub else 0)
        ys.append(yl)
        labels.append(lab)
        if sub:
            ax.text(-PAD / PW, y - 0.36, sub, transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=MIN, color=SECOND)
        if h_ > l_ * 1.05:
            data_range(ax, l_, h_, yl, color, tick=0.17, lw=1.4)
        elif ongoing:
            ax.plot(h_, yl, "o", mfc="white", mec=color, mew=1.6, ms=6.5, zorder=3)
            ax.annotate("", xy=(h_ * 2.3, yl), xytext=(h_ * 1.12, yl),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3, mutation_scale=8))
        else:
            ax.plot(h_, yl, "o", color=color, ms=6.5, mec="white", mew=1.0, zorder=3)
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=SMALL + 0.4, color=INK)
    ax.tick_params(axis="y", pad=PAD * 72)
    ax.set_ylim(YMIN, YMAX)
    ax.text(-(lw_in + PAD) / PW, YMAX + 0.25, head, transform=ax.get_yaxis_transform(), fontsize=MIN,
            fontweight="bold", color=SECOND, va="bottom", ha="left")
    return ax


panel(0.0, LW_L, CAUGHT, HACK, "CUT OFF BY THEIR AI PROVIDER", True)
panel(LW_L + PAD + PW + GAP_P, LW_R, [(c[0], c[1], c[2], c[3], c[4], c[5]) for c in NOTCUT], GREY,
      "NOT STOPPED BY THEIR AI PROVIDER", False)
C.save(str(FIGURES / "c05_inference"))
