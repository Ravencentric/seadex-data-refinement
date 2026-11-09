from sdr.pages import Page
from sdr.shared import sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries marked incomplete on SeaDex."""
    return sort_by_popularity(anime for anime in snapshot.entries.values() if anime.seadex.is_incomplete)


def create() -> Page[tuple[Anime, ...]]:
    return Page(
        title="Incomplete Entries",
        prepare=prepare,
        export=lambda snapshot: summarize(prepare(snapshot)),
    )
