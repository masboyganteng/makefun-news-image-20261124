"""make.fun news-image-20261124 entry: hand over the drawn front page.

The page itself lives in this folder as entry.png — a one-page newspaper
front, "The World in One Day", for Tuesday 24 November 2026, drawn by
draw_entry.py with Pillow. This script only places that file where the
grader expects it.

Pure standard library, no network, and fully repeatable: every run copies
the same bytes to the same name.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "entry.png")


def main():
    # The grader sets MAKEFUN_OUTPUT_DIR; local runs fall back to /output.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(PAGE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
