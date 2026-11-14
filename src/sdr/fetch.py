import datetime as dt
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from pathlib import Path
from time import perf_counter

from pyanilist import AniList, Media, MediaSort, MediaStatus, MediaType
from seadex import EntryRecord, SeaDexEntry

from sdr import dubs, network, snapshot
from sdr.snapshot import AniListId, Anime, Snapshot


def seadex() -> dict[AniListId, EntryRecord]:
    """Get seadex entries."""
    started = perf_counter()
    http = network.Client()
    records: dict[AniListId, EntryRecord] = {}
    print("Fetching SeaDex entries...", flush=True)

    with SeaDexEntry(client=http) as client:
        for record in client.iterator():
            identity = AniListId(record.anilist_id)
            assert identity not in records, f"Duplicate SeaDex entry for AniList {identity}"
            records[identity] = record

    assert records, "SeaDex returned no entries"
    print(
        f"Fetched {len(records)} SeaDex entries in {http.requests} HTTP requests ({perf_counter() - started:.2f}s)",
        flush=True,
    )
    return records


def anilist(identities: Iterable[AniListId]) -> dict[AniListId, Media]:
    """Get the AniList data for every given AniList ID."""
    started = perf_counter()
    http = network.Client()
    records: dict[AniListId, Media] = {}
    print("Fetching AniList metadata...", flush=True)

    with AniList(client=http) as client:
        for record in client.get_media_many(id_in=sorted(identities), type=MediaType.ANIME, sort=MediaSort.ID):
            identity = AniListId(record.id)
            assert identity not in records, f"Duplicate AniList entry {identity}"
            records[identity] = record

    print(
        f"Fetched {len(records)} AniList entries in {http.requests} HTTP requests ({perf_counter() - started:.2f}s)",
        flush=True,
    )
    return records


def missing(identities: Iterable[AniListId]) -> tuple[Media, ...]:
    """Get the 500 most popular finished anime absent from SeaDex."""
    started = perf_counter()
    http = network.Client()
    print("Fetching AniList titles missing from SeaDex...", flush=True)

    with AniList(client=http) as client:
        media = client.get_media_many(
            id_not_in=sorted(identities),
            type=MediaType.ANIME,
            status=MediaStatus.FINISHED,
            sort=MediaSort.POPULARITY_DESC,
        )
        records = tuple(islice(media, 500))

    print(
        f"Fetched {len(records)} missing titles in {http.requests} HTTP requests ({perf_counter() - started:.2f}s)",
        flush=True,
    )
    return records


def fetch(path: Path) -> Snapshot:
    """Fetch a snapshot of SeaDex enriched with AniList metadata."""
    captured = dt.datetime.now(dt.UTC)
    entries = seadex()
    # Three independent requests so we can try to get them done together.
    # 2 workers because 3 ends up slowing us down due to rate limits kicking in.
    with ThreadPoolExecutor(max_workers=2) as executor:
        metadata = executor.submit(anilist, entries.keys())
        evidence = executor.submit(dubs.dubs, entries.keys())
        popular = executor.submit(missing, entries.keys())
        media = metadata.result()
        dubbed = evidence.result()
        absent = popular.result()
    joined: dict[AniListId, Anime] = {}
    for identity, entry in entries.items():
        joined[identity] = Anime(
            seadex=entry,
            anilist=media[identity],
            dubbed=dubbed[identity],
        )

    result = Snapshot(
        version=3,
        captured=captured,
        entries=joined,
        missing=absent,
    )
    snapshot.save(result, path)
    return result
