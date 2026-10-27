# Chart 3: What crime pays

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c03_talent.png`](../../figures/c03_talent.png) · code: [`charts/c03_talent.py`](../../charts/c03_talent.py)

Criminal pay comes from leaked chats of the Conti ransomware group (reported by KrebsOnSecurity and Trellix), Kaspersky's study of job adverts on dark-web forums, a US indictment and a UK National Crime Agency account of LockBit. Honest pay comes from Levels.fyi (self-reported total compensation), national statistics offices (the US Bureau of Labor Statistics, China's National Bureau of Statistics, Belarus's Belstat) and survey firms (Habr Career for Russia, DOU for Ukraine, ITviec for Vietnam, Kolesa for Kazakhstan, Brasscom for Brazil), at World Bank average exchange rates. The Russian figures and the exchange rate are typed into the chart script; they are listed under *Cited outside the tables* below.

**Tables behind this chart**

- [`data/C_pay.csv`](../../data/C_pay.csv): 31 rows; typed numbers checked against it by `tools/check_inputs.py`.
- [`data/C2_dev_pay_by_country.csv`](../../data/C2_dev_pay_by_country.csv): 16 rows; read by the chart's scripts.
- [`data/F_pay.csv`](../../data/F_pay.csv): 2 rows (of the 52 in the file; the others feed other charts); typed numbers checked against it by `tools/check_inputs.py`.

**46 documents from 40 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**ABC News (Australia)**

- [Cambodia scam industry job advertisements (analysis of 4,991 Telegram job ads)](https://www.abc.net.au/news/2026-09-25/cambodia-scam-industry-job-advertisements/107185964) · 2026-09-25 · grade C — `C_pay` rows 13, 14: South-East Asian scam compound: 'victim finder' (most common ad); South-East Asian scam compound: specialist roles (Western-faced 'model'…

**Analyst1**

- [Anastasia: Inside BlackBasta](https://analyst1.com/wp-content/uploads/2025/04/Anastasia-Inside-BlackBasta.pdf) · 2025-04 · grade C — `C_pay` row 11: Black Basta callers (phone pressure on victims)

**arXiv (Stanford-led)**

- [Comparing AI agents to cybersecurity professionals in real-world penetration testing (ARTEMIS study), as summarised in prior project notes](https://arxiv.org/abs/2512.09882) · 2025-12 · grade C — `C_pay` row 28: Professional penetration tester (cost benchmark)

**Belstat (National Statistical Committee of the Republic of Belarus)**

- [Численность и заработная плата работников Республики Беларусь в 2025 году (статистический бюллетень)](https://www.belstat.gov.by/upload/iblock/2d2/iotagk0izrm0ml29ar75z7rf8seyrgv1.pdf) · 2026 · grade A — `C2_dev_pay_by_country` row 2: Belarus: Employees in 'information and communication' sector (all… (2025)

**BleepingComputer (reporting Gemini Advisory)**

- [Hacking gang creates fake firm to hire pentesters for ransomware attacks](https://www.bleepingcomputer.com/news/security/hacking-gang-creates-fake-firm-to-hire-pentesters-for-ransomware-attacks/) · 2021-10-21 · grade C — `C_pay` row 7: FIN7 front company 'Bastion Secure' recruits (C++/PHP/Python programmers…

**Brasscom (via Teletime; also Canaltech)**

- [Brasscom 'Relatório de Regionalização dos Empregos CLT de TIC' (as reported by Teletime)](https://teletime.com.br/18/08/2026/empregos-tic-norte-nordeste-sudeste/) · 2026-08-18 · grade C — `C2_dev_pay_by_country` row 5: Brazil: Systems development analysts (CBO 2124-05), formal CLT… (2025)

**Business Today (citing Infosys annual report FY26)**

- [Infosys pay check: CEO Salil Parekh took home ₹82.6 crore, 742 times median employee pay](https://www.businesstoday.in/amp/latest/corporate/story/infosys-pay-check-ceo-salil-parekh-took-home-rs82-6-crore-742-times-median-employee-pay-534067-2026-05-30) · 2026-05-30 · grade C — `C2_dev_pay_by_country` row 8: India: Median employee of Infosys Ltd (large IT-services employer) (2025-26)

**DARPA**

- [AIxCC results](https://www.darpa.mil/news/2025/aixcc-results) · 2025-08-08 · grade A — `C_pay` row 29: DARPA AIxCC final: prizes (1st Team Atlanta / 2nd Trail of Bits / 3rd Theori)

**Digital Business (reporting a Kolesa Group survey)**

- [Больше 1 млн тенге. Стала известна средняя зарплата разработчиков в Казахстане](https://digitalbusiness.kz/2025-02-07/bolshe-1-mln-tenge-stala-izvestna-srednyaya-zarplata-razrabotchikov-v-kazahstane/amp/) · 2025-02-07 · grade C — `C2_dev_pay_by_country` row 11: Kazakhstan: Software developers and IT managers, all levels (QA and… (2024)

**DOU (Редакція DOU; analytics by Дар'я Перекосова)**

- [Зарплати українських розробників — літо 2026](https://dou.ua/lenta/articles/salary-report-devs-summer-2026/) · 2026-07-13 · grade B — `C2_dev_pay_by_country` row 0: Ukraine: Software developers working in Ukraine, all levels (DOU… (2026)

**Eurojust**

- [Fraud call centres targeting EU citizens shut down (Eurojust), as summarised in prior project notes](https://www.eurojust.europa.eu/news/fraud-call-centres-targeting-eu-citizens-shut-down-eurojusts-support-over-eur-50-million) · grade C — `C_pay` row 15: Albanian/Balkan fraud call-centre operator

**Finance.ua (Ministry of Economy infographic of Derzhstat data)**

- [Де найшвидше зростають зарплати в Україні: дані Мінекономіки](https://news.finance.ua/ua/de-nayshvydshe-zrostayut-zarplaty-v-ukraini-dani-minekonomiky) · 2025-07-03 · grade C — `C2_dev_pay_by_country` row 1: Ukraine: Full-time payroll employees in 'information and… (2025)

**Habr Career**

- [Habr Career salary calculator](https://career.habr.com/salaries) · 2026-10 · grade B — `C_pay` rows 17–21: Russian IT specialist, all levels (Habr Career headline figure); Russian IT specialist, junior (Habr Career headline figure); Russian IT specialist, middle (Habr Career headline figure); and 2 more

**Institutul Naţional de Statistică (INS); most months via press reports**

- [INS monthly releases on average earnings, 2025 (example: 'Câştigul salarial mediu brut pe economie în luna martie 2025 a fost 9495 lei şi cel net 5691 lei', Nr.117)](https://insse.ro/cms/sites/default/files/com_presa/com_pdf/cs03r25.pdf) · 2025-03 to 2026-02 (monthly releases) · grade C — `C2_dev_pay_by_country` row 13: Romania: Employees in IT services (CAEN Rev.2 'activităţi de… (2025)

**ITviec**

- [Vietnam IT Salary & Recruitment Market Report 2025-2026](https://itviec.com/report/vietnam-it-salary-and-recruitment-market) · n.d. (survey closed 2025-11-11) · grade B — `C2_dev_pay_by_country` row 9: Vietnam: Back-end developers, all experience levels (2025)

**Kaspersky**

- [Developers, attackers and designers topped the list of the most demanded IT professionals on the darknet](https://www.kaspersky.com/about/press-releases/developers-attackers-and-designers-topped-the-list-of-the-most-demanded-it-professionals-on-the-darknet) · 2023-01-30 · grade B — `C_pay` rows 2–6: Dark-web IT job ads: developer (median); Dark-web IT job ads: attacker / pentester (median); Dark-web IT job ads: reverse engineer (median); and 2 more

**Kazinform (citing Bureau of National Statistics)**

- [Какие специалисты заработали больше всего в Казахстане в 2025 году](https://www.inform.kz/ru/kakie-spetsialisti-zarabotali-bolshe-vsego-vkazahstane-v2025-godu-4ab5cd90) · 2026-07-21 · grade C — `C2_dev_pay_by_country` row 12: Kazakhstan: Employees in 'information and communication' sector (all… (2025)

**KrebsOnSecurity**

- [Conti Ransomware Group Diaries, Part II: The Office](https://krebsonsecurity.com/2022/03/conti-ransomware-group-diaries-part-ii-the-office/) · 2022-03-02 · grade B — `C_pay` row 0: Conti staff (mostly low-level malware coders and testers), typical salary

**Levels.fyi**

- [End of Year Pay Report 2025](https://www.levels.fyi/2025/) · 2025-12 · grade B — `C_pay` row 22: US software engineer, all levels (median total compensation)
- [Anthropic Software Engineer Salary](https://www.levels.fyi/companies/anthropic/salaries/software-engineer) · 2026-09-24 · grade B/C — `C_pay` row 26: Anthropic software engineer (median total compensation; entry to staff); `F_pay` row 15: United States: Anthropic software engineer, all levels, total compensation (2026)
- [ML / AI Software Engineer Salary](https://www.levels.fyi/t/software-engineer/focus/ml-ai) · 2026-10 · grade B — `C_pay` row 23: US ML/AI software engineer (median total compensation)
- [Meta Machine Learning Engineer Salary](https://www.levels.fyi/companies/meta/salaries/software-engineer/title/machine-learning-engineer) · 2026-10-16 · grade B — `C_pay` row 24: Meta ML engineer (median total compensation; E3 to E6 range)
- [OpenAI Software Engineer Salary](https://www.levels.fyi/companies/openai/salaries/software-engineer) · 2026-10-20 · grade B/C — `C_pay` row 25: OpenAI software engineer (median total compensation; L2 to L5 range); `F_pay` row 14: United States: OpenAI software engineer, all levels, total compensation (2026)

**MSMT (11 governments) via Japan MOFA**

- [Multilateral Sanctions Monitoring Team, third report](https://www.mofa.go.jp/files/101088307.pdf) · 2026-09-16 · grade B — `C_pay` row 16: North Korean IT worker abroad (gross earnings)

**National Bureau of Statistics of China**

- [2025年城镇单位就业人员年平均工资情况](https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202605/t20260515_1963707.html) · 2026-05-15 · grade A — `C2_dev_pay_by_country` rows 3, 4: China: Employees in 'information transmission, software and IT… (2025)

**PayScale**

- [Average Software Engineer Salary in India in 2026](https://www.payscale.com/research/IN/Job=Software_Engineer/Salary) · 2026-07-12 · grade B — `C2_dev_pay_by_country` row 7: India: Software engineers, all experience levels (2026)

**Profit.ro (citing INS)**

- [România avea anul trecut 5,76 milioane salariați (reporting the INS annual earnings release for 2025)](https://profit.ro/taxe-si-consultanta/romania-avea-anul-trecut-5-76-milioane-salariati-botosani-si-teleorman-cele-mai-mici-salarii-la-polul-opus-bucuresti-22784743) · 2026-09-25 · grade C — `C2_dev_pay_by_country` row 14: Romania: Employees in section K: telecoms, computer programming and… (2025)

**Salario.com.br (Portal Salário, from Novo CAGED / Ministério do Trabalho e Emprego)**

- [Analista de Desenvolvimento de Sistemas - Salário 2026 (CBO 212405)](https://www.salario.com.br/profissao/analista-de-desenvolvimento-de-sistemas-cbo-212405/) · 2026-10-08 · grade B — `C2_dev_pay_by_country` row 6: Brazil: Systems development analysts (CBO 2124-05), CLT hires and… (2025-26)

**The Register**

- [Scattered Lapsus$ Hunters female recruits (as summarised in prior project notes)](https://www.theregister.com/2026/02/26/scattered_lapsus_hunters_female_recruits/) · 2026-02-26 · grade C — `C_pay` row 12: Scattered Lapsus$ Hunters callers recruited on Telegram

**Tiền Phong (citing TopCV)**

- [Ngành nghề nào có thu nhập bình quân cao nhất hiện nay? (reporting TopCV annual recruitment market report 2024-2025)](https://tienphong.vn/nganh-nghe-nao-co-thu-nhap-binh-quan-cao-nhat-hien-nay-post1725755.tpo) · 2025-03-17 · grade C — `C2_dev_pay_by_country` row 10: Vietnam: IT (software) specialists ('chuyên viên IT', a mid-level… (2024)

**Trellix**

- [Conti Leaks: Examining the Panama Papers of Ransomware](https://www.trellix.com/blogs/research/conti-leaks-examining-the-panama-papers-of-ransomware/) · 2022-03 · grade C — `C_pay` row 1: Conti/Trickbot callers (phone pressure on victims), base pay

**UK National Crime Agency**

- [LockBit leader unmasked and sanctioned](https://www.nationalcrimeagency.gov.uk/news/lockbit-leader-unmasked-and-sanctioned) · 2024-05-07 · grade A — `C_pay` row 10: LockBit affiliates: share who never received a ransom

**US Bureau of Labor Statistics (OEWS)**

- [Occupational Employment and Wages News Release - 2025 A01 Results (Occupational Employment and Wages, May 2025)](https://www.bls.gov/news.release/archives/ocwage_05152026.htm) · 2026-05-15 · grade A — `C2_dev_pay_by_country` row 15: United States: Software developers (SOC 15-1252) (2025 (May 2025 reference))

**US Department of Justice**

- [U.S. Charges Russian National with Developing and Operating LockBit Ransomware](https://www.justice.gov/opa/pr/us-charges-russian-national-developing-and-operating-lockbit-ransomware) · 2024-05-07 · grade A — `C_pay` row 9: LockBit administrator (Dmitry Khoroshev, alleged), 20% share of ransoms
- [United States Charges Dual Russian and Israeli National as Developer of LockBit Ransomware Group](https://www.justice.gov/opa/pr/united-states-charges-dual-russian-and-israeli-national-developer-lockbit-ransomware-group) · 2024-12-20 · grade A — `C_pay` row 8: LockBit developer (Rostislav Panev, alleged), payments from LockBit…

**Wikipedia (secondary; NYT/WSJ primary not opened)**

- [Meta Superintelligence Labs (Wikipedia, citing NYT 2025-06-10 and WSJ 2025-06-22)](https://en.wikipedia.org/wiki/Meta_Superintelligence_Labs) · 2025-06 · grade C — `C_pay` row 27: Frontier-lab recruitment offers (Meta Superintelligence Labs, 2025)

**XBOW**

- [XBOW Rewarded for Exploit Affecting a Billion Users (XBOW news index)](https://xbow.com/news/xbow-rewarded-for-exploit-affecting-a-billion-users) · 2026-10-13 · grade C — `C_pay` row 30: Legitimate exploit market: Google Chrome full-chain vulnerability reward…

## Cited outside the tables

Numbers typed into a script, milestones that a table's notes name without a link, and links written inside notes columns come from these pages. [`data/extra_sources.csv`](../../data/extra_sources.csv) says what each typed one supports and where it is used.

**canaltech.com.br**

- [https://canaltech.com.br/mercado/analista-de-desenvolvimento-de-sistemas-e-o-profissional-de-ti-mais-contratado-em-clt-no-brasil/](https://canaltech.com.br/mercado/analista-de-desenvolvimento-de-sistemas-e-o-profissional-de-ti-mais-contratado-em-clt-no-brasil/) — `C2_dev_pay_by_country` row 5: link written in the notes column

**forbes.ua**

- [https://forbes.ua/news/mediana-zarplat-it-rozrobnikiv-zrosla-do-3450-khto-z-ukrainskikh-aytivtsiv-zaroblyae-naybilshe-doslidzhennya-dou-12012026-35431](https://forbes.ua/news/mediana-zarplat-it-rozrobnikiv-zrosla-do-3450-khto-z-ukrainskikh-aytivtsiv-zaroblyae-naybilshe-doslidzhennya-dou-12012026-35431) — `C2_dev_pay_by_country` row 0: link written in the notes column

**Habr Career**

- [Зарплаты разработчиков в первой половине 2021: квалификации и основные языки](https://habr.com/ru/companies/habr_career/articles/584514/) — Russian developers' median take-home pay by level in the first half of 2021, in roubles a month: junior 52,000, middle 120,000, senior 195,000, lead 230,000. The like-for-like comparison for the dark-web job ads, which were posted mostly on Russian-language forums. *Used in:* charts/c03_talent.py (typed in the script; docstring).

**in.indeed.com**

- [https://in.indeed.com/career/software-engineer/salaries](https://in.indeed.com/career/software-engineer/salaries) — `C2_dev_pay_by_country` row 7: link written in the notes column

**interfax.com.ua**

- [https://interfax.com.ua/news/economic/1100501.html](https://interfax.com.ua/news/economic/1100501.html) — `C2_dev_pay_by_country` row 1: link written in the notes column

**Kaspersky (Securelist)**

- [Securelist report on dark-web IT job ads](https://securelist.com/darknet-it-headhunting/108526/) — Kaspersky's own report on its study of IT job ads on 155 dark-web forums (January 2020 to June 2022). The study's press release is the source of the role-by-role pay medians in C_pay.csv rows 2-6. *Used in:* Listed with Chart 3's sources; the figures themselves are read from C_pay.csv.

**theregister.com**

- [https://www.theregister.com/2023/01/30/dark_web_it_employment_kaspersky/](https://www.theregister.com/2023/01/30/dark_web_it_employment_kaspersky/) — `C_pay` row 3: link written in the notes column

**wagedex.com**

- [https://wagedex.com/jobs/software-developers](https://wagedex.com/jobs/software-developers) — `C2_dev_pay_by_country` row 15: link written in the notes column

**World Bank**

- [Official exchange rates, annual averages (PA.NUS.FCRF)](https://data.worldbank.org/indicator/PA.NUS.FCRF) — The 2021 average of 73.65 roubles per US dollar, used to convert the Habr Career salaries. *Used in:* charts/c03_talent.py (typed in the script; docstring).
