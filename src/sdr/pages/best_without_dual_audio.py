from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries whose Best releases lack the dual audio available in Alts."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        best = tuple(torrent for torrent in anime.seadex.torrents if torrent.is_best)
        alt = tuple(torrent for torrent in anime.seadex.torrents if not torrent.is_best)
        if (
            best
            and not any(torrent.is_dual_audio for torrent in best)
            and any(torrent.is_dual_audio for torrent in alt)
        ):
            entries.append(anime)
    return sort_by_popularity(entries)


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Best Releases Without Dual Audio",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
