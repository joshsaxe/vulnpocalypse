# Chart 8: How far governments lag business

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c08_govlag.png`](../../figures/c08_govlag.png) · code: [`charts/c08_govlag.py`](../../charts/c08_govlag.py)

For each technology, a range of years in which it became mainstream in American business and a range in which it became mainstream in US defence and intelligence agencies, with the milestone used for each (a policy memo, a contract, a new organisation, a user count) taken from trade press, news reports and law-firm and encyclopaedia pages. Several of those milestones are named in the table's notes without a link; their pages are listed under *Cited outside the tables* below. Two grade-D rows (personal computers, corporate e-mail and web) were never sourced and are not used. The last row is a projection, not an observation.

**Tables behind this chart**

- [`data/G_adoption.csv`](../../data/G_adoption.csv): 10 rows; read by the chart's scripts.

**18 documents from 13 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Air Force Times / C4ISRNET**

- [Pentagon shattered speed record to give 1 million people remote work tools](https://www.airforcetimes.com/it-networks/2021/01/11/pentagon-shattered-speed-record-to-give-1-million-people-remote-work-tools) · 2021-01-11 · grade A — `G_adoption` row 5: SaaS / video conferencing

**CDO Magazine**

- [DoD's GenAI.mil hits 1.7M users](https://www.cdomagazine.tech/us-federal-news-bureau/dods-genai-mil-hits-1-7m-users-offering-a-blueprint-for-governing-ai-at-scale) · 2026-09-24 · grade B — `G_adoption` row 8: Generative AI (LLM chatbots)

**Defense One / Defense Systems**

- [Apple garners DISA approval for its mobile operating system](https://www.defenseone.com/defense-systems/2013/05/apple-garners-disa-approval-for-its-mobile-operating-system/190553) · 2013-05-17 · grade A — `G_adoption` row 4: Smartphones / mobile devices

**DefenseScoop**

- [Army cyber chief reveals AI task force building agents to hunt in the DoD networks](https://defensescoop.com/2026/08/19/army-cyber-chief-reveals-ai-task-force-building-agents-to-hunt-in-the-dod-networks/) · 2026-08-19 · grade B — `G_adoption` row 9: Agentic AI for offensive cyber

**Linux Journal**

- [Finally! SecDef signs Clarifying Guidance Regarding Open Source Software](https://www.linuxjournal.com/node/1008883) · 2009-10-27 · grade C — `G_adoption` row 2: Open-source software

**Washington Technology**

- [Amazon win restarts CIA cloud contract](https://washingtontechnology.com/articles/2013/10/08/amazon-cia-contract-resume.aspx) · 2013-10-08 · grade A — `G_adoption` row 3: Commercial cloud

**Wikipedia**

- [Kessel Run](https://en.wikipedia.org/wiki/Kessel_Run) · 2024 · grade C — `G_adoption` row 6: Agile / DevSecOps
- [Project Maven](https://en.wikipedia.org/wiki/Project_Maven) · 2026 · grade B — `G_adoption` row 7: Machine learning (production ML)

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**Breaking Defense**

- [CYBERCOM requests 2,660% increase in AI for cyber operations](https://breakingdefense.com/2026/05/cybercom-requests-2660-percent-increase-in-ai-for-cyber-operations/) · 2026-05-12 — US Cyber Command's first dedicated funding for AI in cyber operations: $5m in fiscal 2026 and a $138m request for fiscal 2027 (a 2,660% rise). Evidence that agencies began to work on AI agents for offensive cyber operations in 2026. *Used in:* G_adoption.csv row 9 (ns_milestone_desc and notes).

**DefenseScoop**

- [Pentagon awards AWS, Google, Microsoft and Oracle spots on JWCC](https://defensescoop.com/2022/12/07/pentagon-awards-aws-google-microsoft-and-oracle-spots-on-joint-warfighting-cloud-capability-solicitation/) · 2022-12-07 — The Joint Warfighting Cloud Capability multi-cloud contract (about $9bn) awarded on 7 December 2022 to four vendors: a milestone in the commercial-cloud row. *Used in:* G_adoption.csv row 3 (ns_milestone_desc and notes).
- [Defense Department establishes generative AI task force](https://defensescoop.com/2023/08/10/defense-department-generative-ai-task-force/) · 2023-08-10 — Task Force Lima (the Pentagon's Chief Digital and AI Office) set up on 10 August 2023: the first agency milestone in the generative-AI row. *Used in:* G_adoption.csv row 8 (ns_milestone_desc).

**Fortune**

- [Fortune, 28 Feb 2026 (on the OpenAI-Pentagon deal and Anthropic's supply-chain-risk designation)](https://fortune.com/2026/02/28/openai-pentagon-deal-anthropic-designated-supply-chain-risk-unprecedented-action-damage-its-growth) · 2026-02-28 — Cited in Chart 8's sources with the 1 September 2026 Fortune piece. The generative-AI row's notes cite Fortune for the frontier-AI contracts of up to $200m each that the Pentagon's AI office gave Anthropic, Google, OpenAI and xAI in July 2025 (the exact announcement date was not re-fetched). *Used in:* G_adoption.csv row 8 (ns_milestone_desc and notes).
- [Fortune, 1 Sep 2026 (on GenAI.mil's users)](https://www.fortune.com/2026/09/01/pentagon-chatgpt-grok-government-military-ai-members-pete-hegseth-defense-department/) · 2026-09-01 — GenAI.mil, the Pentagon's generative-AI platform, reaching about 1.7 million of about 3 million personnel (corroborates CDO Magazine, the row's own source). *Used in:* G_adoption.csv row 8 (notes).

**McKinsey & Company**

- [The state of AI in 2023: Generative AI's breakout year](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2023-generative-ais-breakout-year) — The private-sector side of the generative-AI row: 33% of organisations regularly using generative AI in at least one function (survey of April 2023). The row's notes also cite 65% from McKinsey's early-2024 survey, which has no separate link here. *Used in:* G_adoption.csv row 8 (private_milestone_desc and notes).

**Military Times**

- [Air Force's ChatGPT-like AI pilot draws 80k users in initial months](https://www.militarytimes.com/air/2024/09/16/air-forces-chatgpt-like-ai-pilot-draws-80k-users-in-initial-months/) · 2024-09-16 — The Air Force's NIPRGPT pilot, launched June 2024, with more than 80,000 users by September 2024. *Used in:* G_adoption.csv row 8 (ns_milestone_desc).

**Perkins Coie**

- [OMB launches FedRAMP initiative to increase efficiency in cloud (2011)](https://www.perkinscoie.com/en/news-insights/omb-launches-fedramp-initiative-to-increase-efficiency-in-cloud.html) — FedRAMP, the federal cloud-authorisation programme, launched on 8 December 2011 through an OMB memo. *Used in:* G_adoption.csv row 3 (ns_milestone_desc and notes).

**The Intercept**

- [The Army Wants to Sic AI Agents on Its Enemies](https://theintercept.com/2026/10/19/army-autonomous-ai-agents-arcyber/) · 2026-10-19 — Army Cyber Command's procurement of an autonomous offensive-cyber agent ('ECHOTRIBBLE', vendor selected 8 October 2026), described at newspaper level only. *Used in:* G_adoption.csv row 9 (ns_milestone_desc and notes).

**Wikipedia**

- [Chief Digital and Artificial Intelligence Office](https://en.wikipedia.org/wiki/Chief_Digital_and_Artificial_Intelligence_Office) — The Pentagon's AI office began operations on 1 June 2022, absorbing the Joint AI Center: a milestone in the production-ML row. *Used in:* G_adoption.csv row 7 (ns_milestone_desc and notes).

## Rows recorded without a link

The table has no source link for these rows; the notes column says why.

- `G_adoption` row 0: Personal computers / desktop PCs (grade D). GAP: could not source a specific DoD/IC desktop program-of-record date this turn (search budget exhausted). Private-side IBM PC 1981 is common knowledge but not independently fetched. Lag estimated ~5-10 yrs by analogy; treat as…
- `G_adoption` row 1: Corporate email & web/internet (grade D). GAP: NIPRNet/SIPRNet founding dates and corporate-email mainstream share not fetched this turn. Included for completeness; do not treat dates as sourced.
