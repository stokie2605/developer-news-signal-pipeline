# Developer News Signal Pipeline

[![CI](https://github.com/stokie2605/developer-news-signal-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/stokie2605/developer-news-signal-pipeline/actions/workflows/ci.yml)

Backend data pipeline that collects developer news from the official Hacker News API, normalises raw item payloads, scores technical relevance, and stores reviewable SQLite, JSON, and HTML snapshots.

This is a recruiter-safe rebuild of an older scraping experiment. It avoids fragile HTML scraping and instead demonstrates an API-first workflow with typed models, deterministic transforms, local persistence, automated tests, and GitHub Actions CI.

## Project Snapshot

| Capability | Implementation |
| --- | --- |
| Source integration | Official Hacker News Firebase API |
| Processing style | Fetch, normalise, score, persist, report |
| Storage | SQLite snapshot with repeatable upsert behaviour |
| Exports | JSON file and static HTML report |
| Verification | Pytest suite and GitHub Actions workflow |
| Positioning | Backend automation, data processing, and CI/CD practice |

## What This Demonstrates

| Area | Evidence |
| --- | --- |
| API integration | Fetches story IDs and item records from the official Hacker News Firebase API |
| Data normalisation | Converts raw HN payloads into typed story records with consistent fields |
| Signal scoring | Scores stories using engagement, freshness, comments, and technical keywords |
| Persistence | Stores snapshots in SQLite with repeatable upsert behaviour |
| Testing | Unit tests cover scoring, filtering, storage, and the full pipeline using a fake API client |
| CI/CD | GitHub Actions runs the pytest suite on pushes and pull requests |

## Architecture

The pipeline is intentionally small, testable, and easy to reason about:

```text
src/hn_signal/client.py    -> HN API client
src/hn_signal/models.py    -> typed dataclasses
src/hn_signal/scoring.py   -> keyword and engagement scoring
src/hn_signal/storage.py   -> SQLite persistence
src/hn_signal/pipeline.py  -> orchestration
src/hn_signal/report.py    -> static HTML report rendering
src/hn_signal/cli.py       -> command-line interface
```

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
      +--> HTML Report
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

Or run it directly from the source layout:

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
HTML report: data/latest-report.html
```

The generated HTML report is static and self-contained, making it easy to inspect the latest ranked snapshot locally without running a web server.

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

## Why This Project Exists

This project shows the kind of backend work that sits behind operational dashboards and automation tools: collecting external data, turning inconsistent payloads into a stable schema, applying explainable scoring rules, and producing artifacts that can be tested, stored, and reviewed.

## Positioning

This is a portfolio project for backend automation, data processing, and operational reliability practice. It is not a commercial news product and does not scrape private or restricted content.
