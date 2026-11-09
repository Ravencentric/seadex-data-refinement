from seadex import Tracker

from sdr.pages import Page
from sdr.shared import sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with releases on public trackers other than Nyaa."""
    return sort_by_popularity(
        anime
        for anime in snapshot.entries.values()
        if any(torrent.tracker.is_public() and torrent.tracker is not Tracker.NYAA for torrent in anime.seadex.torrents)
    )


def create() -> Page[tuple[Anime, ...]]:
    return Page(
        title="Public Releases Outside Nyaa",
        prepare=prepare,
        export=lambda snapshot: summarize(prepare(snapshot)),
    )
