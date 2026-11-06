from sdr.pages import Page
from sdr.shared import sort_by_popularity
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries whose releases are all on private trackers."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if anime.seadex.torrents and all(torrent.tracker.is_private() for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...]]:
    return Page(title="Entries Only on Private Trackers", prepare=prepare)
