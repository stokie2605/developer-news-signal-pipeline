from __future__ import annotations

from datetime import datetime, timezone
from math import log1p

from hn_signal.models import NormalizedStory, RawStory


KEYWORD_WEIGHTS = {
    "ai": 12,
    "agent": 10,
    "automation": 10,
    "cloud": 8,
    "devops": 10,
    "docker": 8,
    "github": 8,
    "infrastructure": 9,
    "kubernetes": 9,
    "linux": 7,
    "monitoring": 8,
    "python": 8,
    "security": 10,
    "testing": 7,
}


def find_keywords(title: str) -> list[str]:
    title_lower = title.lower()
    return [keyword for keyword in KEYWORD_WEIGHTS if keyword in title_lower]


def story_age_hours(story_time: int, now: datetime | None = None) -> float:
    current = now or datetime.now(timezone.utc)
    created = datetime.fromtimestamp(story_time, tz=timezone.utc)
    return max((current - created).total_seconds() / 3600, 0.0)


def score_story(story: RawStory, now: datetime | None = None) -> NormalizedStory:
    age_hours = story_age_hours(story.time, now)
    keywords = find_keywords(story.title)
    keyword_bonus = sum(KEYWORD_WEIGHTS[keyword] for keyword in keywords)

    engagement = log1p(story.score) * 12 + log1p(story.descendants) * 8
    freshness_penalty = min(age_hours * 1.8, 36)
    signal_score = max(engagement + keyword_bonus - freshness_penalty, 0)

    created_at = datetime.fromtimestamp(story.time, tz=timezone.utc).replace(microsecond=0).isoformat()
    return NormalizedStory(
        id=story.id,
        title=story.title,
        url=story.url,
        author=story.by,
        points=story.score,
        comments=story.descendants,
        created_at=created_at,
        age_hours=round(age_hours, 2),
        keywords=keywords,
        signal_score=round(signal_score, 2),
    )
