# Chart 6: How fast criminals adopt new technology

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c06_attacker_lag.png`](../../figures/c06_attacker_lag.png) · code: [`charts/c06_attacker_lag.py`](../../charts/c06_attacker_lag.py)

Eighteen techniques, each dated by when its enabling technology became publicly available and when criminal use became widespread (the definition of 'widespread' is in each row), from court records, security-vendor and AI-lab reports, academic papers and encyclopaedias. Fifteen are charted; the other three (neural machine translation, agentic ransomware and browser cryptojacking) are left out, the last because its dates were recalled rather than checked. The sample is hand-picked from well-known cases, so the medians are illustrative.

**Tables behind this chart**

- [`data/I_adoption_lags.csv`](../../data/I_adoption_lags.csv): 18 rows; read by the chart's scripts.

**19 documents from 16 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Anthropic**

- [Detecting and countering misuse of AI: August 2025 (GTG-2002)](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025) · 2025-08-27 · grade C — `I_adoption_lags` row 15: Agentic intrusion / extortion

**Cloudflare**

- [Exploitation of CVE-2021-44228 before public disclosure](https://blog.cloudflare.com/exploitation-of-cve-2021-44228-before-public-disclosure-and-evolution-of-waf-evasion-patterns/) · 2021-12-14 · grade B — `I_adoption_lags` row 8: Mass exploitation of Log4Shell

**Coveware**

- [Ransomware Marketplace Report Q4 2020](https://coveware.com/2021/02/ransomware-marketplace-report-q4-2020/) · 2021-02-01 · grade B — `I_adoption_lags` row 4: Double extortion (steal + encrypt + leak)

**FinCEN**

- [FinCEN Alert on Fraud Schemes Involving Deepfake Media](https://www.fincen.gov/system/files/shared/FinCEN-Alert-DeepFakes-Alert508FINAL.pdf) · 2024-11-13 · grade A — `I_adoption_lags` row 10: Deepfake voice / audio impersonation fraud
- [Ransomware Trends in Bank Secrecy Act Data Between 2022 and 2024](https://www.fincen.gov/system/files/2025-12/FTA-Ransomware.pdf) · 2025 · grade A — `I_adoption_lags` row 1: Ransomware payments in Bitcoin

**Google**

- [A Neural Network for Machine Translation, at Production Scale](https://research.google/blog/a-neural-network-for-machine-translation-at-production-scale/) · 2016-09-27 · grade A — `I_adoption_lags` row 11: Neural machine translation for non-English phishing/BEC

**Google GTIG**

- [Threat Actor Usage of AI Tools (PROMPTFLUX, PROMPTSTEAL)](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools) · 2025-11-05 · grade C — `I_adoption_lags` row 14: LLM-in-the-loop / AI-generated malware

**IEEE (Young & Yung)**

- [Cryptovirology: Extortion-Based Security Threats and Countermeasures](https://www.ieee-security.org/TC/SP2020/tot-papers/young-1996.pdf) · 1996 · grade A — `I_adoption_lags` row 0: Cryptoviral extortion (public-key ransomware)

**Microsoft**

- [Ransomware-as-a-service: Understanding the cybercrime gig economy](https://www.microsoft.com/en-us/security/blog/2022/05/09/ransomware-as-a-service-understanding-the-cybercrime-gig-economy-and-how-to-protect-yourself/) · 2022-05-09 · grade C — `I_adoption_lags` row 3: Ransomware-as-a-service (RaaS)

**Palo Alto Unit 42**

- [The Dilemma of AI: Malicious LLMs](https://unit42.paloaltonetworks.com/dilemma-of-ai-malicious-llms/) · 2025-11-25 · grade C — `I_adoption_lags` row 13: Dedicated criminal LLMs (WormGPT, FraudGPT)

**Proofpoint**

- [Adylkuzz Cryptocurrency Mining Malware Spreading via EternalBlue/DoublePulsar](https://www.proofpoint.com/us/blog/threat-insight/adylkuzz-cryptocurrency-mining-malware-spreading-for-weeks-via-eternalblue-doublepulsar) · 2017-05-15 · grade B — `I_adoption_lags` row 7: EternalBlue-based worms (WannaCry, NotPetya)
- [Cobalt Strike: Favorite Tool from APT to Crimeware](https://www.proofpoint.com/us/blog/threat-insight/cobalt-strike-favorite-tool-apt-crimeware) · 2021-06-29 · grade B — `I_adoption_lags` row 5: Cobalt Strike as criminal C2 standard

**Sysdig**

- [JADEPUFFER: Agentic ransomware for automated database extortion](https://sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) · 2026-07-01 · grade C — `I_adoption_lags` row 16: Agentic ransomware (autonomous chain)

**USENIX Security (Soska & Christin)**

- [Measuring the Longitudinal Evolution of the Online Anonymous Marketplace Ecosystem](https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-soska-updated.pdf) · 2015 · grade B — `I_adoption_lags` row 2: Darknet drug/data markets on Tor

**Verizon**

- [2026 Data Breach Investigations Report](https://www.verizon.com/business/resources/T343/reports/2026-dbir-data-breach-investigations-report.pdf) · 2026 · grade B — `I_adoption_lags` row 12: LLM-written phishing/BEC text

**Wikipedia**

- [Mirai (malware)](https://en.wikipedia.org/wiki/Mirai_%28malware%29) · 2026 · grade C — `I_adoption_lags` row 9: IoT DDoS botnets (Mirai)

**Wikipedia (citing Trend Micro, RAND, BBC, Malwarebytes)**

- [Exploit kit](https://en.wikipedia.org/wiki/Exploit_kit) · 2026 · grade C — `I_adoption_lags` row 6: Commodity exploit kits

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**Anthropic**

- [Claude 3.7 Sonnet and Claude Code](https://www.anthropic.com/news/claude-3-7-sonnet) · 2025-02-24 — The date agentic coding tools became publicly available (Claude Code research preview, 24 February 2025): the start of the clock for 'agentic intrusion'. *Used in:* I_adoption_lags.csv row 15 (availability_date and notes); typed in charts/c06_attacker_lag.py (OPEN).

**US Department of Justice**

- [US leads multi-national action against GameOver Zeus botnet and CryptoLocker ransomware](https://www.justice.gov/opa/pr/us-leads-multi-national-action-against-gameover-zeus-botnet-and-cryptolocker-ransomware) · 2014-06-02 — CryptoLocker's scale: 234,000+ infected computers by April 2014, the row's definition of encrypt-and-ransom having 'scaled'. *Used in:* I_adoption_lags.csv row 0 (scaled_definition).

## Rows recorded without a link

The table has no source link for these rows; the notes column says why.

- `I_adoption_lags` row 17: Browser cryptojacking (Coinhive-style) (grade D). DATES RECALLED, NOT PRIMARY-VERIFIED THIS SESSION. Included only as a 'fast-then-collapsed' reference-class example; verify Coinhive launch (Sep 2017) and shutdown (Mar 2019) before print.
