from datetime import datetime

from sdr.pages import Page
from sdr.snapshot import Snapshot


def prepare(snapshot: Snapshot) -> datetime:
    return snapshot.captured


def create() -> Page[datetime]:
    return Page(title="Home", prepare=prepare)
