from __future__ import annotations

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


class HackerNewsClient:
    """Small API client for the official Hacker News Firebase API."""

    def __init__(self, base_url: str = "https://hacker-news.firebaseio.com/v0", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get_json(self, path: str) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            with urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f"Hacker News API request failed for {path}: {exc}") from exc

    def top_story_ids(self, limit: int) -> list[int]:
        ids = self._get_json("topstories.json")
        if not isinstance(ids, list):
            raise RuntimeError("Hacker News API returned an unexpected topstories payload")
        return [story_id for story_id in ids[:limit] if isinstance(story_id, int)]

    def item(self, item_id: int) -> dict[str, Any] | None:
        item = self._get_json(f"item/{item_id}.json")
        return item if isinstance(item, dict) else None


def fetch_items(client: HackerNewsClient, item_ids: list[int], pause_seconds: float = 0.0) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for index, item_id in enumerate(item_ids):
        item = client.item(item_id)
        if item is not None:
            items.append(item)
        if pause_seconds > 0 and index < len(item_ids) - 1:
            time.sleep(pause_seconds)
    return items
