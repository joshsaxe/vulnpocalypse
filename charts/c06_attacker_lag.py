"""Chart 6 — how long criminals take to adopt new technology at scale.

Data: data/I_adoption_lags.csv. For each technique: when the enabling technology became publicly
available and when criminal use became widespread ('scaled', defined per row). The author classed techniques as
READY-MADE EXPLOITS (a working attack handed to criminals: a leaked or disclosed exploit), NEW TOOLS (usable inside
existing criminal work, with no new market, payment system or infrastructure) or NEW BUSINESS MODELS (needed one of
those first). An earlier version had one 'drop-in' class; it was split into exploits and tools because the two exploits
were used within days or weeks while every tool took years, so one median for both described neither. The sample is hand-picked from
well-known cases and the classes were assigned knowing the outcomes, so the medians are illustrative.

Model: within the tool and business-model classes, lag ~ log-normal(mu, sigma), priors mu ~ N(log 1 yr, 2),
sigma ~ HalfNormal(1.5). Dates are year-precise, so scaled lags enter as intervals (+/- 0.5 year, never below half
the lag). Techniques that have NOT yet scaled enter as right-censored: criminal chatbots (WormGPT) and malware that
calls AI models in the tool class; AI agents that run whole intrusions in the business-model class. The chance that
agentic intrusion scales by 2028/2030/2032 is computed under the business-model posterior (the chart's assumption)
and, as a sensitivity, under the tool posterior refitted with agentic intrusion as a censored tool, in each case
conditional on its not having scaled by October 2026. The two exploits are shown, not fitted.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # the repository root
from common.paths import DATA, FIGURES, RESULTS, dump_json
import json
import numpy as np
import pandas as pd
from scipy import stats
from common.bayes import lognormal_interval_fit
from common.chart import *

D = pd.read_csv(DATA / "I_adoption_lags.csv")
NOW = 2026.8
SCALED = {  # technique -> (label, class, lag override or None)
    "Mass exploitation of Log4Shell": ("Log4Shell bug", "exploit", None),
    "EternalBlue-based worms (WannaCry, NotPetya)": ("Leaked NSA exploit", "exploit", None),
    "Deepfake voice / audio impersonation fraud": ("Deepfake-voice fraud", "tool", None),
    "IoT DDoS botnets (Mirai)": ("Hijacked-gadget botnets", "tool", 2.3),   # from cheap insecure gadgets (~2014)
    "LLM-written phishing/BEC text": ("AI-written phishing text", "tool", None),
    "Ransomware-as-a-service (RaaS)": ("Ransomware-as-a-service", "eco", None),
    "Double extortion (steal + encrypt + leak)": ("Double extortion (leak sites)", "eco", None),
    "Commodity exploit kits": ("Exploit kits", "eco", None),
    "Ransomware payments in Bitcoin": ("Bitcoin ransoms", "eco", None),
    "Cobalt Strike as criminal C2 standard": ("Pirated hacking toolkits", "eco", None),
    "Darknet drug/data markets on Tor": ("Dark-web markets", "eco", None),
    "Cryptoviral extortion (public-key ransomware)": ("Encrypt-and-ransom (idea, 1996)", "eco", None),
}
OPEN = {  # not yet scaled: label, class, start
    "Dedicated criminal LLMs (WormGPT, FraudGPT)": ("Criminal chatbots (WormGPT)", "tool", 2023 + 5 / 12),
    "LLM-in-the-loop / AI-generated malware": ("Malware that calls AI", "tool", 2022 + 10.97 / 12),
    "Agentic intrusion / extortion": ("AI agents running intrusions", "eco", 2025 + 1.8 / 12),
}
rows = []
for t, (lab, cl, ov) in SCALED.items():
    r = D[D.technique == t].iloc[0]
    rows.append({"label": lab, "cls": cl, "lag": float(ov if ov is not None else r.lag_scaled_years)})
rows = pd.DataFrame(rows)
opens = pd.DataFrame([{"label": v[0], "cls": v[1], "elapsed": NOW - v[2]} for v in OPEN.values()])


def fit_class(L, censored, seed=11):
    L = np.asarray(L, float)
    lo = np.maximum(np.maximum(L - 0.5, L * 0.5), 1 / 365)
    hi = L + np.where(L < 1, L * 0.5, 0.5)
    lo = np.r_[lo, censored]
    hi = np.r_[hi, np.full(len(censored), np.inf)]
    return lognormal_interval_fit(lo, hi, prior_mu=0.0, prior_mu_sd=2.0, prior_sigma_scale=1.5, seed=seed)


def p_scaled_by(f, elapsed, start):
    mu, sg = f["mu"], f["sigma"]
    S_el = stats.norm.sf((np.log(elapsed) - mu) / sg)
    out = {}
    for target in (2028, 2030, 2032):
        tt = target - start
        out[str(target)] = round(float(np.mean((stats.norm.cdf((np.log(tt) - mu) / sg) - (1 - S_el)) / S_el)), 3)
    return out


fits = {}
for cl in ("tool", "eco"):
    fits[cl] = fit_class(rows[rows.cls == cl].lag.values, opens[opens.cls == cl].elapsed.values)
med = {cl: np.exp(f["mu"]) for cl, f in fits.items()}
ag = opens[opens.label.str.startswith("AI agents")].iloc[0]
ag_start = NOW - ag.elapsed
p_eco = p_scaled_by(fits["eco"], ag.elapsed, ag_start)
tool_with_agents = fit_class(rows[rows.cls == "tool"].lag.values,
                             np.r_[opens[opens.cls == "tool"].elapsed.values, ag.elapsed])
p_tool = p_scaled_by(tool_with_agents, ag.elapsed, ag_start)
res = {"class_median_years": {cl: np.quantile(m, [0.1, 0.5, 0.9]).round(2).tolist() for cl, m in med.items()},
       "class_sigma_median": {cl: round(float(np.median(f["sigma"])), 2) for cl, f in fits.items()},
       "exploit_lags_years": rows[rows.cls == "exploit"].lag.tolist(),
       "rhat": {cl: f["rhat"].round(3).tolist() for cl, f in fits.items()},
       "agentic_elapsed_years": round(float(ag.elapsed), 2),
       "p_agentic_scaled_by": p_eco,
       "p_agentic_scaled_by_if_tool": p_tool}
dump_json(res, RESULTS / "c06_attacker_lag.json")
print(json.dumps(res, indent=1))
# the posterior draws that Chart 10 turns into odds-by-year curves
np.savez(RESULTS / "c10_draws_criminals.npz", eco_mu=fits["eco"]["mu"], eco_sigma=fits["eco"]["sigma"],
         tw_mu=tool_with_agents["mu"], tw_sigma=tool_with_agents["sigma"], elapsed=ag.elapsed, start=ag_start)

mt, me = res["class_median_years"]["tool"][1], res["class_median_years"]["eco"][1]
NUM = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def words(y):
    if y < 0.7:
        return f"about {round(y * 12):.0f} months"
    if y < 1.5:
        return "about a year"
    return f"about {NUM.get(round(y), round(y))} years"


AI_SCALED = {"AI-written phishing text", "Deepfake-voice fraud"}
pt30 = p_tool["2030"]      # 'by 2030' = by 1 Jan 2030 = by the end of 2029
C = Chart(6, "Crooks use ready-made exploits within weeks, but take years to adopt new tools and business models",
          "Time from a technology becoming available to widespread criminal use, log scale",
          "Sources: Young and Yung (1996); FinCEN; Coveware; Chainalysis; Soska and Christin (USENIX 2015); "
          "Microsoft; Proofpoint; Cloudflare; Wikipedia; Krebs on Security; Verizon DBIR; Palo Alto Networks Unit 42; "
          "Anthropic and Google threat reports; author's Bayesian censored log-normal model (shading: 80% credible "
          "interval of each group's median)",
          note=("New tools fit existing criminal work; business models need a new market, payment system or "
                "infrastructure. Classes were assigned knowing the outcomes, and the cases were hand-picked, so "
                "medians are illustrative. Amber: AI. As a business model, AI agents running whole intrusions have about a "
                "one-in-three chance of being widespread by the end of 2029; as a new tool, "
                f"{'one in two' if 0.42 <= pt30 <= 0.58 else f'{pt30:.0%}'}."),
          plot_h_in=2.75)
TW = C.width_in - 0.24
GAP = 0.32
PW = (TW - GAP) / 2
BOT, HGT = 0.115, 0.86
XL = (1 / 365 * 0.6, 40)
LX = np.log10(XL)


def frac(v):
    return (np.log10(v) - LX[0]) / (LX[1] - LX[0])


def panel(x0_in):
    ax = C.axes((x0_in / TW, BOT, PW / TW, HGT))
    hbar_axis(ax)
    ax.set_xscale("log")
    ax.set_xlim(*XL)
    ax.set_xticks([1 / 365, 30 / 365, 1, 10])
    ax.set_xticklabels(["1 day", "1 month", "1 year", "10 years"], fontsize=SMALL + 0.2)
    ax.minorticks_off()
    ax.set_yticks([])
    return ax


def draw_group(ax, y, head, cl, col, median=True):
    halo_text(ax, 0.0, y, head, transform=ax.get_yaxis_transform(), fontsize=MIN, fontweight="bold", color=SECOND,
            va="center", ha="left")
    top = y - 0.45
    sub = rows[rows.cls == cl].sort_values("lag")
    # labels sit right-aligned just left of the group's median band (or of the dot, if the dot is further left),
    # so no label crosses the band's median line
    anchor = res["class_median_years"][cl][0] / 1.35 if median else None
    for _, r in sub.iterrows():
        y -= 1
        c_ = AI if r.label in AI_SCALED else col
        ax.plot(r.lag, y, "o", color=c_, ms=6.5, mec="white", mew=1.0, zorder=3)
        if anchor is None:
            halo_text(ax, r.lag * 1.6, y, r.label, ha="left", va="center", fontsize=SMALL + 0.2, color=INK, zorder=4)
        else:
            halo_text(ax, min(anchor, r.lag / 1.6), y, r.label, ha="right", va="center", fontsize=SMALL + 0.2, color=INK,
                    zorder=4)
    for _, r in opens[opens.cls == cl].iterrows():
        y -= 1.45
        ax.plot(r.elapsed, y + 0.27, "o", mfc="white", mec=AI, mew=1.7, ms=6.5, zorder=3)
        ax.annotate("", xy=(r.elapsed * 2.1, y + 0.27), xytext=(r.elapsed * 1.15, y + 0.27),
                    arrowprops=dict(arrowstyle="-|>", color=AI, lw=1.4, mutation_scale=8))
        xa = min(anchor, r.elapsed / 1.6) if anchor else r.elapsed / 1.6
        halo_text(ax, xa, y + 0.27, r.label, ha="right", va="center", fontsize=SMALL + 0.2, color=INK, zorder=4)
        halo_text(ax, xa, y - 0.33, f"not widespread after {r.elapsed:.1f} years", ha="right", va="center",
                fontsize=MIN, color=SECOND, zorder=4)
    if median:
        lo_m, mid_m, hi_m = res["class_median_years"][cl]
        ax.fill_betweenx([y - 0.5, top], lo_m, hi_m, color=col, alpha=0.13, lw=0, zorder=0)
        ax.plot([mid_m, mid_m], [y - 0.5, top], color=col, lw=1.0, zorder=1)
        y -= 1.0
        halo_text(ax, hi_m * 1.08, y + 0.05, f"median: {words(mid_m)}", fontsize=MIN, color=INK, ha="right", va="center",
                fontweight="bold")
    return y


axL = panel(0.0)
y = -0.5
y = draw_group(axL, y, "READY-MADE EXPLOITS", "exploit", GREY, median=False)
y = draw_group(axL, y - 0.85, "NEW TOOLS FOR EXISTING WORK", "tool", GREY)
y_min = y
axR = panel(PW + GAP)
yR = draw_group(axR, -0.5, "NEW BUSINESS MODELS", "eco", HACK)
y_min = min(y_min, yR)
for a in (axL, axR):
    a.set_ylim(y_min - 0.45, -0.1)
C.save(str(FIGURES / "c06_attacker_lag"))

