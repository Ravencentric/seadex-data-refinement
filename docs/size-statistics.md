# Size Statistics

These statistics are NOT 100% accurate, but they likely are as realistic as (reasonably) possible.

The definition of an entry (or a "complete" torrent) is quite murky. SeaDex defines it as an AniList entry, but every private tracker has their own definition (typically, they follow AniDB or TVDB), while Nyaa does not enforce a specific definition. Every release can quite possibly have slightly different torrents across trackers, or a single torrent on Nyaa can include several SeaDex entries. A Nyaa torrent might contain an entire franchise, but only a single file out of it might be relevant.

All of this and more means that we need to settle on a method to calculate these statistics. This was essentially calculated by iterating over every SeaDex entry, and if an entry has both private tracker torrent and public torrent from the same group, only the former is considered; otherwise, all torrents are considered. The `total_entries` metric counts how many times a group appears across entries, with each group counted up to twice per entry—once for best torrents and once for alt torrents. This avoids skewing results from entries with multiple torrents (e.g., a single entry with 12 torrents counts as one for `total_entries`). Exact duplicates are also discarded.

## Overview

- Total size: `131.7 TiB`
- Best size: `100.1 TiB`
- Alt size: `31.7 TiB`
- Realistic size: `103.1 TiB`

The `Realistic size` stat tries to emulate a scenario where a user will likely download the best dual audio release for an entry, falling back to the best single audio release if that's not present, and again falling back to whatever is available if neither exists.


## Breakdown by Group

| Rank | Group            | Total Size | Best Size           | Total Entries         |
| :----| :----------------| :----------| :-------------------| :---------------------|
| 1    | -ZR-             | 13.9 TiB   | 13.1 TiB (94.05%)   | 189 (~75.3 GiB each)  |
| 2    | CRUCiBLE         | 10.3 TiB   | 10.3 TiB (100.00%)  | 140 (~75.3 GiB each)  |
| 3    | NAN0             | 8.3 TiB    | 8.2 TiB (99.09%)    | 110 (~76.8 GiB each)  |
| 4    | sam              | 3.9 TiB    | 3.6 TiB (92.76%)    | 132 (~30.3 GiB each)  |
| 5    | Headpatter       | 3.8 TiB    | 3.2 TiB (81.89%)    | 116 (~34.0 GiB each)  |
| 6    | Moxie            | 3.8 TiB    | 3.8 TiB (100.00%)   | 97 (~40.0 GiB each)   |
| 7    | hchcsen          | 3.0 TiB    | 2.1 TiB (70.18%)    | 73 (~41.8 GiB each)   |
| 8    | PMR              | 2.8 TiB    | 2.8 TiB (100.00%)   | 37 (~78.8 GiB each)   |
| 9    | TTGA             | 2.6 TiB    | 2.5 TiB (95.12%)    | 36 (~74.4 GiB each)   |
| 10   | B00BA            | 2.3 TiB    | 2.3 TiB (100.00%)   | 26 (~91.1 GiB each)   |
| 11   | SoM              | 1.8 TiB    | 1.8 TiB (100.00%)   | 3 (~614.9 GiB each)   |
| 12   | MTBB             | 1.6 TiB    | 1.4 TiB (84.49%)    | 105 (~15.7 GiB each)  |
| 13   | LazyRemux        | 1.4 TiB    | 1.4 TiB (100.00%)   | 20 (~72.3 GiB each)   |
| 14   | LaCroiX          | 1.4 TiB    | 1.4 TiB (100.00%)   | 19 (~75.5 GiB each)   |
| 15   | JySzE            | 1.4 TiB    | 1.4 TiB (100.00%)   | 6 (~232.1 GiB each)   |
| 16   | SubsPlease       | 1.3 TiB    | 161.3 GiB (12.34%)  | 76 (~17.2 GiB each)   |
| 17   | A&C              | 1.3 TiB    | 1.2 TiB (97.97%)    | 5 (~260.6 GiB each)   |
| 18   | GetItTwisted     | 1.2 TiB    | 917.6 GiB (74.17%)  | 49 (~25.2 GiB each)   |
| 19   | FLE              | 1.0 TiB    | 993.1 GiB (96.30%)  | 26 (~39.7 GiB each)   |
| 20   | smol             | 1.0 TiB    | 976.7 GiB (95.18%)  | 58 (~17.7 GiB each)   |
| 21   | NOGRP            | 984.4 GiB  | 771.9 GiB (78.41%)  | 32 (~30.8 GiB each)   |
| 22   | LYS1TH3A         | 935.0 GiB  | 909.6 GiB (97.29%)  | 36 (~26.0 GiB each)   |
| 23   | koala            | 920.5 GiB  | 920.5 GiB (100.00%) | 18 (~51.1 GiB each)   |
| 24   | KH               | 887.7 GiB  | 139.7 GiB (15.74%)  | 57 (~15.6 GiB each)   |
| 25   | YURASUKA         | 887.1 GiB  | 243.1 GiB (27.40%)  | 78 (~11.4 GiB each)   |
| 26   | Holomux          | 887.0 GiB  | 193.5 GiB (21.81%)  | 34 (~26.1 GiB each)   |
| 27   | YURI             | 873.3 GiB  | 389.7 GiB (44.62%)  | 71 (~12.3 GiB each)   |
| 28   | Okay-Subs        | 862.6 GiB  | 845.6 GiB (98.02%)  | 40 (~21.6 GiB each)   |
| 29   | RUDY             | 846.8 GiB  | 828.3 GiB (97.80%)  | 11 (~77.0 GiB each)   |
| 30   | Vodes            | 827.1 GiB  | 533.6 GiB (64.51%)  | 18 (~46.0 GiB each)   |
| 31   | FraMeSToR        | 822.9 GiB  | 822.9 GiB (100.00%) | 12 (~68.6 GiB each)   |
| 32   | sittingmongoose  | 782.5 GiB  | 782.5 GiB (100.00%) | 1 (~782.5 GiB each)   |
| 33   | UQW              | 765.4 GiB  | 36.3 GiB (4.74%)    | 8 (~95.7 GiB each)    |
| 34   | ZeroBuild        | 761.7 GiB  | 712.7 GiB (93.57%)  | 17 (~44.8 GiB each)   |
| 35   | LostYears        | 727.1 GiB  | 207.6 GiB (28.55%)  | 43 (~16.9 GiB each)   |
| 36   | Bunny-Apocalypse | 698.0 GiB  | 161.0 GiB (23.06%)  | 33 (~21.2 GiB each)   |
| 37   | Lulu             | 664.4 GiB  | 339.0 GiB (51.02%)  | 33 (~20.1 GiB each)   |
| 38   | Mehul            | 662.7 GiB  | 662.7 GiB (100.00%) | 21 (~31.6 GiB each)   |
| 39   | Arid             | 645.1 GiB  | 207.8 GiB (32.20%)  | 45 (~14.3 GiB each)   |
| 40   | Erai-raws        | 644.7 GiB  | 84.2 GiB (13.06%)   | 38 (~17.0 GiB each)   |
| 41   | Drag             | 641.2 GiB  | 146.0 GiB (22.76%)  | 59 (~10.9 GiB each)   |
| 42   | Meakes           | 637.8 GiB  | 624.4 GiB (97.90%)  | 9 (~70.9 GiB each)    |
| 43   | Reza             | 636.9 GiB  | 273.3 GiB (42.91%)  | 26 (~24.5 GiB each)   |
| 44   | D4C              | 556.0 GiB  | 556.0 GiB (100.00%) | 2 (~278.0 GiB each)   |
| 45   | Almighty         | 555.9 GiB  | 0 B (0.00%)         | 5 (~111.2 GiB each)   |
| 46   | fig              | 552.9 GiB  | 552.9 GiB (100.00%) | 7 (~79.0 GiB each)    |
| 47   | Crash            | 552.3 GiB  | 552.3 GiB (100.00%) | 2 (~276.2 GiB each)   |
| 48   | BBT-RMX          | 548.0 GiB  | 374.5 GiB (68.33%)  | 12 (~45.7 GiB each)   |
| 49   | WAP              | 540.8 GiB  | 540.8 GiB (100.00%) | 6 (~90.1 GiB each)    |
| 50   | Others           | 42.8 TiB   | 23.6 TiB (55.07%)   | 1928 (~22.8 GiB each) |
