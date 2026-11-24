"""Entry for make.fun news-image-20261124.

Writes the bundled front-page image (entry.png, JPEG bytes) to the
grader's output directory as /output/entry.png. Standard library only.
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
