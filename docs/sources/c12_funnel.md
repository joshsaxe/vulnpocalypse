# Chart 12: AI-found flaws, from discovery to patch

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c12_funnel.png`](../../figures/c12_funnel.png) · code: [`charts/c12_funnel.py`](../../charts/c12_funnel.py)

The funnel comes from Anthropic's coordinated-disclosure dashboard (2 October 2026) and the exploitation rate from VulnCheck's tracker of AI-attributed vulnerabilities; the counts are typed into the script and checked against `J_ai_vulns.csv`. Each headline count has a single source, which is the organisation that runs the programme or tracker. The other documents are background on AI-found flaws.

**Tables behind this chart**

- [`data/J_ai_vulns.csv`](../../data/J_ai_vulns.csv): 12 rows; typed numbers checked against it by `tools/check_inputs.py`.

**8 documents from 7 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**Anthropic**

- [Project Glasswing: an initial update](https://anthropic.com/research/glasswing-initial-update) · 2026-05-22 · grade C — `J_ai_vulns` rows 5, 6: Glasswing partners: 10000+ serious bugs in a month; open-source scan: 23019 findings
- [Anthropic coordinated vulnerability disclosure dashboard](https://red.anthropic.com/2026/cvd/) · 2026-10-02 · grade B — `J_ai_vulns` rows 7, 8: 6157 reported to maintainers; 516 patched upstream

**DARPA**

- [AIxCC results](https://www.darpa.mil/news/2025/aixcc-results) · 2025-08-08 · grade A — `J_ai_vulns` row 2: DARPA challenge: 18 real bugs

**Google Threat Intelligence Group**

- [GTIG: AI vulnerability exploitation for initial access](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access) · 2026-05-11 · grade C — `J_ai_vulns` row 11: first AI-built zero-day exploit (intercepted)

**Schneier on Security (quoting AISLE)**

- [AI Found Twelve New Vulnerabilities in OpenSSL](https://www.schneier.com/blog/archives/2026/02/ai-found-twelve-new-vulnerabilities-in-openssl.html) · 2026-02 · grade C — `J_ai_vulns` row 3: AISLE: all 12 OpenSSL bugs

**TechRadar**

- [Google's new AI-powered bug hunting tool finds major issues in open source software](https://www.techradar.com/pro/security/googles-new-ai-powered-bug-hunting-tool-finds-major-issues-in-open-source-software) · 2025-08-05 · grade B — `J_ai_vulns` rows 0, 1: Big Sleep's first real bug; Big Sleep: 20 bugs

**The Hacker News**

- [Claude Opus 4.6 Finds 500+ High-Severity Flaws](https://thehackernews.com/2026/02/claude-opus-46-finds-500-high-severity.html) · 2026-02-06 · grade C — `J_ai_vulns` row 4: Claude Opus 4.6: 500+ flaws

**VulnCheck**

- [State of Exploitation 1H 2026](https://www.vulncheck.com/blog/state-of-exploitation-1h-2026) · 2026-07-28 · grade B — `J_ai_vulns` rows 9, 10: 1061 AI-found bugs tracked; 14 exploited in the wild
