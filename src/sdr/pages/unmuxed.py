from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """
    An unmuxed entry is an entry that has a theoretical_best.
    """
    return sort_by_popularity(anime for anime in snapshot.entries.values() if anime.seadex.theoretical_best is not None)


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Unmuxed",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
