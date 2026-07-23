"""
generate_terminal.py
=====================
Builds `assets/terminal-card.svg` — a premium macOS-style terminal
window that:
  1. Fetches the GitHub avatar for GITHUB_USERNAME.
  2. Converts it to high-density ASCII art with Pillow.
  3. Renders the ASCII art inside the terminal with a line-by-line
     typing reveal, a sweeping cursor, a blinking cursor, and a soft
     CRT glow — all via pure SMIL.

If the avatar can't be fetched (e.g. no network access, offline dev
environment), a deterministic placeholder gradient image is generated
locally so the script never fails.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (  # noqa: E402
    ASSETS_DIR, AVATAR_URL, GITHUB_USERNAME, NAME, TERMINAL_WIDTH,
    TERMINAL_HEIGHT, PALETTE,
)
from scripts.svg_common import (  # noqa: E402
    svg_open, svg_close, crt_filter, glow_filter, mac_dots, glass_panel,
    base_style, esc,
)

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None


# Dense-to-sparse ASCII ramp (dark -> light)
ASCII_RAMP = "@%#*+=-:. "

ASCII_COLS = 70
ASCII_ROWS = 34


def _fetch_avatar() -> "Image.Image":
    """Download the GitHub avatar; fall back to a generated placeholder
    if network access is unavailable."""
    if requests is not None:
        try:
            resp = requests.get(AVATAR_URL, timeout=8)
            resp.raise_for_status()
            return Image.open(io.BytesIO(resp.content)).convert("L")
        except Exception as exc:  # noqa: BLE001
            print(f"[terminal] avatar fetch failed ({exc}); using placeholder")

    # Deterministic placeholder: radial gradient circle, avoids crashing
    # in sandboxes without internet access.
    size = 200
    img = Image.new("L", (size, size), color=0)
    px = img.load()
    cx = cy = size / 2
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            px[x, y] = max(0, 255 - int(d * 1.9))
    return img


def image_to_ascii(cols: int = ASCII_COLS, rows: int = ASCII_ROWS) -> list[str]:
    """Convert the avatar into `rows` lines of `cols` ASCII characters."""
    if Image is None:
        # Absolute fallback if Pillow isn't installed for some reason.
        return [f"{'.' * cols}" for _ in range(rows)]

    img = _fetch_avatar()
    img = img.resize((cols, rows))
    pixels = list(img.getdata())

    ramp_len = len(ASCII_RAMP)
    lines: list[str] = []
    for r in range(rows):
        row_pixels = pixels[r * cols:(r + 1) * cols]
        line = "".join(
            ASCII_RAMP[min(ramp_len - 1, (255 - p) * ramp_len // 256)]
            for p in row_pixels
        )
        lines.append(line)
    return lines


def build(ascii_lines: list[str]) -> str:
    w, h = TERMINAL_WIDTH, TERMINAL_HEIGHT
    pad_x, top = 22, 58
    line_h = 14.5
    font_size = 9.3

    parts: list[str] = [svg_open(w, h)]
    parts.append("<defs>")
    parts.append(glow_filter("termGlow", 2.2))
    parts.append(crt_filter("crt"))
    parts.append("</defs>")
    parts.append(base_style(f".ascii{{fill:{PALETTE.green};}}"))

    # Window chrome
    parts.append(f'<rect width="{w}" height="{h}" rx="14" fill="{PALETTE.bg_alt}" '
                  f'stroke="{PALETTE.border}"/>')
    parts.append(f'<rect width="{w}" height="34" rx="14" fill="{PALETTE.panel}"/>')
    parts.append(f'<rect y="20" width="{w}" height="14" fill="{PALETTE.panel}"/>')
    parts.append(mac_dots(24, 17))
    parts.append(
        f'<text x="{w / 2}" y="21" text-anchor="middle" font-size="11" '
        f'class="dim">{GITHUB_USERNAME}@github: ~</text>'
    )

    # Body glass panel
    parts.append(glass_panel(10, 44, w - 20, h - 96, rx=10, opacity=0.35))

    # ASCII block, revealed line by line
    start_delay = 0.4
    per_line = 0.05
    for i, line in enumerate(ascii_lines):
        y = top + i * line_h
        begin = start_delay + i * per_line
        parts.append(
            f'<text x="{pad_x}" y="{y:.1f}" font-size="{font_size}" class="ascii" '
            f'filter="url(#crt)" opacity="0" xml:space="preserve">{esc(line)}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" '
            f'begin="{begin:.2f}s" fill="freeze"/>'
            f"</text>"
        )

    reveal_end = start_delay + len(ascii_lines) * per_line + 0.4

    # Sweeping horizontal scan line while typing
    parts.append(
        f'<rect x="{pad_x}" y="{top - 10}" width="{w - 2 * pad_x - 20}" height="2" '
        f'fill="{PALETTE.cyan}" opacity="0.55">'
        f'<animate attributeName="y" values="{top - 10};{top + len(ascii_lines) * line_h}" '
        f'dur="{reveal_end - start_delay:.2f}s" begin="{start_delay:.2f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0.55;0" begin="{reveal_end:.2f}s" '
        f'dur="0.4s" fill="freeze"/>'
        f"</rect>"
    )

    # Footer prompt block
    footer_y = h - 40
    footer_lines = [
        ("$ whoami", PALETTE.cyan),
        (NAME, PALETTE.text),
        ("AI Engineer · Machine Learning Enthusiast", PALETTE.text_dim),
    ]
    parts.append(f'<line x1="10" y1="{h - 58}" x2="{w - 10}" y2="{h - 58}" '
                  f'stroke="{PALETTE.border}"/>')
    for i, (txt, color) in enumerate(footer_lines):
        begin = reveal_end + 0.15 + i * 0.18
        parts.append(
            f'<text x="{pad_x}" y="{footer_y + i * 13}" font-size="10.5" fill="{color}" '
            f'opacity="0">{esc(txt)}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" '
            f'begin="{begin:.2f}s" fill="freeze"/>'
            f"</text>"
        )

    # Blinking cursor after final line
    cursor_x = pad_x + len(footer_lines[-1][0]) * 6.3
    cursor_begin = reveal_end + 0.15 + len(footer_lines) * 0.18
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="{footer_y + 2 * 13 - 9}" width="6.5" height="11" '
        f'fill="{PALETTE.green}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" '
        f'begin="{cursor_begin:.2f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" '
        f'begin="{cursor_begin + 0.2:.2f}s" repeatCount="indefinite"/>'
        f"</rect>"
    )

    parts.append(svg_close())
    return "\n".join(parts)


def main() -> None:
    ascii_lines = image_to_ascii()
    svg = build(ascii_lines)
    out_path = ASSETS_DIR / "terminal-card.svg"
    out_path.write_text(svg, encoding="utf-8")
    print(f"[terminal] wrote {out_path} ({len(ascii_lines)} ascii rows)")


if __name__ == "__main__":
    main()
