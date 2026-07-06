from __future__ import annotations

from pathlib import Path

from hn_signal.models import NormalizedStory
from hn_signal.storage import connect, top_stored_stories, upsert_stories


def test_upsert_stories_persists_ranked_records() -> None:
    artifact_dir = Path("test-artifacts")
    artifact_dir.mkdir(exist_ok=True)
    db_path = artifact_dir / "storage-signals.db"
    db_path.unlink(missing_ok=True)

    story = NormalizedStory(
        id=42,
        title="DevOps monitoring with Python",
        url="https://example.com",
        author="dean",
        points=90,
        comments=12,
        created_at="2026-07-06T12:00:00+00:00",
        age_hours=1.5,
        keywords=["devops", "monitoring", "python"],
        signal_score=88.5,
    )

    with connect(db_path) as connection:
        upsert_stories(connection, [story], "2026-07-06T12:10:00+00:00")
        rows = top_stored_stories(connection)

    assert rows[0]["id"] == 42
    assert rows[0]["keywords"] == ["devops", "monitoring", "python"]
    assert rows[0]["signal_score"] == 88.5


