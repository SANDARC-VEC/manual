"""
Reading-time hook for MkDocs Material — no external dependencies.

Injects a small "N min read" meta row directly after each page's first
<h1>, wrapped in <div class="page-meta">…</div> (styled in
docs/stylesheets/extra.css). Wired in mkdocs.yml:

    hooks:
      - hooks/reading_time.py

Reading speed assumes ~200 words/min. The Home page (hero landing) is
skipped so the meta row doesn't appear over the hero.
"""

import math
import re

WORDS_PER_MINUTE = 200

# Matches the first closing </h1> tag on the page.
_H1_CLOSE = re.compile(r"</h1>", re.IGNORECASE)
# Strips HTML tags for a rough word count.
_TAGS = re.compile(r"<[^>]+>")

_CLOCK_SVG = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
    'stroke-width="2.2" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
)


def on_page_content(html, page, config, files, **kwargs):
    # Skip the landing/hero page.
    if page.is_homepage or "hero-landing" in html:
        return html

    text = _TAGS.sub(" ", html)
    words = len(text.split())
    if words == 0:
        return html

    minutes = max(1, math.ceil(words / WORDS_PER_MINUTE))
    meta = (
        '<div class="page-meta">'
        f"{_CLOCK_SVG}{minutes} min read"
        "</div>"
    )

    # Insert immediately after the first </h1>. If a page has no H1
    # (shouldn't happen after normalization), leave it untouched.
    return _H1_CLOSE.sub("</h1>\n" + meta, html, count=1)
