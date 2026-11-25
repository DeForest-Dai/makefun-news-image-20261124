"""Entry for make.fun news-image-20261124 (v2).

Writes the bundled one-page infographic (entry.png, JPEG bytes) to the
grader's output directory as /output/entry.png. Standard library only.

v2: a dense "world in one day" page, 29 stories, every one dated Tuesday
24 November 2026. The image was drawn by draw_v2.py (PIL, vector-style
art, exact text) and bundled here; this program only copies it verbatim,
so two runs write identical bytes. See draw_v2.py for how the page was
built, and the DATE CHECK strip at its foot for what was left out and why.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"


def output_dir() -> Path:
    # Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output.
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    if not IMAGE.is_file():
        raise SystemExit(f"missing image: {IMAGE}")
    target = output_dir() / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(IMAGE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
