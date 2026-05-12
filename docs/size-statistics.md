# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `137.2 TiB`
- Best size: `104.1 TiB`
- Alt size: `33.1 TiB`
- Realistic size: `107.4 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 13.8 TiB   | 13.0 TiB (94.01%)   | 188 (~75.2 GiB each)  |
| 2    | CRUCiBLE         | 10.0 TiB   | 10.0 TiB (100.00%)  | 136 (~75.0 GiB each)  |
| 3    | NAN0             | 8.3 TiB    | 8.2 TiB (99.09%)    | 111 (~76.3 GiB each)  |
| 4    | hchcsen          | 5.0 TiB    | 3.9 TiB (78.92%)    | 79 (~64.6 GiB each)   |
| 5    | Headpatter       | 4.3 TiB    | 3.4 TiB (78.30%)    | 139 (~31.6 GiB each)  |
| 6    | sam              | 3.9 TiB    | 3.6 TiB (93.25%)    | 132 (~30.3 GiB each)  |
| 7    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 97 (~40.0 GiB each)   |
| 8    | PMR              | 3.0 TiB    | 3.0 TiB (100.00%)   | 38 (~81.1 GiB each)   |
| 9    | TTGA             | 2.8 TiB    | 2.7 TiB (93.76%)    | 39 (~74.3 GiB each)   |
| 10   | B00BA            | 2.8 TiB    | 2.8 TiB (100.00%)   | 31 (~92.3 GiB each)   |
| 11   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~614.9 GiB each)   |
| 12   | MTBB             | 1.6 TiB    | 1.4 TiB (84.55%)    | 106 (~15.6 GiB each)  |
| 13   | LaCroiX          | 1.5 TiB    | 1.5 TiB (100.00%)   | 20 (~75.0 GiB each)   |
| 14   | GetItTwisted     | 1.4 TiB    | 1.1 TiB (72.86%)    | 55 (~26.9 GiB each)   |
| 15   | LazyRemux        | 1.4 TiB    | 1.4 TiB (100.00%)   | 20 (~72.3 GiB each)   |
| 16   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 17   | A&C              | 1.3 TiB    | 1.2 TiB (97.97%)    | 5 (~260.6 GiB each)   |
| 18   | SubsPlease       | 1.2 TiB    | 161.3 GiB (12.65%)  | 74 (~17.2 GiB each)   |
| 19   | NOGRP            | 1.1 TiB    | 786.3 GiB (71.23%)  | 38 (~29.0 GiB each)   |
| 20   | FLE              | 1.0 TiB    | 1022.7 GiB (96.41%) | 27 (~39.3 GiB each)   |
| 21   | smol             | 1.0 TiB    | 976.7 GiB (95.18%)  | 58 (~17.7 GiB each)   |
| 22   | YURASUKA         | 958.1 GiB  | 314.0 GiB (32.78%)  | 84 (~11.4 GiB each)   |
| 23   | KH               | 947.0 GiB  | 139.7 GiB (14.75%)  | 58 (~16.3 GiB each)   |
| 24   | LYS1TH3A         | 935.0 GiB  | 909.6 GiB (97.29%)  | 36 (~26.0 GiB each)   |
| 25   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 26   | YURI             | 873.3 GiB  | 389.7 GiB (44.62%)  | 71 (~12.3 GiB each)   |
| 27   | Okay-Subs        | 862.6 GiB  | 845.6 GiB (98.02%)  | 40 (~21.6 GiB each)   |
| 28   | Holomux          | 854.9 GiB  | 193.5 GiB (22.63%)  | 33 (~25.9 GiB each)   |
| 29   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 30   | Vodes            | 827.1 GiB  | 533.6 GiB (64.51%)  | 18 (~46.0 GiB each)   |
| 31   | FraMeSToR        | 822.9 GiB  | 822.9 GiB (100.00%) | 12 (~68.6 GiB each)   |
| 32   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 33   | ZeroBuild        | 761.7 GiB  | 712.7 GiB (93.57%)  | 17 (~44.8 GiB each)   |
| 34   | LostYears        | 738.3 GiB  | 207.6 GiB (28.12%)  | 44 (~16.8 GiB each)   |
| 35   | Mehul            | 735.2 GiB  | 735.2 GiB (100.00%) | 23 (~32.0 GiB each)   |
| 36   | Erai-raws        | 676.8 GiB  | 100.4 GiB (14.83%)  | 40 (~16.9 GiB each)   |
| 37   | Kawatare         | 675.5 GiB  | 575.2 GiB (85.14%)  | 23 (~29.4 GiB each)   |
| 38   | Lulu             | 664.4 GiB  | 339.0 GiB (51.02%)  | 33 (~20.1 GiB each)   |
| 39   | Bunny-Apocalypse | 657.3 GiB  | 161.0 GiB (24.49%)  | 31 (~21.2 GiB each)   |
| 40   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 41   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 42   | Arid             | 602.0 GiB  | 201.1 GiB (33.40%)  | 42 (~14.3 GiB each)   |
| 43   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 44   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 45   | BBT-RMX          | 555.0 GiB  | 374.5 GiB (67.47%)  | 13 (~42.7 GiB each)   |
| 46   | fig              | 552.9 GiB  | 552.9 GiB (100.00%) | 7 (~79.0 GiB each)    |
| 47   | Crash            | 552.3 GiB  | 552.3 GiB (100.00%) | 2 (~276.2 GiB each)   |
| 48   | SEV              | 542.9 GiB  | 0 B (0.00%)         | 11 (~49.4 GiB each)   |
| 49   | WAP              | 540.8 GiB  | 540.8 GiB (100.00%) | 6 (~90.1 GiB each)    |
| 50   | Others           | 45.0 TiB   | 24.4 TiB (54.22%)   | 2001 (~23.0 GiB each) |
