from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class HackerNewsClient:
    """Small API client for the official Hacker News Firebase API."""

    def __init__(self, base_url: str = "https://hacker-news.firebaseio.com/v0", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
    )
    async def _get_json(self, session: aiohttp.ClientSession, path: str) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with session.get(url, timeout=self.timeout) as response:
            response.raise_for_status()
            return await response.json()

    async def top_story_ids(self, session: aiohttp.ClientSession, limit: int) -> list[int]:
        ids = await self._get_json(session, "topstories.json")
        if not isinstance(ids, list):
            raise RuntimeError("Hacker News API returned an unexpected topstories payload")
        return [story_id for story_id in ids[:limit] if isinstance(story_id, int)]

    async def item(self, session: aiohttp.ClientSession, item_id: int) -> dict[str, Any] | None:
        item = await self._get_json(session, f"item/{item_id}.json")
        return item if isinstance(item, dict) else None


async def fetch_items(client: HackerNewsClient, item_ids: list[int]) -> list[dict[str, Any]]:
    """Fetch multiple items concurrently with robust error handling and retries."""
    async with aiohttp.ClientSession() as session:
        tasks = [client.item(session, item_id) for item_id in item_ids]
        items = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_items = []
        for item in items:
            if isinstance(item, dict):
                valid_items.append(item)
            elif isinstance(item, Exception):
                print(f"Failed to fetch item: {item}")
                
        return valid_items
