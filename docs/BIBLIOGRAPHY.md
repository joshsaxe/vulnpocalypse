# Annotated bibliography

Where every number in the figures comes from. Each chart has a page listing the documents behind it, grouped by publisher, with what was taken from each one and which rows of which table it fed. The same list is in [`data/sources.csv`](../data/sources.csv), one row per chart and document, for sorting and filtering. A document that feeds two charts appears on both pages.

**563 distinct documents from 264 publishers** across the 13 figures. This list is built by [`tools/build_bibliography.py`](../tools/build_bibliography.py) from the `source_url` column of each data table, the links written in the tables' notes columns, and [`data/extra_sources.csv`](../data/extra_sources.csv) (documents that numbers were typed from). It contains every link in the post's list of chart sources, and more: the tables cite some documents that the post's shorter list leaves out. The sources for the post's *text* are cited in the post itself.

## How reliable is this?

- The data tables were compiled by AI research agents working from public web sources in October 2026, under a brief that told them to open every page they took a number from, to prefer primary sources, to grade each data point and never to invent a number, date or source. They were **not reviewed row by row by a human or by an independent party**. The `notes` column of each table says where a page could not be opened, where a figure was relayed second-hand, and where the agents disagreed with each other.
- Not every link has been re-fetched for this repository. Links rot: if one has gone, search for the title, or try the Internet Archive's Wayback Machine.
- Many numbers are echoes of a single source. The grade says how good that source is, not how many repeat it.
- The newest evidence, on AI misuse and AI-found flaws, is mostly grade C or B: vendors and AI labs describing their own detections, with no outside check and no denominator.

## Grades

Every row in the tables carries the grade of its source:

- **A**: official statistic, court record or primary disclosure
- **B**: peer-reviewed paper, or a reputable industry report that states its method
- **C**: vendor or press report with a thin method
- **D**: rumour, a single anonymous source, or dates recalled rather than checked
- **E**: not verified at the primary source and relayed by secondary coverage (one row)

The grade describes the *source*, not the claim. Chart 7 uses it to set how much each pay figure counts (grade A 0.15, B 0.25, C 0.40, D 0.60 as the standard deviation of the log of pay). In `G_vendor_ai`, which has no source grade, a separate A/B/C/none grade describes the vendor's *feature* (A: autonomous or deeply integrated generative AI; B: an assistant or copilot generally available; C: announced or thin; none: nothing substantive).

## By chart

| Chart | Page | Documents | Publishers | Rows by grade (A / B / C / D / E) |
|---|---|---:|---:|---|
| 0. The price of a hack (the lede figure) | [`c00_lede_cost.md`](sources/c00_lede_cost.md) | 3 | 3 | — |
| 1. Losses to fraud and hacking, and the part caused by AI | [`c01_losses.md`](sources/c01_losses.md) | 214 | 79 | 829 / 163 / 127 / 3 / 0 |
| 2. What happens to criminal enterprises | [`c02_police.md`](sources/c02_police.md) | 103 | 24 | 39 / 90 / 20 / 3 / 0 |
| 3. What crime pays | [`c03_talent.md`](sources/c03_talent.md) | 46 | 40 | 8 / 21 / 20 / 0 / 0 |
| 4. Amdahl's law for a ransomware gang | [`c04_amdahl.md`](sources/c04_amdahl.md) | 44 | 33 | 11 / 16 / 36 / 2 / 0 |
| 5. How long abusers keep access to hosted AI | [`c05_inference.md`](sources/c05_inference.md) | 51 | 20 | 7 / 4 / 69 / 0 / 1 |
| 6. How fast criminals adopt new technology | [`c06_attacker_lag.md`](sources/c06_attacker_lag.md) | 19 | 16 | 4 / 6 / 7 / 1 / 0 |
| 7. Public versus private pay | [`c07_pay.md`](sources/c07_pay.md) | 37 | 18 | 8 / 17 / 25 / 2 / 0 |
| 8. How far governments lag business | [`c08_govlag.md`](sources/c08_govlag.md) | 18 | 13 | 3 / 3 / 2 / 2 / 0 |
| 9. How long state hackers stay hidden | [`c09_state_patience.md`](sources/c09_state_patience.md) | 32 | 26 | 7 / 12 / 3 / 0 / 0 |
| 10. The odds that AI agents become routine | — | — | — | built from the models behind Charts 6 and 8; their sources are on those pages |
| 11. The defenders' build-up | [`c11_defenders.md`](sources/c11_defenders.md) | 38 | 36 | — |
| 12. AI-found flaws, from discovery to patch | [`c12_funnel.md`](sources/c12_funnel.md) | 8 | 7 | 1 / 6 / 5 / 0 / 0 |

Rows are counted by row, not by document, so a document that feeds many rows counts many times. Charts 0, 3, 8, 11 and 12 also rest on documents cited outside the tables; those have no grade of their own.

## Earlier study

The level of losses in Chart 1 and the headcount of cybercriminals cited in the post come from the author's earlier study, *Where are all the agentic cyber attacks? Data, model and figures* (repository `where-are-the-agentic-cyber-attacks`, version 1.0, 17 October 2026). That study has its own evidence library; the numbers taken from it are typed into the scripts and listed in [PARAMETERS](PARAMETERS.md) (look for "the author's earlier triangulation"). Rows in `data/E_stage_judgements.csv` that cite `prior-project RC-nnn` refer to rows of that library.

## Reading a row of `data/sources.csv`

| Column | Meaning |
|---|---|
| `chart` | The figure (0 is the lede figure). |
| `publisher`, `title`, `url`, `pub_date` | As recorded in the table; `pub_date` may be a year or a month. |
| `grade` | The grade(s) of the rows that cite it; blank for documents cited outside the tables. |
| `kind` | `table` (the link is a row's `source_url`), `notes` (the link is written in a notes column) or `extra` (`data/extra_sources.csv`). |
| `tables`, `rows` | Which tables it feeds and which rows (pandas row numbers). |
| `supports` | What was taken from it, in words. |

