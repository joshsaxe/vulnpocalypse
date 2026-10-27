# Chart 2: What happens to criminal enterprises

[← Bibliography](../BIBLIOGRAPHY.md) · figure: [`figures/c02_police.png`](../../figures/c02_police.png) · code: [`charts/c02_police.py`](../../charts/c02_police.py)

A hand-built list of 152 named criminal enterprises in ten sectors (ransomware brands, darknet markets, botnets and malware services, forums and others), each with how and when it ended, taken from takedown announcements, court records, sanctions notices and trackers. Most rows rest on one press report or tracker entry (grade B). The list is not a random sample: enterprises famous enough to be documented are more often ones police acted against, which probably flatters the police.

**Tables behind this chart**

- [`data/B_enterprise_lifespans.csv`](../../data/B_enterprise_lifespans.csv): 152 rows; read by the chart's scripts.

**103 documents from 24 publishers.** Each entry gives the link, the date and grade recorded in the table, then which rows of which table came from it and what they hold. Row numbers count from 0 (a spreadsheet shows row *N* as *N* + 2). Grades are explained in the [bibliography index](../BIBLIOGRAPHY.md#grades).

## Documents in the tables

**BleepingComputer**

- [Avaddon ransomware shuts down and releases decryption keys](https://www.bleepingcomputer.com/news/security/avaddon-ransomware-shuts-down-and-releases-decryption-keys/) · 2021-06-11 · grade B — `B_enterprise_lifespans` row 9: Avaddon

**Chainalysis**

- [Global Law Enforcement Dismantles 'AudiA6' Crypto Laundering Network](https://www.chainalysis.com/blog/law-enforcement-dismantles-audia6-laundering-network-june-2026/) · 2026-06-11 · grade B — `B_enterprise_lifespans` rows 82, 132: Dark2Web; AudiA6
- [OFAC and DOJ Strike Xinbi, a Multibillion-Dollar Marketplace for Cybercriminals](https://www.chainalysis.com/blog/ofac-sanctions-xinbi-cybercriminal-crypto-marketplace/) · 2026-09-09 · grade B — `B_enterprise_lifespans` row 135: Xinbi Guarantee

**CISA/FBI**

- [#StopRansomware: BlackSuit (Royal) Ransomware (AA23-061A)](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-061a) · 2024-08-07 · grade A — `B_enterprise_lifespans` row 16: Royal

**Collier, Thomas, Clayton, Hutchings (ACM IMC)**

- [Booting the Booters (IMC 2019)](https://www.cl.cam.ac.uk/~ah793/papers/2019booting.pdf) · 2019-10 · grade C — `B_enterprise_lifespans` row 112: vDOS

**Dutch National Police / FBI**

- [Operation Magnus](https://www.operation-magnus.com/) · 2024-10-28 · grade A — `B_enterprise_lifespans` rows 101, 102: RedLine Stealer; META Stealer

**Elliptic**

- [Tudou Guarantee winds down operations after $12 billion in transactions](https://www.elliptic.co/insights/tudou-guarantee-winds-down-operations-after-12-billion-in-transactions/) · 2026-01-19 · grade B — `B_enterprise_lifespans` row 134: Tudou Guarantee

**Eurojust**

- [World's most dangerous malware EMOTET disrupted through global action](https://www.eurojust.europa.eu/news/worlds-most-dangerous-malware-emotet-disrupted-through-global-action) · 2021-01-27 · grade A — `B_enterprise_lifespans` row 92: Emotet

**Europol**

- [World's biggest marketplace selling internet paralysing DDoS attacks taken down](https://www.europol.europa.eu/media-press/newsroom/news/world%E2%80%99s-biggest-marketplace-selling-internet-paralysing-ddos-attacks-taken-down) · 2018-04-25 · grade A — `B_enterprise_lifespans` row 111: Webstresser
- [288 dark web vendors arrested in major marketplace seizure (Operation SpecTor)](https://www.europol.europa.eu/media-press/newsroom/news/288-dark-web-vendors-arrested-in-major-marketplace-seizure) · 2023-05-02 · grade C — `B_enterprise_lifespans` row 62: Monopoly Market
- [Ragnar Locker ransomware gang taken down by international police swoop](https://www.europol.europa.eu/media-press/newsroom/news/ragnar-locker-ransomware-gang-taken-down-international-police-swoop) · 2023-10-20 · grade A — `B_enterprise_lifespans` row 14: Ragnar Locker

**Fraunhofer FKIE Malpedia (MISP galaxy mirror)**

- [Malpedia entry gandcrab (via MISP galaxy malpedia.json)](https://malpedia.caad.fkie.fraunhofer.de/details/win.gandcrab) · 2026 · grade B — `B_enterprise_lifespans` row 0: GandCrab

**Gwern Branwen**

- [Darknet Market mortality risks (survival table)](https://gwern.net/dnm-survival) · 2019-06-09 · grade B — `B_enterprise_lifespans` rows 38–55: Silk Road; Silk Road 2.0; Hydra (2014 English-language market); Cloud-Nine; and 14 more

**KrebsOnSecurity**

- [Joker's Stash Carding Market to Call it Quits](https://krebsonsecurity.com/2021/01/jokers-stash-carding-market-to-call-it-quits/) · 2021-01 · grade B — `B_enterprise_lifespans` row 116: Joker's Stash
- [Russian Govt. Continues Carding Shop Crackdown](https://krebsonsecurity.com/2022/02/russian-govt-continues-carding-shop-crackdown/) · 2022-02-09 · grade B — `B_enterprise_lifespans` rows 117–120: Trump's Dumps; Ferum Shop; Sky-Fraud; UAS (UAS Store)

**Microsoft**

- [Catching the big fish: Analyzing a large-scale phishing-as-a-service operation](https://www.microsoft.com/en-us/security/blog/2021/09/21/catching-the-big-fish-analyzing-a-large-scale-phishing-as-a-service-operation/) · 2021-09-21 · grade C — `B_enterprise_lifespans` row 138: BulletProftLink
- [Disrupting Lumma Stealer: Microsoft leads global action against favored cybercrime tool](https://blogs.microsoft.com/on-the-issues/2025/05/21/microsoft-leads-global-action-against-favored-cybercrime-tool/) · 2025-05-21 · grade B — `B_enterprise_lifespans` row 103: Lumma Stealer
- [Microsoft seizes 338 websites to disrupt rapidly growing 'RaccoonO365' phishing service](https://blogs.microsoft.com/on-the-issues/2025/09/16/microsoft-seizes-338-websites-to-disrupt-rapidly-growing-raccoono365-phishing-service/) · 2025-09-16 · grade B — `B_enterprise_lifespans` row 139: RaccoonO365
- [How a global coalition disrupted Tycoon](https://blogs.microsoft.com/on-the-issues/2026/03/04/how-a-global-coalition-disrupted-tycoon/) · 2026-03-04 · grade B — `B_enterprise_lifespans` row 110: Tycoon 2FA
- [Disrupting EvilTokens: the AI chatbot built for cybercrime](https://blogs.microsoft.com/on-the-issues/2026/09/22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/) · 2026-09-22 · grade B — `B_enterprise_lifespans` row 140: EvilTokens

**MITRE**

- [MITRE ATT&CK software/group entry S0266](https://attack.mitre.org/software/S0266) · 2026 · grade B — `B_enterprise_lifespans` row 93: TrickBot
- [MITRE ATT&CK software/group entry S0446](https://attack.mitre.org/software/S0446) · 2026 · grade B — `B_enterprise_lifespans` row 1: Ryuk
- [MITRE ATT&CK software/group entry S0554](https://attack.mitre.org/software/S0554) · 2026 · grade B — `B_enterprise_lifespans` row 3: Egregor

**Operation Endgame partners (Europol/BKA/Dutch police site)**

- [Operation Endgame news page](https://www.operation-endgame.com/news) · 2026-06-24 · grade A — `B_enterprise_lifespans` rows 95–99, 104, 107–109, 150: IcedID; SmokeLoader; Pikabot; Bumblebee; and 6 more

**PBS NewsHour / Associated Press**

- [Myanmar has declared a zero-tolerance policy for cyberscams but the fraud goes on (AP)](https://www.pbs.org/newshour/world/myanmar-has-declared-a-zero-tolerance-policy-for-cyberscams-but-the-fraud-goes-on) · 2025-12-17 · grade B — `B_enterprise_lifespans` row 137: KK Park (Myawaddy scam compound)

**ransomware.live (community leak-site tracker)**

- [ransomware.live group page: akira](https://www.ransomware.live/group/akira) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 24: Akira
- [ransomware.live group page: bianlian](https://www.ransomware.live/group/bianlian) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 30: BianLian
- [ransomware.live group page: blackbasta](https://www.ransomware.live/group/blackbasta) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 19: Black Basta
- [ransomware.live group page: blacksuit](https://www.ransomware.live/group/blacksuit) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 17: BlackSuit
- [ransomware.live group page: cactus](https://www.ransomware.live/group/cactus) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 31: Cactus
- [ransomware.live group page: chaos](https://www.ransomware.live/group/chaos) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 18: Chaos
- [ransomware.live group page: clop](https://www.ransomware.live/group/clop) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 23: Cl0p
- [ransomware.live group page: cuba](https://www.ransomware.live/group/cuba) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 15: Cuba
- [ransomware.live group page: dispossessor](https://www.ransomware.live/group/dispossessor) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 21: Dispossessor (Radar)
- [ransomware.live group page: dragonforce](https://www.ransomware.live/group/dragonforce) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 28: DragonForce
- [ransomware.live group page: everest](https://www.ransomware.live/group/everest) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 34: Everest
- [ransomware.live group page: hunters](https://www.ransomware.live/group/hunters) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 32: Hunters International
- [ransomware.live group page: incransom](https://www.ransomware.live/group/incransom) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 33: INC Ransom
- [ransomware.live group page: lynx](https://www.ransomware.live/group/lynx) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 35: Lynx
- [ransomware.live group page: maze](https://www.ransomware.live/group/maze) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 2: Maze
- [ransomware.live group page: medusa](https://www.ransomware.live/group/medusa) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 27: Medusa
- [ransomware.live group page: play](https://www.ransomware.live/group/play) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 25: Play
- [ransomware.live group page: qilin](https://www.ransomware.live/group/qilin) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 26: Qilin (Agenda)
- [ransomware.live group page: ransomhub](https://www.ransomware.live/group/ransomhub) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 22: RansomHub
- [ransomware.live group page: rhysida](https://www.ransomware.live/group/rhysida) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 29: Rhysida
- [ransomware.live group page: safepay](https://www.ransomware.live/group/safepay) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 36: SafePay
- [ransomware.live group page: thegentlemen](https://www.ransomware.live/group/thegentlemen) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 37: The Gentlemen

**Recorded Future (Insikt Group)**

- [Dark Covenant 3.0: Controlled Impunity and Russia's Cybercriminals](https://www.recordedfuture.com/research/dark-covenant-3-controlled-impunity-and-russias-cybercriminals) · 2025-10-23 · grade B — `B_enterprise_lifespans` row 131: Cryptex (and UAPS/PM2BTC)

**Sophos X-Ops**

- [Ransomware and data-extortion ecosystem research notes (prior project, Sophos X-Ops forum study cited)](https://www.sophos.com/en-us/blog/cybercriminals-cant-agree-on-gpts) · 2023-11 · grade C — `B_enterprise_lifespans` row 83: Exploit.in

**The Record (Recorded Future News)**

- [BlackMatter ransomware says it's shutting down due to pressure from local authorities](https://therecord.media/blackmatter-ransomware-says-its-shutting-down-due-to-pressure-from-local-authorities) · 2021-11-03 · grade B — `B_enterprise_lifespans` row 7: BlackMatter
- [Operation Endgame strikes again (Rhadamanthys, VenomRAT, Elysium)](https://therecord.media/operation-endgame-cybercrime-takedowns-rhadamanthys-venomrat-elysium) · 2025-11-13 · grade B — `B_enterprise_lifespans` rows 105, 106: Rhadamanthys; VenomRAT

**UK National Crime Agency**

- [LockBit leader unmasked and sanctioned](https://www.nationalcrimeagency.gov.uk/news/lockbit-leader-unmasked-and-sanctioned) · 2024-05-07 · grade A — `B_enterprise_lifespans` row 13: LockBit

**US Department of Justice**

- [AlphaBay, the Largest Online 'Dark Market,' Shut Down](https://www.justice.gov/opa/pr/alphabay-largest-online-dark-market-shut-down) · 2017-07-20 · grade A — `B_enterprise_lifespans` row 56: AlphaBay
- [Thirty-Six Defendants Indicted for Alleged Roles in Transnational Criminal Organization (Infraud)](https://www.justice.gov/opa/pr/thirty-six-defendants-indicted-alleged-roles-transnational-criminal-organization-responsible) · 2018-02-07 · grade A — `B_enterprise_lifespans` row 73: Infraud Organization
- [Ohio Resident Charged with Operating Darknet-Based Bitcoin 'Mixer'](https://www.justice.gov/opa/pr/ohio-resident-charged-operating-darknet-based-bitcoin-mixer-which-laundered-over-300-million) · 2020-02-13 · grade A — `B_enterprise_lifespans` row 124: Helix
- [Department of Justice Launches Global Action Against NetWalker Ransomware](https://www.justice.gov/opa/pr/department-justice-launches-global-action-against-netwalker-ransomware) · 2021-01-27 · grade A — `B_enterprise_lifespans` row 5: NetWalker
- [Individual Arrested and Charged with Operating Notorious Darknet Cryptocurrency 'Mixer'](https://www.justice.gov/opa/pr/individual-arrested-and-charged-operating-notorious-darknet-cryptocurrency-mixer) · 2021-04-28 · grade A — `B_enterprise_lifespans` row 123: Bitcoin Fog
- [Justice Department Investigation Leads to Shutdown of Largest Online Darknet Marketplace](https://www.justice.gov/opa/pr/justice-department-investigation-leads-shutdown-largest-online-darknet-marketplace) · 2022-04-05 · grade A — `B_enterprise_lifespans` row 64: Hydra Market
- [U.S. Department of Justice Disrupts Hive Ransomware Variant](https://www.justice.gov/archives/opa/pr/us-department-justice-disrupts-hive-ransomware-variant) · 2023-01-26 · grade A — `B_enterprise_lifespans` row 11: Hive
- [Criminal Marketplace Disrupted by International Cyber Operation (Genesis)](https://www.justice.gov/opa/pr/criminal-marketplace-disrupted-international-cyber-operation) · 2023-04-05 · grade A — `B_enterprise_lifespans` row 66: Genesis Market
- [Russian National Charged for Ransomware Attacks Against Critical Infrastructure (Matveev)](https://www.justice.gov/opa/pr/russian-national-charged-ransomware-attacks-against-critical-infrastructure) · 2023-05-16 · grade A — `B_enterprise_lifespans` row 10: Babuk
- [Qakbot Malware Disrupted in International Cyber Takedown](https://www.justice.gov/opa/pr/qakbot-malware-disrupted-international-cyber-takedown) · 2023-08-29 · grade A — `B_enterprise_lifespans` row 94: Qakbot
- [Justice Department Disrupts Prolific ALPHV/Blackcat Ransomware Variant](https://www.justice.gov/opa/pr/justice-department-disrupts-prolific-alphvblackcat-ransomware-variant) · 2023-12-19 · grade A — `B_enterprise_lifespans` row 12: ALPHV/BlackCat
- [911 S5 Botnet Dismantled and Its Administrator Arrested in Coordinated International Operation](https://www.justice.gov/opa/pr/911-s5-botnet-dismantled-and-its-administrator-arrested-coordinated-international-operation) · 2024-05-29 · grade A — `B_enterprise_lifespans` row 100: 911 S5
- [Cracked and Nulled Marketplaces Disrupted in International Cyber Operation](https://www.justice.gov/opa/pr/cracked-and-nulled-marketplaces-disrupted-international-cyber-operation) · 2025-01-30 · grade A — `B_enterprise_lifespans` rows 80, 81: Cracked; Nulled
- [Phobos Ransomware Affiliates Arrested in Coordinated International Disruption](https://www.justice.gov/opa/pr/phobos-ransomware-affiliates-arrested-coordinated-international-disruption) · 2025-02-10 · grade A — `B_enterprise_lifespans` row 20: Phobos/8Base
- [Garantex Cryptocurrency Exchange Disrupted in International Operation](https://www.justice.gov/opa/pr/garantex-cryptocurrency-exchange-disrupted-international-operation) · 2025-03-07 · grade A — `B_enterprise_lifespans` row 130: Garantex
- [Chairman of Prince Group Indicted for Operating Cambodian Forced Labor Scam Compounds](https://www.justice.gov/opa/pr/chairman-prince-group-indicted-operating-cambodian-forced-labor-scam-compounds-engaged) · 2025-10-14 · grade A — `B_enterprise_lifespans` row 136: Prince Group (scam-compound conglomerate)

**US Department of Justice (via prior project evidence file)**

- [Two Sudanese Nationals Indicted for Alleged Role in Anonymous Sudan Cyberattacks](https://www.justice.gov/usao-cdca/pr/two-sudanese-nationals-indicted-alleged-role-anonymous-sudan-cyberattacks) · 2024-10-16 · grade B — `B_enterprise_lifespans` row 114: Anonymous Sudan (DCAT/Godzilla/Skynet DDoS service)

**US Treasury**

- [Treasury Sanctions Mixer Used by the DPRK to Launder Stolen Virtual Currency (Sinbad)](https://home.treasury.gov/news/press-releases/jy1933) · 2023-11-29 · grade A — `B_enterprise_lifespans` rows 126, 127: Blender.io; Sinbad
- [Treasury sanctions Zservers (press release sb0018)](https://home.treasury.gov/news/press-releases/sb0018) · 2025-02-11 · grade A — `B_enterprise_lifespans` row 147: Zservers
- [Treasury sanctions Aeza Group (press release sb0185)](https://home.treasury.gov/news/press-releases/sb0185) · 2025-07-01 · grade A — `B_enterprise_lifespans` row 148: Aeza Group
- [Treasury sanctions Media Land (press release sb0319)](https://home.treasury.gov/news/press-releases/sb0319) · 2025-11-19 · grade A — `B_enterprise_lifespans` row 149: Media Land (Yalishanda)

**Wikipedia**

- [AlphaBay](https://en.wikipedia.org/wiki/AlphaBay) · 2026-10-21 · grade C — `B_enterprise_lifespans` row 65: AlphaBay (relaunch)
- [Archetyp Market](https://en.wikipedia.org/wiki/Archetyp_Market) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 68: Archetyp Market
- [Avalanche (phishing group)](https://en.wikipedia.org/wiki/Avalanche_%28phishing_group%29) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 85: Avalanche
- [Botnet (historical list table)](https://en.wikipedia.org/wiki/Botnet) · 2026-10-21 · grade C — `B_enterprise_lifespans` rows 86–91, 115: Rustock; Waledac; Mariposa; BredoLab; and 3 more
- [BreachForums](https://en.wikipedia.org/wiki/BreachForums) · 2026-10-21 · grade B/C — `B_enterprise_lifespans` rows 75–78: BreachForums v1; BreachForums v2; BreachForums v3; BreachForums v4
- [BTC-e](https://en.wikipedia.org/wiki/BTC-e) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 122: BTC-e
- [Bulletproof hosting](https://en.wikipedia.org/wiki/Bulletproof_hosting) · 2026-10-21 · grade C — `B_enterprise_lifespans` rows 143, 144, 146, 151: Russian Business Network; McColo; LolekHosted; CrazyRDP
- [Carder.su](https://en.wikipedia.org/wiki/Carder.su) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 71: Carder.su
- [CarderPlanet](https://en.wikipedia.org/wiki/CarderPlanet) · 2026-10-21 · grade C — `B_enterprise_lifespans` row 70: CarderPlanet
- [ChipMixer](https://en.wikipedia.org/wiki/ChipMixer) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 125: ChipMixer
- [Conti (ransomware)](https://en.wikipedia.org/wiki/Conti_%28ransomware%29) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 8: Conti
- [CyberBunker](https://en.wikipedia.org/wiki/CyberBunker) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 145: CyberBunker
- [DarkMarket](https://en.wikipedia.org/wiki/DarkMarket) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 60: DarkMarket
- [Darknet market (Wall Street Market section)](https://en.wikipedia.org/wiki/Darknet_market) · 2026-10-21 · grade C — `B_enterprise_lifespans` row 59: Wall Street Market
- [Darkode](https://en.wikipedia.org/wiki/Darkode) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 72: Darkode
- [DarkSide (hacker group)](https://en.wikipedia.org/wiki/DarkSide_%28hacker_group%29) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 6: DarkSide
- [Dream Market](https://en.wikipedia.org/wiki/Dream_Market) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 58: Dream Market
- [Empire Market](https://en.wikipedia.org/wiki/Empire_Market) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 63: Empire Market
- [Gameover ZeuS](https://en.wikipedia.org/wiki/Gameover_ZeuS) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 84: Gameover ZeuS
- [Hansa (market)](https://en.wikipedia.org/wiki/Hansa_%28market%29) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 57: Hansa
- [Huione Group](https://en.wikipedia.org/wiki/Huione_Group) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 133: Huione Guarantee (Haowang)
- [Incognito Market](https://en.wikipedia.org/wiki/Incognito_Market) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 67: Incognito Market
- [Operation PowerOFF](https://en.wikipedia.org/wiki/Operation_PowerOFF) · 2026-10-21 · grade C — `B_enterprise_lifespans` row 113: Quantum Booter
- [RaidForums](https://en.wikipedia.org/wiki/RaidForums) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 74: RaidForums
- [REvil](https://en.wikipedia.org/wiki/REvil) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 4: REvil/Sodinokibi
- [Samourai Wallet](https://en.wikipedia.org/wiki/Samourai_Wallet) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 129: Samourai Wallet
- [Shadowcrew](https://en.wikipedia.org/wiki/Shadowcrew) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 69: ShadowCrew
- [Tornado Cash](https://en.wikipedia.org/wiki/Tornado_Cash) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 128: Tornado Cash
- [White House Market](https://en.wikipedia.org/wiki/White_House_Market) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 61: White House Market
- [XSS.is](https://en.wikipedia.org/wiki/XSS.is) · 2026-10-21 · grade B — `B_enterprise_lifespans` row 79: XSS (ex-DaMaGeLaB)

## Rows recorded without a link

The table has no source link for these rows; the notes column says why.

- `B_enterprise_lifespans` row 121: BidenCash (grade D). UNVERIFIED THIS SESSION: recalled launch ~Mar 2022 and US/Dutch seizure of ~145 domains ~June 2025. Dates left blank because no page could be opened (DOJ and BleepingComputer fetches failed). Verify before use.
- `B_enterprise_lifespans` row 141: LabHost (grade D). UNVERIFIED THIS SESSION: recalled Met Police/Europol takedown in April 2024 with dozens of arrests; launch ~2021. Dates left blank because Met, Europol, NCA, Interpol and press pages all failed to load. Verify before use.
- `B_enterprise_lifespans` row 142: 16shop (grade D). UNVERIFIED THIS SESSION: recalled Interpol-coordinated arrests in Indonesia and Japan in 2023; Interpol pages returned server errors. Dates left blank. Verify before use.
