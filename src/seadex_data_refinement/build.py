from __future__ import annotations

from pathlib import Path

from tqdm import tqdm

from . import anilist, fetch
from .pages import PAGES
from .render import render_template


def build(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    snapshot = fetch.snapshot()
    anilist_map = anilist.enrich({e.anilist_id for e in snapshot})
    for module in tqdm(PAGES, desc="Rendering", unit="page"):
        module.build(out, snapshot, anilist_map)
    render_template("index.md.j2", out / "index.md")
