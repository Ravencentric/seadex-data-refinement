import os.path
import re

from seadex import TorrentRecord

from sdr.pages import Page
from sdr.shared import sort_by_popularity, summarize
from sdr.snapshot import Anime, Snapshot


def is_remux(torrent: TorrentRecord) -> bool:
    """Whether a release is labelled as a remux."""
    # Check the largest to avoid false positives with stuff like NCOP/EDs
    largest = max(torrent.files, key=lambda file: file.size)
    name = os.path.basename(largest.name.replace("\\", "/"))
    name = name.replace("_", " ")
    # Match Remux, BDRemux, and DVDRemux as release labels.
    return re.search(r"(?:\b|BD|DVD)remux\b", name, re.IGNORECASE) is not None


def mentions_remux(notes: str) -> bool:
    """Whether entry notes describe a disc remux."""
    # Ignore edition labels such as "(Director's Cut)" between BD and Remux.
    notes = re.sub(r"\([^)]*\)", "", notes)
    return re.search(r"(?:BD(?:BOX)?|DVD)\s*Remux\b", notes, re.IGNORECASE) is not None


def prepare(snapshot: Snapshot) -> tuple[Anime, ...]:
    """Find entries with a remux best release and no alt releases."""
    entries: list[Anime] = []
    for anime in snapshot.entries.values():
        has_best = any(torrent.is_best for torrent in anime.seadex.torrents)
        has_alt = any(not torrent.is_best for torrent in anime.seadex.torrents)
        if not has_best or has_alt:
            continue

        if any(is_remux(torrent) for torrent in anime.seadex.torrents) or mentions_remux(anime.seadex.notes):
            entries.append(anime)

    return sort_by_popularity(entries)


def create() -> Page[tuple[Anime, ...]]:
    return Page(
        title="Best Remux Releases Without Alts",
        prepare=prepare,
        export=lambda snapshot: summarize(prepare(snapshot)),
    )
