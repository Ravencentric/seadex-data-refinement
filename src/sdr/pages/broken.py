from collections.abc import Iterator
from dataclasses import dataclass

from seadex import Tag, TorrentRecord

from sdr.history import Export, History
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


@dataclass(frozen=True, slots=True, kw_only=True)
class Row:
    anime: Anime
    groups: tuple[str, ...]


def broken(anime: Anime) -> Iterator[TorrentRecord]:
    """Yield the entry's releases marked as broken."""
    return (torrent for torrent in anime.seadex.torrents if Tag.BROKEN in torrent.tags)


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with at least one release marked as broken."""
    return sort_by_popularity(anime for anime in snapshot.entries.values() if any(broken(anime)))


def prepare(snapshot: Snapshot, _: History[tuple[Summary, ...]]) -> tuple[Row, ...]:
    """Show each group with a broken release once per entry."""
    rows: list[Row] = []
    for anime in sort_by_popularity(snapshot.entries.values()):
        groups = {torrent.release_group for torrent in broken(anime)}
        if groups:
            rows.append(Row(anime=anime, groups=tuple(sorted(groups))))
    return tuple(rows)


def create() -> Page[tuple[Row, ...], tuple[Summary, ...]]:
    return Page(
        title="Broken Releases",
        prepare=prepare,
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
