"""Chart 3 — what crime pays coders, against what honest developers earn where the criminal job ads are posted and
elsewhere in emerging economies, and against American pay.

Like-for-like comparison: the dark-web job ads (Kaspersky, 155 forums, Jan 2020-Jun 2022) were posted mostly on
Russian-language forums, so the main comparison is with Russian developers' take-home pay in the same period (Habr
Career, first half of 2021, by level). Kaspersky itself "did not detect a significant difference between the median
levels of IT professionals' compensation in the cybercriminal ecosystem and the legitimate job market". The band is the
range of the ads' median pay by role ($1,300-4,000 a month), drawn behind every row so each figure can be read against
it.

Data:
- data/C_pay.csv: leaked Conti chats (via Krebs on Security), Kaspersky's dark-web job-ad study, the
  US indictment of LockBit's alleged developer, Levels.fyi (self-reported total compensation, including stock).
- Habr Career, "Зарплаты разработчиков в первой половине 2021" (developers' medians by level, take-home, roubles a
  month): junior 52,000, middle 120,000, senior 195,000, lead 230,000; converted at the World Bank's 2021 average of
  73.65 roubles per dollar.
- data/C2_dev_pay_by_country.csv: Ukraine (DOU survey median, take-home, 2026), Belarus (Belstat, information-and-
  communication sector mean, 2025), China (National Bureau of Statistics, IT-sector mean wage in private and in
  non-private units, 2025: drawn as a range), Brazil (Brasscom, systems-development analysts on formal contracts,
  Dec 2025), Vietnam (ITviec survey median, back-end developers, 2025), Kazakhstan (Kolesa Group survey median,
  developers, 2024); and the BLS median annual wage of US software developers (May 2025).
Nominal US dollars a year at market exchange rates (annual averages).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from common.chart import *

C2 = pd.read_csv(DATA / "C2_dev_pay_by_country.csv")


def pick(country, contains):
    r = C2[(C2.country == country) & C2.basis.str.contains(contains, regex=False)]
    assert len(r) >= 1, (country, contains)
    return float(r.iloc[0].usd_annual)


RUB_2021 = 73.65                                  # World Bank, average roubles per dollar, 2021
RU21 = [("Junior", 52000), ("Mid-level", 120000), ("Senior", 195000), ("Lead", 230000)]   # Habr Career, H1 2021
RUSSIA = [(lab, rub * 12 / RUB_2021, None) for lab, rub in RU21]
BAND = (1300 * 12, 4000 * 12)                     # Kaspersky: median pay offered, by role, $1,300-4,000 a month

CRIME = [  # label, low, high
    ("Conti coders, 2021", 12000, 24000),
    ("Dark-web ads: developers", 24000, 24000),
    ("Dark-web ads: reverse engineers", 48000, 48000),
    ("LockBit's alleged developer", 120000, 120000),
]
US = [
    ("Median salary, 2025", pick("United States", "median"), None),
    ("Median total pay, 2025", 195000, None),
    ("AI engineers' total pay, 2026", 250000, None),
    ("OpenAI or Anthropic, 2026", 878750, None),
]
DEV = [  # label, low, high
    ("Ukraine*, 2026", pick("Ukraine", "median; net"), None),
    ("China, 2025", pick("China", "mean; gross; annual"), pick("China", "incl. bonuses and allowances")),
    ("Kazakhstan, 2024", pick("Kazakhstan", "median"), None),
    ("Belarus, 2025", pick("Belarus", "mean"), None),
    ("Brazil, 2025", pick("Brazil", "mean"), None),
    ("Vietnam, 2025", pick("Vietnam", "median"), None),
]
ai_med = US[2][1]

C = Chart(3, "Criminal coders earn about what honest ones do in emerging economies, a tenth of what American AI "
             "engineers make",
          "Annual pay, $, log scale",
          "Sources: Krebs on Security (Conti leaks); Kaspersky (155 dark-web forums); US Department of Justice; Habr "
          "Career; DOU; Belstat; China's National Bureau of Statistics; Brasscom; ITviec; Kolesa Group; US Bureau of "
          "Labor Statistics; Levels.fyi",
          note=("Band: median pay offered in dark-web IT job ads, 2020-22, from designers (\\$16k) to reverse engineers "
                "(\\$48k); Kaspersky, which collected them, found no significant difference from legitimate pay. "
                "Elsewhere: latest medians, except averages for Brazil (formal contracts) and the IT sector in "
                "Belarus and China (private to state employers). *Take-home pay; others before tax. US: BLS median "
                "salary; Levels.fyi median total pay, including stock. Crime pay is salary; the few who share in "
                "ransoms earn far more. Not adjusted for inflation."),
          plot_h_in=3.0)
TW = C.width_in - 0.24
PAD = 0.08
LCL, PWL = 1.80, 1.46          # left: label column and plot width, inches
GAP = 0.30
LCR = 1.02                      # right: label column
PWR = TW - LCL - PAD - PWL - GAP - LCR - PAD
BOT, HGT = 0.095, 0.795
XL = (5000, 1.3e6)
YMIN, YMAX = -12.35, 0.55


def panel(x0_in, lc_in, pw_in):
    ax = C.axes(((x0_in + lc_in + PAD) / TW, BOT, pw_in / TW, HGT))
    hbar_axis(ax, xgrid=False)
    ax.set_xscale("log")
    ax.set_xlim(*XL)
    ax.set_xticks([10000, 100000, 1000000])
    ax.set_xticklabels(["$10k", "$100k", "$1m"])
    ax.minorticks_off()
    ax.set_ylim(YMIN, YMAX)
    ax.tick_params(axis="y", length=0, pad=PAD * 72)
    return ax


def money(v):
    return f"${v/1000:,.0f}k" if v < 1e6 else f"${v/1e6:.1f}m"


def rows(ax, items, y0, col, lc_in, pw_in, head, first_gap=0.0, step=1.0):
    ax.text(-(lc_in + PAD) / pw_in, y0, head, transform=ax.get_yaxis_transform(), fontsize=MIN, fontweight="bold",
            color=SECOND, va="center", ha="left", linespacing=1.0, path_effects=HALO)
    ys, labs = [], []
    y = y0 - first_gap
    for lab, lo, hi in items:
        y -= step
        ys.append(y); labs.append(lab)
        hi = hi if hi is not None else lo
        if hi > lo * 1.05:
            data_range(ax, lo, hi, y, col, tick=0.17, lw=1.4, zorder=3)
            txt, xr = f"${lo/1000:.0f}k{chr(8211)}{hi/1000:.0f}k", hi * 1.15
        else:
            ax.plot(lo, y, "o", color=col, ms=7, mec="white", mew=1.1, zorder=4)
            txt, xr = money(lo), lo * 1.22
        if xr * 3.2 > XL[1]:
            halo_text(ax, lo / 1.22, y, txt, va="center", ha="right", fontsize=SMALL, color=INK, zorder=5)
        else:
            halo_text(ax, xr, y, txt, va="center", ha="left", fontsize=SMALL, color=INK, zorder=5)
    return ys, labs, y


def band_and_grid(ax, groups):
    """The crime band and the vertical hairlines, drawn group by group so they stop short of the headings."""
    for ys in groups:
        top, bot = ys[0] + 0.55, ys[-1] - 0.55
        ax.fill_betweenx([bot, top], BAND[0], BAND[1], color=HACK, alpha=0.15, lw=0, zorder=1)
        ax.vlines([1e4, 1e5, 1e6], bot, top, color=GRID, lw=0.7, zorder=0.5)
    ax.vlines([1e4, 1e5, 1e6], YMIN, groups[-1][-1] - 0.55, color=GRID, lw=0.7, zorder=0.5)


# ---- left: crime and the United States
axL = panel(0.0, LCL, PWL)
ys1, l1, yend = rows(axL, CRIME, -0.1, HACK, LCL, PWL, "CRIME", step=1.25)
ys2, l2, _ = rows(axL, US, yend - 1.5, PRIV, LCL, PWL, "US SOFTWARE ENGINEERS", step=1.25)
band_and_grid(axL, [ys1, ys2])
axL.set_yticks(ys1 + ys2)
axL.set_yticklabels(l1 + l2, fontsize=SMALL + 0.4, color=INK)

# ---- right: honest developers, like for like where the ads were posted, then elsewhere
x0R = LCL + PAD + PWL + GAP
axR = panel(x0R, LCR, PWR)
ys3, l3, yend = rows(axR, RUSSIA, 0.05, PRIV, LCR, PWR, "RUSSIAN DEVELOPERS' TAKE-HOME\nPAY BY LEVEL, 2021",
                     first_gap=0.45)
ys4, l4, _ = rows(axR, DEV, yend - 1.15, PRIV, LCR, PWR, "OTHER EMERGING ECONOMIES")
band_and_grid(axR, [ys3, ys4])
axR.set_yticks(ys3 + ys4)
axR.set_yticklabels(l3 + l4, fontsize=SMALL + 0.4, color=INK)

# ---- key for the band, above the panels
ky = 0.975
L0, B0, W0, H0 = C.region
C.fig.add_artist(Rectangle((L0, B0 + ky * H0 - 0.05 / C.H), 0.17 / C.width_in, 0.10 / C.H,
                           transform=C.fig.transFigure, facecolor=HACK, alpha=0.15, lw=0))
C.text(0.24 / TW, ky, f"Dark-web IT job ads, 2020-22: median pay by role, \\${BAND[0]/1000:.0f}k{chr(8211)}"
       f"{BAND[1]/1000:.0f}k", fontsize=SMALL + 0.2, color=INK, ha="left", va="center")
C.save(str(FIGURES / "c03_talent"))
dump_json({"russia_2021_usd": {l: round(v) for l, v, _ in RUSSIA},
           "crime_usd": {l: [lo, hi] for l, lo, hi in CRIME},
           "us_usd": {l: v for l, v, _ in US},
           "other_emerging_usd": {l: [round(lo), None if hi is None else round(hi)] for l, lo, hi in DEV},
           "band_usd": list(BAND),
           "dev_ad_over_ai_engineers_pay": round(24000 / ai_med, 3),
           "dev_ad_over_us_median_salary": round(24000 / US[0][1], 3)}, RESULTS / "c03_talent.json")
print("Russia 2021:", [(l, round(v)) for l, v, _ in RUSSIA])
print("dev ad / AI engineers' pay:", round(24000 / ai_med, 3), " dev ad / US median salary:", round(24000 / US[0][1], 3))
print("others:", [(l, round(lo), None if hi is None else round(hi)) for l, lo, hi in DEV])
