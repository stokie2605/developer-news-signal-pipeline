# CLAUDE.md

This file is lightweight project memory for AI-assisted work on Developer News Signal Pipeline.
It is documentation only and does not affect the application runtime.

## 1. Git Workflow

- Main branch: main
- Commit style: short, practical messages that describe the user-facing change.
- Push policy: push only after checks pass or documentation-only changes are reviewed.
- Avoid unrelated cleanup while working on a focused change.

## 2. Project Purpose

Backend data pipeline that collects developer news from the official Hacker News API, normalises story payloads, scores technical relevance, and stores SQLite, JSON, and HTML snapshots.

Primary stack: Python 3.11, typed dataclasses, SQLite, pytest, GitHub Actions.

## 3. Decisions

- Use the official Hacker News API rather than fragile HTML scraping.
- Keep transforms deterministic and testable.
- Store local snapshots in SQLite and export reviewable JSON/HTML reports.
- Keep positioning focused on backend automation, data processing, and CI/CD practice.

## 4. Session Mode

- Read this file and README.md before making non-trivial changes.
- Explain intent before multi-file edits.
- Run the relevant check command where practical: $(System.Collections.Hashtable.Check).
- Keep copy technical, plain, and recruiter-safe.
- Do not introduce secrets, real customer data, or unrelated commercial positioning.

## 5. Current State

### What got done

- Repository is part of the active portfolio set.
- README explains the project purpose and reviewer-facing evidence.
- Project memory has been added so future work starts with context.

### Where things stand

- Current positioning: Backend data pipeline that collects developer news from the official Hacker News API, normalises story payloads, scores technical relevance, and stores SQLite, JSON, and HTML snapshots.
- Review command/context: $(System.Collections.Hashtable.Check).

### Next

- Add richer report filtering or documented sample output if the project continues.

### Blocked on

- Nothing.