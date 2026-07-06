from __future__ import annotations

from pathlib import Path

from hn_signal.pipeline import normalize_items, run_pipeline


class FakeClient:
    def top_story_ids(self, limit: int) -> list[int]:
        return [101, 102, 103][:limit]

    def item(self, item_id: int) -> dict[str, object] | None:
        items = {
            101: {
                "id": 101,
                "type": "story",
                "title": "Show HN: Cloud monitoring dashboard",
                "url": "https://example.com/cloud",
                "by": "alice",
                "score": 190,
                "descendants": 55,
                "time": 1_783_338_000,
            },
            102: {
                "id": 102,
                "type": "story",
                "title": "Python testing patterns for backend teams",
                "url": "https://example.com/python",
                "by": "bob",
                "score": 150,
                "descendants": 20,
                "time": 1_783_338_100,
            },
            103: {
                "id": 103,
                "type": "job",
                "title": "Hiring now",
                "time": 1_783_338_200,
            },
        }
        return items[item_id]


def test_normalize_items_filters_non_story_records() -> None:
    stories = normalize_items(
        [
            {"id": 1, "type": "story", "title": "AI infrastructure", "score": 10, "descendants": 2, "time": 1},
            {"id": 2, "type": "comment", "text": "not a story"},
        ],
    )

    assert len(stories) == 1
    assert stories[0].title == "AI infrastructure"


def test_run_pipeline_stores_sqlite_and_exports_json() -> None:
    artifact_dir = Path("test-artifacts")
    artifact_dir.mkdir(exist_ok=True)
    db_path = artifact_dir / "pipeline-signals.db"
    json_path = artifact_dir / "pipeline-latest.json"
    db_path.unlink(missing_ok=True)
    json_path.unlink(missing_ok=True)

    result = run_pipeline(limit=3, db_path=db_path, json_path=json_path, client=FakeClient())  # type: ignore[arg-type]

    assert result.fetched_items == 3
    assert result.normalized_stories == 2
    assert result.stored_stories == 2
    assert result.top_story is not None
    assert db_path.exists()
    assert json_path.exists()


