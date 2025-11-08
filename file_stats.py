#!/usr/bin/env python3

from __future__ import annotations

"""CLI utilities to compute basic statistics for a text file."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

CHUNK_SIZE = 64 * 1024  # balance IO and memory usage


@dataclass
class FileStats:
    """Aggregated counters describing a text file."""

    characters: int = 0
    lines: int = 0
    spaces: int = 0
    tabs: int = 0
    words: int = 0
    special: int = 0


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Print the number of characters, lines, spaces, tabs, words, "
            "and special characters in a file."
        )
    )
    parser.add_argument("path", type=Path, help="Path to the file to analyze")
    return parser.parse_args()


def _update_stats(stats: FileStats, ch: str, *, state: dict[str, bool]) -> None:
    """Update counters for a single code point."""

    if ch == " ":
        stats.spaces += 1
    elif ch == "\t":
        stats.tabs += 1

    if ch == "\r":
        stats.lines += 1
        state["pending_cr"] = True
    elif ch == "\n":
        if state["pending_cr"]:
            state["pending_cr"] = False
        else:
            stats.lines += 1
    else:
        state["pending_cr"] = False

    if ch.isspace():
        state["in_word"] = False
        return

    if ch.isalnum():
        if not state["in_word"]:
            stats.words += 1
            state["in_word"] = True
        return

    state["in_word"] = False
    stats.special += 1


def compute_file_stats(stream: TextIO) -> FileStats:
    """Compute statistics for the provided text stream."""

    stats = FileStats()
    state = {"in_word": False, "pending_cr": False}
    last_char = ""

    while True:
        chunk = stream.read(CHUNK_SIZE)
        if not chunk:
            break
        stats.characters += len(chunk)
        for ch in chunk:
            last_char = ch
            _update_stats(stats, ch, state=state)

    if stats.characters and last_char not in ("\n", "\r"):
        stats.lines += 1

    return stats


def main() -> int:
    """Entrypoint for the CLI."""

    args = parse_args()
    file_path: Path = args.path

    if not file_path.is_file():
        print(f"error: {file_path} is not a readable file", file=sys.stderr)
        return 1

    try:
        with file_path.open(encoding="utf-8") as stream:
            stats = compute_file_stats(stream)
    except OSError as exc:
        print(f"error: failed to read {file_path}: {exc}", file=sys.stderr)
        return 1

    print(f"Characters: {stats.characters}")
    print(f"Lines: {stats.lines}")
    print(f"Spaces: {stats.spaces}")
    print(f"Tabs: {stats.tabs}")
    print(f"Words: {stats.words}")
    print(f"Special characters: {stats.special}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
