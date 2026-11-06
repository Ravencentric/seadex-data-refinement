from sdr.pages import Page
from sdr.shared import sort_by_popularity
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """
    An unmuxed entry is an entry that has a theoretical_best.
    """
    return sort_by_popularity(anime for anime in snapshot.entries.values() if anime.seadex.theoretical_best is not None)


def create() -> Page[tuple[Anime, ...]]:
    return Page(title="Unmuxed", prepare=prepare)
