from sdr.pages import Page
from sdr.shared import sort_by_popularity
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with releases missing a season pack."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if any(torrent.grouped_url is not None for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...]]:
    return Page(title="Missing Season Packs", prepare=prepare)
