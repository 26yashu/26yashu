"""
generate_header.py
===================
Builds `assets/header.svg` — a premium animated hero banner with an
animated gradient title, a typed subtitle, soft glow, and minimal
floating particles. Pure SVG + SMIL, no JavaScript, no external CSS.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (  # noqa: E402
    ASSETS_DIR, HEADER_WIDTH, HEADER_HEIGHT, NAME, SUBTITLE, PALETTE,
)
from scripts.svg_common import (  # noqa: E402
    svg_open, svg_close, glow_filter, linear_gradient, radial_gradient,
    base_style, esc,
)


def _particles(n: int, w: int, h: int, seed: int = 7) -> str:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        cx = rng.uniform(20, w - 20)
        cy = rng.uniform(20, h - 20)
        r = rng.uniform(1.0, 2.4)
        dur = rng.uniform(4.5, 8.5)
        delay = rng.uniform(0, 3)
        color = rng.choice([PALETTE.cyan, PALETTE.green, PALETTE.purple])
        out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="{color}" opacity="0.0">'
            f'<animate attributeName="opacity" values="0;0.8;0" dur="{dur:.2f}s" '
            f'begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{cy:.1f};{cy - 18:.1f};{cy:.1f}" '
            f'dur="{dur * 1.4:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    return "\n".join(out)


def _typed_subtitle(text: str, x: int, y: int, start: float = 1.6) -> str:
    """Character-by-character reveal using a clip-path width animation
    (keeps a single <text> node instead of one node per glyph)."""
    n = len(text)
    dur = max(1.6, n * 0.045)
    return f"""
    <clipPath id="typeClip">
      <rect x="{x - 4}" y="{y - 22}" height="30" width="0">
        <animate attributeName="width" from="0" to="620" dur="{dur:.2f}s"
                 begin="{start:.2f}s" fill="freeze" calcMode="linear"/>
      </rect>
    </clipPath>
    <text x="{x}" y="{y}" font-size="16" letter-spacing="0.5"
          fill="{PALETTE.text_dim}" clip-path="url(#typeClip)">{esc(text)}</text>
    <rect x="{x - 4}" y="{y - 22}" width="2.4" height="20" fill="{PALETTE.cyan}">
      <animate attributeName="x" from="{x - 4}" to="{x + 616}" dur="{dur:.2f}s"
               begin="{start:.2f}s" fill="freeze" calcMode="linear"/>
      <animate attributeName="opacity" values="1;0;1" dur="0.9s"
               begin="{start + dur:.2f}s" repeatCount="indefinite"/>
    </rect>"""


def build() -> str:
    w, h = HEADER_WIDTH, HEADER_HEIGHT
    cx, cy = w // 2, h // 2

    parts: list[str] = [svg_open(w, h)]
    parts.append("<defs>")
    parts.append(radial_gradient("bgGlow", [
        ("0%", PALETTE.cyan, 0.16), ("55%", PALETTE.purple, 0.08), ("100%", PALETTE.bg, 0.0),
    ]))
    parts.append(linear_gradient("titleGrad", [
        ("0%", PALETTE.cyan, 1.0), ("50%", PALETTE.green, 1.0), ("100%", PALETTE.purple, 1.0),
    ]))
    parts.append(glow_filter("softGlow", 4.5))
    parts.append("</defs>")

    parts.append(base_style())

    # Background
    parts.append(f'<rect width="{w}" height="{h}" rx="18" fill="{PALETTE.bg}"/>')
    parts.append(f'<rect width="{w}" height="{h}" rx="18" fill="url(#bgGlow)"/>')
    parts.append(
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" '
        f'fill="none" stroke="{PALETTE.border}"/>'
    )

    parts.append(_particles(26, w, h))

    # Animated gradient sweep behind title (moves the gradient stops)
    parts.append(f"""
    <animate xlink:href="#titleGrad" attributeName="x1" values="0%;100%;0%" dur="6s" repeatCount="indefinite"/>
    <animate xlink:href="#titleGrad" attributeName="x2" values="100%;200%;100%" dur="6s" repeatCount="indefinite"/>
    """)

    greeting_y = cy - 34
    name_y = cy + 10

    parts.append(
        f'<text x="{cx}" y="{greeting_y}" text-anchor="middle" font-size="15" '
        f'fill="{PALETTE.text_dim}" letter-spacing="3" opacity="0">'
        f'HELLO, WORLD — I AM'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="0.1s" fill="freeze"/>'
        f"</text>"
    )

    parts.append(
        f'<text x="{cx}" y="{name_y}" text-anchor="middle" font-size="42" font-weight="700" '
        f'fill="url(#titleGrad)" filter="url(#softGlow)" opacity="0">{esc(NAME)}'
        f'<animate attributeName="opacity" from="0" to="1" dur="1s" begin="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0,10;0,0" dur="1s" begin="0.35s" fill="freeze"/>'
        f"</text>"
    )

    parts.append(_typed_subtitle(SUBTITLE, cx - 232, name_y + 46, start=1.5))

    # Thin animated underline
    parts.append(
        f'<rect x="{cx - 60}" y="{name_y + 62}" width="120" height="2" rx="1" fill="url(#titleGrad)" opacity="0.85">'
        f'<animate attributeName="width" values="0;120" dur="0.8s" begin="1.3s" fill="freeze"/>'
        f'<animate attributeName="x" values="{cx};{cx - 60}" dur="0.8s" begin="1.3s" fill="freeze"/>'
        f"</rect>"
    )

    parts.append(svg_close())
    return "\n".join(parts)


def main() -> None:
    svg = build()
    out_path = ASSETS_DIR / "header.svg"
    out_path.write_text(svg, encoding="utf-8")
    print(f"[header] wrote {out_path}")


if __name__ == "__main__":
    main()
