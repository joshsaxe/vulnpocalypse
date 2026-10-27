"""Chart 4 — Amdahl's law applied to a ransomware gang's labour.

Inputs: data/E_stage_judgements.csv: the author's judgements, for eight stages of a big ransomware
attack, of each stage's share of the gang's working hours and of the share of that stage's work today's best AI
could do unaided. They rest on incident timelines (Colonial Pipeline, Ireland's HSE, Change Healthcare, MGM and
others), leaked gang chats (Conti, Black Basta), NCA data on LockBit's affiliates, Sophos/Mandiant/Coveware timing
statistics and AI-lab threat reports. No public dataset measures labour hours by stage.

Monte Carlo (40,000 draws):
  hour shares   w ~ Dirichlet(c * central), c chosen so the 80% ranges match the stated widths
  AI shares     p_j ~ Beta fitted to each stage's low/central/high judgement (10th/50th/90th percentiles)
  ceiling       1 / (1 - P),  P = sum_j w_j p_j   (today's AI does everything it can, instantly and without error)
  likely today  1 / ((1 - dP) + dP(1/k + v)), with d = share of AI-doable work gangs actually hand to AI
                (80% range 10-80%: unknown, so deliberately wide), k = AI's speed-up on that work (3-20x),
                v = time spent checking AI's work relative to doing it by hand (10-40%)
  future        1 / (1 - (w1 + w2 + w3 + w4) - sum_{j>4} w_j p_j): AI that could do all four technical stages,
                instantly, as well as everything today's AI can already do in the other stages
The stage bars show the author's central judgements (they sum to 100%); the speed-ups use the full distributions.
The judgements describe the hours of one attack, mostly an affiliate's (see data/README.md).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from common.bayes import beta_from_q, beta_from_q3, lognormal_from_q
from common.chart import *

ST = pd.read_csv(DATA / "E_stage_judgements.csv")
ST = ST[ST.stage.str.match(r"^\d")].reset_index(drop=True)
SHORT = ["Get in", "Spread through the network", "Find and steal data", "Disable backups, encrypt",
         "Research victim, write threats", "Negotiate, apply pressure", "Launder and cash out", "Run the platform"]
rng = np.random.default_rng(55)
N = 40000
cen = ST.labour_share_mid.values / ST.labour_share_mid.sum()
target_rel = np.mean((ST.labour_share_high - ST.labour_share_low).values / ST.labour_share_mid.values)
best = None
for c in [5, 8, 12, 16, 20, 25, 30, 40, 50, 60, 75, 90, 120]:
    w = rng.dirichlet(c * cen, 8000)
    rel = np.mean((np.quantile(w, 0.9, axis=0) - np.quantile(w, 0.1, axis=0)) / cen)
    if best is None or abs(rel - target_rel) < best[1]:
        best = (c, abs(rel - target_rel))
W = rng.dirichlet(best[0] * cen, N)
P = np.empty((N, len(ST)))
for j, r in ST.iterrows():
    a, b = beta_from_q3(max(r.ai_automatable_low, 0.01), r.ai_automatable_mid, min(r.ai_automatable_high, 0.99))
    P[:, j] = rng.beta(a, b, N)
Ptot = np.sum(W * P, axis=1)
S_max = 1 / (1 - Ptot)
d = rng.beta(*beta_from_q(0.10, 0.80), N)
mk, sk = lognormal_from_q(3, 20)
k = np.exp(rng.normal(mk, sk, N))
v = rng.beta(*beta_from_q(0.10, 0.40), N)
S_real = 1 / ((1 - d * Ptot) + d * Ptot * (1 / k + v))
tech = np.sum(W[:, :4], axis=1)
nontech_ai = np.sum(W[:, 4:] * P[:, 4:], axis=1)
S_tech = 1 / (1 - tech - nontech_ai)
human_left = W * (1 - P)
q = lambda x: [round(float(t), 3) for t in np.quantile(x, [0.1, 0.5, 0.9])]
res = {"ai_share_of_hours": q(Ptot), "ceiling": q(S_max), "likely": q(S_real), "future_all_technical": q(S_tech),
       "p_ceiling_above_65pc": round(float(np.mean(S_max > 1.65)), 3),
       "technical_share_of_hours": q(tech),
       "share_of_remaining_human_hours_in_technical_stages": q(human_left[:, :4].sum(1) / human_left.sum(1)),
       "stage_share_med": dict(zip(SHORT, [round(float(np.median(W[:, j])), 3) for j in range(len(ST))])),
       "stage_auto_med": dict(zip(SHORT, [round(float(np.median(P[:, j])), 3) for j in range(len(ST))]))}
dump_json(res, RESULTS / "c04_amdahl.json")
print(json.dumps(res, indent=1))

sh = ST.labour_share_mid.values * 100          # the author's central judgements (sum to 100)
au = ST.ai_automatable_mid.values
EN = "\u2013"
sh_ai = res["ai_share_of_hours"]
ceiling = [(t - 1) * 100 for t in res["ceiling"]]      # [44, 63, 89]
exp26 = [(t - 1) * 100 for t in res["likely"]]         # [2, 10, 25]
C = Chart(4, "AI can do two-fifths of a ransomware gang's hours, but lifts its output per hour only about a tenth",
          "The stages of an attack, the hours AI can take on, and the productivity gain by the end of 2026",
          "Sources: post-incident reports (Colonial Pipeline, Ireland's HSE, Change Healthcare, MGM, CDK Global); "
          "Conti and Black Basta chat leaks; NCA; Sophos; Mandiant; Coveware; Chainalysis; GuidePoint; GreyNoise; "
          "Gambit Security; BakerHostetler; Anthropic and Google threat reports; the author's earlier ransomware "
          "model; author's judgements and Monte Carlo model",
          note=("Hour and AI shares are the author's judgements (bars show central ones). Productivity follows "
                "Amdahl's law: automating two-fifths of the hours raises output per hour by at most ~60%, and only if "
                "AI did that work instantly and without error. The end-2026 figure assumes a gang hands AI 10" + EN +
                "80% of what it could do, that AI works 3" + EN + "20 times faster, and that checking takes 10" + EN +
                "40% as long as doing the work by hand. Dots: medians; shaded bars: 80% ranges."),
          plot_h_in=2.72)
TW = C.width_in - 0.24
LCOL, PAD = 1.86, 0.08            # stage-label column and gap, inches
LPW = 1.74                        # stage-bar plot width, inches
RX0 = 4.18                        # right panel starts here, inches from the left of the text area
RPW = TW - RX0 - 0.12             # right panel plot width, inches
BOT, HGT = 0.235, 0.60

# ---- left: the attack as a process, stage by stage; each bar split into AI-doable (amber) and human (grey)
ax = C.axes(((LCOL + PAD) / TW, BOT, LPW / TW, HGT))
hbar_axis(ax)
ys = np.arange(len(SHORT))[::-1]
for y, s_, a_ in zip(ys, sh, au):
    ax.barh(y, s_ * a_, height=0.6, color=AI, lw=0, zorder=3)
    ax.barh(y, s_ * (1 - a_), left=s_ * a_, height=0.6, color=LIGHT, lw=0, zorder=3)
    halo_text(ax, s_ + 0.7, y, f"{s_:.0f}%", va="center", ha="left", fontsize=SMALL + 0.2, color=INK)
ax.set_yticks(ys)
ax.set_yticklabels([f"{i+1}  {s}" for i, s in enumerate(SHORT)], fontsize=SMALL + 0.4, color=INK)
ax.tick_params(axis="y", pad=PAD * 72)
ax.set_xlim(0, 30)
ax.set_xticks([0, 10, 20, 30])
ax.set_xticklabels(["0", "10", "20", "30%"])
ax.set_ylim(-0.55, len(SHORT) - 0.45)
kx = -(LCOL + PAD) / LPW
key(ax, kx, 1.14, "AI can do this", AI, kind="patch", size=SMALL + 0.2, gap=0.012)
key(ax, kx + 0.62, 1.14, "needs people", LIGHT, kind="patch", size=SMALL + 0.2, gap=0.012)
C.text(0.0, 0.025, f"Together, AI can do about two-fifths of the hours ({sh_ai[0]*100:.0f}{EN}{sh_ai[2]*100:.0f}%)",
       fontsize=SMALL + 0.4, fontweight="bold", color=INK)

# ---- right: the pay-off, output per hour of work
bx = C.axes((RX0 / TW, BOT, RPW / TW, HGT))
hbar_axis(bx)
rows = [("The most AI could add: if it did all it\ncan, instantly and without error", ceiling, 2.0, AI_LIGHT, False),
        ("What a gang should actually gain\nby the end of 2026", exp26, 0.4, AI, True)]
for lab, qq, y, col, hero in rows:
    lo, mid, hi = qq
    model_bar(bx, lo, hi, y, col, lw=11, alpha=0.95 if not hero else 0.4)
    bx.plot(mid, y, "o", color=AI, ms=8.5 if hero else 7, mfc=AI if hero else "white", mec=AI,
            mew=1.1 if hero else 1.7, zorder=3)
    t = halo_text(bx, hi + 4, y, f"+{round(mid, -1):.0f}%", va="center", ha="left", fontsize=LABEL + (1 if hero else 0),
                  color=INK, fontweight="bold" if hero else "normal")
    bx.annotate(f" ({round(lo):.0f}{EN}{round(hi):.0f}%)", xycoords=t, xy=(1, 0.5), va="center", ha="left",
                fontsize=MIN, color=SECOND, path_effects=HALO)
    for i, ln in enumerate(lab.split("\n")[::-1]):
        halo_text(bx, 0, y + 0.42 + i * 0.34, ln, ha="left", va="bottom", fontsize=SMALL + 0.2, color=INK,
                  fontweight="bold" if hero else "normal")
bx.set_xlim(0, 100)
bx.set_xticks([0, 25, 50, 75, 100])
bx.set_xticklabels(["0", "25", "50", "75", "100%"])
bx.set_yticks([])
bx.set_ylim(-0.75, 3.4)
bx.text(0.0, 1.14, "Extra output per hour of work", transform=bx.transAxes, fontsize=LABEL, fontweight="bold",
        color=INK, ha="left", va="center")
C.save(str(FIGURES / "c04_amdahl"))
print("ok", "auto-share", sh_ai, "ceiling", ceiling, "exp2026", exp26)
