from __future__ import annotations

import importlib
import importlib.resources
import inspect
from typing import TYPE_CHECKING, Final, Protocol, cast

if TYPE_CHECKING:
    from pathlib import Path

    from pyanilist import Media
    from seadex import EntryRecord


class Page(Protocol):
    @staticmethod
    def build(out: Path, snapshot: tuple[EntryRecord, ...], anilist_map: dict[int, Media]) -> None: ...


BUILDSIG: Final = inspect.signature(Page.build)


def pages() -> tuple[Page, ...]:
    loaded: list[Page] = []

    for file in importlib.resources.files(__package__).iterdir():
        if not file.is_file() or not file.name.endswith(".py") or file.name.startswith("_"):
            continue

        name = file.name.removesuffix(".py")
        module = importlib.import_module(f".{name}", __package__)
        buildfn = getattr(module, "build", None)

        if not callable(buildfn):
            msg = f"page module {name!r} must define a callable build()"
            raise TypeError(msg)

        if (sig := inspect.signature(buildfn)) != BUILDSIG:
            msg = f"page module {name!r} has an invalid build() signature: expected {BUILDSIG}, got {sig}"
            raise TypeError(msg)

        loaded.append(cast(Page, module))

    return tuple(loaded)


__all__ = ["Page", "pages"]
