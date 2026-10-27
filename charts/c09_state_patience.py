"""Chart 9 (new) -- state hackers sit on access for years and exploit only a sliver of it.

Data: data/H_espionage_cases.csv: for well-documented state-linked campaigns, the time from first
intrusion to discovery (years_undetected) and, where reported, how many of the systems reached were actually worked.
Benchmarks: Mandiant M-Trends 2026 (2025 investigations): median dwell time 122 days for espionage and North Korean
IT-worker cases, 14 days for all intrusions.

Not a model: every number is a reported date or count. Campaigns are those later discovered and made public, so
campaigns still hidden are missing and famous ones are over-represented (stated in the note). Volt Typhoon's figure is
a lower bound (CISA: 'at least five years' in some victims) and is drawn with a hollow end marker. Flame (grade C,
read through Wikipedia) and Salt Typhoon (dwell only reported at second hand) are left out.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import pandas as pd
from common.chart import *

E = pd.read_csv(DATA / "H_espionage_cases.csv")
get = lambda name: float(E[E.campaign.str.startswith(name)].years_undetected.astype(float).iloc[0])
eq, regin, sw = get("Equation Group"), get("Regin"), get("SolarWinds SUNBURST (")
brick, opm = get("UNC5221 BRICKSTORM"), get("OPM")
mb, ivanti, s0558 = get("Midnight Blizzard"), get("UNC5221 Ivanti"), get("Storm-0558")
volt = 5.0                       # lower bound
spy_med, all_med = 122 / 365, 14 / 365

# (label, years, value label, annotation, annotation placement, kind)
ROWS = [
    ("Equation Group", eq, "14 years", "500+ victims among tens of thousands infected", "inside", "state"),
    ("Regin", regin, "11 years", "27 victims in 14 countries", "inside", "state"),
    ("Volt Typhoon\u2020", volt, "5+ years", "in US water, power and transport; not yet used", "right", "open"),
    ("SolarWinds", sw, "15 months", "about 110 of 18,000 infected were exploited", "right", "state"),
    ("BRICKSTORM", brick, "13 months", "average across Mandiant cases", "right", "state"),
    ("OPM breach", opm, "11 months", None, None, "state"),
    ("Midnight Blizzard", mb, "7 weeks", None, None, "state"),
    ("Ivanti zero-days", ivanti, "5 weeks", None, None, "state"),
    ("Storm-0558", s0558, "1 month", None, None, "state"),
    None,
    ("Typical spying case*", spy_med, "122 days", None, None, "bench"),
    ("Typical intruder*", all_med, "14 days", None, None, "bench"),
]

C = Chart(9, "State hackers can stay hidden for years and use only a sliver of their access",
          "Time from first intrusion to discovery, selected state-linked campaigns",
          "Sources: Kaspersky (Equation Group, Regin); CISA, NSA and FBI (Volt Typhoon); White House (SolarWinds); "
          "Mandiant (M-Trends 2026; BRICKSTORM); US House Oversight Committee (OPM); Microsoft (Midnight Blizzard); "
          "Cyber Safety Review Board (Storm-0558); Volexity (Ivanti)",
          note=("Well-documented campaigns, not a sample: ones still hidden are missing and famous ones over-represented. "
                "\u2020CISA reported access held for at least five years in some networks (February 2024). *Medians of "
                "Mandiant's 2025 investigations: espionage and North Korean IT-worker cases, and all intrusions."),
          plot_h_in=2.8)
TW = C.width_in - 0.24
LCOL, PAD = 1.62, 0.08
PW = TW - LCOL - PAD
ax = C.axes(((LCOL + PAD) / TW, 0.075, PW / TW, 0.925))
hbar_axis(ax)
XMAX = 19.0
n = len(ROWS)
ys = [n - 1 - i for i in range(n)]
ticks, labs = [], []
for y, r in zip(ys, ROWS):
    if r is None:
        continue
    lab, v, vlab, ann, place, kind = r
    col = GOV if kind in ("state", "open") else GREY
    ax.barh(y, v, height=0.56, color=col, lw=0, zorder=3, alpha=0.9 if kind != "open" else 0.9)
    if kind == "open":
        ax.plot(v, y, ">", ms=8, mfc="white", mec=GOV, mew=1.5, zorder=4)
    else:
        ax.plot(v, y, "o", ms=4.2, color=col, zorder=4)
    xlab = v + (0.55 if kind == "open" else 0.3)
    t = halo_text(ax, xlab, y, vlab, va="center", ha="left", fontsize=LABEL, fontweight="bold", color=INK)
    if ann and place == "right":
        ax.annotate("  " + ann, xycoords=t, xy=(1, 0.5), va="center", ha="left", fontsize=SMALL, color=SECOND,
                    path_effects=HALO)
    elif ann and place == "inside":
        ax.text(0.3, y, ann, va="center", ha="left", fontsize=SMALL, color="white", zorder=5)
    ticks.append(y)
    labs.append(lab)
ax.set_yticks(ticks)
ax.set_yticklabels(labs, fontsize=SMALL + 0.6, color=INK)
ax.tick_params(axis="y", pad=PAD * 72)
ax.set_xlim(0, XMAX)
ax.set_xticks([0, 5, 10, 15])
ax.set_xticklabels(["0", "5", "10", "15 years"])
ax.set_ylim(-0.6, n - 0.4)
# a hairline between the campaigns and the benchmarks
yb = ys[9]
ax.plot([0, XMAX], [yb, yb], color=LIGHT, lw=0.7, zorder=1)
C.save(str(FIGURES / "c09_state_patience"))
print("ok", {r[0]: round(r[1], 2) for r in ROWS if r})
dump_json({"years_to_discovery": {r[0]: round(r[1], 3) for r in ROWS if r},
           "lower_bound_rows": [r[0] for r in ROWS if r and r[5] == "open"]}, RESULTS / "c09_state_patience.json")
