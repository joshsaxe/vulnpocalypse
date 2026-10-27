# Figures

The thirteen figures of the post: the lede figure and Charts 1 to 12. Each is drawn by one script in [`charts/`](../charts) from tables in [`data/`](../data) (or from a model's saved output) and is saved twice: a **PNG** (250 dpi, 1,625 pixels wide) for reading and an **SVG** (text kept as text, so it can be edited) for reuse. Next to each figure, a JSON file in [`results/`](../results) records the numbers the script computed and drew.

This page is the guide to the plots: what each one shows, how to read its marks, the numbers on it, and where to find the code, the data, the model card and the sources. For the models see [MODELS](../docs/MODELS.md); for the data see the [data dictionary](../data/README.md); for the documents behind the data see the [bibliography](../docs/BIBLIOGRAPHY.md).

## Contents

| Figure | The finding, as the chart's title puts it | Script |
|---|---|---|
| [Lede](#lede-the-price-of-a-hack) | If breaking in and finding flaws are this cheap, where are the attacks? | [`c00_lede_cost.py`](../charts/c00_lede_cost.py) |
| [1](#chart-1-losses-to-fraud-and-hacking-and-the-part-caused-by-ai) | AI probably caused less than 5% of the $300bn lost to cybercrime in 2025 | [`c01_losses.py`](../charts/c01_losses.py) |
| [2](#chart-2-what-happens-to-criminal-enterprises) | Police ended most criminal services that closed, but not most ransomware brands or darknet markets | [`c02_police.py`](../charts/c02_police.py) |
| [3](#chart-3-what-crime-pays) | Criminal coders earn about what honest ones do in emerging economies, a tenth of what American AI engineers make | [`c03_talent.py`](../charts/c03_talent.py) |
| [4](#chart-4-amdahls-law-for-a-ransomware-gang) | AI can do two-fifths of a ransomware gang's hours, but lifts its output per hour only about a tenth | [`c04_amdahl.py`](../charts/c04_amdahl.py) |
| [5](#chart-5-how-long-abusers-keep-access-to-hosted-ai) | AI firms cut some abusers off within weeks, but as many run for half a year | [`c05_inference.py`](../charts/c05_inference.py) |
| [6](#chart-6-how-fast-criminals-adopt-new-technology) | Crooks use ready-made exploits within weeks, but take years to adopt new tools and business models | [`c06_attacker_lag.py`](../charts/c06_attacker_lag.py) |
| [7](#chart-7-public-versus-private-pay) | Private firms pay AI engineers about two to three times what Western agencies do | [`c07_pay.py`](../charts/c07_pay.py) |
| [8](#chart-8-how-far-governments-lag-business) | US security agencies adopted chatbots within two years, against four to nine before | [`c08_govlag.py`](../charts/c08_govlag.py) |
| [9](#chart-9-how-long-state-hackers-stay-hidden) | State hackers can stay hidden for years and use only a sliver of their access | [`c09_state_patience.py`](../charts/c09_state_patience.py) |
| [10](#chart-10-the-odds-year-by-year-that-ai-agents-become-routine) | By the end of 2029, AI agents are probably routine in American cyber operations, and may be in crime too | [`c10_odds.py`](../charts/c10_odds.py) |
| [11](#chart-11-the-defenders-build-up) | Defenders embraced AI fast; attackers have barely begun | [`c11_defenders.py`](../charts/c11_defenders.py) |
| [12](#chart-12-ai-found-flaws) | Only one in 12 flaws that AI found and reported has been patched so far | [`c12_funnel.py`](../charts/c12_funnel.py) |

## How to read any chart here

* **Median and 80% range.** Wherever a figure shows an estimate with a shaded band, a pale bar or a whisker, the line or dot is the posterior median and the band, bar or whisker is the 80% credible interval (the 10th to the 90th percentile). The "common idea" of the models is explained in plain language in [METHODS](../docs/METHODS.md#the-common-idea).
* **Three looks for model uncertainty, and no others.** A *shaded band* on time series, a *light, thick, square-ended bar behind a dot* on dot plots, and a *thin dark whisker* on bar charts. A *hairline with end ticks* is something else: a range reported in the data, not model uncertainty.
* **Hollow markers mean "so far" or "projected".** A hollow dot with an arrow is an operation or technology that is still running or not yet widespread; a hollow dot on a curve is a projected value.
* **Every figure says what it cannot show.** The grey note under each plot gives the caveat that matters most for that chart (for example "only cases caught and disclosed appear" on Chart 5). Those notes are repeated under each figure below.

## Lede: the price of a hack

![Dot plot on a log dollar scale of three automated hacking jobs: finding a software flaw costs 20 cents to $8, breaking into a top AI lab under $3,000, building a browser exploit chain about $40,000](c00_lede_cost.png)

* **Plots.** What AI charged, in tokens converted to dollars, for three automated jobs.
* **Marks.** Each is one documented public case, not a market average. The line for finding a flaw runs from a cheap open model ($0.22 a bug) to a frontier one ($7.80 a bug) in the same academic test (CyberGym).
* **Numbers.** [`results/c00_lede_cost.json`](../results/c00_lede_cost.json): $0.22 to $7.80 per flaw; "less than $3,000" to break into an AI lab's internal code; "about $40,000" for a full-chain browser exploit.
* **Read with care.** Only the automated part of each job is priced; much of a real attack is still done by hand (the later charts are about that).
* **Built from.** [`charts/c00_lede_cost.py`](../charts/c00_lede_cost.py). There is no data table: the costs are typed into the script and listed in [PARAMETERS](../docs/PARAMETERS.md); `tools/check_inputs.py` redoes the CyberGym division ($4.38 for 20 bugs, $132.65 for 17).
* **More.** [Model card](../docs/MODELS.md#lede-the-price-of-a-hack) · [methods](../docs/METHODS.md#lede-figure-the-price-of-a-hack) · [3 sources](../docs/sources/c00_lede_cost.md)

## Chart 1: losses to fraud and hacking, and the part caused by AI

![Stacked columns of estimated global losses to fraud and hacking from 2015 to 2025 with a 2026 projection, with the small part caused by AI in amber, and a grid of 296 squares for 2025 of which five are amber](c01_losses.png)

* **Plots.** Left: estimated global losses to fraud (blue) and hacking (red), 2015 to 2025, in billions of dollars at 2025 prices, with a one-year projection for 2026 (pale, dashed outline); the amber cap is the part judged to be caused by AI. Right: the 2025 total as a grid of $1bn squares, with the AI part in amber (the central estimate) and pale amber (up to the top of its 80% range).
* **Marks.** Columns are medians. Whiskers are 80% credible intervals for the total; they are wide because the overall *level* is uncertain, while the *trend* is better determined.
* **Numbers.** [`results/c01_loss_trend.json`](../results/c01_loss_trend.json). 2025: fraud $222bn (80% range $123bn to $390bn), hacking $74bn ($37bn to $155bn), total median $308bn (the title rounds to $300bn; the grid shows the $296bn sum of the two medians). AI-caused: about $5bn ($1.5bn to $15bn), or 1.6% of the total (0.5% to 4.5%); chance the share is below 5% about 93%.
* **Read with care.** The AI part is the author's estimate, not a measurement. The 2025 level of losses comes from an earlier study and is typed in (see [PARAMETERS](../docs/PARAMETERS.md)); the model's own contribution is the trend. How much the answer depends on those choices is in the [robustness checks](../docs/MODELS.md#chart-1-the-trend).
* **Built from.** [`models/c01_loss_trend.py`](../models/c01_loss_trend.py) fits the model (a dynamic factor model of 23 published loss series; it takes about ten seconds) and saves its draws; [`charts/c01_losses.py`](../charts/c01_losses.py) draws the chart from them. Data: [`A1_fraud_series`](../data/A1_fraud_series.csv), [`A2_hacking_series`](../data/A2_hacking_series.csv), [`cpi_u`](../data/cpi_u.csv), [`A1_fraud_ai_evidence`](../data/A1_fraud_ai_evidence.csv), [`A2_hacking_ai_evidence`](../data/A2_hacking_ai_evidence.csv). Robustness: [`sensitivity/s01_loss_trend.py`](../sensitivity/s01_loss_trend.py).
* **More.** [Model card](../docs/MODELS.md#chart-1-losses-to-fraud-and-hacking-and-the-part-caused-by-ai) · [methods](../docs/METHODS.md#chart-1-losses-to-fraud-and-hacking-and-the-part-caused-by-ai) · [sources](../docs/sources/c01_losses.md)

## Chart 2: what happens to criminal enterprises

![Horizontal bars showing, for six kinds of criminal enterprise and for all 152, the share of those that closed that were ended by police; 74% overall, 46% of ransomware brands and 48% of darknet markets](c02_police.png)

* **Plots.** For 152 named criminal enterprises in six sectors, how those that have closed came to an end: ended by police (purple) or quit, vanished or rebranded (grey). The right-hand column says how many of each sector have closed.
* **Marks.** Whiskers are 80% credible intervals from a beta-binomial model. "Ended by police" includes takedowns, seizures, arrests, sanctions and quitting under police pressure.
* **Numbers.** [`results/c02_police.json`](../results/c02_police.json). 132 of the 152 have closed; police ended 74% of those (69% to 79%), but only 46% of closed ransomware brands (34% to 58%) and 48% of darknet markets (37% to 60%). For the 115 enterprises with launch and end dates, the same file has the chance that police end an enterprise within two, five and ten years of its launch: about 21%, 40% and 65%.
* **Read with care.** Shares flatter the police: documented enterprises are more often the ones they caught. The robustness check says by how much: police stop being the majority if they are about 2.9 times as likely to be documented as other closures, and "about two-thirds" goes at about 1.4. For darknet markets and ransomware brands the data say "about half" rather than "less than half", and 14 of the 38 ransomware brands are still running.
* **Built from.** [`charts/c02_police.py`](../charts/c02_police.py) and [`common/lifespans.py`](../common/lifespans.py). Data: [`B_enterprise_lifespans`](../data/B_enterprise_lifespans.csv) (152 rows). Robustness: [`sensitivity/s02_police_selection.py`](../sensitivity/s02_police_selection.py).
* **More.** [Model card](../docs/MODELS.md#chart-2-what-happens-to-criminal-enterprises) · [methods](../docs/METHODS.md#chart-2-what-happens-to-criminal-enterprises) · [sources](../docs/sources/c02_police.md)

## Chart 3: what crime pays

![Dot plots of annual pay on a log scale: criminal coders and dark-web job ads, American software engineers, Russian developers by level, and developers in other emerging economies, with a shaded band for dark-web advertised pay](c03_talent.png)

* **Plots.** Annual pay in dollars on a log scale. Left: crime pay (red) and pay for US software engineers (cyan). Right: honest developers in Russia (by level, 2021) and in other emerging economies. The shaded band is the median pay offered in dark-web IT job ads, 2020 to 2022, from designers ($16k) to reverse engineers ($48k).
* **Marks.** Dots are single figures; a hairline with end ticks is a range reported in the source.
* **Numbers.** [`results/c03_talent.json`](../results/c03_talent.json). The median dark-web developer ad ($24,000) is 9.6% of the median total pay of an American AI engineer ($250,000); Conti coders $12,000 to $24,000; LockBit's alleged developer $120,000; Russian developers $8k (junior) to $37k (lead); other emerging economies $17k to $42k; US median software salary $136k.
* **Read with care.** Crime pay is salary; the few who share in ransoms earn far more. Figures are not adjusted for inflation, and some are averages rather than medians (the note says which). The Russian developer medians are typed into the script in roubles and converted at a stated rate.
* **Built from.** [`charts/c03_talent.py`](../charts/c03_talent.py). Data: [`C_pay`](../data/C_pay.csv), [`C2_dev_pay_by_country`](../data/C2_dev_pay_by_country.csv), and two rows of [`F_pay`](../data/F_pay.csv).
* **More.** [Model card](../docs/MODELS.md#chart-3-what-crime-pays) · [methods](../docs/METHODS.md#chart-3-what-crime-pays) · [sources](../docs/sources/c03_talent.md)

## Chart 4: Amdahl's law for a ransomware gang

![Left, eight stages of a ransomware attack as bars showing each stage's share of a gang's working hours and the part AI can do. Right, the most AI could add (about 60%) and what a gang should gain by the end of 2026 (about 10%, range 2 to 25%)](c04_amdahl.png)

* **Plots.** Left: the eight stages of an attack, each bar the stage's share of the working hours behind one big attack, with the part AI can do alone in amber. Right: the productivity gain. Amdahl's law says that if AI does a fraction of the hours, output per hour can rise by at most 1 / (1 − that fraction), however fast the AI is, because people still do the rest.
* **Marks.** Dots are medians; shaded bars are 80% ranges; the hollow dot is the theoretical ceiling, the solid dot what a gang should actually gain by the end of 2026.
* **Numbers.** [`results/c04_amdahl.json`](../results/c04_amdahl.json). AI can do 39% of the hours (31% to 47%); the ceiling is +63% (+44% to +89%), printed on the chart to the nearest ten as "+60%"; the likely gain by the end of 2026 is +10% (+2% to +25%); if AI could also do all four technical stages (1 to 4) instantly, on top of what it can already do in the other stages, output per hour could be about four times as high (3.3 to 6.1 times).
* **Read with care.** The hour shares and the AI shares are the author's judgements, informed by the evidence tables but not measured: no public dataset records a gang's hours by stage. The end-2026 figure also assumes how much of its capability a gang hands to AI (10% to 80%), how much faster AI works (3 to 20 times) and how long checking takes (10% to 40% of doing the work).
* **Built from.** [`charts/c04_amdahl.py`](../charts/c04_amdahl.py) (a Monte Carlo of those judgements). Data: [`E_stage_judgements`](../data/E_stage_judgements.csv) and [`E_stage_times`](../data/E_stage_times.csv); three further tables ([`E_incident_timelines`](../data/E_incident_timelines.csv), [`E_laundering`](../data/E_laundering.csv), [`I_business_models`](../data/I_business_models.csv)) are the evidence behind the judgements and no script reads them.
* **More.** [Model card](../docs/MODELS.md#chart-4-amdahls-law-for-a-ransomware-gang) · [methods](../docs/METHODS.md#chart-4-amdahls-law-for-a-ransomware-attack) · [sources](../docs/sources/c04_amdahl.md)

## Chart 5: how long abusers keep access to hosted AI

![Two panels of lines on a log time scale, one for operations cut off by their AI provider and one for operations no provider stopped, from one day to over a year](c05_inference.png)

* **Plots.** Fifteen malicious operations that used AI models, by how long each ran (log scale, one day to over a year): nine that their AI provider cut off (left) and six that no provider ended (right).
* **Marks.** Lines are published ranges; where a report gives only one bound the other is assumed. Arrows mean the operation is still running. The dotted line marks one month.
* **Numbers.** [`results/c05_inference.json`](../results/c05_inference.json). Of the nine cut off, three went within a month and four lasted six months or more. The beta-binomial estimate for the population of caught operations is 41% within a month (22% to 62%) and 44% six months or more (25% to 64%).
* **Read with care.** Only cases caught and disclosed appear, and the disclosures cover under three years, so long-running recent operations are missing and the true durations are probably longer, although quick catches that no report mentions would push the other way. The robustness check shows that two hidden quick catches would make most cut-offs quick, that hidden long cases can only strengthen the long end, that the shares move by 17 to 24 points depending on which of the nine cases are kept (they measure different things), and that the chart says nothing about how often providers catch abuse.
* **Built from.** [`charts/c05_inference.py`](../charts/c05_inference.py). Data: 15 of the 81 rows of [`D_platform_cases`](../data/D_platform_cases.csv), listed with their duration bounds in the script; [the data dictionary](../data/README.md#d-how-long-abusers-keep-access-to-hosted-ai-chart-5) says why the other rows are left out. Robustness: [`sensitivity/s05_provider_selection.py`](../sensitivity/s05_provider_selection.py).
* **More.** [Model card](../docs/MODELS.md#chart-5-how-long-abusers-keep-access-to-hosted-ai) · [methods](../docs/METHODS.md#chart-5-how-long-abusers-keep-access-to-hosted-ai) · [sources](../docs/sources/c05_inference.md)

## Chart 6: how fast criminals adopt new technology

![Three groups of dots on a log time scale from one day to ten years: ready-made exploits within weeks, new tools for existing work with a median of about four years, and new business models with a median of about six years, with two AI cases not yet widespread](c06_attacker_lag.png)

* **Plots.** The time from a technology becoming available to widespread criminal use, on a log scale, in three groups: ready-made exploits, new tools for existing criminal work, and new business models (which need a new market, payment system or infrastructure).
* **Marks.** A dot is one case. Amber is AI. A hollow amber dot with an arrow is an AI case that is not yet widespread, drawn at the time elapsed so far. The line is the median of its group and the shading its 80% credible interval.
* **Numbers.** [`results/c06_attacker_lag.json`](../results/c06_attacker_lag.json). Median lag: new tools 3.9 years (2.5 to 6.9), business models 5.9 years (3.7 to 9.2). AI agents running whole intrusions have been around for about 1.65 years. The chance they are widespread by the end of 2027, 2029 and 2031: 14%, 35% and 51% if they are a new business model; 22%, 55% and 72% if a new tool.
* **Read with care.** The cases were hand-picked and the classes were assigned knowing the outcomes, so the medians are illustrative. The tool path depends on how one case is dated (hijacked-gadget botnets: from the arrival of cheap gadgets in about 2014, or from the first Mirai sighting, which gives 34% instead of 55% by end-2029); see the [robustness checks](../docs/MODELS.md#chart-6-classification-and-dating).
* **Built from.** [`charts/c06_attacker_lag.py`](../charts/c06_attacker_lag.py) (a Bayesian censored log-normal model per class; cases still unfolding enter as right-censored). Data: 15 of the 18 rows of [`I_adoption_lags`](../data/I_adoption_lags.csv). Robustness: [`sensitivity/s06_adoption_lags.py`](../sensitivity/s06_adoption_lags.py).
* **More.** [Model card](../docs/MODELS.md#chart-6-how-fast-criminals-adopt-new-technology) · [methods](../docs/METHODS.md#chart-6-how-fast-criminals-adopt-new-technology) · [sources](../docs/sources/c06_attacker_lag.md)

## Chart 7: public versus private pay

![For the United States, United Kingdom, Israel and China, pairs of dots with ranges on a log dollar scale comparing state pay with private pay for AI engineers, with ratios of 1.9, 2.3, 2.6 and 8.4 times](c07_pay.png)

* **Plots.** Typical annual pay in dollars at market exchange rates (log scale) for state employers (purple) and private firms (cyan) in four countries, and the ratio of private to state pay on the right.
* **Marks.** Dots are posterior medians; bars are 80% credible intervals.
* **Numbers.** [`results/c07_pay.json`](../results/c07_pay.json). Private pay as a multiple of state pay: United States 1.9 times (0.9 to 3.7), United Kingdom 2.3 (1.2 to 4.4), Israel 2.6 (1.3 to 4.9), China 8.4 (3.4 to 20.4). Against Mossad and Shin Bet alone the Israeli ratio is about 1.7.
* **Read with care.** State pay is mostly an average for all staff or an advertised scale, not an engineer's pay, and excludes pensions and job security; private pay is self-reported or surveyed. The model puts that mismatch into the uncertainty. Russia and Iran publish nothing comparable.
* **Built from.** [`charts/c07_pay.py`](../charts/c07_pay.py) (a Bayesian measurement model of log pay, with noise that depends on each source's grade). Data: 20 of the 52 rows of [`F_pay`](../data/F_pay.csv). Robustness: [`sensitivity/s07_israel_state_pay.py`](../sensitivity/s07_israel_state_pay.py).
* **More.** [Model card](../docs/MODELS.md#chart-7-public-versus-private-pay) · [methods](../docs/METHODS.md#chart-7-public-versus-private-pay) · [sources](../docs/sources/c07_pay.md)

## Chart 8: how far governments lag business

![Pairs of dots on a timeline from 2005 to 2030 for seven technologies showing when each became mainstream in American business and in US defence and intelligence agencies, with the gap in years, and a projection for AI agents in offensive cyber operations](c08_govlag.png)

* **Plots.** When each technology became mainstream in American business (cyan) and in US defence and intelligence agencies (purple), with the gap in years, and a projection for AI agents in US offensive cyber operations (hollow dot and bar).
* **Marks.** Dots are the midpoints of the range of years (the lines) in which a technology became mainstream; the milestone differs by row (a policy memo, a big contract, a new unit, user numbers). The grey Covid row is drawn but not fitted.
* **Numbers.** [`results/c08_govlag.json`](../results/c08_govlag.json). On all six fitted rows the lag fell from about nine years in 2005 to about two in 2024 (1.2 to 3.3); without the generative-AI row, from about seven to about four (1.7 to 8.0). The projection mixes the two fits: agents become mainstream in the agencies around mid-2028 (early 2027 to mid-2033), a 72% chance by the end of 2029. Dating open source in the agencies at 2009 to 2011 instead lowers that to 55%.
* **Read with care.** The business-side years (except for generative AI) and the agencies' years for open source are the author's estimates. Six rows are few, and the downward trend in the lag rests heavily on the generative-AI case; see the [robustness checks](../docs/MODELS.md#chart-8-dating-open-source-in-the-agencies).
* **Built from.** [`charts/c08_govlag.py`](../charts/c08_govlag.py) (a Bayesian interval-censored regression of the lag on the year). Data: 7 of the 10 rows of [`G_adoption`](../data/G_adoption.csv). Robustness: [`sensitivity/s08_open_source_dating.py`](../sensitivity/s08_open_source_dating.py).
* **More.** [Model card](../docs/MODELS.md#chart-8-how-far-governments-lag-business) · [methods](../docs/METHODS.md#chart-8-how-far-governments-lag-business) · [sources](../docs/sources/c08_govlag.md)

## Chart 9: how long state hackers stay hidden

![Horizontal bars of years between first intrusion and discovery for nine state-linked campaigns, from Equation Group at 14 years to Storm-0558 at about a month, with typical Mandiant medians of 122 days for spying and 14 days for any intruder](c09_state_patience.png)

* **Plots.** Time from first intrusion to discovery for nine well-documented state-linked campaigns, and (below the line) two benchmarks.
* **Marks.** Bars and dots are single values. The open triangle on Volt Typhoon means "at least": CISA reported access held for five years or more in some networks.
* **Numbers.** [`results/c09_state_patience.json`](../results/c09_state_patience.json). Equation Group 14 years, Regin 11, Volt Typhoon 5 or more, SolarWinds about 15 months, BRICKSTORM about 13 months (an average across Mandiant cases), the OPM breach about 11 months, Midnight Blizzard about 7 weeks, the Ivanti zero-days about 5 weeks, Storm-0558 about a month. Benchmarks: a typical spying case 122 days; a typical intruder 14 days (medians of Mandiant's 2025 investigations).
* **Read with care.** These are well-documented campaigns, not a sample: ones still hidden are missing by construction and famous ones are over-represented. There is no statistical model here. Campaigns that were never found can only be long, so they cannot weaken "years"; what could is the long cases themselves (two are Kaspersky's dating of malware, and one is a lower bound that the table's own dates put at 1.9 years). The robustness check also gives the factor by which the number worked would have to be undercounted for the "sliver" to reach one in ten.
* **Built from.** [`charts/c09_state_patience.py`](../charts/c09_state_patience.py). Data: [`H_espionage_cases`](../data/H_espionage_cases.csv) (21 rows; the chart reads nine) and one row of [`E_stage_times`](../data/E_stage_times.csv). Robustness: [`sensitivity/s09_state_selection.py`](../sensitivity/s09_state_selection.py).
* **More.** [Model card](../docs/MODELS.md#chart-9-how-long-state-hackers-stay-hidden) · [methods](../docs/METHODS.md#chart-9-how-long-state-hackers-stay-hidden) · [sources](../docs/sources/c09_state_patience.md)

## Chart 10: the odds, year by year, that AI agents become routine

![Cumulative probability curves from 2027 to 2034: US defence and intelligence agencies reach 72% by the end of 2029, criminals 55% if agents are a new tool and 35% if a new business model](c10_odds.png)

* **Plots.** The chance, by each date, that AI agents running whole intrusions are in widespread use, given that they are not yet: for US defence and intelligence agencies (purple; band from the fit with and without the generative-AI case, line their mix) and for criminals (red; solid if agents are a new business model, dashed if a new tool).
* **Marks.** Dates are the start of the year, so "2030" is the end of 2029; the dotted line marks it.
* **Numbers.** [`results/c10_odds.json`](../results/c10_odds.json). Chance by the end of 2029: agencies 72% (89% on the fit with all rows, 58% without generative AI); criminals 35% if a new business model, 55% if a new tool. Years from today to even odds: agencies 1.6 (0.8 to 2.7); criminals 5.0 as a business model, 2.8 as a tool.
* **Read with care.** This chart only recombines the two models behind Charts 6 and 8, so it inherits all their weaknesses: few, hand-picked cases and judgement calls about dating. Read the numbers as rough.
* **Built from.** [`charts/c10_odds.py`](../charts/c10_odds.py), which reads the posterior draws that `c06_attacker_lag.py` and `c08_govlag.py` save in [`results/`](../results) (so those two must run first; `tools/run_all.py` does). No data table of its own.
* **More.** [Model card](../docs/MODELS.md#chart-10-the-odds-year-by-year-that-ai-agents-become-routine) · [methods](../docs/METHODS.md#chart-10-the-odds-year-by-year-that-ai-agents-become-routine) · sources: those of [Chart 6](../docs/sources/c06_attacker_lag.md) and [Chart 8](../docs/sources/c08_govlag.md)

## Chart 11: the defenders' build-up

![Left, a line of the number of 34 tracked security vendors shipping a generative-AI feature, rising from 0 in 2022 to 29 by 2026. Right, estimated annual AI spend on a log scale, about $20bn on defence against about $22m on offence in 2026](c11_defenders.png)

* **Plots.** Left: how many of 34 security and platform vendors had shipped a substantive generative-AI security feature, by year. Right: estimated annual AI spend by defenders (green) and attackers (red), on a log scale.
* **Marks.** Median (line and dots) and 80% credible interval (band).
* **Numbers.** [`results/c11_defenders.json`](../results/c11_defenders.json). 18 of 34 vendors by 2023 and 29 by 2026 (27 to 31). Defensive spend about $16bn in 2025 and $20bn in 2026; attacker spend about $22m in 2026 (about $7m to $65m); the ratio in 2026 is about 900 to 1 (roughly 275 to 3,100).
* **Read with care.** The left panel is a model of *dates* (a vendor census with graded evidence, allowing for uncertainty about dates and about what counts as "substantive"). The right panel is a judgement Monte Carlo, not a measurement: the defensive figure is the generative-AI cyber-defence market as sized by two research houses, and the attacker figure is a deliberately generous guess. Read it as an order of magnitude.
* **Built from.** [`charts/c11_defenders.py`](../charts/c11_defenders.py). Data: [`G_vendor_ai`](../data/G_vendor_ai.csv) (34 rows; the sources for each vendor are in [`G_vendor_ai_sources.md`](../data/G_vendor_ai_sources.md)).
* **More.** [Model card](../docs/MODELS.md#chart-11-the-defenders-build-up) · [methods](../docs/METHODS.md#chart-11-the-defenders-head-start) · [sources](../docs/sources/c11_defenders.md)

## Chart 12: AI-found flaws

![Left, a funnel of AI-found flaws from 29,439 flagged to 6,157 reported, 5,103 acknowledged and 516 patched. Right, the share exploited in real attacks: 1.3% of AI-found flaws tracked by VulnCheck against about 1.4% of all flaws](c12_funnel.png)

* **Plots.** Left: flaws found with AI in Anthropic's coordinated-disclosure programme, by stage, to 2 October 2026. Right: the share of AI-found flaws exploited in real attacks (VulnCheck's tracker), against a rough benchmark for all flaws.
* **Marks.** Dot: the observed share; bar: 80% credible interval from a beta-binomial.
* **Numbers.** [`results/c12_funnel.json`](../results/c12_funnel.json). 29,439 flagged (unchecked), 6,157 reported to maintainers, 5,103 acknowledged, 516 patched: 8.4% of those reported, about one in 12. Exploited: 14 of 1,061 AI-found flaws tracked, 1.3% (1.0% to 1.9%); the all-flaws benchmark is about 1.4%.
* **Read with care.** The counts are Anthropic's own and each headline number has a single source. Many reports are recent, so the patched share (and the exploitation rate) may rise. The all-flaws figure is a rough benchmark, not a like-for-like rate.
* **Built from.** [`charts/c12_funnel.py`](../charts/c12_funnel.py): the counts are typed into the script and checked against [`J_ai_vulns`](../data/J_ai_vulns.csv) (12 rows) by `tools/check_inputs.py`.
* **More.** [Model card](../docs/MODELS.md#chart-12-ai-found-flaws) · [methods](../docs/METHODS.md#chart-12-ai-found-flaws) · [sources](../docs/sources/c12_funnel.md)

## The colour contract

Colours follow the *entity*, and mean the same in every chart. Text never wears a data colour: a coloured mark sits beside text in ink.

| Colour | Hex | Means |
|---|---|---|
| Blue | `#006BA2` | Fraud and scam losses (Chart 1) |
| Red | `#DB444B` | Attackers and crime: hacking losses, criminals' pay, operations cut off, criminals' adoption, offensive spend, flaws exploited in real attacks |
| Amber | `#D08E00` | AI: what AI can do, the part of losses AI caused, AI cases among the adoption examples (pale amber: the upper range of an estimate) |
| Green | `#00876C` | Defenders: vendors and defensive spend (Charts 11 and 12) |
| Purple | `#8A4FA8` | Governments, police and state hackers |
| Cyan | `#0FA3C7` | The private sector and honest employers: business adoption, private-firm pay, legitimate developers' pay |
| Grey-blue | `#758D99` | Comparison, benchmark or "not X": cases that do not fit the chart's main contrast |
| Light grey | `#C9D3D9` | The remainder: "everything else", work that needs people, background bars |
| Red tag, top left | `#E3120B` | House-style decoration; carries no meaning |

The colours are defined once, in [`common/chart.py`](../common/chart.py), and every chart script imports them from there.

## How the charts are built

* **One canvas.** Every figure is 6.5 inches wide and must come out landscape (the script stops if its height exceeds 0.8 of its width). At 728 pixels wide, the width of a blog column, 9-point labels render at about 14 pixels and the 14-point title at about 22.
* **One layout.** A red tag with the chart number, a title that states the finding, a subtitle saying what is plotted and in what units, the plot, then a note (the caveat) and the source line in small print. The drawing code is in [`common/chart.py`](../common/chart.py).
* **Type.** [Inter](https://rsms.me/inter/) in regular, bold and italic is bundled in [`fonts/`](fonts) under the SIL Open Font License 1.1 (licence text in [`fonts/OFL.txt`](fonts/OFL.txt)), so every machine lays the charts out the same way. Nothing inside a plot is set below 8 points; labels that cross data get a white halo.
* **Numbers come from results, not from memory.** Each script computes its numbers from `data/` (or from saved draws), writes them to `results/`, and draws from those. Where a number comes from outside the tables (a cost typed from a report, a judgement bound), it is a named constant in the script, listed in [PARAMETERS](../docs/PARAMETERS.md) and, where the data hold it, checked by `tools/check_inputs.py`. `tools/verify_numbers.py` then checks the 186 numbers quoted in the methods against the results files.

## Rebuild

From the repository root, with the pinned packages installed (`pip install -r requirements.txt`):

    python tools/run_all.py --figures      # all 13 figures, reusing the saved Chart 1 model fit
    python tools/run_all.py                # refit the Chart 1 model first, then all 13
    python tools/run_all.py --only c04 c07 # just those charts (a prefix of the script name is enough)
    python charts/c04_amdahl.py            # one figure; scripts run from any directory

`make figures` and `make all` do the first two. Figures write to this folder and numbers to [`results/`](../results). Two charts need the output of others and `run_all.py` respects that: Chart 1 reads the loss-trend model's draws, and Chart 10 reads the draws that Charts 6 and 8 save.

**Reproducibility.** Every random draw is seeded (the seeds are listed in [MODELS](../docs/MODELS.md#at-a-glance)). SVG files carry no timestamp and use a fixed hash salt, so they are the same bytes from run to run. In the author's test, a rebuild in a fresh environment (`pip install -r requirements.txt`, Python 3.13, Linux) wrote all 13 PNG and all 13 SVG files byte for byte the same as the ones in this folder; that is one machine, not a guarantee for others. On other versions of matplotlib, text can shift by a fraction of a pixel, and on other versions of numpy or scipy the random streams can differ slightly; `make verify` then reports how far the regenerated numbers are from the reference ones. To see what a rebuild changed, run it inside a git clone and then `git status`.

## Reuse

The figures are licensed CC BY 4.0 ([`LICENSE-CONTENT.md`](../LICENSE-CONTENT.md)): share and adapt them, including commercially, with credit to Joshua Saxe, a link to the licence and a note of any changes. The SVG files keep their text as text and are the better starting point for edits. The underlying facts and sources keep their own rights: cite the original source (every row in `data/` has its link) where you can.
