# Chart 9: How long state hackers stay hidden

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c09_state_patience.png`](../../figures/c09_state_patience.png) · code: [`charts/c09_state_patience.py`](../../charts/c09_state_patience.py)

Well-documented state-linked campaigns, each with the time from first intrusion to discovery and, where it was reported, how many of the systems reached were actually worked, from government advisories, vendor incident write-ups (Microsoft, Mandiant, Kaspersky and others) and press reports. The 14-day benchmark for all intrusions is one row of `E_stage_times`. Campaigns still hidden are missing from the sample by construction.

**Tables behind this chart**

- [`data/H_espionage_cases.csv`](../../data/H_espionage_cases.csv): 21 rows; read by the chart's scripts.
- [`data/E_stage_times.csv`](../../data/E_stage_times.csv): 1 row (of the 23 in the file; the others feed other charts); typed numbers checked against it by `tools/check_inputs.py`.

**32 documents from 26 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Anthropic**

- [Disrupting the first reported AI-orchestrated cyber espionage campaign (full report)](https://www-cdn.anthropic.com/d7dd50dd1185f59be051b307150d877f2b82bd2c.pdf) · 2025-11-13 · grade C — `H_espionage_cases` row 20: Contrast: GTG-1002 AI-orchestrated espionage (Claude Code)
- [Investigating incidents from our cybersecurity evaluations](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals) · 2026-07-30 · grade C — `H_espionage_cases` row 19: Contrast: Anthropic evaluation incidents (AI agents reached real…

**CISA, NSA, FBI and partners**

- [People's Republic of China State-Sponsored Cyber Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure (AA24-038A)](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a) · 2024-02-07 · grade A — `H_espionage_cases` row 2: Volt Typhoon

**Cyber Safety Review Board (DHS)**

- [Review of the Summer 2023 Microsoft Exchange Online Intrusion](https://www.cisa.gov/sites/default/files/2024-04/CSRB_Review_of_the_Summer_2023_MEO_Intrusion_Final_508c.pdf) · 2024-03-20 · grade A — `H_espionage_cases` row 11: Storm-0558 (Microsoft Exchange Online)

**FireEye/Mandiant (Google Cloud)**

- [Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor](https://cloud.google.com/blog/topics/threat-intelligence/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor) · 2020-12-13 · grade B — `H_espionage_cases` row 1: SolarWinds SUNBURST - tradecraft source

**Google Threat Intelligence Group / Mandiant**

- [Ghost in the Router: China-Nexus Espionage Actor UNC3886 Targets Juniper Routers](https://cloud.google.com/blog/topics/threat-intelligence/china-nexus-espionage-targets-juniper-routers) · 2025-03-12 · grade B — `H_espionage_cases` row 15: UNC3886 (Juniper routers; Singapore)
- [Another BRICKSTORM: Stealthy Backdoor Enabling Espionage into Tech and Legal Sectors](https://cloud.google.com/blog/topics/threat-intelligence/brickstorm-espionage-campaign) · 2025-09-24 · grade B — `H_espionage_cases` row 14: UNC5221 BRICKSTORM

**Hugging Face**

- [Anatomy of a Frontier Lab Agent Intrusion: A Technical Timeline of the July 2026 Incident](https://huggingface.co/blog/agent-intrusion-technical-timeline) · 2026-07-27 · grade A — `H_espionage_cases` row 18: Contrast: OpenAI evaluation agent swarm vs Hugging Face (AI agents…

**Kaspersky Lab**

- [Equation Group: Questions and Answers (v1.5)](https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2018/03/08064459/Equation_group_questions_and_answers.pdf) · 2015-02 · grade B — `H_espionage_cases` row 4: Equation Group (EquationDrug/GrayFish/DoubleFantasy)
- [The Mystery of Duqu 2.0: a sophisticated cyberespionage actor returns (v2.1)](https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2018/03/07205202/The_Mystery_of_Duqu_2_0_a_sophisticated_cyberespionage_actor_returns.pdf) · 2015-06-11 · grade B — `H_espionage_cases` row 7: Duqu 2.0

**Kaspersky Lab (Securelist)**

- [Regin: nation-state ownage of GSM networks](https://securelist.com/regin-nation-state-ownage-of-gsm-networks/67741/) · 2014-11-24 · grade B — `H_espionage_cases` row 5: Regin

**Kaspersky Lab (via Wikipedia)**

- [The Flame: Questions and Answers (via Wikipedia hub)](https://securelist.com/the-flame-questions-and-answers/34344/) · 2012-05-28 · grade C — `H_espionage_cases` row 6: Flame (sKyWIper)

**Mandiant (Google Cloud)**

- [M-Trends 2025](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2025) · 2025-04-23 · grade B — `H_espionage_cases` row 17: Mandiant M-Trends 2025: dwell by detection source benchmark
- [M-Trends 2026](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2026) · 2026-03-23 · grade B — `H_espionage_cases` row 16: Mandiant M-Trends 2026: espionage dwell time benchmark; `E_stage_times` row 10: Overall intrusion: Global median dwell time

**Microsoft MSRC**

- [Update on Microsoft Actions Following Attack by Nation State Actor Midnight Blizzard](https://www.microsoft.com/en-us/msrc/blog/2024/03/update-on-microsoft-actions-following-attack-by-nation-state-actor-midnight-blizzard) · 2024-03-08 · grade A — `H_espionage_cases` row 12: Midnight Blizzard vs Microsoft corporate email

**NBC News**

- [China used three private companies to hack global telecoms U.S. says](https://www.nbcnews.com/tech/security/china-used-three-private-companies-hack-global-telecoms-us-says-rcna227543) · 2025-08-27 · grade B — `H_espionage_cases` row 3: Salt Typhoon

**NSA**

- [US Agencies and Allies Partner to Identify Russian Snake Malware Infrastructure](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/3389044/us-agencies-and-allies-partner-to-identify-russian-snake-malware-infrastructure/) · 2023-05-09 · grade A — `H_espionage_cases` row 8: Turla Snake (Operation MEDUSA)

**The White House**

- [Press Briefing by Press Secretary Jen Psaki and Deputy National Security Advisor Anne Neuberger](https://bidenwhitehouse.archives.gov/briefing-room/press-briefings/2021/02/17/press-briefing-by-press-secretary-jen-psaki-and-deputy-national-security-advisor-for-cyber-and-emerging-technology-anne-neuberger-february-17-2021/) · 2021-02-17 · grade A — `H_espionage_cases` row 0: SolarWinds SUNBURST (StellarParticle/UNC2452)

**US Department of Justice**

- [Two Chinese Hackers Associated With the Ministry of State Security Charged with Global Computer Intrusion Campaigns](https://www.justice.gov/archives/opa/pr/two-chinese-hackers-associated-ministry-state-security-charged-global-computer-intrusion) · 2018-12-20 · grade A — `H_espionage_cases` row 9: APT10 Cloud Hopper

**US House Committee on Oversight and Government Reform**

- [The OPM Data Breach: How the Government Jeopardized Our National Security for More than a Generation](https://oversight.house.gov/wp-content/uploads/2016/09/The-OPM-Data-Breach-How-the-Government-Jeopardized-Our-National-Security-for-More-than-a-Generation.pdf) · 2016-09-07 · grade B — `H_espionage_cases` row 10: OPM breach

**Volexity**

- [Ivanti Connect Secure VPN Exploitation Goes Global](https://www.volexity.com/blog/2024/01/15/ivanti-connect-secure-vpn-exploitation-goes-global/) · 2024-01-15 · grade B — `H_espionage_cases` row 13: UNC5221 Ivanti Connect Secure zero-days (2023-24)

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**blogs.microsoft.com**

- [https://blogs.microsoft.com/on-the-issues/2020/12/17/cyberattacks-cybersecurity-solarwinds-fireeye/](https://blogs.microsoft.com/on-the-issues/2020/12/17/cyberattacks-cybersecurity-solarwinds-fireeye/) — `H_espionage_cases` row 1: link written in the notes column

**cbsnews.com**

- [https://www.cbsnews.com/news/solarwinds-hack-russia-cyberattack-60-minutes-2021-02-14/](https://www.cbsnews.com/news/solarwinds-hack-russia-cyberattack-60-minutes-2021-02-14/) — `H_espionage_cases` row 1: link written in the notes column

**cloud.google.com**

- [https://cloud.google.com/blog/topics/threat-intelligence/ivanti-connect-secure-vpn-zero-day](https://cloud.google.com/blog/topics/threat-intelligence/ivanti-connect-secure-vpn-zero-day) — `H_espionage_cases` row 13: link written in the notes column

**crowdstrike.com**

- [https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/](https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/) — `H_espionage_cases` row 1: link written in the notes column

**csis.org**

- [https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents](https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents) — `H_espionage_cases` row 15: link written in the notes column

**en.wikipedia.org**

- [https://en.wikipedia.org/wiki/Flame_(malware](https://en.wikipedia.org/wiki/Flame_%28malware) — `H_espionage_cases` row 6: link written in the notes column
- [https://en.wikipedia.org/wiki/Office_of_Personnel_Management_data_breach](https://en.wikipedia.org/wiki/Office_of_Personnel_Management_data_breach) — `H_espionage_cases` row 10: link written in the notes column

**microsoft.com**

- [https://www.microsoft.com/en-us/msrc/blog/2024/01/microsoft-actions-following-attack-by-nation-state-actor-midnight-blizzard](https://www.microsoft.com/en-us/msrc/blog/2024/01/microsoft-actions-following-attack-by-nation-state-actor-midnight-blizzard) — `H_espionage_cases` row 12: link written in the notes column
- [https://www.microsoft.com/en-us/security/blog/2023/05/24/volt-typhoon-targets-us-critical-infrastructure-with-living-off-the-land-techniques/](https://www.microsoft.com/en-us/security/blog/2023/05/24/volt-typhoon-targets-us-critical-infrastructure-with-living-off-the-land-techniques/) — `H_espionage_cases` row 2: link written in the notes column

**nsa.gov**

- [https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4287371/nsa-and-others-provide-guidance-to-counter-china-state-sponsored-actors-targeti/](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4287371/nsa-and-others-provide-guidance-to-counter-china-state-sponsored-actors-targeti/) — `H_espionage_cases` row 3: link written in the notes column

**solarwinds.com**

- [https://www.solarwinds.com/blog/new-findings-from-our-investigation-of-sunburst](https://www.solarwinds.com/blog/new-findings-from-our-investigation-of-sunburst) — `H_espionage_cases` row 1: link written in the notes column
