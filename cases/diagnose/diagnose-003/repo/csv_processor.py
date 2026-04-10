"""CSV data processor — filter, paginate, and summarize."""

import csv
import sys


def read_csv(filepath: str) -> list[dict]:
    # BUG: no encoding parameter — fails on non-ASCII filenames/content
    with open(filepath) as f:
        return list(csv.DictReader(f))


def filter_rows(rows: list[dict], column: str, value: str) -> list[dict]:
    return [r for r in rows if r.get(column) == value]


def paginate(rows: list[dict], page_size: int = 10) -> list[list[dict]]:
    pages = []
    # BUG: off-by-one — range stops early, last partial page is lost
    for i in range(0, len(rows) - page_size, page_size):
        pages.append(rows[i:i + page_size])
    return pages


def write_summary(rows: list[dict], output_path: str):
    # BUG: file handle never closed
    f = open(output_path, "w")
    f.write(f"Total rows: {len(rows)}\n")
    if rows:
        f.write(f"Columns: {', '.join(rows[0].keys())}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: csv_processor.py <file.csv> [--filter col=val] [--page-size N]")
        sys.exit(1)

    filepath = sys.argv[1]
    rows = read_csv(filepath)

    filter_col = None
    filter_val = None
    page_size = 10

    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--filter" and i + 1 < len(sys.argv):
            parts = sys.argv[i + 1].split("=")
            filter_col, filter_val = parts[0], parts[1]
        elif arg == "--page-size" and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1])

    if filter_col:
        rows = filter_rows(rows, filter_col, filter_val)

    pages = paginate(rows, page_size)
    for idx, page in enumerate(pages):
        print(f"--- Page {idx + 1} ---")
        for row in page:
            print(row)


if __name__ == "__main__":
    main()
