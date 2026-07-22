from __future__ import annotations

from pathlib import Path

from tqdm import tqdm

from . import anilist, fetch
from .pages import pages
from .render import render_template


def build(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    entries = anilist.enrich(fetch.snapshot())
    for module in tqdm(pages(), desc="Rendering", unit="page"):
        module.build(out, entries)
    render_template("index.md.j2", out / "index.md")
