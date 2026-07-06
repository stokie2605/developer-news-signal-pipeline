from __future__ import annotations

from datetime import datetime, timezone

from hn_signal.models import RawStory
from hn_signal.scoring import find_keywords, score_story


def test_find_keywords_matches_technical_terms() -> None:
    keywords = find_keywords("Python automation pipeline for cloud monitoring")

    assert keywords == ["automation", "cloud", "monitoring", "python"]


def test_score_story_rewards_engagement_and_keywords() -> None:
    now = datetime(2026, 7, 6, 12, 0, tzinfo=timezone.utc)
    story = RawStory(
        id=1,
        title="Python automation for cloud infrastructure",
        url="https://example.com",
        by="dean",
        score=250,
        descendants=80,
        time=1_783_338_000,
        type="story",
    )

    scored = score_story(story, now=now)

    assert scored.id == 1
    assert scored.author == "dean"
    assert "python" in scored.keywords
    assert "automation" in scored.keywords
    assert scored.signal_score > 60
