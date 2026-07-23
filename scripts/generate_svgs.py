"""
generate_svgs.py
=================
Entry point that regenerates every SVG asset for the profile:

    python scripts/generate_svgs.py

Runs each specialised generator in sequence and reports a summary.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import (  # noqa: E402
    generate_header,
    generate_terminal,
    generate_info_card,
    generate_contributions,
)


def main() -> None:
    start = time.time()
    steps = [
        ("Header banner", generate_header.main),
        ("Terminal card", generate_terminal.main),
        ("Info card", generate_info_card.main),
        ("Contribution animation", generate_contributions.main),
    ]

    print("Generating all SVG assets for the GitHub profile…\n")
    for label, fn in steps:
        print(f"→ {label}")
        fn()

    elapsed = time.time() - start
    print(f"\nDone. All assets written to /assets in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
