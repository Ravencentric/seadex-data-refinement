from typing import Final

from seadex import TorrentRecord

from sdr.history import Export
from sdr.pages import Page
from sdr.shared import Summary, sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot

# Groups that do not want their releases mirrored to public trackers.
EXCLUDED: Final[frozenset[str]] = frozenset({"-ZR-", "FraMeSToR", "NAN0", "KEKKU", "Doc", "Kitsune"})


def same_torrent(left: TorrentRecord, right: TorrentRecord) -> bool:
    """Check whether two tracker records contain the same release files."""
    left_files = {(file.name, file.size) for file in left.files}
    right_files = {(file.name, file.size) for file in right.files}
    if not left_files or not right_files:
        return False

    # A public megapack may contain every file from a private standalone torrent.
    same_files = left_files <= right_files or right_files <= left_files
    return same_files


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
            # The same release can have different Best/Alt labels across trackers,
            # for example when a public megapack contains more than this entry.
            # Match its files as well so a separate release by the same group does
            # not hide the private-only torrent.
            counterpart = any(
                other.release_group == torrent.release_group
                and other.is_best != torrent.is_best
                and same_torrent(torrent, other)
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
