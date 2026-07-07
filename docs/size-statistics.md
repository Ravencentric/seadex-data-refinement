# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `146.1 TiB`
- Best size: `111.3 TiB`
- Alt size: `34.7 TiB`
- Realistic size: `114.5 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 14.9 TiB   | 14.1 TiB (94.61%)   | 184 (~82.9 GiB each)  |
| 2    | CRUCiBLE         | 9.6 TiB    | 9.6 TiB (100.00%)   | 131 (~74.8 GiB each)  |
| 3    | hchcsen          | 8.6 TiB    | 7.3 TiB (84.70%)    | 111 (~79.2 GiB each)  |
| 4    | NAN0             | 8.4 TiB    | 8.3 TiB (98.66%)    | 115 (~75.2 GiB each)  |
| 5    | Headpatter       | 5.1 TiB    | 3.8 TiB (75.20%)    | 167 (~31.0 GiB each)  |
| 6    | sam              | 3.9 TiB    | 3.6 TiB (93.26%)    | 132 (~30.3 GiB each)  |
| 7    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 99 (~39.5 GiB each)   |
| 8    | PMR              | 3.1 TiB    | 3.1 TiB (100.00%)   | 38 (~82.8 GiB each)   |
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
| 20   | YURASUKA         | 1.1 TiB    | 428.2 GiB (37.60%)  | 97 (~11.7 GiB each)   |
| 21   | Sylvar           | 1.1 TiB    | 1.0 TiB (93.65%)    | 13 (~86.3 GiB each)   |
| 22   | FLE              | 1.0 TiB    | 1022.7 GiB (96.41%) | 27 (~39.3 GiB each)   |
| 23   | smol             | 1022.8 GiB | 973.4 GiB (95.17%)  | 57 (~17.9 GiB each)   |
| 24   | Mehul            | 926.2 GiB  | 866.9 GiB (93.60%)  | 27 (~34.3 GiB each)   |
| 25   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 26   | KH               | 914.0 GiB  | 139.7 GiB (15.28%)  | 57 (~16.0 GiB each)   |
| 27   | Holomux          | 881.0 GiB  | 193.5 GiB (21.96%)  | 34 (~25.9 GiB each)   |
| 28   | Okay-Subs        | 862.6 GiB  | 845.6 GiB (98.02%)  | 40 (~21.6 GiB each)   |
| 29   | LYS1TH3A         | 855.0 GiB  | 829.7 GiB (97.04%)  | 35 (~24.4 GiB each)   |
| 30   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 31   | YURI             | 834.0 GiB  | 360.7 GiB (43.25%)  | 70 (~11.9 GiB each)   |
| 32   | Vodes            | 827.1 GiB  | 533.6 GiB (64.51%)  | 18 (~46.0 GiB each)   |
| 33   | FraMeSToR        | 822.9 GiB  | 822.9 GiB (100.00%) | 12 (~68.6 GiB each)   |
| 34   | ZeroBuild        | 805.2 GiB  | 756.2 GiB (93.92%)  | 18 (~44.7 GiB each)   |
| 35   | Erai-raws        | 787.3 GiB  | 116.5 GiB (14.80%)  | 46 (~17.1 GiB each)   |
| 36   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 37   | LostYears        | 727.1 GiB  | 207.6 GiB (28.55%)  | 43 (~16.9 GiB each)   |
| 38   | Kawatare         | 699.3 GiB  | 580.7 GiB (83.04%)  | 24 (~29.1 GiB each)   |
| 39   | Lulu             | 681.0 GiB  | 355.5 GiB (52.21%)  | 34 (~20.0 GiB each)   |
| 40   | nekotan          | 671.7 GiB  | 632.9 GiB (94.22%)  | 12 (~56.0 GiB each)   |
| 41   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 42   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 43   | Bunny-Apocalypse | 620.3 GiB  | 161.0 GiB (25.95%)  | 30 (~20.7 GiB each)   |
| 44   | Arid             | 602.0 GiB  | 201.1 GiB (33.40%)  | 42 (~14.3 GiB each)   |
| 45   | VARYG            | 569.9 GiB  | 51.6 GiB (9.05%)    | 35 (~16.3 GiB each)   |
| 46   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 47   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 48   | BBT-RMX          | 555.0 GiB  | 374.5 GiB (67.47%)  | 13 (~42.7 GiB each)   |
| 49   | Crash            | 552.3 GiB  | 552.3 GiB (100.00%) | 2 (~276.2 GiB each)   |
| 50   | Others           | 46.4 TiB   | 25.3 TiB (54.62%)   | 2029 (~23.4 GiB each) |
