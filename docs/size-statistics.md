# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `151.5 TiB`
- Best size: `115.1 TiB`
- Alt size: `36.4 TiB`
- Realistic size: `118.4 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 15.1 TiB   | 14.3 TiB (94.73%)   | 179 (~86.1 GiB each)  |
| 2    | CRUCiBLE         | 9.4 TiB    | 9.4 TiB (100.00%)   | 129 (~75.0 GiB each)  |
| 3    | hchcsen          | 9.1 TiB    | 7.8 TiB (86.09%)    | 112 (~83.2 GiB each)  |
| 4    | NAN0             | 8.8 TiB    | 8.7 TiB (98.72%)    | 118 (~76.8 GiB each)  |
| 5    | Headpatter       | 5.8 TiB    | 4.3 TiB (74.01%)    | 199 (~29.6 GiB each)  |
| 6    | sam              | 4.1 TiB    | 3.8 TiB (93.58%)    | 137 (~30.7 GiB each)  |
| 7    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 98 (~39.2 GiB each)   |
| 8    | PMR              | 3.2 TiB    | 3.2 TiB (100.00%)   | 41 (~80.4 GiB each)   |
| 9    | B00BA            | 3.0 TiB    | 3.0 TiB (100.00%)   | 34 (~90.2 GiB each)   |
| 10   | TTGA             | 2.8 TiB    | 2.7 TiB (95.47%)    | 39 (~73.9 GiB each)   |
| 11   | GetItTwisted     | 2.1 TiB    | 1.6 TiB (77.58%)    | 67 (~31.9 GiB each)   |
| 12   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~619.5 GiB each)   |
| 13   | NOGRP            | 1.8 TiB    | 1.1 TiB (62.49%)    | 49 (~37.9 GiB each)   |
| 14   | MTBB             | 1.6 TiB    | 1.3 TiB (84.09%)    | 106 (~15.1 GiB each)  |
| 15   | Sylvar           | 1.4 TiB    | 1.3 TiB (94.97%)    | 17 (~83.3 GiB each)   |
| 16   | LaCroiX          | 1.4 TiB    | 1.4 TiB (100.00%)   | 19 (~74.3 GiB each)   |
| 17   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 18   | LazyRemux        | 1.3 TiB    | 1.3 TiB (100.00%)   | 19 (~68.9 GiB each)   |
| 19   | A&C              | 1.3 TiB    | 1.2 TiB (97.97%)    | 5 (~260.6 GiB each)   |
| 20   | nekotan          | 1.2 TiB    | 986.2 GiB (79.58%)  | 36 (~34.4 GiB each)   |
| 21   | SubsPlease       | 1.2 TiB    | 160.2 GiB (13.00%)  | 70 (~17.6 GiB each)   |
| 22   | YURASUKA         | 1.2 TiB    | 464.7 GiB (38.96%)  | 99 (~12.0 GiB each)   |
| 23   | FLE              | 1.1 TiB    | 1.0 TiB (93.83%)    | 29 (~38.3 GiB each)   |
| 24   | Erai-raws        | 1.0 TiB    | 154.5 GiB (14.40%)  | 65 (~16.5 GiB each)   |
| 25   | smol             | 991.2 GiB  | 941.7 GiB (95.01%)  | 56 (~17.7 GiB each)   |
| 26   | Mehul            | 969.8 GiB  | 910.5 GiB (93.89%)  | 28 (~34.6 GiB each)   |
| 27   | ZeroBuild        | 938.7 GiB  | 889.7 GiB (94.79%)  | 22 (~42.7 GiB each)   |
| 28   | Holomux          | 931.8 GiB  | 193.5 GiB (20.76%)  | 36 (~25.9 GiB each)   |
| 29   | Okay-Subs        | 922.7 GiB  | 867.1 GiB (93.98%)  | 43 (~21.5 GiB each)   |
| 30   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 31   | KH               | 914.0 GiB  | 116.7 GiB (12.77%)  | 57 (~16.0 GiB each)   |
| 32   | FraMeSToR        | 882.6 GiB  | 745.7 GiB (84.48%)  | 12 (~73.6 GiB each)   |
| 33   | LYS1TH3A         | 855.0 GiB  | 829.7 GiB (97.04%)  | 35 (~24.4 GiB each)   |
| 34   | Vodes            | 851.4 GiB  | 557.9 GiB (65.53%)  | 19 (~44.8 GiB each)   |
| 35   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 36   | YURI             | 820.1 GiB  | 360.7 GiB (43.98%)  | 69 (~11.9 GiB each)   |
| 37   | Kawatare         | 805.4 GiB  | 686.9 GiB (85.28%)  | 26 (~31.0 GiB each)   |
| 38   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 39   | LostYears        | 709.4 GiB  | 189.9 GiB (26.77%)  | 41 (~17.3 GiB each)   |
| 40   | Lulu             | 681.0 GiB  | 354.4 GiB (52.05%)  | 33 (~20.6 GiB each)   |
| 41   | Crash            | 653.9 GiB  | 653.9 GiB (100.00%) | 3 (~218.0 GiB each)   |
| 42   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 43   | Bunny-Apocalypse | 639.4 GiB  | 161.0 GiB (25.17%)  | 31 (~20.6 GiB each)   |
| 44   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 45   | Arid             | 599.1 GiB  | 201.1 GiB (33.56%)  | 41 (~14.6 GiB each)   |
| 46   | uba              | 587.8 GiB  | 587.8 GiB (100.00%) | 10 (~58.8 GiB each)   |
| 47   | Pizza            | 570.2 GiB  | 418.0 GiB (73.31%)  | 10 (~57.0 GiB each)   |
| 48   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 49   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 50   | Others           | 48.0 TiB   | 25.7 TiB (53.52%)   | 2089 (~23.5 GiB each) |
