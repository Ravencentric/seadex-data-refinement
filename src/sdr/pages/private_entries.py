from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries whose releases are all on private trackers."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if anime.seadex.torrents and all(torrent.tracker.is_private() for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Entries Only on Private Trackers",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
