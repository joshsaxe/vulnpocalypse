# Chart 7: Public versus private pay

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c07_pay.png`](../../figures/c07_pay.png) · code: [`charts/c07_pay.py`](../../charts/c07_pay.py)

State side: advertised pay scales and job adverts (NSA, GCHQ and the National Cyber Force, the NCSC), an official Israeli wage report (via Ynet) and a leaked salary sheet from i-Soon, a contractor to China's security ministries. Private side: Levels.fyi median total pay for machine-learning engineers in each country, and for engineers at OpenAI and Anthropic. These are advertised scales and self-reported pay, not payroll data, and the state figures are mostly averages for all staff, not engineers.

**Tables behind this chart**

- [`data/F_pay.csv`](../../data/F_pay.csv): 52 rows; read by the chart's scripts.

**37 documents from 18 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**AI Security Institute (Greenhouse job board)**

- [Expression of Interest - Core Technology Team (AI Security Institute)](https://job-boards.eu.greenhouse.io/aisi/jobs/5000476101) · 2026 · grade A — `F_pay` row 23: United Kingdom: UK AI Security Institute technical staff, levels 3-7 (base… (2026)

**Associated Press (Dake Kang, Zen Soo), syndicated by WJXT News4JAX**

- [Behind the doors of a Chinese hacking company, a sordid culture fueled by influence, alcohol and sex](https://www.news4jax.com/business/2024/03/08/behind-the-doors-of-a-chinese-hacking-company-a-sordid-culture-fueled-by-influence-alcohol-and-sex/) · 2024-03-08 · grade C — `F_pay` row 41: China: i-Soon (contract hacker for the MPS and MSS): most… (2022)

**Federal News Network**

- [Pentagon approves higher cyber pay for NSA, other defense intelligence agencies](https://federalnewsnetwork.com/pay/2023/08/pentagon-approves-higher-cyber-pay-for-nsa-other-defense-intelligence-agencies/) · 2023 · grade B — `F_pay` row 7: United States: DCIPS STEM/cyber Targeted Local Market Supplement (NSA… (2023)

**Flexa (mirror of the GCHQ / UK Intelligence Services advert)**

- [Computer Network Exploitation Roles Ref. 3864 (UK Intelligence Services)](https://flexa.careers/jobs/ukintelligenceservices-computer-network-exploitation-roles-ref-3864-6accbd1156fafcf1304df97a) · 2026 · grade B — `F_pay` row 19: United Kingdom: GCHQ / National Cyber Force computer network exploitation… (2026)
- [Exploitation Engineers Ref. 3851 (UK Intelligence Services)](https://flexa.careers/jobs/ukintelligenceservices-exploitation-engineers-ref-3851-6ab11c1139695170cc44f31b) · 2026 · grade B — `F_pay` row 18: United Kingdom: GCHQ Exploitation Engineers (Ref 3851), Cheltenham (2026)
- [Senior Data Scientist Ref. 3704 (UK Intelligence Services)](https://flexa.careers/jobs/ukia-senior-data-scientist-ref-3704-69d7f167d0b65d9f61a03f23) · 2026 · grade B — `F_pay` row 20: United Kingdom: GCHQ Senior Data Scientist (Ref 3704), Cheltenham (2026)
- [Senior Software Engineer Ref. 3839 (UK Intelligence Services)](https://flexa.careers/jobs/ukintelligenceservices-senior-software-engineer-ref-3839-6ab11c1139695170cc44f31a) · 2026 · grade B — `F_pay` row 17: United Kingdom: GCHQ Senior Software Engineer (Ref 3839)… (2026)

**Globes (citing the Central Bureau of Statistics)**

- [Average salary reaches NIS 14,677](https://en.globes.co.il/en/article-1001533964) · 2026-02-04 · grade B — `F_pay` row 38: Israel: Israeli high-tech sector: average monthly gross salary… (2025)

**Habr Career**

- [Почему зарплаты в IT перестали быстро расти и что это значит для карьеры](https://habr.com/ru/companies/habr_career/articles/1081998/) · 2026-09-14 · grade B — `F_pay` row 48: Russia: All IT specialists in Russia: median monthly salary, H1… (2026)
- [Где в IT зарплаты растут быстрее всего в 2026 году](https://habr.com/ru/companies/habr_career/articles/1083850/) · 2026-09-18 · grade B — `F_pay` row 49: Russia: Information-security specialists in Russia: median monthly… (2026)

**Levels.fyi**

- [Security Software Engineer Salary (United Kingdom)](https://www.levels.fyi/t/software-engineer/focus/security/locations/united-kingdom) · 2026-10-13 · grade C — `F_pay` row 25: United Kingdom: Security software engineer, total compensation… (2026)
- [Yandex Software Engineer Salaries](https://www.levels.fyi/companies/yandex/salaries/software-engineer) · 2026-10-13 · grade C — `F_pay` row 47: Russia: Yandex software engineer (Levels.fyi company median) (2026)
- [Software Engineer Salary (China)](https://www.levels.fyi/t/software-engineer/locations/china) · 2026-10-14 · grade C — `F_pay` rows 43, 44: China: ByteDance software engineer, China (Levels.fyi company… (2026); China: Alibaba software engineer, China (Levels.fyi company median) (2026)
- [Anthropic Software Engineer Salaries](https://www.levels.fyi/companies/anthropic/salaries/software-engineer) · 2026-10-20 · grade C — `F_pay` row 15: United States: Anthropic software engineer, all levels, total compensation (2026)
- [ML / AI Software Engineer Salary (China)](https://www.levels.fyi/t/software-engineer/focus/ml-ai/locations/china) · 2026-10-20 · grade C — `F_pay` row 42: China: ML/AI software engineer, total compensation (Levels.fyi… (2026)
- [ML / AI Software Engineer Salary (United States)](https://www.levels.fyi/t/software-engineer/focus/ml-ai) · 2026-10-20 · grade C — `F_pay` row 11: United States: ML/AI software engineer, total compensation (Levels.fyi, US) (2026)
- [OpenAI Software Engineer Salaries](https://www.levels.fyi/companies/openai/salaries/software-engineer) · 2026-10-20 · grade C — `F_pay` row 14: United States: OpenAI software engineer, all levels, total compensation (2026)
- [AI Engineer Salary (United States)](https://www.levels.fyi/t/software-engineer/title/ai-engineer) · 2026-10-21 · grade C — `F_pay` row 13: United States: 'AI Engineer' job title, total compensation (Levels.fyi, US) (2026)
- [ML / AI Software Engineer Salary (Israel)](https://www.levels.fyi/t/software-engineer/focus/ml-ai/locations/israel) · 2026-10-21 · grade C — `F_pay` row 39: Israel: ML/AI software engineer, total compensation (Levels.fyi… (2026)
- [ML / AI Software Engineer Salary (Russia)](https://www.levels.fyi/t/software-engineer/focus/ml-ai/locations/russia) · 2026-10-21 · grade C — `F_pay` row 45: Russia: ML/AI software engineer, total compensation (Levels.fyi… (2026)
- [ML / AI Software Engineer Salary (United Kingdom)](https://www.levels.fyi/t/software-engineer/focus/ml-ai/locations/united-kingdom) · 2026-10-21 · grade C — `F_pay` row 24: United Kingdom: ML/AI software engineer, total compensation (Levels.fyi, UK) (2026)
- [Security Software Engineer Salary (Israel)](https://www.levels.fyi/t/software-engineer/focus/security/locations/israel) · 2026-10-21 · grade C — `F_pay` row 40: Israel: Security software engineer, total compensation… (2026)
- [Security Software Engineer Salary (Russia)](https://www.levels.fyi/t/software-engineer/focus/security/locations/russia) · 2026-10-21 · grade C — `F_pay` row 46: Russia: Security software engineer, total compensation… (2026)
- [Security Software Engineer Salary (United States)](https://www.levels.fyi/t/software-engineer/focus/security) · 2026-10-21 · grade C — `F_pay` row 12: United States: Security software engineer, total compensation… (2026)
- [Software Engineer Salary (Iran)](https://www.levels.fyi/t/software-engineer/locations/iran) · 2026-10-21 · grade D — `F_pay` row 50: Iran: Software engineer, total compensation (Levels.fyi, Iran) (2026)

**Multilateral Sanctions Monitoring Team (hosted by Japan MOFA)**

- [The DPRK's Use of Overseas Labour to Violate and Evade UN Sanctions (MSMT/2026/1)](https://www.mofa.go.jp/files/101088307.pdf) · 2026-09-16 · grade B — `F_pay` row 51: North Korea: DPRK state-controlled IT workers abroad (mainly Russia and… (2025)

**The Decoder (citing Wired)**

- [Meta reportedly offers top OpenAI researchers up to $300 million over four years](https://the-decoder.com/meta-reportedly-offers-top-openai-researchers-up-to-300-million-over-four-years) · 2025-07-02 · grade D — `F_pay` row 16: United States: Meta Superintelligence Labs offers to top researchers… (2025)

**The New York Times (Scott Shane, Nicole Perlroth, David E. Sanger); read via a derechos.org reproduction**

- [Security Breach and Spilled Secrets Have Shaken the N.S.A. to Its Core](https://www.derechos.org/nizkor/espana/doc/nsa179.html) · 2017-11-12 · grade C — `F_pay` rows 9, 10: United States: NSA Tailored Access Operations (TAO): young hacker salary (2017); United States: Former NSA TAO hackers in private-sector security jobs (2017)

**The Record (Recorded Future News)**

- [DHS launches new effort to attract cybersecurity talent](https://therecord.media/dhs-launches-new-effort-to-attract-cybersecurity-talent/) · 2021-11-15 · grade B — `F_pay` row 8: United States: DHS Cybersecurity Talent Management System (CISA and DHS… (2021)

**The Register (Iain Thomson)**

- [UK needs cyber security professionals, but won't pay up](https://www.theregister.com/2024/10/29/gchq_needs_advanced_cybersecurity_professionals/) · 2024-10-29 · grade C — `F_pay` rows 21, 22, 26: United Kingdom: NCSC Lead cyber security expert, London (2024); United Kingdom: NCSC Senior cyber security expert, London (2024); United Kingdom: BAE Systems IT security manager (upper end, as reported) (2024)

**The Times of Israel (Shoshanna Solomon)**

- [IDF battles to keep its finest from defecting to private sector](https://www.timesofisrael.com/israel-army-battles-to-keep-its-best-from-high-tech-siren-song/) · 2016-10-27 · grade C — `F_pay` rows 30, 31, 36, 37: Israel: IDF career lieutenant in a technological post (pre-tax) (2016); Israel: IDF career captain in a technological post (pre-tax) (2016); Israel: Israeli high-tech offer to a recent Unit 8200 graduate (2016); and 1 more

**US Office of Personnel Management**

- [Salary Table 2026-DCB (Washington-Baltimore-Arlington locality)](https://www.opm.gov/policy-data-oversight/pay-leave/salaries-wages/salary-tables/26Tables/html/DCB.aspx) · 2026 · grade A — `F_pay` rows 2–5: United States: Federal General Schedule GS-12, steps 1-10… (2026); United States: Federal General Schedule GS-13, steps 1-10… (2026); United States: Federal General Schedule GS-14, steps 1-10… (2026); and 1 more
- [Salary Table No. 2026-EX](https://piv.opm.gov/policy-data-oversight/pay-leave/salaries-wages/salary-tables/26Tables/exec/pdf/EX.pdf) · 2026 · grade A — `F_pay` row 6: United States: Executive Schedule Level IV (statutory ceiling on GS base… (2026)

**USAJOBS (National Security Agency/Central Security Service)**

- [Network System Engineer - Entry to Expert Level (Maryland)](https://www.usajobs.gov/job/872079300) · 2026-06-08 · grade A — `F_pay` row 0: United States: NSA/CSS Network System Engineer, entry to expert (GG-7 to… (2026)

**USAJOBS Intelligence Careers (National Security Agency/Central Security Service)**

- [Computer Science & Engineering Professionals - Mid to Expert Level (Maryland)](https://intelligencecareers.usajobs.gov/job/869515000) · 2026-05-15 · grade A — `F_pay` row 1: United States: NSA/CSS Computer Science & Engineering Professionals, mid… (2026)

**ynet**

- [ynet (Hebrew): conscript pay rise from the January 2022 salary](https://www.ynet.co.il/news/article/hjpko119uy) · 2021-11-23 · grade B — `F_pay` rows 27–29: Israel: IDF conscript, rear/non-combat role (many Unit 8200 roles… (2022); Israel: IDF conscript, combat-support role (2022); Israel: IDF conscript, combat role (comparator); high = elite… (2022)

**Ynetnews (Gad Lior), reporting a Finance Ministry wage report**

- [For your eyes only: what do Israel's soldiers, spies and police really earn?](https://www.ynetnews.com/business/article/hyx5wo2pgg) · 2026-08-26 · grade B — `F_pay` rows 32–35: Israel: IDF young permanent-service (career) personnel: average… (2024); Israel: IDF permanent-service (career) personnel: average monthly… (2024); Israel: Mossad and Shin Bet: average gross monthly wage, all staff… (2024); and 1 more
