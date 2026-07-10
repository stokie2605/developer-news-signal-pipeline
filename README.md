# Developer News Signal Pipeline
> **The 1-Line Mission:** An educational data ingestion pipeline that queries the official public Hacker News API, scores relevance using custom heuristics, and stores lightweight local metadata snapshots.

### Engineering Breakdown
* **The Problem:** Raw technology news feeds contain high volumes of noise, making it resource-intensive to parse and query targeted developer insights.
* **The Solution:** A Python ingestion engine that cleanly polls the official public Hacker News Firebase API, normalizes schemas, and commits lightweight metadata records into a locally indexed SQLite database.
* **The Tech Stack:** `Python` `SQLite` `Pytest` `GitHub Actions`
