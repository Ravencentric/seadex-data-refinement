# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `148.1 TiB`
- Best size: `112.9 TiB`
- Alt size: `35.2 TiB`
- Realistic size: `115.9 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 15.3 TiB   | 14.5 TiB (94.75%)   | 186 (~84.2 GiB each)  |
| 2    | CRUCiBLE         | 9.5 TiB    | 9.5 TiB (100.00%)   | 130 (~74.8 GiB each)  |
| 3    | NAN0             | 8.6 TiB    | 8.5 TiB (98.68%)    | 116 (~75.8 GiB each)  |
| 4    | hchcsen          | 8.5 TiB    | 7.2 TiB (85.09%)    | 111 (~78.4 GiB each)  |
| 5    | Headpatter       | 5.2 TiB    | 3.9 TiB (75.30%)    | 175 (~30.5 GiB each)  |
| 6    | sam              | 3.9 TiB    | 3.7 TiB (93.33%)    | 134 (~30.2 GiB each)  |
| 7    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 99 (~39.5 GiB each)   |
| 8    | PMR              | 3.1 TiB    | 3.1 TiB (100.00%)   | 40 (~80.5 GiB each)   |
| 9    | B00BA            | 2.9 TiB    | 2.9 TiB (100.00%)   | 33 (~89.3 GiB each)   |
| 10   | TTGA             | 2.8 TiB    | 2.7 TiB (95.47%)    | 39 (~73.9 GiB each)   |
| 11   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~619.5 GiB each)   |
| 12   | NOGRP            | 1.8 TiB    | 1.1 TiB (64.35%)    | 47 (~38.4 GiB each)   |
| 13   | GetItTwisted     | 1.8 TiB    | 1.3 TiB (74.93%)    | 63 (~28.5 GiB each)   |
| 14   | MTBB             | 1.6 TiB    | 1.4 TiB (84.55%)    | 106 (~15.6 GiB each)  |
| 15   | LaCroiX          | 1.5 TiB    | 1.5 TiB (100.00%)   | 20 (~75.0 GiB each)   |
| 16   | LazyRemux        | 1.4 TiB    | 1.4 TiB (100.00%)   | 20 (~72.3 GiB each)   |
| 17   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 18   | A&C              | 1.3 TiB    | 1.2 TiB (97.97%)    | 5 (~260.6 GiB each)   |
| 19   | SubsPlease       | 1.3 TiB    | 192.6 GiB (14.83%)  | 75 (~17.3 GiB each)   |
| 20   | nekotan          | 1.1 TiB    | 940.2 GiB (80.07%)  | 32 (~36.7 GiB each)   |
| 21   | YURASUKA         | 1.1 TiB    | 445.7 GiB (38.55%)  | 98 (~11.8 GiB each)   |
| 22   | Sylvar           | 1.1 TiB    | 1.0 TiB (93.65%)    | 13 (~86.3 GiB each)   |
| 23   | FLE              | 1.0 TiB    | 1022.7 GiB (96.41%) | 27 (~39.3 GiB each)   |
| 24   | smol             | 1022.8 GiB | 973.4 GiB (95.17%)  | 57 (~17.9 GiB each)   |
| 25   | FraMeSToR        | 959.9 GiB  | 822.9 GiB (85.73%)  | 13 (~73.8 GiB each)   |
| 26   | Mehul            | 926.2 GiB  | 866.9 GiB (93.60%)  | 27 (~34.3 GiB each)   |
| 27   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 28   | KH               | 914.0 GiB  | 139.7 GiB (15.28%)  | 57 (~16.0 GiB each)   |
| 29   | Holomux          | 882.5 GiB  | 193.5 GiB (21.92%)  | 35 (~25.2 GiB each)   |
| 30   | Okay-Subs        | 862.6 GiB  | 845.6 GiB (98.02%)  | 40 (~21.6 GiB each)   |
| 31   | LYS1TH3A         | 855.0 GiB  | 829.7 GiB (97.04%)  | 35 (~24.4 GiB each)   |
| 32   | Vodes            | 851.4 GiB  | 557.9 GiB (65.53%)  | 19 (~44.8 GiB each)   |
| 33   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 34   | Erai-raws        | 839.3 GiB  | 116.5 GiB (13.89%)  | 48 (~17.5 GiB each)   |
| 35   | YURI             | 820.1 GiB  | 360.7 GiB (43.98%)  | 69 (~11.9 GiB each)   |
| 36   | Kawatare         | 818.6 GiB  | 700.0 GiB (85.51%)  | 26 (~31.5 GiB each)   |
| 37   | ZeroBuild        | 805.2 GiB  | 756.2 GiB (93.92%)  | 18 (~44.7 GiB each)   |
| 38   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 39   | LostYears        | 712.4 GiB  | 189.9 GiB (26.66%)  | 42 (~17.0 GiB each)   |
| 40   | Lulu             | 681.0 GiB  | 355.5 GiB (52.21%)  | 34 (~20.0 GiB each)   |
| 41   | Crash            | 653.9 GiB  | 653.9 GiB (100.00%) | 3 (~218.0 GiB each)   |
| 42   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 43   | Bunny-Apocalypse | 639.4 GiB  | 161.0 GiB (25.17%)  | 31 (~20.6 GiB each)   |
| 44   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 45   | Arid             | 602.0 GiB  | 201.1 GiB (33.40%)  | 42 (~14.3 GiB each)   |
| 46   | uba              | 587.8 GiB  | 587.8 GiB (100.00%) | 10 (~58.8 GiB each)   |
| 47   | VARYG            | 569.9 GiB  | 51.6 GiB (9.05%)    | 35 (~16.3 GiB each)   |
| 48   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 49   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 50   | Others           | 46.8 TiB   | 25.5 TiB (54.51%)   | 2038 (~23.5 GiB each) |
