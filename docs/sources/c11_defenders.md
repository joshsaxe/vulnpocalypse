# Chart 11: The defenders' build-up

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c11_defenders.png`](../../figures/c11_defenders.png) · code: [`charts/c11_defenders.py`](../../charts/c11_defenders.py)

Left panel: a census of 34 security and platform vendors, each dated to its first substantive generative-AI security feature, from the vendor's own announcement or trade press (the vendor's page is the source; the feature grade A/B/C/none is the author's). Right panel: two typed spend judgements; the defensive anchors are two market-research houses' figures and the offensive guess rests on reporting about criminal AI tools. Those pages are listed under *Cited outside the tables* below.

**Tables behind this chart**

- [`data/G_vendor_ai.csv`](../../data/G_vendor_ai.csv): 34 rows; read by the chart's scripts.

**38 documents from 36 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**1Password**

- [1Password: none (no GenAI SOC/defender copilot; Watchtower is rule/ML)](https://blog.1password.com/) — `G_vendor_ai` row 33: no substantive security feature (feature grade none)

**Abnormal Security**

- [Abnormal Security: CheckGPT (core is behavioural ML)](https://www.businesswire.com/news/home/20230808611823/en/Abnormal-Announces-New-Capability-to-Detect-AI-Generated-Email-Attacks) — `G_vendor_ai` row 22: first substantive feature 2023-08 (feature grade B)

**Amazon/AWS**

- [Amazon/AWS: Detective GenAI summaries + Amazon Q](https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-detective-group-summaries-generative-ai) — `G_vendor_ai` row 4: first substantive feature 2023-11 (feature grade C)

**Atlassian**

- [Atlassian: none (Atlassian Intelligence is general-purpose; Guard is ML)](https://www.businesswire.com/news/home/20240201718713/en) — `G_vendor_ai` row 32: no substantive security feature (feature grade none)

**Bugcrowd**

- [Bugcrowd: AI Triage Assistant](https://www.bugcrowd.com/press-release/bugcrowd-unveils-new-ai-functionality-to-streamline-and-strengthen-security-resilience/) — `G_vendor_ai` row 30: first substantive feature 2025-12 (feature grade B)

**Check Point**

- [Check Point: Infinity AI Copilot](https://www.globenewswire.com/news-release/2024/01/31/2820683/0/en/check-point-software-unveils-infinity-ai-copilot-transforming-cyber-security-with-intelligent-genai-automation-and-support.html) — `G_vendor_ai` row 10: first substantive feature 2024-01 (feature grade B)

**Cisco**

- [Cisco: AI Assistant for Security](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2023/m12/cisco-redefines-cybersecurity-defense-with-powerful-portfolio-wide-artificial-intelligence-capabilities.html) — `G_vendor_ai` row 3: first substantive feature 2023-12 (feature grade B)

**Cloudflare**

- [Cloudflare: AI Assistant for Security Analytics](https://blog.cloudflare.com/security-analytics-ai-assistant) — `G_vendor_ai` row 6: first substantive feature 2024-03 (feature grade B)

**CrowdStrike**

- [CrowdStrike: Charlotte AI](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-introduces-charlotte-ai-to-deliver-generative-ai-powered-cybersecurity/) — `G_vendor_ai` row 2: first substantive feature 2023-05 (feature grade A)

**Darktrace**

- [Darktrace: Darktrace Heal (GenAI; core is legacy ML)](https://www.helpnetsecurity.com/2023/07/26/darktrace-heal/) — `G_vendor_ai` row 14: first substantive feature 2023-07 (feature grade B)

**Datadog**

- [Datadog: Bits AI Security Analyst](https://www.datadoghq.com/about/latest-news/press-releases/datadog-unveils-latest-ai-agents-to-rapidly-resolve-application-issues/) — `G_vendor_ai` row 27: first substantive feature 2025-06 (feature grade A)

**Dropbox**

- [Dropbox: none (Dash is general-purpose AI search, not security)](https://www.techtarget.com/enterprise-software/news/366623137/Dropbox-users-get-Dash-generative-AI-video-image-search) — `G_vendor_ai` row 31: no substantive security feature (feature grade none)

**Elastic Security**

- [Elastic Security: Elastic AI Assistant for Security](https://www.elastic.co/blog/introducing-elastic-ai-assistant) — `G_vendor_ai` row 19: first substantive feature 2023-05 (feature grade B)

**Fortinet**

- [Fortinet: Fortinet Advisor](https://fortinet.gcs-web.com/news-releases/news-release-details/meet-fortinet-advisor-generative-ai-assistant-accelerates-threat) — `G_vendor_ai` row 8: first substantive feature 2023-12 (feature grade B)

**GitHub**

- [GitHub: Copilot Autofix for code scanning](https://github.blog/2024/03/20/found-means-fixed-introducing-code-scanning-autofix-powered-by-github-copilot-and-codeql/) — `G_vendor_ai` row 25: first substantive feature 2024-03 (GA 2024-08) (feature grade B)

**GitLab**

- [GitLab: GitLab Duo (Explain/Resolve Vulnerability)](https://about.gitlab.com/blog/meet-gitlab-duo-the-suite-of-ai-capabilities/) — `G_vendor_ai` row 26: first substantive feature 2023-06 (feature grade B)

**Google/Mandiant**

- [Google/Mandiant: Security AI Workbench / Sec-PaLM → Gemini in Security](https://cloud.google.com/blog/products/identity-security/rsa-google-cloud-security-ai-workbench-generative-ai) — `G_vendor_ai` row 1: first substantive feature 2023-04 (feature grade A)

**HackerOne**

- [HackerOne: Hai (GenAI copilot)](https://www.hackerone.com/press-release/hackerone-leads-ai-driven-innovation-genai-copilot-and-ai-red-teaming) — `G_vendor_ai` row 29: first substantive feature 2024-02 (feature grade B)

**Microsoft**

- [Microsoft: Security Copilot](https://www.microsoft.com/en-us/security/blog/2024/03/13/microsoft-copilot-for-security-is-generally-available-on-april-1-2024-with-new-capabilities/) — `G_vendor_ai` row 0: first substantive feature 2023-03 (GA 2024-04) (feature grade A)

**Okta**

- [Okta: Okta AI (thin GenAI over ML)](https://www.okta.com/newsroom/press-releases/okta-introduces-okta-ai-securely-connecting-people-to-technology-ai-era/) — `G_vendor_ai` row 17: first substantive feature 2023-10 (feature grade C)

**Palo Alto Networks**

- [Palo Alto Networks: Precision AI copilots](https://www.paloaltonetworks.com/company/press/2024/palo-alto-networks-delivers-more-autonomous-cybersecurity-through-copilots-for-strata--prisma-and-cortex-platforms) — `G_vendor_ai` row 5: first substantive feature 2024-05 (feature grade B)

**Proofpoint**

- [Proofpoint: NexusAI (LLM detection)](https://www.csoonline.com/article/651232/proofpoint-unveils-new-features-to-break-cyberattack-chain.html) — `G_vendor_ai` row 18: first substantive feature 2024-05 (feature grade B)

**Rapid7**

- [Rapid7: AI Engine (generative AI)](https://www.rapid7.com/about/press-releases/rapid7s-ai-engine-supercharges-security-operations-with-generative-ai/) — `G_vendor_ai` row 13: first substantive feature 2024-06 (feature grade B)

**SecurityScorecard**

- [SecurityScorecard: GPT-4 security ratings](https://venturebeat.com/ai/rsac-2023-securityscorecard-launches-first-gpt-4-security-ratings-platform) — `G_vendor_ai` row 21: first substantive feature 2023-04 (feature grade B)

**SentinelOne**

- [SentinelOne: Purple AI](https://www.sentinelone.com/press/sentinelone-revolutionizes-cybersecurity-with-purple-ai/) — `G_vendor_ai` row 7: first substantive feature 2023-04 (feature grade A)

**Snyk**

- [Snyk: DeepCode AI Fix / Snyk Autofix](https://snyk.io/blog/ai-code-security-snyk-autofix-deepcode-ai/) — `G_vendor_ai` row 24: first substantive feature 2023-04 (feature grade B)

**Sophos**

- [Sophos: Sophos AI Assistant](https://www.sophos.com/en-us/blog/sophos-ai-assistant-accelerating-security-operations-with-genai) — `G_vendor_ai` row 15: first substantive feature 2025-02 (feature grade B)

**Splunk**

- [Splunk: Splunk AI Assistant](https://www.splunk.com/en_us/newsroom/press-releases/2023/conf23-splunk-introduces-new-ai-offerings-to-accelerate-detection-investigation-and-response-across-security-and-observability.html) — `G_vendor_ai` row 20: first substantive feature 2023-07 (feature grade B)

**Tenable**

- [Tenable: ExposureAI](https://www.tenable.com/press-releases/tenable-integrates-generative-ai-capabilities-across-cybersecurity-platform-with-exposure-ai) — `G_vendor_ai` row 12: first substantive feature 2023-08 (feature grade B)

**Trellix**

- [Trellix: Trellix Wise](https://www.helpnetsecurity.com/2024/05/03/trellix-wise/) — `G_vendor_ai` row 11: first substantive feature 2024-05 (feature grade A)

**Trend Micro**

- [Trend Micro: Trend Companion](https://newsroom.trendmicro.com/2023-11-27-Trend-Micro-First-to-Market-with-AI-powered-Cybersecurity-Assistant-for-Security-Teams) — `G_vendor_ai` row 16: first substantive feature 2023-11 (feature grade B)

**Vanta**

- [Vanta: Vanta AI](https://www.helpnetsecurity.com/2023/10/10/vanta-ai/) — `G_vendor_ai` row 28: first substantive feature 2023-10 (feature grade B)

**Wiz**

- [Wiz: AI-powered remediation guidance](https://www.wiz.io/blog/azure-ai-powered-remediation-guidance) — `G_vendor_ai` row 23: first substantive feature 2024-03 (feature grade B)

**Zscaler**

- [Zscaler: GenAI suite (Navigator etc.)](https://www.zscaler.com/press/zscaler-unveils-suite-cyber-solutions-designed-harness-full-potential-generative-ai) — `G_vendor_ai` row 9: first substantive feature 2023-06 (feature grade B)

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**Abnormal Security**

- [What happened to WormGPT and other criminal AI tools](https://abnormal.ai/blog/what-happened-to-wormgpt-cybercriminal-tools) — Criminal AI tools such as WormGPT turned out to be thin wrappers around mainstream models, or scams: the basis for the small, deliberately generous offensive-spend guess. *Used in:* charts/c11_defenders.py (OFF_M and docstring: typed judgement).

**Microsoft**

- [Security Copilot inclusion in Microsoft 365 E5 and E7 (Microsoft Learn)](https://learn.microsoft.com/en-us/copilot/security/security-copilot-inclusion) — Shows that Security Copilot is bundled into Microsoft 365 E5 and E7 licences. Context for the defensive-spend estimate; not an input to any calculation. *Used in:* Listed with Chart 11's sources.

**Mordor Intelligence**

- [Generative AI in cyber defence market](https://www.mordorintelligence.com/industry-reports/generative-artificial-intelligence-ai-in-cyber-defense-market) — Market-research estimate of the generative-AI cyber-defence market: $16.44bn (2025) and $20.58bn (2026). One of two anchors for the defensive-spend medians. *Used in:* charts/c11_defenders.py (DEF_BN and docstring: typed judgement anchored on it).

**Precedence Research**

- [AI security operations center market](https://www.precedenceresearch.com/ai-security-operations-center-market) — Market-research estimate of the AI security-operations-centre market: $19.45bn (2026). The second anchor for the defensive-spend medians. *Used in:* charts/c11_defenders.py (DEF_BN and docstring).
