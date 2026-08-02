# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `149.1 TiB`
- Best size: `113.5 TiB`
- Alt size: `35.6 TiB`
- Realistic size: `116.4 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 15.3 TiB   | 14.5 TiB (94.75%)   | 186 (~84.2 GiB each)  |
| 2    | CRUCiBLE         | 9.4 TiB    | 9.4 TiB (100.00%)   | 129 (~75.0 GiB each)  |
| 3    | NAN0             | 8.7 TiB    | 8.6 TiB (98.70%)    | 116 (~76.8 GiB each)  |
| 4    | hchcsen          | 8.5 TiB    | 7.2 TiB (85.09%)    | 111 (~78.4 GiB each)  |
| 5    | Headpatter       | 5.3 TiB    | 3.9 TiB (73.75%)    | 179 (~30.4 GiB each)  |
| 6    | sam              | 4.0 TiB    | 3.8 TiB (93.45%)    | 136 (~30.2 GiB each)  |
| 7    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 99 (~39.5 GiB each)   |
| 8    | PMR              | 3.1 TiB    | 3.1 TiB (100.00%)   | 40 (~80.5 GiB each)   |
| 9    | B00BA            | 2.9 TiB    | 2.9 TiB (100.00%)   | 33 (~89.3 GiB each)   |
| 10   | TTGA             | 2.8 TiB    | 2.7 TiB (95.47%)    | 39 (~73.9 GiB each)   |
| 11   | GetItTwisted     | 1.9 TiB    | 1.5 TiB (76.26%)    | 64 (~30.8 GiB each)   |
| 12   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~619.5 GiB each)   |
| 13   | NOGRP            | 1.8 TiB    | 1.1 TiB (63.06%)    | 49 (~37.9 GiB each)   |
| 14   | MTBB             | 1.6 TiB    | 1.4 TiB (84.55%)    | 106 (~15.6 GiB each)  |
| 15   | LaCroiX          | 1.5 TiB    | 1.5 TiB (100.00%)   | 20 (~75.0 GiB each)   |
| 16   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 17   | Sylvar           | 1.3 TiB    | 1.3 TiB (94.83%)    | 16 (~86.2 GiB each)   |
| 18   | LazyRemux        | 1.3 TiB    | 1.3 TiB (100.00%)   | 19 (~68.9 GiB each)   |
| 19   | A&C              | 1.3 TiB    | 1.2 TiB (97.97%)    | 5 (~260.6 GiB each)   |
| 20   | SubsPlease       | 1.3 TiB    | 192.6 GiB (14.83%)  | 75 (~17.3 GiB each)   |
| 21   | nekotan          | 1.2 TiB    | 986.2 GiB (79.58%)  | 36 (~34.4 GiB each)   |
| 22   | YURASUKA         | 1.2 TiB    | 474.4 GiB (40.04%)  | 99 (~12.0 GiB each)   |
| 23   | FLE              | 1.1 TiB    | 1022.7 GiB (93.72%) | 28 (~39.0 GiB each)   |
| 24   | smol             | 1022.8 GiB | 973.4 GiB (95.17%)  | 57 (~17.9 GiB each)   |
| 25   | FraMeSToR        | 959.9 GiB  | 822.9 GiB (85.73%)  | 13 (~73.8 GiB each)   |
| 26   | Erai-raws        | 938.1 GiB  | 116.5 GiB (12.42%)  | 53 (~17.7 GiB each)   |
| 27   | Holomux          | 931.8 GiB  | 193.5 GiB (20.76%)  | 36 (~25.9 GiB each)   |
| 28   | Mehul            | 926.2 GiB  | 866.9 GiB (93.60%)  | 27 (~34.3 GiB each)   |
| 29   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 30   | KH               | 914.0 GiB  | 139.7 GiB (15.28%)  | 57 (~16.0 GiB each)   |
| 31   | Okay-Subs        | 862.6 GiB  | 845.6 GiB (98.02%)  | 40 (~21.6 GiB each)   |
| 32   | LYS1TH3A         | 855.0 GiB  | 829.7 GiB (97.04%)  | 35 (~24.4 GiB each)   |
| 33   | Vodes            | 851.4 GiB  | 557.9 GiB (65.53%)  | 19 (~44.8 GiB each)   |
| 34   | ZeroBuild        | 850.1 GiB  | 801.2 GiB (94.24%)  | 19 (~44.7 GiB each)   |
| 35   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 36   | YURI             | 820.1 GiB  | 360.7 GiB (43.98%)  | 69 (~11.9 GiB each)   |
| 37   | Kawatare         | 818.6 GiB  | 700.0 GiB (85.51%)  | 26 (~31.5 GiB each)   |
| 38   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 39   | LostYears        | 709.4 GiB  | 189.9 GiB (26.77%)  | 41 (~17.3 GiB each)   |
| 40   | Lulu             | 681.0 GiB  | 355.5 GiB (52.21%)  | 34 (~20.0 GiB each)   |
| 41   | Bunny-Apocalypse | 664.1 GiB  | 161.0 GiB (24.24%)  | 32 (~20.8 GiB each)   |
| 42   | Crash            | 653.9 GiB  | 653.9 GiB (100.00%) | 3 (~218.0 GiB each)   |
| 43   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 44   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 45   | Arid             | 602.0 GiB  | 201.1 GiB (33.40%)  | 42 (~14.3 GiB each)   |
| 46   | uba              | 587.8 GiB  | 587.8 GiB (100.00%) | 10 (~58.8 GiB each)   |
| 47   | Pizza            | 570.2 GiB  | 418.0 GiB (73.31%)  | 10 (~57.0 GiB each)   |
| 48   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 49   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 50   | Others           | 46.9 TiB   | 25.2 TiB (53.73%)   | 2063 (~23.3 GiB each) |
