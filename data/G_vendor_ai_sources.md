# Vendor census — first substantive generative-AI security feature (2022–2026)

Backing data for the "defenders' build-up" exhibit. Each vendor is dated to its FIRST post-ChatGPT substantive
generative/agentic security feature (not legacy machine learning). Grades: A = autonomous/agentic or deeply
integrated GenAI; B = LLM copilot/assistant at GA; C = announced/preview-heavy or thin; none = no substantive
security-specific GenAI (kept in the denominator). Modelled in charts/c11_defenders.py from data/G_vendor_ai.csv.

Counts: of 34 tracked, 31 have shipped a substantive feature. By first year: 2022: 0; 2023: 19; 2024: 9; 2025: 3;
2026: 0. By grade: A 6, B 23, C 2, none 3. Modelled cumulative (median, 80% CI): 2022 ~0; 2023 ~18 [16–19];
2024 ~26 [24–28]; 2025–26 ~29 [27–31].

| Vendor | Tier | Feature | First | Grade | Source |
|---|---|---|---|---|---|
| Microsoft | Platform | Security Copilot | 2023-03 (GA 2024-04) | A | https://www.microsoft.com/en-us/security/blog/2024/03/13/microsoft-copilot-for-security-is-generally-available-on-april-1-2024-with-new-capabilities/ |
| Google / Mandiant | Platform | Security AI Workbench / Sec-PaLM → Gemini in Security | 2023-04 | A | https://cloud.google.com/blog/products/identity-security/rsa-google-cloud-security-ai-workbench-generative-ai |
| CrowdStrike | Platform | Charlotte AI | 2023-05 | A | https://www.crowdstrike.com/en-us/press-releases/crowdstrike-introduces-charlotte-ai-to-deliver-generative-ai-powered-cybersecurity/ |
| Cisco | Platform | AI Assistant for Security | 2023-12 | B | https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2023/m12/cisco-redefines-cybersecurity-defense-with-powerful-portfolio-wide-artificial-intelligence-capabilities.html |
| Amazon / AWS | Platform | Detective GenAI summaries + Amazon Q | 2023-11 | C | https://aws.amazon.com/about-aws/whats-new/2023/11/amazon-detective-group-summaries-generative-ai |
| Palo Alto Networks | Platform | Precision AI copilots | 2024-05 | B | https://www.paloaltonetworks.com/company/press/2024/palo-alto-networks-delivers-more-autonomous-cybersecurity-through-copilots-for-strata--prisma-and-cortex-platforms |
| Cloudflare | Platform | AI Assistant for Security Analytics | 2024-03 | B | https://blog.cloudflare.com/security-analytics-ai-assistant |
| SentinelOne | Pure-play | Purple AI | 2023-04 | A | https://www.sentinelone.com/press/sentinelone-revolutionizes-cybersecurity-with-purple-ai/ |
| Fortinet | Pure-play | Fortinet Advisor | 2023-12 | B | https://fortinet.gcs-web.com/news-releases/news-release-details/meet-fortinet-advisor-generative-ai-assistant-accelerates-threat |
| Zscaler | Pure-play | GenAI suite (Navigator etc.) | 2023-06 | B | https://www.zscaler.com/press/zscaler-unveils-suite-cyber-solutions-designed-harness-full-potential-generative-ai |
| Check Point | Pure-play | Infinity AI Copilot | 2024-01 | B | https://www.globenewswire.com/news-release/2024/01/31/2820683/0/en/check-point-software-unveils-infinity-ai-copilot-transforming-cyber-security-with-intelligent-genai-automation-and-support.html |
| Trellix | Pure-play | Trellix Wise | 2024-05 | A | https://www.helpnetsecurity.com/2024/05/03/trellix-wise/ |
| Tenable | Pure-play | ExposureAI | 2023-08 | B | https://www.tenable.com/press-releases/tenable-integrates-generative-ai-capabilities-across-cybersecurity-platform-with-exposure-ai |
| Rapid7 | Pure-play | AI Engine (generative AI) | 2024-06 | B | https://www.rapid7.com/about/press-releases/rapid7s-ai-engine-supercharges-security-operations-with-generative-ai/ |
| Darktrace | Pure-play | Darktrace Heal (GenAI; core is legacy ML) | 2023-07 | B | https://www.helpnetsecurity.com/2023/07/26/darktrace-heal/ |
| Sophos | Pure-play | Sophos AI Assistant | 2025-02 | B | https://www.sophos.com/en-us/blog/sophos-ai-assistant-accelerating-security-operations-with-genai |
| Trend Micro | Pure-play | Trend Companion | 2023-11 | B | https://newsroom.trendmicro.com/2023-11-27-Trend-Micro-First-to-Market-with-AI-powered-Cybersecurity-Assistant-for-Security-Teams |
| Okta | Pure-play | Okta AI (thin GenAI over ML) | 2023-10 | C | https://www.okta.com/newsroom/press-releases/okta-introduces-okta-ai-securely-connecting-people-to-technology-ai-era/ |
| Proofpoint | Pure-play | NexusAI (LLM detection) | 2024-05 | B | https://www.csoonline.com/article/651232/proofpoint-unveils-new-features-to-break-cyberattack-chain.html |
| Elastic Security | Pure-play | Elastic AI Assistant for Security | 2023-05 | B | https://www.elastic.co/blog/introducing-elastic-ai-assistant |
| Splunk (Cisco) | Pure-play | Splunk AI Assistant | 2023-07 | B | https://www.splunk.com/en_us/newsroom/press-releases/2023/conf23-splunk-introduces-new-ai-offerings-to-accelerate-detection-investigation-and-response-across-security-and-observability.html |
| SecurityScorecard | Pure-play | GPT-4 security ratings | 2023-04 | B | https://venturebeat.com/ai/rsac-2023-securityscorecard-launches-first-gpt-4-security-ratings-platform |
| Abnormal Security | Pure-play | CheckGPT (core is behavioural ML) | 2023-08 | B | https://www.businesswire.com/news/home/20230808611823/en/Abnormal-Announces-New-Capability-to-Detect-AI-Generated-Email-Attacks |
| Wiz | Pure-play | AI-powered remediation guidance | 2024-03 | B | https://www.wiz.io/blog/azure-ai-powered-remediation-guidance |
| Snyk | Pure-play | DeepCode AI Fix / Snyk Autofix | 2023-04 | B | https://snyk.io/blog/ai-code-security-snyk-autofix-deepcode-ai/ |
| GitHub (Microsoft) | Adjacent | Copilot Autofix for code scanning | 2024-03 (GA 2024-08) | B | https://github.blog/2024/03/20/found-means-fixed-introducing-code-scanning-autofix-powered-by-github-copilot-and-codeql/ |
| GitLab | Adjacent | GitLab Duo (Explain/Resolve Vulnerability) | 2023-06 | B | https://about.gitlab.com/blog/meet-gitlab-duo-the-suite-of-ai-capabilities/ |
| Datadog | Adjacent | Bits AI Security Analyst | 2025-06 | A | https://www.datadoghq.com/about/latest-news/press-releases/datadog-unveils-latest-ai-agents-to-rapidly-resolve-application-issues/ |
| Vanta | Adjacent | Vanta AI | 2023-10 | B | https://www.helpnetsecurity.com/2023/10/10/vanta-ai/ |
| HackerOne | Adjacent | Hai (GenAI copilot) | 2024-02 | B | https://www.hackerone.com/press-release/hackerone-leads-ai-driven-innovation-genai-copilot-and-ai-red-teaming |
| Bugcrowd | Adjacent | AI Triage Assistant | 2025-12 | B | https://www.bugcrowd.com/press-release/bugcrowd-unveils-new-ai-functionality-to-streamline-and-strengthen-security-resilience/ |
| Dropbox | Adjacent | none (Dash is general-purpose AI search, not security) | n/a | none | https://www.techtarget.com/enterprise-software/news/366623137/Dropbox-users-get-Dash-generative-AI-video-image-search |
| Atlassian | Adjacent | none (Atlassian Intelligence is general-purpose; Guard is ML) | n/a | none | https://www.businesswire.com/news/home/20240201718713/en |
| 1Password | Adjacent | none (no GenAI SOC/defender copilot; Watchtower is rule/ML) | n/a | none | https://blog.1password.com/ |

Lower-confidence dates (modelled with wider spread): Elastic (month inferred from the 8.8 release), Wiz (earliest
GenAI touch uncertain), Snyk (beta 2023-04 firm, GA year inferred). Several grade-B vendors (Microsoft, CrowdStrike,
Google, SentinelOne, Palo Alto, Proofpoint, Bugcrowd) added agentic capabilities in 2025–26.
