from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class RawStory:
    id: int
    title: str
    url: str | None
    by: str
    score: int
    descendants: int
    time: int
    type: str


@dataclass(frozen=True)
class NormalizedStory:
    id: int
    title: str
    url: str | None
    author: str
    points: int
    comments: int
    created_at: str
    age_hours: float
    keywords: list[str]
    signal_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def story_from_hn_item(item: dict[str, Any]) -> RawStory | None:
    if item.get("type") != "story":
        return None

    title = item.get("title")
    story_id = item.get("id")
    if not isinstance(title, str) or not isinstance(story_id, int):
        return None

    return RawStory(
        id=story_id,
        title=title,
        url=item.get("url") if isinstance(item.get("url"), str) else None,
        by=item.get("by") if isinstance(item.get("by"), str) else "unknown",
        score=item.get("score") if isinstance(item.get("score"), int) else 0,
        descendants=item.get("descendants") if isinstance(item.get("descendants"), int) else 0,
        time=item.get("time") if isinstance(item.get("time"), int) else 0,
        type="story",
    )


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
