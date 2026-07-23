"""
svg_common.py
=============
Small, dependency-free helpers for building hand-rolled SVG + SMIL markup.
Every generator script imports from here instead of duplicating boilerplate
(gradients, glow filters, glass panels, monospace text rows).

No JavaScript is used anywhere — all motion is pure SMIL (<animate>,
<animateTransform>) and all interactivity (hover) is pure CSS inside a
single inline <style> block, which keeps every SVG 100% self-contained.
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import PALETTE  # noqa: E402


def esc(text: str) -> str:
    """Escape text for safe embedding inside SVG/XML."""
    return escape(str(text))


def svg_open(width: int, height: int, extra_class: str = "") -> str:
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" '
        f'{f"class=\"{extra_class}\" " if extra_class else ""}'
        f'font-family="JetBrains Mono, Fira Code, Consolas, monospace">'
    )


def svg_close() -> str:
    return "</svg>"


def glow_filter(fid: str, std_dev: float = 3.2) -> str:
    """A soft neon glow filter usable via filter="url(#fid)"."""
    return f"""
    <filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="{std_dev}" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>"""


def crt_filter(fid: str) -> str:
    """Subtle CRT scanline / glow filter for the terminal card."""
    return f"""
    <filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="0.6" result="soft"/>
      <feColorMatrix in="soft" type="matrix"
        values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.9 0" result="tinted"/>
      <feMerge>
        <feMergeNode in="tinted"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>"""


def linear_gradient(gid: str, stops: list[tuple[str, str, float]], angle: str = "0%") -> str:
    """stops: list of (offset%, color, opacity)."""
    inner = "".join(
        f'<stop offset="{off}" stop-color="{color}" stop-opacity="{op}"/>'
        for off, color, op in stops
    )
    return f'<linearGradient id="{gid}" x1="0%" y1="0%" x2="100%" y2="{angle}">{inner}</linearGradient>'


def radial_gradient(gid: str, stops: list[tuple[str, str, float]]) -> str:
    inner = "".join(
        f'<stop offset="{off}" stop-color="{color}" stop-opacity="{op}"/>'
        for off, color, op in stops
    )
    return f'<radialGradient id="{gid}" cx="50%" cy="50%" r="70%">{inner}</radialGradient>'


def glass_panel(x: int, y: int, w: int, h: int, rx: int = 16, opacity: float = 0.55) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{PALETTE.panel}" fill-opacity="{opacity}" '
        f'stroke="{PALETTE.border}" stroke-width="1"/>'
    )


def mac_dots(x: int, y: int) -> str:
    colors = ["#ff5f56", "#ffbd2e", "#27c93f"]
    dots = "".join(
        f'<circle cx="{x + i * 18}" cy="{y}" r="5.5" fill="{c}"/>'
        for i, c in enumerate(colors)
    )
    return dots


def base_style(extra: str = "") -> str:
    """Inline <style> block shared by all cards (fonts, base fill, hover)."""
    return f"""
    <style>
      text {{ font-family: 'JetBrains Mono','Fira Code',Consolas,monospace; }}
      .sans {{ font-family: 'Segoe UI','Inter',Helvetica,Arial,sans-serif; }}
      .dim {{ fill: {PALETTE.text_dim}; }}
      .bright {{ fill: {PALETTE.text}; }}
      {extra}
    </style>"""
