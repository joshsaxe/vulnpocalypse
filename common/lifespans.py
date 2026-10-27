"""Dated lifespans of criminal enterprises, as used by Chart 2's competing-risks estimate.

Data: data/B_enterprise_lifespans.csv: 152 named ransomware brands, darknet markets, botnets and malware services, forums,
laundering services and other criminal services, with first-seen and end dates and how each ended. Rows need a first-seen
date and either an end date or 'still active' (censored on 21 October 2026).

Event: an ending caused by police action (takedown, seizure, arrests, sanctions) or a shutdown or rebrand that the
operators or reporting tied to police pressure. Endings for other reasons (retirement, exit scam, plain rebrand) are
censored at that date: we learn the enterprise survived police at least that long.
"""
import numpy as np
import pandas as pd

from common.paths import DATA

CENSOR = 2026 + (10 - 1) / 12 + 20 / 365
LE = {"le_takedown", "le_seizure", "le_arrests", "sanctions", "rebrand_after_le_pressure"}
SECT = {
    "botnet_maas": "Botnets and malware services",
    "forum": "Hacking and carding forums",
    "mixer_laundering": "Money-laundering services",
    "darknet_market": "Darknet markets",
    "ransomware": "Ransomware brands",
    "carding_shop": "Other services*", "ddos_booter": "Other services*", "phaas": "Other services*",
    "bph_vpn": "Other services*", "scam_compound": "Other services*",
}


def to_year(s, is_end=False):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    parts = s.split("-")
    y = int(parts[0])
    if len(parts) == 1:
        return y + 0.5
    m = int(parts[1])
    if len(parts) == 2:
        return y + (m - 0.5) / 12
    d = int(parts[2])
    return y + (m - 1) / 12 + (d - 0.5) / 365


def load():
    d = pd.read_csv(DATA / "B_enterprise_lifespans.csv")
    d["start"] = d.first_seen.map(to_year)
    d["end"] = d.end_date.map(to_year)
    d["active"] = d.end_type.eq("still_active")
    d = d[d.start.notna() & (d.end.notna() | d.active)].copy()
    d["stop"] = np.where(d.active, CENSOR, d.end)
    d["t"] = np.maximum(d.stop - d.start, 0.08)
    d["event"] = d.end_type.isin(LE).astype(int) & ~d.active
    d["group"] = d.sector.map(SECT)
    return d
