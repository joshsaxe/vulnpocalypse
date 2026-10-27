# Parameters, judgements and typed numbers

Almost every number behind the figures is read from `data/` or computed from it. This page lists the rest: the numbers the author supplied as **judgements**, and the numbers **typed into a script** from a table's notes column or from an outside source. They are what a sceptical reader should look at first, because no table settles them.

| Kind | Where it lives | How it is checked |
|---|---|---|
| Read from `data/` | the chart and model scripts load the tables | `tools/verify_numbers.py` compares every output with the stored reference |
| Typed into a script, with a source | named constants in `charts/` and `models/` | `tools/check_inputs.py` finds each one and says whether the table agrees (the table at the end of this page) |
| Judgement | priors, assumptions and expert ranges, named constants in `charts/` and `models/` | not checkable against data; listed below with the range tried and the check that varies it |

## Start here: the choices that move the answers most

1. **Chart 1's AI share is a judgement informed by evidence, not a measurement.** The central estimate averages three sets of "but-for" assumptions (central, sceptical, generous) about how much of the AI-mentioning losses would not have happened without AI. The loss data cannot show an effect of a few per cent, so the model also runs a trend test: refitted on data to 2022 and projected forward, losses in 2023-25 sit *below* that projection with probability 0.84 for fraud and 0.74 for hacking. The first table below lists each assumption.
2. **Chart 1's levels come from an earlier study.** Published loss series are floors, because most victims never report. The 2025 level (fraud $220bn, 90% interval 105-461; hacking $76bn, 31-188; America about 42% of fraud) comes from the author's earlier triangulation and is typed into the script. The data tables say how losses changed, not how big they are.
3. **Growth after 2022 is lower than before in every variant for hacking, but for fraud the slowdown depends on one assumption; the exact rates always do.** With no common drift, double drift and tighter or looser idiosyncratic drift, fraud losses grew by 11-17% a year in 2017-22 and by 8-11% a year in 2022-25 (medians; the post's methods appendix quotes 12-17% for the first period, taking the lower end on means, 11.6, rather than medians, 11.1). Hacking losses grew by 22-25%, then 9-11%: a fall of at least ten points a year in every variant. For fraud the fall is 4 to 9 points in four variants but almost nothing (11.1%, then 10.7%) when each series may drift by a point a year relative to the others ([model card](MODELS.md#chart-1-the-trend)). Dropping the two indicators that count incidents rather than dollars leaves hacking losses roughly flat since 2022 (3% a year). `sensitivity/s01_loss_trend.py`.
4. **Chart 4's stage shares are judgements.** No public data measure a ransomware gang's hours by stage. The ranges are in `data/E_stage_judgements.csv`, with the reasoning in its `reasoning` column; the hand-over share (10-80%), speed-up (3-20x) and checking time (10-40% of doing the work by hand) are stated in the chart's note.
5. **Chart 6 depends on how two rows are dated.** The tool-path line in Chart 10 (the chance agents are widespread by 2030 if they are a "new tool") rests on the Mirai botnet's lag being counted from the era of cheap insecure gadgets (about 2014; 2.3 years) rather than from the code's first sighting (the table's 0.1 years). With the table's value the tool-class median lag falls from 3.9 to 2.5 years and that chance falls from 55% to 34%. Dating the AI-written-phishing lag by calendar year (1.6 years, not the table's 2.5) lowers it to 51%. The business-model line is steadier (35% in the chart; 21% under the original classification, which counted deepfake-voice fraud as a business model and double extortion as a tool; 41% if encrypt-and-ransom is dated from its first criminal use in 2006). `sensitivity/s06_adoption_lags.py`.
6. **Chart 8's agency lags rest on estimated years.** Dating open source's arrival in US agencies from the Pentagon's October 2009 memo (2009-11) instead of 2012-14 removes the downward trend from the fit without generative AI (the chance the lag is shrinking falls from 79% to 45%) and lowers the chance that agencies use AI agents routinely by the end of 2029 from 72% to 55% (median mid-2029, not 2028). `sensitivity/s08_open_source_dating.py`.
7. **Chart 7's Israeli state figures are averages for all army, Mossad and Shin Bet staff, not engineers.** Against Mossad and Shin Bet alone the private-to-state ratio is 1.7 (80% range 0.8-3.6), not 2.6. `sensitivity/s07_israel_state_pay.py`.
8. **Chart 11's spending panel is an order-of-magnitude judgement.** Defensive medians are anchored on two market-research houses; offensive medians are a deliberately generous guess. They are not measurements.
9. **A few chart-5 durations are approximate or assumed.** The table gives one bound (or none) for some cases and the author supplied the other; one duration (263 days) rounds a table figure of about 252. See the `ASSUMED` and `APPROX` lines in the table at the end.
10. **Charts 2, 5 and 9 can count only what was caught, and no table says how much is missing.** Police stop being the majority in Chart 2 if police endings are about 2.9 times as likely as other closures to be documented (at least 64 other closures missing); "about two-thirds" goes at about 1.4. In Chart 5 two hidden quick catches would make most cut-offs quick, and five hidden long cases would make long ones twice as common as quick ones; which of the nine cases are kept moves its shares by 17 to 24 points. In Chart 9 hidden campaigns can only add long cases, so the claim that state hackers can stay hidden for years depends on the few long ones that are plotted. The data cannot estimate any of these; `sensitivity/s02_police_selection.py`, `sensitivity/s05_provider_selection.py` and `sensitivity/s09_state_selection.py` give the thresholds, and the model cards tabulate them.
11. **Price indices for countries other than the United States are hand-entered.** See "Hand-entered deflators" below.

## Judgement parameters, by chart

Ranges in brackets are 80% ranges unless said otherwise. "Where" gives the file; every value is a named constant near the top of the script.

### Chart 1: `models/c01_loss_trend.py`

| Parameter | Value | What it does |
|---|---|---|
| 2025 fraud loss level | log-normal, median $220bn, 90% interval 105-461 | scales the trend to dollars (from the earlier study) |
| 2025 hacking loss level | log-normal, median $76bn, 90% interval 31-188 | same |
| America's share of 2025 fraud | mean 0.42, 10th percentile 0.32 | splits fraud between the American and the rest-of-world trend |
| Common reporting drift subtracted | America 2% a year (sd 2 points), other countries 1% (sd 1.5), hacking 1% (sd 2) | if more victims report each year everywhere, every series rises faster than true losses; varied in `s01` (zero, doubled) |
| Idiosyncratic drift | each series may drift 3 points a year relative to the others | varied in `s01` (1 and 6 points) |
| Noticed AI share | fraud 4.2% [2.5-7%], hacking 1.4% [0.7-2.8%] of dollars | the dollars in FBI IC3 complaints that mention AI (`A1_fraud_ai_evidence.csv`) |
| But-for share of noticed AI losses | central 25% [8-55%]; sceptical 10% [3-25%]; generous 50% [25-75%] | how much would not have happened without AI; the three sets are averaged with equal weight |
| Unnoticed AI share | fraud 10% [4-25%], hacking 20% [10-35%] (generous: 15% and 30%) | AI used but invisible to victims; Verizon's 10% of malicious e-mail and IBM's 16-25% of breaches |
| But-for share of unnoticed losses | fraud 8% [2-25%], hacking 3% [1-10%] (sceptical 3% and 1%; generous 15% and 8%) | phishing's success did not rise as AI text spread |
| AI adoption relative to 2025 | 2023 about 0.25 [0.10-0.45], 2024 about 0.50 [0.30-0.70]; 2026 log-normal around 1.4 (90% interval 1.0-2.0) | scales the 2025 share to earlier years and to the 2026 projection |

### Chart 2: `charts/c02_police.py`, `common/lifespans.py`

Uniform Beta(1,1) priors on each sector's police share, binomial likelihood. Which end types count as "police" (takedown, seizure, arrests or sanctions, plus shutdowns the operators or reporting tied to police pressure) is the author's classification in `data/B_enterprise_lifespans.csv` (`end_type`). A Bayesian bootstrap gives the intervals on the Aalen-Johansen estimate. The robustness check `sensitivity/s02_police_selection.py` varies one documentation gap `R` (how many times more likely a police ending is to be documented than another closure) over a fixed grid, 1 to 10; no value is preferred and the data cannot estimate it. Its "strict" reading counts only arrests, takedowns and seizures as police endings, and one variant counts police endings that share an end date (coordinated takedowns) once. It treats a row as one enterprise, as the chart does.

### Chart 4: `charts/c04_amdahl.py`

Stage shares of hours and AI-doable shares (low, central, high) are in `data/E_stage_judgements.csv`. Hour shares are Dirichlet around the central values with a concentration chosen so the 80% ranges match the stated widths; AI shares are Beta distributions fitted to each stage's low, central and high. Hand-over share d: 10-80%; AI speed-up k: 3-20x; checking time v: 10-40% of doing the work by hand. 40,000 draws.

### Chart 5: `charts/c05_inference.py`

Each case's duration is log-uniform between its bounds; where the report gives one bound the author assumes the other (`ASSUMED` in the table below). Uniform Beta(1,1) prior on the population shares. The nine "cut off" and six "not cut off" cases are listed in the script (`CAUGHT`, `NOTCUT`). The robustness check `sensitivity/s05_provider_selection.py` adds three judgement lists. `CUT` is the 35 distinct hacking, fraud and spying operations in `D_platform_cases` that an AI provider cut off (36 rows; two of them are one joint report by OpenAI and Microsoft), by provider: the nine the chart uses, one with a stated duration that the chart leaves out (a ban at sign-up) and 25 with none (borderline rows, such as a disruption of a planned exploit or the suspension of consumer e-mail accounts, are left out). `EXCLUDED_QUICK` and `EXCLUDED_LONG` are the four cut-offs with a stated duration that Chart 5 leaves out (two influence operations, a model-copying campaign and the ban at sign-up). `WINDOWS` and `NOT_ANTHROPIC` are two groups of three of the nine, dropped in turn to show how much the shares depend on them: the three whose short "duration" is a reporting window, a stretch of network activity or one stolen key's use, and the three long cases that are not Anthropic's. The readings it tests (most, twice as common, a quarter, a fifth) are round-number thresholds, not estimates.

### Chart 6: `charts/c06_attacker_lag.py`

| Parameter | Value | Note |
|---|---|---|
| Class of each technique | exploit, tool or business model (the script's `SCALED` and `OPEN` dictionaries) | assigned by the author, knowing the outcomes; an earlier version had one "drop-in" class |
| Priors | mu ~ N(log 1 year, 2); sigma ~ HalfNormal(1.5) | |
| Mirai lag | 2.3 years, from mid-2014 (cheap insecure gadgets) | the table says 0.1 from first sighting; `OVERRIDE` below; varied in `s06` |
| Not-yet-scaled cases | right-censored at the time elapsed to October 2026 | criminal chatbots, AI-generated malware (tool class); AI agents running intrusions (business-model class) |
| Agents' start | 24 February 2025 (first coding agents) | typed from `data/I_adoption_lags.csv` row 15 |

### Chart 7: `charts/c07_pay.py`

Source-quality standard deviations on log pay: grade A 0.15, B 0.25, C 0.40, D 0.60; role-mismatch 0.25; an advertised range's half-width is taken as 1.28 standard deviations (an 80% interval). Prior: log-normal centred on $80,000 with sd 10 in log units (essentially flat). Which rows count on each side is the script's `USE` dictionary (verified against the table below).

### Chart 8: `charts/c08_govlag.py`

Priors a ~ N(log 5, 1), b ~ N(0, 0.1), s ~ HalfNormal(0.7); adaptive Metropolis, four chains of 30,000 iterations with the first 8,000 discarded, thinned by 5. "Now" is 2026.8 (late October 2026). The projection draws business adoption of AI agents uniformly in 2025-26. The Covid-era video-conferencing row is shown but not fitted; the two grade-D rows are excluded. Fitted twice, with and without the generative-AI row.

### Chart 9: `sensitivity/s09_state_selection.py`

Chart 9 has no parameters: every bar is a reported date or count. The robustness check types four counts from the notes columns of `H_espionage_cases` (SolarWinds: about 109 organisations worked, of 18,000, or 17,000 on SolarWinds' own figure, that installed the update; Equation Group: more than 500 victims seen, of "tens of thousands" infected, read as 20,000 or, loosely, 10,000) and stops if the table's text does not contain them. Salt Typhoon's "1-2" years is read as 1.5. A second part of the check recomputes each plotted duration from the table's own start and discovery dates, placing a date given only as a month or a year at the middle of it (the 15th of the month; 1 July). A separate figure, how long Regin ran before Kaspersky knew of it, reads "spring 2012" as 15 April 2012; the script stops if the table's text no longer says "spring 2012".

### Chart 10: `charts/c10_odds.py`

Combines the posterior draws of Charts 6 and 8. "Now" is 2026.8. The agency line mixes the two fits (all rows; without generative AI) with equal weight.

### Chart 11: `charts/c11_defenders.py`

| Parameter | Value |
|---|---|
| Chance a vendor's feature counts as substantive | by feature grade: A 1.0, B 0.95, C 0.60, none 0 |
| Date uncertainty | date confidence A: that year; B: that year with probability 0.8, else plus or minus 1; C: that year with probability 0.5, plus or minus 1 with 0.2 each, plus or minus 2 with 0.05 each |
| Defensive spend, median $bn, 2022-26 | 8.0, 10.5, 13.5, 16.4, 20.3 (log-sd 0.42), anchored on Mordor Intelligence and Precedence Research |
| Offensive spend, median $m, 2022-26 | 0.3, 2.0, 6.0, 12.0, 22.0 (log-sd 0.85), a deliberately generous guess |

### Chart 12: `charts/c12_funnel.py`

Uniform Beta(1,1) prior on the chance an AI-found flaw is exploited; 14 of 1,061 observed gives Beta(15, 1048).

## Hand-entered deflators

`common/deflators.py` puts every loss series in 2025 prices. For the United States it reads the BLS CPI-U annual averages in `data/cpi_u.csv` (plus a 2004 value, 188.9, typed in). For the other jurisdictions it holds annual-average consumer-price inflation, in per cent, typed in by hand and rounded to 0.1 point: Britain, Australia, Japan, Canada, Singapore, Hong Kong and the euro area, for 2005-2025. The docstring names the sources (national statistics offices as compiled in the IMF's World Economic Outlook database). These values have no source link in `data/` and were not re-checked line by line against the agencies' series for this repository; spot checks of recent years look right. An error of a point or two in a price level is small next to the noise in the loss series themselves (typically 15-40% a year).

## Typed numbers, checked

`python tools/check_inputs.py` finds every number typed into a chart script and says what kind it is:

| Status | Meaning |
|---|---|
| MATCH | the typed number equals the number in the data table |
| DERIVED | it follows from the table by arithmetic the script redoes |
| APPROX | a rounding of a table figure, within a stated tolerance |
| ASSUMED | the table gives one bound (or none) and the author supplied the rest; the data bound is shown |
| OVERRIDE | deliberately different from the table, for the reason given |
| NOTE | a quirk in the data worth knowing about; the chart script is not wrong |
| NOT IN DATA | typed from an outside source that is not in the tables; the source is in [`data/extra_sources.csv`](../data/extra_sources.csv) and the [bibliography](BIBLIOGRAPHY.md) |
| FAIL | the typed number contradicts the table (the script then exits with status 1) |

Row numbers are pandas row numbers (0 is the first data row); a spreadsheet shows that row as the number plus 2.

<!-- BEGIN CHECKS -->
| Chart | What is typed | Typed value | Status | Where it comes from, and what was checked |
|---|---|---|---|---|
| 0 | Cost to find a flaw, per bug: $0.22 (cheap model) to $7.80 (frontier agent) | `0.22, 7.8` | **NOT IN DATA** | CyberGym (Lu et al., 2026): $4.38 for 20 bugs, $132.65 for 17; arithmetic checked (0.219, 7.80) |
| 0 | Cost to break into an AI lab's code repository | `3,000` | **NOT IN DATA** | Hacktron write-up: 'less than $3,000 in tokens' |
| 0 | Cost of a browser exploit chain | `40,000` | **NOT IN DATA** | XBOW: about $40,000 in API fees for six days |
| 1 | Chainalysis crypto-scam revenue 2021, $bn | `10.9` | MATCH | A1_fraud_series V2023 2021 = 10.9 |
| 1 | Chainalysis crypto-scam revenue 2022, $bn | `5.9` | MATCH | A1_fraud_series V2023 2022 = 5.9 |
| 1 | Chainalysis crypto-scam revenue 2024, $bn | `12.0` | MATCH | A1_fraud_series V2026 2024 = 12.0 |
| 1 | Chainalysis crypto-scam revenue 2025, $bn | `17.0` | MATCH | A1_fraud_series V2026_PROJ 2025 = 17.0 |
| 1 | Chainalysis ransomware payments 2025, $bn | `0.90` | **OVERRIDE** | table: $0.82bn (published floor); override to $0.90bn because Chainalysis says it expects 2025 'to approach or exceed $900 million' once attribution catches up (same row's notes) |
| 1 | FinCEN ransomware payments 2023, $bn | `1.1` | MATCH | A2_hacking_series FINCEN_RANSOMWARE_PAYMENTS 2023 = 1.1 |
| 1 | FinCEN ransomware payments 2024, $bn | `0.734` | MATCH | A2_hacking_series FINCEN_RANSOMWARE_PAYMENTS 2024 = 0.734 |
| 1 | FinCEN ransomware payments 2022, $bn | `0.62` | **DERIVED** | FinCEN gives 2023 = $1.1bn, up 77% on 2022, which implies 1.1/1.77 = $0.62bn; the row's notes say this figure is 'derived, not published' |
| 1 | Share of fraud dollars in IC3 complaints that mention AI (the 'noticed' share), central value | `0.042` | **APPROX** | A1_fraud_ai_evidence: $893.3m of $20.877bn = 0.0428 of all IC3 losses (the 2025 report); range 2.5-7% is a judgement |
| 1 | Share of hacking-type dollars in IC3 complaints that mention AI, central value | `0.014` | **APPROX** | A1_fraud_ai_evidence: $6,277,887 of AI-referencing losses over the hacking-type categories' dollars = 1.3% (data breach, malware, botnet, SIM swap) to 1.4% (data breach and malware only); range 0.7-2.8% is a judgement |
| 1 | Share of malicious e-mail with AI-written text, used for 'unnoticed' AI in fraud (mean) | `0.10` | MATCH | A2_hacking_ai_evidence (Verizon DBIR 2025): 0.1 |
| 1 | Share of breaches in which attackers used AI, used for 'unnoticed' AI in hacking (mean) | `0.20` | **APPROX** | A2_hacking_ai_evidence (IBM): 16% (2025 edition) and 25% (2026 edition); their midpoint is 0.205 |
| 1 | Total level of 2025 fraud losses: lognormal(median $220bn, 90% interval 105-461) | `220, 105, 461` | **NOT IN DATA** | the author's earlier triangulation (docs/PARAMETERS.md); no table in data/ |
| 1 | Total level of 2025 hacking losses: lognormal(median $76bn, 90% interval 31-188) | `76, 31, 188` | **NOT IN DATA** | the author's earlier triangulation (docs/PARAMETERS.md); no table in data/ |
| 1 | America's share of 2025 fraud losses: mean 0.42, 10th percentile 0.32 | `0.42, 0.32` | **NOT IN DATA** | the author's earlier triangulation (docs/PARAMETERS.md); no table in data/ |
| 1 | Common reporting drift subtracted: America 0.02+/-0.02, elsewhere 0.01+/-0.015, hacking 0.01+/-0.02 a year | `see models/c01_loss_trend.py` | **ASSUMED** | judgement; sensitivity/s01_loss_trend.py halves and doubles it |
| 1 | AI adoption vs 2025: 2023 about 0.25, 2024 about 0.5; 2026 lognormal(1.4, 90% interval 1.0-2.0) | `0.25, 0.5, 1.4` | **ASSUMED** | judgement |
| 1 | But-for fractions (central 25%, sceptical 10%, generous 50% of noticed AI losses) and unnoticed shares | `see model` | **ASSUMED** | judgements; the model averages the three sets with equal weight |
| 1 | Number of loss series pooled | `23 (in the chart's source line)` | MATCH | results/c01_loss_trend.json n_series = 23 |
| 2 | 'All 152' (row label) | `152` | MATCH | B_enterprise_lifespans.csv has 152 rows; 115 have dates and enter the competing-risks estimate |
| 3 | Conti staff (mostly low-level malware coders and testers), t | `$12,000-24,000` | MATCH | C_pay.csv row 0: $12,000-$24,000 |
| 3 | Dark-web IT job ads: developer (median) | `$24,000` | MATCH | C_pay.csv row 2: $24,000-$24,000 |
| 3 | Dark-web IT job ads: reverse engineer (median) | `$48,000` | MATCH | C_pay.csv row 4: $48,000-$48,000 |
| 3 | LockBit developer (Rostislav Panev, alleged), payments from  | `$120,000` | MATCH | C_pay.csv row 8: $120,000-$120,000 |
| 3 | Median total pay, US software engineers, 2025 | `195,000` | MATCH | C_pay.csv row 22: $195,000 |
| 3 | AI engineers' total pay, 2026 | `250,000` | MATCH | C_pay.csv row 23: $250,000 |
| 3 | OpenAI or Anthropic, 2026 | `878,750` | **DERIVED** | mean of the two medians in F_pay.csv rows 14 and 15: ($875,000 + $882,500) / 2 |
| 3 | Band: median pay in dark-web job ads by role, $1,300-4,000 a month | `15,600-48,000 a year` | MATCH | C_pay.csv rows 2-5: lowest role median $15,600 (designer), highest $48,000 (reverse engineer) |
| 3 | Russian developers' take-home pay by level, H1 2021 (roubles a month: 52,000 / 120,000 / 195,000 / 230,000) | `52,000 ... 230,000` | **NOT IN DATA** | Habr Career, first half of 2021 (bibliography) |
| 3 | Roubles per dollar, 2021 average | `73.65` | **NOT IN DATA** | World Bank (bibliography) |
| 4 | Eight stages; the central hour shares sum to 100% | `8 stages, 1.00` | MATCH | E_stage_judgements.csv: 8 stages, shares sum to 1.00 |
| 4 | 'Together, AI can do about 36% of the hours' (note under the bars) | `36%` | **DERIVED** | sum of share x AI-doable share over the eight stages = 0.364 |
| 4 | Hand-over share 10-80%, AI speed-up 3-20x, checking time 10-40% of doing it by hand | `10-80%, 3-20x, 10-40%` | **ASSUMED** | judgements: no public dataset measures them; stated in the chart's note |
| 5 | ANT-2026-09-GTG50020: duration, days (cut off) | `4-26` | MATCH | D_platform_cases: 4-26 days |
| 5 | ANT-2025-08-GTG2002: duration, days (cut off) | `7-30` | **ASSUMED** | D_platform_cases gives only the upper bound (30 days); the lower bound 7 is assumed |
| 5 | ANT-2025-11-GTG1002: duration, days (cut off) | `10-60` | **ASSUMED** | D_platform_cases gives 10 days (ban after detection); the upper bound 60 is assumed |
| 5 | ANT-2026-09-GTG50014: duration, days (cut off) | `21` | MATCH | D_platform_cases: 21-21 days |
| 5 | ANT-2026-09-GTG50029: duration, days (cut off) | `30-148` | MATCH | D_platform_cases: 30-148 days |
| 5 | OAI-2025-04-AKIRABOT: duration, days (cut off) | `180-225` | **DERIVED** | dates in the table: 2024-09 to 2025-04-09 is 191-220 days; the typed range rounds that outward |
| 5 | MS-2026-09-EVILTOKENS: duration, days (cut off) | `213` | MATCH | D_platform_cases: 213-213 days |
| 5 | ANT-2025-08-GTG5004: duration, days (cut off) | `180-225` | **DERIVED** | dates in the table: 2025-01-17 to 2025-08-27 is 222-222 days; the typed range rounds that outward |
| 5 | SVC-XANTHOROX: duration, days (cut off) | `290-315` | **DERIVED** | dates in the table: 2025-04 to 2026-02-12 is 288-317 days; the typed range rounds that outward |
| 5 | CS-2026-10-ARTEX: duration, days (not cut off) | `7-21` | MATCH | D_platform_cases: 7-21 days |
| 5 | AWS-2026-02-FORTIGATE: duration, days (not cut off) | `38` | MATCH | D_platform_cases: 38-38 days |
| 5 | SVC-WORMGPT: duration, days (not cut off) | `62-188` | MATCH | D_platform_cases: 62-188 days |
| 5 | ANT-2025-08-VIETNAM: duration, days (not cut off) | `270` | MATCH | D_platform_cases: 270-270 days |
| 5 | ANT-2026-09-GTG50027: duration, days (not cut off) | `263` | **APPROX** | row: system built Jan-Jul 2026, account banned in July, still running on local models at the report (10 Sep 2026 = 252 days after 1 Jan); 263 days is within 5% of that, invisible on a log axis |
| 5 | SVC-GHOSTGPT: duration, days (not cut off) | `610` | **DERIVED** | first documented 23 Jan 2025 (Abnormal; the row's pub_date), still sold in Sep 2026: 586-615 days |
| 5 | Of the nine cut off: 'three or four within a month' and 'four lasted six months or more' (note) | `3-4, 4` | **DERIVED** | counts from the nine ranges: 3 end by day 30 (a fourth, 30-148, starts at day 30), 4 start at day 180 or later |
| 6 | Mirai botnets: lag from cheap insecure gadgets (about 2014) to widespread use | `2.3` | **OVERRIDE** | table lag is 0.1 years (from the Mirai code's first sighting, Aug 2016); the chart counts from mid-2014 to Oct 2016 = 2.3; sensitivity/s06_adoption_lags.py shows the alternative |
| 6 | WormGPT start: June 2023 | `2023.417` | MATCH | I_adoption_lags availability_date 2023-06 = 2023.417 |
| 6 | AI-malware start: 30 Nov 2022 | `2022.914` | MATCH | I_adoption_lags availability_date 2022-11-30 = 2022.914 |
| 6 | Agentic intrusion start: 24 Feb 2025 | `2025.150` | MATCH | I_adoption_lags availability_date 2025-02-24 = 2025.147 |
| 6 | LLM-written phishing/BEC text: lag in the table vs lag implied by its dates | `2.5` | **NOTE** | table says 2.5 years; its availability and 'scaled' years imply 1.6. The table counts to the 2025 Verizon report that found about 10% of malicious e-mail had AI text. Used as given; sensitivity/s06_adoption_lags.py shows the effect of the other reading |
| 7 | United States: rows used on each side | `{state: [0, 1, 7], private: [11], frontier: [14, 15]}` | MATCH | F_pay.csv: state rows are national_security, private rows are the country's Levels.fyi ML/AI engineer median, frontier rows OpenAI and Anthropic |
| 7 | United Kingdom: rows used on each side | `{state: [17, 18, 19, 20, 21, 22], private: [24]}` | MATCH | F_pay.csv: state rows are national_security, private rows are the country's Levels.fyi ML/AI engineer median, frontier rows OpenAI and Anthropic |
| 7 | Israel: rows used on each side | `{state: [32, 33, 34, 35], private: [39]}` | MATCH | F_pay.csv: state rows are national_security, private rows are the country's Levels.fyi ML/AI engineer median, frontier rows OpenAI and Anthropic |
| 7 | China: rows used on each side | `{state: [41], private: [42]}` | MATCH | F_pay.csv: state rows are national_security, private rows are the country's Levels.fyi ML/AI engineer median, frontier rows OpenAI and Anthropic |
| 7 | Measurement-model settings: grade sd A .15 / B .25 / C .40 / D .60, role-mismatch sd .25, prior N(log 80,000, 10) | `see chart` | **ASSUMED** | judgements; Chart 7's docstring explains them |
| 8 | The seven technologies fitted or shown | `7 names` | MATCH | all seven appear in G_adoption.csv; the two grade-D rows (PCs, corporate e-mail and web) are left out |
| 8 | Priors a ~ N(log 5, 1), b ~ N(0, 0.1), s ~ HalfNormal(0.7); NOW = 2026.8 | `see chart` | **ASSUMED** | judgements |
| 9 | SolarWinds: bar label | `15 months` | MATCH | H_espionage_cases years_undetected 1.27 = 15.2 months |
| 9 | BRICKSTORM: bar label | `13 months` | MATCH | H_espionage_cases years_undetected 1.08 = 13.0 months |
| 9 | OPM breach: bar label | `11 months` | MATCH | H_espionage_cases years_undetected 0.9 = 10.8 months |
| 9 | Midnight Blizzard: bar label | `7 weeks` | MATCH | H_espionage_cases years_undetected 0.13 = 6.8 weeks |
| 9 | Ivanti zero-days: bar label | `5 weeks` | MATCH | H_espionage_cases years_undetected 0.1 = 5.2 weeks |
| 9 | Storm-0558: bar label | `1 month` | MATCH | H_espionage_cases years_undetected 0.09 = 1.1 month |
| 9 | Equation Group: bar label | `14 years` | MATCH | H_espionage_cases years_undetected = 14 |
| 9 | Regin: bar label | `11 years` | MATCH | H_espionage_cases years_undetected = 11 |
| 9 | Volt Typhoon: 5+ years (a lower bound, hollow marker) | `5.0` | MATCH | H_espionage_cases: 5; notes: 'at least five years' (CISA) |
| 9 | Typical spying case: 122 days | `122/365` | MATCH | H_espionage_cases (Mandiant M-Trends 2026 row): 0.33 years; notes: 'the median dwell time for both categories was 122 days' |
| 9 | Typical intruder: 14 days | `14/365` | MATCH | E_stage_times.csv: Global median dwell time = 14.0 days (2025) |
| 9 | Equation Group annotation '500+ victims among tens of thousands infected' | `500, tens of thousands` | MATCH | H_espionage_cases victims columns |
| 9 | Regin annotation '27 victims in 14 countries' | `27, 14` | MATCH | H_espionage_cases victims_targeted |
| 9 | SolarWinds annotation 'about 110 of 18,000 infected were exploited' | `110 of 18,000` | **DERIVED** | about 100 companies + 9 agencies = about 109 (Neuberger, 2021) of about 18,000 that downloaded the update |
| 10 | 'Now' is 2026.8 in charts/c06_attacker_lag.py | `2026.8` | MATCH | late October 2026, when the data were compiled |
| 10 | 'Now' is 2026.8 in charts/c08_govlag.py | `2026.8` | MATCH | late October 2026, when the data were compiled |
| 10 | 'Now' is 2026.8 in charts/c10_odds.py | `2026.8` | MATCH | late October 2026, when the data were compiled |
| 11 | 34 vendors tracked | `34 (in the chart's text)` | MATCH | G_vendor_ai.csv has 34 rows |
| 11 | Probability a feature counts: A 1.0, B 0.95, C 0.60, none 0; date confidence A/B/C offsets | `see chart` | **ASSUMED** | judgements; every grade in G_vendor_ai.csv is covered by the script's lookup |
| 11 | Defensive spend medians $bn 2022-26: 8.0, 10.5, 13.5, 16.4, 20.3 (log-sd 0.42) | `8.0 ... 20.3` | **ASSUMED** | judgement anchored on two market-research houses' figures for 2025-26 (about $16bn and $20bn); not in data/ |
| 11 | Offensive spend medians $m 2022-26: 0.3, 2.0, 6.0, 12.0, 22.0 (log-sd 0.85) | `0.3 ... 22.0` | **ASSUMED** | a deliberately generous guess at what attackers spend; not in data/ |
| 11 | Market-research anchors: Mordor Intelligence $16.44bn (2025) and $20.58bn (2026); Precedence Research $19.45bn (2026) | `see docstring` | **NOT IN DATA** | G_vendor_ai_sources.md and the bibliography list the pages |
| 12 | Funnel: 6,157 reported; 516 patched | `6157, 516` | MATCH | J_ai_vulns.csv value column |
| 12 | Funnel: 29,439 flagged; 5,103 acknowledged | `29439, 5103` | MATCH | J_ai_vulns.csv notes of the 6,157 row ('29439 candidates; ... 5103 acknowledged') |
| 12 | 14 exploited of 1,061 AI-found flaws tracked | `14, 1061` | MATCH | J_ai_vulns.csv value column |
| 12 | All-flaws benchmark: about 1.4% | `1.4%` | MATCH | J_ai_vulns.csv notes of the 14 row |
| 12 | 'Nine in ten reports checked by outsiders proved real' (note) | `90%` | **DERIVED** | notes of the 6,157 row: 5,674 of 6,123 externally reviewed confirmed valid = 92.7% |
| 12 | 'Only one in 12 ... has been patched' (title) | `1 in 12` | **DERIVED** | 6,157 / 516 = 11.9 |
<!-- END CHECKS -->
