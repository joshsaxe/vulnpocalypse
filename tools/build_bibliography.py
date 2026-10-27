#!/usr/bin/env python3
"""Build the annotated bibliography from the data tables.

Every row of every table in data/ carries its source (source_title, source_url, publisher, pub_date, grade). This
script groups those rows by document and by chart and writes three things:

    docs/sources/cNN_*.md      one page per chart: every document behind it, grouped by publisher, saying which rows
                               of which table came from it and what they hold
    docs/BIBLIOGRAPHY.md       the index: how to read an entry, the grade key, one line per chart
    data/sources.csv           the same list with one row per chart and document, for sorting and filtering

It also reads data/extra_sources.csv (documents that numbers were typed from, or that notes columns name without a link)
and the links written inside notes columns. Nothing is fetched: the script only rearranges what the tables already say.

Usage:
    python tools/build_bibliography.py            # rewrite the outputs
    python tools/build_bibliography.py --check    # exit 1 if they are out of date, or if a table is not used where
                                                  # this script says it is

Row numbers are pandas row numbers (0 is the first data row, as the chart scripts count them); a spreadsheet shows that
row as number + 2 because of the header.
"""
import argparse
import csv
import io
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pandas as pd

from common.paths import DATA

DOCS = ROOT / "docs"
PAGES = DOCS / "sources"

# ------------------------------------------------------------------------------------------------------ what each chart rests on
# role: read     the chart or its model loads the table
#       checked  numbers typed into the script are verified against the table by tools/check_inputs.py
#       context  evidence the author drew on for a judgement; no script reads or checks it
# An optional third item restricts the table to the rows that feed this chart (a pandas query string).
CHARTS = [
    dict(n=0, slug="c00_lede_cost", name="The price of a hack (the lede figure)", tables=[], code=["charts/c00_lede_cost.py"],
         blurb=("Three automated jobs priced in AI tokens: finding a software flaw, breaking into an AI lab's code "
                "repository and building a browser exploit chain. Each number is one documented public case, not a market "
                "average, and all three are typed into `charts/c00_lede_cost.py` rather than read from a table. Only the "
                "automated part of each job is priced; much of a real attack is still done by hand.")),
    dict(n=1, slug="c01_losses", name="Losses to fraud and hacking, and the part caused by AI",
         tables=[("A1_fraud_series", "read"), ("A2_hacking_series", "read"), ("cpi_u", "read"),
                 ("A1_fraud_ai_evidence", "checked"), ("A2_hacking_ai_evidence", "checked")],
         code=["charts/c01_losses.py", "models/c01_loss_trend.py", "common/deflators.py"],
         blurb=("Twenty-three loss series from police, regulators, banks, insurers, statisticians and security vendors "
                "(FBI IC3, the FTC's Consumer Sentinel, UK Finance, the Australian ACCC, Japan's National Police Agency, "
                "Chainalysis, IBM and Ponemon, Verizon, Sophos and others), pooled by a dynamic-factor model that corrects for "
                "drift in how losses are reported, and priced in 2025 dollars with US CPI-U from the Bureau of Labor "
                "Statistics (other countries' price indices are hand-entered in `common/deflators.py`; see "
                "[PARAMETERS](../PARAMETERS.md)). The two `evidence` tables hold what the AI share rests on: counts of "
                "complaints that mention AI, surveys of how many breaches or phishing e-mails involved AI, and police and "
                "vendor claims, each graded. The weakest part of the chart is that AI share: it is a judgement informed by "
                "this evidence, not a measurement (see [METHODS](../METHODS.md)).")),
    dict(n=2, slug="c02_police", name="What happens to criminal enterprises",
         tables=[("B_enterprise_lifespans", "read")], code=["charts/c02_police.py", "common/lifespans.py"],
         blurb=("A hand-built list of 152 named criminal enterprises in ten sectors (ransomware brands, darknet markets, "
                "botnets and malware services, forums and others), each with how and when it ended, taken from takedown "
                "announcements, court records, sanctions notices and trackers. Most rows rest on one press report or "
                "tracker entry (grade B). The list is not a random sample: enterprises famous enough to be documented are more "
                "often ones police acted against, which probably flatters the police.")),
    dict(n=3, slug="c03_talent", name="What crime pays",
         tables=[("C_pay", "checked"), ("C2_dev_pay_by_country", "read"), ("F_pay", "checked", "index in [14, 15]")],
         code=["charts/c03_talent.py"],
         blurb=("Criminal pay comes from leaked chats of the Conti ransomware group (reported by KrebsOnSecurity and Trellix), "
                "Kaspersky's study of job adverts on dark-web forums, a US indictment and a UK National Crime Agency account "
                "of LockBit. Honest pay comes from Levels.fyi (self-reported total compensation), national statistics offices "
                "(the US Bureau of Labor Statistics, China's National Bureau of Statistics, Belarus's Belstat) and survey "
                "firms (Habr Career for Russia, DOU for Ukraine, ITviec for Vietnam, Kolesa for Kazakhstan, Brasscom for "
                "Brazil), at World Bank average exchange rates. The Russian figures and the exchange rate are typed into "
                "the chart script; they are listed under *Cited outside the tables* below.")),
    dict(n=4, slug="c04_amdahl", name="Amdahl's law for a ransomware gang",
         tables=[("E_stage_judgements", "read"), ("E_stage_times", "checked"), ("E_incident_timelines", "context"),
                 ("E_laundering", "context"), ("I_business_models", "context")],
         code=["charts/c04_amdahl.py"],
         blurb=("No public dataset measures a ransomware gang's working hours by stage, so the eight stage judgements are "
                "the author's own. They draw on incident timelines (Colonial Pipeline, Ireland's health service, Change "
                "Healthcare, MGM and others), leaked gang chats, National Crime Agency data on LockBit's affiliates, "
                "Sophos, Mandiant and Coveware timing statistics, and AI-lab threat reports. This page lists the evidence "
                "tables behind those judgements (none of them is read by the chart script) and, at the end, the sources the "
                "judgements name without a link.")),
    dict(n=5, slug="c05_inference", name="How long abusers keep access to hosted AI",
         tables=[("D_platform_cases", "read")], code=["charts/c05_inference.py"],
         blurb=("Disruption reports by OpenAI, Anthropic and Microsoft (2024-26), plus cases where no AI provider cut the "
                "operation off (self-hosted or resold models, criminal chatbots sold openly). The chart uses nine cases that were "
                "cut off and six that were not; the other rows in the table (influence operations, a model-copying campaign, bans at "
                "sign-up and two context rows) are not charted. Almost every row is grade C: a vendor describing its own "
                "detection, with no outside check and no denominator.")),
    dict(n=6, slug="c06_attacker_lag", name="How fast criminals adopt new technology",
         tables=[("I_adoption_lags", "read")], code=["charts/c06_attacker_lag.py"],
         blurb=("Eighteen techniques, each dated by when its enabling technology became publicly available and when criminal "
                "use became widespread (the definition of 'widespread' is in each row), from court records, security-vendor and "
                "AI-lab reports, academic papers and encyclopaedias. Fifteen are charted; the other three (neural machine "
                "translation, agentic ransomware and browser cryptojacking) are left out, the last because its dates were "
                "recalled rather than checked. The sample is hand-picked from well-known cases, so the medians are illustrative.")),
    dict(n=7, slug="c07_pay", name="Public versus private pay",
         tables=[("F_pay", "read")], code=["charts/c07_pay.py"],
         blurb=("State side: advertised pay scales and job adverts (NSA, GCHQ and the National Cyber Force, the NCSC), an "
                "official Israeli wage report (via Ynet) and a leaked salary sheet from i-Soon, a contractor to China's "
                "security ministries. Private side: Levels.fyi median total pay for machine-learning engineers in each country, "
                "and for engineers at OpenAI and Anthropic. These are advertised scales and self-reported pay, not payroll "
                "data, and the state figures are mostly averages for all staff, not engineers.")),
    dict(n=8, slug="c08_govlag", name="How far governments lag business",
         tables=[("G_adoption", "read")], code=["charts/c08_govlag.py"],
         blurb=("For each technology, a range of years in which it became mainstream in American business and a range in which it "
                "became mainstream in US defence and intelligence agencies, with the milestone used for each (a policy memo, "
                "a contract, a new organisation, a user count) taken from trade press, news reports and law-firm and "
                "encyclopaedia pages. Several of those milestones are named in the table's notes without a link; "
                "their pages are listed under *Cited outside the tables* below. Two grade-D rows (personal computers, corporate "
                "e-mail and web) were never sourced and are not used. The last row is a projection, not an observation.")),
    dict(n=9, slug="c09_state_patience", name="How long state hackers stay hidden",
         tables=[("H_espionage_cases", "read"), ("E_stage_times", "checked", "metric == 'Global median dwell time'")],
         code=["charts/c09_state_patience.py"],
         blurb=("Well-documented state-linked campaigns, each with the time from first intrusion to discovery and, where it was "
                "reported, how many of the systems reached were actually worked, from government advisories, vendor incident "
                "write-ups (Microsoft, Mandiant, Kaspersky and others) and press reports. The 14-day benchmark for all intrusions "
                "is one row of `E_stage_times`. Campaigns still hidden are missing from the sample by construction.")),
    dict(n=11, slug="c11_defenders", name="The defenders' build-up",
         tables=[("G_vendor_ai", "read")], code=["charts/c11_defenders.py"],
         blurb=("Left panel: a census of 34 security and platform vendors, each dated to its first substantive generative-AI "
                "security feature, from the vendor's own announcement or trade press (the vendor's page is the source; the "
                "feature grade A/B/C/none is the author's). Right panel: two typed spend judgements; the defensive anchors are "
                "two market-research houses' figures and the offensive guess rests on reporting about criminal AI tools. "
                "Those pages are listed under *Cited outside the tables* below.")),
    dict(n=12, slug="c12_funnel", name="AI-found flaws, from discovery to patch",
         tables=[("J_ai_vulns", "checked")], code=["charts/c12_funnel.py"],
         blurb=("The funnel comes from Anthropic's coordinated-disclosure dashboard (2 October 2026) and the exploitation rate "
                "from VulnCheck's tracker of AI-attributed vulnerabilities; the counts are typed into the script and checked "
                "against `J_ai_vulns.csv`. Each headline count has a single source, which is the organisation that runs "
                "the programme or tracker. The other documents are background on AI-found flaws.")),
]
CHART_NAMES = {c["n"]: c["name"] for c in CHARTS}
CHART_NAMES[10] = "The odds that AI agents become routine"
ROLE_TEXT = {"read": "read by the chart's scripts", "checked": "typed numbers checked against it by `tools/check_inputs.py`",
             "context": "evidence behind the author's judgements; no script reads it"}

GRADE_KEY = [
    ("A", "official statistic, court record or primary disclosure"),
    ("B", "peer-reviewed paper, or a reputable industry report that states its method"),
    ("C", "vendor or press report with a thin method"),
    ("D", "rumour, a single anonymous source, or dates recalled rather than checked"),
    ("E", "not verified at the primary source and relayed by secondary coverage (one row)"),
]


# ------------------------------------------------------------------------------------------------------------ small helpers
def norm_url(u):
    """A key that treats http/https, www, trailing slashes and percent-encoding alike."""
    p = urlsplit(u.strip())
    host = p.netloc.lower()
    host = host[4:] if host.startswith("www.") else host
    path = unquote(p.path)
    path = path[:-1] if path.endswith("/") and len(path) > 1 else path
    return host + path + (f"?{p.query}" if p.query else "")


def md_url(u):
    return u.strip().replace(" ", "%20").replace("(", "%28").replace(")", "%29").replace("<", "%3C").replace(">", "%3E")


def md_text(s):
    s = " ".join(str(s).split())
    for ch in ("\\", "[", "]", "*", "`", "<", ">"):
        s = s.replace(ch, "\\" + ch)
    return s


def trim(s, n):
    s = " ".join(str(s).split())
    if len(s) <= n:
        return s
    return s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:- ") + "…"


def uniq(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def some(items, k):
    items = uniq(i for i in items if i)
    return "; ".join(items) if len(items) <= k else "; ".join(items[:k]) + f"; and {len(items) - k} more"


def spans(nums):
    """[3,4,5,9] -> '3–5, 9'"""
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else (f"{nums[i]}, {nums[j]}" if j == i + 1 else f"{nums[i]}–{nums[j]}"))
        i = j + 1
    return ", ".join(out)


def rows_text(idx):
    idx = sorted(set(idx))
    return ("row " if len(idx) == 1 else "rows ") + spans(idx)


def years_text(vals):
    ys = sorted({str(v) for v in vals if str(v)})
    if ys and all(re.fullmatch(r"\d{4}", y) for y in ys):
        return spans([int(y) for y in ys])
    return ", ".join(ys)


def domain(u):
    h = urlsplit(u).netloc.lower()
    return h[4:] if h.startswith("www.") else h


# ------------------------------------------------------------------------------------------------------ describing a table's rows
def d_series(r):
    parts = [f"{trim(m, 85)} ({years_text(g.year)})" for m, g in r.groupby("measure", sort=False)]
    return some(parts, 3)


def d_col(col, n=100, k=3):
    return lambda r: some([trim(v, n) for v in r[col]], k)


DESCRIBE = {
    "A1_fraud_series": d_series,
    "A2_hacking_series": d_series,
    "A1_fraud_ai_evidence": d_col("claim", 100, 2),
    "A2_hacking_ai_evidence": d_col("claim", 100, 2),
    "B_enterprise_lifespans": d_col("name", 60, 4),
    "C_pay": d_col("role", 80, 3),
    "C2_dev_pay_by_country": lambda r: some([f"{c}: {trim(x, 60)} ({y})" for c, x, y in zip(r.country, r.role, r.year)], 3),
    "D_platform_cases": d_col("case_id", 40, 4),
    "E_incident_timelines": d_col("incident", 60, 4),
    "E_laundering": d_col("case", 70, 3),
    "E_stage_times": lambda r: some([f"{trim(s, 45)}: {m}" for s, m in zip(r.stage, r.metric)], 3),
    "F_pay": lambda r: some([f"{c}: {trim(x, 60)} ({y})" for c, x, y in zip(r.country, r.role, r.year)], 3),
    "G_adoption": d_col("technology", 60, 3),
    "G_vendor_ai": lambda r: some([("no substantive security feature (feature grade none)" if g.strip().lower() == "none"
                                    else f"first substantive feature {d} (feature grade {g})")
                                   for d, g in zip(r["first"], r.substance)], 2),
    "H_espionage_cases": d_col("campaign", 70, 3),
    "I_adoption_lags": d_col("technique", 70, 3),
    "I_business_models": d_col("role_or_model", 70, 3),
    "J_ai_vulns": lambda r: some([trim(v, 70) for v in r.label], 3),
    "cpi_u": lambda r: f"CPI-U annual averages ({years_text(r.year)})",
}


def load_table(name):
    """A table as strings (blank cells are ''), indexed by pandas row number. G_vendor_ai also gets its link and feature
    from data/G_vendor_ai_sources.md, which is where that table's sources are kept."""
    df = pd.read_csv(DATA / f"{name}.csv", dtype=str, keep_default_na=False)
    if name == "G_vendor_ai":
        md = (DATA / "G_vendor_ai_sources.md").read_text(encoding="utf-8")
        vkey = lambda s: re.sub(r"\s*\(.*?\)", "", s).replace(" / ", "/").strip().lower()   # "Splunk (Cisco)" is "Splunk"
        by = {}
        for line in md.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 6 and cells[5].startswith("http"):
                by[vkey(cells[0])] = dict(feature=cells[2], first=cells[3], source_url=cells[5])
        missing = [v for v in df.vendor if vkey(v) not in by]
        assert not missing, f"G_vendor_ai_sources.md has no row for {missing}"
        df["feature"] = [by[vkey(v)]["feature"] for v in df.vendor]
        df["first"] = [by[vkey(v)]["first"] for v in df.vendor]
        df["source_url"] = [by[vkey(v)]["source_url"] for v in df.vendor]
        df["source_title"] = [f"{v}: {by[vkey(v)]['feature']}" for v in df.vendor]
        df["publisher"] = df.vendor
        df["pub_date"] = ""                      # the table dates the feature, not the page
        df["grade"] = ""
    for c in ("source_url", "source_title", "publisher", "pub_date", "grade", "notes"):
        if c not in df.columns:
            df[c] = ""
    return df


URL_IN_TEXT = re.compile(r"https?://[^\s<>\"']+")


def urls_in(text):
    return [u.rstrip(".,;:)]}") for u in URL_IN_TEXT.findall(text)]


# ------------------------------------------------------------------------------------------------------------- build the entries
class Entry:
    def __init__(self, url):
        self.url, self.key = url, norm_url(url)
        self.titles, self.pubs, self.dates, self.grades = Counter(), Counter(), [], set()
        self.tables = OrderedDict()        # table -> [(row, describe-able row)]
        self.notes_in = OrderedDict()      # table -> [row numbers whose notes name this link
        self.extra = []                    # (supports, where_used) from data/extra_sources.csv
        self.n_rows = 0

    def add_row(self, table, idx, row):
        self.tables.setdefault(table, []).append(idx)
        self.n_rows += 1
        for col, ctr in (("source_title", self.titles), ("publisher", self.pubs)):
            if row[col].strip():
                ctr[row[col].strip()] += 1
        if row["pub_date"].strip():
            self.dates.append(row["pub_date"].strip())
        if row["grade"].strip():
            self.grades.add(row["grade"].strip())

    @property
    def title(self):
        if self.titles:
            return self.titles.most_common(1)[0][0]
        return self.url

    @property
    def publisher(self):
        if self.pubs:
            return self.pubs.most_common(1)[0][0]
        return domain(self.url)

    @property
    def date(self):
        return sorted(self.dates)[0] if self.dates else ""


def build_chart(chart, extras):
    entries = OrderedDict()
    unlinked = []                # (table, idx, row)
    frames = {}
    for spec in chart["tables"]:
        table, role = spec[0], spec[1]
        df = load_table(table)
        if len(spec) > 2:
            df = df.query(spec[2])
        frames[table] = df
        if table == "E_stage_judgements":          # judgements, not documents: its named sources are listed separately
            continue
        for idx, row in df.iterrows():
            own = row["source_url"].strip()
            if own:
                e = entries.setdefault(norm_url(own), Entry(own))
                e.add_row(table, idx, row)
            else:
                unlinked.append((table, idx, row))
            for u in urls_in(row["notes"]):
                if not own or norm_url(u) != norm_url(own):
                    e2 = entries.setdefault(norm_url(u), Entry(u))
                    e2.notes_in.setdefault(table, []).append(idx)
    for x in extras:
        if int(x["chart"]) != chart["n"]:
            continue
        e = entries.setdefault(norm_url(x["url"]), Entry(x["url"]))
        e.extra.append((x["supports"], x["where_used"]))
        e.titles[x["title"]] += 100
        e.pubs[x["publisher"]] += 100
        if x["pub_date"]:
            e.dates.append(x["pub_date"])
    return entries, unlinked, frames


def annotate(e, frames, chart):
    """The plain-text annotation of one entry, as a list of (table-or-None, text)."""
    parts = []
    for spec in chart["tables"]:
        t = spec[0]
        if t in e.tables:
            sub = frames[t].loc[sorted(set(e.tables[t]))]
            parts.append((t, rows_text(e.tables[t]), DESCRIBE[t](sub)))
    for t, idx in e.notes_in.items():
        if not (t in e.tables and set(idx) <= set(e.tables[t])):
            parts.append((t, rows_text(idx), "link written in the notes column"))
    return parts


def kind_of(e):
    if e.tables:
        return "table"
    if e.extra:
        return "extra"
    return "notes"


# ------------------------------------------------------------------------------------------------------------------ rendering
def entry_line(e, frames, chart):
    meta = [m for m in (e.date, ("grade " + "/".join(sorted(e.grades))) if e.grades else "") if m]
    head = f"- [{md_text(e.title)}]({md_url(e.url)})" + (f" · {' · '.join(meta)}" if meta else "")
    bits = []
    for t, rows, what in annotate(e, frames, chart):
        bits.append(f"`{t}` {rows}" + (f": {md_text(what)}" if what else ""))
    for sup, where in e.extra:
        bits.append(f"{md_text(sup)} *Used in:* {md_text(where)}")
    return head + (" — " + "; ".join(bits) if bits else "")


def plain_annotation(e, frames, chart):
    bits = []
    for t, rows, what in annotate(e, frames, chart):
        bits.append(f"{t} {rows}" + (f": {what}" if what else ""))
    for sup, where in e.extra:
        bits.append(f"{sup} Used in: {where}")
    return " | ".join(bits)


def page_for(chart, entries, unlinked, frames, judgement_sources):
    L = [f"# Chart {chart['n']}: {chart['name']}", "",
         f"[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/{chart['slug']}.png`](../../figures/{chart['slug']}.png) · "
         f"code: [`charts/{chart['slug']}.py`](../../charts/{chart['slug']}.py)", "",
         chart["blurb"], ""]
    if chart["tables"]:
        L += ["**Tables behind this chart**", ""]
        for spec in chart["tables"]:
            t, role = spec[0], spec[1]
            n = len(frames[t])
            what = f"{n} row{'s' if n != 1 else ''}" + (f" (of the {len(load_table(t))} in the file; the others feed other charts)" if len(spec) > 2 else "")
            L.append(f"- [`data/{t}.csv`](../../data/{t}.csv): {what}; {ROLE_TEXT[role]}.")
        L.append("")
    pubs = {e.publisher for e in entries.values()}
    L += [f"**{len(entries)} documents from {len(pubs)} publishers.**" + (
          " Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and "
          "what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the "
          "[bibliography index](../BIBLIOGRAPHY.md#grades)." if chart["tables"] else ""), ""]
    table_entries = [e for e in entries.values() if kind_of(e) == "table"]
    notes_entries = [e for e in entries.values() if kind_of(e) == "notes"]
    extra_entries = [e for e in entries.values() if kind_of(e) == "extra"]

    def block(title, items, intro=None):
        if not items:
            return []
        out = [f"## {title}", ""] + ([intro, ""] if intro else [])
        by_pub = OrderedDict()
        for e in sorted(items, key=lambda e: (e.publisher.casefold(), e.date, e.title.casefold())):
            by_pub.setdefault(e.publisher, []).append(e)
        for p, es in by_pub.items():
            out += [f"**{md_text(p)}**", ""]
            out += [entry_line(e, frames, chart) for e in es]
            out.append("")
        return out

    L += block("Documents in the tables", table_entries)
    L += block("Cited outside the tables", extra_entries + notes_entries,
               intro=("Numbers typed into a script, milestones that a table's notes name without a link, and links written inside "
                      "notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each "
                      "typed one supports and where it is used."))
    if judgement_sources:
        L += ["## Sources the stage judgements name without a link", "",
              "These come from the `key_sources` column of `data/E_stage_judgements.csv`. Most correspond to documents listed "
              "above (Sophos, Coveware, Chainalysis, Mandiant, Anthropic and Google reports); `prior-project RC-nnn` means a row "
              "of the evidence library of the author's earlier study, *Where are all the agentic cyber attacks?* (see the "
              "[index](../BIBLIOGRAPHY.md#earlier-study)).", ""]
        L += judgement_sources + [""]
    if unlinked:
        L += ["## Rows recorded without a link", "",
              "The table has no source link for these rows; the notes column says why.", ""]
        for t, idx, row in unlinked:
            what = DESCRIBE[t](pd.DataFrame([row]))
            g = f" (grade {row['grade']})" if row["grade"].strip() else ""
            L.append(f"- `{t}` row {idx}: {md_text(what)}{g}. {md_text(trim(row['notes'], 230))}")
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def judgement_lines():
    df = pd.read_csv(DATA / "E_stage_judgements.csv", dtype=str, keep_default_na=False)
    out = []
    for _, r in df.iterrows():
        if r["key_sources"].strip():
            label = trim(r["stage"].split("(")[0].strip(), 70)
            out.append(f"- {md_text(label)}: {md_text(r['key_sources'])}")
    return out


def index_page(per_chart, total_docs, n_pubs):
    L = ["# Annotated bibliography", "",
         "Where every number in the figures comes from. Each chart has a page listing the documents behind it, grouped by "
         "publisher, with what was taken from each one and which rows of which table it fed. The same list is in "
         "[`data/sources.csv`](../data/sources.csv), one row per chart and document, for sorting and filtering. "
         "A document that feeds two charts appears on both pages.", "",
         f"**{total_docs} distinct documents from {n_pubs} publishers** across the 13 figures. This list is built by "
         "[`tools/build_bibliography.py`](../tools/build_bibliography.py) from the `source_url` column of each data table, the links "
         "written in the tables' notes columns, and [`data/extra_sources.csv`](../data/extra_sources.csv) (documents that numbers "
         "were typed from). It contains every link in the post's list of chart sources, and more: the tables cite some documents "
         "that the post's shorter list leaves out. The sources for the post's *text* are cited in the post itself.", "",
         "## How reliable is this?", "",
         "- The data tables were compiled by AI research agents working from public web sources in October 2026, under a brief "
         "that told them to open every page they took a number from, to prefer primary sources, to grade each data point and "
         "never to invent a number, date or source. They were **not reviewed row by row by a human or by an independent "
         "party**. The `notes` column of each table says where a page could not be opened, where a figure was relayed "
         "second-hand, and where the agents disagreed with each other.",
         "- Not every link has been re-fetched for this repository. Links rot: if one has gone, search for the title, or try the "
         "Internet Archive's Wayback Machine.",
         "- Many numbers are echoes of a single source. The grade says how good that source is, not how many repeat it.",
         "- The newest evidence, on AI misuse and AI-found flaws, is mostly grade C or B: vendors and AI labs describing their own "
         "detections, with no outside check and no denominator.", "",
         "## Grades", "", "Every row in the tables carries the grade of its source:", ""]
    L += [f"- **{g}**: {t}" for g, t in GRADE_KEY]
    L += ["", "The grade describes the *source*, not the claim. Chart 7 uses it to set how much each pay figure counts (grade A "
          "0.15, B 0.25, C 0.40, D 0.60 as the standard deviation of the log of pay). In `G_vendor_ai`, which has no source "
          "grade, a separate A/B/C/none grade describes the vendor's *feature* (A: autonomous or deeply integrated generative "
          "AI; B: an assistant or copilot generally available; C: announced or thin; none: nothing substantive).", "",
          "## By chart", "",
          "| Chart | Page | Documents | Publishers | Rows by grade (A / B / C / D / E) |", "|---|---|---:|---:|---|"]
    for c, entries, frames in per_chart:
        if c["n"] > 10 and not any(r.startswith("| 10.") for r in L):
            L.append("| 10. The odds that AI agents become routine | — | — | — | built from the models behind Charts 6 and 8; "
                     "their sources are on those pages |")
        pubs = {e.publisher for e in entries.values()}
        cnt = Counter()
        for spec in c["tables"]:
            t = spec[0]
            cnt.update(g for g in frames[t]["grade"] if g.strip())
        gtxt = " / ".join(str(cnt.get(g, 0)) for g in "ABCDE") if cnt else "—"
        L.append(f"| {c['n']}. {c['name']} | [`{c['slug']}.md`](sources/{c['slug']}.md) | {len(entries)} | {len(pubs)} | {gtxt} |")
    L += ["", "Rows are counted by row, not by document, so a document that feeds many rows counts many times. Charts 0, 3, 8, 11 and 12 "
          "also rest on documents cited outside the tables; those have no grade of their own.", "",
          "## Earlier study", "",
          "The level of losses in Chart 1 and the headcount of cybercriminals cited in the post come from the author's earlier study, "
          "*Where are all the agentic cyber attacks? Data, model and figures* (repository `where-are-the-agentic-cyber-attacks`, "
          "version 1.0, 17 October 2026). That study has its own evidence library; the numbers taken from it are typed into the "
          "scripts and listed in [PARAMETERS](PARAMETERS.md) (look for \"the author's earlier triangulation\"). Rows in "
          "`data/E_stage_judgements.csv` that cite `prior-project RC-nnn` refer to rows of that library.", "",
          "## Reading a row of `data/sources.csv`", "",
          "| Column | Meaning |", "|---|---|",
          "| `chart` | The figure (0 is the lede figure). |",
          "| `publisher`, `title`, `url`, `pub_date` | As recorded in the table; `pub_date` may be a year or a month. |",
          "| `grade` | The grade(s) of the rows that cite it; blank for documents cited outside the tables. |",
          "| `kind` | `table` (the link is a row's `source_url`), `notes` (the link is written in a notes column) or `extra` "
          "(`data/extra_sources.csv`). |",
          "| `tables`, `rows` | Which tables it feeds and which rows (pandas row numbers). |",
          "| `supports` | What was taken from it, in words. |", ""]
    return "\n".join(L)


def sources_csv(per_chart):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["chart", "publisher", "title", "url", "pub_date", "grade", "kind", "tables", "rows", "supports"])
    for c, entries, frames in per_chart:
        for e in sorted(entries.values(), key=lambda e: (e.publisher.casefold(), e.date, e.title.casefold())):
            tabs = [t for t in [s[0] for s in c["tables"]] if t in e.tables]
            rows = "; ".join(f"{t}: {spans(e.tables[t])}" for t in tabs)
            w.writerow([c["n"], e.publisher, e.title, e.url, e.date, "/".join(sorted(e.grades)), kind_of(e), " ".join(tabs), rows,
                        plain_annotation(e, frames, c)])
    return buf.getvalue()


# --------------------------------------------------------------------------------------------------------------------- checks
def check_roles():
    """Each table must be used where this script says: 'read' tables named in the chart's code, 'checked' tables in check_inputs."""
    problems = []
    check_src = (ROOT / "tools" / "check_inputs.py").read_text(encoding="utf-8")
    for c in CHARTS:
        code = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in c["code"])
        for spec in c["tables"]:
            t, role = spec[0], spec[1]
            if role == "read" and f"{t}.csv" not in code:
                problems.append(f"chart {c['n']}: {t} is not read by {c['code']}")
            if role == "checked" and f'"{t}.csv"' not in check_src and f"{t}.csv" not in check_src:
                problems.append(f"chart {c['n']}: {t} is not checked by tools/check_inputs.py")
    used = {s[0] for c in CHARTS for s in c["tables"]} | {"E_stage_judgements", "G_vendor_ai"}
    for p in sorted(DATA.glob("*.csv")):
        if p.stem not in used and p.stem not in ("extra_sources", "sources"):
            problems.append(f"data/{p.name} is not attached to any chart in tools/build_bibliography.py")
    return problems


def build():
    extras = list(csv.DictReader(open(DATA / "extra_sources.csv", encoding="utf-8")))
    per_chart, pages = [], {}
    all_urls, all_pubs = set(), set()
    for c in CHARTS:
        if not c["tables"] and not any(int(x["chart"]) == c["n"] for x in extras):
            continue
        entries, unlinked, frames = build_chart(c, extras)
        js = judgement_lines() if c["n"] == 4 else []
        pages[f"sources/{c['slug']}.md"] = page_for(c, entries, unlinked, frames, js)
        per_chart.append((c, entries, frames))
        all_urls |= set(entries)
        all_pubs |= {e.publisher.casefold() for e in entries.values()}
    out = {"BIBLIOGRAPHY.md": index_page(per_chart, len(all_urls), len(all_pubs)) + "\n"}
    out.update({k: v for k, v in pages.items()})
    out["../data/sources.csv"] = sources_csv(per_chart)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if the outputs are out of date")
    args = ap.parse_args()
    problems = check_roles()
    for p in problems:
        print("PROBLEM:", p)
    out = build()
    stale = []
    for rel, text in out.items():
        path = (DOCS / rel).resolve()
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if args.check:
        for s in stale:
            print("OUT OF DATE:", s)
        print("bibliography: " + ("OK" if not stale and not problems else "needs attention"))
        sys.exit(1 if stale or problems else 0)
    print(f"wrote {len(out)} files: " + ", ".join(sorted(out)))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
