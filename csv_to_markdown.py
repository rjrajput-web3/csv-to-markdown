#!/usr/bin/env python3
"""Convert CSV into a GitHub-flavoured Markdown table.

Reads a CSV file (or stdin) and prints a Markdown table. Pipe characters
inside cells are escaped, surrounding whitespace is stripped, and long
cells can be truncated with --max-col-width.

Usage:
    python csv_to_markdown.py data.csv
    cat data.csv | python csv_to_markdown.py
    python csv_to_markdown.py data.csv --align center --max-col-width 30

Exit codes: 0 ok, 1 malformed CSV or missing file, 2 empty input or bad argument.
"""

import argparse
import csv
import sys

ALIGNMENTS = ("left", "center", "right")
SEPARATORS = {"left": ":---", "center": ":---:", "right": "---:"}


def escape_cell(value):
    """Escape pipes and newlines so a cell cannot break the table."""
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def truncate(value, width):
    if width is not None and len(value) > width:
        return value[: max(width - 1, 0)] + "…"
    return value


def build_table(rows, align, max_col_width):
    header = [truncate(escape_cell(c), max_col_width) for c in rows[0]]
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join(SEPARATORS[align] for _ in header) + " |")
    for row in rows[1:]:
        cells = row + [""] * (len(header) - len(row))  # pad short rows
        cells = [truncate(escape_cell(c), max_col_width) for c in cells[: len(header)]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert CSV into a GitHub-flavoured Markdown table."
    )
    parser.add_argument("file", nargs="?", help="CSV file to read (default: stdin)")
    parser.add_argument(
        "--align",
        choices=ALIGNMENTS,
        default="left",
        help="column alignment (default: left)",
    )
    parser.add_argument(
        "--max-col-width",
        type=int,
        default=None,
        metavar="N",
        help="truncate cells longer than N characters",
    )
    args = parser.parse_args(argv)

    if args.max_col_width is not None and args.max_col_width < 2:
        parser.error("--max-col-width must be at least 2")

    try:
        if args.file:
            handle = open(args.file, newline="", encoding="utf-8")
        else:
            handle = sys.stdin
        with handle:
            rows = [row for row in csv.reader(handle) if row]
    except FileNotFoundError:
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return 1
    except csv.Error as exc:
        print(f"error: malformed CSV: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print("error: empty input — no CSV rows found", file=sys.stderr)
        return 2

    print(build_table(rows, args.align, args.max_col_width))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
