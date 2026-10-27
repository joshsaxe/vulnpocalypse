# Chart 4: Amdahl's law for a ransomware gang

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c04_amdahl.png`](../../figures/c04_amdahl.png) · code: [`charts/c04_amdahl.py`](../../charts/c04_amdahl.py)

No public dataset measures a ransomware gang's working hours by stage, so the eight stage judgements are the author's own. They draw on incident timelines (Colonial Pipeline, Ireland's health service, Change Healthcare, MGM and others), leaked gang chats, National Crime Agency data on LockBit's affiliates, Sophos, Mandiant and Coveware timing statistics, and AI-lab threat reports. This page lists the evidence tables behind those judgements (none of them is read by the chart script) and, at the end, the sources the judgements name without a link.

**Tables behind this chart**

- [`data/E_stage_judgements.csv`](../../data/E_stage_judgements.csv): 9 rows; read by the chart's scripts.
- [`data/E_stage_times.csv`](../../data/E_stage_times.csv): 23 rows; typed numbers checked against it by `tools/check_inputs.py`.
- [`data/E_incident_timelines.csv`](../../data/E_incident_timelines.csv): 11 rows; evidence behind the author's judgements; no script reads it.
- [`data/E_laundering.csv`](../../data/E_laundering.csv): 11 rows; evidence behind the author's judgements; no script reads it.
- [`data/I_business_models.csv`](../../data/I_business_models.csv): 20 rows; evidence behind the author's judgements; no script reads it.

**44 documents from 33 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Anthropic**

- [Detecting and countering misuse of AI: August 2025](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025) · 2025-08-27 · grade C — `I_business_models` rows 9, 10: AI-assisted RaaS development (no-code malware); AI-run data extortion (vibe hacking)
- [Disrupting the first reported AI-orchestrated cyber espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage) · 2025-11-13 · grade C — `I_business_models` row 16: Agent-driven espionage collection
- [Detecting and countering misuse of AI: September 2026](https://anthropic.com/threat-intelligence-report-september-2026) · 2026-09-10 · grade C — `I_business_models` row 17: Access-arbitrage economy (stolen keys, reseller fraud)

**BakerHostetler / SC Media**

- [Ransomware negotiations are taking longer, and that's a good thing](https://scworld.com/analysis/ransomware-negotiations-are-taking-longer-and-thats-a-good-thing) · 2022-04-07 · grade B — `E_stage_times` row 16: Negotiation: Typical negotiation duration (elapsed)

**BleepingComputer / GreyNoise**

- [AI-powered attack exploited PaperCut flaws to hack 395 organizations (GreyNoise)](https://bleepingcomputer.com/news/security/ai-powered-attack-exploited-papercut-flaws-to-hack-395-organizations) · 2026-09-10 · grade C — `E_incident_timelines` row 10: PaperCut mass-exploitation (AI-agent campaign)

**Chainalysis**

- [Total Ransomware Payments Stagnate for Second Consecutive Year (Chainalysis)](https://www.chainalysis.com/blog/crypto-ransomware-2026/) · 2026 · grade B/C — `E_stage_times` row 18: Payment: Payment rate; `I_business_models` rows 2, 7: Initial access broker (IAB); Phishing-as-a-service (PhaaS) platform
- [Crypto Theft Hits Record Highs in 2025 (Chainalysis)](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2026/) · 2026-02-01 · grade B — `E_laundering` rows 0, 1: North Korea - Bybit theft; North Korea - 2025 total theft
- [The On-Chain Laundering Economy (Chainalysis 2026)](https://www.chainalysis.com/blog/2026-crypto-money-laundering/) · 2026-02-01 · grade B — `E_laundering` rows 4, 5: Chinese-language money-laundering networks (CMLNs); Laundering channel speed ('time to $1bn')
- [Law enforcement dismantles AudiA6 laundering network (June 2026)](https://www.chainalysis.com/blog/law-enforcement-dismantles-audia6-laundering-network-june-2026/) · 2026-06-11 · grade C — `E_laundering` row 10: AudiA6 mixer-as-a-service (dismantled)

**Coveware**

- [Ransomware Marketplace Report Q4 2020](https://coveware.com/2021/02/ransomware-marketplace-report-q4-2020/) · 2021-02-01 · grade B — `I_business_models` rows 3, 4: Negotiator / extortion support; Data-leak-site operator
- [Insider Threats Loom while Ransom Payment Rates Plummet (Coveware Q3 2025)](https://coveware.com/2025/10/insider-threats-loom-while-ransom-payment-rates-plummet/) · 2025-10-24 · grade C — `E_stage_times` rows 17, 19: Payment: Payment rate; Payment: Median ransom payment
- [Adverse cyber extortions are more common than commonly advised (Coveware Q2 2026)](https://coveware.com/2026/07/adverse-cyber-extortions-are-more-common-than-commonly-advised/) · 2026-07-29 · grade C — `E_stage_times` rows 20, 21: Payment: Average ransom payment; Tactics present: Lateral movement present in cases

**Coveware / HIPAA Journal**

- [The average ransomware payment fell by 38% in Q2 2021 (Coveware via HIPAA Journal)](https://www.hipaajournal.com/the-average-ransomware-payment-fell-by-38-in-q2-2021/) · 2021-07-27 · grade C — `E_stage_times` row 22: Downtime: Average downtime after attack

**CrowdStrike**

- [CrowdStrike 2026 Global Threat Report](https://www.crowdstrike.com/en-us/global-threat-report/) · 2026-02-01 · grade C — `E_stage_times` row 15: Breakout: Average eCrime breakout time

**Cyber Monitoring Centre (UK)**

- [CMC Statement on ransomware incidents in the retail sector (June 2025)](https://cybermonitoringcentre.com/2025/06/20/cyber-monitoring-centre-statement-on-ransomware-incidents-in-the-retail-sector-june-2025/) · 2025-06-20 · grade B — `E_incident_timelines` row 8: Marks & Spencer and Co-op
- [CMC Statement on the Jaguar Land Rover cyber incident (October 2025)](https://cybermonitoringcentre.com/2025/10/22/cyber-monitoring-centre-statement-on-the-jaguar-land-rovercyber-incident-october-2025/) · 2025-10-22 · grade B — `E_incident_timelines` row 9: Jaguar Land Rover

**EclecticIQ**

- [GLOBAL GROUP: Emerging Ransomware-as-a-Service](https://blog.eclecticiq.com/global-group-emerging-ransomware-as-a-service) · 2025-07-15 · grade C — `I_business_models` row 11: AI negotiation bot (RaaS)

**Elliptic**

- [Behind the FBI Case Against Huione](https://www.elliptic.co/insights/behind-the-fbi-case-against-huione) · 2026-06-24 · grade C — `E_laundering` rows 6, 7: Huione Guarantee / Haowang (marketplace); Xinbi Guarantee (marketplace); `I_business_models` row 14: AI vendors in guarantee (escrow) markets
- [AI agents can now use a crypto mixer](https://www.elliptic.co/insights/ai-agents-can-now-use-a-crypto-mixer/) · 2026-10-15 · grade C — `I_business_models` row 18: Agentic laundering (early signal)

**Google GTIG**

- [Threat Actor Usage of AI Tools](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools) · 2025-11-05 · grade C — `I_business_models` row 15: Automated / AI-assisted initial access

**Health Service Executive / PwC**

- [Conti cyber attack on the HSE: Independent Post Incident Review (PwC)](https://www.hse.ie/eng/services/publications/conti-cyber-attack-on-the-hse-full-report.pdf) · 2021-12-10 · grade A — `E_incident_timelines` row 1: Ireland HSE

**Huntress / CSO Online**

- [Ransomware gangs extort victims 17 hours after intrusion on average (Huntress 2025 report)](https://www.csoonline.com/article/3825444/ransomware-gangs-extort-victims-17-hours-after-intrusion-on-average.html) · 2025-02-17 · grade C — `E_stage_times` row 13: Time to ransom: Average time from intrusion to ransom/extortion

**Krebs on Security**

- [Meet Paunch, accused author of the Blackhole Exploit Kit](https://krebsonsecurity.com/2013/12/meet-paunch-the-accused-author-of-the-blackhole-exploit-kit/) · 2013-12-06 · grade B — `I_business_models` row 6: Infrastructure / bulletproof hosting, crypters

**Mandiant / Google Cloud**

- [M-Trends 2026](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026) · 2026-03-23 · grade B — `E_stage_times` rows 10, 11: Overall intrusion: Global median dwell time; Initial access to hand-off: Median time initial access to hand-off to secondary group

**Microsoft**

- [Disrupting EvilTokens: the AI chatbot built for cybercrime](https://blogs.microsoft.com/on-the-issues/2026/09/22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/) · 2026-09-22 · grade B — `I_business_models` row 19: End-to-end AI-enabled BEC service

**NATO CCDCOE Cyber Law Toolkit**

- [2022 Costa Rica ransomware attack](https://cyberlaw.ccdcoe.org/wiki/Costa_Rica_ransomware_attack_%282022%29) · 2023-05-01 · grade B — `E_incident_timelines` row 2: Costa Rica government

**Palo Alto Networks Unit 42**

- [2026 Unit 42 Global Incident Response Report - Attacks Now 4x Faster](https://www.paloaltonetworks.com/blog/2026/02/unit-42-global-ir-report) · 2026-02-19 · grade C — `E_stage_times` row 12: Exfiltration: Fastest-case time from initial access to exfiltration

**Palo Alto Unit 42**

- [The Dilemma of AI: Malicious LLMs](https://unit42.paloaltonetworks.com/dilemma-of-ai-malicious-llms/) · 2025-11-25 · grade C — `I_business_models` row 8: Malicious inference / LLM-as-a-service

**Sophos**

- [2025 Sophos Active Adversary Report](https://www.sophos.com/en-us/blog/2025-sophos-active-adversary-report) · 2025-04-02 · grade C — `E_stage_times` rows 1, 2, 5, 7, 8: Overall intrusion: Median dwell time; Ransomware: Median dwell time (IR cases); Reach Active Directory: Median time from access to AD attempt; and 2 more
- [Sophos Active Adversary Report 2026](https://www.sophos.com/en-us/blog/2026-sophos-active-adversary-report) · 2026-02-24 · grade C — `E_stage_times` rows 0, 4, 9: Overall intrusion: Median dwell time; Reach Active Directory: Median time from access to AD attempt; Off-hours deployment: Ransomware payloads deployed outside business hours

**Sophos / HIPAA Journal**

- [Active Adversary Report for Tech Leaders 2023 (via HIPAA Journal)](https://www.hipaajournal.com/ransomware-groups-dwell-time-5-days/) · 2023-08-30 · grade C — `E_stage_times` rows 3, 6: Ransomware: Median dwell time; Reach Active Directory: Average time from access to AD/priv-esc

**Sysdig**

- [JADEPUFFER: Agentic ransomware for automated database extortion](https://sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) · 2026-07-01 · grade C — `I_business_models` row 12: Agentic ransomware (autonomous chain)

**The DFIR Report / SecurityWeek**

- [A 4-Hour Time to Ransom Seen as Accelerated Ransomware Attacks Increasingly Common](https://www.securityweek.com/4-hour-time-ransom-seen-quantum-attack-accelerated-ransomware-increasingly-common/amp/) · 2022-05-01 · grade C — `E_stage_times` row 14: Time to ransom: Fastest observed intrusion-to-encryption

**Trend Micro**

- [Back to the Hype: how cybercriminals are using GenAI](https://www.trendaisecurity.com/en-us/resources-insights/deep-research/back-to-the-hype-an-update-on-how-cybercriminals-are-using-genai) · 2024-05-08 · grade C — `I_business_models` row 13: Deepfake-as-a-service

**UK NCA**

- [LockBit leader unmasked and sanctioned](https://www.nationalcrimeagency.gov.uk/news/lockbit-leader-unmasked-and-sanctioned) · 2024-05-07 · grade A — `I_business_models` row 1: Affiliate / intruder

**US Department of Justice**

- [DOJ: Department of Justice Seizes $2.3 Million in Cryptocurrency Paid to Colonial Pipeline Extortionists](https://www.justice.gov/usao-ndca/pr/department-justice-seizes-23-million-cryptocurrency-paid-ransomware-extortionists) · 2021-06-08 · grade A — `E_incident_timelines` row 0: Colonial Pipeline; `E_laundering` row 2: Colonial Pipeline ransom (laundering + seizure)
- [Ukrainian Arrested and Charged with Ransomware Attack on Kaseya](https://www.justice.gov/opa/pr/ukrainian-arrested-and-charged-ransomware-attack-kaseya) · 2021-11-08 · grade A — `E_incident_timelines` row 3: Kaseya VSA (supply chain)

**US DOJ**

- [US Charges Russian National Developing/Operating LockBit](https://www.justice.gov/opa/pr/us-charges-russian-national-developing-and-operating-lockbit-ransomware) · 2024-05-07 · grade A — `I_business_models` row 0: RaaS operator / developer

**US FinCEN**

- [Financial Trend Analysis: Ransomware (BSA data 2022-2024)](https://www.fincen.gov/system/files/2025-12/FTA-Ransomware.pdf) · 2025 · grade A — `E_laundering` row 3: Ransomware payment rails (FinCEN BSA data); `I_business_models` row 5: Launderer / cash-out (mixers, exchanges)

**US House of Representatives**

- [Testimony of Andrew Witty, UnitedHealth Group (House Energy & Commerce)](https://democrats-energycommerce.house.gov/sites/evo-subsites/democrats-energycommerce.house.gov/files/evo-media-document/Testimony_Witty_OI_2024.05.01.pdf) · 2024-05-01 · grade A — `E_incident_timelines` row 4: Change Healthcare

**US SEC (Caesars)**

- [Caesars Entertainment, Inc. Form 8-K](https://www.sec.gov/Archives/edgar/data/1590895/000119312523235015/d537840d8k.htm) · 2023-09-14 · grade A — `E_incident_timelines` row 6: Caesars Entertainment

**US SEC (MGM Resorts)**

- [MGM Resorts International Form 8-K](https://www.sec.gov/Archives/edgar/data/789570/000119312523251667/d461062d8k.htm) · 2023-10-05 · grade A — `E_incident_timelines` row 5: MGM Resorts

**Wikipedia (citing Reuters, CNN, Anderson Economic Group)**

- [CDK Global (2024 cyberattack)](https://en.wikipedia.org/wiki/CDK_Global) · 2024-07-01 · grade C — `E_incident_timelines` row 7: CDK Global (auto-dealer SaaS)

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**Gambit Security**

- [Aurora ransomware targets ESXi, abuses Cursor agent for exploitation](https://gambit.security/blog-posts/aurora-ransomware-targets-esxi-abuses-cursor-agent-for-exploitation) — Evidence for the stage-2 judgement (foothold, discovery, privilege escalation, lateral movement): in this ransomware case an AI coding agent was used, but under human supervision and with most of its commands failing at the first try. *Used in:* data/E_stage_judgements.csv (stage 2: reasoning and key_sources); charts/c04_amdahl.py (note).

## Sources the stage judgements name without a link

These come from the `key_sources` column of `data/E_stage_judgements.csv`. Most correspond to documents listed above (Sophos, Coveware, Chainalysis, Mandiant, Anthropic and Google reports); `prior-project RC-nnn` means a row of the evidence library of the author's earlier study, *Where are all the agentic cyber attacks?* (see the [index](../BIBLIOGRAPHY.md#earlier-study)).

- 1. Target selection and access acquisition: Chainalysis 2026; M-Trends 2026; prior-project RANSOM_CARTEL (RC-099); Sophos AA 2026
- 2. Foothold, discovery, privilege escalation, lateral movement: Sophos AA 2026 (3.4h to AD); Gambit/Aurora 2026; GreyNoise PaperCut 2026; prior-project RC-100
- 3. Data collection, staging and exfiltration: Sophos AA 2026; Coveware Q2 2026; prior-project RC-101
- 4. Evasion, backup/hypervisor targeting, encryption deployment: Anthropic Aug 2025 (GTG-5004); Sophos AA 2026; prior-project RC-102
- 5. Victim research and extortion packaging, leak-site posting: GuidePoint GRIT Q2 2026; prior-project RC-103; Anthropic Aug 2025 (GTG-2002 note drafting)
- 6. Negotiation and pressure: Coveware Q2 2026; Chainalysis 2026; Axios/Picus (Global Group) 2025; BakerHostetler (8-day negotiations); prior-project RC-104
- 7. Payment verification, decryptor, laundering and cash-out, payouts: Chainalysis 2026 laundering report; FinCEN 2025; prior-project RC-105
- 8. Platform overhead: Prior-project RC-106; Conti/LockBit leak structure (NCA; Wired)
- AGGREGATE / Amdahl reading: Prior-project RANSOM_CARTEL model (processes.yaml, ransomware_ecosystem.md Q4); Chainalysis 2026; Coveware 2026

## Rows recorded without a link

The table has no source link for these rows; the notes column says why.

- `E_laundering` row 8: Garantex (exchange, seized) (grade D). RECALLED/UNVERIFIED this session (web-search budget exhausted; DOJ/Treasury primary not fetched). ~$26bn lifetime volume and Mar 2025 seizure widely reported; Conti/Black Basta proceeds linked (OFAC Apr 2022 cited ~$6m from…
- `E_laundering` row 9: Ronin Bridge theft (DPRK, 2022) (grade D). RECALLED/UNVERIFIED this session. ~$625m stolen Mar 2022, attributed to Lazarus; OFAC sanctioned the receiving wallet and Tornado Cash. CONFIRM figures/dates before publication.
