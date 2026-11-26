"""Copy the pre-rendered entry image to the output directory.

Stdlib only: no network, no clock, no randomness. The image is rendered
locally by the builder (render_draft.py, PIL) and committed as entry.png;
this program only copies it, as the competition rules explicitly allow
("the simplest program copies an image the repository holds").
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(OUT_DIR, "entry.png"),
    )


if __name__ == "__main__":
    main()
