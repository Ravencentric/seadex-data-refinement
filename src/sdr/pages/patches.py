from seadex import Tag

from sdr.pages import Page
from sdr.shared import sort_by_popularity
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with at least one release requiring a patch."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if any(Tag.PATCH_REQUIRED in torrent.tags for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...]]:
    return Page(title="Releases Needing Patches", prepare=prepare)
