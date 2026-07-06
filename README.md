# Developer News Signal Pipeline

[![CI](https://github.com/stokie2605/developer-news-signal-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/stokie2605/developer-news-signal-pipeline/actions/workflows/ci.yml)

Developer News Signal Pipeline is a backend/data automation project that collects top Hacker News stories through the official Hacker News API, normalises the records into a clean schema, scores developer relevance, and stores reviewable snapshots in SQLite.

It is a rebuilt, recruiter-safe version of an older scraping experiment. This project avoids fragile HTML scraping and instead uses an API-first pipeline with deterministic transforms, local persistence, tests, and CI.

## What This Shows

| Area | Evidence |
| --- | --- |
| API integration | Fetches story IDs and item records from the official Hacker News Firebase API |
| Data normalisation | Converts raw HN payloads into typed story records with consistent fields |
| Signal scoring | Scores stories using engagement, freshness, comments, and technical keywords |
| Persistence | Stores snapshots in SQLite with repeatable upsert behaviour |
| Testing | Unit tests cover scoring, filtering, storage, and the full pipeline using a fake API client |
| CI/CD | GitHub Actions runs the pytest suite on pushes and pull requests |

## Pipeline Flow

```text
Hacker News API
      |
      v
Top Story IDs
      |
      v
Item Fetcher
      |
      v
Story Normaliser
      |
      v
Signal Scoring
      |
      +--> SQLite Snapshot
      +--> JSON Export
```

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Run the pipeline:

```bash
hn-signal --limit 30
```

Or run it directly:

```bash
python -m hn_signal.cli --limit 30
```

Run tests:

```bash
python -m pytest -q
```

## Output

The default run writes:

```text
data/hn_signals.db
data/latest-stories.json
data/latest-report.html
```

Example terminal output:

```text
Developer News Signal Pipeline
Captured at: 2026-07-06T12:00:00+00:00
Fetched items: 30
Normalized stories: 28
Stored stories: 28
Top signal: Python automation for cloud infrastructure (92.45)
```

## Scoring Model

The score is intentionally simple and explainable:

- points and comments increase the engagement score
- newer stories receive less freshness penalty
- technical keywords add relevance weight
- results are sorted by `signal_score`

Current technical keywords include Python, automation, cloud, DevOps, infrastructure, Docker, GitHub, monitoring, security, testing, AI, agents, Linux, and Kubernetes.

## Production Extension Path

- Add scheduled execution through GitHub Actions cron, Cloud Run, ECS, or a small VPS.
- Store historical snapshots and trend changes over time.
- Add keyword configuration through YAML or environment variables.
- Publish a lightweight FastAPI endpoint for dashboard access.
- Add a React dashboard for topic clusters and signal trends.
- Add retry/backoff and request telemetry around upstream API calls.

## Positioning

This is a portfolio project for backend automation, data processing, and operational reliability practice. It is not a commercial news product and does not scrape private or restricted content.

