from sdr.pages import Page
from sdr.shared import sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with English dub but no dual-audio torrent."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        if anime.dubbed and not any(torrent.is_dual_audio for torrent in anime.seadex.torrents):
            entries.append(anime)
    return sort_by_popularity(entries)


def create() -> Page[tuple[Anime, ...]]:
    return Page(
        title="Dubbed Entries Without Dual Audio",
        prepare=prepare,
        export=lambda snapshot: summarize(prepare(snapshot)),
    )
