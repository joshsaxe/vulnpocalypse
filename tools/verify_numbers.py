#!/usr/bin/env python3
"""Check that the numbers this repository produces are the numbers behind the article.

Run it after `python tools/run_all.py` (or on the committed results/ as they stand). It makes three comparisons and labels
every line with one of three words:

    IDENTICAL    exactly the number the article's run produced (or, for a quoted number, exactly what rounding the stored
                 result gives)
    CONSISTENT   different, but inside a stated tolerance: Monte Carlo noise from another version of numpy or scipy for a
                 stored result; a looser wording ("about", "mid-2028") for a quoted one. The line says why.
    DIFFERENT    outside the tolerance. The script then exits with status 1.

  1. results/ against tests/reference_numbers.json: every number the scripts write (a snapshot of the article's run).
     On the pinned library versions in requirements-lock.txt this is IDENTICAL throughout; on other versions expect some
     CONSISTENT lines (the random streams differ a little) and no DIFFERENT ones.
  2. The numbers quoted in the methods appendix, against the results they come from (tests/appendix_a_numbers.csv: one row
     per quoted number, naming the file and key, the printed figure, and how it was rounded).
  3. Numbers quoted from the data tables rather than from a model (counts, dates, a few sums), recomputed from data/.

Usage:
    python tools/verify_numbers.py                 # summary lines, then anything not IDENTICAL
    python tools/verify_numbers.py -v              # every line
    python tools/verify_numbers.py --update-reference   # re-snapshot results/ (only when you mean to change the reference)
"""
import argparse
import csv
import json
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd

from common.paths import DATA, RESULTS

REFERENCE = ROOT / "tests" / "reference_numbers.json"
LEDGER = ROOT / "tests" / "appendix_a_numbers.csv"
SENSITIVITY = ("sensitivity_c01.json", "sensitivity_c02.json", "sensitivity_c05.json", "sensitivity_c06.json",
               "sensitivity_c07.json", "sensitivity_c08.json", "sensitivity_c09.json")
REL_TOL, ABS_TOL = 0.05, 0.002        # for a stored result: inside 5% (plus a hair for tiny numbers) is Monte Carlo noise

# ------------------------------------------------------------------------------------------------------ helpers
_cache = {}


def results_json(name):
    if name not in _cache:
        p = RESULTS / f"{name}.json"
        _cache[name] = json.load(open(p)) if p.exists() else None
    return _cache[name]


def r(name, path):
    """results/<name>.json at a dotted path (list positions are numbers)."""
    cur = results_json(name)
    if cur is None:
        raise FileNotFoundError(name)
    for tok in path.split("."):
        cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
    return cur


def round_half_up(x, decimals):
    q = Decimal(1).scaleb(-decimals)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def flatten(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}.{i}" if prefix else str(i))
    else:
        yield prefix, obj


def npz_summary(path):
    out = {}
    with np.load(path) as z:
        for k in z.files:
            a = np.asarray(z[k], float)
            q = np.quantile(a, [0.1, 0.5, 0.9]) if a.size else [float("nan")] * 3
            out[k] = {"shape": list(a.shape), "mean": float(f"{a.mean():.8g}"), "sd": float(f"{a.std():.8g}"),
                      "q10": float(f"{q[0]:.8g}"), "q50": float(f"{q[1]:.8g}"), "q90": float(f"{q[2]:.8g}")}
    return out


def snapshot():
    snap = {}
    for p in sorted(RESULTS.glob("*.json")):
        snap[p.name] = {k: v for k, v in flatten(json.load(open(p)))}
    for p in sorted(RESULTS.glob("*.npz")):
        flat = {}
        for k, d in npz_summary(p).items():
            flat[f"{k}.shape"] = json.dumps(d["shape"])
            for stat in ("mean", "sd", "q10", "q50", "q90"):
                flat[f"{k}.{stat}"] = d[stat]
        snap[p.name] = flat
    return snap


def compare_number(ref, got):
    """IDENTICAL / CONSISTENT / DIFFERENT for one stored number."""
    if isinstance(ref, bool) or isinstance(got, bool) or isinstance(ref, str) or ref is None or got is None:
        return "IDENTICAL" if ref == got else "DIFFERENT"
    if ref == got:
        return "IDENTICAL"
    if isinstance(ref, int) and isinstance(got, int):
        return "DIFFERENT"                                           # a count or a year that changed is a real change
    if abs(got - ref) <= REL_TOL * max(abs(got), abs(ref)) + ABS_TOL:
        return "CONSISTENT"
    return "DIFFERENT"


# ------------------------------------------------------------------------------------------------------ 1. snapshot
def check_snapshot(verbose, out):
    ref = json.load(open(REFERENCE))["files"]
    now = snapshot()
    counts = {"IDENTICAL": 0, "CONSISTENT": 0, "DIFFERENT": 0, "NOT RUN": 0}
    print("1. results/ against tests/reference_numbers.json (the article's run)")
    for fname, rv in ref.items():
        if fname not in now:
            status = "NOT RUN" if fname in SENSITIVITY else "DIFFERENT"
            counts[status] += 1
            print(f"   {status:10s} {fname:34s} {'(run `make sensitivity` to produce it)' if status == 'NOT RUN' else 'file is missing'}")
            continue
        worst, n_by, notes = "IDENTICAL", {"IDENTICAL": 0, "CONSISTENT": 0, "DIFFERENT": 0}, []
        for k, v in rv.items():
            s = compare_number(v, now[fname].get(k, None))
            n_by[s] += 1
            if s != "IDENTICAL":
                notes.append((s, k, v, now[fname].get(k)))
        extra = set(now[fname]) - set(rv)
        for k in sorted(extra):
            n_by["DIFFERENT"] += 1
            notes.append(("DIFFERENT", k, "(not in the reference)", now[fname][k]))
        worst = "DIFFERENT" if n_by["DIFFERENT"] else "CONSISTENT" if n_by["CONSISTENT"] else "IDENTICAL"
        counts[worst] += 1
        print(f"   {worst:10s} {fname:34s} {sum(n_by.values()):5d} numbers"
              + (f"  ({n_by['CONSISTENT']} consistent, {n_by['DIFFERENT']} different)" if worst != "IDENTICAL" else ""))
        if worst != "IDENTICAL" or verbose:
            for s, k, v, g in notes[:40 if not verbose else None]:
                print(f"       {s:10s} {k}: reference {v} now {g}")
    for fname in sorted(set(now) - set(ref)):
        print(f"   {'NOTE':10s} {fname:34s} not in the reference (new output)")
    out.update(counts)
    return counts["DIFFERENT"] == 0


# ------------------------------------------------------------------------------------------------------ 2. ledger
def judge(text_value, printed, scale, decimals, tol):
    """Compare one quoted number with the value it came from."""
    value = float(text_value) * float(scale)
    p = str(printed).strip()
    if p[0] in "<>":
        bound = float(p[1:])
        ok = value > bound if p[0] == ">" else value < bound
        return ("IDENTICAL" if ok else "DIFFERENT"), value
    printed = float(p)
    if abs(round_half_up(value, int(decimals)) - printed) < 1e-9:
        return "IDENTICAL", value
    if tol not in ("", None) and abs(value - printed) <= float(tol) + 1e-9:
        return "CONSISTENT", value
    return "DIFFERENT", value


def check_ledger(verbose, out):
    rows = list(csv.DictReader(open(LEDGER)))
    counts = {"IDENTICAL": 0, "CONSISTENT": 0, "DIFFERENT": 0, "NOT RUN": 0}
    lines = []
    for row in rows:
        try:
            if row["key"].startswith("="):
                value = eval(row["key"][1:], {"__builtins__": {}}, {"r": r, "round": round, "len": len, "abs": abs})
            else:
                value = r(row["results_file"], row["key"])
        except FileNotFoundError:
            status, value = "NOT RUN", None
        except (KeyError, IndexError, TypeError) as e:
            status, value = "DIFFERENT", None
            row = {**row, "note": f"key not found in the results ({e!r})"}
        else:
            status, value = judge(value, row["printed"], row["scale"], row["decimals"], row["tolerance"])
        counts[status] += 1
        shown = "" if value is None else f"{value:.6g}"
        lines.append((status, row, shown))
    print(f"\n2. numbers quoted in Appendix A against the results they come from (tests/appendix_a_numbers.csv, {len(rows)} rows)")
    print("   " + "  ".join(f"{k} {v}" for k, v in counts.items() if v))
    for status, row, shown in lines:
        if status == "IDENTICAL" and not verbose:
            continue
        print(f"   {status:10s} chart {row['chart']:>4s}  {row['quoted_in_appendix_a'][:78]}\n"
              f"{'':14s}printed {row['printed']}  result {shown}" + (f"   {row['note']}" if row["note"] else ""))
    out["ledger"] = counts
    return counts["DIFFERENT"] == 0


# ------------------------------------------------------------------------------------------------------ 3. data tables
def check_data_claims(verbose, out):
    from common.lifespans import load as load_lifespans
    raw = pd.read_csv(DATA / "B_enterprise_lifespans.csv")
    life = load_lifespans()
    ended_police_dated = int(life.event.sum())
    police_any = r("c02_police", "all.police_any")
    A1 = pd.read_csv(DATA / "A1_fraud_series.csv", dtype={"year": str})
    C_PAY, C2 = pd.read_csv(DATA / "C_pay.csv"), pd.read_csv(DATA / "C2_dev_pay_by_country.csv")
    G = pd.read_csv(DATA / "G_vendor_ai.csv")
    H = pd.read_csv(DATA / "H_espionage_cases.csv").set_index("campaign")
    J = pd.read_csv(DATA / "J_ai_vulns.csv")
    I = pd.read_csv(DATA / "I_adoption_lags.csv")
    ftc = lambda sid: float(A1[(A1.series_id == sid) & (A1.year == "2025")].value.iloc[0])
    vn = C2[C2.country == "Vietnam"].iloc[0]
    fx = 37.8e6 * 12 / vn.usd_annual                                    # VND per dollar implied by the row's own conversion
    row = lambda prefix: H[H.index.str.startswith(prefix)].iloc[0]
    yrs = lambda s: int(str(s)[:4]) if pd.notna(s) else None
    jnote = str(J[J.metric.str.contains("findings reported", na=False)].notes.iloc[0])
    claims = [   # (chart, quoted, value, printed, decimals[, tolerance])
        ("2", "152 named enterprises", len(raw), 152, 0),
        ("2", "in ten sectors", raw.sector.nunique(), 10, 0),
        ("2", "the 37 undated enterprises", len(raw) - len(life), 37, 0),
        ("2", "30 of them ended by police", police_any - ended_police_dated, 30, 0),
        ("1", "FTC conservative adjustment, $38bn", ftc("US_FTC_ADJ_FRAUD_LOW"), 38, 0),
        ("1", "FTC base-case adjustment, $262bn", ftc("US_FTC_ADJ_FRAUD_HIGH"), 262, 0),
        ("3", "Habr Career's headline figure for 2025, about $26,000 a year", C_PAY.iloc[17].usd_annual_low, 26000, -3),
        ("3", "BLS median wage for software developers, about $136,000 a year", C2[C2.country == "United States"].iloc[0].usd_annual, 136000, -3),
        ("3", "Vietnam: back-end developers with more than eight years' experience, about $25,000 (54.9 million dong a month)",
         54.9e6 * 12 / fx, 25000, -3),
        ("9", "BRICKSTORM average of 393 days (the table keeps it as 1.08 years)", float(row("UNC5221 BRICKSTORM").years_undetected) * 365, 393, 0, 2),
        ("9", "Kaspersky dates Equation Group to 2001", yrs(row("Equation Group").start), 2001, 0),
        ("9", "... and found it in 2015", yrs(row("Equation Group").discovered), 2015, 0),
        ("9", "Regin dated to 2003", yrs(row("Regin").start), 2003, 0),
        ("9", "... found in 2014", yrs(row("Regin").discovered), 2014, 0),
        ("9", "SolarWinds: first access in September 2019", str(row("SolarWinds SUNBURST (").start), "2019-09", None),
        ("9", "SolarWinds: discovered in December 2020", str(row("SolarWinds SUNBURST (").discovered)[:7], "2020-12", None),
        ("9", "Midnight Blizzard: from November 2023", str(row("Midnight Blizzard").start), "2023-11", None),
        ("9", "... to January 2024", str(row("Midnight Blizzard").discovered)[:7], "2024-01", None),
        ("9", "Ivanti: from December 2023", str(row("UNC5221 Ivanti").start)[:7], "2023-12", None),
        ("9", "... to January 2024", str(row("UNC5221 Ivanti").discovered)[:7], "2024-01", None),
        ("9", "Storm-0558: from May 2023", str(row("Storm-0558").start), "2023-05", None),
        ("9", "... to June 2023", str(row("Storm-0558").discovered)[:7], "2023-06", None),
        ("11", "19 of the 34 vendors shipped their first feature in 2023", int((G.first_year == 2023).sum()), 19, 0),
        ("11", "nine in 2024", int((G.first_year == 2024).sum()), 9, 0),
        ("11", "three in 2025", int((G.first_year == 2025).sum()), 3, 0),
        ("11", "three vendors with no security-specific generative-AI product: Dropbox, Atlassian, 1Password",
         ", ".join(sorted(G[G.substance.str.lower() == "none"].vendor)), "1Password, Atlassian, Dropbox", None),
        ("12", "6,157 reported to the maintainers of 591 projects", jnote.split(" projects")[0], "591", None),
        ("12", "6,123 reviewed by outsiders, 5,674 confirmed valid", "5674 of 6123 externally reviewed confirmed valid" in jnote, True, None),
        ("6", "agents run whole intrusions: available since early 2025 (24 Feb 2025)",
         str(I[I.technique == "Agentic intrusion / extortion"].availability_date.iloc[0]), "2025-02-24", None),
    ]
    counts = {"IDENTICAL": 0, "CONSISTENT": 0, "DIFFERENT": 0, "NOT RUN": 0}
    lines = []
    for chart, quoted, value, printed, dec, *tol in claims:
        if dec is None:
            status = "IDENTICAL" if value == printed else "DIFFERENT"
        elif abs(round_half_up(value, dec) - printed) < 1e-9:
            status = "IDENTICAL"
        elif tol and abs(value - printed) <= tol[0]:
            status = "CONSISTENT"
        else:
            status = "DIFFERENT"
        counts[status] += 1
        lines.append((status, chart, quoted, value, printed))
    print(f"\n3. numbers quoted from the data tables, recomputed from data/ ({len(claims)} claims)")
    print("   " + "  ".join(f"{k} {v}" for k, v in counts.items() if v))
    for status, chart, quoted, value, printed in lines:
        if status == "IDENTICAL" and not verbose:
            continue
        v = f"{value:,.1f}" if isinstance(value, float) else value
        print(f"   {status:10s} chart {chart:>4s}  {quoted[:90]}\n{'':14s}printed {printed}  data {v}")
    out["data"] = counts
    return counts["DIFFERENT"] == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true", help="print every line, not only those that are not IDENTICAL")
    ap.add_argument("--update-reference", action="store_true", help="re-snapshot results/ into tests/reference_numbers.json")
    args = ap.parse_args()
    if args.update_reference:
        import matplotlib
        import scipy
        meta = {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__,
                "matplotlib": matplotlib.__version__,
                "about": "every number written by the scripts in results/, flattened; written by tools/verify_numbers.py --update-reference"}
        REFERENCE.write_text(json.dumps({"_meta": meta, "files": snapshot()}, indent=0, sort_keys=False))
        print("wrote", REFERENCE)
        return 0
    meta = json.load(open(REFERENCE))["_meta"]
    import matplotlib
    import scipy
    now = {"numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__}
    same = all(meta.get(k) == v for k, v in now.items())
    print("libraries: " + ", ".join(f"{k} {v}" for k, v in now.items()) + ("  (the versions the article's run used)" if same else
          f"  (the article's run used numpy {meta['numpy']}, scipy {meta['scipy']}, pandas {meta['pandas']}, matplotlib {meta['matplotlib']}; "
          "expect some CONSISTENT lines)"))
    out = {}
    ok = check_snapshot(args.verbose, out)
    ok &= check_ledger(args.verbose, out)
    ok &= check_data_claims(args.verbose, out)
    print("\n" + ("OK: nothing is DIFFERENT." if ok else "FAILED: some numbers are DIFFERENT (see above)."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
