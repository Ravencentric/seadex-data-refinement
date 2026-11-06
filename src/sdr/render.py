import html
import re

from jinja2 import Environment, PackageLoader, StrictUndefined

from sdr.pages import Page
from sdr.snapshot import Snapshot


def literal(value: str) -> str:
    """
    Keep titles from being interpreted as Markdown or HTML.

    This exists for anime titles, which may have special characters
    that can be interpreted as markdown or html.

    For example, without this function,
    "<DOGEZA>I Tried Asking While Kowtowing."
    will only show up as "I Tried Asking While Kowtowing."
    becuase `<>` gets interpreted as an HTML tag.
    """
    text = html.escape(" ".join(value.splitlines()), quote=False)
    return re.sub(r"[\\`*_{}\[\]|~/]", lambda match: f"&#{ord(match[0])};", text)


def slug(value: str) -> str:
    """Turn title words into a readable URL slug."""
    return re.sub(r"[\W_]+", "-", value.casefold()).strip("-")


def environment() -> Environment:
    """
    Preconfigured jinja environment.
    """
    environment = Environment(
        loader=PackageLoader("sdr", package_path="pages"),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters["literal"] = literal
    environment.filters["slug"] = slug
    return environment


def render[Data](environment: Environment, name: str, page: Page[Data], snapshot: Snapshot) -> str:
    """Render a page."""
    template = environment.get_template(f"{name}.md.jinja")
    return template.render(page=page, snapshot=snapshot, data=page.prepare(snapshot))
