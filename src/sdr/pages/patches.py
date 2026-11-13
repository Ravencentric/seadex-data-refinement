from seadex import Tag

from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with at least one release requiring a patch."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if any(Tag.PATCH_REQUIRED in torrent.tags for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Releases Needing Patches",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
