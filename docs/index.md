SeaDex Data Refinement
======================

SeaDex Data Refinement[^1], brought to you by Lumon Industries[^2], 
provides information and identifies specific [SeaDex](https://releases.moe) entries that are currently lacking in one way or another.
You can use this page as a resource to stay informed and help contribute to SeaDex.

If you notice any entries that seem to be in the wrong category, please report them [here](https://github.com/Ravencentric/seadex-data-refinement/issues).
For any other issues with SeaDex, please report them to the [SeaDex Discord server](https://discord.com/invite/jPeeZewWRn).

[^1]: <https://severance.wiki/macrodata_refinement>
[^2]: <https://severance.wiki/lumon_industries>

```{toctree}
:hidden:

leaderboards.md
size-statistics.md
unmuxed.md
no-comparisons.md
marked-incomplete.md
public-non-nyaa.md
private-tracker-only-entries.md
private-tracker-only-torrents.md
public-tracker-only.md
top-500.md
best-missing-dual.md
alt-missing-dual.md
no-dub.md
encode-best-entries.md
patch-required.md
broken-entries.md
missing-season-pack.md
```

## Overview

* {doc}`leaderboards`: Leaderboards for SeaDex entries.

* {doc}`size-statistics`: Statistics about SeaDex's size.

* {doc}`unmuxed`: SeaDex entries that outline the recommended combinations for muxing to create the ideal release. Check out the [tutorial](https://thewiki.moe/advanced/muxing/) if you want to mux these releases.

* {doc}`no-comparisons`: SeaDex entries without any comparisons. Check out the [tutorial](https://thewiki.moe/tutorials/comparison/) if you're interested in making comparisons, and share them in the `#comparisons` channel on [Discord](https://discord.com/invite/jPeeZewWRn).

* {doc}`marked-incomplete`: SeaDex entries explicitly marked as incomplete by the editors. They often lack comparisons or contain *useless* comparisons that need to be replaced with proper ones, though other issues may also contribute to their incomplete status.

* {doc}`public-non-nyaa`: SeaDex entries that are publicly available but not yet on Nyaa. Reposting them to Nyaa is a simple way to contribute, just be mindful of Nyaa's rules.

* {doc}`private-tracker-only-entries`: SeaDex entries found only on private trackers. You can contribute by reposting them to Nyaa, but only if the private tracker allows it.

* {doc}`private-tracker-only-torrents`: SeaDex entries with atleast one torrent found only on private trackers. You can contribute by reposting them to Nyaa, but only if the private tracker allows it.

* {doc}`public-tracker-only`: SeaDex entries found only on public trackers. You can contribute by reposting them to private trackers, following their rules and requirements.

* {doc}`top-500`: Top 500 AniList entries that aren't yet on SeaDex. If you'd like to see any of these added, your comparison submissions are needed. The [tutorial](https://thewiki.moe/tutorials/comparison/) provides a step-by-step guide. Once you've made your comparisons, please share them in the `#comparisons` channel on [Discord](https://discord.com/invite/jPeeZewWRn).

* {doc}`best-missing-dual`: Best entries that currently do not have a dual audio version available. If you're interested in creating dual audio muxes for these entries, it's recommended to first join the [Discord](https://discord.com/invite/jPeeZewWRn) to consult with others before starting. You can also find a helpful guide in the [muxing tutorial](https://thewiki.moe/advanced/muxing/).

* {doc}`alt-missing-dual`: Same as best-missing-dual, but for alt releases instead.

* {doc}`no-dub`: For entries where none have dual audio but there is a dub according to AniList.

* {doc}`encode-best-entries`: Entries where an encode beats the store.

* {doc}`patch-required`: An entry appears here if at least one of its releases requires a patch to be applied.

* {doc}`broken-entries`: An entry appears here if at least one of its releases is marked as broken.

* {doc}`missing-season-pack.md`: Entries that do not have a complete season pack available.

## Running locally

If you just want to build the docs:

````{tab} uv
```console
$ git clone https://github.com/Ravencentric/seadex-data-refinement.git
$ cd seadex-data-refinement
$ uv run nox -s build-docs
```
````

````{tab} python
```console
$ git clone https://github.com/Ravencentric/seadex-data-refinement.git
$ cd seadex-data-refinement
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install .
$ nox -s build-docs
```
````

If you want to use the underlying SeaDex Data Refinement (SDR) CLI:

````{tab} uv
```console
$ git clone https://github.com/Ravencentric/seadex-data-refinement.git
$ cd seadex-data-refinement
$ uv run sdr --help
```
````

````{tab} python
```console
$ git clone https://github.com/Ravencentric/seadex-data-refinement.git
$ cd seadex-data-refinement
$ python -m venv .venv
$ source .venv/bin/activate
$ python -m pip install .
$ sdr --help
```
````

The CLI tool provides additional functionalities, such as controlling the maximum number of entries retrieved and outputting data in JSON format.