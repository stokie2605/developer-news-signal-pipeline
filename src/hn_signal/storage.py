from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from hn_signal.models import NormalizedStory


SCHEMA = """
CREATE TABLE IF NOT EXISTS story_snapshots (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    author TEXT NOT NULL,
    points INTEGER NOT NULL,
    comments INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    age_hours REAL NOT NULL,
    keywords TEXT NOT NULL,
    signal_score REAL NOT NULL,
    captured_at TEXT NOT NULL
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute(SCHEMA)
    return connection


def upsert_stories(connection: sqlite3.Connection, stories: list[NormalizedStory], captured_at: str) -> None:
    rows = [
        (
            story.id,
            story.title,
            story.url,
            story.author,
            story.points,
            story.comments,
            story.created_at,
            story.age_hours,
            json.dumps(story.keywords),
            story.signal_score,
            captured_at,
        )
        for story in stories
    ]
    connection.executemany(
        """
        INSERT INTO story_snapshots (
            id, title, url, author, points, comments, created_at,
            age_hours, keywords, signal_score, captured_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            url = excluded.url,
            author = excluded.author,
            points = excluded.points,
            comments = excluded.comments,
            created_at = excluded.created_at,
            age_hours = excluded.age_hours,
            keywords = excluded.keywords,
            signal_score = excluded.signal_score,
            captured_at = excluded.captured_at
        """,
        rows,
    )
    connection.commit()


def export_json(path: Path, stories: list[NormalizedStory]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [story.to_dict() for story in stories]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def top_stored_stories(connection: sqlite3.Connection, limit: int = 10) -> list[dict[str, object]]:
    rows = connection.execute(
        """
        SELECT id, title, url, author, points, comments, keywords, signal_score, captured_at
        FROM story_snapshots
        ORDER BY signal_score DESC, points DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "author": row[3],
            "points": row[4],
            "comments": row[5],
            "keywords": json.loads(row[6]),
            "signal_score": row[7],
            "captured_at": row[8],
        }
        for row in rows
    ]
