from __future__ import annotations

import argparse
from pathlib import Path

from hn_signal.pipeline import run_pipeline
from hn_signal.report import render_html_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect Hacker News top stories, score developer signals, and store a SQLite snapshot.",
    )
    parser.add_argument("--limit", type=int, default=30, help="Number of top story IDs to inspect.")
    parser.add_argument("--db", type=Path, default=Path("data/hn_signals.db"), help="SQLite database path.")
    parser.add_argument(
        "--json",
        type=Path,
        default=Path("data/latest-stories.json"),
        help="Optional JSON export path.",
    )
    parser.add_argument(
        "--html",
        type=Path,
        default=Path("data/latest-report.html"),
        help="Optional static HTML report path.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_pipeline(limit=args.limit, db_path=args.db, json_path=args.json)

    print("Developer News Signal Pipeline")
    print(f"Captured at: {result.captured_at}")
    print(f"Fetched items: {result.fetched_items}")
    print(f"Normalized stories: {result.normalized_stories}")
    print(f"Stored stories: {result.stored_stories}")
    if result.top_story:
        print(f"Top signal: {result.top_story.title} ({result.top_story.signal_score})")

    if args.html:
        render_html_report(result.stories, args.html)
        print(f"HTML report: {args.html}")


if __name__ == "__main__":
    main()


