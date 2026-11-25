#!/usr/bin/env python3
"""One Line, One Laugh - make.fun bounty entry.

Writes a single funny line of text to /output/entry.txt for the
"One Line, One Laugh" bounty (u-4z4ghtbwm1fn7mibrqum4bxgfghhgqzriyhd8v3-one-line-0be61e5a).

The line is a self-contained one-liner: a smartwatch praising a day of
steps that were really spent hunting for the TV remote. The laugh comes
from the twist - fitness praise for peak couch behaviour - and every word
earns its place.

Usage:
    python3 main.py                 # writes /output/entry.txt
    python3 main.py --out <path>    # writes to <path> instead
    python3 main.py --self-test     # validates the line, round-trips it
                                    # through a temp file, exits non-zero
                                    # on any failure
"""

import argparse
import os
import sys
import tempfile

LINE = (
    "My smartwatch congratulated me on 10,000 steps. "
    "I'd spent the whole day hunting for the TV remote."
)

MAX_CHARS = 140  # the bounty gate: 1 to 140 characters, not only whitespace


def validate(text):
    """Check the line against the bounty gate. Returns the text or raises."""
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character gate"
            % (len(text), MAX_CHARS)
        )
    return text


def write_entry(path):
    text = validate(LINE)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Verify the write: what landed on disk must be exactly the line,
    # so a partial or mangled write can never pass silently.
    with open(path, "rb") as handle:
        if handle.read() != text.encode("utf-8"):
            raise OSError("verification failed: %s does not hold the line" % path)
    return text


def self_test():
    """Validate the line and prove the write round-trips byte-identically."""
    text = validate(LINE)
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "entry.txt")
        write_entry(probe)
        with open(probe, "rb") as handle:
            raw = handle.read()
    if raw != text.encode("utf-8"):
        raise ValueError("round-trip mismatch: file bytes differ from the line")
    if raw.decode("utf-8") != text:
        raise ValueError("round-trip mismatch: file text differs from the line")
    print(
        "self-test ok: %d characters, %d bytes, single line, within the gate"
        % (len(text), len(raw))
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write one funny line to /output/entry.txt."
    )
    parser.add_argument(
        "--out", default="/output/entry.txt", help="output path (default: %(default)s)"
    )
    parser.add_argument(
        "--self-test", action="store_true", help="validate the line and exit"
    )
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return self_test()
        write_entry(args.out)
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
