# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `157.4 TiB`
- Best size: `119.6 TiB`
- Alt size: `37.9 TiB`
- Realistic size: `123.2 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 15.2 TiB   | 14.4 TiB (94.78%)   | 181 (~86.1 GiB each)  |
| 2    | hchcsen          | 9.4 TiB    | 8.1 TiB (86.17%)    | 115 (~83.8 GiB each)  |
| 3    | CRUCiBLE         | 9.4 TiB    | 9.4 TiB (100.00%)   | 128 (~75.0 GiB each)  |
| 4    | NAN0             | 9.2 TiB    | 9.1 TiB (98.77%)    | 121 (~77.7 GiB each)  |
| 5    | Headpatter       | 6.7 TiB    | 4.8 TiB (70.46%)    | 244 (~28.3 GiB each)  |
| 6    | Moxie            | 4.2 TiB    | 4.2 TiB (100.00%)   | 107 (~40.3 GiB each)  |
| 7    | sam              | 4.1 TiB    | 3.8 TiB (93.58%)    | 137 (~30.7 GiB each)  |
| 8    | PMR              | 3.3 TiB    | 3.3 TiB (100.00%)   | 41 (~81.6 GiB each)   |
| 9    | TTGA             | 3.0 TiB    | 2.9 TiB (95.76%)    | 41 (~75.2 GiB each)   |
| 10   | B00BA            | 3.0 TiB    | 3.0 TiB (100.00%)   | 34 (~90.2 GiB each)   |
| 11   | GetItTwisted     | 2.3 TiB    | 1.8 TiB (78.34%)    | 72 (~32.1 GiB each)   |
| 12   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~619.5 GiB each)   |
| 13   | NOGRP            | 1.7 TiB    | 1.1 TiB (62.41%)    | 46 (~38.2 GiB each)   |
| 14   | MTBB             | 1.6 TiB    | 1.3 TiB (84.09%)    | 106 (~15.1 GiB each)  |
| 15   | Sylvar           | 1.6 TiB    | 1.5 TiB (93.55%)    | 21 (~76.2 GiB each)   |
| 16   | A&C              | 1.4 TiB    | 1.4 TiB (98.14%)    | 5 (~285.4 GiB each)   |
| 17   | LaCroiX          | 1.4 TiB    | 1.4 TiB (100.00%)   | 19 (~74.3 GiB each)   |
| 18   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 19   | YURASUKA         | 1.3 TiB    | 604.9 GiB (45.32%)  | 107 (~12.5 GiB each)  |
| 20   | nekotan          | 1.3 TiB    | 1.0 TiB (80.76%)    | 39 (~34.1 GiB each)   |
| 21   | LazyRemux        | 1.3 TiB    | 1.3 TiB (100.00%)   | 19 (~68.9 GiB each)   |
| 22   | SubsPlease       | 1.2 TiB    | 144.0 GiB (12.00%)  | 68 (~17.6 GiB each)   |
| 23   | Mehul            | 1.1 TiB    | 1.0 TiB (94.74%)    | 29 (~38.9 GiB each)   |
| 24   | FLE              | 1.1 TiB    | 1.0 TiB (93.83%)    | 29 (~38.3 GiB each)   |
| 25   | Erai-raws        | 1.0 TiB    | 120.5 GiB (11.32%)  | 63 (~16.9 GiB each)   |
| 26   | smol             | 991.2 GiB  | 941.7 GiB (95.01%)  | 56 (~17.7 GiB each)   |
| 27   | Kawatare         | 971.6 GiB  | 853.1 GiB (87.80%)  | 32 (~30.4 GiB each)   |
| 28   | FraMeSToR        | 968.7 GiB  | 831.7 GiB (85.86%)  | 13 (~74.5 GiB each)   |
| 29   | Okay-Subs        | 957.0 GiB  | 884.1 GiB (92.38%)  | 46 (~20.8 GiB each)   |
| 30   | ZeroBuild        | 938.7 GiB  | 889.7 GiB (94.79%)  | 22 (~42.7 GiB each)   |
| 31   | KH               | 929.8 GiB  | 116.7 GiB (12.55%)  | 58 (~16.0 GiB each)   |
| 32   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 33   | Holomux          | 905.9 GiB  | 193.5 GiB (21.36%)  | 35 (~25.9 GiB each)   |
| 34   | LYS1TH3A         | 855.0 GiB  | 824.7 GiB (96.45%)  | 35 (~24.4 GiB each)   |
| 35   | Vodes            | 851.4 GiB  | 557.9 GiB (65.53%)  | 19 (~44.8 GiB each)   |
| 36   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 37   | YURI             | 820.1 GiB  | 340.3 GiB (41.49%)  | 71 (~11.6 GiB each)   |
| 38   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 39   | LostYears        | 709.4 GiB  | 189.9 GiB (26.77%)  | 41 (~17.3 GiB each)   |
| 40   | Lulu             | 681.0 GiB  | 354.4 GiB (52.05%)  | 33 (~20.6 GiB each)   |
| 41   | Drag             | 673.7 GiB  | 146.6 GiB (21.77%)  | 60 (~11.2 GiB each)   |
| 42   | Crash            | 653.9 GiB  | 653.9 GiB (100.00%) | 3 (~218.0 GiB each)   |
| 43   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 44   | Bunny-Apocalypse | 624.2 GiB  | 161.0 GiB (25.79%)  | 31 (~20.1 GiB each)   |
| 45   | Arid             | 599.1 GiB  | 201.1 GiB (33.56%)  | 41 (~14.6 GiB each)   |
| 46   | uba              | 598.6 GiB  | 598.6 GiB (100.00%) | 11 (~54.4 GiB each)   |
| 47   | CTR              | 589.2 GiB  | 138.6 GiB (23.52%)  | 26 (~22.7 GiB each)   |
| 48   | SEV              | 585.9 GiB  | 0 B (0.00%)         | 13 (~45.1 GiB each)   |
| 49   | Pizza            | 570.2 GiB  | 418.0 GiB (73.31%)  | 10 (~57.0 GiB each)   |
| 50   | Others           | 50.4 TiB   | 27.7 TiB (54.98%)   | 2130 (~24.2 GiB each) |
