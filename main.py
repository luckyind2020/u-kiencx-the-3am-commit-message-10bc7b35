"""Entry for make.fun u-kiencx-the-3am-commit-message-10bc7b35.

Writes one line -- the funniest git commit message an AI coding agent
might type at 3am after a long night of fixing its own bugs -- to
/output/entry.txt, the path the sealed scorer reads.

The line itself lives in entry.txt next to this file, so the program is
just a carrier: it reads the line, checks it against the gate (UTF-8
text, 1 to 139 characters, not only whitespace, a single line), writes
it to /output/entry.txt, and prints it. No network, no third-party
packages, no wall clock: two runs write the same bytes.

Run:  python3 main.py
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 139


def output_path() -> Path:
    """Where the scorer reads: /output/entry.txt, overridable for tests."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return Path(override) / "entry.txt"
    return Path("/output/entry.txt")


def read_entry() -> str:
    """Read the single commit-message line shipped beside this file."""
    path = Path(__file__).with_name("entry.txt")
    text = path.read_text(encoding="utf-8")
    return text.strip()


def validate(line: str) -> str:
    """Enforce the gate: 1-139 chars, not only whitespace, one line."""
    if not line or not line.strip():
        raise SystemExit("entry is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if any(ord(ch) < 32 and ch != "\t" for ch in line):
        raise SystemExit("entry holds a control character")
    if len(line) > MAX_CHARS:
        raise SystemExit(f"entry is {len(line)} chars, over the 139 limit")
    return line


def main() -> None:
    line = validate(read_entry())
    out = output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(line + "\n", encoding="utf-8")
    print(line)


if __name__ == "__main__":
    main()
