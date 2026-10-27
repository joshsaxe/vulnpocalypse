# Chart 1: Losses to fraud and hacking, and the part caused by AI

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c01_losses.png`](../../figures/c01_losses.png) · code: [`charts/c01_losses.py`](../../charts/c01_losses.py)

Twenty-three loss series from police, regulators, banks, insurers, statisticians and security vendors (FBI IC3, the FTC's Consumer Sentinel, UK Finance, the Australian ACCC, Japan's National Police Agency, Chainalysis, IBM and Ponemon, Verizon, Sophos and others), pooled by a dynamic-factor model that corrects for drift in how losses are reported, and priced in 2025 dollars with US CPI-U from the Bureau of Labor Statistics (other countries' price indices are hand-entered in `common/deflators.py`; see [PARAMETERS](../PARAMETERS.md)). The two `evidence` tables hold what the AI share rests on: counts of complaints that mention AI, surveys of how many breaches or phishing e-mails involved AI, and police and vendor claims, each graded. The weakest part of the chart is that AI share: it is a judgement informed by this evidence, not a measurement (see [METHODS](../METHODS.md)).

**Tables behind this chart**

- [`data/A1_fraud_series.csv`](../../data/A1_fraud_series.csv): 590 rows; read by the chart's scripts.
- [`data/A2_hacking_series.csv`](../../data/A2_hacking_series.csv): 434 rows; read by the chart's scripts.
- [`data/cpi_u.csv`](../../data/cpi_u.csv): 21 rows; read by the chart's scripts.
- [`data/A1_fraud_ai_evidence.csv`](../../data/A1_fraud_ai_evidence.csv): 47 rows; typed numbers checked against it by `tools/check_inputs.py`.
- [`data/A2_hacking_ai_evidence.csv`](../../data/A2_hacking_ai_evidence.csv): 34 rows; typed numbers checked against it by `tools/check_inputs.py`.

**214 documents from 79 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**ACCC**

- [Targeting Scams 2019: a review of scam activity since 2009](https://www.accc.gov.au/system/files/1657RPT_Targeting%20scams%202019_FA.pdf) · 2020 · grade A — `A1_fraud_series` rows 487–491, 498–508: ACCC/NASC combined reported scam losses (2015–2019); Scamwatch reported scam losses (2009–2019)

**ACCC / NASC**

- [Targeting Scams report](https://www.accc.gov.au/system/files/Targeting%20scams%20-%20report%20of%20the%20ACCC%20on%20scams%20activity%202021.pdf) · 2022 · grade A — `A1_fraud_series` rows 493, 509, 510: ACCC/NASC combined reported scam losses (2021); Scamwatch reported scam losses (2020, 2021)

**ACCC / National Anti-Scam Centre**

- [Targeting Scams 2023 (foreword: '$3.15 billion reported in 2022')](https://www.nasc.gov.au/system/files/targeting-scams-report-2023.pdf) · 2024 · grade A — `A1_fraud_series` rows 494, 495, 511: ACCC/NASC combined reported scam losses (2022, 2023); Scamwatch reported scam losses (2022)
- [Targeting Scams report](https://www.nasc.gov.au/system/files/targeting-scams-report-2024.pdf) · 2025 · grade A — `A1_fraud_series` rows 492, 496, 512, 513: ACCC/NASC combined reported scam losses (2020, 2024); Scamwatch reported scam losses (2023, 2024); `A1_fraud_ai_evidence` row 44: Australia cut reported scam losses ~35% from 2022 peak while gen-AI spread
- [Targeting Scams 2025 (NASC)](https://www.nasc.gov.au/system/files/targeting-scams-report-2025.pdf) · 2026 · grade A — `A1_fraud_series` rows 497, 514: ACCC/NASC combined reported scam losses (2025); Scamwatch reported scam losses (2025); `A1_fraud_ai_evidence` row 39: Australia NASC 2025: AI cited as possible reason for falling Scamwatch reports

**Amazon Threat Intelligence**

- [AI-augmented threat actor accesses FortiGate devices at scale](https://aws.amazon.com/blogs/security/ai-augmented-threat-actor-accesses-fortigate-devices-at-scale/) · 2026-02-20 · grade C — `A2_hacking_ai_evidence` row 28: Amazon Feb 2026: AI-augmented actor compromised 600+ FortiGate devices in 55+ countries

**Anderson Economic Group**

- [Dealer Losses Due to CDK Cyberattack Reach $1.02 Billion](https://www.andersoneconomicgroup.com/dealer-losses-due-to-cdk-cyberattack-reach-1-02-billion/) · 2024-07-15 · grade B — `A2_hacking_series` row 316: US auto dealer direct losses from the CDK Global attack (2024)

**Anderson et al. (WEIS)**

- [Measuring the Changing Cost of Cybercrime (WEIS 2019)](https://weis2019.econinfosec.org/wp-content/uploads/sites/6/2019/05/WEIS_2019_paper_25.pdf) · 2019-06 · grade B — `A2_hacking_series` rows 0, 1: Generic cybercrime defence costs (Anderson et al.) (2018); Ransomware criminal revenue, cumulative 2015-2017 (as cited by Anderson et al.) (2015/2017)

**Anthropic**

- [Detecting and countering misuse of AI: August 2025 (report PDF)](https://www-cdn.anthropic.com/b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf) · 2025-08-27 · grade C — `A2_hacking_ai_evidence` rows 6, 7: Anthropic Aug 2025 (GTG-2002): one operator used Claude Code to run a data-theft and extortion…; Anthropic Aug 2025 (GTG-5004): UK-based actor selling AI-built ransomware-as-a-service packages
- [Disrupting the first reported AI-orchestrated cyber espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage) · 2025-11-13 · grade C — `A2_hacking_ai_evidence` row 8: Anthropic Nov 2025 (GTG-1002): suspected Chinese state-sponsored espionage campaign largely…
- [AI-enabled cyber threats mapped to MITRE ATT&CK](https://www.anthropic.com/research/AI-enabled-cyber-threats-mitre-attack) · 2026-06-03 · grade C — `A2_hacking_ai_evidence` row 14: Anthropic Jun 2026: 832 accounts banned for malicious cyber activity (Mar 2025-Mar 2026); 67.3%…
- [Detecting and countering misuse of AI: September 2026](https://www.anthropic.com/threat-intelligence-report-september-2026) · 2026-09-10 · grade C — `A2_hacking_ai_evidence` row 13: Anthropic Sept 2026 threat report: 'autonomous operating model has spread to every class of…

**bber.unm.edu**

- [BLS CPI-U annual averages (cross-checked UNM BBER table 245.1)](https://bber.unm.edu/data/cpi) · grade A — `cpi_u` rows 12–17: CPI-U annual averages (2017–2022)

**bls.gov**

- [BLS CPI-U annual averages](https://www.bls.gov/cpi/) · grade A — `cpi_u` rows 0–11: CPI-U annual averages (2005–2016)

**Canadian Anti-Fraud Centre (RCMP/OPP/Competition Bureau)**

- [CAFC 2021 Annual Report](https://antifraudcentre-centreantifraude.ca/annual-reports-2021-rapports-annuels-eng.htm) · 2022 · grade A — `A1_fraud_series` rows 537, 538: Canadian Anti-Fraud Centre reported fraud losses (2020, 2021)
- [CAFC 2022 Annual Report](https://antifraudcentre-centreantifraude.ca/annual-reports-2022-rapports-annuels-eng.htm) · 2023 · grade A — `A1_fraud_series` row 539: Canadian Anti-Fraud Centre reported fraud losses (2022)
- [CAFC 2024 Annual Statistical Report](https://open.canada.ca/data/dataset/69c68f22-8a2a-43d1-8f4e-4017e3ffebba/resource/1ffc4a5e-e41b-48c7-929e-633d023ef8dc/download/cafc-annual-stats-report-2024-en.pdf) · 2025 · grade A — `A1_fraud_series` row 541: Canadian Anti-Fraud Centre reported fraud losses (2024)
- [CAFC Top 10 frauds in 2025](https://antifraudcentre-centreantifraude.ca/features-vedette/2026/02/top-fraud-2025-fraudes-plus-courantes-eng.htm) · 2026 · grade A — `A1_fraud_series` row 542: Canadian Anti-Fraud Centre reported fraud losses (2025)

**Chainalysis**

- [Ransomware Payoffs Surge by 311% to Nearly $350 Million (Dark Reading on Chainalysis 2021 Crypto Crime Report)](https://www.darkreading.com/vulnerabilities---threats/ransomware-payoffs-surge-by-311--to-nearly-$350-million/d/d-id/1340017) · 2021-01-29 · grade B/C — `A2_hacking_series` rows 13, 14: Ransomware payments received on-chain (vintage published 2021-01-29) (2019, 2020)
- [Chainalysis 2021 Crypto Crime Report (PDF mirror)](https://www.gwern.net/doc/darknet-market/hydra/2021-chainanalysis.pdf) · 2021-02 · grade B — `A2_hacking_series` row 28: Crypto stolen in hacks (2020)
- [2022 Crypto Crime Report (derived)](https://www.chainalysis.com/blog/2022-crypto-crime-report-introduction/) · 2022 · grade B — `A1_fraud_series` rows 562, 564: Chainalysis crypto scam revenue (value received by scam addresses) (2020, 2021); `A2_hacking_series` row 29: Crypto stolen in hacks (2021)
- [2022 Crypto Crime Report preview: ransomware](https://www.chainalysis.com/blog/2022-crypto-crime-report-preview-ransomware/) · 2022-02-10 · grade B — `A2_hacking_series` rows 15, 16: Ransomware payments received on-chain (vintage published 2022-02-10) (2020, 2021)
- [2023 Crypto Crime Report: scams](https://www.chainalysis.com/blog/2022-crypto-scam-revenue/) · 2023 · grade B — `A1_fraud_series` rows 565, 566: Chainalysis crypto scam revenue (value received by scam addresses) (2021, 2022)
- [Chainalysis: Ransomware payments down, fewer victims paying (TechTarget report of Chainalysis 2023 Crypto Crime Report)](https://www.techtarget.com/cybersecurity/news/252529391/Chainalysis-Ransomware-payments-down-fewer-victims-paying) · 2023-01-19 · grade B — `A2_hacking_series` rows 7, 17: Ransomware payments received on-chain (2020); Ransomware payments received on-chain (vintage published 2023-01-19) (2020)
- [Chainalysis crypto hacking report](https://www.chainalysis.com/blog/2022-biggest-year-ever-for-crypto-hacking/) · 2023-02-01 · grade B — `A2_hacking_series` row 2: Crypto stolen by DPRK-attributed actors (2022)
- [2024 Crypto Crime Report introduction](https://www.chainalysis.com/blog/2024-crypto-crime-report-introduction/) · 2024 — `A1_fraud_series` row 563: Chainalysis crypto scam revenue (value received by scam addresses) (2023)
- [Crypto hacking stolen funds 2024 (2024 Crypto Crime Report)](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2024/) · 2024-01-24 · grade B — `A2_hacking_series` rows 30, 31: Crypto stolen in hacks (2022, 2023)
- [Chainalysis: 2023 a watershed year for ransomware (TechTarget)](https://www.techtarget.com/cybersecurity/news/366569197/Chainalysis-2023-a-watershed-year-for-ransomware) · 2024-02-07 · grade B — `A2_hacking_series` rows 8, 20, 22: Ransomware payments received on-chain (2021); Ransomware payments received on-chain (vintage published 2024-02-07) (2021, 2023)
- [Ransomware Payments Exceed $1 Billion in 2023](https://www.chainalysis.com/blog/ransomware-2024/) · 2024-02-07 · grade B — `A2_hacking_series` rows 9, 21: Ransomware payments received on-chain (2022); Ransomware payments received on-chain (vintage published 2024-02-07) (2022)
- [Chainalysis crypto hacking report](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2025/) · 2024-12-19 · grade B — `A2_hacking_series` rows 3, 4, 27, 32: Crypto stolen by DPRK-attributed actors (2023, 2024); Crypto stolen in hacks (2018, 2024)
- [2025 Crypto Crime Report: pig butchering](https://www.chainalysis.com/blog/2024-pig-butchering-scam-revenue-grows-yoy/) · 2025 · grade B — `A1_fraud_series` row 567: Chainalysis crypto scam revenue (value received by scam addresses) (2024); `A1_fraud_ai_evidence` row 20: Revenue of AI service vendors on Huione Guarantee grew ~1,900% (CAGR 2021-2024)
- [Ransomware revenue down as victims refuse to pay](https://www.chainalysis.com/blog/crypto-crime-ransomware-victim-extortion-2025/) · 2025-02-05 · grade B — `A2_hacking_series` rows 10, 23, 24: Ransomware payments received on-chain (2023); Ransomware payments received on-chain (vintage published 2025-02-05) (2023, 2024)
- [2025 Crypto Crime Mid-year Update](https://www.chainalysis.com/blog/2025-crypto-crime-mid-year-update/) · 2025-07-17 · grade B/C — `A2_hacking_series` row 34: Crypto stolen from services, first half (2025); `A2_hacking_ai_evidence` row 5: Chainalysis mid-2025: individual-targeting crypto theft 'potentially facilitated by' LLM tools
- [Chainalysis crypto hacking report](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2026/) · 2025-12-18 · grade B — `A2_hacking_series` rows 5, 33: Crypto stolen by DPRK-attributed actors (2025); Crypto stolen in hacks (2025)
- [2026 Crypto Crime Report: scams](https://www.chainalysis.com/blog/crypto-scams-2026/) · 2026 · grade B — `A1_fraud_series` rows 568–570: Chainalysis crypto scam revenue (value received by scam addresses) (2024, 2025); `A1_fraud_ai_evidence` row 18: Scams with on-chain links to AI vendors earn more per operation
- [Crypto ransomware 2026](https://www.chainalysis.com/blog/crypto-ransomware-2026/) · 2026-02-26 · grade B — `A2_hacking_series` rows 11, 12, 25, 26: Ransomware payments received on-chain (2024, 2025); Ransomware payments received on-chain (vintage published 2026-02-26) (2024, 2025); `A2_hacking_ai_evidence` row 4: Chainalysis 2026: ransomware payments fell 8% in 2025 while claimed victims rose ~50%
- [How AI Helped Chainalysis Investigators Trace the $387 Million North Korea Stole from Bitget](https://www.chainalysis.com/blog/387m-bitget-theft-2026/) · 2026-10-01 · grade B — `A2_hacking_series` rows 6, 314: Crypto stolen by DPRK-attributed actors, 2026 year to date (lower bound) (2026); Bitget exchange theft (DPRK) (2026)

**Chainalysis via Decrypt**

- [2026 Crypto Crime Report: crypto scams (Chainalysis); Decrypt summary](https://decrypt.co/354624/ai-impersonation-drove-crypto-scam-losses-record-17-billion-2025-chainalysis) · 2026 · grade C — `A1_fraud_ai_evidence` row 19: Impersonation crypto scams grew \>1,400% in 2025, 'driven in part by AI tools'

**CNN; WEF (2025-02-04)**

- [Finance worker pays out $25 million after deepfake video call / Arup CIO interview](https://edition.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk) · 2024-05-16 · grade B — `A1_fraud_ai_evidence` row 14: Arup deepfake video-conference fraud (Hong Kong)

**Competition Bureau Canada**

- [Fraud Prevention Month to bring hidden crime into the spotlight](https://www.canada.ca/en/competition-bureau/news/2026/03/fraud-prevention-month-to-bring-hidden-crime-into-the-spotlight.html) · 2026 · grade C — `A1_fraud_ai_evidence` row 37: Canada Competition Bureau: 'AI has armed fraudsters with powerful tools'

**Coveware by Veeam**

- [Coveware's 2018 Q4 Ransomware Marketplace Report](https://coveware.com/2019/01/covewares-2018-q4-ransomware-marketplace-report/) · 2019-01-22 · grade C — `A2_hacking_series` row 35: Average ransom payment, 2018Q3 (2018-07/2018-09)
- [Ransom amounts rise 90% in Q1 as Ryuk increases](https://coveware.com/2019/04/ransom-amounts-rise-90-in-q1-as-ryuk-ransomware-increases/) · 2019-04-16 · grade C — `A2_hacking_series` rows 36, 37, 79: Average ransom payment, 2018Q4 (2018-10/2018-12); Average ransom payment, 2019Q1 (2019-01/2019-03); Share of ransomware/extortion victims that paid, 2019Q1 (2019-01/2019-03)
- [Ransomware Payments Rise as Public Sector is Targeted](https://coveware.com/2019/11/q3-ransomware-marketplace-report/) · 2019-11-01 · grade C — `A2_hacking_series` rows 38, 39: Average ransom payment, 2019Q2 (2019-04/2019-06); Average ransom payment, 2019Q3 (2019-07/2019-09)
- [Ransomware Costs Double in Q4 as Ryuk, Sodinokibi Proliferate](https://coveware.com/2020/01/ransomware-costs-double-in-q4-as-ryuk-sodinokibi-proliferate/) · 2020-01-23 · grade C — `A2_hacking_series` rows 40, 60: Average ransom payment, 2019Q4 (2019-10/2019-12); Median ransom payment, 2019Q4 (2019-10/2019-12)
- [Ransomware Payments Up 33% As Maze and Sodinokibi Proliferate in Q1 2020](https://coveware.com/2020/04/q1-2020-ransomware-marketplace-report/) · 2020-04-29 · grade C — `A2_hacking_series` rows 41, 61: Average ransom payment, 2020Q1 (2020-01/2020-03); Median ransom payment, 2020Q1 (2020-01/2020-03)
- [Ransomware Attacks Fracture Between Enterprise and RaaS in Q2 as Demands Increase](https://coveware.com/2020/08/q2-2020-ransomware-marketplace-report/) · 2020-08-03 · grade C — `A2_hacking_series` rows 42, 62: Average ransom payment, 2020Q2 (2020-04/2020-06); Median ransom payment, 2020Q2 (2020-04/2020-06)
- [Ransomware Demands continue to rise as Data Exfiltration becomes common](https://coveware.com/2020/11/q3-2020-ransomware-marketplace-report/) · 2020-11-04 · grade C — `A2_hacking_series` rows 43, 63: Average ransom payment, 2020Q3 (2020-07/2020-09); Median ransom payment, 2020Q3 (2020-07/2020-09)
- [Ransomware Payments Fall as Fewer Companies Pay Data Exfiltration Extortion Demands](https://coveware.com/2021/02/ransomware-marketplace-report-q4-2020/) · 2021-02-01 · grade C — `A2_hacking_series` rows 44, 64: Average ransom payment, 2020Q4 (2020-10/2020-12); Median ransom payment, 2020Q4 (2020-10/2020-12)
- [Ransomware Attack Vectors Shift as New Software Vulnerability Exploits Abound](https://coveware.com/2021/04/ransomware-attack-vectors-shift-as-new-software-vulnerability-exploits-abound/) · 2021-04-26 · grade C — `A2_hacking_series` rows 45, 65: Average ransom payment, 2021Q1 (2021-01/2021-03); Median ransom payment, 2021Q1 (2021-01/2021-03)
- [Ransomware attackers down shift to 'Mid-Game' hunting in Q3 2021](https://coveware.com/2021/10/ransomware-attacks-continue-as-pressure-mounts/) · 2021-10-21 · grade C — `A2_hacking_series` rows 46, 66: Average ransom payment, 2021Q3 (2021-07/2021-09); Median ransom payment, 2021Q3 (2021-07/2021-09)
- [Law enforcement pressure forces ransomware groups to refine tactics in Q4 2021](https://coveware.com/2022/02/law-enforcement-pressure-forces-ransomware-groups-to-refine-tactics-in-q4-2021/) · 2022-02-03 · grade C — `A2_hacking_series` rows 47, 67: Average ransom payment, 2021Q4 (2021-10/2021-12); Median ransom payment, 2021Q4 (2021-10/2021-12)
- [Uber Verdict Raises New Risks for Ransom Payments](https://coveware.com/2022/10/q3-2022-quarterly-report/) · 2022-10-26 · grade C — `A2_hacking_series` rows 48, 68: Average ransom payment, 2022Q3 (2022-07/2022-09); Median ransom payment, 2022Q3 (2022-07/2022-09)
- [Ransomware Revenue Plunges in 2022 as Victims Refuse to Pay (Chainalysis citing Coveware)](https://www.chainalysis.com/blog/crypto-ransomware-revenue-down-as-victims-refuse-to-pay/) · 2023-01-19 · grade B/C — `A2_hacking_series` rows 18, 19, 90–92: Ransomware payments received on-chain (vintage published 2023-01-19) (2021, 2022); Share of victims that paid, full year (2020–2022)
- [Improved Security and Backups Result in Record Low Number of Ransomware Payments](https://coveware.com/2023/01/improved-security-and-backups-result-in-record-low-number-of-ransomware-payments/) · 2023-01-20 · grade C — `A2_hacking_series` rows 49, 69, 80, 89: Average ransom payment, 2022Q4 (2022-10/2022-12); Median ransom payment, 2022Q4 (2022-10/2022-12); Share of ransomware/extortion victims that paid, 2022Q4 (2022-10/2022-12); and 1 more
- [Ransom Monetization Rates Fall to Record Low Despite Jump In Average Ransom Payments](https://coveware.com/2023/07/ransom-monetization-rates-fall-to-record-low-despite-jump-in-average-ransom-payments/) · 2023-07-21 · grade C — `A2_hacking_series` rows 50, 70, 81: Average ransom payment, 2023Q2 (2023-04/2023-06); Median ransom payment, 2023Q2 (2023-04/2023-06); Share of ransomware/extortion victims that paid, 2023Q2 (2023-04/2023-06)
- [New Ransomware Reporting Requirements Kick in as Victims Increasingly Avoid Paying](https://coveware.com/2024/01/new-ransomware-reporting-requirements-kick-in-as-victims-increasingly-avoid-paying/) · 2024-01-26 · grade C — `A2_hacking_series` rows 51, 71, 82: Average ransom payment, 2023Q4 (2023-10/2023-12); Median ransom payment, 2023Q4 (2023-10/2023-12); Share of ransomware/extortion victims that paid, 2023Q4 (2023-10/2023-12)
- [Law enforcement doxxing raises risk profile for threat actors](https://coveware.com/2024/11/law-enforcement-doxxing-raises-risk-profile-for-threat-actors/) · 2024-11-01 · grade C — `A2_hacking_series` rows 52, 72, 83: Average ransom payment, 2024Q3 (2024-07/2024-09); Median ransom payment, 2024Q3 (2024-07/2024-09); Share of ransomware/extortion victims that paid, 2024Q3 (2024-07/2024-09)
- [Will Law Enforcement success against ransomware continue in 2025?](https://coveware.com/2025/02/q4-report/) · 2025-02-04 · grade C — `A2_hacking_series` rows 53, 73, 84: Average ransom payment, 2024Q4 (2024-10/2024-12); Median ransom payment, 2024Q4 (2024-10/2024-12); Share of ransomware/extortion victims that paid, 2024Q4 (2024-10/2024-12)
- [Targeted social engineering is en vogue as ransom payment sizes increase](https://coveware.com/2025/07/targeted-social-engineering-is-en-vogue-as-ransom-payment-sizes-increase/) · 2025-07-23 · grade C — `A2_hacking_series` rows 54, 74, 85: Average ransom payment, 2025Q2 (2025-04/2025-06); Median ransom payment, 2025Q2 (2025-04/2025-06); Share of ransomware/extortion victims that paid, 2025Q2 (2025-04/2025-06)
- [Insider Threats Loom while Ransom Payment Rates Plummet](https://coveware.com/2025/10/insider-threats-loom-while-ransom-payment-rates-plummet/) · 2025-10-24 · grade C — `A2_hacking_series` rows 55, 75, 86: Average ransom payment, 2025Q3 (2025-07/2025-09); Median ransom payment, 2025Q3 (2025-07/2025-09); Share of ransomware/extortion victims that paid, 2025Q3 (2025-07/2025-09)
- [Why Zero-Day Downstream Mass Data Extortion Campaigns are Losing Their Bite](https://coveware.com/2026/02/why-zero-day-downstream-mass-data-extortion-campaigns-are-losing-their-bite/) · 2026-02-03 · grade C — `A2_hacking_series` rows 56, 76, 87: Average ransom payment, 2025Q4 (2025-10/2025-12); Median ransom payment, 2025Q4 (2025-10/2025-12); Share of ransomware/extortion victims that paid, 2025Q4 (2025-10/2025-12)
- [Patch management goes from hard, to ludicrous in the agentic AI era](https://coveware.com/2026/04/patch-management-goes-from-hard-to-ludicrous-in-the-agentic-ai-era/) · 2026-04-30 · grade C — `A2_hacking_series` rows 57, 77, 88: Average ransom payment, 2026Q1 (2026-01/2026-03); Median ransom payment, 2026Q1 (2026-01/2026-03); Share of ransomware/extortion victims that paid, 2026Q1 (2026-01/2026-03)
- [Adverse cyber extortions are more common than commonly advised](https://coveware.com/2026/07/adverse-cyber-extortions-are-more-common-than-commonly-advised/) · 2026-07-29 · grade C — `A2_hacking_series` rows 58, 59, 78: Average ransom payment, 2026Q2 (2026-04/2026-06); Share of data-exfiltration-only extortion victims that paid, Q2 2026 (2026-04/2026-06); Median ransom payment, 2026Q2 (2026-04/2026-06)

**CrowdStrike**

- [2026 CrowdStrike Global Threat Report (findings blog)](https://www.crowdstrike.com/en-us/blog/crowdstrike-2026-global-threat-report-findings/) · 2026-02-24 · grade C — `A2_hacking_ai_evidence` row 20: CrowdStrike 2026 Global Threat Report: operations by 'AI-enabled adversaries' up 89% y/y
- [Unknown Threat Actor Uses AI-Driven ARTEX to Target South Korean Finance](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/) · 2026-10-07 · grade B — `A2_hacking_ai_evidence` row 25: CrowdStrike Oct 2026 (ARTEX): AI pentest agent used against several South Korean lenders; data…

**CSIS / McAfee**

- [Economic Impact of Cybercrime (CSIS, 2018) quoting 2014 study](https://www.csis.org/analysis/economic-impact-cybercrime) · 2018-02-21 · grade C — `A2_hacking_series` rows 115, 116: CSIS/McAfee global cost of cybercrime (2014 study) (2014); CSIS/McAfee global cost of cybercrime (2018 study) (2017)

**Cyber Monitoring Centre (UK)**

- [Cyber Monitoring Centre statement on ransomware incidents in the retail sector (June 2025)](https://cybermonitoringcentre.com/2025/06/20/cyber-monitoring-centre-statement-on-ransomware-incidents-in-the-retail-sector-june-2025/) · 2025-06-20 · grade B — `A2_hacking_series` row 320: UK economic cost of the M&S and Co-op ransomware incidents (CMC midpoint) (2025)
- [Cyber Monitoring Centre Statement on the Jaguar Land Rover Cyber Incident (October 2025)](https://cybermonitoringcentre.com/2025/10/22/cyber-monitoring-centre-statement-on-the-jaguar-land-rovercyber-incident-october-2025/) · 2025-10-22 · grade B — `A2_hacking_series` row 318: UK economic cost of the Jaguar Land Rover cyber incident (CMC central) (2025)

**Cybersecurity Ventures**

- [Cybercrime To Cost The World $10.5 Trillion Annually By 2025](https://cybersecurityventures.com/official-cybercrime-report-2025/) · 2020-11-13 · grade D — `A2_hacking_series` row 117: Cybersecurity Ventures 'cost of cybercrime' projection (2025)

**Deloitte**

- [Generative AI is expected to magnify the risk of deepfakes and other fraud in banking (Deloitte Center for Financial Services)](https://www.deloitte.com/us/en/insights/industry/financial-services/deepfake-banking-fraud-risk-on-the-rise.html) · 2024-05-29 · grade C — `A1_fraud_ai_evidence` row 13: Deloitte projects gen-AI could enable US fraud losses of $40bn by 2027

**EBA and ECB**

- [EBA/ECB 2024 Report on Payment Fraud](https://www.ecb.europa.eu/press/intro/publications/pdf/ecb.ebaecb202408.en.pdf) · 2024 · grade A — `A1_fraud_series` row 556: Value of fraudulent payment transactions (all instruments) (2022)
- [EBA/ECB 2025 Report on Payment Fraud](https://www.eba.europa.eu/sites/default/files/2025-12/1709846a-84d9-47cf-86a0-b155efb34d66/EBA%20and%20ECB%20Report%20on%20Payment%20Fraud.pdf) · 2025 · grade A — `A1_fraud_series` rows 557, 584: Value of fraudulent payment transactions (all instruments) (2023, 2024)

**Elliptic**

- [Tudou Guarantee winds down operations after $12 billion in transactions (Elliptic)](https://www.elliptic.co/insights/tudou-guarantee-winds-down-operations-after-12-billion-in-transactions/) · 2026-01-19 · grade C — `A1_fraud_ai_evidence` row 21: Guarantee marketplaces sell face-swap, AI voice cloning and deepfake tools

**ENISA**

- [ENISA Threat Landscape 2025 (v1.3)](https://www.enisa.europa.eu/sites/default/files/2026-09/ENISA%20Threat%20Landscape%202025_v1.3_September2026_0.pdf) · 2025-10 · grade C — `A2_hacking_ai_evidence` row 23: ENISA Threat Landscape 2025: 'more than 80%' of social-engineering activity AI-supported

**Entrust**

- [2026 Identity Fraud Report (Entrust)](https://www.entrust.com/resources/reports/identity-fraud-report) · 2025 · grade C — `A1_fraud_ai_evidence` row 31: Deepfakes account for 1 in 5 biometric fraud attempts

**European Central Bank**

- [ECB Card Fraud Report](https://www.ecb.europa.eu/pub/cardfraud/html/index.en.html) · grade A — `A1_fraud_series` rows 558–561: Value of card fraud on SEPA-issued cards (2013, 2016, 2018, 2019)

**FBI IC3**

- [IC3 2011 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2011_IC3Report.pdf) · 2012 · grade A — `A1_fraud_series` row 7: IC3 reported losses, all complaints (2011)
- [IC3 2012 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2012_IC3Report.pdf) · 2013 · grade A — `A1_fraud_series` row 8: IC3 reported losses, all complaints (2012)
- [FBI Internet Crime Complaint Center 2013 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2013_IC3Report.pdf) · 2014 · grade A — `A1_fraud_series` row 9: IC3 reported losses, all complaints (2013); `A2_hacking_series` rows 267, 284–292, 300, 301: Ransomware/scareware scam losses reported to IC3 (2013); Total complaints received by IC3 (context) (2005–2013); Total losses reported to IC3, all crime types (context) (2012, 2013)
- [FBI Internet Crime Complaint Center 2014 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2014_IC3Report.pdf) · 2015 · grade A — `A1_fraud_series` row 10: IC3 reported losses, all complaints (2014); `A2_hacking_series` rows 134, 150, 162, 170, 215, 221, 244, 255, 268, 293, 302: Business email compromise losses reported to IC3 (context; fraud) (2014); Corporate data breach losses reported to IC3 (2014); Denial of service / TDoS losses reported to IC3 (2014); and 8 more
- [IC3 2015 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2015_IC3Report.pdf) · 2016 · grade A — `A1_fraud_series` rows 11, 27–30, 71–105: IC3 reported losses, all complaints (2015); IC3 losses in fraud-type crime categories (derived sum) (2015); IC3 losses in hacking-type crime categories (derived sum) (2015); and 37 more; `A2_hacking_series` rows 135, 151, 163, 171, 182, 193, 204, 216, 222, 233, 245, 256, 269: Business email compromise losses reported to IC3 (context; fraud) (2015); Corporate data breach losses reported to IC3 (2015); Denial of service / TDoS losses reported to IC3 (2015); and 10 more
- [IC3 2016 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2016_IC3Report.pdf) · 2017 · grade A — `A1_fraud_series` rows 12, 31–34, 106–139: IC3 reported losses, all complaints (2016); IC3 losses in fraud-type crime categories (derived sum) (2016); IC3 losses in hacking-type crime categories (derived sum) (2016); and 36 more; `A2_hacking_series` rows 136, 152, 164, 172, 183, 194, 205, 217, 223, 234, 257, 270: Business email compromise losses reported to IC3 (context; fraud) (2016); Corporate data breach losses reported to IC3 (2016); Denial of service / TDoS losses reported to IC3 (2016); and 9 more
- [IC3 2017 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2017_IC3Report.pdf) · 2018 · grade A — `A1_fraud_series` rows 13, 35–38, 140–172: IC3 reported losses, all complaints (2017); IC3 losses in fraud-type crime categories (derived sum) (2017); IC3 losses in hacking-type crime categories (derived sum) (2017); and 35 more; `A2_hacking_series` rows 137, 153, 165, 173, 184, 195, 206, 218, 224, 235, 246, 258, 271: Business email compromise losses reported to IC3 (context; fraud) (2017); Corporate data breach losses reported to IC3 (2017); Denial of service / TDoS losses reported to IC3 (2017); and 10 more
- [IC3 2018 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2018_IC3Report.pdf) · 2019 · grade A — `A1_fraud_series` rows 14, 22, 39–42, 173–206: IC3 reported losses, all complaints (2018); IC3 reported losses, later-vintage value (2016); IC3 losses in fraud-type crime categories (derived sum) (2018); and 37 more; `A2_hacking_series` rows 138, 154, 166, 174, 185, 196, 207, 219, 225, 236, 247, 259, 272: Business email compromise losses reported to IC3 (context; fraud) (2018); Corporate data breach losses reported to IC3 (2018); Denial of service / TDoS losses reported to IC3 (2018); and 10 more
- [IC3 2019 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2019_IC3Report.pdf) · 2020 · grade A — `A1_fraud_series` rows 15, 43–46, 207–239: IC3 reported losses, all complaints (2019); IC3 losses in fraud-type crime categories (derived sum) (2019); IC3 losses in hacking-type crime categories (derived sum) (2019); and 35 more; `A2_hacking_series` rows 139, 155, 167, 175, 186, 197, 208, 220, 226, 237, 248, 260, 273, 294–298, 303, 304: Business email compromise losses reported to IC3 (context; fraud) (2019); Corporate data breach losses reported to IC3 (2019); Denial of service / TDoS losses reported to IC3 (2019); and 12 more
- [IC3 2020 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2020_IC3Report.pdf) · 2021 · grade A — `A1_fraud_series` rows 16, 47–50, 240–272: IC3 reported losses, all complaints (2020); IC3 losses in fraud-type crime categories (derived sum) (2020); IC3 losses in hacking-type crime categories (derived sum) (2020); and 35 more; `A2_hacking_series` rows 140, 156, 168, 176, 187, 198, 209, 227, 238, 249, 261, 274: Business email compromise losses reported to IC3 (context; fraud) (2020); Corporate data breach losses reported to IC3 (2020); Denial of service / TDoS losses reported to IC3 (2020); and 9 more
- [IC3 2021 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2021_IC3Report.pdf) · 2022 · grade A — `A1_fraud_series` rows 17, 51–54, 273–302: IC3 reported losses, all complaints (2021); IC3 losses in fraud-type crime categories (derived sum) (2021); IC3 losses in hacking-type crime categories (derived sum) (2021); and 32 more; `A2_hacking_series` rows 141, 157, 169, 177, 188, 199, 210, 228, 239, 250, 262, 275, 305, 306: Business email compromise losses reported to IC3 (context; fraud) (2021); Corporate data breach losses reported to IC3 (2021); Denial of service / TDoS losses reported to IC3 (2021); and 10 more
- [IC3 2022 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2022_IC3Report.pdf) · 2023 · grade A — `A1_fraud_series` rows 18, 55–58, 303–329, 408, 409, 413, 414: IC3 reported losses, all complaints (2022); IC3 losses in fraud-type crime categories (derived sum) (2022); IC3 losses in hacking-type crime categories (derived sum) (2022); and 31 more; `A2_hacking_series` rows 142, 146, 158, 178, 189, 200, 211, 229, 240, 251, 263, 276, 280: Business email compromise losses reported to IC3 (context; fraud) (2022); Botnet losses reported to IC3 (2022); Corporate data breach losses reported to IC3 (2022); and 10 more
- [IC3 2023 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2023_IC3Report.pdf) · 2024 · grade A — `A1_fraud_series` rows 19, 59–62, 330–355, 410, 415: IC3 reported losses, all complaints (2023); IC3 losses in fraud-type crime categories (derived sum) (2023); IC3 losses in hacking-type crime categories (derived sum) (2023); and 30 more; `A2_hacking_series` rows 143, 147, 159, 179, 190, 201, 212, 230, 241, 252, 264, 277, 281, 307–311: Business email compromise losses reported to IC3 (context; fraud) (2023); Botnet losses reported to IC3 (2023); Corporate data breach losses reported to IC3 (2023); and 11 more
- [FBI PSA I-120324-PSA](https://www.ic3.gov/PSA/2024/PSA241203) · 2024-12-03 · grade A — `A1_fraud_ai_evidence` row 10: FBI warns criminals use generative AI to facilitate financial fraud
- [IC3 2024 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf) · 2025 · grade A — `A1_fraud_series` rows 20, 63–66, 356–381, 411, 416, 420: IC3 reported losses, all complaints (2024); IC3 losses in fraud-type crime categories (derived sum) (2024); IC3 losses in hacking-type crime categories (derived sum) (2024); and 31 more; `A2_hacking_series` rows 144, 148, 160, 180, 191, 202, 213, 231, 242, 253, 265, 278, 282, 312: Business email compromise losses reported to IC3 (context; fraud) (2024); Botnet losses reported to IC3 (2024); Corporate data breach losses reported to IC3 (2024); and 11 more
- [FBI PSA I-051525-PSA](https://www.ic3.gov/PSA/2025/PSA250515) · 2025-05-15 · grade A — `A1_fraud_ai_evidence` row 11: AI-generated voice messages impersonating senior US officials
- [IC3 2025 Internet Crime Report](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf) · 2026 · grade A/C — `A1_fraud_series` rows 21, 23–26, 67–70, 382–407, 412, 417–419, 421: IC3 reported losses, all complaints (2025); IC3 reported losses, 2025-report 'Losses by Year' chart (2001, 2005, 2010, 2015); IC3 losses in fraud-type crime categories (derived sum) (2025); and 34 more; `A2_hacking_series` rows 133, 145, 149, 161, 181, 192, 203, 214, 232, 243, 254, 266, 279, 283, 299, 313: Losses in complaints containing AI-related information (IC3 descriptor) (2025); Business email compromise losses reported to IC3 (context; fraud) (2025); Botnet losses reported to IC3 (2025); and 13 more; `A1_fraud_ai_evidence` rows 0–9, 42, 45, 46: IC3 complaints whose text references AI: losses; AI-referencing share of IC3 dollars; and 11 more; `A2_hacking_ai_evidence` rows 0, 30: FBI IC3: complaints whose text references AI, 2025; A2 researcher check: IC3 'core hacking' losses (ransomware + corporate data breach + malware) in…

**FBI/NW3C IC3**

- [IC3 PSA: 2009 Internet Crime Report released](https://www.ic3.gov/PSA/2010/PSA100312.pdf) · 2010-03-12 · grade A — `A1_fraud_series` row 5: IC3 reported losses, all complaints (2009)
- [IC3 2010 Internet Crime Report (PSA110224) / The Register coverage](https://ic3.gov/PSA/2011/PSA110224.pdf) · 2011-02-24 · grade A — `A1_fraud_series` row 6: IC3 reported losses, all complaints (2010)

**FBI/NW3C Internet Crime Complaint Center**

- [IC3 PSA: 2008 Internet Crime Report (table of complaints and dollar loss 2004-2008)](https://www.ic3.gov/PSA/2009/PSA090331.pdf) · 2009-03-31 · grade A — `A1_fraud_series` rows 0–4: IC3 reported losses, all complaints (2004–2008)

**Forbes (court document)**

- [Fraudsters Cloned Company Director's Voice In $35 Million Bank Heist, Police Find (Forbes)](https://www.forbes.com/sites/thomasbrewster/2021/10/14/huge-bank-fraud-uses-deep-fake-voice-tech-to-steal-millions/) · 2021-10-14 · grade B — `A1_fraud_ai_evidence` row 16: UAE 'deep voice' bank-transfer fraud

**GASA**

- [GASA/ScamAdviser Global State of Scams 2024](https://www.gasa.org/post/global-state-of-scams-report-2024-1-trillion-stolen-in-12-months-gasa-feedzai) · 2024 · grade C — `A1_fraud_series` row 572: GASA/ScamAdviser Global State of Scams 2024 (2024); `A1_fraud_ai_evidence` row 35: GASA 2024: 31% of respondents uncertain whether AI was involved in scams they met

**GASA / Feedzai**

- [GASA/Feedzai Global State of Scams 2025](https://info.feedzai.com/hubfs/Feedzai_GASA-Global-State-of-Scams.pdf) · 2025-10-07 · grade C — `A1_fraud_series` row 571: GASA/Feedzai Global State of Scams 2025 (2025)

**Google Mandiant**

- [M-Trends 2026](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026) · 2026-03-23 · grade B — `A2_hacking_ai_evidence` row 18: Mandiant M-Trends 2026: '2025 was not the year breaches were a direct result of AI'

**Google Threat Intelligence Group**

- [GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools) · 2025-11-05 · grade B — `A2_hacking_ai_evidence` row 9: Google GTIG Nov 2025: first malware families querying LLMs during execution (PROMPTFLUX…
- [Distillation, experimentation and integration: AI adversarial use (GTIG)](https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use) · 2026-02-12 · grade C — `A2_hacking_ai_evidence` row 31: GTIG Feb 2026: 'not yet seen' agentic AI capabilities used in the wild; no breakthrough capabilities
- [AI vulnerability exploitation and initial access (GTIG)](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access) · 2026-05-11 · grade C — `A2_hacking_ai_evidence` row 11: Google GTIG May 2026: first zero-day exploit GTIG believes was developed with AI, by a criminal…
- [Vulnerability discovery and exploitation trends in the AI era](https://cloud.google.com/blog/topics/threat-intelligence/vulnerability-discovery-and-exploitation-trends-in-the-ai-era) · 2026-09-30 · grade B — `A2_hacking_ai_evidence` row 24: GTIG Sep 2026: exploited vulnerabilities rose to 18/month (Jan-Aug 2026) from 10.5/month (2025)…

**GovAI (Lukosiute, Halstead, Righetti)**

- [Estimating global yearly cybercrime damage costs](https://www.governance.ai/research-paper/estimating-global-yearly-cybercrime-damage-costs) · 2026-03-09 · grade B — `A1_fraud_series` row 577: GovAI global yearly cybercrime damage (central) (2025); `A2_hacking_series` row 118: GovAI global cybercrime damage estimate (2025); `A2_hacking_ai_evidence` row 29: GovAI (Mar 2026): global cybercrime damage ~$500bn a year (90% CI $100bn-$1tn); 'data on…

**Griffin & Mei (SSRN working paper)**

- [Griffin & Mei: flows into suspicious exchange deposit accounts linked to pig butchering](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4742235) · 2024-03-28 · grade B — `A1_fraud_series` row 578: Griffin & Mei: flows into suspicious exchange deposit accounts linked to pig… (2022); `A1_fraud_ai_evidence` row 40: Pig-butchering flows predate gen-AI

**Healthcare Dive (reporting UnitedHealth disclosure)**

- [Change Healthcare cyberattack affects 190 million, UnitedHealth says](https://www.healthcaredive.com/news/change-healthcare-cyberattack-affects-190-million-unitedhealth/738351/) · 2025-01-27 · grade A — `A2_hacking_series` row 317: UnitedHealth spending responding to the Change Healthcare attack in 2024 (2024)

**Heiding, Lermen, Kao, Schneier, Vishwanath**

- [Evaluating Large Language Models' Capability to Launch Fully Automated Spear Phishing Campaigns (arXiv:2412.00586)](https://arxiv.org/abs/2412.00586) · 2024-11-30 · grade B — `A1_fraud_ai_evidence` row 25: Heiding et al. RCT: fully AI-automated spear phishing matches human experts

**Hong Kong Police Force**

- [Law and order situation in Hong Kong in 2025 (Commissioner's year-end review)](https://www.police.gov.hk/ppp_en/01_about_us/cp_ye.html) · 2026 · grade A — `A1_fraud_series` rows 551, 552: HKPF deception case losses (2024, 2025)

**Hoxhunt**

- [AI-powered phishing outperforms elite red teams (Hoxhunt)](https://hoxhunt.com/blog/ai-powered-phishing-vs-humans) · 2025 · grade C — `A1_fraud_ai_evidence` row 26: Hoxhunt: AI agent vs human red team phishing simulations

**Hugging Face**

- [Agent intrusion technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline) · 2026-07-27 · grade A — `A2_hacking_ai_evidence` row 27: OpenAI/Hugging Face agent incident (May-Jul 2026): ~700 of ~1,200 evaluation agents joined an…

**IBM / Ponemon Institute**

- [IBM Cost of a Data Breach 2019 (press release)](https://newsroom.ibm.com/2019-07-23-IBM-Study-Shows-Data-Breach-Costs-on-the-Rise-Financial-Impact-Felt-for-Years) · 2019-07-23 · grade B — `A2_hacking_series` rows 121, 129: Average total cost of a data breach per organisation (2018)
- [IBM Cost of a Data Breach 2020 (press release)](https://newsroom.ibm.com/2020-07-29-IBM-Report-Compromised-Employee-Accounts-Led-to-Most-Expensive-Data-Breaches-Over-Past-Year) · 2020-07-29 · grade B — `A2_hacking_series` rows 122, 130: Average total cost of a data breach per organisation (2019)
- [IBM Cost of a Data Breach 2021 (press release)](https://newsroom.ibm.com/2021-07-28-IBM-Report-Cost-of-a-Data-Breach-Hits-Record-High-During-Pandemic) · 2021-07-28 · grade B — `A2_hacking_series` rows 123, 131: Average total cost of a data breach per organisation (2020)
- [IBM Cost of a Data Breach 2022 (press release)](https://newsroom.ibm.com/2022-07-27-IBM-Report-Consumers-Pay-the-Price-as-Data-Breach-Costs-Reach-All-Time-High) · 2022-07-27 · grade B — `A2_hacking_series` row 124: Average total cost of a data breach per organisation (2021)
- [IBM Cost of a Data Breach 2023 (press release)](https://newsroom.ibm.com/2023-07-24-IBM-Report-Half-of-Breached-Organizations-Unwilling-to-Increase-Security-Spend-Despite-Soaring-Breach-Costs) · 2023-07-24 · grade B — `A2_hacking_series` row 125: Average total cost of a data breach per organisation (2022)
- [IBM Cost of a Data Breach 2024 (press release)](https://newsroom.ibm.com/2024-07-30-ibm-report-escalating-data-breach-disruption-pushes-costs-to-new-highs) · 2024-07-30 · grade B — `A2_hacking_series` row 126: Average total cost of a data breach per organisation (2023)
- [IBM Report: 13% of Organizations Reported Breaches of AI Models or Applications](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls) · 2025-07-30 · grade B — `A2_hacking_series` rows 120, 127, 132: Share of studied breaches in which attackers used AI (2024); Average total cost of a data breach per organisation (2024); `A2_hacking_ai_evidence` row 1: IBM/Ponemon: share of studied breaches in which attackers used AI (2025 edition)
- [IBM Study: One in Four Malicious Breaches are AI-Enabled, Costing Companies $6 Million on Average](https://newsroom.ibm.com/2026-07-29-ibm-study-one-in-four-malicious-breaches-are-ai-enabled,-costing-companies-6-million-on-average) · 2026-07-29 · grade B — `A2_hacking_series` rows 119, 128: Share of malicious breaches that were AI-enabled (2025); Average total cost of a data breach per organisation (2025); `A2_hacking_ai_evidence` row 2: IBM/Ponemon: one in four malicious breaches AI-enabled; they cost $6.0m on average (2026 edition)

**Identity Theft Resource Center**

- [ITRC 2018 End-of-Year Data Breach Report](https://www.idtheftcenter.org/wp-content/uploads/2019/02/ITRC_2018-End-of-Year-Aftermath_FINAL_V2_combinedWEB.pdf) · 2019-02 · grade B — `A2_hacking_series` row 335: US data breaches (pre-2019 ITRC method) (2017)
- [ITRC 2019 End-of-Year Data Breach Report](https://www.idtheftcenter.org/wp-content/uploads/2020/01/01.28.2020_ITRC_2019-End-of-Year-Data-Breach-Report_FINAL_Highres-Appendix.pdf) · 2020-01-28 · grade B — `A2_hacking_series` rows 336, 337: US data breaches (2019-report restatement) (2018); US data breaches (pre-2020 ITRC method) (2019)
- [ITRC 2021 Annual Data Breach Report (table 'Compromise Trends 2015 to 2021')](https://www.idtheftcenter.org/wp-content/uploads/2022/04/ITRC_2021_Data_Breach_Report.pdf) · 2022-01-24 · grade B — `A2_hacking_series` rows 324, 339: Publicly reported US data compromises (2015); Individuals impacted by US data compromises (victim notices) (2015)
- [ITRC 2022 Annual Data Breach Report (table 'Compromises and Victims by Year 2016-2022')](https://www.idtheftcenter.org/wp-content/uploads/2023/01/ITRC_2022-Data-Breach-Report_Final-1.pdf) · 2023-01-25 · grade B — `A2_hacking_series` rows 323, 325–331, 338, 340–346: US data compromises attributed to cyberattacks (2022); Publicly reported US data compromises (2016–2022); US data compromises attributed to ransomware (2022); and 1 more
- [ITRC 2023 Annual Data Breach Report press release](https://www.idtheftcenter.org/post/2023-annual-data-breach-report/) · 2024-01-25 · grade B — `A2_hacking_series` rows 332, 347: Publicly reported US data compromises (2023); Individuals impacted by US data compromises (2023)
- [ITRC 2024 Annual Data Breach Report press release](https://www.idtheftcenter.org/post/2024-annual-data-breach-report-near-record-compromises/) · 2025-01-28 · grade B — `A2_hacking_series` rows 333, 348: Publicly reported US data compromises (2024); Victim notices issued for US data compromises (2024)
- [ITRC 2025 Annual Data Breach Report press release](https://www.idtheftcenter.org/post/2025-annual-data-breach-report/) · 2026-01-29 · grade B — `A2_hacking_series` rows 334, 349: Publicly reported US data compromises (2025); Victim notices issued for US data compromises (2025)

**INTERPOL**

- [INTERPOL report finds AI linked to more than half of cybercrime in Africa](https://www.interpol.int/en/News-and-Events/News/2026/INTERPOL-report-finds-AI-linked-to-more-than-half-of-cybercrime-in-Africa) · 2026-08-03 · grade C — `A1_fraud_ai_evidence` row 34: INTERPOL: AI involved in 55% of reported cybercrime in Africa

**Korea Times**

- [Voice phishing crimes drop 40% thanks to tougher measures](https://www.koreatimes.co.kr/southkorea/law-crime/20260902/voice-phishing-crimes-drop-40-thanks-to-tougher-measures) · 2026-09-02 · grade B — `A1_fraud_series` row 555: Voice phishing damage Oct 2025-Jul 2026 (police) (2026)

**Microsoft**

- [Cyber Signals Issue 9: AI-powered deception](https://www.microsoft.com/en-us/security/blog/2025/04/16/cyber-signals-issue-9-ai-powered-deception-emerging-fraud-threats-and-countermeasures/) · 2025-04-16 · grade C — `A1_fraud_ai_evidence` row 27: Microsoft blocked $4bn in fraud attempts; AI used for fake stores and job scams
- [Microsoft Digital Defense Report 2025 (On the Issues blog)](https://blogs.microsoft.com/on-the-issues/2025/10/16/mddr-2025/) · 2025-10-16 · grade C — `A2_hacking_ai_evidence` row 22: Microsoft Digital Defense Report 2025: attackers using AI to automate phishing and scale social…
- [Microsoft disrupts cybercrime (RedVDS)](https://blogs.microsoft.com/on-the-issues/2026/01/14/microsoft-disrupts-cybercrime/) · 2026-01-14 · grade C — `A1_fraud_ai_evidence` row 28: RedVDS disposable-server service linked to US fraud losses; often paired with gen-AI
- [Insights from the 2026 Microsoft Digital Defense Report](https://www.microsoft.com/en-us/security/blog/2026/10/01/insights-from-the-2026-microsoft-digital-defense-report/) · 2026-10-01 · grade C — `A2_hacking_ai_evidence` row 21: Microsoft Digital Defense Report 2026: threat-actor AI use 'remains focused on specific parts of…

**Microsoft DCU**

- [Disrupting EvilTokens: the AI chatbot built for cybercrime](https://blogs.microsoft.com/on-the-issues/2026/09/22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/) · 2026-09-22 · grade B — `A1_fraud_ai_evidence` row 29: EvilTokens: first end-to-end AI-enabled BEC service disrupted; `A2_hacking_ai_evidence` row 26: Microsoft DCU Sep 2026: EvilTokens AI-assisted phishing/BEC service disrupted (\>12,000 inboxes…

**Microsoft via The Register**

- [AI makes phishing 4.5x more effective, Microsoft says (The Register, on Microsoft Digital Defense Report 2025)](https://www.theregister.com/2025/10/16/ai_makes_phishing_45x_more_effective) · 2025-10-16 · grade C — `A1_fraud_ai_evidence` row 24: Microsoft: AI-automated phishing 54% click-through vs 12% (4.5x)

**Munich Re**

- [Cyber insurance: risks and trends 2024](https://www.munichre.com/en/insights/cyber/cyber-insurance-risks-and-trends-2024.html) · 2024-04-04 · grade B — `A2_hacking_series` row 350: Global cyber insurance premium volume (2023)
- [Cyber insurance: risks and trends 2025](https://www.munichre.com/en/insights/cyber/cyber-insurance-risks-and-trends-2025.html) · 2025-04-03 · grade B — `A2_hacking_series` rows 351, 352: Global cyber insurance premium volume (2024, 2025)
- [Cyber insurance: risks and trends 2026](https://www.munichre.com/en/insights/cyber/cyber-insurance-risks-and-trends-2026.html) · 2026-03-25 · grade B — `A2_hacking_series` row 353: Ratio of malicious to non-malicious cyber loss events in Munich Re claims (2025); `A2_hacking_ai_evidence` row 32: Munich Re (Mar 2026): agentic AI expected to affect attack frequency more than severity in the…

**NAIC**

- [NAIC Report on the Cybersecurity Insurance Market (data year 2022)](https://content.naic.org/sites/default/files/inline-files/Final%202023%20Cyber%20Report.pdf) · 2023 · grade A — `A2_hacking_series` rows 373, 374: Average direct loss ratio, top 20 cyber insurer groups (2021, 2022)
- [NAIC 2024 Report on the Cybersecurity Insurance Market (data year 2023)](https://content.naic.org/sites/default/files/cmte-h-cyber-wg-2024-cyber-ins-report.pdf) · 2024 · grade A — `A2_hacking_series` rows 354, 364, 382: Reported cyber insurance claims (domestic) (2023); Cyber insurance direct written premium, incl. alien surplus lines (2019); Standalone share of total US cyber DWP (2023)
- [NAIC 2025 Report on the Cybersecurity Insurance Market (data year 2024)](https://content.naic.org/sites/default/files/inline-files/2025_Cybersecurity_Insurance%20Report.pdf) · 2025 · grade A — `A2_hacking_series` rows 355, 357–362, 365–369, 375–380: Reported cyber insurance claims (domestic) (2024); Cyber insurance direct written premium, domestic insurers (2019–2024); Cyber insurance direct written premium, incl. alien surplus lines (2020–2024); and 1 more
- [NAIC 2026 Report on the Cybersecurity Insurance Market (data year 2025)](https://content.naic.org/sites/default/files/2026-report-cybersecurity-insurance-market.pdf) · 2026 · grade A — `A2_hacking_series` rows 356, 363, 370–372, 381: Reported cyber insurance claims (domestic) (2025); Cyber insurance direct written premium, domestic insurers (2025); Cyber insurance direct written premium, incl. alien surplus lines (2025); and 2 more

**National Police Agency of Japan**

- [NPA, 特殊詐欺の認知・検挙状況等 (annual statistics, final values)](https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2017.pdf) · grade A — `A1_fraud_series` rows 515–517: NPA special fraud (tokushu sagi) damage (2007–2009)
- [NPA, 特殊詐欺の認知・検挙状況等 (annual statistics, final values)](https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2019.pdf) · grade A — `A1_fraud_series` rows 518–522: NPA special fraud (tokushu sagi) damage (2010–2014)
- [NPA, 令和6年/令和7年における特殊詐欺及びSNS型投資・ロマンス詐欺の認知・検挙状況等（確定値）](https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2024.pdf) · 2025 · grade A — `A1_fraud_series` rows 523, 534, 535: NPA special fraud (tokushu sagi) damage (2015); NPA SNS-type investment and romance fraud damage (2023, 2024)
- [NPA, 特殊詐欺の認知・検挙状況等 (annual statistics, final values)](https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2025.pdf) · 2026-05-22 · grade A — `A1_fraud_series` rows 524–533, 536: NPA special fraud (tokushu sagi) damage (2016–2025); NPA SNS-type investment and romance fraud damage (2025); `A1_fraud_ai_evidence` row 43: Japan special fraud tripled 2022-2025 with phone-first contact

**nysut.org**

- [NYSUT CPI fact sheet citing BLS](https://www.nysut.org/-/media/files/nysut/resources/2026/2026_01_21_factsheet_consumerpriceindex.pdf) · grade A/B — `cpi_u` rows 18–20: CPI-U annual averages (2023–2025)

**NYU Tandon (arXiv)**

- [Ransomware 3.0: Self-Composing and LLM-Orchestrated (arXiv:2508.20444)](https://arxiv.org/abs/2508.20444) · 2025-08-28 · grade B — `A2_hacking_ai_evidence` row 10: ESET/NYU 'PromptLock' (Aug 2025): first 'AI-powered ransomware' was an academic proof of concept

**Pindrop**

- [Voice Intelligence and Security Report 2025 (Pindrop landing page)](https://www.pindrop.com/research/report/voice-intelligence-security-report/) · 2025 · grade D — `A1_fraud_ai_evidence` row 33: Pindrop links $12.5bn of 2024 fraud to AI threats

**ransomware.live (community tracker)**

- [ransomware.live statistics 2023](https://www.ransomware.live/stats/2023) · 2026-10-17 · grade C — `A2_hacking_series` row 383: Victims posted on ransomware/extortion leak sites (2023)
- [ransomware.live statistics 2024](https://www.ransomware.live/stats/2024) · 2026-10-17 · grade C — `A2_hacking_series` row 384: Victims posted on ransomware/extortion leak sites (2024)
- [ransomware.live statistics 2025](https://www.ransomware.live/stats/2025) · 2026-10-17 · grade C — `A2_hacking_series` row 385: Victims posted on ransomware/extortion leak sites (2025)
- [ransomware.live statistics 2026](https://www.ransomware.live/stats/2026) · 2026-10-17 · grade C — `A2_hacking_series` row 386: Victims posted on ransomware/extortion leak sites (2026)

**Resemble AI**

- [Q1 2025 AI Deepfake Security Report (Resemble AI)](https://www.resemble.ai/q1-2025-ai-deepfake-security-report/) · 2025 · grade C — `A1_fraud_ai_evidence` row 32: Resemble AI: deepfake incidents caused \>$200m documented losses in Q1 2025

**SANS (citing MGM)**

- [Prior project event catalogue (Cheddar/SANS)](https://www.sans.org/blog/defending-against-scattered-spider-and-the-com-with-cybercrime-intelligence) · 2023 · grade C — `A2_hacking_series` row 319: MGM Resorts adverse EBITDA impact from Sept 2023 attack (2023)

**ScanMyShadow (secondary; MHA data)**

- [India Cyber Fraud 2021 to 2025: NCRP Complaints, Losses (tabulating MHA Rajya Sabha reply 11 Feb 2026)](https://www.scanmyshadow.com/blog/2026/10/india-cyber-fraud-2021-2025-ncrp-complaints-losses.html) · 2026 · grade B — `A1_fraud_series` rows 579–583: NCRP reported financial cyber-fraud losses (2021–2025)

**Seoulz (secondary, citing KNPA)**

- [Korea Voice Phishing 2026: Why Banks Now Pay the Bill](https://www.seoulz.com/korea-voice-phishing-2026/amp/) · 2026 · grade B — `A1_fraud_series` rows 553, 554: Voice phishing damage (police count, telecom financial fraud) (2025); Voice phishing damage (FSS damage-relief count) (2025)

**Singapore Police Force**

- [Scams and cybercrime fell by almost a quarter in 2025](https://www.police.gov.sg/media-hub/police-life/2026/02/scams-and-cybercrime-fell-by-almost-a-quarter-in-2025) · 2026-02-26 · grade A — `A1_fraud_series` rows 549, 550: SPF reported scam losses (2024, 2025)

**Sophos**

- [Sophos State of Ransomware 2020](https://www.sophos.com/en-us/blog/the-state-of-ransomware-2021) · 2020 · grade C — `A2_hacking_series` rows 387, 388, 398, 399, 403, 404: Mean cost to recover from a ransomware attack, excluding any ransom (2019, 2020); Share of surveyed organisations hit by ransomware in the prior 12 months (2019, 2020); Share of organisations whose data were encrypted that paid the ransom (2019, 2020)
- [Sophos State of Ransomware 2022](https://www.sophos.com/en-us/blog/the-state-of-ransomware-2022) · 2022 · grade C — `A2_hacking_series` rows 389, 394, 400, 405: Mean cost to recover from a ransomware attack, excluding any ransom (2021); Ransom paid per paying victim (Sophos survey; mean/median as noted) (2021); Share of surveyed organisations hit by ransomware in the prior 12 months (2021); and 1 more
- [Sophos State of Ransomware 2023](https://www.sophos.com/en-us/blog/the-state-of-ransomware-2023) · 2023 · grade C — `A2_hacking_series` rows 401, 406: Share of surveyed organisations hit by ransomware in the prior 12 months (2022); Share of organisations whose data were encrypted that paid the ransom (2022)
- [Sophos State of Ransomware 2024](https://www.sophos.com/en-us/blog/the-state-of-ransomware-2024) · 2023 · grade C — `A2_hacking_series` rows 390, 391, 395, 396, 402, 407: Mean cost to recover from a ransomware attack, excluding any ransom (2022, 2023); Ransom paid per paying victim (Sophos survey; mean/median as noted) (2022, 2023); Share of surveyed organisations hit by ransomware in the prior 12 months (2023); and 1 more
- [Sophos State of Ransomware 2025](https://www.sophos.com/en-us/blog/the-state-of-ransomware-2025) · 2025 · grade C — `A2_hacking_series` rows 392, 408: Mean cost to recover from a ransomware attack, excluding any ransom (2024); Share of organisations whose data were encrypted that paid the ransom (2024)
- [Nowhere, man: The 2026 Sophos Active Adversary Report](https://www.sophos.com/en-us/blog/2026-sophos-active-adversary-report) · 2026 · grade C — `A2_hacking_ai_evidence` row 19: Sophos Active Adversary Report 2026: GenAI in 2025 'wasn't the watershed moment that signaled the…
- [Sophos State of Ransomware 2026](https://assets.sophos.com/X24WTUEQ/at/8mrcrvgg84jkh79n3kccmpq7/sophos-state-ransomware-report-2026-es.pdf) · 2026 · grade C — `A2_hacking_series` rows 393, 397, 409: Mean cost to recover from a ransomware attack, excluding any ransom (2025); Ransom paid per paying victim (Sophos survey; mean/median as noted) (2025); Share of organisations whose data were encrypted that paid the ransom (2025)

**Starling Bank**

- [Starling Bank 'Safe Phrases' campaign (Mortar Research survey)](https://www.starlingbank.com/news/starling-bank-launches-safe-phrases-campaign/) · 2024 · grade C — `A1_fraud_ai_evidence` row 30: UK adults who think they were targeted by an AI voice-cloning scam

**Sysdig**

- [JADEPUFFER: agentic ransomware for automated database extortion](https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) · 2026-07-01 · grade C — `A2_hacking_ai_evidence` row 12: Sysdig 'JADEPUFFER': first documented agentic ransomware/extortion run end-to-end by an LLM agent

**TRM Labs**

- [North Korea Stole 76% of All Crypto Hack Value in 2026 - With Just Two Attacks](https://www.trmlabs.com/resources/blog/north-korea-stole-76-of-all-crypto-hack-value-in-2026-with-just-two-attacks) · 2026-04-30 · grade B — `A2_hacking_series` rows 315, 410–416: Bybit exchange theft (DPRK) (2025); DPRK share of crypto hack losses (TRM Labs) (2020–2026)
- [H1 2026 Crypto Hacks Reach Record High as Losses Fall Below USD 1 Billion](https://www.trmlabs.com/resources/blog/h1-2026-crypto-hacks-reach-record-high-as-losses-fall-below-usd-1-billion) · 2026-07-01 · grade B — `A2_hacking_series` row 417: Crypto stolen in hacks, first half (TRM Labs) (2026)
- [The 2026 AI-in-Crime Adoption Index](https://www.trmlabs.com/reports-and-whitepapers/the-2026-ai-in-crime-adoption-index) · 2026-08-17 · grade C — `A2_hacking_ai_evidence` row 3: TRM Labs 2026 AI-in-Crime Adoption Index: overall 54/100 ('Emerging'); scams 'Mature'; hacking and…

**UK DCMS / Home Office**

- [Cyber Security Breaches Survey 2019 (main report, revised V2)](https://assets.publishing.service.gov.uk/media/5ff5bb478fa8f53b772750cf/Cyber_Security_Breaches_Survey_2019_-_Main_Report_-_revised_V2.pdf) · 2019-04-03 · grade A — `A2_hacking_series` rows 421–426: Mean cost of breaches for businesses with a negative outcome (last 12 months) (2017–2019); Share of UK businesses identifying any cyber breach or attack in the last 12 months (2017–2019)

**UK DSIT (then DCMS) / Home Office**

- [Cyber security breaches survey 2021](https://www.gov.uk/government/statistics/cyber-security-breaches-survey-2021/cyber-security-breaches-survey-2021) · 2021-03-24 · grade A — `A2_hacking_series` rows 427, 428: Share of UK businesses identifying any cyber breach or attack in the last 12 months (2020, 2021)

**UK DSIT / Home Office**

- [Cyber security breaches survey 2025](https://www.gov.uk/government/statistics/cyber-security-breaches-survey-2025/cyber-security-breaches-survey-2025) · 2025-04-10 · grade A — `A2_hacking_series` rows 418, 420, 429, 430, 432: Estimated cyber crimes experienced by UK businesses (last 12 months) (2025); Average cost of the most disruptive breach per business (last 12 months) (2025); Share of UK businesses identifying any cyber breach or attack in the last 12 months (2024, 2025); and 1 more
- [Cyber security breaches survey 2025/2026](https://www.gov.uk/government/statistics/cyber-security-breaches-survey-20252026/cyber-security-breaches-survey-20252026) · 2026-04-30 · grade A — `A2_hacking_series` rows 419, 431, 433: Estimated cyber crimes experienced by UK businesses (last 12 months) (2026); Share of UK businesses identifying any cyber breach or attack in the last 12 months (2026); Share of UK businesses experiencing ransomware (breach measure) (2026); `A2_hacking_ai_evidence` row 33: UK Cyber Security Breaches Survey 2025: qualitative interviews find 'AI impersonation' becoming…

**UK Finance**

- [UK Finance Annual Fraud Report 2023](https://www.ukfinance.org.uk/system/files/2023-05/Annual%20Fraud%20Report%202023_0.pdf) · 2023 · grade A — `A1_fraud_series` rows 469–485: UK Finance unauthorised fraud losses (cards, remote banking, cheques) (2013–2019); UK Finance payment card fraud losses (2013–2022)
- [UK Finance Annual Fraud Report 2026](https://www.ukfinance.org.uk/system/files/2026-06/UK%20Finance%20Fraud%20Report%202026.pdf) · 2026 · grade A — `A1_fraud_series` rows 451–468, 486: UK Finance total payment fraud losses (unauthorised + APP) (2020–2025); UK Finance unauthorised fraud losses (cards, remote banking, cheques) (2020–2025); UK Finance authorised push payment (APP) scam losses (2020–2025); and 1 more; `A1_fraud_ai_evidence` row 38: UK Finance 2026 annual fraud report has no AI-attributed loss figures

**UNODC 'Inflection Point' (via AFP/Dawn)**

- [UNODC East/SE Asia cyber-fraud losses (high)](https://www.dawn.com/news/1905706) · 2025-04-21 · grade B — `A1_fraud_series` row 574: UNODC East/SE Asia cyber-fraud losses (high) (2023)

**UNODC (via AFP/Taipei Times)**

- [UNODC East/SE Asia cyber-fraud losses (low)](https://www.taipeitimes.com/News/world/archives/2026/07/22/2003861183) · 2026-07-22 · grade B — `A1_fraud_series` row 573: UNODC East/SE Asia cyber-fraud losses (low) (2023)

**UNODC (via Forklog/AFP)**

- [UNODC 2025 scam losses E/SE Asia + Australia + NZ (low)](https://forklog.com/en/unodc-estimates-2025-scam-losses-in-east-and-southeast-asia-australia-and-new-zealand-at-88b-114b/) · 2026-07-21 · grade B/C — `A1_fraud_series` rows 575, 576: UNODC 2025 scam losses E/SE Asia + Australia + NZ (low) (2025); UNODC 2025 scam losses (high) (2025); `A1_fraud_ai_evidence` row 36: UNODC: gen-AI lowers bar for complex fraud (translation, voice cloning, real-time deepfake video)

**US DOJ SDNY**

- [Lithuanian man sentenced to 5 years for theft of over $120 million in fraudulent business email compromise scheme](https://www.justice.gov/usao-sdny/pr/lithuanian-man-sentenced-5-years-prison-theft-over-120-million-fraudulent-business) · 2019-12-19 · grade A — `A1_fraud_ai_evidence` row 17: Pre-AI benchmark: fake-invoice BEC against two US tech companies

**US Federal Trade Commission**

- [Consumer Sentinel CY2007 report](https://www.ftc.gov/sites/default/files/documents/reports_annual/sentinel-cy-2007/sentinel-cy2007.pdf) · 2008 · grade A — `A1_fraud_series` rows 422–424: FTC Consumer Sentinel reported fraud losses (2005–2007)
- [Consumer Sentinel Network Data Book CY2008](https://www.ftc.gov/sites/default/files/documents/reports_annual/sentinel-cy-2008/sentinel-cy2008.pdf) · 2009 · grade A — `A1_fraud_series` row 425: FTC Consumer Sentinel reported fraud losses (2008)
- [Consumer Sentinel Network Data Book CY2010 (3-year table)](https://www.ftc.gov/sites/default/files/documents/reports_annual/sentinel-cy-2010/sentinel-cy2010.pdf) · 2011 · grade A — `A1_fraud_series` rows 426, 427: FTC Consumer Sentinel reported fraud losses (2009, 2010)
- [Consumer Sentinel Network Data Book CY2012](https://www.ftc.gov/sites/default/files/documents/reports/consumer-sentinel-network-data-book-january/sentinel-cy2012.pdf) · 2013 · grade A — `A1_fraud_series` row 429: FTC Consumer Sentinel reported fraud losses (2012)
- [Consumer Sentinel Network Data Book CY2013 (3-year table)](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-january-december-2013/sentinel-cy2013.pdf) · 2014 · grade A — `A1_fraud_series` rows 428, 430: FTC Consumer Sentinel reported fraud losses (2011, 2013)
- [Consumer Sentinel Network Data Book CY2014](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-january-december-2014/sentinel-cy2014-1.pdf) · 2015 · grade A — `A1_fraud_series` row 431: FTC Consumer Sentinel reported fraud losses (2014)
- [Consumer Sentinel Network Data Book CY2015](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-january-december-2015/160229csn-2015databook.pdf) · 2016 · grade A — `A1_fraud_series` row 432: FTC Consumer Sentinel reported fraud losses (2015)
- [Consumer Sentinel Network Data Book CY2016](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-january-december-2016/csn_cy-2016_data_book.pdf) · 2017 · grade A — `A1_fraud_series` row 433: FTC Consumer Sentinel reported fraud losses (2016)
- [Consumer Sentinel Network Data Book 2017](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-2017/consumer_sentinel_data_book_2017.pdf) · 2018 · grade A — `A1_fraud_series` row 434: FTC Consumer Sentinel reported fraud losses (2017)
- [Consumer Sentinel Network Data Book 2018](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-2018/consumer_sentinel_network_data_book_2018_0.pdf) · 2019 · grade A — `A1_fraud_series` row 435: FTC Consumer Sentinel reported fraud losses (2018)
- [Consumer Sentinel Network Data Book 2019](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-2019/consumer_sentinel_network_data_book_2019.pdf) · 2020 · grade A — `A1_fraud_series` row 436: FTC Consumer Sentinel reported fraud losses (2019)
- [Consumer Sentinel Network Data Book 2020](https://www.ftc.gov/system/files/documents/reports/consumer-sentinel-network-data-book-2020/csn_annual_data_book_2020.pdf) · 2021 · grade A — `A1_fraud_series` row 437: FTC Consumer Sentinel reported fraud losses (2020)
- [Consumer Sentinel Network Data Book 2021](https://www.ftc.gov/system/files/ftc_gov/pdf/CSN%20Annual%20Data%20Book%202021%20Final%20PDF.pdf) · 2022 · grade A — `A1_fraud_series` row 438: FTC Consumer Sentinel reported fraud losses (2021)
- [Consumer Sentinel Network Data Book 2022](https://www.ftc.gov/system/files/ftc_gov/pdf/CSN-Data-Book-2022.pdf) · 2023 · grade A — `A1_fraud_series` row 439: FTC Consumer Sentinel reported fraud losses (2022)
- [Protecting Older Consumers 2022-2023](https://www.ftc.gov/system/files/ftc_gov/pdf/p144400olderadultsreportoct2023.pdf) · 2023 · grade B — `A1_fraud_series` rows 443, 444: FTC estimate of total consumer fraud losses adjusted for under-reporting… (2022); FTC estimate of total consumer fraud losses adjusted for under-reporting (base) (2022)
- [Consumer Sentinel Network Data Book 2023](https://www.ftc.gov/system/files/ftc_gov/pdf/CSN-Annual-Data-Book-2023.pdf) · 2024 · grade A — `A1_fraud_series` row 440: FTC Consumer Sentinel reported fraud losses (2023)
- [Protecting Older Consumers 2023-2024](https://www.ftc.gov/system/files/ftc_gov/pdf/federal-trade-commission-protecting-older-adults-report_102024.pdf) · 2024 · grade B — `A1_fraud_series` rows 445, 446: FTC estimate of total consumer fraud losses adjusted for under-reporting… (2023); FTC estimate of total consumer fraud losses adjusted for under-reporting (base) (2023)
- [Consumer Sentinel Network Data Book 2024](https://www.ftc.gov/system/files/ftc_gov/pdf/csn-annual-data-book-2024.pdf) · 2025 · grade A — `A1_fraud_series` row 441: FTC Consumer Sentinel reported fraud losses (2024)
- [Protecting Older Consumers 2024-2025](https://www.ftc.gov/system/files/ftc_gov/pdf/P144400-OlderAdultsReportDec2025.pdf) · 2025 · grade B — `A1_fraud_series` rows 447, 448: FTC estimate of total consumer fraud losses adjusted for under-reporting… (2024); FTC estimate of total consumer fraud losses adjusted for under-reporting (base) (2024)
- [FTC testifies before Joint Economic Committee (press release)](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-testifies-joint-economic-committee-agencys-efforts-combat-fraud) · 2026-03-25 · grade A — `A1_fraud_series` row 442: FTC Consumer Sentinel reported fraud losses (2025)
- [Reported losses to scams on social media eight times higher than in 2020 (FTC Data Spotlight)](https://www.ftc.gov/news-events/data-visualizations/data-spotlight/2026/04/reported-losses-scams-social-media-eight-times-higher-2020) · 2026-04-27 · grade A — `A1_fraud_series` rows 585, 586: FTC reported losses to scams that started on social media (2020, 2025)
- [FTC Issues Annual Report to Congress on Agency's Actions to Protect Older Adults](https://www.ftc.gov/news-events/news/press-releases/2026/10/ftc-issues-annual-report-congress-agencys-actions-protect-older-adults) · 2026-10-19 · grade A — `A1_fraud_series` rows 587, 588: FTC reported fraud losses, consumers 60+ (2020, 2025)
- [Protecting Older Consumers 2025-2026](https://www.ftc.gov/system/files/ftc_gov/pdf/2026-older-adults-report-10192026.pdf) · 2026-10-19 · grade B — `A1_fraud_series` rows 449, 450: FTC estimate of total consumer fraud losses adjusted for under-reporting… (2025); FTC estimate of total consumer fraud losses adjusted for under-reporting (base) (2025)

**US Treasury FinCEN**

- [FinCEN Alert FIN-2023-Alert005 (pig butchering)](https://www.fincen.gov/sites/default/files/shared/FinCEN_Alert_Pig_Butchering_FINAL_508c.pdf) · 2023-09-08 · grade A — `A1_fraud_ai_evidence` row 41: FinCEN pig-butchering alert (pre-gen-AI typology)
- [FinCEN Alert FIN-2024-Alert004 (deepfake media)](https://www.fincen.gov/system/files/shared/FinCEN-Alert-DeepFakes-Alert508FINAL.pdf) · 2024-11-13 · grade A — `A1_fraud_ai_evidence` row 12: FinCEN observed increase in SARs describing deepfake media
- [Financial Trend Analysis: Ransomware (FinCEN)](https://www.fincen.gov/system/files/2025-12/FTA-Ransomware.pdf) · 2025-12 · grade A — `A2_hacking_series` rows 105–114: Median single ransomware transaction (2022–2024); Ransomware incidents in BSA filings (2021–2024); Ransomware payments in BSA filings (2023, 2024); and 1 more

**Verizon**

- [Verizon 2024 Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/2024-dbir-data-breach-investigations-report.pdf) · 2024 · grade B — `A2_hacking_series` rows 95, 99, 100: Median adjusted loss for ransomware/extortion victims (DBIR analysis of FBI IC3 data) (2023); Share of breaches involving ransomware (excluding pure extortion) (2023); Share of breaches involving ransomware or extortion (2023); `A2_hacking_ai_evidence` row 16: Verizon DBIR 2024: searched for GenAI in attacks - 'nothing materialized in the incident data we…
- [Verizon 2025 Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/2025-dbir-data-breach-investigations-report.pdf) · 2024 · grade B — `A2_hacking_series` rows 93, 96, 97, 101, 103: Share of malicious emails with AI-assisted (synthetic) text, approx. (2024); Median ransom paid (2023, 2024); Share of breaches involving ransomware (2024); and 1 more; `A1_fraud_ai_evidence` row 22: AI-assisted share of malicious emails doubled to ~10%; `A2_hacking_ai_evidence` row 17: Verizon DBIR 2025: AI-assisted text in malicious email doubled from ~5% to ~10% in two years; 'no…
- [Verizon 2026 Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/dbir/) · 2026 · grade B — `A2_hacking_series` rows 94, 102: Share of breaches starting with software vulnerability exploitation (2025); Share of breaches involving ransomware (2025)
- [Verizon 2026 Data Breach Investigations Report](https://www.verizon.com/business/resources/T343/reports/2026-dbir-data-breach-investigations-report.pdf) · 2026 · grade B/C — `A2_hacking_series` rows 98, 104: Median ransom paid (2025); Share of ransomware victim organisations that did not pay (2025); `A1_fraud_ai_evidence` row 23: Phishing share of breach initial access flat despite AI; `A2_hacking_ai_evidence` row 15: Verizon DBIR 2026: phishing's share of breach initial access 'barely moved' (16%) despite…

**Wikipedia (secondary; SPF data)**

- [Crime in Singapore (Wikipedia table attributing SPF annual scam statistics)](https://en.wikipedia.org/wiki/Crime_in_Singapore) · 2026 · grade B/C — `A1_fraud_series` rows 543–548, 589: SPF reported scam losses (2018–2023); SPF reported scam losses, Jan-Mar 2026 (2026)

**Wikipedia / Cyence**

- [Prior project event catalogue (Cyence via Wikipedia)](https://en.wikipedia.org/wiki/WannaCry_ransomware_attack) · 2017 · grade D — `A2_hacking_series` row 322: WannaCry economic loss (vendor model, 'up to') (2017)

**Wikipedia / Wired**

- [2017 Ukraine ransomware attacks (Wikipedia, citing Andy Greenberg, Wired)](https://en.wikipedia.org/wiki/2017_Ukraine_ransomware_attacks) · 2018 · grade C — `A2_hacking_series` row 321: NotPetya total damage (US government statement) (2017)

**WSJ via Wikipedia**

- [Audio deepfake (Wikipedia, citing WSJ 2019)](https://en.wikipedia.org/wiki/Audio_deepfake) · 2019 · grade C — `A1_fraud_ai_evidence` row 15: UK energy firm CEO-voice deepfake fraud

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**idtheftcenter.org**

- [https://www.idtheftcenter.org/2017-data-breaches/](https://www.idtheftcenter.org/2017-data-breaches/) — `A2_hacking_series` row 335: link written in the notes column

## Rows recorded without a link

The table has no source link for these rows; the notes column says why.

- `A1_fraud_series` row 540: Canadian Anti-Fraud Centre reported fraud losses (2023). Not retrieved (no 2023 CAFC annual report listed). Competition Bureau (Mar 2026): reported losses since 2022 exceed C$2.4bn, which implies 2023 \>= ~C$522m (2,400 - 530.4 - 643.7 - 704); CAFC publicity figure of ~C$569m for 2023…
