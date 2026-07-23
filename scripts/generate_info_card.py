"""
generate_info_card.py
======================
Builds `assets/info-card.svg` — a neofetch-inspired information panel
listing About / Education / Focus / Tech Stack / Projects / Achievements
/ Languages. Every row slides up + fades in with a 0.06s stagger and a
terminal-style "printing" caret, all via pure SMIL.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (  # noqa: E402
    ASSETS_DIR, INFO_CARD_WIDTH, INFO_CARD_HEIGHT, PALETTE, ACCENTS,
    NAME, ROLE, EDUCATION, CGPA, LOCATION, CURRENT_FOCUS, TECH_STACK,
    PROJECTS, ACHIEVEMENTS,
)
from scripts.svg_common import (  # noqa: E402
    svg_open, svg_close, glow_filter, mac_dots, glass_panel, base_style, esc,
)

STAGGER = 0.06
ROW_START = 0.35


def _rows() -> list[tuple[str, object]]:
    langs = ", ".join(TECH_STACK["Programming Languages"])
    frameworks = ", ".join(TECH_STACK["Frameworks"][:4]) + " …"
    ai_ml = ", ".join(t.replace("%20", " ").replace("--", "-") for t in TECH_STACK["AI / Machine Learning"][:4]) + " …"
    dbs = ", ".join(TECH_STACK["Databases"])
    tools = ", ".join(t.replace("%20", " ") for t in TECH_STACK["Developer Tools"][:4]) + " …"

    # Split project names across two short bulleted lines so nothing
    # gets truncated or overflows the card width.
    project_names = [p.name for p in PROJECTS]
    half = (len(project_names) + 1) // 2
    projects_lines = [
        " • ".join(project_names[:half]),
        " • ".join(project_names[half:]),
    ]

    return [
        ("about", "AI/ML Engineer passionate about building intelligent, real-world software solutions."),
        ("education", EDUCATION),
        ("cgpa", CGPA),
        ("location", LOCATION),
        ("focus", CURRENT_FOCUS),
        ("languages", langs),
        ("frameworks", frameworks),
        ("ai_ml", ai_ml),
        ("databases", dbs),
        ("tools", tools),
        ("projects", projects_lines),
        ("achievements", "; ".join(ACHIEVEMENTS)),
    ]


def build() -> str:
    w, h = INFO_CARD_WIDTH, INFO_CARD_HEIGHT
    parts: list[str] = [svg_open(w, h)]
    parts.append("<defs>")
    parts.append(glow_filter("infoGlow", 2.4))
    parts.append("</defs>")
    parts.append(base_style())

    parts.append(f'<rect width="{w}" height="{h}" rx="14" fill="{PALETTE.bg_alt}" '
                  f'stroke="{PALETTE.border}"/>')
    parts.append(f'<rect width="{w}" height="34" rx="14" fill="{PALETTE.panel}"/>')
    parts.append(f'<rect y="20" width="{w}" height="14" fill="{PALETTE.panel}"/>')
    parts.append(mac_dots(24, 17))
    parts.append(f'<text x="{w/2}" y="21" text-anchor="middle" font-size="11" class="dim">'
                  f'neofetch — {esc(NAME)}</text>')

    parts.append(glass_panel(10, 44, w - 20, h - 56, rx=10, opacity=0.35))

    # Avatar-style ASCII glyph block on the left (decorative, static)
    glyph_x, glyph_y = 34, 70
    glyph_lines = [
        "   ╭──────╮",
        "   │ 26   │",
        "   │ yashu│",
        "   ╰──────╯",
    ]
    for i, gl in enumerate(glyph_lines):
        parts.append(
            f'<text x="{glyph_x}" y="{glyph_y + i * 13}" font-size="10.5" '
            f'fill="{ACCENTS[i % len(ACCENTS)]}" opacity="0.9">{esc(gl)}</text>'
        )
    parts.append(f'<text x="{glyph_x}" y="{glyph_y + len(glyph_lines) * 13 + 14}" '
                  f'font-size="9.5" class="dim">{esc(ROLE)}</text>')

    parts.append(f'<line x1="10" y1="{glyph_y + 62}" x2="{w - 10}" y2="{glyph_y + 62}" '
                  f'stroke="{PALETTE.border}"/>')

    rows = _rows()
    row_y0 = glyph_y + 84
    row_h = (h - 56 - (row_y0 - 44) - 12) / len(rows)
    row_h = max(row_h, 20)

    label_x = 34
    value_x = 168
    avail_px = w - value_x - 18  # usable width for the value column

    def fit_font(text: str, default_size: float = 10.0, floor: float = 6.8) -> tuple[float, str]:
        """Shrink font size (never truncate) so `text` fits in one line
        within avail_px; only truncate as a last resort at the floor size."""
        needed = default_size
        if text:
            needed = min(default_size, avail_px / (0.56 * len(text)))
        if needed >= floor:
            return round(needed, 2), text
        max_chars = max(1, int(avail_px / (0.56 * floor)))
        return floor, (text[:max_chars - 1] + "…" if len(text) > max_chars else text)

    for i, (label, value) in enumerate(rows):
        y = row_y0 + i * row_h
        begin = ROW_START + i * STAGGER
        color = ACCENTS[i % len(ACCENTS)]
        group_transform_from = "0,10"

        parts.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" '
            f'begin="{begin:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="{group_transform_from};0,0" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/>'
            f'<text x="{label_x}" y="{y:.1f}" font-size="10.5" fill="{color}" font-weight="700">'
            f'{esc(label)}</text>'
        )

        if label == "projects":
            # Two short bulleted lines instead of one truncated line.
            line1, line2 = value
            parts.append(
                f'<text x="{value_x}" y="{y:.1f}" font-size="10" class="bright">{esc(line1)}</text>'
                f'<text x="{value_x}" y="{y + 13:.1f}" font-size="10" class="bright">{esc(line2)}</text>'
            )
        elif label == "about":
            font_size, value_disp = fit_font(value, default_size=10.0, floor=6.8)
            parts.append(
                f'<text x="{value_x}" y="{y:.1f}" font-size="{font_size}" class="bright">'
                f'{esc(value_disp)}</text>'
            )
        else:
            value_disp = value if len(value) <= 54 else value[:51] + "..."
            parts.append(
                f'<text x="{value_x}" y="{y:.1f}" font-size="10" class="bright">{esc(value_disp)}</text>'
            )

        parts.append("</g>")

    total_end = ROW_START + len(rows) * STAGGER + 0.4
    # Trailing blinking caret under the last row
    caret_y = row_y0 + len(rows) * row_h
    parts.append(
        f'<rect x="{label_x}" y="{caret_y - 9:.1f}" width="6" height="10" fill="{PALETTE.green}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{total_end:.2f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" begin="{total_end + 0.2:.2f}s" '
        f'repeatCount="indefinite"/>'
        f"</rect>"
    )

    parts.append(svg_close())
    return "\n".join(parts)


def main() -> None:
    svg = build()
    out_path = ASSETS_DIR / "info-card.svg"
    out_path.write_text(svg, encoding="utf-8")
    print(f"[info-card] wrote {out_path}")


if __name__ == "__main__":
    main()
