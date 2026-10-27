# Data

Everything the charts read, as plain CSV files that open in any spreadsheet. There are 20 tables (1,627 rows), one markdown companion file and two lists of sources: one made by hand (`extra_sources.csv`) and one built from the tables (`sources.csv`).

This page says what each table is, what a row means, which chart reads it, how far to trust it and which rows no chart uses. For where each number came from, see the [annotated bibliography](../docs/BIBLIOGRAPHY.md); for the few numbers that are typed into scripts rather than read from a table, see [PARAMETERS](../docs/PARAMETERS.md).

**Row numbers.** Wherever these docs say "row 14", they mean the pandas row number (0 is the first data row, as the chart scripts count). A spreadsheet shows that row as number + 2, because of the header and because spreadsheets start at 1.

```python
import pandas as pd
F = pd.read_csv("data/F_pay.csv")
F.iloc[14]          # row 14 of the docs = spreadsheet row 16
```

## What is here

The letter at the start of a file name is the research workstream that produced the table (A was losses, B police, and so on). The letters do not follow the order of the charts, and `C2` was added later to `C`. "Read" means a chart script or model loads the table; "checked" means numbers typed into a script are verified against it by [`tools/check_inputs.py`](../tools/check_inputs.py); "context" means the evidence behind a judgement, which no script reads.

| File | Rows | One row is | Chart | How it is used |
|---|---:|---|---|---|
| [`A1_fraud_series.csv`](A1_fraud_series.csv) | 590 | one year of one published series of fraud losses (95 series) | 1 | read: 14 series (154 rows) are pooled |
| [`A2_hacking_series.csv`](A2_hacking_series.csv) | 434 | one year of one published series on hacking losses, or a count that stands for them (89 series) | 1 | read: 9 series (61 rows) are pooled |
| [`A1_fraud_ai_evidence.csv`](A1_fraud_ai_evidence.csv) | 47 | one claim or statistic about the role of AI in fraud | 1 | checked |
| [`A2_hacking_ai_evidence.csv`](A2_hacking_ai_evidence.csv) | 34 | one claim or statistic about the role of AI in hacking | 1 | checked |
| [`cpi_u.csv`](cpi_u.csv) | 21 | one year of the US consumer price index, 2005-25 | 1 | read |
| [`B_enterprise_lifespans.csv`](B_enterprise_lifespans.csv) | 152 | one named criminal enterprise and how it ended | 2 | read: every row; 115 have dates |
| [`C_pay.csv`](C_pay.csv) | 31 | one pay observation: criminal, honest or state | 3 | checked |
| [`C2_dev_pay_by_country.csv`](C2_dev_pay_by_country.csv) | 16 | one country's average or median software-developer pay | 3 | read |
| [`F_pay.csv`](F_pay.csv) | 52 | one pay observation for a security agency or a private tech employer | 7 (and 3) | read: 20 rows for Chart 7; rows 14-15 also checked for Chart 3 |
| [`E_stage_judgements.csv`](E_stage_judgements.csv) | 9 | one stage of a ransomware attack (eight), plus a text row that sums them up | 4 | read: the eight stages |
| [`E_stage_times.csv`](E_stage_times.csv) | 23 | one published timing, payment-rate or ransom statistic | 4, 9 | checked; one row ("Global median dwell time") is also checked for Chart 9 |
| [`E_incident_timelines.csv`](E_incident_timelines.csv) | 11 | one named ransomware incident | 4 | context |
| [`E_laundering.csv`](E_laundering.csv) | 11 | one laundering case | 4 | context |
| [`I_business_models.csv`](I_business_models.csv) | 20 | one criminal role or business model, before or after AI | 4 | context |
| [`D_platform_cases.csv`](D_platform_cases.csv) | 81 | one disclosed case of AI misuse, or a context row | 5 | read: 15 rows are drawn |
| [`I_adoption_lags.csv`](I_adoption_lags.csv) | 18 | one technique and how long criminals took to adopt it | 6 (and 10) | read: 15 rows are used |
| [`G_adoption.csv`](G_adoption.csv) | 10 | one technology and when business and the US security agencies adopted it | 8 (and 10) | read: 7 rows (6 fitted, 1 only shown) |
| [`H_espionage_cases.csv`](H_espionage_cases.csv) | 21 | one state-linked campaign, benchmark or contrast case | 9 | read: 9 campaigns; one benchmark row is checked |
| [`G_vendor_ai.csv`](G_vendor_ai.csv) | 34 | one security or platform vendor | 11 | read: every row |
| [`J_ai_vulns.csv`](J_ai_vulns.csv) | 12 | one headline count about AI-found software flaws | 12 | checked |
| [`G_vendor_ai_sources.md`](G_vendor_ai_sources.md) | | the feature and source page for each vendor in `G_vendor_ai.csv` | 11 | read by humans; the bibliography merges it |
| [`extra_sources.csv`](extra_sources.csv) | 23 | one document that a number was typed from, or that notes name without a link | 0, 3, 4, 6, 8, 11 | the source list for typed numbers |
| [`sources.csv`](sources.csv) | 613 | one document cited for one chart | all | built by [`tools/build_bibliography.py`](../tools/build_bibliography.py); do not edit by hand |

Chart 0 (the lede) and Chart 10 (the odds) have no table of their own. Chart 0 prices three documented cases typed into its script (see [PARAMETERS](../docs/PARAMETERS.md)), and Chart 10 combines the posterior draws that Charts 6 and 8 save.

## Columns every table shares

Almost every table ends with the same columns, which say where the row came from:

| Column | Meaning |
|---|---|
| `source_title` | The title of the page, report or filing the row was taken from. |
| `source_url` | Its address. Several rows can share one. A few rows have none (see "How reliable is this?"). |
| `publisher` | Who published it: an agency, a company, a news outlet, a journal. |
| `pub_date` | When it was published. It may be a year or a month. |
| `grade` | How good the source is (below). |
| `notes` | The compiler's comments: quirks, caveats, where a page could not be opened, how a number was derived. |

Three tables differ. `G_vendor_ai.csv` has no source columns (its sources are in `G_vendor_ai_sources.md`), `E_stage_judgements.csv` has `key_sources` instead (a free-text list), and `cpi_u.csv` has no publisher or publication date.

## Grades

The grade describes the *source*, not the claim.

| Grade | Meaning |
|---|---|
| **A** | Official statistic, court record or primary disclosure. |
| **B** | Peer-reviewed paper, or a reputable industry report that states its method. |
| **C** | Vendor or press report with a thin method. |
| **D** | Rumour, a single anonymous source, or dates recalled rather than checked. |
| **E** | Not verified at the primary source and relayed by secondary coverage (one row). |

Chart 7 uses the grade to set how much each pay figure counts: standard deviation of the log of pay 0.15 for A, 0.25 for B, 0.40 for C and 0.60 for D. No other chart weights by *source* grade.

`G_vendor_ai.csv` has two codes of its own, and Chart 11 weights by them. `substance` is the author's grade for the vendor's *feature*: A, autonomous or deeply integrated generative AI; B, an assistant or copilot that is generally available; C, announced or thin; `none`, nothing substantive (the vendor stays in the count). The model counts a vendor's feature with probability 1.0 for A, 0.95 for B, 0.60 for C and 0 for `none`. `date_conf` is how sure the date is: A, that year for certain; B, that year with probability 0.8, otherwise a year either side; C, that year with probability 0.5.

## How reliable is this?

- The tables were compiled by **AI research agents** working from public web sources in October 2026. Their brief told them to open every page they took a number from, to prefer primary sources, to grade each data point and never to invent a number, date or source. **No human or independent party has reviewed the tables row by row.** The repository checks that the typed numbers match the tables and that the published numbers match the scripts; it does not check the tables against the world.
- **Not every link has been re-fetched** for this repository. Links rot. If one has gone, search for the title or try the Internet Archive's Wayback Machine.
- Some rows say so in their `notes`. The agents' own markers are `UNVERIFIED`, `RECALLED`, `not re-fetched` and `GAP`; search the notes columns for them. A `not re-fetched` note means the value was carried over from the author's earlier study (fetched 17 October 2026) without opening the page again.
- **A blank is better than a recalled date.** Where a date could not be checked, the agents left it empty. That is why only 115 of the 152 enterprises in `B_enterprise_lifespans.csv` are dated and enter the cumulative-incidence estimate in Chart 2. All 152 enter the sector shares, which need only how each enterprise ended.
- **Fourteen rows have grade D or E.** Only three of them are charted: BidenCash, LabHost and 16shop in `B_enterprise_lifespans.csv` (rows 121, 141 and 142). The agents recalled that each was ended by police but could not open a page, so they are marked unverified and left undated. They count in the sector shares in Chart 2. Delete the three rows and rerun `charts/c02_police.py` to see what they are worth: the median share of ended enterprises that police ended moves from 74.0% to 73.4%. The other eleven rows are context or are left out of every chart (listed below).
- **Many numbers echo one source.** The grade says how good that source is, not how many outlets repeat it.
- **The newest evidence is the thinnest.** The rows on AI misuse and AI-found flaws (`D_platform_cases`, `J_ai_vulns`, the `ai_evidence` tables) are mostly grade C or B: companies describing their own detections, with no outside check and no denominator.
- **Some numbers live in `notes` columns.** The funnel behind Chart 12 is an example: the 29,439 candidate flaws and the 5,103 acknowledged reports are in the notes of `J_ai_vulns.csv` row 7, and the benchmark of about 1.4% of all vulnerabilities being exploited is in the notes of row 10. The chart script types them, and `tools/check_inputs.py` confirms each against the note.
- **Three of the headline judgements are not in a table.** The level of 2025 losses in Chart 1 comes from the author's earlier study, and Chart 4's stage shares and Chart 11's spending judgements are the author's own. [PARAMETERS](../docs/PARAMETERS.md) lists them with their ranges.

## Table by table

Columns not listed here are the shared ones above.

### A. Losses to fraud and hacking (Chart 1)

**`A1_fraud_series.csv`** and **`A2_hacking_series.csv`** are long tables: one row per series per year.

| Column | Meaning |
|---|---|
| `series_id` | A stable name for a series, such as `UK_FIN_UNAUTH_LOSS`. A break in definition is a different series. |
| `geography` | Country or region the series covers. |
| `measure` | What is counted, in words. |
| `year` | The year. In `A2` it is occasionally a span such as `2026-04/2026-06`; the model reads four-digit years only. |
| `value`, `unit`, `currency` | The figure, in the unit named (US$ bn, £ m, a count, a share). `A2` mixes dollars, counts and shares, so read `unit` before using a value. |
| `definition`, `coverage_notes` | What the series includes and leaves out, and any break or revision. |

The tables hold far more series than the model pools: 95 fraud series and 89 hacking series, of which 14 and 9 are used. The rest are the FBI's individual crime categories (about fifty of them), earlier vintages of the same Chainalysis estimates, alternative totals, series for other countries, one-off global estimates (for example the United Nations' for Southeast Asia) and, in `A2`, insurance, survey and single-incident figures (Bybit, NotPetya, WannaCry and others). They stay in the table as context. A few series are rebuilt in the model from several rows (the FBI's fraud-type losses are the total times the fraud-type share) or entered as typed vintages (Chainalysis scam revenue, FinCEN ransomware payments); [PARAMETERS](../docs/PARAMETERS.md) lists those.

**`A1_fraud_ai_evidence.csv`** and **`A2_hacking_ai_evidence.csv`** hold what the AI share in Chart 1 rests on.

| Column | Meaning |
|---|---|
| `claim` | The statement, in words (for example how many complaints mention AI, or a police warning about voice cloning). |
| `metric`, `value`, `unit`, `period`, `geography` | The number, if there is one; some rows are qualitative. |
| `ai_role` | What AI did in the case: lure text, cloned voice, deepfake video, a model run inside malware, an agent that ran an intrusion. |
| `but_for_judgement` | The compiler's view on whether the loss would not have happened without AI ("but-for"), or whether AI was merely present. It is an opinion; it is what the chart's but-for percentages were built from, not a measurement. |

Chart 1's AI-share inputs (for example that about 4.2% of the dollars in FBI fraud-type complaints mention AI) are typed in `models/c01_loss_trend.py` and checked against these tables.

**`cpi_u.csv`**: the US consumer price index, annual averages from the Bureau of Labor Statistics, used to put every US-dollar series in 2025 dollars. Other countries' price indices are hand-entered in `common/deflators.py` and are not backed by a table; see [PARAMETERS](../docs/PARAMETERS.md).

### B. How criminal enterprises end (Chart 2)

**`B_enterprise_lifespans.csv`**

| Column | Meaning |
|---|---|
| `name` | The enterprise: a ransomware brand, darknet market, botnet or malware service, forum, laundering service, and so on. |
| `sector` | One of ten: `ransomware`, `darknet_market`, `botnet_maas`, `forum`, `mixer_laundering`, `bph_vpn`, `phaas`, `carding_shop`, `ddos_booter`, `scam_compound`. The last five are pooled as "other services" in the chart. |
| `first_seen`, `end_date` | Year, month or day; blank if not checked. |
| `end_type` | `le_takedown`, `le_seizure`, `le_arrests`, `sanctions` (police endings); `rebrand_after_le_pressure` (counted as police pressure); `voluntary_retirement`, `exit_scam`, `rebrand_other` (not police); `still_active`. |
| `le_involved` | `yes`, `no` or `partial`: whether law enforcement was involved at all. |
| `base_region` | Where the operators were believed to be (free text). |

The list is not a random sample: enterprises famous enough to be documented are more often ones police acted against, which probably flatters the police. Endings that were not police actions are treated as censoring in the dated estimate (the enterprise survived police at least that long), which is why the table keeps the non-police endings.

### C and F. What crime pays, and what governments pay (Charts 3 and 7)

**`C_pay.csv`**: one observation per row. `role`, `sector` (`criminal`, `legit` or `state`), `country`, `pay_low`, `pay_high` in the local `currency` per `period` (month, year, per call and so on), `year`, and the same converted to `usd_annual_low` and `usd_annual_high`. The exchange rates are in the notes. Chart 3 types its criminal and Russian figures and `check_inputs.py` confirms them against these rows.

**`C2_dev_pay_by_country.csv`**: honest developer pay in nine countries. `country`, `role`, `basis` (mean or median, gross or net, and what the figure covers), `pay_local`, `currency`, `period`, `year`, `usd_annual`, `fx_rate_used` and `fx_note`. Chart 3 reads it.

**`F_pay.csv`**: the pay comparison behind Chart 7. `country`, `sector` (`national_security`, `other_government`, `private_tech`, `private_frontier_ai`), `role`, low and high pay in local currency (`pay_low_local`, `pay_high_local`) per `period`, `currency`, `year`, the same in US dollars a year, the exchange rate used (`fx_rate_used`) and `basis` (`advertised`, `median`, `survey` or `anecdote`). Chart 7 uses 20 of the 52 rows, listed by number in `USE` in `charts/c07_pay.py`: for each of the United States, United Kingdom, Israel and China, the state rows and the private-sector median, and for the United States also the OpenAI and Anthropic medians. The other rows (Russia, Iran, North Korea, a reported Meta offer of up to $300 million, other agencies) are context.

State pay is mostly an average for all staff or an advertised scale, not what an engineer is paid, and private pay is self-reported (Levels.fyi) or surveyed. Pensions and job security, which narrow public-private gaps, are left out. Chart 7 puts that mismatch into the uncertainty (a role-mismatch term of 0.25 in log pay on every source).

### D. How long abusers keep access to hosted AI (Chart 5)

**`D_platform_cases.csv`**

| Column | Meaning |
|---|---|
| `case_id` | A short key. The prefix says who reported it: `ANT` Anthropic, `OAI` OpenAI, `MS` Microsoft, `GTIG` Google's Threat Intelligence Group, `SENT` SentinelOne, `CS` CrowdStrike, `AWS` Amazon, `SYS` Sysdig, `SVC` a service sold openly, `CTX` a context row. |
| `provider`, `actor_type` | The AI provider whose model was used; `criminal`, `state`, `fraud`, `influence`, `hacktivist`, `mixed` or `other`. |
| `activity` | What the actors did, in words. |
| `start_date`, `detect_date`, `end_date` | When the activity began, was noticed and was cut off, as far as the report says. |
| `duration_days_low`, `duration_days_high`, `duration_basis` | Bounds on how long it ran, and what they rest on. |
| `scale_metric`, `scale_value_low`, `scale_value_high` | How big it was (accounts, victims, operations), if the report says. |
| `outcome`, `moved_elsewhere` | What the provider did, and where the actors went next. |

Chart 5 draws 15 of the 81 rows: nine hacking, fraud or spying cases that a provider cut off, and six where no provider ended it. They are listed with their duration bounds in `CAUGHT` and `NOTCUT` in `charts/c05_inference.py`. Where the table's duration columns are blank or give only one bound, the script types the bounds from dates in the notes or assumes the missing one; `tools/check_inputs.py` says which for each case. The other 66 rows are influence operations, a model-copying campaign, bans at sign-up, platform-wide enforcement tallies, cases whose report gives no usable duration and two context rows. They stay in the table as background.

### E. The anatomy of a ransomware attack (Chart 4)

**`E_stage_judgements.csv`** is the one table of the author's own judgements. For each of eight stages: `labour_share_low`, `_mid`, `_high` (the stage's share of the working hours behind one big attack) and `ai_automatable_low`, `_mid`, `_high` (the share of that work today's best AI could do unaided), the `reasoning` and `key_sources` (a free-text list; "RC-nnn" means a row of the earlier study's evidence library). The ninth row, "AGGREGATE / Amdahl reading", is text and is not read.

No public dataset measures a gang's working hours by stage, so these are judgements informed by the evidence tables below, not measurements. **They describe the hours behind one attack, mostly an affiliate's** (the crew that breaks in), not the platform operators' hours; platform overhead is a small share of an affiliate's hours but, by the row's own estimate, 15-25% of whole-ecosystem hours.

**`E_stage_times.csv`**: published timing statistics (dwell times, time to the domain controller, time to exfiltration, negotiation length, payment rates, ransom sizes) from Sophos, Mandiant, Coveware, Unit 42, CrowdStrike, Huntress, BakerHostetler, the DFIR Report and Chainalysis. `stage`, `metric`, `value`, `unit`, `population` (who was counted) and `year`. Chart 4 types the numbers it quotes and `check_inputs.py` confirms them here; the "Global median dwell time" row (14 days) is the benchmark in Chart 9.

**`E_incident_timelines.csv`**, **`E_laundering.csv`** and **`I_business_models.csv`** are the evidence the stage judgements were written from. No script reads them. They are kept because a reader who disagrees with a judgement should be able to see what it rested on.

- `E_incident_timelines`: `incident`, `actor`, dates of initial access and of detection or encryption, `dwell_days`, `initial_access_method`, `manual_steps`, and the ransom demanded and paid and total cost in dollars.
- `E_laundering`: `case`, `amount_usd`, `steps`, `duration_days` and `human_steps`. Two rows (Garantex, row 8; the Ronin bridge theft, row 9) are grade D, recalled rather than checked.
- `I_business_models`: `role_or_model`, `era` (`pre_AI` or `AI`), `description`, `revenue_share_or_price` and `evidence`.

### G. How fast governments and businesses adopt technology (Chart 8)

**`G_adoption.csv`**: one technology per row, with a range of years in which it became mainstream in American business (`private_mainstream_year_low`, `_high`) and in US defence and intelligence agencies, the "national security" side (`ns_mainstream_year_low`, `_high`), the year the technology first became available to business (`private_first_available_year`) and was first used by the agencies (`ns_first_use_year`), the milestone chosen for each side in words (`private_milestone_desc`, `ns_milestone_desc`), and `confidence` (`high`, `medium`, `low`). Milestones differ by row: a policy memo, a large contract, a new organisation, a user count.

Chart 8 reads seven rows. Six are fitted. The seventh, the switch to video calls in the Covid emergency, is drawn but not fitted, because an emergency is not routine adoption. Rows 0 and 1 (personal computers; corporate e-mail and the web) are grade D and were never sourced (the compiler's note says `GAP`), so they are not used. The last row, "Agentic AI for offensive cyber", is a projection, not an observation; the chart's projection comes from the fitted model instead.

**`G_vendor_ai.csv`** is the vendor census for Chart 11: `vendor`, `tier` (`Pure-play` security vendors, `Platform` companies and `Adjacent` firms whose business is not security), `first_year` of the first substantive generative-AI security feature, `substance` and `date_conf` (see the grades above). Its sources are in [`G_vendor_ai_sources.md`](G_vendor_ai_sources.md), which gives the feature, the month and the link for each vendor.

### H. How long state hackers stay hidden (Chart 9)

**`H_espionage_cases.csv`**: `campaign`, `attributed_state` (with who made the attribution and how firm it is), `start`, `discovered`, `years_undetected`, `victims_broad` (free text: how many systems were reached) and `victims_targeted` (free text: how many were actually worked), `stealth_tradecraft` and `human_effort`. The chart reads nine campaigns: Equation Group, Regin, SolarWinds, Volt Typhoon (its five years is a lower bound), BRICKSTORM, the OPM breach, Midnight Blizzard, the Ivanti zero-days and Storm-0558. The 122-day benchmark for espionage cases is the "M-Trends 2026" row, typed in the script and checked here.

The campaigns are the ones later discovered and made public, so campaigns still hidden are missing by construction and famous ones are over-represented.

### I. How fast criminals adopt new technology (Chart 6)

**`I_adoption_lags.csv`**: `technique`, `enabling_tech`, `availability_date`, `first_criminal_use_date`, `scaled_use_date`, `scaled_definition` (what "widespread" means for this row), `lag_first_years`, `lag_scaled_years` and `why_slow_or_fast`. Dates may be a year or a day. Charts 6 and 10 use 15 of the 18 rows: twelve that scaled and three that have not yet. Chart 6 overrides one lag from the table (hijacked-gadget botnets, 2.3 years, dated from the arrival of cheap insecure gadgets in about 2014 rather than from the first Mirai sighting; the table's own figure is 0.1), and `sensitivity/s06_adoption_lags.py` shows what that choice is worth. The classes (ready-made exploits, new tools, new business models) are assigned in the chart script, not in the table, and were assigned knowing the outcomes.

### J. AI-found software flaws (Chart 12)

**`J_ai_vulns.csv`**: `date`, `side` (`defender`, `attacker` or `both`), `program_or_tool`, `organization`, `model_access`, `metric`, `value` and `label` (the short name used in the chart). Each headline count has one source, usually the organisation that runs the programme or tracker, and none of them has an outside check. The funnel in Chart 12 is rows 7 and 8 (Anthropic's disclosure dashboard, 2 October 2026) and the exploitation rate is rows 9 and 10 (VulnCheck, 28 July 2026). The other rows are background.

## Rows no chart uses

| Table | Rows left out | Why |
|---|---|---|
| `A1_fraud_series` | 81 of 95 series | not pooled: crime categories, earlier vintages, alternative totals, other countries, one-off estimates |
| `A2_hacking_series` | 80 of 89 series | not pooled; includes two grade-D rows, a security-industry global cost estimate (row 117) and a WannaCry total carried over from the earlier study (row 322) |
| `A1_fraud_ai_evidence`, `A2_hacking_ai_evidence` | those not typed into the script | background for the AI-share judgement; the Pindrop row (A1 row 33, grade D) is marked "do not use as AI attribution" |
| `F_pay` | 32 of 52 | other countries and agencies, a reported outlier offer (row 16, grade D), Iran (row 50, grade D, n = 11) |
| `D_platform_cases` | 66 of 81 | no usable duration or not a hacking, fraud or spying case (see above); row 80 is grade E, relayed second-hand |
| `I_adoption_lags` | rows 11, 16, 17 | no criminal-use dates (neural translation), unclear dates (agentic ransomware), dates recalled not checked (browser cryptojacking, grade D) |
| `G_adoption` | rows 0, 1, 9; row 5 shown but not fitted | unsourced (grade D, a stated gap), a projection, and an emergency |
| `H_espionage_cases` | rows 1, 3, 6, 7, 8, 9, 15, 17, 18, 19, 20 | a second source for SolarWinds; Salt Typhoon (dwell only at second hand, "1-2" years); Flame (grade C, figures read from an encyclopaedia page); UNC3886, Duqu 2.0, Turla and APT10 (no dwell time stated; APT10's discovery date is from memory); the 2025 M-Trends benchmark; three "contrast" rows about AI agents, which are not espionage |
| `E_stage_judgements` | row 8 | text summary |
| `E_incident_timelines`, `E_laundering`, `I_business_models` | all | context: no script reads them |

## What is not here

The research behind the post also produced tables that back only sentences in its text, such as a country-level talent-risk ranking, education and motive tables, timelines of wartime cyber operations and worms, and a price list for access to networks. No figure depends on them, so they are not in this repository, and **the numbers in the post that came from them cannot be reproduced from here**; the post cites the sources for its text itself. A provisional draft of one figure was also left out.

## The two lists of sources

- [`extra_sources.csv`](extra_sources.csv) is written by hand. It lists documents that numbers were *typed* from (so they appear in no table's `source_url`), and documents that a notes column mentions without a link. Columns: `chart`, `publisher`, `title`, `url`, `pub_date`, `supports` (what was taken) and `where_used` (the script and variable).
- [`sources.csv`](sources.csv) is generated. It merges every table's source columns, the links written inside notes columns and `extra_sources.csv` into one row per chart and document. Columns are explained in the [bibliography](../docs/BIBLIOGRAPHY.md#reading-a-row-of-datasourcescsv). Run `python tools/build_bibliography.py` after editing a table; `make verify` fails if it is out of date.

## Changing the data

Edit a row, then `make figures` (or run one chart script, for example `python charts/c07_pay.py`) and `make verify`. The check will say if a number typed into a script no longer matches the table, and which published numbers moved. Chart 1 refits a model that takes about ten seconds, Charts 6 and 8 take a minute or so each and Chart 10 about fifteen seconds; the others take a few seconds.

If you find an error in a row, open an issue with the row number, the table and a link to the correct page.
