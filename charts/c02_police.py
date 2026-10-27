"""Chart 2 — how criminal enterprises end: police, or their own hand.

Data: data/B_enterprise_lifespans.csv: 152 named criminal enterprises in ten sectors, with how
each ended. Every row is used (no dates needed for this view).

Bayesian estimate: for each sector, the share of enterprises ended by police (takedown, seizure, arrests or
sanctions, plus shutdowns the operators or reporting tied to police pressure) has a uniform Beta(1,1) prior and a
binomial likelihood; the posterior is Beta(1 + police, 1 + others). We report its median and 80% interval.
Separately, from the 115 rows with dates, an Aalen-Johansen estimate gives the share of all enterprises ended by
police within 2, 5 and 10 years of launch (competing risks: other endings remove an enterprise from risk), with a
Bayesian bootstrap for its 80% interval. Selection caveat: enterprises famous enough to be documented are more often
ones police acted against, so these shares probably flatter the police.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from scipy import stats
from common.chart import *
from common.lifespans import load as load_dated

d = pd.read_csv(DATA / "B_enterprise_lifespans.csv")
GROUP = {"botnet_maas": "Botnets and malware services", "forum": "Hacking and carding forums",
         "mixer_laundering": "Money-laundering services", "darknet_market": "Darknet markets",
         "ransomware": "Ransomware brands"}
d["group"] = d.sector.map(GROUP).fillna("Other criminal services*")
FATE = {"le_takedown": "police", "le_seizure": "police", "le_arrests": "police", "sanctions": "police",
        "rebrand_after_le_pressure": "pressure", "voluntary_retirement": "other", "exit_scam": "other",
        "rebrand_other": "other", "still_active": "active"}
d["fate"] = d.end_type.map(FATE)
tab = pd.crosstab(d.group, d.fate).reindex(columns=["police", "pressure", "other", "active"], fill_value=0)
tab["n"] = tab.sum(axis=1)
tab["police_any"] = tab.police + tab.pressure
tab["ended"] = tab.n - tab.active
res = {"by_group": {}}
for g, r in tab.iterrows():
    k, n = int(r.police_any), int(r.ended)        # share of ENDED enterprises that police ended
    a, b = 1 + k, 1 + n - k
    res["by_group"][g] = {"n": int(r.n), "police": int(r.police), "pressure": int(r.pressure),
                          "other": int(r.other), "active": int(r.active),
                          "police_share_of_ended_q": [round(float(stats.beta.ppf(p, a, b)), 3)
                                                      for p in (0.1, 0.5, 0.9)]}
k, n = int(tab.police_any.sum()), int(tab.ended.sum())
res["all"] = {"n": int(tab.n.sum()), "ended": n, "police_any": k, "active": int(tab.active.sum()),
              "police_share_of_ended_q": [round(float(stats.beta.ppf(p, 1 + k, 1 + n - k)), 3)
                                          for p in (0.1, 0.5, 0.9)]}

# ---- cumulative incidence of police endings (Aalen-Johansen) on dated rows, Bayesian bootstrap
dd = load_dated()
t = dd.t.values
ev = np.where(dd.active.values, 0, np.where(dd.event.values == 1, 1, 2))   # 1 police, 2 other, 0 censored


def cif(t, ev, w, horizons):
    order = np.argsort(t)
    t, ev, w = t[order], ev[order], w[order]
    S, F, out, h_i = 1.0, 0.0, [], 0
    at_risk = w.sum()
    uniq = np.unique(t)
    res_ = {}
    for u in uniq:
        m = t == u
        d1 = w[m & (ev == 1)].sum()
        d2 = w[m & (ev == 2)].sum()
        if at_risk > 0:
            F += S * d1 / at_risk
            S *= 1 - (d1 + d2) / at_risk
        at_risk -= w[m].sum()
        res_[u] = F
    keys = np.array(sorted(res_))
    vals = np.array([res_[k_] for k_ in keys])
    return [float(vals[keys <= h][-1]) if np.any(keys <= h) else 0.0 for h in horizons]


H = [2, 5, 10]
point = cif(t, ev, np.ones(len(t)), H)
rng = np.random.default_rng(22)
boot = np.array([cif(t, ev, rng.dirichlet(np.ones(len(t))), H) for _ in range(4000)])
res["cif_police"] = {str(h): [round(float(q), 3) for q in np.quantile(boot[:, i], [0.1, 0.5, 0.9])]
                     for i, h in enumerate(H)}
res["cif_point"] = dict(zip(map(str, H), [round(p, 3) for p in point]))
res["n_dated"] = int(len(t))
dump_json(res, RESULTS / "c02_police.json")
print(json.dumps(res, indent=1))

# ------------------------------------------------------------------------------------------------ chart
# Bars show how the enterprises that have CLOSED came to an end (still-running ones go in the count column), so
# young sectors are not penalised for not having closed yet. Police shutdowns are drawn in the state colour.
# Whiskers are 80% highest-density intervals of the Beta posterior, so that a sector where police ended every closed
# enterprise (a share of 100%) is not drawn outside its own interval, as an equal-tailed interval would.


def beta_hdi(a, b, mass=0.8, n=20001):
    xs = np.linspace(0, 1, n)
    cdf = stats.beta.cdf(xs, a, b)
    best = (0.0, 1.0)
    j = 0
    for i in range(n):
        while j < n and cdf[j] - cdf[i] < mass:
            j += 1
        if j >= n:
            break
        if xs[j] - xs[i] < best[1] - best[0]:
            best = (xs[i], xs[j])
    return best


order = sorted(res["by_group"], key=lambda g: -res["by_group"][g]["police_share_of_ended_q"][1])
SHORT = {"Botnets and malware services": "Botnets, malware services", "Hacking and carding forums": "Hacking forums",
         "Money-laundering services": "Laundering services", "Darknet markets": "Darknet markets",
         "Ransomware brands": "Ransomware brands", "Other criminal services*": "Other services*"}
EN = "\u2013"
C = Chart(2, "Police ended most criminal services that closed, but not most ransomware brands or darknet markets",
          f"{res['all']['n']} named criminal enterprises: how those that have closed came to an end, % of each sector",
          "Sources: US Department of Justice; Europol and Operation Endgame partners; Britain's National Crime "
          "Agency; US Treasury; Microsoft; MITRE; Chainalysis; Krebs on Security; Wikipedia; ransomware.live; Gwern "
          "Branwen; court records and press reports; author's beta-binomial model (whiskers: 80% credible "
          "intervals)",
          note=("Ended by police: takedowns, seizures, arrests, sanctions or quitting under police pressure. *Carding "
                "shops, DDoS-for-hire, phishing kits, bulletproof hosting, scam compounds. Shares flatter the police: "
                "documented enterprises are more often ones they caught."),
          plot_h_in=2.75)
ax = C.axes((0.255, 0.115, 0.60, 0.765))
ys = list(np.arange(len(order))[::-1] + 1.25)
rows_ = [(y, g, res["by_group"][g]) for y, g in zip(ys, order)]
allr = {"police": sum(r["police"] for _, _, r in rows_), "pressure": sum(r["pressure"] for _, _, r in rows_),
        "other": sum(r["other"] for _, _, r in rows_), "active": sum(r["active"] for _, _, r in rows_),
        "n": sum(r["n"] for _, _, r in rows_)}
rows_.append((0.0, "All", allr))
hdis = {}
for y, g, r in rows_:
    closed = r["police"] + r["pressure"] + r["other"]
    k_ = r["police"] + r["pressure"]
    pol = 100 * k_ / closed
    oth = 100 - pol
    ax.barh(y, pol, height=0.6, color=GOV, lw=0, zorder=2)
    ax.barh(y, oth, left=pol, height=0.6, color=GREY, alpha=0.55, lw=0, zorder=2)
    ax.plot([pol, pol], [y - 0.30, y + 0.30], color="white", lw=1.2, zorder=3)
    lo_, hi_ = (100 * v for v in beta_hdi(1 + k_, 1 + closed - k_))
    hdis[g] = (round(lo_, 1), round(hi_, 1))
    yw = y + 0.42
    ax.plot([lo_, hi_], [yw, yw], color=INK, lw=0.9, zorder=5, solid_capstyle="butt")
    for xx in (lo_, hi_):
        ax.plot([xx, xx], [yw - 0.08, yw + 0.08], color=INK, lw=0.9, zorder=5)
    ax.text(1.5, y, f"{pol:.0f}%", va="center", ha="left", fontsize=SMALL + 0.4, color="white", fontweight="bold",
            zorder=4)
    ax.text(103, y, f"{closed} of {r['n']}", va="center", ha="left", fontsize=SMALL + 0.4, color=SECOND)
ax.axhline(0.72, color=GRID, lw=0.8, xmin=-0.42, clip_on=False)
ax.text(103, max(ys) + 0.5, "Closed", va="bottom", ha="left", fontsize=MIN, color=SECOND)
ax.set_yticks([y for y, _, _ in rows_])
ax.set_yticklabels([SHORT.get(g, "All 152") for _, g, _ in rows_], fontsize=LABEL, color=INK)
for lab in ax.get_yticklabels():
    if lab.get_text() == "All 152":
        lab.set_fontweight("bold")
hbar_axis(ax, xgrid=False)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100%"])
ax.set_ylim(-0.5, max(ys) + 0.6)
key(ax, 0.0, 1.10, "Ended by police", GOV, kind="patch", size=SMALL + 0.4, gap=0.01)
key(ax, 0.33, 1.10, "Quit, vanished or rebranded", GREY, kind="patch", size=SMALL + 0.4, alpha=0.55, gap=0.01)
C.save(str(FIGURES / "c02_police"))
print("all closed share", allr, 100 * (allr["police"] + allr["pressure"]) / (allr["n"] - allr["active"]))
print("80% HDIs", hdis)
# the whiskers on the chart, in per cent of closed enterprises, kept with the other results
res["police_share_of_closed_hdi80_pct"] = {g: list(v) for g, v in hdis.items()}
dump_json(res, RESULTS / "c02_police.json")
