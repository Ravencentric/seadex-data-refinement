from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, is_slowpics_url, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries without a slow.pics comparison."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if not any(is_slowpics_url(comparison) for comparison in anime.seadex.comparisons)
    )


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Missing Comparisons",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
