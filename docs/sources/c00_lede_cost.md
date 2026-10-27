# Chart 0: The price of a hack (the lede figure)

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c00_lede_cost.png`](../../figures/c00_lede_cost.png) · code: [`charts/c00_lede_cost.py`](../../charts/c00_lede_cost.py)

Three automated jobs priced in AI tokens: finding a software flaw, breaking into an AI lab's code repository and building a browser exploit chain. Each number is one documented public case, not a market average, and all three are typed into `charts/c00_lede_cost.py` rather than read from a table. Only the automated part of each job is priced; much of a real attack is still done by hand.

**3 documents from 3 publishers.**

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**arXiv (Lu et al.)**

- [CyberGym (Lu et al., arXiv:2610.11602)](https://arxiv.org/abs/2610.11602) · 2026-10 — Cost per software flaw found by autonomous coding agents on real open-source C/C++ bugs: a cheap open model solved all 20 bugs for $4.38 (about $0.22 each); a frontier agent (Codex with GPT-5.5) solved 17 of 20 for $132.65 (about $7.80 each). *Used in:* charts/c00_lede_cost.py (COST, first row; docstring). tools/check_inputs.py redoes the division.

**Crypto Briefing (reporting XBOW)**

- [XBOW's full-chain Chrome exploit, via Crypto Briefing](https://cryptobriefing.com/xbow-gpt-5-6-chrome-exploit-bounty/) — About $40,000 in API fees for the six-day effort that produced a full-chain Chrome exploit, which Google later rewarded with its maximum bounty. *Used in:* charts/c00_lede_cost.py (COST, third row).

**Hacktron**

- [Hacking OpenAI](https://www.hacktron.ai/blog/hacking-openai) — The tokens spent on Hacktron's two-month project that reached OpenAI's internal code repository: 'less than $3,000 in tokens'. *Used in:* charts/c00_lede_cost.py (COST, second row).
