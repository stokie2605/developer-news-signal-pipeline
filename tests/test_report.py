from __future__ import annotations

from pathlib import Path

from hn_signal.models import NormalizedStory
from hn_signal.report import render_html_report


def test_render_html_report_writes_static_dashboard() -> None:
    artifact_dir = Path("test-artifacts")
    artifact_dir.mkdir(exist_ok=True)
    output_path = artifact_dir / "report.html"
    output_path.unlink(missing_ok=True)

    stories = [
        NormalizedStory(
            id=7,
            title="Python monitoring pipeline",
            url="https://example.com/report",
            author="dean",
            points=100,
            comments=25,
            created_at="2026-07-06T12:00:00+00:00",
            age_hours=2.0,
            keywords=["python", "monitoring"],
            signal_score=91.2,
        ),
    ]

    render_html_report(stories, output_path)

    html = output_path.read_text(encoding="utf-8")
    assert "Developer News Signal Pipeline" in html
    assert "Python monitoring pipeline" in html
    assert "91.2" in html
