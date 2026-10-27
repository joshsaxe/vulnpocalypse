# Models

One card per figure: the question it answers, what goes in, what the model does, which inputs are the author's judgements, how it is seeded, what it writes and where it is weak. The post's plain-language version is in [METHODS](METHODS.md), the numbers typed into scripts are in [PARAMETERS](PARAMETERS.md), and the tables are in the [data dictionary](../data/README.md).

Most of the figures are not models at all. Charts 0, 3 and 9 draw reported numbers; Chart 12 is one line of conjugate algebra. The statistical work is in Charts 1, 2, 4, 5, 6, 7, 8 and 11, and Chart 10 combines two of them. The code is deliberately plain (numpy and scipy, no probabilistic-programming library) so that it can be read: the samplers are in [`common/bayes.py`](../common/bayes.py) and [`common/dfm.py`](../common/dfm.py) and are short.

## At a glance

| Figure | Kind | Method | Seeds | Draws |
|---|---|---|---|---|
| 0 Lede | no model | three documented costs | none | none |
| 1 Losses | Bayesian trend, plus judgement Monte Carlo | one-factor dynamic model by Gibbs sampling for the trend; a separately triangulated level; a structural Monte Carlo for the AI share | 11, 12, 31 (trend fits); 21, 22, 32 (fits to 2022); 2025 (level, drift, AI share); 5, 6, 8, 15, 16, 18 (forecasts) | 6,000 per quantity (9,000 Gibbs sweeps, 3,000 burn-in) |
| 2 Police | Bayesian estimate | beta-binomial by sector; Aalen-Johansen estimate with a Bayesian bootstrap | 22 | 4,000 bootstrap resamples |
| 3 Pay | no model | direct observations | none | none |
| 4 Amdahl | judgement Monte Carlo | Amdahl's law with stage shares and AI-doable shares drawn from the author's ranges | 55 | 40,000 |
| 5 Access | Bayesian estimate | log-uniform durations between bounds; beta-binomial shares | 44 | 20,000 |
| 6 Adoption | Bayesian estimate | interval- and right-censored log-normal lags by class; adaptive Metropolis | 11 | 4 chains, 20,000 iterations, 5,000 burn-in, every 5th kept |
| 7 Pay gap | Bayesian estimate | normal measurement model for log pay, one posterior per country and side | 66 | 60,000 |
| 8 Government lag | Bayesian regression | interval-censored regression of log lag on year; adaptive Metropolis | 7, 8 (fits); 78, 79 (predictions) | 4 chains, 30,000 iterations, 8,000 burn-in, every 5th kept |
| 9 State | no model | reported dates and counts | none | none |
| 10 Odds | combination | posterior draws from Charts 6 and 8 | none (reads their draws) | those of Charts 6 and 8 |
| 11 Defenders | two Monte Carlos | vendor census with uncertain feature and date; spend judgements | 77 (vendors); 2026 (spend) | 60,000; 80,000 |
| 12 Funnel | Bayesian estimate | beta-binomial | none (exact) | none |

**Conventions.** A line or dot is the posterior median and a band or whisker an 80% interval: a credible interval where the data decide the answer, an "80% range" where the author's judgements do (the AI share in Chart 1, Chart 4, the spend panel of Chart 11). Dates in results files are the start of a year, so "2030" means the end of 2029.

**Convergence.** Charts 6 and 8 store the Gelman-Rubin R-hat of their four chains (1.00 to three decimals for every parameter). The Gibbs sampler for Chart 1 has no stored diagnostic: every conditional distribution is conjugate, so it is exact, and 6,000 sweeps are kept after 3,000 of burn-in.

**Randomness and versions.** Every script is seeded and writes the same numbers on every run on the same library versions ([`requirements.txt`](../requirements.txt) pins the four that matter; [`requirements-lock.txt`](../requirements-lock.txt) pins all fourteen). Rebuilt in a fresh environment, every results file and every file of saved draws came out byte for byte the same as the one in this repository. On other versions of numpy and scipy the random streams differ and numbers move by Monte Carlo noise, a point or so on a probability; `tools/verify_numbers.py` says which numbers moved and whether the move is within tolerance.

---

## Lede: the price of a hack

Code: [`charts/c00_lede_cost.py`](../charts/c00_lede_cost.py) · results: [`results/c00_lede_cost.json`](../results/c00_lede_cost.json)

- **Question.** How little does the automated part of a cyber-attack now cost, in AI tokens?
- **Inputs.** Three documented cases, typed in the script: about $0.22 and $7.80 a bug (CyberGym: a cheap open model solved 20 of 20 bugs for $4.38 and a frontier agent 17 of 20 for $132.65; `tools/check_inputs.py` redoes the division), "less than $3,000 in tokens" (Hacktron's break-in to OpenAI's code repository) and about $40,000 (XBOW's full-chain Chrome exploit).
- **Weak points.** Single cases, not averages. Only the automated part is priced: a real attack also needs people, infrastructure and luck, and a flaw that crashes a program is far from a reliable weapon. "Less than $3,000" is an upper bound.

## Chart 1: losses to fraud and hacking, and the part caused by AI

Code: [`models/c01_loss_trend.py`](../models/c01_loss_trend.py), [`common/dfm.py`](../common/dfm.py), [`common/deflators.py`](../common/deflators.py), [`charts/c01_losses.py`](../charts/c01_losses.py) · results: [`results/c01_loss_trend.json`](../results/c01_loss_trend.json) and the draws in `c01_loss_trend_draws.npz` · robustness: [`sensitivity/s01_loss_trend.py`](../sensitivity/s01_loss_trend.py)

- **Question.** How large are losses to cyber-enabled fraud and to hacking, how fast did they grow, and how much of 2025's losses would not have happened without AI?
- **Data.** 23 pooled loss series: 15 for fraud (five American pieces and ten from other countries and regions) and eight for hacking, built from `A1_fraud_series`, `A2_hacking_series` and `cpi_u`; AI evidence in `A1_fraud_ai_evidence` and `A2_hacking_ai_evidence`. All values are put in 2025 dollars (US CPI-U; other countries' indices are hand-entered in `common/deflators.py`).
- **Step 1, the shape.** On the log scale, series *s* in year *t* is its own level, plus its own slow reporting drift, plus a shared trend, plus noise: `y[s,t] = alpha[s] + delta[s] (t - t0) + x[t] + e[s,t]`. The trend is smooth: its second difference is normal with variance tau squared, so its growth rate can drift a little each year. Priors: level `N(0, 10^2)`, drift `N(0, 0.03^2)` (three points a year), noise variance inverse-gamma(3, 0.12) (a typical noise of about 0.2 log points), tau squared inverse-gamma(2, 0.02). A reference series (the one with the most years) pins the level. A change of definition starts a new series. America and the rest of the world are fitted separately for fraud and added; hacking is one global trend. The sampler is Gibbs, 9,000 sweeps with 3,000 burn-in.
- **Step 2, the level.** Every published series is a floor, so the 2025 level comes from the author's earlier triangulation, typed in the script: fraud log-normal with median $220bn and 90% interval $105-461bn, hacking median $76bn ($31-188bn), America's share of fraud a beta with mean 0.42 and 10th percentile 0.32. The trend is scaled to this level; it supplies the shape only.
- **Step 3, the reporting drift.** If reporting rises everywhere at once, every series overstates growth and step 1 cannot tell. The model subtracts an assumed common drift: America's portals 2% a year (sd 2 points), other countries 1% (sd 1.5), hacking 1% (sd 2). It is an assumption, not an estimate; `s01` varies it.
- **The AI share.** Not read from the loss data (a few per cent is far inside the noise) but built from evidence: `share = noticed x but-for(noticed) + unnoticed x but-for(unnoticed)`. "Noticed" is the share of dollars in FBI complaints that mention AI (4.2% of fraud-type and 1.4% of hacking-type dollars in 2025, log-normal around those); "unnoticed" is losses where AI was used and victims could not tell (about 10% for fraud and 20% for hacking, from Verizon and IBM); the two but-for fractions are betas matched to a stated mean and 80% range. Because the but-for fractions are judgements, three sets of them are averaged with equal weight: central (a quarter of the noticed losses would not have happened without AI), sceptical (a tenth) and generous (a half, with larger unnoticed shares). 2024 and 2023 scale 2025 by an adoption index (betas with means 0.5 and 0.25). The parameters are in `AI_PARAMS` and `AI_SPECS` in the script.
- **The test the data can do.** Both trend models are refitted on data to 2022 and projected to 2025 under the smooth-trend prior (`forecast_from` in `common/dfm.py`). If AI had driven a surge, 2023-25 losses would sit above the projection; they sit below it with probability 0.84 (fraud) and 0.74 (hacking). The 2026 column is the same machinery run one more year.
- **Output.** `fraud_q`, `hack_q` (quantiles by year), `ai_*`, `total_2025`, `ai_share_total_2025` (10th, 50th, 90th percentiles: 0.5%, 1.6%, 4.5%), the growth rates, `p_fraud_below_pretrend`, `p_hack_below_pretrend`, and more, in the JSON.
- **Weak points.** The level is not estimated here. The AI share is a judgement and its interval is wide by design. The common drift is assumed. The pre-2022 test cannot rule out a small AI effect masked by other forces such as banks' new anti-scam controls. Two of the hacking indicators count incidents rather than dollars. Series with definition breaks are split by hand. The fraud slowdown after 2022 is not robust to every assumption: see [Robustness checks](#robustness-checks).

## Chart 2: what happens to criminal enterprises

Code: [`charts/c02_police.py`](../charts/c02_police.py), [`common/lifespans.py`](../common/lifespans.py) · results: [`results/c02_police.json`](../results/c02_police.json)

- **Question.** What share of criminal enterprises end because police act, and how soon?
- **Data.** `B_enterprise_lifespans`: 152 enterprises in ten sectors (grouped into six on the chart). `end_type` says how each ended; police endings are takedown, seizure, arrests, sanctions and a shutdown or rebrand that the operators or reporting tie to police pressure (six rows). Endings by retirement, exit scam or plain rebrand, and enterprises still running, are not police endings.
- **Model.** For each sector, the police share of *ended* enterprises has a uniform Beta(1, 1) prior and a binomial likelihood, so the posterior is Beta(1 + police, 1 + others). The bars show only enterprises that have ended, so young sectors are not counted against the police for being young. Whiskers are 80% highest-density intervals, so that a sector where police ended every closed enterprise is not drawn outside its own interval. Separately, the 115 enterprises with known start and end dates give an Aalen-Johansen estimate of the share ended by police within 2, 5 and 10 years of launch (other endings are competing risks that remove an enterprise from the risk set; the 16 of them still running are censored on 21 October 2026), with a Bayesian bootstrap (Dirichlet weights, 4,000 resamples) for its 80% interval. Dates given to the year, month or day are placed at the middle of that period, and a lifespan is at least 0.08 years.
- **Output.** `all`: 132 ended, 98 by police, median 0.74 (0.69-0.787). `cif_police`: 0.207, 0.395 and 0.655 at 2, 5 and 10 years (medians). `police_share_of_closed_hdi80_pct`: the highest-density intervals drawn.
- **Weak points.** Selection: enterprises famous enough to be documented are more often ones police acted against, which probably flatters the police. The classification of ambiguous endings is a judgement. Three rows are unverified recollections (see the [data dictionary](../data/README.md#how-reliable-is-this); dropping them moves the all-sector median from 74.0% to 73.4%). The 37 undated enterprises are out of the dated estimate, so the text does not rely on it.

## Chart 3: what crime pays

Code: [`charts/c03_talent.py`](../charts/c03_talent.py) · results: [`results/c03_talent.json`](../results/c03_talent.json)

- **Question.** What do criminal organisations pay coders, against what honest developers earn where the adverts were posted and elsewhere?
- **Not a model.** Observations only: leaked Conti chats, Kaspersky's study of dark-web job adverts, a US indictment, Habr Career's Russian medians (typed, converted at the World Bank's 2021 rate of 73.65 roubles to the dollar), national statistics and surveys for Ukraine, Belarus, China, Brazil, Vietnam and Kazakhstan, the US Bureau of Labor Statistics, and Levels.fyi. The band is the range of the adverts' median pay by role, $1,300-4,000 a month.
- **Output.** The title's "a tenth" is the median developer advert ($24,000) over American AI engineers' median total pay ($250,000): 9.6% (`dev_ad_over_ai_engineers_pay`).
- **Weak points.** The figures are not strictly comparable: survey medians, sector means, gross and net, total pay with and without stock, developers of every level against adverts that probably seek experienced coders. Self-selected surveys lean towards the better paid. Iran is left out for want of a reliable figure.

## Chart 4: Amdahl's law for a ransomware gang

Code: [`charts/c04_amdahl.py`](../charts/c04_amdahl.py), [`common/bayes.py`](../common/bayes.py) · results: [`results/c04_amdahl.json`](../results/c04_amdahl.json)

- **Question.** If AI did everything it can, how much more output per working hour could a ransomware attack have?
- **Inputs.** `E_stage_judgements`: for eight stages, the author's low, central and high judgements of each stage's share of the hours behind one attack and of the share of that work today's best AI could do unaided. They draw on `E_stage_times`, `E_incident_timelines`, `E_laundering` and `I_business_models`. No public dataset measures hours by stage.
- **Model.** 40,000 draws. Hour shares are Dirichlet with the central judgements as the mean, the concentration chosen from a grid so that the 80% ranges match the stated widths. Each stage's AI-doable share is a beta fitted to its low, central and high judgement as the 10th, 50th and 90th percentiles. With `P = sum(w_j p_j)`:
    - *ceiling*: `1 / (1 - P)`, if AI did all it could, instantly and without error;
    - *likely gain today*: `1 / ((1 - dP) + dP (1/k + v))`, where `d` is the share of AI-doable work that gangs actually hand to AI (80% range 10-80%, deliberately wide), `k` AI's speed-up on that work (log-normal, 80% range 3-20 times) and `v` the time spent checking AI's work relative to doing it by hand (80% range 10-40%);
    - *future*: `1 / (1 - technical hours - AI-doable share of the other hours)`, if AI could do all four technical stages as well.
- **Output.** Ceiling 1.63 times (80% range 1.44-1.89); likely gain 1.10 (1.02-1.25); future 4.3 (3.3-6.1); AI-doable share of hours 39% (31-47%); the stage bars show the central judgements, which sum to 100%.
- **Weak points.** Everything is judgement, and the 80% ranges are the author's. The shares describe the hours behind one attack, mostly an affiliate's, not the platform operators'. Amdahl's law caps how fast the workers go, not how many attacks there are or how many victims pay; the table's own text notes that conversion to payment is demand-limited. The "likely" figure depends on the three wide inputs `d`, `k` and `v`.

## Chart 5: how long abusers keep access to hosted AI

Code: [`charts/c05_inference.py`](../charts/c05_inference.py) · results: [`results/c05_inference.json`](../results/c05_inference.json)

- **Question.** When an AI provider catches a hacking, fraud or spying operation, how long had it run, and how often is nobody stopping it?
- **Data.** 15 of the 81 rows of `D_platform_cases`: nine cases a provider cut off and whose report bounds the duration (`CAUGHT` in the script), and six where no provider ended the operation (`NOTCUT`). Where a report gives one bound only, the other is assumed and labelled in the note; where a duration is exact it is widened by 20% each way.
- **Model.** In each of 20,000 draws every case's duration is log-uniform between its bounds. The model counts the cases cut off within 30 days and those that ran 180 days or more, and combines each count with a uniform Beta(1, 1) prior to give the population share (median and 80% interval).
- **Output.** Cut off within 30 days: 41% (22-62%); ran 180 days or more: 44% (25-64%).
- **Weak points.** Nine cases. Only operations that were caught and disclosed appear, over a window of about three years, so long-running recent operations are missing and true durations are probably longer. Almost every row is a vendor describing its own detection. The log-uniform assumption within bounds, and the assumed bounds, are choices.

## Chart 6: how fast criminals adopt new technology

Code: [`charts/c06_attacker_lag.py`](../charts/c06_attacker_lag.py), [`common/bayes.py`](../common/bayes.py) · results: [`results/c06_attacker_lag.json`](../results/c06_attacker_lag.json), draws in `c10_draws_criminals.npz` · robustness: [`sensitivity/s06_adoption_lags.py`](../sensitivity/s06_adoption_lags.py)

- **Question.** How long do criminals take to adopt a new technique at scale, and what does that imply for AI agents?
- **Data.** 15 of the 18 rows of `I_adoption_lags`: twelve techniques that scaled and three that have not yet (criminal chatbots, malware that calls AI, AI agents that run whole intrusions). The author classed each as a ready-made exploit, a new tool (usable inside existing criminal work) or a new business model (needing a new market, payment system or infrastructure). The two exploits were used within days or weeks, so they are shown and not fitted.
- **Model.** Within the tool and business-model classes, lag is log-normal with `mu ~ N(0, 2^2)` (centred on one year) and `sigma ~ HalfNormal(1.5)`. Dates are known to the year, so a scaled lag *L* enters as the interval *L* plus or minus half a year (plus or minus half of *L* if it is under a year, and never shorter than a day); techniques that have not scaled enter as right-censored ("at least this long so far"). The posterior is sampled by adaptive Metropolis (four chains). The chance that AI agents running whole intrusions, around since February 2025 (1.65 years before October 2026), are widespread by a later date `t` is `[F(t - start) - F(elapsed)] / [1 - F(elapsed)]`, averaged over posterior draws, where `F` is the log-normal distribution function. The business-model line is the chart's assumption; the tool line refits the tool class with agentic intrusion included as a not-yet-scaled tool.
- **Output.** Median lag for tools 3.9 years (80% interval 2.5-6.9) and for business models 5.9 (3.7-9.2). Chance agents are widespread by the end of 2027, 2029 and 2031: 14%, 35%, 51% as a business model; 22%, 55%, 72% as a tool (results keys 2028, 2030, 2032).
- **Weak points.** Fifteen hand-picked, famous cases. The author assigned the classes knowing the outcomes, and the numbers depend on that and on two datings (see [Robustness checks](#robustness-checks)). The log-normal shape and the assumption that past lags guide this technology are not tested.

## Chart 7: public versus private pay

Code: [`charts/c07_pay.py`](../charts/c07_pay.py) · results: [`results/c07_pay.json`](../results/c07_pay.json) · robustness: [`sensitivity/s07_israel_state_pay.py`](../sensitivity/s07_israel_state_pay.py)

- **Question.** How much more do private firms pay AI engineers than security agencies do, country by country?
- **Data.** 20 of the 52 rows of `F_pay` (listed by number in `USE` in the script): for the United States, United Kingdom, Israel and China, the state rows and the private-sector median, and for the United States the OpenAI and Anthropic medians.
- **Model.** For each country and side, typical pay `P` is estimated on the log scale. Each source is a noisy measurement of `log P`: the midpoint of its range, with a standard deviation that adds, in quadrature, source quality (0.15 for grade A, 0.25 B, 0.40 C, 0.60 D), half the width of an advertised range divided by 1.28 (the range is read as an 80% interval) and 0.25 for mismatch between the role and the engineer. The prior is log-normal centred on $80,000 with a standard deviation of 10 log units, which is flat in effect. The posterior is exact (normal); 60,000 draws are taken from it, and the private-to-state ratio is computed draw by draw so that its interval reflects both sides.
- **Output.** Private-to-state ratio: United States 1.9 (80% interval 0.95-3.7), United Kingdom 2.3 (1.2-4.4), Israel 2.6 (1.3-4.9), China 8.4 (3.4-20).
- **Weak points.** State pay is mostly an advertised scale or an average for all staff, not engineers' pay; private pay is self-reported. China's state figure is one contractor's 2022 salary sheet, set against 2026 private pay. Pensions and job security are excluded. Russia and Iran publish nothing comparable.

## Chart 8: how far governments lag business

Code: [`charts/c08_govlag.py`](../charts/c08_govlag.py), [`common/bayes.py`](../common/bayes.py) · results: [`results/c08_govlag.json`](../results/c08_govlag.json), draws in `c10_draws_agencies.npz` · robustness: [`sensitivity/s08_open_source_dating.py`](../sensitivity/s08_open_source_dating.py)

- **Question.** How long do US defence and intelligence agencies take to adopt technology that business adopted first, is that shrinking, and when might they routinely use AI agents in offensive cyber operations?
- **Data.** Six rows of `G_adoption` are fitted (open source, agile development, smartphones, cloud, machine learning, generative AI); the Covid-era switch to video calls is shown and not fitted. Each row gives a range of years in which the technology became mainstream in business and a range for the agencies; the lag is known only to lie in `[agency_low - business_high, agency_high - business_low]` (at least a quarter of a year).
- **Model.** `log L_i ~ Normal(a + b (year_i - 2015), s)` with the interval known only: an interval-censored regression of log lag on the year of business adoption. Priors: `a ~ N(log 5, 1)`, `b ~ N(0, 0.1^2)`, `s ~ HalfNormal(0.7)`. Adaptive Metropolis, four chains of 30,000 iterations with 8,000 burn-in. It is fitted twice, with all rows and without generative AI, which is the only recent row and carries much of the trend. The projection takes business adoption of AI agents as uniform over 2025-26, adds a lag drawn from each fit's posterior predictive, keeps dates after October 2026 ("not yet"), and pools the two fits' draws. The two fits have equal weight before that condition; afterwards about 44% of the draws come from the all-rows fit and 56% from the fit without generative AI, because the second puts more of its probability on later dates.
- **Output.** With all rows the lag falls from about 8.9 years in 2005 to 1.95 in 2024 (80% interval 1.2-3.3); without generative AI, from about 7.2 to 3.9 (1.7-8.0). Agencies' routine use of agents: median mid-2028 (2027.1 to 2033.5), 72% by the end of 2029.
- **Weak points.** Six data points. The business-side years for all but generative AI and the agency years for open source are the author's estimates. Milestones differ by row. The result leans on generative AI (without it the lag may or may not be shrinking: probability 0.79). "Business adoption in 2025-26" for AI agents is typed. See [Robustness checks](#robustness-checks) for the dating of open source.

## Chart 9: how long state hackers stay hidden

Code: [`charts/c09_state_patience.py`](../charts/c09_state_patience.py) · results: [`results/c09_state_patience.json`](../results/c09_state_patience.json)

- **Not a model.** Every bar is a reported date or count: the time from a campaign's first intrusion to its discovery as the investigators give it (nine campaigns of `H_espionage_cases`), and two benchmarks from Mandiant's M-Trends 2026 (122 days for espionage and North Korean IT-worker cases, 14 days for all intrusions). Volt Typhoon's five years is a lower bound (time in the network, not time to discovery) and has a hollow marker.
- **Weak points.** Campaigns still hidden are missing by construction and famous ones are over-represented, so the bars show what is possible, not how typical it is.

## Chart 10: the odds, year by year, that AI agents become routine

Code: [`charts/c10_odds.py`](../charts/c10_odds.py) · results: [`results/c10_odds.json`](../results/c10_odds.json)

- **Question.** For each date, how likely is it that AI agents running whole intrusions are in routine use by criminals, and by US agencies, given that they are not yet?
- **Inputs.** The posterior draws that Chart 6 (criminals) and Chart 8 (agencies) save in `results/`; nothing else. Run those first.
- **Method.** Criminals: the formula in Chart 6, over the posterior draws of the business-model fit (solid line) and of the tool fit (dashed line). Agencies: the share of the pooled draws from Chart 8 that fall before each date.
- **Output.** By the end of 2029: agencies 72% (89% on the fit with all rows, 58% without generative AI), criminals 35% as a business model and 55% as a tool. Years from October 2026 to even odds: agencies 1.6 (0.8 and 2.7 on the two fits), criminals 5.0 as a business model and 2.8 as a tool.
- **Weak points.** Inherits every weakness of Charts 6 and 8, assumes the two models are independent, and rests on few hand-picked cases.

## Chart 11: the defenders' build-up

Code: [`charts/c11_defenders.py`](../charts/c11_defenders.py) · results: [`results/c11_defenders.json`](../results/c11_defenders.json)

- **Left panel, vendor adoption.** The census is `G_vendor_ai`: 34 vendors, each dated to its first substantive generative-AI security feature, with the feature graded A, B, C or none and the date's confidence A, B or C. In each of 60,000 draws a vendor's feature counts with probability 1.0 (A), 0.95 (B), 0.60 (C) or 0 (none), and its year is the recorded year (confidence A), that year with probability 0.8 and a year either side otherwise (B), or that year with probability 0.5 and up to two years either side (C), clipped to 2022-26. Every vendor tracked stays in the denominator. Output: a median of 18 vendors by 2023 and 29 by 2026 (80% interval 27-31), against 31 in the raw census.
- **Right panel, spend.** A judgement Monte Carlo (80,000 draws), not a measurement. Defensive spend is log-normal around anchors of $8.0bn in 2022 rising to $20.3bn in 2026 (two market-research houses' figures for the generative-AI cyber-defence market, about $16bn in 2025 and $20bn in 2026, and the implied back-cast), with a log-standard-deviation of 0.42. Offensive spend is log-normal around the author's generous guess of $0.3m in 2022 rising to $22m in 2026, with a log-standard-deviation of 0.85. The two are drawn independently. Output: a 2026 ratio of about 920 (80% range about 275-3,100).
- **Weak points.** The census is of large vendors, chosen by the author, and dates come from the vendors' own announcements. The defensive anchors are soft market-research figures and probably broad. The offensive figure is a guess: bespoke criminal tools proved thin wrappers or scams, and most criminal use is of jailbroken mainstream models. The ratio is an order of magnitude, nothing finer.

## Chart 12: AI-found flaws

Code: [`charts/c12_funnel.py`](../charts/c12_funnel.py) · results: [`results/c12_funnel.json`](../results/c12_funnel.json)

- **Data.** Counts typed in the script and checked against `J_ai_vulns`: Anthropic's coordinated-disclosure dashboard (2 October 2026: 29,439 candidates, 6,157 reported to the maintainers of 591 projects, 5,103 acknowledged, 516 patched) and VulnCheck's tracker of AI-attributed vulnerabilities (28 July 2026: 14 of 1,061 exploited in real attacks).
- **Model.** The chance that an AI-found flaw is exploited has a uniform Beta(1, 1) prior and 14 successes in 1,061, so the posterior is Beta(15, 1,048): median 1.4% (80% interval 0.97-1.9%). The patched share of reported flaws is 516 / 6,157 = 8.4%.
- **Weak points.** Each headline count has one source, the organisation that runs the programme or tracker, with no outside check. The comparison rate, about 1.4%, is VulnCheck's ratio of flaws newly confirmed as exploited in the first half of 2026 to flaws newly published then; it is not like for like, because exploitation builds up over years (over the long run about 6% of published flaws have been exploited). AI-found flaws are mostly recent, so the exploitation rate may rise and the patched share will.

---

## Shared code

| File | What it does |
|---|---|
| [`common/paths.py`](../common/paths.py) | Finds the repository root, so every script runs from any folder, and gives `dump_json`, which writes every results file the same way (indented JSON). |
| [`common/chart.py`](../common/chart.py) | The chart kit: a 6.5-inch landscape canvas with a numbered tag, a title that states the finding, a subtitle, the note and the source line; one fixed colour per kind of thing; the bundled Inter font; label halos and annotation helpers; and fixed matplotlib settings (including a fixed SVG hash salt and no timestamp) so that the SVGs are byte-for-byte reproducible. Each figure is saved as a PNG at 250 dpi and as an SVG. See the [figure guide](../figures/README.md). |
| [`common/bayes.py`](../common/bayes.py) | Adaptive random-walk Metropolis with R-hat; the interval-censored log-normal fit; functions that turn a stated low, central and high judgement into a beta or log-normal distribution. |
| [`common/dfm.py`](../common/dfm.py) | The one-factor dynamic model for Chart 1 (a Gibbs sampler) and its forecast function. |
| [`common/deflators.py`](../common/deflators.py) | Converts each country's loss series to 2025 prices: US CPI-U from `data/cpi_u.csv`, other countries' indices typed by hand. |
| [`common/lifespans.py`](../common/lifespans.py) | Loads and dates the enterprise lifespans for Chart 2. |

## Robustness checks

Four scripts in [`sensitivity/`](../sensitivity) reproduce the robustness numbers quoted in the post's methods appendix, by rerunning a model with one assumption changed at a time. Each stops if its "charted" row does not reproduce the chart's own results. Run them with `make sensitivity` (about five minutes on two cores; Charts 6, 7 and 8 are rerun first, because the checks for them compare against those charts' results). Results are in `results/sensitivity_*.json`.

### Chart 1: the trend

Medians, per cent a year. Source: [`results/sensitivity_c01.json`](../results/sensitivity_c01.json).

| Variant | Fraud 2017-22 | Fraud 2022-25 | Hacking 2017-22 | Hacking 2022-25 | 2025 fraud, $bn | 2025 hacking, $bn |
|---|---:|---:|---:|---:|---:|---:|
| as charted | 14.0 | 9.3 | 23.4 | 10.2 | 221.6 | 74.4 |
| no common reporting drift | 15.3 | 10.9 | 24.6 | 11.3 | 218.8 | 76.2 |
| common drift doubled | 12.9 | 8.0 | 22.1 | 9.1 | 220.4 | 76.7 |
| each series may drift 1 point a year | 11.1 | 10.7 | 24.1 | 9.8 | 220.3 | 76.2 |
| each series may drift up to 6 points a year | 16.9 | 8.2 | 21.9 | 11.0 | 218.5 | 75.4 |
| hacking: dollar series only | | | 28.8 | 3.2 | | 75.7 |

How to read it:

- **The 2025 levels barely move**, because they are fixed by the triangulation, not by the trend.
- **For hacking, growth slowed after 2022 in every variant**, by at least ten points a year. With only the dollar series, it has been about 3% a year since 2022.
- **For fraud, the slowdown is 4 to 9 points a year in four variants and almost nothing in the fifth**, where series are allowed to drift only one point a year relative to the others (11.1% a year, then 10.7%). The post's appendix says the finding "survives" these changes, and gives the ranges across variants (12-17% then 8-11%); the table is the fuller picture. On medians the first range is 11.1-16.9%.

### Chart 6: classification and dating

Median lag in years (80% interval), and the chance that AI agents running whole intrusions are widespread by the end of 2027, 2029 and 2031 (results keys 2028, 2030, 2032). Source: [`results/sensitivity_c06.json`](../results/sensitivity_c06.json).

| Business-model class | Median lag | By end-2027 | By end-2029 | By end-2031 |
|---|---|---:|---:|---:|
| as charted | 5.87 (3.66-9.24) | 14% | 35% | 51% |
| original classification (deepfake-voice fraud a business model; double extortion a tool) | 7.41 (5.69-9.55) | 4% | 21% | 43% |
| encrypt-and-ransom dated from its first criminal use, 2006 (7 years, not the 1996 paper's 17) | 5.27 (3.47-7.72) | 16% | 41% | 58% |

The quoted values are in the post's appendix. The next table is **not**: auditing the inputs found two dates that can be read differently, and the new-tool line of Chart 10 (the dashed line) is sensitive to both.

| New-tool class | Median lag | By end-2027 | By end-2029 | By end-2031 |
|---|---|---:|---:|---:|
| as charted | 3.92 (2.52-6.92) | 22% | 55% | 72% |
| hijacked-gadget botnets (Mirai) dated from first sighting, 0.1 years, not from the spread of cheap insecure gadgets in about 2014, 2.3 years | 2.51 (0.83-8.05) | 17% | 34% | 44% |
| AI-written phishing at the lag implied by calendar years, 1.6 years, not the table's 2.5 (which counts to Verizon's 2025 finding that about 10% of malicious e-mail had AI-written text) | 3.72 (2.16-7.33) | 23% | 51% | 66% |

The new-tool path to routine criminal use of AI agents by the end of 2029 is 55% as charted and 34% if Mirai is dated from its first sighting.

### Chart 7: Israel

Private-to-state pay ratio, 80% interval. Source: [`results/sensitivity_c07.json`](../results/sensitivity_c07.json).

| State side | Ratio |
|---|---|
| as charted: IDF career staff (starting and average pay), Mossad and Shin Bet average, IDF civilian staff | 2.57 (1.34-4.92) |
| Mossad and Shin Bet average only | 1.68 (0.78-3.57) |

### Chart 8: dating open source in the agencies

Source: [`results/sensitivity_c08.json`](../results/sensitivity_c08.json).

| Open source's agency years | Chance the lag is shrinking, all rows | ... without generative AI | Agencies' routine use: median (80% interval) | By end-2029 |
|---|---:|---:|---|---:|
| 2012-14 (as charted) | 0.975 | 0.789 | 2028.4 (2027.1-2033.5) | 72% |
| 2009-11 (from the Pentagon's October 2009 policy memo) | 0.917 | 0.448 | 2029.5 (2027.2-2037.9) | 55% |

With the earlier date, the fit without generative AI no longer finds a shrinking lag (probability 0.45), so the case that the lag is shrinking rests on generative AI alone.
