from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_TEMPLATES = Path(__file__).parent.parent.parent / "templates"


def _human_size(num_bytes: int) -> str:
    if num_bytes < 0:
        msg = f"Cannot humanize negative byte count: {num_bytes}"
        raise ValueError(msg)
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return _format_size(size, unit)
        size /= 1024
    return _format_size(size, units[-1])


def _format_size(size: float, unit: str) -> str:
    if unit == "B":
        return f"{int(size)} {unit}"
    return f"{size:.1f} {unit}"


_ENV = Environment(
    loader=FileSystemLoader(_TEMPLATES),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
_ENV.filters["human_size"] = _human_size


def render_page(module_path: Path, dest: Path, **ctx: object) -> None:
    page_id = module_path.stem.replace("_", "-")
    template_name = f"{page_id}.md.j2"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_ENV.get_template(template_name).render(**ctx), encoding="utf-8")


def render_template(template_name: str, dest: Path, **ctx: object) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_ENV.get_template(template_name).render(**ctx), encoding="utf-8")


__all__ = ["render_page", "render_template"]
