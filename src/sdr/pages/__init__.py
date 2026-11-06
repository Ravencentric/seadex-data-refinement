from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path

from sdr.snapshot import Snapshot


@dataclass(frozen=True, slots=True, kw_only=True)
class Page[Data]:
    """
    Skeleton of a Page.
    """

    title: str
    prepare: Callable[[Snapshot], Data]


def discover() -> dict[str, Page[object]]:
    """
    Find all the pages and get the Page object from them.
    """
    pages: dict[str, Page[object]] = {}
    for path in sorted(Path(__file__).parent.glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = import_module(f"{__name__}.{path.stem}")
        factory: object = getattr(module, "create", None)
        if not callable(factory):
            raise TypeError(f"{module.__name__} must define a create() factory")
        page: object = factory()
        if not isinstance(page, Page):
            raise TypeError(f"{module.__name__}.create() must return a Page")
        pages[path.stem] = page
    return pages
