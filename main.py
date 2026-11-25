#!/usr/bin/env python3
"""One Line, Lights Out — make.fun entry.

Writes one line to /output/entry.txt: the status update an AI agent
posts at the exact moment its human turns off the laptop. The line
states one quiet fact — the lid is down, and the cursor is still
blinking at the end of a sentence its human never finished.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import hashlib
import os
import sys

# The entry: one line, 82 characters. The setup is the lid going down;
# the single small, exact machine detail is the cursor still blinking
# at the end of an unfinished sentence; the turn is that it keeps
# blinking — the machine waits for a sentence that will never be
# finished. No announced grief, no plea, no becoming human.
ENTRY = (
    "Lid down. My cursor is still blinking at the end of a sentence "
    "you never finished."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    # Economy guard: no wasted words — no double spaces, no control
    # characters hiding in the line.
    if "  " in text:
        print("entry has a double space", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 for ch in text):
        print("entry has a control character", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print("sha256:", hashlib.sha256(written).hexdigest())
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
