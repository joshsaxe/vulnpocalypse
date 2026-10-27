# Methods

This page reproduces the plain-language methods appendix of the post (Appendix A), so that the repository can be read on its own, and says under each figure where to find its code, results, data and checks. The text is the post's, apart from one sentence in the first paragraph, which pointed to "the author" and now points to this repository, and the run-in bold labels, which have become headings. Numbers are the post's too: `python tools/verify_numbers.py` recomputes every one of them from the results files (see [Notes on the wording](#notes-on-the-wording-above)).

For the models in more detail (priors, seeds, what each script writes, how each was checked) see [MODELS](MODELS.md). For the documents behind the data see the [bibliography](BIBLIOGRAPHY.md); for every number typed into a script see [PARAMETERS](PARAMETERS.md); for what is in each table and how far to trust it see the [data dictionary](../data/README.md).

## Where each figure is made

| Figure | Run | Results | Robustness check |
|---|---|---|---|
| Lede: the price of a hack | `c00_lede_cost.py` | [`c00_lede_cost.json`](../results/c00_lede_cost.json) |  |
| 1. Losses to fraud and hacking | `c01_loss_trend.py` + `c01_losses.py` | [`c01_loss_trend.json`](../results/c01_loss_trend.json) | [`s01_loss_trend.py`](../sensitivity/s01_loss_trend.py) |
| 2. How criminal enterprises end | `c02_police.py` | [`c02_police.json`](../results/c02_police.json) | [`s02_police_selection.py`](../sensitivity/s02_police_selection.py) |
| 3. What crime pays | `c03_talent.py` | [`c03_talent.json`](../results/c03_talent.json) |  |
| 4. Amdahl's law for a ransomware gang | `c04_amdahl.py` | [`c04_amdahl.json`](../results/c04_amdahl.json) |  |
| 5. Access to hosted AI | `c05_inference.py` | [`c05_inference.json`](../results/c05_inference.json) | [`s05_provider_selection.py`](../sensitivity/s05_provider_selection.py) |
| 6. How fast criminals adopt technology | `c06_attacker_lag.py` | [`c06_attacker_lag.json`](../results/c06_attacker_lag.json) | [`s06_adoption_lags.py`](../sensitivity/s06_adoption_lags.py) |
| 7. Public versus private pay | `c07_pay.py` | [`c07_pay.json`](../results/c07_pay.json) | [`s07_israel_state_pay.py`](../sensitivity/s07_israel_state_pay.py) |
| 8. How far governments lag business | `c08_govlag.py` | [`c08_govlag.json`](../results/c08_govlag.json) | [`s08_open_source_dating.py`](../sensitivity/s08_open_source_dating.py) |
| 9. How long state hackers stay hidden | `c09_state_patience.py` | [`c09_state_patience.json`](../results/c09_state_patience.json) | [`s09_state_selection.py`](../sensitivity/s09_state_selection.py) |
| 10. The odds that AI agents become routine | `c06_attacker_lag.py` + `c08_govlag.py` + `c10_odds.py` | [`c10_odds.json`](../results/c10_odds.json) |  |
| 11. The defenders' build-up | `c11_defenders.py` | [`c11_defenders.json`](../results/c11_defenders.json) |  |
| 12. AI-found flaws | `c12_funnel.py` | [`c12_funnel.json`](../results/c12_funnel.json) |  |

Charts 1 and 10 depend on other scripts: Chart 1 reads the loss-trend model's output, and Chart 10 reads the posterior draws that Charts 6 and 8 save. `python tools/run_all.py` respects that order.

## Appendix A: methods in plain language

Each paragraph below explains how one figure’s numbers were made, in the order the figures appear, and what they can and cannot show.

### The common idea

The charts that show estimates use Bayesian statistics. In plain terms: start from a stated range of plausible values (the “prior”), let the evidence narrow it (the “likelihood”), and report what is left (the “posterior”). Where a chart shows a line or dot with a shaded band, a pale bar or a whisker, the line or dot is the posterior median, the single most representative value, and the band, bar or whisker is an 80% credible interval: on the model’s assumptions there is an 80% chance that the true value lies inside it. Wide bands mean thin evidence. Several inputs are the author’s judgements, not measurements; they are stated below so that readers can disagree with them, and where an estimate rests mainly on such judgements (the AI share in chart 1, chart 4 and the spending comparison in chart 11) its interval is called an 80% range rather than a credible interval. Code, data and research notes are in this repository.

### Lede figure: the price of a hack

Not an estimate; each number is one documented public case, picked as the best available evidence. Costs are in AI tokens, converted to dollars. To find a flaw: the per-bug cost of autonomous coding agents set loose on real open-source bugs in the CyberGym academic test (Lu et al., October 2026), from about 20 cents a bug with a cheap open model to about $8 with a frontier one. To break in: the “less than $3,000 in tokens” that Hacktron reports spending on the two-month project that chained an image-processing flaw to reach OpenAI’s internal code repository. To build a working browser exploit: the roughly $40,000 in API fees that XBOW reports for the six-day effort that produced a full-chain Chrome exploit, which Google later rewarded with its top bounty. These are only the automated parts of an attack: finding a crashing bug is easier than building a reliable weapon, and much of a real intrusion is still done by hand (see charts 4 and 9). The point is how small the numbers are: jobs that once needed scarce talent now cost from cents to tens of thousands of dollars, which is why the piece asks where the attacks are.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c00_lede_cost.py` (or `make figures` for everything)
- **Code:** [`charts/c00_lede_cost.py`](../charts/c00_lede_cost.py)
- **Results:** [`results/c00_lede_cost.json`](../results/c00_lede_cost.json)
- **Figure:** [`figures/c00_lede_cost.png`](../figures/c00_lede_cost.png) and [`figures/c00_lede_cost.svg`](../figures/c00_lede_cost.svg)
- **Data:** none of its own (every number is typed in the script and listed in [PARAMETERS](PARAMETERS.md))
- **Sources:** [bibliography page](sources/c00_lede_cost.md)
- **Checked:** 4 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 1: losses to fraud and hacking, and the part caused by AI

No one measures global cybercrime losses directly. Police, regulators, banks and blockchain analysts each publish a partial count, and most victims never report. The model therefore answers three separate questions.

- *How did losses change?* Twenty-three published loss series are treated as noisy views of a few underlying trends. They come from America’s FBI and Federal Trade Commission, UK Finance, Australia’s Scamwatch, Japan’s police, Canada’s Anti-Fraud Centre, Singapore’s and Hong Kong’s police, European banking regulators, the European Central Bank, Chainalysis, FinCEN, IBM, the Identity Theft Resource Center, Sophos and ransomware leak-site trackers. On a log scale, each series is allowed its own level, its own slow drift (because more victims learn to report to it, or because one country’s experience differs) and year-to-year noise; the shared trend is smooth. Fraud is modelled separately for America and for the rest of the world and then added up; hacking is one global trend. A change of definition starts a new series. All values are in 2025 prices. Before 2009 almost all the fraud data are American; the chart starts in 2015, when the hacking data begin.
- *How big are losses?* Every published series is a floor, so the 2025 level comes from a separate triangulation in the author’s earlier study: national statistics grossed up for under-reporting, bottom-up costings and two global surveys. It gives fraud losses of about $220bn and hacking losses of about $76bn, each uncertain by a factor of about two either way (90% intervals $105bn–461bn and $31bn–188bn). America is taken to account for about 42% of fraud losses, about $90bn in 2025. That sits between the Federal Trade Commission’s own two adjustments for under-reporting, $38bn (conservative) and $262bn (base case) for American consumer fraud of all kinds. The model’s trend is scaled to this level, so the chart’s level is only as good as the triangulation; its trend is better founded. Combining the two, the 2025 medians are $222bn for fraud and $74bn for hacking (80% credible intervals $123bn–390bn and $37bn–155bn), which the piece rounds to $220bn and $75bn.
- *Reporting that rises everywhere at once.* If more victims report each year in every country, every series rises faster than true losses, and the trend model cannot tell. So the model assumes that reporting rose by a modest common amount each year (2% a year for American complaint portals, 1% elsewhere and for hacking, each with its own uncertainty) and subtracts it. This lowers the estimated growth and widens the bands for early years.

*The AI share.* Loss statistics cannot detect a change of a few per cent, so the AI share is built from direct evidence. For 2025 it is the sum of two parts. The first is the share of dollars in complaints to the FBI that mention AI (about 4.2% of fraud dollars and 1.4% of hacking dollars), times the fraction of those losses that would not have happened without AI, since most are investment frauds of a kind that boomed before ChatGPT. The second is the share of losses where AI was used but victims could not tell (about a tenth for fraud, a fifth for hacking, based on Verizon’s finding that a tenth of malicious e-mail contains AI-written text and on IBM’s breach studies), times a small but-for fraction, because phishing’s success has not risen as AI-written text has spread. The but-for fractions are judgements, so the estimate averages three sets of them with equal weight: a central set (about a quarter of the noticed losses would not have happened without AI), a sceptical set (about a tenth) and a generous set (about half, with larger unnoticed shares). Each input is a probability distribution, not a point; 6,000 random draws give the result: about 1.6% of 2025 fraud losses (80% range 0.4–5.3%), 0.8% of hacking losses (0.2–3.8%) and 1.6% of all losses (0.5–4.5%), or about $5bn ($1.5bn–15bn). The chance that the share is below 5% is about 93%. Each figure is a separate median, so parts do not sum exactly to totals: the median total, about $308bn, exceeds the sum of the two medians, $296bn, because the distributions are skewed, and the chart’s title rounds it to $300bn. On the chart, each column stacks the median fraud and hacking estimates for one year, with the AI part in amber at the top (barely visible, because it is small), and the whisker is the 80% credible interval of the total. The grid on the right shows 2025 at $1bn a square: 296 squares in all, five amber for the central AI estimate and ten pale amber reaching the top of its 80% range. Earlier years are scaled down for lower adoption (2024 about half of 2025, 2023 about a quarter).

*The test the data can do.* The trend models were refitted on data up to 2022 and projected forward (this test is not drawn on the chart). Both fraud and hacking losses in 2025 came in below their pre-ChatGPT trends, by about 30% (80% intervals: fraud 0.4–1.1 times the projection, hacking 0.4–1.5 times), with probabilities of 84% for fraud and 74% for hacking. That is the opposite of what an AI-driven surge would produce, though it cannot rule out a small effect masked by other forces, such as banks’ new anti-scam controls. Growth comparisons in the text are computed draw by draw: hacking grew more slowly in 2022–25 than in 2017–22 with probability 96% (less than half as fast with probability 59%); fraud grew more slowly than in 2019–22 with probability 89%.

*Robustness.* The main finding, that growth slowed after 2022, survives changes to the assumptions: no common reporting drift, double the drift, and tighter or looser limits on how far a single series may drift. Across them, fraud losses grew by 12–17% a year in 2017–22 and by 8–11% a year in 2022–25; hacking losses grew by 22–25% a year, then by 9–11%. Two hacking indicators count incidents rather than dollars (breach notices multiplied by the average cost of a breach, and victims named on leak sites). Dropping them makes hacking losses roughly flat since 2022 (3% a year). The 2026 column is a projection, not an estimate from data: the dynamic-factor model’s own forecast carries each trend one year past 2025 (the machinery used for the pre-2022 check), and AI’s share is extended beyond 2025 by an adoption factor (median 1.4 times the 2025 share, 90% range 1.0 to 2.0). Its wider whisker reflects forecast uncertainty on top of the uncertainty about the level. The projection puts 2026 losses at about $340bn in total (80% range $210bn to $560bn), of which about $8bn, or 2.3%, caused by AI (80% range $2bn to $25bn).

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python models/c01_loss_trend.py`, then `python charts/c01_losses.py` (or `make all` for everything)
- **Code:** [`models/c01_loss_trend.py`](../models/c01_loss_trend.py), [`charts/c01_losses.py`](../charts/c01_losses.py), [`common/dfm.py`](../common/dfm.py), [`common/deflators.py`](../common/deflators.py)
- **Results:** [`results/c01_loss_trend.json`](../results/c01_loss_trend.json), [`results/sensitivity_c01.json`](../results/sensitivity_c01.json)
- **Figure:** [`figures/c01_losses.png`](../figures/c01_losses.png) and [`figures/c01_losses.svg`](../figures/c01_losses.svg)
- **Data:** [`data/A1_fraud_series.csv`](../data/A1_fraud_series.csv), [`data/A2_hacking_series.csv`](../data/A2_hacking_series.csv), [`data/A1_fraud_ai_evidence.csv`](../data/A1_fraud_ai_evidence.csv), [`data/A2_hacking_ai_evidence.csv`](../data/A2_hacking_ai_evidence.csv), [`data/cpi_u.csv`](../data/cpi_u.csv)
- **Sources:** [bibliography page](sources/c01_losses.md)
- **Robustness checks quoted above:** [`sensitivity/s01_loss_trend.py`](../sensitivity/s01_loss_trend.py)
- **Checked:** 61 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 2: what happens to criminal enterprises

The data are the histories of 152 named enterprises in ten sectors (grouped into six on the chart): ransomware brands, darknet markets, botnets and malware services, hacking and carding forums, laundering services and others. Each is classed by how it ended: by police (takedown, seizure, arrests or sanctions, or a shutdown that the operators or reporting tie to police pressure); by quitting, vanishing or rebranding for other reasons (retirement, exit scam, rebrand); or not at all (still running). The chart shows how the 132 that have closed came to an end, so that young sectors, such as ransomware brands, over a third of which are still running, are not counted against the police merely for being young. For each sector the share ended by police gets a flat prior, which the observed counts update (a beta-binomial model); the whisker is its 80% credible interval, taken as the narrowest such interval so that a sector in which police ended every closed enterprise (hacking forums) is not drawn outside its own interval. Police ended 74% of all closed enterprises (69–79%), but only 46% of closed ransomware brands (34–58%) and 48% of darknet markets (37–60%). A second calculation, not drawn, uses the 115 enterprises with known launch and end dates to estimate the share of all enterprises that police end within two, five and ten years of launch (about 21%, 40% and 65%; 80% intervals 16–26%, 34–46% and 59–72%), treating other endings as “competing risks”, which remove an enterprise from the chance of being ended by police. The 37 undated enterprises, 30 of them ended by police, are left out of it, so the piece does not rely on it. Enterprises famous enough to be documented are more often ones the police acted against, so these shares probably flatter the police.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c02_police.py` (or `make figures` for everything)
- **Code:** [`charts/c02_police.py`](../charts/c02_police.py), [`common/lifespans.py`](../common/lifespans.py)
- **Results:** [`results/c02_police.json`](../results/c02_police.json), [`results/sensitivity_c02.json`](../results/sensitivity_c02.json)
- **Figure:** [`figures/c02_police.png`](../figures/c02_police.png) and [`figures/c02_police.svg`](../figures/c02_police.svg)
- **Data:** [`data/B_enterprise_lifespans.csv`](../data/B_enterprise_lifespans.csv)
- **Robustness check (added after the post; not quoted above):** [`sensitivity/s02_police_selection.py`](../sensitivity/s02_police_selection.py)
- **Sources:** [bibliography page](sources/c02_police.md)
- **Checked:** 23 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 3: what crime pays

These are direct observations, not model estimates. Crime: leaked chats from the Conti gang (via Krebs on Security), Kaspersky’s study of job adverts on 155 dark-web forums in 2020–22, and the American indictment of LockBit’s alleged developer. The band shows the range of the adverts’ median pay by role, from $1,300 a month for designers to $4,000 for reverse engineers. The adverts were posted mostly on Russian-language forums, so the like-for-like comparison is with Russian developers at the same time: Habr Career’s medians for the first half of 2021, by level and take-home (junior 52,000 roubles a month, mid-level 120,000, senior 195,000, lead 230,000), converted at the World Bank’s 2021 average of 73.65 roubles to the dollar. Kaspersky itself found no significant difference between the median pay of IT workers in the criminal ecosystem and in the legitimate job market. Russian IT pay has since risen a little in dollars (Habr Career’s headline figure for 2025 is about $26,000 a year), which does not change the comparison. Other emerging economies, at their latest figures: DOU’s survey of Ukrainian developers (summer 2026, take-home; most Ukrainian developers work as low-tax contractors), Belstat’s average wage in Belarus’s information-and-communication sector (2025), China’s National Bureau of Statistics average wage in the IT sector (2025; privately owned firms at the low end of the range, and “non-private” units, meaning state-owned, listed, limited-liability and foreign-funded employers, including the big tech firms, at the high end), Brasscom’s figure, from Brazil’s employment registers, for systems-development analysts on formal contracts (December 2025), ITviec’s survey median for Vietnamese back-end developers (2025) and the Kolesa Group’s survey median for developers in Kazakhstan (2024). These cover developers of every level, juniors included, whereas the adverts probably seek experienced coders, so in the poorer countries an advert can look generous next to the median when it is closer to what an experienced developer earns there (in Vietnam, back-end developers with more than eight years’ experience earn a median of about $25,000). United States: the Bureau of Labor Statistics’ median wage for software developers (May 2025: $65.38 an hour, about $136,000 a year), and Levels.fyi’s self-reported median total pay, including stock, for software engineers, AI engineers and engineers at OpenAI and Anthropic. Figures are nominal US dollars a year at market exchange rates (annual averages). Survey medians, sector averages, pre-tax and take-home figures are not strictly comparable, and self-selected surveys probably lean towards better-paid workers. The title’s “a tenth” compares the median dark-web developer advert ($24,000) with American AI engineers’ median total pay ($250,000): 9.6%. “Emerging economies” rather than “middle-income countries” because the World Bank has classed Russia as high-income since 2024. Iran, also a source of malware, is left out for want of a reliable figure.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c03_talent.py` (or `make figures` for everything)
- **Code:** [`charts/c03_talent.py`](../charts/c03_talent.py)
- **Results:** [`results/c03_talent.json`](../results/c03_talent.json)
- **Figure:** [`figures/c03_talent.png`](../figures/c03_talent.png) and [`figures/c03_talent.svg`](../figures/c03_talent.svg)
- **Data:** [`data/C_pay.csv`](../data/C_pay.csv), [`data/C2_dev_pay_by_country.csv`](../data/C2_dev_pay_by_country.csv), [`data/F_pay.csv`](../data/F_pay.csv)
- **Sources:** [bibliography page](sources/c03_talent.md)
- **Checked:** 7 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 4: Amdahl’s law for a ransomware attack

A big ransomware attack is divided into eight stages, from getting in to laundering the proceeds. For each stage the author judged its share of the hours worked on one attack (mostly an affiliate’s) and the share of that work today’s best AI could do unaided, with ranges; the bars show the central judgements. The judgements draw on incident timelines (Colonial Pipeline, Ireland’s health service, Change Healthcare, MGM), leaked chats (Conti, Black Basta), British data on LockBit’s affiliates, timing statistics from Sophos, Mandiant, Coveware, GuidePoint, GreyNoise, Gambit Security and BakerHostetler, AI companies’ threat reports and the author’s earlier ransomware model. No public dataset measures criminals’ hours by stage, so these are judgements. Amdahl’s law then gives three numbers, each simulated 40,000 times with every input drawn from its range. The *ceiling*: if AI did all it could, instantly and without error, output per hour would rise by 1/(1 − P), where P is the AI-doable share of hours (about 39%, 80% range 31–47%, hence “about two-fifths”; the bars, which use the central judgements, add up to 36%), giving about +63% (80% range +44% to +89%), which the piece rounds to “about 60%, perhaps 45–90%”. The *likely* gain a gang should actually capture by the end of 2026 assumes that affiliates hand AI only part of that work (10–80%, deliberately wide because nobody knows), that AI does it 3–20 times faster rather than instantly, and that checking its work takes 10–40% as long as doing it by hand; the result is about +10% (+2% to +25%). The *future* estimate (quoted in the text, not plotted) assumes AI could also do every technical stage, giving roughly four times today’s output (3.3–6.1 times). The law caps how fast an attack’s workers go, not how many attacks there are.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c04_amdahl.py` (or `make figures` for everything)
- **Code:** [`charts/c04_amdahl.py`](../charts/c04_amdahl.py), [`common/bayes.py`](../common/bayes.py)
- **Results:** [`results/c04_amdahl.json`](../results/c04_amdahl.json)
- **Figure:** [`figures/c04_amdahl.png`](../figures/c04_amdahl.png) and [`figures/c04_amdahl.svg`](../figures/c04_amdahl.svg)
- **Data:** [`data/E_stage_judgements.csv`](../data/E_stage_judgements.csv), [`data/E_stage_times.csv`](../data/E_stage_times.csv), [`data/E_incident_timelines.csv`](../data/E_incident_timelines.csv), [`data/E_laundering.csv`](../data/E_laundering.csv), [`data/I_business_models.csv`](../data/I_business_models.csv)
- **Sources:** [bibliography page](sources/c04_amdahl.md)
- **Checked:** 12 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 5: how long abusers keep access to hosted AI

The data are AI providers’ disruption reports (Anthropic, OpenAI, Microsoft and Google) and security firms’ write-ups of related cases, 2023–26. The left panel includes every hacking, fraud or spying case in those reports whose AI provider cut it off and whose report states or bounds how long it ran: nine in all. OpenAI’s bans of scam rings are left out because “in the last three months” is a reporting window, not a duration; influence operations, a model-copying campaign and a ban at sign-up are also left out. Where a report gives only one bound, the other is assumed: Chinese state spies at most two months; the “vibe-hacking” extortionist at least a week (up to the month the report describes); the AI-built ransomware seller, active from January 2025 and banned by the time of Anthropic’s August report, six to seven and a half months. Each case’s true duration is treated as equally likely to be anywhere between its bounds (on a logarithmic scale). In each of 20,000 random draws the model counts the cases cut off within 30 days and those lasting 180 days or more, and combines the counts with a flat prior to estimate the shares among operations like these: about 41% cut off within a month (80% credible interval 22–62%) and 44% running six months or more (25–64%). These are shares of operations that were caught and disclosed, over a window of only about three years, so long-running recent operations are missing and true durations are probably longer. The right panel lists six operations that no AI provider stopped: three ran on self-hosted or local models or on access bought through a reseller, one was found by Amazon with no ban reported, one was caught but no ban was reported, and one (GhostGPT) is still on sale.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c05_inference.py` (or `make figures` for everything)
- **Code:** [`charts/c05_inference.py`](../charts/c05_inference.py)
- **Results:** [`results/c05_inference.json`](../results/c05_inference.json), [`results/sensitivity_c05.json`](../results/sensitivity_c05.json)
- **Figure:** [`figures/c05_inference.png`](../figures/c05_inference.png) and [`figures/c05_inference.svg`](../figures/c05_inference.svg)
- **Data:** [`data/D_platform_cases.csv`](../data/D_platform_cases.csv)
- **Robustness check (added after the post; not quoted above):** [`sensitivity/s05_provider_selection.py`](../sensitivity/s05_provider_selection.py)
- **Sources:** [bibliography page](sources/c05_inference.md)
- **Checked:** 7 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 6: how fast criminals adopt new technology

For each technique, the data give when the enabling technology or idea became available and when criminal use became widespread, defined case by case (for example, the dominant ransom currency, or about a tenth of malicious e-mail). Each technique is put in one of three classes: a ready-made exploit (a working attack handed to criminals, such as the leaked EternalBlue exploit or the Log4Shell flaw); a new tool, usable inside existing criminal work with no new market, payment system or infrastructure; or a new business model, which first needed one of those. Exploits and tools are kept apart because the two exploits were used within days or weeks while every tool took years, so one median would describe neither. The author assigned the classes knowing the outcomes, so the rule was then applied strictly: double extortion, which needed leak sites, counts as a business model; deepfake-voice fraud, which slots into existing impersonation fraud, as a new tool; hijacked-gadget botnets are dated from the spread of cheap, insecure internet-connected gadgets (about 2014), not from the Mirai code (2016). A browser-mining case whose dates could not be verified was dropped. Each class’s typical lag is estimated on a log scale, allowing for dates known only to the year. AI techniques that are not yet widespread enter as “at least this long so far” (right-censored): criminal chatbots and malware that calls AI models among new tools, and AI agents that run whole intrusions among business models. The two exploits are shown but not modelled. New tools took a median of about 3.9 years (80% credible interval 2.5–6.9); business models about 5.9 (3.7–9.2). If AI agents behave like past business-model innovations, the chance that they are widespread by the end of 2027, 2029 and 2031 is about 14%, 35% and 51% (a median around late 2031); if they spread like new tools, about 22%, 55% and 72%. These are chances given that agents running whole intrusions, around since early 2025, have not yet become widespread; chart 10 plots them year by year. Other defensible choices move these numbers: with the original classification the business-model median is 7.4 years and the chance by the end of 2029 is 21%; dating encrypt-and-ransom from the first criminal tool (2006) rather than the 1996 paper gives 5.3 years and 41%. The cases are well-known ones picked by hand, so these are illustrations of a pattern rather than calibrated forecasts.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c06_attacker_lag.py` (or `make figures` for everything)
- **Code:** [`charts/c06_attacker_lag.py`](../charts/c06_attacker_lag.py), [`common/bayes.py`](../common/bayes.py)
- **Results:** [`results/c06_attacker_lag.json`](../results/c06_attacker_lag.json), [`results/sensitivity_c06.json`](../results/sensitivity_c06.json)
- **Figure:** [`figures/c06_attacker_lag.png`](../figures/c06_attacker_lag.png) and [`figures/c06_attacker_lag.svg`](../figures/c06_attacker_lag.svg)
- **Data:** [`data/I_adoption_lags.csv`](../data/I_adoption_lags.csv)
- **Sources:** [bibliography page](sources/c06_attacker_lag.md)
- **Robustness checks quoted above:** [`sensitivity/s06_adoption_lags.py`](../sensitivity/s06_adoption_lags.py)
- **Checked:** 18 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 7: public versus private pay

For each country and side, typical pay is estimated from several noisy sources: advertised government pay scales and job adverts (NSA, GCHQ and Britain’s National Cyber Force and NCSC), an official Israeli wage report, a leaked salary sheet from i-Soon (a contractor to China’s security ministries) and Levels.fyi’s median pay for machine-learning and AI engineers. Each source is treated as a measurement of typical pay with an error that grows with poorer source quality, wider advertised ranges and a looser match to the job; the prior is deliberately vague, so the data decide. The private-to-state ratio is calculated draw by draw, so its interval reflects uncertainty on both sides: America 1.9 times (80% credible interval 0.9–3.7), Britain 2.3 (1.2–4.4), Israel 2.6 (1.3–4.9), China 8.4 (3.4–20). Israel’s state figures are averages for all army, Mossad and Shin Bet staff, not engineers; against Mossad and Shin Bet alone the ratio is about 1.7. China’s “state” figure is a contractor’s 2022 pay sheet, set against 2026 private pay. Pensions and job security, which narrow public–private gaps, are excluded. Russia and Iran publish nothing comparable.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c07_pay.py` (or `make figures` for everything)
- **Code:** [`charts/c07_pay.py`](../charts/c07_pay.py)
- **Results:** [`results/c07_pay.json`](../results/c07_pay.json), [`results/sensitivity_c07.json`](../results/sensitivity_c07.json)
- **Figure:** [`figures/c07_pay.png`](../figures/c07_pay.png) and [`figures/c07_pay.svg`](../figures/c07_pay.svg)
- **Data:** [`data/F_pay.csv`](../data/F_pay.csv)
- **Sources:** [bibliography page](sources/c07_pay.md)
- **Robustness checks quoted above:** [`sensitivity/s07_israel_state_pay.py`](../sensitivity/s07_israel_state_pay.py)
- **Checked:** 13 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 8: how far governments lag business

For each technology invented outside government (open-source software, smartphones, cloud computing, agile development, machine learning and generative AI), there is a range of years in which it became mainstream in American business and another for American defence and intelligence agencies; milestones differ by row (a policy memo, a big contract, a new organisation, user counts), and the business-side years for every technology except generative AI, and the agencies’ years for open source, are the author’s estimates. Two weakly sourced rows (personal computers, and corporate e-mail and the web) are left out. The smartphone row measures the iPhone, approved for Pentagon networks in 2013; the Pentagon already used about 470,000 BlackBerrys by then. The chart shows each range of years as a line, with a dot at its midpoint (cyan for business, purple for the agencies), and labels the gap between the midpoints; the lag is known only to lie between the two ranges, so the bracketed range runs from the earliest agency year minus the latest business year to the latest agency year minus the earliest business year. Past technologies took about four to nine years; generative AI about two. The Covid-era switch to video calls, made in weeks under emergency orders, is shown in grey and left out of the fit. The model fits a lag that can shrink or grow steadily over time (a regression on the year of business adoption, on a log scale, with interval-censored data). Because generative AI, the newest technology, carries much of the trend, the model is also fitted without it, and the projection averages the two fits. With it, the lag fell from about nine years in 2005 to about two in 2024 (80% credible interval 1.2–3.3); without it, from about seven to about four (1.7–8.0). The projection for AI agents in American offensive cyber operations takes business adoption as 2025–26, adds a lag drawn from each fit, keeps only dates after October 2026 (routine use has not yet begun), and averages the two: a median of mid-2028 (80% interval early 2027 to mid-2033), with a 72% chance of routine use by the end of 2029. That rests partly on the estimated years: dating open source’s agency adoption from the Pentagon’s October 2009 policy memo (2009–11) instead of 2012–14 removes the downward trend from the fit without generative AI and lowers the chance to 55% (median mid-2029). The army is already experimenting: a task force set up in April 2026 runs agent-based cyber-protection missions, and in October a partner of Army Cyber Command chose a firm to build offensive agents, though officials say no agent yet acts on its own.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c08_govlag.py` (or `make figures` for everything)
- **Code:** [`charts/c08_govlag.py`](../charts/c08_govlag.py), [`common/bayes.py`](../common/bayes.py)
- **Results:** [`results/c08_govlag.json`](../results/c08_govlag.json), [`results/sensitivity_c08.json`](../results/sensitivity_c08.json)
- **Figure:** [`figures/c08_govlag.png`](../figures/c08_govlag.png) and [`figures/c08_govlag.svg`](../figures/c08_govlag.svg)
- **Data:** [`data/G_adoption.csv`](../data/G_adoption.csv)
- **Sources:** [bibliography page](sources/c08_govlag.md)
- **Robustness checks quoted above:** [`sensitivity/s08_open_source_dating.py`](../sensitivity/s08_open_source_dating.py)
- **Checked:** 15 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 9: how long state hackers stay hidden

Not an estimate: every number is a reported date or count. Each bar is the time from a campaign’s first intrusion to its discovery, as the investigators give it. Kaspersky dates Equation Group to 2001 and Regin to 2003, and found them in 2015 and 2014 (14 and 11 years); it did not name the state behind either, though press reports link both to Western intelligence. For Volt Typhoon, American agencies said in February 2024 that Chinese hackers had held access to some victims’ networks for at least five years; because that is time in the network, not time to discovery, its bar ends in a hollow marker (†) and is a lower bound. The others come from official or victim reports: SolarWinds (first access in September 2019, discovered in December 2020; the White House counted about 100 companies and nine federal agencies compromised out of some 18,000 that installed the poisoned update), Mandiant’s average of 393 days for BRICKSTORM intrusions, the Office of Personnel Management breach (about 11 months), Midnight Blizzard’s break-in at Microsoft (late November 2023 to January 2024), the Ivanti zero-day exploitation (December 2023 to Volexity’s disclosure in January 2024) and Storm-0558’s theft of government e-mail (May to June 2023). The two grey bars are benchmarks from Mandiant’s M-Trends 2026: the median time to discovery in its 2025 investigations was 122 days for espionage and North Korean IT-worker cases together, and 14 days for all intrusions. The annotations give the number of victims actually worked: Equation Group infected tens of thousands of machines but Kaspersky saw more than 500 victims; Regin had 27 known victims in 14 countries. The campaigns are the ones later discovered and made public, so those still hidden are missing and famous ones are over-represented; the bars show what is possible, not how typical it is. Flame (dated only through Wikipedia) and Salt Typhoon (dwell time reported only at second hand) are left out.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c09_state_patience.py` (or `make figures` for everything)
- **Code:** [`charts/c09_state_patience.py`](../charts/c09_state_patience.py)
- **Results:** [`results/c09_state_patience.json`](../results/c09_state_patience.json), [`results/sensitivity_c09.json`](../results/sensitivity_c09.json)
- **Figure:** [`figures/c09_state_patience.png`](../figures/c09_state_patience.png) and [`figures/c09_state_patience.svg`](../figures/c09_state_patience.svg)
- **Data:** [`data/H_espionage_cases.csv`](../data/H_espionage_cases.csv), [`data/E_stage_times.csv`](../data/E_stage_times.csv)
- **Robustness check (added after the post; not quoted above):** [`sensitivity/s09_state_selection.py`](../sensitivity/s09_state_selection.py)
- **Sources:** [bibliography page](sources/c09_state_patience.md)
- **Checked:** every number is a reported date or count; those typed in the script are compared with the table by `tools/check_inputs.py`

</details>

### Chart 10: the odds, year by year, that AI agents become routine

This chart joins the adoption-lag models behind charts 6 and 8 and asks, for each date, how likely it is that AI agents running whole intrusions will by then be in routine use, given that they are not yet. *Criminals.* Chart 6 fits a distribution to the time from a technology’s arrival to widespread criminal use, separately for new tools and for new business models. Agents that run whole intrusions have existed since early 2025, 1.65 years before October 2026, without becoming widespread. For each draw from the fitted distribution, the chart takes the share of the lag distribution that lies between the time already elapsed and the date in question, divides it by the share that lies beyond the time already elapsed (which discards the part of the distribution that “not yet” has ruled out), and averages the result over all draws. The solid line treats agents as a new business model, the dashed line as a new tool, and the shaded band marks the range between them. *Agencies.* The curve for American defence and intelligence agencies uses the same posterior draws as chart 8: the lag between business and agency adoption, projected from the fit with all rows and from the fit without the generative-AI row, with business adoption of agents in 2025–26 and conditioned on agency adoption not having happened by October 2026. The purple line mixes the two fits equally; the band’s edges are the fits themselves. At the end of 2029 (the 2030 mark, since dates are the start of the year) the chances are: agencies 72% (89% on the fit with all rows, 58% without generative AI), which the text rounds to about 70%; criminals 35% if agents are a new business model and 55% if a new tool. The text’s “within one to three years” for agencies is the time to a 50% chance from October 2026: 0.8 years on the fit with all rows, 1.6 on the mix, 2.7 without generative AI; its “three to five” for crime is 2.8 years for the tool path and 5.0 for the business-model path. Both models rest on few, hand-picked cases, assume that past lags are a guide to this technology, and were fitted separately; read the numbers as rough.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c10_odds.py`; it reads the draws that Charts 6 and 8 save, so run those first (or `make figures`)
- **Code:** [`charts/c06_attacker_lag.py`](../charts/c06_attacker_lag.py), [`charts/c08_govlag.py`](../charts/c08_govlag.py), [`charts/c10_odds.py`](../charts/c10_odds.py), 
- **Results:** [`results/c10_odds.json`](../results/c10_odds.json)
- **Figure:** [`figures/c10_odds.png`](../figures/c10_odds.png) and [`figures/c10_odds.svg`](../figures/c10_odds.svg)
- **Data:** none of its own (it combines the posterior draws saved by Charts 6 and 8)
- **Sources:** those of [Chart 6](sources/c06_attacker_lag.md) and [Chart 8](sources/c08_govlag.md)
- **Checked:** 10 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 11: the defenders’ head start

Two estimates, both the author’s. Left panel, vendor adoption: a census of 34 of the largest security and platform vendors, each dated to its first substantive generative-AI security feature (a copilot or an autonomous agent, not the machine-learning detection most have used for years), from company announcements and trade press. A Monte Carlo allows for two uncertainties (whether a borderline feature really counts as substantive, and when it shipped) and reports, for each year, the cumulative number that had adopted, as a median and an 80% credible interval. In the census itself 19 of the 34 shipped their first feature in 2023, nine in 2024 and three in 2025; the simulation’s median count rises from 0 in 2022 to 18 in 2023 and 29 by 2026 (80% interval 27–31), lower than the raw census because some borderline features are discounted. Three vendors (Dropbox, Atlassian, 1Password) have shipped no security-specific generative-AI product and sit in the denominator. Right panel, spend: a judgement Monte Carlo (median and 80% range). Defensive spend is anchored to two market-research houses’ figures for the generative-AI cyber-defence market (about $16bn in 2025 and $20bn in 2026); attacker spend is a deliberately generous guess, since bespoke criminal tools proved thin wrappers or scams and most criminal use is of jailbroken mainstream models. The gap, roughly a thousandfold (80% range about 300 to 3,000), is order-of-magnitude, not a measurement.

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c11_defenders.py` (or `make figures` for everything)
- **Code:** [`charts/c11_defenders.py`](../charts/c11_defenders.py)
- **Results:** [`results/c11_defenders.json`](../results/c11_defenders.json)
- **Figure:** [`figures/c11_defenders.png`](../figures/c11_defenders.png) and [`figures/c11_defenders.svg`](../figures/c11_defenders.svg)
- **Data:** [`data/G_vendor_ai.csv`](../data/G_vendor_ai.csv)
- **Sources:** [bibliography page](sources/c11_defenders.md)
- **Checked:** 11 numbers quoted in this section are recomputed by `make verify`

</details>

### Chart 12: AI-found flaws

The funnel comes from Anthropic’s coordinated-disclosure dashboard (2 October 2026): 29,439 candidate findings, mostly not yet checked; 6,157 reported to the maintainers of 591 projects (of the 6,123 reviewed by outsiders, 5,674 were confirmed valid); 5,103 acknowledged; and 516 patched. Most reports are recent and maintainers usually get about 90 days, so the patched share will rise. The exploitation rate comes from VulnCheck’s tracker (28 July 2026): 14 of 1,061 AI-attributed vulnerabilities exploited in real attacks; the dot shows this observed share, 1.3%, and a flat prior gives an 80% credible interval of 1.0–1.9% (posterior median 1.4%). The comparison figure, about 1.4%, is VulnCheck’s ratio of flaws newly confirmed as exploited in the first half of 2026 to flaws newly published then. It is a rough benchmark, not a like-for-like rate: exploitation builds up over years, and over the long run about 6% of all published flaws have been exploited (Cyentia and FIRST’s EPSS study).

<details>
<summary><b>In the repository:</b> code, data, results and checks for this figure</summary>

- **Run:** `python charts/c12_funnel.py` (or `make figures` for everything)
- **Code:** [`charts/c12_funnel.py`](../charts/c12_funnel.py)
- **Results:** [`results/c12_funnel.json`](../results/c12_funnel.json)
- **Figure:** [`figures/c12_funnel.png`](../figures/c12_funnel.png) and [`figures/c12_funnel.svg`](../figures/c12_funnel.svg)
- **Data:** [`data/J_ai_vulns.csv`](../data/J_ai_vulns.csv)
- **Sources:** [bibliography page](sources/c12_funnel.md)
- **Checked:** 5 numbers quoted in this section are recomputed by `make verify`

</details>

### What these estimates cannot do

Most evidence on AI misuse comes from AI companies’ own reports, which are selective. Criminal and state operations that are never caught leave no trace in any of these data. Several inputs (chart 4’s stage shares, chart 6’s classification, chart 1’s but-for fractions) are judgements, and the forecasts in charts 8 and 10 rest on a handful of hand-picked precedents, one of which (generative AI) carries much of the trend. The estimates are best read as the author’s carefully stated bets, with the uncertainty shown, rather than as measurements.

## Notes on the wording above

Every number in the appendix is recomputed from the results files by `python tools/verify_numbers.py` (186 numbers, each in [`tests/appendix_a_numbers.csv`](../tests/appendix_a_numbers.csv) with the file and key it comes from and how it was rounded; `-v` prints them all). A handful are phrased more loosely than the stored result. The checker labels them CONSISTENT and says why; they are listed here so that nobody has to wonder.

- **Chart 1, robustness: "12-17% a year in 2017-22".** The 17 is the highest median across the variants (16.9%). The 12 is the mean-based figure from one variant (11.6%). On medians, as everywhere else in the appendix, the range is 11.1-16.9%, so "11-17%" would be the exact wording. The other three ranges in that sentence (8-11%, 22-25% and 9-11%) are medians and agree.
- **Chart 1, robustness: the ranges hide one variant.** The appendix gives ranges across the variants (fraud 12-17% a year, then 8-11%). Within each variant the slowdown is a different size: for fraud it is 4 to 9 points a year in four variants, and almost nothing in the fifth, where each series may drift only one point a year relative to the others (11.1% a year in 2017-22 and 10.7% in 2022-25). For hacking every variant shows a slowdown of at least 10 points. [MODELS](MODELS.md#robustness-checks) has the table.
- **Chart 1: "a fifth" of hacking losses with AI unnoticed** is the mean of the central set of judgements (20%); the median across the three sets is 21.6%. **"2023 about a quarter of 2025"** is the prior mean of the adoption index (0.25); the median of the fraud draws is 0.22. **"About 30% below" the pre-2022 trend** is the fraud figure (30%); the hacking median is 28% below.
- **Chart 8: "early 2027"** describes the lower end of the interval, 2027.1 (February).
- **Chart 9: BRICKSTORM's "393 days"** is Mandiant's figure. The table stores it as 1.08 years, which is 394 days.
- **Dates in the results files are the start of a year.** "By 2030" in a results file means by the end of 2029, so the appendix's "end of 2027, 2029 and 2031" for Chart 6 are the file's 2028, 2030 and 2032.
- **Rounding is half-up.** The variant in Chart 6 that dates encrypt-and-ransom from 2006 gives 0.405, printed as 41%; Python's own `round()` would print 40%.
- **Chart 2's intervals are highest-density intervals**, as the text says (stored as `police_share_of_closed_hdi80_pct`). The equal-tailed quantiles stored next to them (`police_share_of_ended_q`) are close for the middle sectors and up to four points lower at the bottom end for sectors where police ended nearly every closed enterprise.
- **Charts 8 and 10: "mixes the two fits equally".** The two fits' draws are pooled with equal weight and then conditioned on "not yet" (a date after October 2026). The condition keeps about 70% of the draws of the fit with all rows and 90% of those of the fit without generative AI, so afterwards the mixture is about 44% the first and 56% the second.
- **Charts 2, 5 and 9: how many missing cases it would take.** The appendix says these charts count only what was caught and that the shares probably flatter the police. Three checks added after the post was published put numbers on it. Police stop being the majority in Chart 2 at about 2.9 times the documentation rate of other closures (at least 64 other closures missing); "a large majority", read as two-thirds, goes at about 1.4. Two hidden quick catches would make most of Chart 5's cut-offs quick, while hidden long cases can only add to its long end; the nine cases also measure different things, and which are kept moves its shares by 17 to 24 points. Hidden campaigns cannot weaken Chart 9's "years", an existence claim that rests on three long cases (two of them Kaspersky's dating); it would fail only if they were overstated 2.5- to 7-fold. See [MODELS](MODELS.md#robustness-checks).
- **A few robustness results are not in the appendix.** `sensitivity/s06_adoption_lags.py` also reports what happens if hijacked-gadget botnets are dated from the first Mirai sighting (the table's own 0.1 years) rather than from about 2014 (2.3 years), and if AI-written phishing takes the lag implied by calendar years (1.6 years) rather than the table's 2.5; both are in [MODELS](MODELS.md#robustness-checks).
