from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with English dub but no dual-audio torrent."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        if anime.dubbed and not any(torrent.is_dual_audio for torrent in anime.seadex.torrents):
            entries.append(anime)
    return sort_by_popularity(entries)


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Dubbed Entries Without Dual Audio",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
