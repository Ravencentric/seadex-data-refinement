import re

from seadex import EntryRecord

from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, is_slowpics_url, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def predicate(entry: EntryRecord, /) -> bool:
    if notes := entry.notes.casefold():
        if "remux" in notes:
            return False

        if re.search(r"web[-\s]?DL", notes.splitlines()[0], re.IGNORECASE):
            return False

    if entry.is_incomplete:
        return False

    comparisons = [comparison for comparison in entry.comparisons if is_slowpics_url(comparison)]
    if not comparisons:
        return False

    return any(torrent.is_best for torrent in entry.torrents)


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries where an encode beats the store."""
    return sort_by_popularity(anime for anime in snapshot.entries.values() if predicate(anime.seadex))


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Best Encode Releases",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
