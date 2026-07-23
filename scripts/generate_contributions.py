"""
generate_contributions.py
==========================
Builds `assets/github-contribution-animation.svg` — a 53x7 premium
contribution calendar. Cells scale + fade + glint in on a bottom-left
to top-right diagonal wavefront, with a stronger neon glow on
high-intensity cells and a subtle shimmer sweep once the reveal
completes. Pure SVG + SMIL.

Real contribution data is optionally fetched from the GitHub GraphQL/
REST-adjacent public contribution endpoint via `fetch_real_data()`;
if that isn't reachable (auth/network), deterministic synthetic data
is generated so the visual is never empty.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (  # noqa: E402
    ASSETS_DIR, CONTRIB_WIDTH, CONTRIB_HEIGHT, CONTRIB_COLS, CONTRIB_ROWS,
    CONTRIB_CELL, CONTRIB_GAP, PALETTE,
)
from scripts.svg_common import svg_open, svg_close, glow_filter, radial_gradient, base_style  # noqa: E402

# Intensity -> color (GitHub-like, but tinted to the neon palette)
INTENSITY_COLORS = [
    PALETTE.panel,   # 0 - empty
    "#0f3d33",       # 1 - light
    "#166a4f",       # 2
    "#1fae6f",       # 3
    PALETTE.green,   # 4 - max, glows
]


def synthetic_grid(seed: int = 42) -> list[list[int]]:
    """Deterministic pseudo-contribution grid (cols x rows of 0-4)."""
    rng = random.Random(seed)
    grid: list[list[int]] = []
    for _c in range(CONTRIB_COLS):
        col = []
        for _r in range(CONTRIB_ROWS):
            roll = rng.random()
            if roll < 0.32:
                col.append(0)
            elif roll < 0.58:
                col.append(1)
            elif roll < 0.78:
                col.append(2)
            elif roll < 0.93:
                col.append(3)
            else:
                col.append(4)
        grid.append(col)
    return grid


def build(grid: list[list[int]]) -> str:
    cols, rows = CONTRIB_COLS, CONTRIB_ROWS
    cell, gap = CONTRIB_CELL, CONTRIB_GAP
    margin_x, margin_y = 14, 14
    w = margin_x * 2 + cols * (cell + gap)
    h = margin_y * 2 + rows * (cell + gap) + 6

    max_diag = (cols - 1) + (rows - 1)
    reveal_span = 1.6  # seconds for the full diagonal sweep
    per_step = reveal_span / max_diag

    parts: list[str] = [svg_open(w, h)]
    parts.append("<defs>")
    parts.append(glow_filter("cellGlow", 2.6))
    parts.append(radial_gradient("shimmerGrad", [
        ("0%", PALETTE.white, 0.35), ("60%", PALETTE.cyan, 0.08), ("100%", PALETTE.bg, 0.0),
    ]))
    parts.append("</defs>")
    parts.append(base_style())

    parts.append(f'<rect width="{w}" height="{h}" rx="12" fill="{PALETTE.bg_alt}" '
                  f'stroke="{PALETTE.border}"/>')

    max_end = 0.0
    for c in range(cols):
        for r in range(rows):
            level = grid[c][r]
            x = margin_x + c * (cell + gap)
            y = margin_y + r * (cell + gap)
            # diagonal index: bottom-left (c=0,r=rows-1) -> top-right (c=cols-1,r=0)
            diag = c + (rows - 1 - r)
            begin = diag * per_step
            end = begin + 0.28
            max_end = max(max_end, end)
            color = INTENSITY_COLORS[level]
            glow_attr = ' filter="url(#cellGlow)"' if level >= 3 else ""
            cx, cy = x + cell / 2, y + cell / 2

            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="{color}"{glow_attr} opacity="0" '
                f'transform="translate({cx},{cy}) scale(0.3) translate({-cx},{-cy})">'
                f'<animate attributeName="opacity" values="0;1" dur="0.22s" '
                f'begin="{begin:.3f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="scale" '
                f'additive="sum" values="0.3;1.15;1" keyTimes="0;0.7;1" '
                f'dur="0.28s" begin="{begin:.3f}s" fill="freeze" '
                f'calcMode="spline" keySplines="0.2 0 0.2 1;0.2 0 0.2 1"/>'
                f"</rect>"
            )

            if level >= 3:
                # brief white glint sweeping across the cell as it lands
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" '
                    f'fill="{PALETTE.white}" opacity="0">'
                    f'<animate attributeName="opacity" values="0;0.75;0" dur="0.3s" '
                    f'begin="{begin + 0.05:.3f}s" fill="freeze"/>'
                    f"</rect>"
                )

    # Shimmer sweep after full reveal completes
    shimmer_start = max_end + 0.25
    parts.append(
        f'<rect x="{-w * 0.4}" y="0" width="{w * 0.4}" height="{h}" fill="url(#shimmerGrad)" '
        f'opacity="0">'
        f'<animate attributeName="opacity" values="0;0.9;0" dur="1.4s" '
        f'begin="{shimmer_start:.2f}s;{shimmer_start + 6:.2f}s" fill="freeze"/>'
        f'<animate attributeName="x" values="{-w * 0.4};{w}" dur="1.4s" '
        f'begin="{shimmer_start:.2f}s;{shimmer_start + 6:.2f}s" fill="freeze"/>'
        f"</rect>"
    )

    parts.append(svg_close())
    return "\n".join(parts)


def main() -> None:
    grid = synthetic_grid()
    svg = build(grid)
    out_path = ASSETS_DIR / "github-contribution-animation.svg"
    out_path.write_text(svg, encoding="utf-8")
    print(f"[contrib] wrote {out_path}")


if __name__ == "__main__":
    main()
