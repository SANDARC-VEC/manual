"""
Per-page changelog hook for MkDocs Material — no external dependencies.

Appends a "History" disclosure button to the .page-meta row (created by
hooks/reading_time.py, which must be listed first in mkdocs.yml). The
button expands a popover listing each revision of the page's source file
(following renames) with the ACTUAL text edits, not commit messages:
every entry shows a +added/−removed word count and expands into snippets
of the changed text — removed words struck through, added words
highlighted — parsed from `git log -p --word-diff=porcelain`.

    hooks:
      - hooks/reading_time.py
      - hooks/git_changelog.py

Pages with no git history (untracked files, builds outside a git repo)
are left untouched. Shallow clones — Cloudflare's git-connected builds
clone at depth 1, which would collapse every page's history into a
single "created today" boundary commit — are deepened with
`git fetch --unshallow` on first use; if that fails, the widget is
omitted entirely rather than showing wrong dates. Styled in
docs/stylesheets/extra.css under "Page changelog".
"""

import html as html_mod
import logging
import os
import re
import subprocess
from datetime import datetime

logger = logging.getLogger("mkdocs.hooks.git_changelog")

# Cap the popover at this many revisions so ancient pages stay readable.
MAX_ENTRIES = 30
# Cap the edit snippets shown per revision.
MAX_REGIONS = 8
# Cap a single run of added/removed words inside one snippet.
MAX_RUN_WORDS = 20
# Unchanged words of context shown on each side of an edit.
CTX_WORDS = 3
# Edits separated by no more than this many unchanged words merge into
# one snippet.
GAP_WORDS = 2

# Matches the closing tag of the reading-time meta row so the History
# button lands inside it, and the first </h1> as a fallback anchor.
_META_ROW = re.compile(r'(<div class="page-meta">.*?)(</div>)', re.DOTALL)
_H1_CLOSE = re.compile(r"</h1>", re.IGNORECASE)

_HISTORY_SVG = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" '
    'stroke-width="2.2" aria-hidden="true">'
    '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>'
    '<path d="M12 7v5l3 2"/></svg>'
)

# Commit separator for parsing `git log` output (unlikely in any diff).
_SEP = "\x01"

# Markdown link/image syntax: `[text](url)` — the text is kept, the
# `](url)` part is dropped (leading `[` / `![` handled separately since
# multi-word link text arrives as separate diff tokens).
_LINK_TAIL = re.compile(r"\]\([^)]*\)")
_LINK_OPEN = re.compile(r"^!?\[")
_EMPHASIS = re.compile(r"^[*_`]{1,3}|[*_`]{1,3}$")
_WORDY = re.compile(r"[A-Za-z0-9]")


def _clean_word(word):
    """Strip markdown syntax from a diff token; return "" for tokens that
    are pure syntax (heading markers, list bullets, table pipes, ...) so
    the popover shows only real text changes."""
    word = _LINK_TAIL.sub("", word)
    word = _LINK_OPEN.sub("", word)
    word = _EMPHASIS.sub("", word)
    if not _WORDY.search(word):
        return ""
    return word


# Tri-state, resolved once per build: None = not yet checked, True =
# full history available, False = shallow clone we could not deepen.
_history_ready = None


def _ensure_full_history(cwd):
    """Deepen a shallow clone so page history is real, once per build.

    Cloudflare's git-connected builds clone at depth 1; without this,
    git log shows every page as created in the latest commit. The origin
    remote stays credentialed during those builds, so fetching the rest
    of the history works. Returns False when the repo is still shallow
    (fetch failed) — the caller then omits the History widget instead of
    rendering wrong dates.
    """
    global _history_ready
    if _history_ready is not None:
        return _history_ready

    def _git(*args, timeout):
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    try:
        probe = _git("rev-parse", "--is-shallow-repository", timeout=15)
        if probe.returncode != 0 or probe.stdout.strip() != "true":
            # Full clone, or not a git repo at all (the per-page git log
            # handles that case by returning no revisions).
            _history_ready = True
            return True
        logger.info(
            "Shallow clone detected; fetching full history for the "
            "page History widgets."
        )
        fetch = _git("fetch", "--quiet", "--unshallow", timeout=300)
        if fetch.returncode == 0:
            _history_ready = True
        else:
            logger.warning(
                "git fetch --unshallow failed; omitting the page History "
                f"widgets rather than showing wrong dates. "
                f"{fetch.stderr.strip()}"
            )
            _history_ready = False
    except (OSError, subprocess.TimeoutExpired) as exc:
        logger.warning(
            f"Could not deepen the shallow git clone ({exc}); omitting "
            "the page History widgets."
        )
        _history_ready = False
    return _history_ready


def _git_word_diffs(abs_src_path):
    """Run git log with per-commit word diffs for one file.

    Returns a list of revisions, newest first:
        {"date": "Jul 6, 2026", "created": bool, "renamed": bool,
         "tokens": [("add"|"del"|"ctx", word), ...]}
    or [] on any failure (untracked file, not a git repo, ...).
    """
    try:
        out = subprocess.run(
            [
                "git", "log", "--follow", "-p",
                "--word-diff=porcelain",
                f"--format={_SEP}%as",
                "--", os.path.basename(abs_src_path),
            ],
            cwd=os.path.dirname(abs_src_path),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if out.returncode != 0:
        return []

    revisions = []
    for chunk in out.stdout.split(_SEP):
        lines = chunk.splitlines()
        if not lines:
            continue
        try:
            date = datetime.strptime(lines[0].strip(), "%Y-%m-%d")
        except ValueError:
            continue

        created = False
        renamed = False
        edited = False  # any raw +/- token, even pure-syntax ones
        tokens = []
        in_hunk = False
        for line in lines[1:]:
            if line.startswith("diff --git"):
                in_hunk = False
            elif line.startswith("new file mode"):
                created = True
            elif line.startswith("rename from"):
                renamed = True
            elif line.startswith("@@"):
                in_hunk = True
            elif in_hunk and line[:1] in ("+", "-", " "):
                kind = {"+": "add", "-": "del", " ": "ctx"}[line[0]]
                if kind != "ctx" and line[1:].strip():
                    edited = True
                tokens.extend(
                    (kind, cw)
                    for w in line[1:].split()
                    if (cw := _clean_word(w))
                )
            # "~" newline markers and other metadata lines are ignored;
            # dropping newlines lets edits on adjacent lines merge into
            # one snippet.

        revisions.append({
            "date": f"{date:%b} {date.day}, {date.year}",
            "created": created,
            "renamed": renamed,
            "edited": edited,
            "tokens": tokens,
        })
    return revisions


def _find_regions(tokens):
    """Return (start, end) index spans covering runs of add/del tokens,
    merging edits separated by at most GAP_WORDS unchanged words."""
    regions = []
    i, n = 0, len(tokens)
    while i < n:
        if tokens[i][0] == "ctx":
            i += 1
            continue
        start = end = i
        gap = 0
        j = i + 1
        while j < n:
            if tokens[j][0] == "ctx":
                gap += 1
                if gap > GAP_WORDS:
                    break
            else:
                end = j
                gap = 0
            j += 1
        regions.append((start, end))
        i = end + 1
    return regions


def _render_region(tokens, start, end):
    """Render one edit snippet with CTX_WORDS of context on each side."""
    lead = max(start - CTX_WORDS, 0)
    trail = min(end + CTX_WORDS, len(tokens) - 1)

    # Merge consecutive same-kind tokens into runs.
    runs = []
    for kind, word in tokens[lead:trail + 1]:
        if runs and runs[-1][0] == kind:
            runs[-1][1].append(word)
        else:
            runs.append((kind, [word]))

    parts = []
    for kind, words in runs:
        if kind != "ctx" and len(words) > MAX_RUN_WORDS:
            words = words[:MAX_RUN_WORDS] + ["…"]
        text = html_mod.escape(" ".join(words))
        if kind == "add":
            parts.append(f"<ins>{text}</ins>")
        elif kind == "del":
            parts.append(f"<del>{text}</del>")
        else:
            parts.append(text)

    prefix = "… " if lead > 0 else ""
    suffix = " …" if trail < len(tokens) - 1 else ""
    return (
        '<p class="page-changelog__region">'
        f"{prefix}{' '.join(parts)}{suffix}</p>"
    )


def _render_entry(rev):
    """Render one revision as a list item for the history popover."""
    date = html_mod.escape(rev["date"])
    added = sum(1 for kind, _ in rev["tokens"] if kind == "add")
    removed = sum(1 for kind, _ in rev["tokens"] if kind == "del")

    # First revision of the file: don't dump the whole page as one diff.
    if rev["created"]:
        return (
            '<li class="page-changelog__item page-changelog__item--label">'
            f'<span class="page-changelog__date">{date}</span>'
            '<span class="page-changelog__label">Page created'
            f' <span class="page-changelog__added">+{added} words</span>'
            "</span></li>"
        )

    # Rename-only, formatting-only, or metadata-only commits have no
    # word changes left after syntax filtering.
    if added == 0 and removed == 0:
        if rev["renamed"]:
            label = "Renamed or moved"
        elif rev["edited"]:
            label = "Formatting changes only"
        else:
            label = "No text changes"
        return (
            '<li class="page-changelog__item page-changelog__item--label">'
            f'<span class="page-changelog__date">{date}</span>'
            f'<span class="page-changelog__label">{label}</span></li>'
        )

    regions = _find_regions(rev["tokens"])
    snippets = "".join(
        _render_region(rev["tokens"], s, e)
        for s, e in regions[:MAX_REGIONS]
    )
    if len(regions) > MAX_REGIONS:
        snippets += (
            '<p class="page-changelog__region page-changelog__more">'
            f"…and {len(regions) - MAX_REGIONS} more edits</p>"
        )

    return (
        '<li class="page-changelog__item">'
        '<details class="page-changelog__entry">'
        "<summary>"
        f'<span class="page-changelog__date">{date}</span>'
        '<span class="page-changelog__stats">'
        f'<span class="page-changelog__added">+{added}</span> '
        f'<span class="page-changelog__removed">−{removed}</span>'
        " words</span>"
        '<span class="page-changelog__chev">›</span>'
        "</summary>"
        f'<div class="page-changelog__diff">{snippets}</div>'
        "</details></li>"
    )


def on_page_content(html, page, config, files, **kwargs):
    # Skip the landing/hero page, same as the reading-time hook.
    if page.is_homepage or "hero-landing" in html:
        return html

    if not _ensure_full_history(os.path.dirname(page.file.abs_src_path)):
        return html
    revisions = _git_word_diffs(page.file.abs_src_path)
    if not revisions:
        return html

    shown = revisions[:MAX_ENTRIES]
    items = "".join(_render_entry(rev) for rev in shown)
    if len(revisions) > MAX_ENTRIES:
        items += (
            '<li class="page-changelog__item page-changelog__item--label">'
            '<span class="page-changelog__label page-changelog__more">'
            f"…and {len(revisions) - MAX_ENTRIES} earlier revisions"
            "</span></li>"
        )

    widget = (
        '<details class="page-changelog">'
        f"<summary>{_HISTORY_SVG}History</summary>"
        '<div class="page-changelog__panel">'
        '<div class="page-changelog__title">Page history</div>'
        f"<ol>{items}</ol>"
        "</div></details>"
    )

    # Preferred spot: inside the meta row, after the reading time.
    if _META_ROW.search(html):
        return _META_ROW.sub(
            r'\1<span class="page-meta__dot"></span>' + widget + r"\2",
            html,
            count=1,
        )
    # Fallback: page had no meta row (e.g. no word count) — make one.
    return _H1_CLOSE.sub(
        f'</h1>\n<div class="page-meta">{widget}</div>', html, count=1
    )
