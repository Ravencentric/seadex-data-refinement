from datetime import datetime

from seadex import TorrentRecord

from sdr.pages import Page
from sdr.snapshot import Snapshot


def prepare(snapshot: Snapshot) -> datetime:
    return snapshot.captured


def export(snapshot: Snapshot) -> dict[str, int]:
    """A callable that's supposed to produce page data suitable for serialization."""
    torrents: set[TorrentRecord] = set()
    for anime in snapshot.entries.values():
        torrents.update(anime.seadex.torrents)
    groups = {torrent.release_group for torrent in torrents}
    return {"entries": len(snapshot.entries), "torrents": len(torrents), "groups": len(groups)}


def create() -> Page[datetime]:
    return Page(title="Home", prepare=prepare, export=export)
