from typing import Final

from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot

# Groups that do not want their releases mirrored to public trackers.
EXCLUDED: Final[frozenset[str]] = frozenset({"-ZR-", "FraMeSToR", "NAN0", "KEKKU", "Doc", "Kitsune"})


def select(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with private releases lacking a public alternative."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        for torrent in anime.seadex.torrents:
            if not torrent.tracker.is_private() or torrent.release_group in EXCLUDED:
                continue
            mirrored = any(
                other.tracker.is_public()
                and other.is_best == torrent.is_best
                and other.is_dual_audio >= torrent.is_dual_audio
                for other in anime.seadex.torrents
            )
            # For a given show (defined by AniList), the same torrent can exist on its own
            # on AB (because they enforce strict grouping) but in a megapack on Nyaa.
            # In these cases, SeaDex marks the AB torrent as Best, but the Nyaa
            # torrent as an Alt because the megapack also contains non-Best shows.
            counterpart = any(
                other.release_group == torrent.release_group and other.is_best != torrent.is_best
                for other in anime.seadex.torrents
            )
            if mirrored or counterpart:
                continue
            entries.append(anime)
            break
    return sort_by_popularity(entries)


def create() -> Page[tuple[Anime, ...], tuple[Summary, ...]]:
    return Page(
        title="Releases Only on Private Trackers",
        prepare=lambda snapshot, _: select(snapshot),
        export=Export(type=tuple[Summary, ...], collect=lambda snapshot: summarize(select(snapshot))),
    )
