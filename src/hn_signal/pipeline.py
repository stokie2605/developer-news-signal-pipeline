from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hn_signal.client import HackerNewsClient, fetch_items
from hn_signal.models import NormalizedStory, story_from_hn_item, utc_now_iso
from hn_signal.scoring import score_story
from hn_signal.storage import connect, export_json, top_stored_stories, upsert_stories


@dataclass(frozen=True)
class PipelineResult:
    fetched_items: int
    normalized_stories: int
    stored_stories: int
    captured_at: str
    top_story: NormalizedStory | None
    stories: list[NormalizedStory]


def normalize_items(items: list[dict[str, object]]) -> list[NormalizedStory]:
    stories = []
    for item in items:
        raw_story = story_from_hn_item(item)
        if raw_story is not None:
            stories.append(score_story(raw_story))
    return sorted(stories, key=lambda story: story.signal_score, reverse=True)


def run_pipeline(
    *,
    limit: int,
    db_path: Path,
    json_path: Path | None = None,
    client: HackerNewsClient | None = None,
) -> PipelineResult:
    if limit <= 0:
        raise ValueError("limit must be greater than zero")

    hn_client = client or HackerNewsClient()
    item_ids = hn_client.top_story_ids(limit)
    items = fetch_items(hn_client, item_ids)
    stories = normalize_items(items)
    captured_at = utc_now_iso()

    with connect(db_path) as connection:
        upsert_stories(connection, stories, captured_at)
        stored = len(top_stored_stories(connection, limit=limit))

    if json_path is not None:
        export_json(json_path, stories)

    return PipelineResult(
        fetched_items=len(items),
        normalized_stories=len(stories),
        stored_stories=stored,
        captured_at=captured_at,
        top_story=stories[0] if stories else None,
        stories=stories,
    )

