from __future__ import annotations

from html import escape
from pathlib import Path

from hn_signal.models import NormalizedStory


def render_html_report(stories: list[NormalizedStory], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(_story_row(story, index + 1) for index, story in enumerate(stories))
    output_path.write_text(_page(rows), encoding="utf-8")


def _story_row(story: NormalizedStory, rank: int) -> str:
    keyword_text = ", ".join(story.keywords) if story.keywords else "general"
    link = story.url or f"https://news.ycombinator.com/item?id={story.id}"
    return f"""
    <article class="story">
      <div class="rank">{rank:02d}</div>
      <div>
        <a href="{escape(link)}" target="_blank" rel="noreferrer">{escape(story.title)}</a>
        <p>{story.points} points · {story.comments} comments · {story.age_hours}h old</p>
        <span>{escape(keyword_text)}</span>
      </div>
      <strong>{story.signal_score}</strong>
    </article>
    """


def _page(rows: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Developer News Signal Pipeline</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
    body {{ margin: 0; background: #070b0f; color: #edf7f3; }}
    main {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; padding: 56px 0; }}
    header {{ display: grid; gap: 14px; margin-bottom: 34px; }}
    .eyebrow {{ color: #62d6a6; font-size: 12px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }}
    h1 {{ margin: 0; max-width: 860px; font-size: clamp(42px, 8vw, 96px); line-height: .92; letter-spacing: 0; }}
    .lede {{ margin: 0; max-width: 720px; color: #a9bbb5; font-size: 18px; line-height: 1.7; }}
    .panel {{ border: 1px solid rgba(255,255,255,.12); background: linear-gradient(145deg, rgba(255,255,255,.08), rgba(255,255,255,.025)); border-radius: 24px; overflow: hidden; box-shadow: 0 30px 90px rgba(0,0,0,.35); }}
    .story {{ display: grid; grid-template-columns: 64px 1fr auto; gap: 18px; align-items: center; padding: 20px; border-bottom: 1px solid rgba(255,255,255,.08); }}
    .story:last-child {{ border-bottom: 0; }}
    .rank {{ color: #e5a93b; font-weight: 800; }}
    a {{ color: #ffffff; font-size: 18px; font-weight: 800; text-decoration: none; }}
    p {{ margin: 7px 0 10px; color: #95a7a1; }}
    span {{ color: #62d6a6; font-size: 13px; }}
    strong {{ color: #e5a93b; font-size: 22px; }}
    @media (max-width: 640px) {{ .story {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">API pipeline · SQLite snapshot · signal scoring</div>
      <h1>Developer news signals, ranked for technical relevance.</h1>
      <p class="lede">A static report generated from normalized Hacker News API records. Scores combine engagement, freshness, comment activity, and backend/devops keyword signals.</p>
    </header>
    <section class="panel">
      {rows}
    </section>
  </main>
</body>
</html>
"""
