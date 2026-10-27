"""Price deflators used to put loss series into 2025 prices.

US: BLS CPI-U annual averages (data/cpi_u.csv).
Other jurisdictions: annual-average consumer-price inflation, % (national statistics offices as compiled in the IMF
World Economic Outlook database; ONS CPI for Britain, ABS CPI for Australia, Statistics Bureau of Japan, Statistics
Canada, Singapore Department of Statistics, Hong Kong Census and Statistics Department, Eurostat HICP for the euro
area). Values are rounded to 0.1 point. Deflation errors of a point or two in level are tiny next to the noise in
the loss series themselves (typically 15-40% a year).
"""
import numpy as np
import pandas as pd

from common.paths import DATA

YEARS = np.arange(2004, 2026)

INFL = {  # annual average CPI inflation, %, 2005..2025
    "GB": [2.1, 2.3, 2.3, 3.6, 2.2, 3.3, 4.5, 2.8, 2.6, 1.5, 0.0, 0.7, 2.7, 2.5, 1.8, 0.9, 2.6, 9.1, 7.3, 2.5, 3.4],
    "AU": [2.7, 3.5, 2.3, 4.4, 1.8, 2.9, 3.3, 1.8, 2.4, 2.5, 1.5, 1.3, 2.0, 1.9, 1.6, 0.9, 2.8, 6.6, 5.6, 3.2, 2.6],
    "JP": [-0.3, 0.2, 0.1, 1.4, -1.3, -0.7, -0.3, 0.0, 0.4, 2.7, 0.8, -0.1, 0.5, 1.0, 0.5, 0.0, -0.2, 2.5, 3.2, 2.7,
           3.1],
    "CA": [2.2, 2.0, 2.1, 2.4, 0.3, 1.8, 2.9, 1.5, 0.9, 1.9, 1.1, 1.4, 1.6, 2.3, 1.9, 0.7, 3.4, 6.8, 3.9, 2.4, 2.1],
    "SG": [0.5, 1.0, 2.1, 6.6, 0.6, 2.8, 5.2, 4.6, 2.4, 1.0, -0.5, -0.5, 0.6, 0.4, 0.6, -0.2, 2.3, 6.1, 4.8, 2.4,
           0.9],
    "HK": [0.9, 2.0, 2.0, 4.3, 0.6, 2.3, 5.3, 4.1, 4.3, 4.4, 3.0, 2.4, 1.5, 2.4, 2.9, 0.3, 1.6, 1.9, 2.1, 1.7, 1.4],
    "EA": [2.2, 2.2, 2.1, 3.3, 0.3, 1.6, 2.7, 2.5, 1.4, 0.4, 0.2, 0.2, 1.5, 1.8, 1.2, 0.3, 2.6, 8.4, 5.4, 2.4, 2.1],
}


def _index_from_inflation(rates):
    """Price index with 2025 = 1, for 2004..2025, from inflation rates for 2005..2025."""
    idx = np.ones(len(YEARS))
    # walk backwards: P[t-1] = P[t] / (1 + infl[t])
    for k in range(len(YEARS) - 1, 0, -1):
        idx[k - 1] = idx[k] / (1 + rates[k - 1] / 100.0)
    return pd.Series(idx, index=YEARS)


def us_index():
    c = pd.read_csv(DATA / "cpi_u.csv").set_index("year")["cpi_u"]
    s = c / c.loc[2025]
    s.loc[2004] = 188.9 / c.loc[2025]  # BLS CPI-U annual average 2004
    return s.sort_index()


PRICE = {"US": us_index()}
for k, v in INFL.items():
    PRICE[k] = _index_from_inflation(v)


def to_2025_prices(values, years, country):
    p = PRICE[country]
    return np.asarray(values, float) / p.loc[list(years)].values


if __name__ == "__main__":
    for k, v in PRICE.items():
        print(k, round(v.loc[2005], 3), round(v.loc[2015], 3), round(v.loc[2025], 3))
