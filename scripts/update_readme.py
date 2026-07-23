"""
update_readme.py
=================
Regenerates README.md from the data in config.py plus the SVG assets
already sitting in /assets. Run after generate_svgs.py:

    python scripts/generate_svgs.py
    python scripts/update_readme.py

This is also what the GitHub Actions workflow runs every 24 hours.
"""

from __future__ import annotations

import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (  # noqa: E402
    README_PATH, GITHUB_USERNAME, NAME, ROLE, SUBTITLE, EDUCATION, CGPA,
    LOCATION, CURRENT_FOCUS, TECH_STACK, SHIELD_LOGOS, BADGE_COLORS,
    ACHIEVEMENTS, CURRENTLY_LEARNING, SOCIAL_LINKS, PALETTE,
)


def badge(label: str, value: str, color: str, logo: str | None = None) -> str:
    label_q = urllib.parse.quote(label)
    value_q = urllib.parse.quote(value)
    url = f"https://img.shields.io/badge/{label_q}-{value_q}-{color}?style=for-the-badge"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return f"![{label}]({url})"


def tech_badges_section() -> str:
    lines = []
    for category, items in TECH_STACK.items():
        color = BADGE_COLORS.get(category, "39d0ff")
        badges = []
        for item in items:
            display = item.replace("%20", " ").replace("--", "-")
            logo = SHIELD_LOGOS.get(item)
            logo_part = f"&logo={logo}&logoColor=white" if logo else ""
            url = f"https://img.shields.io/badge/{urllib.parse.quote(display)}-{color}?style=for-the-badge{logo_part}"
            badges.append(f"![{display}]({url})")
        lines.append(f"**{category}**\n\n{' '.join(badges)}\n")
    return "\n".join(lines)


def stats_section() -> str:
    u = GITHUB_USERNAME
    return f"""
<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=39d0ff&icon_color=3ddc84&text_color=e6edf3" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username={u}&layout=compact&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=39d0ff&text_color=e6edf3" />
</p>

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user={u}&theme=tokyonight&hide_border=true&background=0d1117&stroke=1f2937&ring=39d0ff&fire=ff9f43&currStreakLabel=39d0ff" />
</p>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username={u}&theme=tokyo-night&hide_border=true&bg_color=0d1117&color=39d0ff&line=3ddc84&point=ffffff" width="100%"/>
</p>
""".strip()


def connect_section() -> str:
    badge_specs = [
        ("GitHub", SOCIAL_LINKS["GitHub"], "181717", "github"),
        ("LinkedIn", SOCIAL_LINKS["LinkedIn"], "0A66C2", "linkedin"),
        ("Gmail", SOCIAL_LINKS["Email"], "D14836", "gmail"),
    ]
    anchors = []
    for label, url, color, logo in badge_specs:
        badge_url = (
            f"https://img.shields.io/badge/{urllib.parse.quote(label)}-{color}"
            f"?style=for-the-badge&logo={logo}&logoColor=white"
        )
        anchors.append(
            f'  <a href="{url}"><img src="{badge_url}" alt="{label}"/></a>'
        )
    return "\n".join(anchors)


def build_readme() -> str:
    tech_badges = tech_badges_section()
    stats = stats_section()
    connect = connect_section()
    learning = " · ".join(CURRENTLY_LEARNING)
    achievements = "\n".join(f"- 🏆 {a}" for a in ACHIEVEMENTS)

    return f"""<div align="center">

<img src="assets/header.svg" alt="{NAME} header" width="100%"/>

</div>

## About Me

I'm **{NAME}**, an **{ROLE}** with a strong interest in AI, Machine
Learning, and building software that solves real-world problems. I enjoy
working across the stack — from training models to shipping full
production apps — and I'm always picking up new tools and techniques
along the way. Currently open to **AI/ML** and **Software Engineering**
opportunities.

- 🔭 Currently focused on: **{CURRENT_FOCUS}**
- 🌱 Currently learning: **{learning}**
- 📍 Based in **{LOCATION}**
- 💬 Ask me about: Deep Learning, NLP, Full-Stack Development

<div align="center">

<table>
<tr>
<td width="50%"><img src="assets/terminal-card.svg" alt="terminal card" width="100%"/></td>
<td width="50%"><img src="assets/info-card.svg" alt="info card" width="100%"/></td>
</tr>
</table>

</div>

## Contribution Activity

<div align="center">
<img src="assets/github-contribution-animation.svg" alt="animated contribution calendar" width="100%"/>
</div>

## GitHub Stats

{stats}

## Tech Stack

{tech_badges}

## Achievements

{achievements}

## Currently Learning

{" · ".join(f"`{l}`" for l in CURRENTLY_LEARNING)}

## Connect With Me

<p align="center">
{connect}
</p>

<div align="center">

<sub>Built with Python • SVG + SMIL • Updated automatically using GitHub Actions</sub>

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python%20%2B%20SVG-39d0ff?style=for-the-badge&logo=python&logoColor=white"/>
</p>
"""


def main() -> None:
    content = build_readme()
    README_PATH.write_text(content, encoding="utf-8")
    print(f"[readme] wrote {README_PATH} ({len(content)} chars)")


if __name__ == "__main__":
    main()
