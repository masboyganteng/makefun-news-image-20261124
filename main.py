"""Publish the finished broadsheet image for the make.fun harness.

The image itself is built by draw_entry.py and stored next to this file as
entry.png. All this entrypoint does is place an exact copy of those bytes
into the directory the harness names, after proving the bytes really are a
PNG. Nothing is re-encoded or resized here, so what the judges receive is
byte for byte the picture the builder drew.
"""

import os
from pathlib import Path

# The first eight bytes every PNG file starts with. If the file on disk does
# not open with them, something replaced it and we refuse to ship it.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

SOURCE_NAME = "entry.png"


def publish() -> Path:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    raw = source.read_bytes()
    if raw[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise SystemExit(f"{source} is not a PNG file, refusing to publish it")
    target_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE_NAME
    target.write_bytes(raw)
    return target


def main() -> None:
    placed = publish()
    print(f"published {placed} ({placed.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
