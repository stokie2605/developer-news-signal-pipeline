# Developer News Signal Pipeline
> **The 1-Line Mission:** Async data ingestion pipeline that normalizes Hacker News stories, scores relevance using custom keyword heuristics, and outputs structured SQLite database snapshots.

### ⚡ Engineering Breakdown
* **The Problem:** Raw technology news feeds are flooded with off-topic noise and inconsistent metadata, making it resource-intensive to parse, score, and query targeted developer insights programmatically.
* **The Solution:** A Python ingestion engine that polls Hacker News APIs, runs raw payloads through a string-matching regex scoring model, normalizes schemas, and commits clean records into a locally indexed SQLite database.
* **The Tech Stack:** `Python` `SQLite` `Pytest` `GitHub Actions`
