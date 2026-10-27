# Chart 5: How long abusers keep access to hosted AI

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c05_inference.png`](../../figures/c05_inference.png) · code: [`charts/c05_inference.py`](../../charts/c05_inference.py)

Disruption reports by OpenAI, Anthropic and Microsoft (2024-26), plus cases where no AI provider cut the operation off (self-hosted or resold models, criminal chatbots sold openly). The chart uses nine cases that were cut off and six that were not; the other rows in the table (influence operations, a model-copying campaign, bans at sign-up and two context rows) are not charted. Almost every row is grade C: a vendor describing its own detection, with no outside check and no denominator.

**Tables behind this chart**

- [`data/D_platform_cases.csv`](../../data/D_platform_cases.csv): 81 rows; read by the chart's scripts.

**51 documents from 20 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Abnormal Security / KELA**

- [GhostGPT: Uncensored AI Chatbot / KELA Dark AI](https://abnormal.ai/blog/ghostgpt-uncensored-ai-chatbot) · 2025-01-23 · grade C — `D_platform_cases` row 71: SVC-GHOSTGPT

**Amazon**

- [AI-augmented threat actor accesses FortiGate devices at scale](https://aws.amazon.com/blogs/security/ai-augmented-threat-actor-accesses-fortigate-devices-at-scale/) · 2026-02-20 · grade C — `D_platform_cases` row 76: AWS-2026-02-FORTIGATE

**Anthropic**

- [Anthropic Transparency Hub - Platform Security (Jul-Dec 2024)](https://www.anthropic.com/transparency/system-trust-reporting) · 2025 · grade A — `D_platform_cases` rows 45–48: ANT-TR-2024H2; ANT-TR-2025H1; ANT-TR-2025H2; ANT-TR-2026H1
- [Detecting and countering malicious uses of Claude: March 2025](https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025) · 2025-04-23 · grade C — `D_platform_cases` row 26: ANT-2025-03-IOSERVICE
- [Detecting and countering misuse of AI: August 2025](https://www-cdn.anthropic.com/b2a76c6f6992465c09a6f2fce282f6c0cea8c200.pdf) · 2025-08-27 · grade C — `D_platform_cases` rows 27–31: ANT-2025-08-GTG2002; ANT-2025-08-GTG5004; ANT-2025-08-VIETNAM; ANT-2025-08-CONTAGIOUS; and 1 more
- [Disrupting the first reported AI-orchestrated cyber espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage) · 2025-11-13 · grade C — `D_platform_cases` row 32: ANT-2025-11-GTG1002
- [Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks) · 2026-02-23 · grade C — `D_platform_cases` row 33: ANT-2026-02-DISTILL
- [What we learned mapping a year's worth of AI-enabled cyber threats](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack) · 2026-06-03 · grade B — `D_platform_cases` row 34: ANT-2026-06-832
- [Detecting and countering misuse of AI: September 2026](https://www.anthropic.com/threat-intelligence-report-september-2026) · 2026-09-10 · grade C — `D_platform_cases` rows 35–41, 44: ANT-2026-09-GTG20006; ANT-2026-09-GTG50014; ANT-2026-09-GTG10007; ANT-2026-09-GTG50020; and 4 more
- [GLM-5.3 and the spread of advanced cyber capabilities](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities) · 2026-09-29 · grade C — `D_platform_cases` row 78: ANT-2026-09-GLM53

**Anthropic (via Remio)**

- [Detecting and countering misuse of AI: September 2026 (via Remio summary)](https://www.remio.ai/post/anthropic-ai-dating-scam-exposed-a-human-ai-fraud-pipeline) · 2026-09-10 · grade C — `D_platform_cases` row 43: ANT-2026-09-GTG15001

**Anthropic (via The Next Web)**

- [Detecting and countering misuse of AI: September 2026](https://thenextweb.com/news/anthropic-claude-misuse-threat-intelligence-report) · 2026-09-10 · grade C — `D_platform_cases` row 42: ANT-2026-09-GTG50027

**CrowdStrike**

- [Unknown Threat Actor Uses ARTEX to Target South Korean Finance](https://www.crowdstrike.com/en-us/blog/unknown-threat-actor-uses-artex-to-target-south-korean-finance/) · 2026-10-07 · grade C — `D_platform_cases` row 77: CS-2026-10-ARTEX

**Google GTIG**

- [Adversarial Misuse of Generative AI](https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai) · 2025-01-29 · grade C — `D_platform_cases` row 50: GTIG-2025-01-GEMINI
- [GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools) · 2025-11-05 · grade C — `D_platform_cases` rows 51, 52: GTIG-2025-11-PROMPTSTEAL; GTIG-2025-11-OTHERS
- [GTIG AI Threat Tracker: Distillation, Experimentation, and (Continued) Integration](https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use) · 2026-02-12 · grade C — `D_platform_cases` rows 53, 72: GTIG-2026-02-DISTILL; SVC-XANTHOROX
- [Threat Actors are Increasingly Trying to Weaponize AI for Vulnerability Exploitation and Initial Access](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access) · 2026-05-11 · grade C — `D_platform_cases` row 54: GTIG-2026-05-ZERODAY
- [GTIG AI Threat Tracker: From Prompting to Autonomy](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai) · 2026-09-08 · grade C — `D_platform_cases` rows 55, 56: GTIG-2026-09-AUTONOMY; GTIG-2026-06-OUTSIDER

**Gressel et al. (USENIX Security 2026)**

- [Love, Lies, and Language Models: Investigating AI's Role in Romance-Baiting Scams](https://arxiv.org/html/2512.16280v1) · 2025-12-18 · grade B — `D_platform_cases` row 79: CTX-GRESSEL-COMPOUNDS

**Hugging Face**

- [Agent intrusion technical timeline](https://huggingface.co/blog/agent-intrusion-technical-timeline) · 2026-07-27 · grade A — `D_platform_cases` row 67: OAI-HF-2026-DETECT

**KrebsOnSecurity / Cato Networks**

- [Meet the Brains Behind the Malware-Friendly AI Chat Service WormGPT / Cato CTRL](https://krebsonsecurity.com/2023/08/meet-the-brains-behind-the-malware-friendly-ai-chat-service-wormgpt/) · 2023-08-08 · grade C — `D_platform_cases` row 68: SVC-WORMGPT

**Microsoft**

- [Staying ahead of threat actors in the age of AI](https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/) · 2024-02-14 · grade C — `D_platform_cases` row 57: MS-2024-02-STATE
- [Disrupting a global cybercrime operation abusing generative AI (Storm-2139)](https://blogs.microsoft.com/on-the-issues/2025/02/27/disrupting-cybercrime-abusing-gen-ai/) · 2025-02-27 · grade A — `D_platform_cases` row 58: MS-2025-02-STORM2139
- [Jasper Sleet: North Korean remote IT workers' evolving tactics](https://www.microsoft.com/en-us/security/blog/2025/06/30/jasper-sleet-north-korean-remote-it-workers-evolving-tactics-to-infiltrate-organizations/) · 2025-06-30 · grade C — `D_platform_cases` row 59: MS-2025-06-JASPERSLEET
- [SesameOp: Novel backdoor uses OpenAI Assistants API for C2](https://www.microsoft.com/en-us/security/blog/2025/11/03/sesameop-novel-backdoor-uses-openai-assistants-api-for-command-and-control/) · 2025-11-03 · grade C — `D_platform_cases` row 74: MS-2025-11-SESAMEOP
- [Storm-3168: agentic-driven cloud attacks using compromised service principals](https://www.microsoft.com/en-us/security/blog/2026/09/25/storm-3168-agentic-driven-cloud-attacks-using-compromised-service-principals/) · 2026-09-25 · grade C — `D_platform_cases` row 60: MS-2026-09-STORM3168

**Microsoft DCU**

- [Disrupting EvilTokens: the AI chatbot built for cybercrime](https://blogs.microsoft.com/on-the-issues/2026/09/22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/) · 2026-09-22 · grade A — `D_platform_cases` row 61: MS-2026-09-EVILTOKENS

**Netenrich / Cisco Talos**

- [FraudGPT: the villain avatar of ChatGPT / Cisco Talos](https://netenrich.com/blog/fraudgpt-the-villain-avatar-of-chatgpt) · 2023-07-25 · grade C — `D_platform_cases` row 69: SVC-FRAUDGPT

**OHCHR / UNODC**

- [OHCHR (Aug 2023) / UN News (Feb 2026); UNODC regional loss estimates](https://news.un.org/en/story/2026/02/1167012) · 2023-08-29 · grade E — `D_platform_cases` row 80: CTX-OHCHR-UNODC

**OpenAI**

- [Disrupting malicious uses of AI by state-affiliated threat actors](https://openai.com/index/disrupting-malicious-uses-of-ai-by-state-affiliated-threat-actors/) · 2024-02-14 · grade C — `D_platform_cases` row 0: OAI-2024-02-STATE
- [Disrupting deceptive uses of AI by covert influence operations (May 2024)](https://cdn.openai.com/threat-intelligence-reports/threat-intel-report-may-2024.pdf) · 2024-05-30 · grade C — `D_platform_cases` rows 1, 2: OAI-2024-05-ZEROZENO; OAI-2024-05-IO5
- [Influence and cyber operations: an update (October 2024)](https://cdn.openai.com/threat-intelligence-reports/influence-and-cyber-operations-an-update_October-2024.pdf) · 2024-10-09 · grade C — `D_platform_cases` rows 3, 4: OAI-2024-10-CYBER3; OAI-2024-10-TOTAL
- [Disrupting malicious uses of AI: cyber threat actors (February 2025)](https://openai.com/index/disrupting-malicious-uses-of-ai-cyber-threat-actors/) · 2025-02-01 · grade C — `D_platform_cases` row 7: OAI-2025-02-DPRKCYBER
- [Disrupting malicious uses of our models (February 2025)](https://cdn.openai.com/threat-intelligence-reports/disrupting-malicious-uses-of-our-models-february-2025-update.pdf) · 2025-02-21 · grade C — `D_platform_cases` rows 5, 6, 8, 9: OAI-2025-02-PEERREVIEW; OAI-2025-02-DPRKEMPLOY; OAI-2025-02-GHANA; OAI-2025-02-CAMBODIA
- [Disrupting malicious uses of AI (June 2025)](https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf) · 2025-06-05 · grade C — `D_platform_cases` rows 10–14: OAI-2025-06-SCOPECREEP; OAI-2025-06-APT5-APT15; OAI-2025-06-DPRKIT; OAI-2025-06-HIGHFIVE; and 1 more
- [Disrupting malicious uses of AI (October 2025)](https://cdn.openai.com/threat-intelligence-reports/7d662b68-952f-4dfd-a2f2-fe55b041cc4a/disrupting-malicious-uses-of-ai-october-2025.pdf) · 2025-10-07 · grade C — `D_platform_cases` rows 15–18: OAI-2025-10-TOTAL; OAI-2025-10-RUMALWARE; OAI-2025-10-UTA0388; OAI-2025-10-SCAMS
- [Disrupting malicious uses of AI (February 2026)](https://cdn.openai.com/pdf/df438d70-e3fe-4a6c-a403-ff632def8f79/disrupting-malicious-uses-of-ai.pdf) · 2026-02-25 · grade C — `D_platform_cases` rows 19, 20: OAI-2026-02-DATEBAIT; OAI-2026-02-CYBERSPECOPS
- [Disrupting malicious uses of AI (June 2026)](https://cdn.openai.com/pdf/96b559fa-c165-4575-805d-e636909e2f78/June-2026-Threat-Report.pdf) · 2026-06-10 · grade C — `D_platform_cases` row 21: OAI-2026-06-PRCIO
- [Disrupting a Cambodia-based criminal scam operation](https://openai.com/index/disrupting-malicious-uses-of-ai-criminal-scam-operation/) · 2026-07-31 · grade C — `D_platform_cases` row 22: OAI-2026-07-POIPET
- [Disrupting a new covert influence campaign from Russia](https://openai.com/index/disrupting-malicious-uses-of-ai-influence-campaign-russia/) · 2026-08-25 · grade C — `D_platform_cases` row 23: OAI-2026-08-BURKE
- [Disrupting a coordinated model-distillation campaign](https://openai.com/index/disrupting-a-coordinated-model-distillation-campaign/) · 2026-09-30 · grade C — `D_platform_cases` row 24: OAI-2026-09-DISTILL
- [Disrupting AI-enabled 'false front' operations](https://openai.com/index/disrupting-ai-enabled-false-front-operations/) · 2026-10-08 · grade C — `D_platform_cases` row 25: OAI-2026-10-FALSEFRONT

**OpenAI / Hugging Face / METR / Redwood**

- [The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) · 2026-07-21 · grade B — `D_platform_cases` row 66: OAI-HF-2026-SWARM

**Palo Alto Unit 42**

- [The Dilemma of AI: Malicious LLMs](https://unit42.paloaltonetworks.com/dilemma-of-ai-malicious-llms/) · 2025-11-25 · grade C — `D_platform_cases` row 70: SVC-WORMGPT4

**SentinelOne**

- [AkiraBot: AI-Powered Bot Bypasses CAPTCHAs, Spams Websites at Scale](https://www.sentinelone.com/labs/akirabot-ai-powered-bot-bypasses-captchas-spams-websites-at-scale/) · 2025-04-09 · grade C — `D_platform_cases` row 73: OAI-2025-04-AKIRABOT
- [Prompts as Code, Embedded Keys: The Hunt for LLM-Enabled Malware](https://www.sentinelone.com/labs/prompts-as-code-embedded-keys-the-hunt-for-llm-enabled-malware/) · 2025-09-19 · grade C — `D_platform_cases` row 75: SENT-2025-09-MALTERMINAL

**Sysdig**

- [LLMjacking: Stolen Cloud Credentials Used in New AI Attack](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/) · 2024-05-06 · grade C — `D_platform_cases` row 62: SYS-2024-05-LLMJACK
- [The Growing Dangers of LLMjacking](https://sysdig.com/blog/growing-dangers-of-llmjacking/) · 2024-09-18 · grade C — `D_platform_cases` row 63: SYS-2024-09-LLMJACK
- [LLMjacking targets DeepSeek](https://sysdig.com/blog/llmjacking-targets-deepseek/) · 2025-02-07 · grade C — `D_platform_cases` row 64: SYS-2025-02-DEEPSEEK
- [JADEPUFFER: agentic ransomware for automated database extortion](https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) · 2026-07-01 · grade C — `D_platform_cases` row 65: SYS-2026-07-JADEPUFFER

**Verizon (Anthropic data)**

- [2026 Data Breach Investigations Report](https://www.verizon.com/business/resources/T343/reports/2026-dbir-data-breach-investigations-report.pdf) · 2026 · grade B — `D_platform_cases` row 49: ANT-DBIR-793
