#!/usr/bin/env python3
"""Entry for make.fun competition make-the-ai-judge-feel-curious-20261122-2311.

Writes a single curiosity text (1-280 Unicode code points) to entry.txt in
the output directory. Pure standard library, deterministic, no network.

Why this text: a concrete scene (museum, guard, painted door) with a quiet,
slow mystery that grows one step a day, in plain words with a lingering image
— no stock wellness phrasing, no instruction telling the reader what to feel.
"""

import hashlib
import os

TEXT = (
    "In the museum's smallest room hangs a painting of a door. "
    "Every morning the guard finds it open a little wider, and the "
    "painted hallway one step longer."
)

FILENAME = "entry.txt"


def write_and_verify(text: str, out_dir: str) -> tuple[str, str]:
    """Write text to entry.txt in out_dir, then re-read and verify it.

    Returns (path, sha256 hex digest) of the written file.
    """
    data = text.encode("utf-8")
    data.decode("utf-8")  # validate UTF-8 round-trip

    path = os.path.join(out_dir, FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    with open(path, "rb") as f:
        written = f.read()
    digest = hashlib.sha256(data).hexdigest()
    assert written == data, "entry.txt bytes differ from intended text"
    assert hashlib.sha256(written).hexdigest() == digest, "sha256 mismatch"
    return path, digest


def main() -> None:
    text = TEXT
    count = len(text)
    assert 1 <= count <= 280, f"text length {count} out of range 1-280"
    assert text.strip(), "text must not be only whitespace"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        out_dir = "."
    path, digest = write_and_verify(text, out_dir)

    print(f"chars: {count}")
    print(f"sha256: {digest}")
    print(f"wrote: {path}")
    print("verified: entry.txt bytes match the text exactly")


if __name__ == "__main__":
    main()
